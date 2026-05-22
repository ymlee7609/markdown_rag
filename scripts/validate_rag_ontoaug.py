"""OntologyAugmentedSearch 정식 클래스 검증.

scripts/validate_rag_ablation.py와 같은 100건 셋을 사용하되,
OntologyAugmentedSearch (src/markdown_rag/retriever/ontology_aug.py)를
운영용으로 호출해 동일한 효과(Hit@5 ≈ 100/100)를 재현하는지 확인한다.

평가 정책:
- 직접 hit (chunk.doc_path가 expected_path_contains 포함)
- 보조 카드 hit (referenced_paths_injectable / directory_hints 매칭)
- 주입된 청크(injected_by_onto_card)는 그 자체로 직접 hit으로 평가

사용법:
    python scripts/build_ontology_refs.py
    python scripts/validate_rag_ontoaug.py
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "src"))

from markdown_rag.config import Settings  # noqa: E402
from markdown_rag.embedding.local import LocalEmbedding  # noqa: E402
from markdown_rag.models import SearchResult  # noqa: E402
from markdown_rag.retriever.bm25 import BM25Index  # noqa: E402
from markdown_rag.retriever.hybrid import HybridSearch  # noqa: E402
from markdown_rag.retriever.ontology_aug import OntologyAugmentedSearch  # noqa: E402
from markdown_rag.retriever.search import SemanticSearch  # noqa: E402
from markdown_rag.store.chroma import ChromaStore  # noqa: E402

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def build_hybrid(
    chroma_path: Path, collection: str, bm25_path: Path,
    alpha: float, top_k: int,
) -> tuple[HybridSearch, ChromaStore]:
    embedding = LocalEmbedding(model_name=Settings().local_model)
    store = ChromaStore(persist_path=chroma_path, collection_name=collection)
    semantic = SemanticSearch(
        embedding_backend=embedding, vector_store=store, top_k=top_k * 3,
    )
    bm25 = BM25Index.load(bm25_path)
    engine = HybridSearch(semantic_search=semantic, bm25_index=bm25, alpha=alpha)
    return engine, store


def is_hit(
    results: list[SearchResult],
    expected_path: str | None,
    k: int,
) -> tuple[bool, str]:
    """직접 hit 또는 보조 카드 referenced_paths 매칭으로 hit 인정."""
    if expected_path is None:
        return (len(results) > 0, "direct" if results else "")
    for r in results[:k]:
        dp = str(r.chunk.doc_path)
        meta = r.chunk.metadata or {}
        # 1) 직접 hit
        if expected_path in dp:
            via_card = meta.get("injected_by_onto_card")
            if via_card:
                return (True, f"injected_via:{via_card}")
            return (True, "direct")
        # 2) 보조 카드 hit (annotated)
        if meta.get("via_onto_card"):
            for p in meta.get("referenced_paths_injectable", []):
                if expected_path in p:
                    return (True, f"via:{Path(dp).name}")
            for p in meta.get("referenced_paths_directories", []):
                if expected_path in p:
                    return (True, f"via_dir:{Path(dp).name}")
    return (False, "")


def keyword_match(results: list[SearchResult], expected_keywords: list[str], k: int = 3) -> bool:
    if not expected_keywords:
        return True
    for r in results[:k]:
        text = (r.chunk.content or "").lower()
        if all(kw.lower() in text for kw in expected_keywords):
            return True
    return False


def mrr(results: list[SearchResult], expected_path: str | None) -> float:
    if expected_path is None:
        return 1.0 if results else 0.0
    for idx, r in enumerate(results, start=1):
        ok, _ = is_hit([r], expected_path, 1)
        if ok:
            return 1.0 / idx
    return 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="OntologyAugmentedSearch 검증")
    parser.add_argument("--dataset", type=Path,
                        default=_PROJECT_ROOT / "scripts/validation_dataset.json")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=0.7)
    parser.add_argument("--main-chroma", default="data/chroma_optimized")
    parser.add_argument("--main-collection", default="markdown_docs_optimized")
    parser.add_argument("--main-bm25", default="data/bm25_index_optimized")
    parser.add_argument("--onto-chroma", default="data/chroma_ontology")
    parser.add_argument("--onto-collection", default="markdown_docs_ontology")
    parser.add_argument("--onto-bm25", default="data/bm25_ontology")
    parser.add_argument("--onto-refs", default="data/ontology/onto_refs.json")
    parser.add_argument("--inject-top-n-cards", type=int, default=3)
    parser.add_argument("--inject-chunks-per-card", type=int, default=1)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    os.chdir(_PROJECT_ROOT)

    with args.dataset.open() as f:
        test_cases = json.load(f)["test_cases"]
    print(f"평가 대상: {len(test_cases)}건, top_k={args.top_k}")

    print("[main] 엔진 빌드 중...")
    main_engine, main_store = build_hybrid(
        Path(args.main_chroma), args.main_collection, Path(args.main_bm25),
        alpha=args.alpha, top_k=args.top_k,
    )
    print("[onto] 엔진 빌드 중...")
    onto_engine, _ = build_hybrid(
        Path(args.onto_chroma), args.onto_collection, Path(args.onto_bm25),
        alpha=args.alpha, top_k=args.top_k,
    )
    print(f"[ontoaug] 통합 검색 객체 빌드 (onto_refs={args.onto_refs})")
    augmented = OntologyAugmentedSearch(
        main_search=main_engine,
        onto_search=onto_engine,
        main_store=main_store,
        onto_refs_path=Path(args.onto_refs),
        inject_top_n_cards=args.inject_top_n_cards,
        inject_chunks_per_card=args.inject_chunks_per_card,
    )

    per_case: list[dict[str, Any]] = []
    t_total = time.time()
    for tc in test_cases:
        t0 = time.time()
        results = augmented.search(tc["query"], top_k=args.top_k)
        elapsed = (time.time() - t0) * 1000
        ep = tc.get("expected_path_contains")
        kws = tc.get("expected_keywords", [])
        h1, _ = is_hit(results, ep, 1)
        h3, _ = is_hit(results, ep, 3)
        h5, reason = is_hit(results, ep, 5)
        km = keyword_match(results, kws, k=3)
        m = mrr(results, ep)
        per_case.append({
            "id": tc["id"], "category": tc["category"], "query": tc["query"],
            "passed": h5 and km, "hit_at_1": h1, "hit_at_3": h3, "hit_at_5": h5,
            "keyword_match": km, "mrr": m, "elapsed_ms": elapsed,
            "hit_reason_5": reason,
            "origins": [(r.chunk.metadata or {}).get(
                "injected_by_onto_card") or (
                "onto_card" if (r.chunk.metadata or {}).get("via_onto_card") else "main"
            ) for r in results[: args.top_k]],
        })
    t_eval = time.time() - t_total

    by_cat: dict[str, dict[str, Any]] = defaultdict(lambda: defaultdict(int))
    for c in per_case:
        cat = c["category"]
        by_cat[cat]["total"] += 1
        for k in ("passed", "hit_at_1", "hit_at_3", "hit_at_5", "keyword_match"):
            if c[k]:
                by_cat[cat][k] += 1
    overall = {
        "total": len(per_case),
        "passed": sum(1 for c in per_case if c["passed"]),
        "hit_at_1": sum(1 for c in per_case if c["hit_at_1"]),
        "hit_at_3": sum(1 for c in per_case if c["hit_at_3"]),
        "hit_at_5": sum(1 for c in per_case if c["hit_at_5"]),
        "keyword_match": sum(1 for c in per_case if c["keyword_match"]),
        "avg_mrr": round(sum(c["mrr"] for c in per_case) / max(len(per_case),1), 4),
        "avg_elapsed_ms": round(sum(c["elapsed_ms"] for c in per_case) / max(len(per_case),1), 1),
        "via_onto_hits": sum(1 for c in per_case
                              if str(c["hit_reason_5"]).startswith(("via:", "via_dir:", "injected_via:"))),
        "direct_hits": sum(1 for c in per_case if c["hit_reason_5"] == "direct"),
    }
    print(f"\n평가 완료: {t_eval:.1f}s ({t_eval/len(per_case):.2f}s/건)")
    print("\n" + "=" * 60)
    print(f"  overall passed       {overall['passed']:>3d}/100")
    print(f"  hit_at_1             {overall['hit_at_1']:>3d}/100")
    print(f"  hit_at_3             {overall['hit_at_3']:>3d}/100")
    print(f"  hit_at_5             {overall['hit_at_5']:>3d}/100")
    print(f"  keyword_match        {overall['keyword_match']:>3d}/100")
    print(f"  avg_mrr              {overall['avg_mrr']:>3.4f}")
    print(f"  direct hits          {overall['direct_hits']:>3d}")
    print(f"  via_onto hits        {overall['via_onto_hits']:>3d}  (annotated/injected)")
    print(f"  avg_elapsed_ms       {overall['avg_elapsed_ms']:>5.1f}")
    print("\n--- 카테고리별 hit@5 ---")
    for cat in ("rfc", "ccie", "ko", "edge"):
        if cat in by_cat:
            v = by_cat[cat]
            print(f"  {cat:5s}  {v['hit_at_5']}/{v['total']}")

    if args.output:
        out = args.output
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = _PROJECT_ROOT / f"reports/ontology/m3c_ontoaug_{ts}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "run_at": datetime.now().isoformat(),
        "top_k": args.top_k, "alpha": args.alpha,
        "inject_top_n_cards": args.inject_top_n_cards,
        "inject_chunks_per_card": args.inject_chunks_per_card,
        "overall": overall,
        "by_category": {cat: dict(v) for cat, v in by_cat.items()},
        "per_case": per_case,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n결과 저장: {out}")


if __name__ == "__main__":
    main()
