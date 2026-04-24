"""RAG 검색 결과 사람 리뷰 CLI.

검증 결과 파일을 로드하여 각 테스트 케이스의 검색 품질을
사람이 직접 확인하고 어노테이션할 수 있는 인터랙티브 도구.

사용법:
    python scripts/review_rag.py
    python scripts/review_rag.py --results scripts/validation_results_*.json
    python scripts/review_rag.py --all --category rfc
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

_SCRIPTS_DIR = Path(__file__).parent
_FEEDBACK_DIR = _SCRIPTS_DIR / "feedback"


def find_latest_results() -> Path | None:
    """scripts/ 디렉토리에서 가장 최근 validation_results 파일을 찾는다."""
    results_files = sorted(
        _SCRIPTS_DIR.glob("validation_results_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return results_files[0] if results_files else None


def load_results(results_path: Path) -> dict[str, Any]:
    """검증 결과 JSON 파일을 로드한다."""
    with results_path.open(encoding="utf-8") as f:
        return json.load(f)


def display_case(
    idx: int,
    total: int,
    result: dict[str, Any],
) -> None:
    """테스트 케이스를 보기 좋게 출력한다."""
    status = "PASS" if result["passed"] else "FAIL"
    print(f"\n{'=' * 60}")
    print(f"[{idx}/{total}] {result['id']} ({status})")
    print("-" * 60)
    print(f"쿼리      : {result['query']}")
    print(f"기대 경로  : {result.get('expected_path_contains', '없음')}")
    print(f"기대 키워드: {', '.join(result.get('expected_keywords', []))}")
    print(f"Hit@5={result['hit_at_5']}  KeyMatch={result['keyword_match']}  MRR={result['mrr']}")
    print()

    for tr in result.get("top_results", []):
        print(f"  [{tr['rank']}위] score={tr['score']}")
        print(f"       경로: {tr['path']}")
        if tr.get("headers"):
            print(f"       헤더: {' > '.join(tr['headers'])}")
        print(f"       내용: {tr['content_preview']}")
        print()

    if result.get("notes"):
        print(f"노트: {result['notes']}")
    print("-" * 60)


def prompt_review(result: dict[str, Any]) -> dict[str, Any] | None:
    """사용자로부터 리뷰 어노테이션을 수집한다.

    Returns:
        리뷰 딕셔너리 또는 None(건너뛰기).
        'quit'를 입력하면 KeyboardInterrupt를 발생시킨다.
    """
    print("  [q=종료, s=건너뛰기, Enter=기본값]")

    # 관련성 점수
    score_input = input("  관련성 (0-5, Enter=0): ").strip()
    if score_input.lower() == "q":
        raise KeyboardInterrupt
    if score_input.lower() == "s":
        return None
    human_score = int(score_input) if score_input.isdigit() else 0
    human_score = max(0, min(5, human_score))

    # 올바른 경로
    path_input = input("  올바른 경로 (Enter=유지): ").strip()
    if path_input.lower() == "q":
        raise KeyboardInterrupt
    correct_path = path_input if path_input else None

    # 키워드 수정
    kw_input = input("  키워드 수정 (쉼표 구분, Enter=유지): ").strip()
    if kw_input.lower() == "q":
        raise KeyboardInterrupt
    updated_keywords = (
        [k.strip() for k in kw_input.split(",") if k.strip()]
        if kw_input
        else None
    )

    # 메모
    feedback_input = input("  메모 (Enter=건너뛰기): ").strip()
    if feedback_input.lower() == "q":
        raise KeyboardInterrupt

    return {
        "id": result["id"],
        "query": result["query"],
        "auto_passed": result["passed"],
        "human_score": human_score,
        "correct_path": correct_path,
        "updated_keywords": updated_keywords,
        "feedback": feedback_input if feedback_input else None,
    }


def save_review(
    reviews: list[dict[str, Any]],
    base_results_path: Path,
) -> Path:
    """리뷰 결과를 JSON 파일로 저장한다."""
    _FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = _FEEDBACK_DIR / f"review_{timestamp}.json"

    review_data = {
        "review_id": f"review_{timestamp}",
        "reviewer": "ymlee",
        "base_results": str(base_results_path.name),
        "reviewed_at": datetime.now().isoformat(),
        "total_reviewed": len(reviews),
        "reviews": reviews,
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(review_data, f, ensure_ascii=False, indent=2)

    return output_path


def main() -> None:
    """메인 리뷰 루프."""
    parser = argparse.ArgumentParser(
        description="RAG 검색 결과 사람 리뷰 CLI",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=None,
        help="검증 결과 JSON 파일 (기본값: 최신 파일 자동 선택)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="통과 케이스 포함 전체 리뷰 (기본값: 실패 케이스만)",
    )
    parser.add_argument(
        "--category",
        choices=["rfc", "ccie", "ko", "edge", "all"],
        default="all",
        help="리뷰할 카테고리 (기본값: all)",
    )
    args = parser.parse_args()

    # 결과 파일 선택
    if args.results:
        results_path = args.results
    else:
        results_path = find_latest_results()
        if results_path is None:
            print("검증 결과 파일을 찾을 수 없습니다.")
            print("먼저 실행: python scripts/validate_rag.py")
            sys.exit(1)

    print(f"결과 파일: {results_path.name}")
    data = load_results(results_path)

    # 리뷰 대상 필터링
    cases = data["results"]
    if not args.all:
        cases = [c for c in cases if not c["passed"]]
    if args.category != "all":
        cases = [c for c in cases if c["category"] == args.category]

    if not cases:
        print("리뷰할 케이스가 없습니다.")
        sys.exit(0)

    print(f"리뷰 대상: {len(cases)}개 ({'전체' if args.all else '실패만'})")
    print("  q=종료, s=건너뛰기, Enter=기본값\n")

    # 리뷰 루프
    reviews: list[dict[str, Any]] = []
    try:
        for i, case in enumerate(cases, start=1):
            display_case(i, len(cases), case)
            review = prompt_review(case)
            if review is not None:
                reviews.append(review)
                print(f"  -> 저장됨 (점수: {review['human_score']})")
            else:
                print("  -> 건너뜀")
    except (KeyboardInterrupt, EOFError):
        print("\n\n리뷰 중단.")

    # 결과 저장
    if reviews:
        output = save_review(reviews, results_path)
        print(f"\n리뷰 결과 저장: {output}")
        print(f"리뷰 완료: {len(reviews)}개")
        print(f"\n다음 단계: python scripts/apply_feedback.py --review {output}")
    else:
        print("\n리뷰된 케이스가 없습니다.")


if __name__ == "__main__":
    main()
