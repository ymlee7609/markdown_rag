"""리뷰 피드백을 테스트셋에 반영하는 스크립트.

review_rag.py로 생성된 리뷰 파일을 읽어
validation_dataset.json의 기대값(경로, 키워드)을 업데이트한다.

사용법:
    python scripts/apply_feedback.py
    python scripts/apply_feedback.py --review feedback/review_*.json
    python scripts/apply_feedback.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_SCRIPTS_DIR = Path(__file__).parent
_FEEDBACK_DIR = _SCRIPTS_DIR / "feedback"
_DATASET_PATH = _SCRIPTS_DIR / "validation_dataset.json"


def find_latest_review() -> Path | None:
    """feedback/ 디렉토리에서 가장 최근 리뷰 파일을 찾는다."""
    review_files = sorted(
        _FEEDBACK_DIR.glob("review_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return review_files[0] if review_files else None


def load_review(review_path: Path) -> dict[str, Any]:
    """리뷰 파일을 로드한다."""
    with review_path.open(encoding="utf-8") as f:
        return json.load(f)


def load_dataset(dataset_path: Path) -> dict[str, Any]:
    """테스트셋을 로드한다."""
    with dataset_path.open(encoding="utf-8") as f:
        return json.load(f)


def apply_reviews(
    dataset: dict[str, Any],
    reviews: list[dict[str, Any]],
    dry_run: bool = False,
) -> list[dict[str, str]]:
    """리뷰를 테스트셋에 반영하고 변경 내역을 반환한다.

    Args:
        dataset: 테스트셋 데이터.
        reviews: 리뷰 항목 리스트.
        dry_run: True이면 변경하지 않고 미리보기만.

    Returns:
        변경 내역 리스트.
    """
    # 테스트 케이스를 id로 인덱싱
    cases_by_id: dict[str, dict[str, Any]] = {
        tc["id"]: tc for tc in dataset["test_cases"]
    }

    changes: list[dict[str, str]] = []

    for review in reviews:
        case_id = review["id"]
        case = cases_by_id.get(case_id)
        if case is None:
            changes.append({
                "id": case_id,
                "type": "warning",
                "detail": f"테스트 케이스 '{case_id}'를 찾을 수 없음",
            })
            continue

        # 경로 업데이트
        if review.get("correct_path"):
            old_path = case.get("expected_path_contains", "없음")
            new_path = review["correct_path"]
            if old_path != new_path:
                changes.append({
                    "id": case_id,
                    "type": "path",
                    "detail": f"expected_path: {old_path} -> {new_path}",
                })
                if not dry_run:
                    case["expected_path_contains"] = new_path

        # 키워드 업데이트
        if review.get("updated_keywords"):
            old_kw = set(case.get("expected_keywords", []))
            new_kw = set(review["updated_keywords"])
            added = new_kw - old_kw
            removed = old_kw - new_kw
            if added or removed:
                detail_parts = []
                if added:
                    detail_parts.append(f"+{', '.join(sorted(added))}")
                if removed:
                    detail_parts.append(f"-{', '.join(sorted(removed))}")
                changes.append({
                    "id": case_id,
                    "type": "keywords",
                    "detail": f"keywords: {' '.join(detail_parts)}",
                })
                if not dry_run:
                    case["expected_keywords"] = review["updated_keywords"]

        # 메모 추가
        if review.get("feedback"):
            existing_notes = case.get("notes", "")
            feedback_text = review["feedback"]
            if feedback_text not in existing_notes:
                changes.append({
                    "id": case_id,
                    "type": "notes",
                    "detail": f"notes: +'{feedback_text}'",
                })
                if not dry_run:
                    separator = " | " if existing_notes else ""
                    case["notes"] = existing_notes + separator + feedback_text

    return changes


def save_dataset(dataset: dict[str, Any], dataset_path: Path) -> None:
    """업데이트된 테스트셋을 저장한다."""
    with dataset_path.open("w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    # JSON 파일 끝에 개행 추가
    with dataset_path.open("a", encoding="utf-8") as f:
        f.write("\n")


def print_changes(
    changes: list[dict[str, str]],
    review_data: dict[str, Any],
    dry_run: bool,
) -> None:
    """변경 내역을 출력한다."""
    mode = "[DRY-RUN] " if dry_run else ""
    review_id = review_data.get("review_id", "unknown")
    total_reviewed = review_data.get("total_reviewed", 0)

    print(f"\n{mode}피드백 반영: {review_id}")
    print(f"리뷰 항목: {total_reviewed}개")
    print(f"변경 사항: {len(changes)}개")
    print()

    if not changes:
        print("변경할 사항이 없습니다.")
        return

    # 변경사항 ID별 그룹핑
    by_id: dict[str, list[str]] = {}
    warnings: list[str] = []
    for c in changes:
        if c["type"] == "warning":
            warnings.append(c["detail"])
        else:
            by_id.setdefault(c["id"], []).append(c["detail"])

    for case_id, details in sorted(by_id.items()):
        print(f"  [{case_id}]")
        for d in details:
            print(f"    {d}")

    if warnings:
        print("\n  경고:")
        for w in warnings:
            print(f"    {w}")


def main() -> None:
    """메인 실행."""
    parser = argparse.ArgumentParser(
        description="리뷰 피드백을 테스트셋에 반영",
    )
    parser.add_argument(
        "--review",
        type=Path,
        default=None,
        help="리뷰 파일 경로 (기본값: 최신 리뷰 자동 선택)",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=_DATASET_PATH,
        help="테스트셋 파일 경로 (기본값: scripts/validation_dataset.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="변경사항만 출력하고 실제 적용하지 않음",
    )
    args = parser.parse_args()

    # 리뷰 파일 선택
    if args.review:
        review_path = args.review
    else:
        review_path = find_latest_review()
        if review_path is None:
            print("리뷰 파일을 찾을 수 없습니다.")
            print("먼저 실행: python scripts/review_rag.py")
            sys.exit(1)

    print(f"리뷰 파일: {review_path}")
    print(f"테스트셋 : {args.dataset}")

    review_data = load_review(review_path)
    dataset = load_dataset(args.dataset)

    # 피드백 반영
    changes = apply_reviews(
        dataset,
        review_data["reviews"],
        dry_run=args.dry_run,
    )

    print_changes(changes, review_data, args.dry_run)

    # 저장
    if not args.dry_run and changes:
        save_dataset(dataset, args.dataset)
        print(f"\n{args.dataset} 저장 완료.")
        print("다음 단계: python scripts/validate_rag.py")
    elif args.dry_run and changes:
        print("\n[DRY-RUN] 실제 적용하려면 --dry-run 없이 실행하세요.")


if __name__ == "__main__":
    main()
