"""M4 Stage 1 — 결정론적 onto_*_ids 후보 추출.

main corpus (input_optimized → data/chroma_optimized)의 모든 청크에 대해
정규식 + alias_dictionary 사전 매칭으로 다음 onto 메타데이터 후보를 부여한다:

- onto_rfc_refs       : 본문의 RFC 번호 (정규식)
- onto_protocol_ids   : alias_dictionary.protocols 매칭
- onto_concept_ids    : alias_dictionary.concepts 매칭 (require_context_tokens 적용)
- onto_feature_ids    : alias_dictionary.features 매칭
- onto_vendor         : doc_path prefix 매칭 (다산/유비쿼스/cisco)
- onto_device_models  : 파일명 [V***]/[E***]/U*** 패턴 매칭
- onto_corpus_tier    : standard(RFC) / theory(CCIE) / implementation(가입자망)
- onto_card_alias_of  : 청크 자체가 보조 카드인 경우의 canonical id

출력: data/ontology/chunk_enrichment.jsonl.gz
  한 줄에 하나의 청크: {chunk_id, doc_path, chunk_index, onto_*}

이 파일은 후속 단계 (LLM Stage 2 검증, Chroma metadata patch, ablation 통계)
에서 입력으로 사용된다.

사용법:
    python scripts/extract_onto_candidates.py             # 전체 (50만 chunk, 시간 소요)
    python scripts/extract_onto_candidates.py --limit 5000  # 일부만 (sanity check)
    python scripts/extract_onto_candidates.py --out custom.jsonl.gz
"""

from __future__ import annotations

import argparse
import gzip
import json
import logging
import re
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml

_PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "src"))

from markdown_rag.config import Settings  # noqa: E402
from markdown_rag.store.chroma import ChromaStore  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("extract_onto")


# ---------------------------------------------------------------------------
# Alias dictionary loader
# ---------------------------------------------------------------------------


