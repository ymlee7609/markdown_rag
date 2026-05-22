"""RAG 온톨로지 보조 코퍼스 ablation 평가.

두 모드를 같은 검증 데이터셋(100건)에 적용해 직접 비교:

- A (baseline): 기존 chroma_optimized + bm25_index_optimized 만 사용
- B (ontology-union): 위 + data/chroma_ontology + data/bm25_ontology 보조 검색,
                     양쪽 결과를 RRF로 합치고,
                     보조 카드의 frontmatter(documented_in/taught_in/corpus_paths)에서
                     referenced path를 expected_path 매칭에 함께 사용

사용법:
    python scripts/validate_rag_ablation.py
    python scripts/validate_rag_ablation.py --top-k 5 --category ccie

산출물:
    reports/ontology/m3_ablation_<timestamp>.json
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

_PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "src"))

from markdown_rag.config import Settings  # noqa: E402
from markdown_rag.embedding.local import LocalEmbedding  # noqa: E402
from markdown_rag.models import SearchResult  # noqa: E402
from markdown_rag.retriever.bm25 import BM25Index  # noqa: E402
from markdown_rag.retriever.hybrid import HybridSearch  # noqa: E402
from markdown_rag.retriever.search import SemanticSearch  # noqa: E402
from markdown_rag.store.chroma import ChromaStore  # noqa: E402

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Ontology 카드 referenced paths 추출 (한 번만)
# ---------------------------------------------------------------------------


def load_onto_card_refs(onto_dir: Path) -> dict[str, list[str]]:
    """카드 doc_path -> 그 카드가 가리키는 referenced path 리스트.

    Returns:
        {card_relative_path: [doc_path1, doc_path2, ...]} 매핑.
        Frontmatter의 taught_in / documented_in / corpus_paths / manual_paths
        필드에서 추출.
    """
    refs: dict[str, list[str]] = {}
    fields = ("taught_in", "documented_in", "corpus_paths", "manual_paths")
    for md in onto_dir.rglob("*.md"):
        if md.name == "README.md":
            continue
        try:
            content = md.read_text()
            m = re.match(r"^---\n(.*?)\n---\n", content, re.S)
            if not m:
                continue
            fm = yaml.safe_load(m.group(1))
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(fm, dict):
            continue
        collected: list[str] = []
        for f in fields:
            v = fm.get(f)
            if isinstance(v, list):
                collected.extend(str(x) for x in v if x)
        if collected:
            # key는 카드의 절대 경로 문자열 (chunk.doc_path와 비교용)
            refs[str(md)] = collected
            # key 변형: input_ontology 기준 상대 경로도 등록 (인덱싱된 path 형태에 맞춰)
            try:
                rel = str(md.relative_to(_PROJECT_ROOT))
                refs[rel] = collected
            except ValueError:
                pass
    return refs


# ---------------------------------------------------------------------------
# 평가 헬퍼
# ---------------------------------------------------------------------------


def is_onto_card_path(doc_path: str) -> bool:
    return "input_ontology" in doc_path


def check_hit_with_refs(
    results: list[SearchResult],
    expected_path_contains: str | None,
    k: int,
    onto_refs: dict[str, list[str]],
) -> tuple[bool, str]:
    """직접 hit + 보조 카드 referenced path 매칭 둘 다 인정.

    Returns:
        (is_hit, hit_reason)  hit_reason은 "direct" | "via:<card_path>" | ""
    """
    if expected_path_contains is None:
        return (len(results) > 0, "direct" if results else "")
    for r in results[:k]:
        dp = str(r.chunk.doc_path)
        # 1) 직접 hit
        if expected_path_contains in dp:
            return (True, "direct")
        # 2) 보조 카드 hit → referenced path lookup
        if is_onto_card_path(dp):
            for key in (dp, str(Path(dp).relative_to(_PROJECT_ROOT)) if str(dp).startswith(str(_PROJECT_ROOT)) else dp):
                if key in onto_refs:
                    for ref_path in onto_refs[key]:
                        if expected_path_contains in ref_path:
                            return (True, f"via:{Path(dp).name}")
                    break
    return (False, "")


def check_keyword_match(
    results: list[SearchResult],
    expected_keywords: list[str],
    k: int = 3,
) -> bool:
    if not expected_keywords:
        return True
    for r in results[:k]:
        text = (r.chunk.content or "").lower()
        if all(kw.lower() in text for kw in expected_keywords):
            return True
    return False


def compute_mrr_with_refs(
    results: list[SearchResult],
    expected_path_contains: str | None,
    onto_refs: dict[str, list[str]],
) -> float:
    if expected_path_contains is None:
        return 1.0 if results else 0.0
    for idx, r in enumerate(results, start=1):
        dp = str(r.chunk.doc_path)
        if expected_path_contains in dp:
            return 1.0 / idx
        if is_onto_card_path(dp):
            for key in (dp,):
                if key in onto_refs:
                    for ref_path in onto_refs[key]:
                        if expected_path_contains in ref_path:
                            return 1.0 / idx
                    break
    return 0.0


# ---------------------------------------------------------------------------
# Union (RRF) — 두 엔진 결과 결합
# ---------------------------------------------------------------------------


def rrf_union(
    main_results: list[SearchResult],
    onto_results: list[SearchResult],
    top_k: int,
    k_const: int = 60,
) -> list[SearchResult]:
    """두 결과 리스트를 RRF로 결합. 점수만 갱신하고 SearchResult.chunk는 보존."""
    scored: dict[str, tuple[SearchResult, float]] = {}
    for rank, r in enumerate(main_results, start=1):
        key = str(r.chunk.doc_path) + "::" + str(getattr(r.chunk, "chunk_index", 0))
        score = 1.0 / (k_const + rank)
        if key not in scored or scored[key][1] < score:
            scored[key] = (r, score)
    for rank, r in enumerate(onto_results, start=1):
        key = str(r.chunk.doc_path) + "::" + str(getattr(r.chunk, "chunk_index", 0))
        score = 1.0 / (k_const + rank)
        if key in scored:
            scored[key] = (scored[key][0], scored[key][1] + score)
        else:
            scored[key] = (r, score)
    ranked = sorted(scored.values(), key=lambda x: -x[1])
    return [r for r, _ in ranked[:top_k]]


# ---------------------------------------------------------------------------
# 검색 엔진 빌더
# ---------------------------------------------------------------------------


def build_hybrid(
    chroma_path: Path,
    collection: str,
    bm25_path: Path,
    alpha: float,
    top_k: int,
) -> HybridSearch:
    embedding = LocalEmbedding(model_name=Settings().local_model)
    store = ChromaStore(persist_path=chroma_path, collection_name=collection)
    semantic = SemanticSearch(embedding_backend=embedding, vector_store=store, top_k=top_k * 3)
    bm25 = BM25Index.load(bm25_path)
    return HybridSearch(semantic_search=semantic, bm25_index=bm25, alpha=alpha)


# ---------------------------------------------------------------------------
# 평가
# ---------------------------------------------------------------------------


def evaluate_mode(
    test_cases: list[dict[str, Any]],
    engine_main: HybridSearch,
    engine_onto: HybridSearch | None,
    onto_refs: dict[str, list[str]],
    top_k: int,
    fetch_k: int,
    mode_name: str,
) -> dict[str, Any]:
    per_case: list[dict[str, Any]] = []
    for tc in test_cases:
        t0 = time.time()
        main = engine_main.search(tc["query"], top_k=fetch_k)
        if engine_onto is not None:
            onto = engine_onto.search(tc["query"], top_k=fetch_k)
            results = rrf_union(main, onto, top_k=fetch_k)
        else:
            results = main
        elapsed = (time.time() - t0) * 1000
        expected_path = tc.get("expected_path_contains")
        expected_keywords = tc.get("expected_keywords", [])
        hit1, _ = check_hit_with_refs(results, expected_path, 1, onto_refs)
        hit3, _ = check_hit_with_refs(results, expected_path, 3, onto_refs)
        hit5, r5 = check_hit_with_refs(results, expected_path, 5, onto_refs)
        kw = check_keyword_match(results, expected_keywords, k=3)
        mrr = compute_mrr_with_refs(results, expected_path, onto_refs)
        passed = hit5 and kw
        per_case.append({
            "id": tc["id"], "category": tc["category"], "query": tc["query"],
            "passed": passed, "hit_at_1": hit1, "hit_at_3": hit3, "hit_at_5": hit5,
            "keyword_match": kw, "mrr": mrr, "elapsed_ms": elapsed,
            "hit_reason_5": r5,
            "top_paths": [str(r.chunk.doc_path) for r in results[:top_k]],
        })
    return aggregate(per_case, mode_name)


def aggregate(per_case: list[dict[str, Any]], mode_name: str) -> dict[str, Any]:
    def stats(cases: list[dict[str, Any]]) -> dict[str, Any]:
        n = len(cases) or 1
        return {
            "total": len(cases),
            "passed": sum(1 for c in cases if c["passed"]),
            "hit_at_1": sum(1 for c in cases if c["hit_at_1"]),
            "hit_at_3": sum(1 for c in cases if c["hit_at_3"]),
            "hit_at_5": sum(1 for c in cases if c["hit_at_5"]),
            "keyword_match": sum(1 for c in cases if c["keyword_match"]),
            "avg_mrr": round(sum(c["mrr"] for c in cases) / n, 4),
            "avg_elapsed_ms": round(sum(c["elapsed_ms"] for c in cases) / n, 1),
            "via_onto_count": sum(1 for c in cases if str(c.get("hit_reason_5","")).startswith("via:")),
        }
    by_cat: dict[str, dict[str, Any]] = {}
    for cat in ("rfc", "ccie", "ko", "edge"):
        cases = [c for c in per_case if c["category"] == cat]
        if cases:
            by_cat[cat] = stats(cases)
    return {
        "mode": mode_name,
        "overall": stats(per_case),
        "by_category": by_cat,
        "per_case": per_case,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG ontology ablation")
    parser.add_argument("--dataset", type=Path,
                        default=_PROJECT_ROOT / "scripts/validation_dataset.json")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--category",
                        choices=["rfc", "ccie", "ko", "edge", "all"], default="all")
    parser.add_argument("--alpha", type=float, default=0.7,
                        help="hybrid alpha (default 0.7, baseline 매개변수와 일치)")
    parser.add_argument("--main-chroma", default="data/chroma_optimized")
    parser.add_argument("--main-collection", default="markdown_docs_optimized")
    parser.add_argument("--main-bm25", default="data/bm25_index_optimized")
    parser.add_argument("--onto-chroma", default="data/chroma_ontology")
    parser.add_argument("--onto-collection", default="markdown_docs_ontology")
    parser.add_argument("--onto-bm25", default="data/bm25_ontology")
    parser.add_argument("--onto-dir", default="input_ontology")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    os.chdir(_PROJECT_ROOT)

    with args.dataset.open() as f:
        test_cases = json.load(f)["test_cases"]
    if args.category != "all":
        test_cases = [tc for tc in test_cases if tc["category"] == args.category]
    print(f"평가 대상: {len(test_cases)}건 (category={args.category}), top_k={args.top_k}")

    onto_refs = load_onto_card_refs(Path(args.onto_dir).resolve())
    print(f"보조 카드 참조 path 수집: {len(onto_refs)}개 카드 키")

    fetch_k = args.top_k * 3

    print("\n[mode A] baseline 엔진 빌드 중...")
    engine_main = build_hybrid(
        Path(args.main_chroma), args.main_collection, Path(args.main_bm25),
        alpha=args.alpha, top_k=args.top_k,
    )
    print("[mode A] 평가 시작...")
    t0 = time.time()
    result_a = evaluate_mode(test_cases, engine_main, None, onto_refs,
                              args.top_k, fetch_k, "A (baseline)")
    print(f"[mode A] 완료 ({time.time()-t0:.1f}s)")

    print("\n[mode B] ontology 엔진 빌드 중...")
    engine_onto = build_hybrid(
        Path(args.onto_chroma), args.onto_collection, Path(args.onto_bm25),
        alpha=args.alpha, top_k=args.top_k,
    )
    print("[mode B] 평가 시작...")
    t0 = time.time()
    result_b = evaluate_mode(test_cases, engine_main, engine_onto, onto_refs,
                              args.top_k, fetch_k, "B (baseline + ontology union)")
    print(f"[mode B] 완료 ({time.time()-t0:.1f}s)")

    # 비교 출력
    print("\n" + "=" * 70)
    print(f"{'metric':25s} {'A baseline':>15s} {'B +ontology':>15s} {'delta':>10s}")
    print("-" * 70)
    for k in ("passed", "hit_at_1", "hit_at_3", "hit_at_5", "keyword_match"):
        va, vb = result_a["overall"][k], result_b["overall"][k]
        print(f"{k:25s} {va:>15d} {vb:>15d} {vb-va:>+10d}")
    for k in ("avg_mrr",):
        va, vb = result_a["overall"][k], result_b["overall"][k]
        print(f"{k:25s} {va:>15.4f} {vb:>15.4f} {vb-va:>+10.4f}")
    print(f"{'via_onto (hit@5)':25s} {'-':>15s} {result_b['overall']['via_onto_count']:>15d} {'-':>10s}")

    print("\n--- 카테고리별 hit@5 ---")
    for cat in ("rfc", "ccie", "ko", "edge"):
        if cat in result_a["by_category"]:
            va = result_a["by_category"][cat]["hit_at_5"]
            vb = result_b["by_category"][cat]["hit_at_5"]
            tot = result_a["by_category"][cat]["total"]
            print(f"  {cat:5s} {va:>3d}/{tot} → {vb:>3d}/{tot}  (delta {vb-va:+d})")

    # 저장
    if args.output:
        out = args.output
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = _PROJECT_ROOT / f"reports/ontology/m3_ablation_{ts}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_at": datetime.now().isoformat(),
        "dataset": str(args.dataset),
        "top_k": args.top_k,
        "alpha": args.alpha,
        "category": args.category,
        "mode_a": result_a,
        "mode_b": result_b,
    }
    with out.open("w") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"\n결과 저장: {out}")


if __name__ == "__main__":
    main()
