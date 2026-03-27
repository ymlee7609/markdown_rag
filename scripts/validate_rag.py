"""RAG 기능 검증 스크립트.

100개의 테스트 케이스로 검색 품질을 평가합니다.
Hit@1, Hit@3, Hit@5, Keyword Match, MRR 지표를 측정합니다.

사용법:
    python scripts/validate_rag.py
    python scripts/validate_rag.py --top-k 5 --category rfc
    python scripts/validate_rag.py --output results.json
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# 프로젝트 루트를 sys.path에 추가
_PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "src"))

from markdown_rag.config import Settings
from markdown_rag.embedding.local import LocalEmbedding
from markdown_rag.models import SearchResult
from markdown_rag.retriever.search import SemanticSearch
from markdown_rag.store.chroma import ChromaStore

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 데이터 로드
# ---------------------------------------------------------------------------


def load_dataset(dataset_path: Path) -> list[dict[str, Any]]:
    """검증 데이터셋 JSON 파일을 로드합니다."""
    with dataset_path.open(encoding="utf-8") as f:
        data = json.load(f)
    return data["test_cases"]


# ---------------------------------------------------------------------------
# 평가 로직
# ---------------------------------------------------------------------------


def check_hit(
    results: list[SearchResult],
    expected_path_contains: str | None,
    k: int,
) -> bool:
    """상위 k개 결과 중 expected_path_contains를 포함하는 경로가 있는지 확인합니다."""
    if expected_path_contains is None:
        # EDGE 케이스: 경로 조건 없음 → 결과가 1개 이상이면 Hit
        return len(results) > 0

    for result in results[:k]:
        doc_path_str = str(result.chunk.doc_path)
        if expected_path_contains in doc_path_str:
            return True
    return False


def check_keyword_match(
    results: list[SearchResult],
    expected_keywords: list[str],
    k: int = 3,
) -> bool:
    """상위 k개 결과의 content + headers + path에 키워드가 하나 이상 포함되는지 확인합니다."""
    if not expected_keywords:
        return True

    for result in results[:k]:
        text_to_search = (
            result.chunk.content
            + " "
            + " ".join(result.chunk.headers)
            + " "
            + str(result.chunk.doc_path)
        ).lower()

        for keyword in expected_keywords:
            if keyword.lower() in text_to_search:
                return True
    return False


def compute_mrr(results: list[SearchResult], expected_path_contains: str | None) -> float:
    """MRR(Mean Reciprocal Rank)를 계산합니다."""
    if expected_path_contains is None:
        return 1.0 if results else 0.0

    for i, result in enumerate(results, start=1):
        if expected_path_contains in str(result.chunk.doc_path):
            return 1.0 / i
    return 0.0


def evaluate_single(
    search_engine: SemanticSearch,
    test_case: dict[str, Any],
    top_k: int,
) -> dict[str, Any]:
    """단일 테스트 케이스를 평가합니다."""
    query = test_case["query"]
    expected_path = test_case.get("expected_path_contains")
    expected_keywords = test_case.get("expected_keywords", [])

    start_time = time.time()
    results = search_engine.search(query, top_k=top_k)
    elapsed_ms = (time.time() - start_time) * 1000

    hit_at_1 = check_hit(results, expected_path, k=1)
    hit_at_3 = check_hit(results, expected_path, k=3)
    hit_at_5 = check_hit(results, expected_path, k=5)
    keyword_match = check_keyword_match(results, expected_keywords, k=3)
    mrr = compute_mrr(results, expected_path)
    passed = hit_at_5 and keyword_match

    # 상위 3개 결과 요약
    top_results_summary = []
    for r in results[:3]:
        top_results_summary.append(
            {
                "rank": r.rank,
                "score": round(r.score, 4),
                "path": str(r.chunk.doc_path),
                "headers": r.chunk.headers[:2] if r.chunk.headers else [],
                "content_preview": r.chunk.content[:80].replace("\n", " "),
            }
        )

    return {
        "id": test_case["id"],
        "category": test_case["category"],
        "query": query,
        "expected_path_contains": expected_path,
        "expected_keywords": expected_keywords,
        "passed": passed,
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
        "hit_at_5": hit_at_5,
        "keyword_match": keyword_match,
        "mrr": round(mrr, 4),
        "elapsed_ms": round(elapsed_ms, 1),
        "result_count": len(results),
        "top_results": top_results_summary,
        "notes": test_case.get("notes", ""),
    }


# ---------------------------------------------------------------------------
# 집계 및 출력
# ---------------------------------------------------------------------------


def aggregate_results(
    eval_results: list[dict[str, Any]],
) -> dict[str, Any]:
    """카테고리별 및 전체 집계를 계산합니다."""
    categories = ["rfc", "ccie", "ko", "edge"]
    category_stats: dict[str, dict[str, Any]] = {}

    for cat in categories:
        items = [r for r in eval_results if r["category"] == cat]
        if not items:
            continue

        n = len(items)
        category_stats[cat] = {
            "total": n,
            "passed": sum(1 for r in items if r["passed"]),
            "hit_at_1": sum(1 for r in items if r["hit_at_1"]),
            "hit_at_3": sum(1 for r in items if r["hit_at_3"]),
            "hit_at_5": sum(1 for r in items if r["hit_at_5"]),
            "keyword_match": sum(1 for r in items if r["keyword_match"]),
            "avg_mrr": round(sum(r["mrr"] for r in items) / n, 4),
            "avg_elapsed_ms": round(sum(r["elapsed_ms"] for r in items) / n, 1),
        }
        # 백분율 추가
        for key in ["passed", "hit_at_1", "hit_at_3", "hit_at_5", "keyword_match"]:
            category_stats[cat][f"{key}_pct"] = round(
                category_stats[cat][key] / n * 100, 1
            )

    # 전체 집계
    n_total = len(eval_results)
    overall: dict[str, Any] = {
        "total": n_total,
        "passed": sum(1 for r in eval_results if r["passed"]),
        "hit_at_1": sum(1 for r in eval_results if r["hit_at_1"]),
        "hit_at_3": sum(1 for r in eval_results if r["hit_at_3"]),
        "hit_at_5": sum(1 for r in eval_results if r["hit_at_5"]),
        "keyword_match": sum(1 for r in eval_results if r["keyword_match"]),
        "avg_mrr": round(
            sum(r["mrr"] for r in eval_results) / n_total, 4
        ),
        "avg_elapsed_ms": round(
            sum(r["elapsed_ms"] for r in eval_results) / n_total, 1
        ),
    }
    for key in ["passed", "hit_at_1", "hit_at_3", "hit_at_5", "keyword_match"]:
        overall[f"{key}_pct"] = round(overall[key] / n_total * 100, 1)

    return {"overall": overall, "by_category": category_stats}


def print_summary(
    aggregated: dict[str, Any],
    failed_cases: list[dict[str, Any]],
) -> None:
    """평가 결과 요약을 출력합니다."""
    overall = aggregated["overall"]
    by_cat = aggregated["by_category"]

    print("\n" + "=" * 60)
    print("RAG 검증 결과 요약")
    print("=" * 60)

    # 전체 요약
    print(f"\n[전체] {overall['total']}개 테스트")
    print(f"  통과율    : {overall['passed']}/{overall['total']} ({overall['passed_pct']}%)")
    print(f"  Hit@1     : {overall['hit_at_1']}/{overall['total']} ({overall['hit_at_1_pct']}%)")
    print(f"  Hit@3     : {overall['hit_at_3']}/{overall['total']} ({overall['hit_at_3_pct']}%)")
    print(f"  Hit@5     : {overall['hit_at_5']}/{overall['total']} ({overall['hit_at_5_pct']}%)")
    print(f"  키워드 매치: {overall['keyword_match']}/{overall['total']} ({overall['keyword_match_pct']}%)")
    print(f"  평균 MRR  : {overall['avg_mrr']}")
    print(f"  평균 응답 : {overall['avg_elapsed_ms']}ms")

    # 카테고리별 요약
    cat_labels = {"rfc": "IETF RFC", "ccie": "Cisco CCIE", "ko": "한국어 매뉴얼", "edge": "교차/엣지"}
    print("\n[카테고리별]")
    print(f"  {'카테고리':<14} {'통과':>6} {'Hit@1':>6} {'Hit@3':>6} {'Hit@5':>6} {'키워드':>6} {'MRR':>6}")
    print("  " + "-" * 54)
    for cat, label in cat_labels.items():
        if cat not in by_cat:
            continue
        s = by_cat[cat]
        print(
            f"  {label:<14} "
            f"{s['passed_pct']:>5.1f}% "
            f"{s['hit_at_1_pct']:>5.1f}% "
            f"{s['hit_at_3_pct']:>5.1f}% "
            f"{s['hit_at_5_pct']:>5.1f}% "
            f"{s['keyword_match_pct']:>5.1f}% "
            f"{s['avg_mrr']:>6.4f}"
        )

    # 실패 케이스
    if failed_cases:
        print(f"\n[실패 케이스] {len(failed_cases)}개")
        for fc in failed_cases:
            h5 = "O" if fc["hit_at_5"] else "X"
            km = "O" if fc["keyword_match"] else "X"
            print(
                f"  [{fc['id']}] Hit@5={h5} KeyMatch={km} | {fc['query'][:50]}"
            )
            if fc["top_results"]:
                top = fc["top_results"][0]
                print(f"       1위: {top['path'][:60]} (score={top['score']})")

    print("=" * 60)


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------


def build_search_engine(settings: Settings) -> SemanticSearch:
    """검색 엔진을 초기화합니다."""
    print("검색 엔진 초기화 중...")

    # 임베딩 백엔드
    embedding = LocalEmbedding(model_name=settings.local_model)

    # 벡터 스토어
    store = ChromaStore(
        persist_path=settings.chroma_path,
        collection_name=settings.collection_name,
    )

    # 시맨틱 검색 엔진
    engine = SemanticSearch(
        embedding_backend=embedding,
        vector_store=store,
        top_k=settings.search_top_k,
    )

    chunk_count = store.count()
    print(f"인덱스 로드 완료: {chunk_count:,}개 청크")
    return engine


def main() -> None:
    """메인 평가 루프."""
    parser = argparse.ArgumentParser(
        description="RAG 기능 검증 스크립트",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path(__file__).parent / "validation_dataset.json",
        help="검증 데이터셋 JSON 파일 경로 (기본값: scripts/validation_dataset.json)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="검색 결과 수 (기본값: 5)",
    )
    parser.add_argument(
        "--category",
        choices=["rfc", "ccie", "ko", "edge", "all"],
        default="all",
        help="평가할 카테고리 (기본값: all)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="결과 JSON 저장 경로 (기본값: scripts/validation_results_<timestamp>.json)",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=_PROJECT_ROOT / ".env",
        help=".env 파일 경로",
    )
    args = parser.parse_args()

    # .env 파일 경로를 환경변수로 전달
    if args.env_file.exists():
        os.environ.setdefault("ENV_FILE", str(args.env_file))

    # 설정 로드 (작업 디렉토리를 프로젝트 루트로 변경)
    original_cwd = Path.cwd()
    os.chdir(_PROJECT_ROOT)

    try:
        settings = Settings()
        test_cases = load_dataset(args.dataset)
    finally:
        os.chdir(original_cwd)

    # 카테고리 필터
    if args.category != "all":
        test_cases = [tc for tc in test_cases if tc["category"] == args.category]

    print(f"평가 대상: {len(test_cases)}개 테스트 케이스 (카테고리: {args.category})")

    # 검색 엔진 초기화 (프로젝트 루트에서 실행)
    os.chdir(_PROJECT_ROOT)
    try:
        engine = build_search_engine(settings)
    finally:
        os.chdir(original_cwd)

    # 평가 루프
    print(f"\n평가 시작 (top_k={args.top_k})...")
    eval_results: list[dict[str, Any]] = []

    os.chdir(_PROJECT_ROOT)
    try:
        for i, test_case in enumerate(test_cases, start=1):
            result = evaluate_single(engine, test_case, top_k=args.top_k)
            eval_results.append(result)

            # 진행 표시 (10개마다)
            status = "PASS" if result["passed"] else "FAIL"
            if i % 10 == 0 or i == len(test_cases):
                passed_so_far = sum(1 for r in eval_results if r["passed"])
                print(
                    f"  [{i:3d}/{len(test_cases)}] "
                    f"통과: {passed_so_far}/{i} "
                    f"({passed_so_far/i*100:.1f}%) "
                    f"| 최근: [{test_case['id']}] {status}"
                )
            else:
                # 각 케이스 결과 간략 표시
                marker = "." if result["passed"] else "F"
                print(marker, end="", flush=True)
    finally:
        os.chdir(original_cwd)

    print()  # 줄바꿈

    # 집계
    aggregated = aggregate_results(eval_results)
    failed_cases = [r for r in eval_results if not r["passed"]]

    # 요약 출력
    print_summary(aggregated, failed_cases)

    # JSON 리포트 저장
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(__file__).parent / f"validation_results_{timestamp}.json"
    else:
        output_path = args.output

    report = {
        "run_at": datetime.now().isoformat(),
        "dataset": str(args.dataset),
        "top_k": args.top_k,
        "category_filter": args.category,
        "summary": aggregated,
        "failed_count": len(failed_cases),
        "results": eval_results,
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n리포트 저장: {output_path}")


if __name__ == "__main__":
    main()