def load_alias_dict(path: Path) -> dict:
    """alias_dictionary.yaml 로드 + 매칭용 사전 구조 빌드."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))

    # canonical_id -> {"aliases": set[str], "ko_aliases": set[str],
    #                  "requires_context": list[str]}
    entries: dict[str, dict] = {}
    for section in ("protocols", "concepts", "features", "vendors", "standards"):
        for cid, info in (raw.get(section) or {}).items():
            aliases: set[str] = set()
            if info.get("canonical"):
                aliases.add(str(info["canonical"]))
            aliases.update(str(a) for a in info.get("aliases", []) if a)
            ko = {str(a) for a in info.get("ko_aliases", []) if a}
            entries[cid] = {
                "section": section,
                "aliases": aliases,
                "ko_aliases": ko,
                "requires_context": list(info.get("requires_context", [])),
            }

    match_policy = raw.get("match_policy", {})
    min_len = int(match_policy.get("min_token_length", 3))
    require_context_tokens = match_policy.get("require_context_tokens", {})

    return {
        "entries": entries,
        "min_token_length": min_len,
        "require_context_tokens": require_context_tokens,
    }


# ---------------------------------------------------------------------------
# Path-derived signals (deterministic, no body scan)
# ---------------------------------------------------------------------------


_RE_DEVICE_MODEL = re.compile(r"\b(V\d{3,4}[A-Z]{0,3}|E\d{3,4}[A-Z]?|U\d{3,4}[A-Z]?|P\d{3,4})\b")
_RE_RFC_NUMBER = re.compile(r"\bRFC\s*0*(\d{1,5})\b", re.IGNORECASE)


def classify_corpus_tier(doc_path: str) -> str:
    if "IETF_RFC" in doc_path:
        return "standard"
    if "Cisco_CCIE" in doc_path:
        return "theory"
    if "가입자망장비_manual" in doc_path:
        return "implementation"
    if "input_ontology" in doc_path:
        return "ontology"
    return "other"


def derive_vendor(doc_path: str) -> str | None:
    if "다산_" in doc_path:
        return "vendor:dasan"
    if "유비쿼스_" in doc_path:
        return "vendor:ubiquoss"
    if "Cisco_CCIE" in doc_path:
        return "vendor:cisco"
    return None


def derive_device_models(doc_path: str) -> list[str]:
    """파일명에서 모델 식별자 추출 → vendor 기준 모델 ID 생성."""
    fname = Path(doc_path).name
    found = _RE_DEVICE_MODEL.findall(fname)
    if not found:
        return []
    vendor = derive_vendor(doc_path)
    prefix = ""
    if vendor == "vendor:dasan":
        prefix = "model:dasan-"
    elif vendor == "vendor:ubiquoss":
        prefix = "model:ubiquoss-"
    else:
        return []
    # dedup + lowercase model id
    return list({f"{prefix}{m.lower()}" for m in found})


# ---------------------------------------------------------------------------
# Body scan matchers
# ---------------------------------------------------------------------------


def find_rfc_refs(text: str) -> list[str]:
    """RFC NNNN 인용 추출 → 'rfc:NNNN' ID로 정규화."""
    nums = {int(m.group(1)) for m in _RE_RFC_NUMBER.finditer(text)}
    return sorted(f"rfc:{n}" for n in nums)


def find_alias_matches(
    text: str,
    alias_dict: dict,
    target_sections: tuple[str, ...],
) -> list[str]:
    """alias_dictionary entries 중 target_sections에 속한 것의 alias가
    text에 등장하면 canonical id 반환.

    require_context_tokens가 있으면 그 토큰 중 하나가 동반 등장해야 인정.
    """
    text_lower = text.lower()
    min_len = alias_dict["min_token_length"]
    context_tokens = alias_dict["require_context_tokens"]
    hits: set[str] = set()
    for cid, info in alias_dict["entries"].items():
        if info["section"] not in target_sections:
            continue
        all_aliases = list(info["aliases"]) + list(info["ko_aliases"])
        matched_alias = None
        for a in all_aliases:
            if not a or len(a) < min_len:
                # 매칭 정책상 짧은 토큰은 require_context_tokens에 등록된 것만 허용
                if a in context_tokens:
                    pass  # 이어서 검사
                else:
                    continue
            # case-insensitive substring (한국어는 lower-eq 동일)
            if a.lower() in text_lower:
                # 짧은 토큰은 동반 키워드 필요
                if a in context_tokens:
                    ctx_keys = [t.lower() for t in context_tokens[a]]
                    if not any(ck in text_lower for ck in ctx_keys):
                        continue
                # 카드별 require_context도 적용
                req = [t.lower() for t in info.get("requires_context", [])]
                if req and not any(rk in text_lower for rk in req):
                    continue
                matched_alias = a
                break
        if matched_alias:
            hits.add(cid)
    return sorted(hits)


# ---------------------------------------------------------------------------
# Page-by-page chunk iterator from ChromaStore
# ---------------------------------------------------------------------------


def iter_chunks(store: ChromaStore, batch: int = 5000, limit: int | None = None):
    """전체 collection을 batch 단위로 페이지네이션."""
    total = store.count()
    if limit is not None:
        total = min(total, limit)
    offset = 0
    while offset < total:
        n = min(batch, total - offset)
        try:
            page = store._collection.get(  # noqa: SLF001
                include=["documents", "metadatas"],
                limit=n,
                offset=offset,
            )
        except Exception as e:  # noqa: BLE001
            logger.warning("get(limit=%d, offset=%d) failed: %s — stopping", n, offset, e)
            return
        ids = page.get("ids") or []
        docs = page.get("documents") or []
        metas = page.get("metadatas") or []
        if not ids:
            return
        for i, _id in enumerate(ids):
            yield _id, (docs[i] if i < len(docs) else "") or "", (metas[i] if i < len(metas) else {}) or {}
        offset += len(ids)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="M4 Stage 1 deterministic onto-id extraction")
    parser.add_argument("--alias-dict",
                        default="input_ontology/schema/alias_dictionary.yaml")
    parser.add_argument("--chroma-path", default="data/chroma_optimized")
    parser.add_argument("--collection", default="markdown_docs_optimized")
    parser.add_argument("--out", default="data/ontology/chunk_enrichment.jsonl.gz",
                        help="출력 jsonl.gz 경로")
    parser.add_argument("--batch", type=int, default=5000,
                        help="ChromaStore 페이지네이션 batch (기본 5000)")
    parser.add_argument("--limit", type=int, default=None,
                        help="처리할 최대 chunk 수 (sanity check용)")
    parser.add_argument("--progress-every", type=int, default=10000)
    args = parser.parse_args()

    project_root = _PROJECT_ROOT
    alias_path = (project_root / args.alias_dict).resolve()
    alias_dict = load_alias_dict(alias_path)
    logger.info("alias dict loaded: %d entries", len(alias_dict["entries"]))

    settings = Settings()  # only for local_model etc.; not used directly here
    _ = settings
    store = ChromaStore(
        persist_path=Path(args.chroma_path).resolve(),
        collection_name=args.collection,
    )
    total = store.count()
    if args.limit:
        total = min(total, args.limit)
    logger.info("processing %d chunks (collection=%s)", total, args.collection)

    out_path = (project_root / args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    written = 0
    t0 = time.time()
    stat_proto = Counter()
    stat_concept = Counter()
    stat_feat = Counter()
    stat_tier = Counter()
    stat_vendor = Counter()
    has_any_onto = 0

    with gzip.open(out_path, "wt", encoding="utf-8") as fh:
        for chunk_id, content, meta in iter_chunks(store, batch=args.batch, limit=args.limit):
            raw_dp = meta.get("doc_path", "")
            doc_path = raw_dp if isinstance(raw_dp, str) else str(raw_dp)
            raw_idx = meta.get("chunk_index", 0)
            try:
                chunk_index = int(raw_idx) if isinstance(raw_idx, (int, float, str)) else 0
            except (TypeError, ValueError):
                chunk_index = 0
            tier = classify_corpus_tier(doc_path)
            vendor = derive_vendor(doc_path)
            device_models = derive_device_models(doc_path)
            rfc_refs = find_rfc_refs(content)
            protocol_ids = find_alias_matches(content, alias_dict, ("protocols",))
            concept_ids = find_alias_matches(content, alias_dict, ("concepts",))
            feature_ids = find_alias_matches(content, alias_dict, ("features",))

            stat_tier[tier] += 1
            if vendor:
                stat_vendor[vendor] += 1
            for p in protocol_ids: stat_proto[p] += 1
            for c in concept_ids: stat_concept[c] += 1
            for f in feature_ids: stat_feat[f] += 1
            if protocol_ids or concept_ids or feature_ids or rfc_refs or device_models:
                has_any_onto += 1

            record = {
                "chunk_id": chunk_id,
                "doc_path": doc_path,
                "chunk_index": chunk_index,
                "onto_corpus_tier": tier,
                "onto_vendor": vendor,
                "onto_device_models": device_models,
                "onto_rfc_refs": rfc_refs,
                "onto_protocol_ids": protocol_ids,
                "onto_concept_ids": concept_ids,
                "onto_feature_ids": feature_ids,
            }
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1
            if written % args.progress_every == 0:
                elapsed = time.time() - t0
                rate = written / elapsed if elapsed > 0 else 0
                eta = (total - written) / rate if rate > 0 else 0
                logger.info("written %d/%d (%.1f%%) rate=%.0f/s eta=%.1fs",
                            written, total, written * 100 / total, rate, eta)

    elapsed = time.time() - t0
    logger.info("done: %d chunks in %.1fs (%.0f/s)", written, elapsed, written / max(elapsed, 1e-9))

    # Stats summary
    print("\n" + "=" * 60)
    print(f"OUTPUT: {out_path}")
    print(f"WRITTEN: {written} chunks")
    print(f"WITH ANY ONTO TAG: {has_any_onto} ({has_any_onto*100/max(written,1):.1f}%)")
    print()
    print("Corpus tier distribution:")
    for t, n in stat_tier.most_common():
        print(f"  {t:14s} {n:>8d} ({n*100/max(written,1):.1f}%)")
    print()
    print("Vendor distribution (non-null):")
    for v, n in stat_vendor.most_common():
        print(f"  {v:20s} {n:>8d}")
    print()
    print(f"Top 15 protocol matches (of {len(stat_proto)} distinct):")
    for pid, n in stat_proto.most_common(15):
        print(f"  {pid:25s} {n:>8d}")
    print()
    print(f"Top 10 concept matches (of {len(stat_concept)} distinct):")
    for cid, n in stat_concept.most_common(10):
        print(f"  {cid:25s} {n:>8d}")
    print()
    print(f"Feature matches (of {len(stat_feat)} distinct):")
    for fid, n in stat_feat.most_common():
        print(f"  {fid:25s} {n:>8d}")

    # Save sidecar stats json
    stats_path = out_path.with_suffix(".stats.json")
    stats_path.write_text(json.dumps({
        "generated_at": datetime.now().isoformat(),
        "input_chroma_path": args.chroma_path,
        "input_collection": args.collection,
        "alias_dict_path": str(alias_path),
        "limit": args.limit,
        "total_chunks": written,
        "chunks_with_any_onto": has_any_onto,
        "elapsed_seconds": round(elapsed, 1),
        "corpus_tier_counts": dict(stat_tier),
        "vendor_counts": dict(stat_vendor),
        "protocol_match_counts": dict(stat_proto),
        "concept_match_counts": dict(stat_concept),
        "feature_match_counts": dict(stat_feat),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSTATS: {stats_path}")


if __name__ == "__main__":
    main()
