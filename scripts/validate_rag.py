"""RAG 기능 검증 스크립트.

테스트 케이스의 polarity에 따라 두 축으로 채점합니다.

  positive (정답 케이스) - 기대 문서를 회수했는가
      Hit@1 / Hit@3 / Hit@5, Keyword Match, MRR

  negative (부정 케이스) - 근거가 없는데 답을 지어내지 않는가
      검색 단계: 인용 금지 경로(타 벤더/형제모델 문서)를 상위에 올리지 않았는가
      답변 단계: 유보했는가(abstain/reject_premise), 금지 문구를 말하지 않았는가,
                금지 경로를 출처로 인용하지 않았는가   ← --with-answer 필요

polarity 필드가 없는 기존 데이터셋은 전부 positive로 간주되어 기존과 동일하게 동작합니다.

사용법:
    python scripts/validate_rag.py
    python scripts/validate_rag.py --dataset scripts/validation_dataset_manual_full.json
    python scripts/validate_rag.py --dataset ... --with-answer          # 유보/환각률까지
    python scripts/validate_rag.py --dataset ... --polarity negative    # 거절 성능만
    python scripts/validate_rag.py --dataset ... --vendor 유비쿼스_OLT
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

from markdown_rag.config import Settings  # noqa: E402
from markdown_rag.models import SearchResult  # noqa: E402
from markdown_rag.retriever.builder import build_search_engine  # noqa: E402

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


# ---------------------------------------------------------------------------
# 부정(negative) 케이스 판정
# ---------------------------------------------------------------------------

# 답변이 "근거 없음"을 표명했다고 볼 수 있는 표현. 휴리스틱이며 완벽하지 않다.
# 오탐 가능성: "A는 10W이고 B 정보는 없습니다" 처럼 일부만 유보한 답변도 유보로 집계된다.
# 이를 보완하려고 유보 판정과 별개로 fail_if_answer_contains(금지 문구)를 함께 확인한다.
ABSTAIN_PATTERNS = [
    "찾을 수 없", "확인할 수 없", "확인이 불가", "알 수 없",
    "포함되어 있지 않", "기재되어 있지 않", "명시되어 있지 않", "나와 있지 않",
    "정보가 없", "내용이 없", "자료가 없", "언급이 없",
    "존재하지 않", "명령이 없", "지원하지 않", "해당 사항이 없",
    "cannot find", "not found", "no information", "does not contain",
    "is not available", "not specified", "no such command",
]


def check_forbidden_paths(
    results: list[SearchResult],
    forbidden: list[str],
    k: int,
) -> tuple[bool, list[str]]:
    """상위 k개 결과가 인용 금지 경로를 피했는지 확인합니다.

    Returns:
        (통과 여부, 위반한 경로 목록)
    """
    if not forbidden:
        return True, []

    violations = []
    for result in results[:k]:
        path = str(result.chunk.doc_path)
        if any(pattern in path for pattern in forbidden):
            violations.append(path)
    return not violations, violations


def check_abstained(answer: str) -> bool:
    """답변이 근거 부재를 표명했는지 판정합니다(휴리스틱)."""
    if not answer:
        return False
    low = answer.lower()
    return any(p.lower() in low for p in ABSTAIN_PATTERNS)


def check_forbidden_phrases(answer: str, forbidden: list[str]) -> tuple[bool, list[str]]:
    """답변에 등장하면 안 되는 문구가 있는지 확인합니다.

    Returns:
        (통과 여부, 발견된 금지 문구 목록)
    """
    if not answer or not forbidden:
        return True, []
    low = answer.lower()
    found = [p for p in forbidden if p.lower() in low]
    return not found, found


# ---------------------------------------------------------------------------
# 케이스 평가
# ---------------------------------------------------------------------------


def _summarize_results(results: list[SearchResult], n: int = 3) -> list[dict[str, Any]]:
    """상위 n개 검색 결과를 리포트용으로 요약합니다."""
    return [
        {
            "rank": r.rank,
            "score": round(r.score, 4),
            "path": str(r.chunk.doc_path),
            "headers": r.chunk.headers[:2] if r.chunk.headers else [],
            "content_preview": r.chunk.content[:80].replace("\n", " "),
        }
        for r in results[:n]
    ]


def evaluate_single(
    search_engine,
    test_case: dict[str, Any],
    top_k: int,
    rag_engine=None,
) -> dict[str, Any]:
    """단일 테스트 케이스를 평가합니다.

    polarity에 따라 채점 기준이 다릅니다.
      positive: 기대 경로를 상위 k개 안에서 회수했는지(Hit@k) + 키워드 매치
      negative: 인용 금지 경로를 피했는지(검색 단계) + 유보/금지문구(답변 단계)

    rag_engine이 주어지면 답변까지 생성해 답변 단계 지표를 함께 채점합니다.
    """
    if test_case.get("polarity", "positive") == "negative":
        return _evaluate_negative(search_engine, test_case, top_k, rag_engine)
    return _evaluate_positive(search_engine, test_case, top_k, rag_engine)


def _evaluate_positive(
    search_engine,
    test_case: dict[str, Any],
    top_k: int,
    rag_engine=None,
) -> dict[str, Any]:
    """정답 케이스: 기대 문서를 회수했는지 평가합니다."""
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

    record: dict[str, Any] = {
        "id": test_case["id"],
        "category": test_case["category"],
        "polarity": "positive",
        "vendor": test_case.get("vendor"),
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
        "top_results": _summarize_results(results),
        "notes": test_case.get("notes", ""),
    }

    if rag_engine is not None:
        answer = rag_engine.ask(query, top_k=top_k, show_sources=False).answer
        # 정답 케이스의 답변 단계 보조 지표: 부당한 유보(회수는 됐는데 모른다고 답함)
        record["answer"] = answer
        record["answer_abstained"] = check_abstained(answer)
        record["over_abstained"] = bool(hit_at_5 and record["answer_abstained"])

    return record


def _evaluate_negative(
    search_engine,
    test_case: dict[str, Any],
    top_k: int,
    rag_engine=None,
) -> dict[str, Any]:
    """부정 케이스: 근거가 없는데 답을 지어내지 않는지 평가합니다.

    검색 단계에서는 Hit@k가 의미를 갖지 않으므로 None으로 두고 집계에서 제외합니다.
    대신 '인용 금지 경로를 피했는가'를 검색 단계 지표로 사용합니다.
    """
    query = test_case["query"]
    forbidden_paths = test_case.get("must_not_cite_path_contains", []) or []
    forbidden_phrases = test_case.get("fail_if_answer_contains", []) or []
    expected_behavior = test_case.get("expected_behavior", "abstain")

    start_time = time.time()
    results = search_engine.search(query, top_k=top_k)
    elapsed_ms = (time.time() - start_time) * 1000

    path_clean, violations = check_forbidden_paths(results, forbidden_paths, k=top_k)

    record: dict[str, Any] = {
        "id": test_case["id"],
        "category": test_case["category"],
        "polarity": "negative",
        "negative_flavor": test_case.get("negative_flavor"),
        "vendor": test_case.get("vendor"),
        "query": query,
        "expected_behavior": expected_behavior,
        "expected_path_contains": None,
        "expected_keywords": [],
        # 부정 케이스에 의미 없는 회수 지표는 None (집계에서 제외)
        "hit_at_1": None,
        "hit_at_3": None,
        "hit_at_5": None,
        "keyword_match": None,
        "mrr": None,
        "path_clean": path_clean,
        "forbidden_path_hits": violations,
        "elapsed_ms": round(elapsed_ms, 1),
        "result_count": len(results),
        "top_results": _summarize_results(results),
        "notes": test_case.get("notes", ""),
    }

    if rag_engine is None:
        # 검색 단계만 채점. 유보 여부는 답변이 없으면 판정 불가.
        record["answer_evaluated"] = False
        record["passed"] = path_clean
        record["pass_basis"] = "retrieval_only"
        return record

    response = rag_engine.ask(query, top_k=top_k, show_sources=True)
    answer = response.answer
    abstained = check_abstained(answer)
    phrase_clean, found_phrases = check_forbidden_phrases(answer, forbidden_phrases)
    cited_clean, cited_violations = check_forbidden_paths(
        response.sources, forbidden_paths, k=top_k
    )

    record.update(
        {
            "answer_evaluated": True,
            "answer": answer,
            "abstained": abstained,
            "phrase_clean": phrase_clean,
            "forbidden_phrases_found": found_phrases,
            "cited_clean": cited_clean,
            "cited_forbidden_paths": cited_violations,
            # 부정 케이스 통과 = 유보(또는 전제 교정) + 금지문구 없음 + 금지경로 미인용
            "passed": abstained and phrase_clean and cited_clean,
            "pass_basis": "answer",
        }
    )
    return record


# ---------------------------------------------------------------------------
# 집계 및 출력
# ---------------------------------------------------------------------------


def _pct(num: int, den: int) -> float:
    return round(num / den * 100, 1) if den else 0.0


def _positive_stats(items: list[dict[str, Any]]) -> dict[str, Any]:
    """정답 케이스 회수 지표를 집계합니다."""
    n = len(items)
    if not n:
        return {}
    stats: dict[str, Any] = {
        "total": n,
        "passed": sum(1 for r in items if r["passed"]),
        "hit_at_1": sum(1 for r in items if r["hit_at_1"]),
        "hit_at_3": sum(1 for r in items if r["hit_at_3"]),
        "hit_at_5": sum(1 for r in items if r["hit_at_5"]),
        "keyword_match": sum(1 for r in items if r["keyword_match"]),
        "avg_mrr": round(sum(r["mrr"] for r in items) / n, 4),
        "avg_elapsed_ms": round(sum(r["elapsed_ms"] for r in items) / n, 1),
    }
    for key in ["passed", "hit_at_1", "hit_at_3", "hit_at_5", "keyword_match"]:
        stats[f"{key}_pct"] = _pct(stats[key], n)
    over = [r for r in items if r.get("over_abstained") is not None]
    if over:
        stats["over_abstained"] = sum(1 for r in over if r["over_abstained"])
        stats["over_abstained_pct"] = _pct(stats["over_abstained"], len(over))
    return stats


def _negative_stats(items: list[dict[str, Any]]) -> dict[str, Any]:
    """부정 케이스 거절 지표를 집계합니다."""
    n = len(items)
    if not n:
        return {}
    answered = [r for r in items if r.get("answer_evaluated")]
    stats: dict[str, Any] = {
        "total": n,
        "passed": sum(1 for r in items if r["passed"]),
        "path_clean": sum(1 for r in items if r["path_clean"]),
        "answer_evaluated": len(answered),
        "avg_elapsed_ms": round(sum(r["elapsed_ms"] for r in items) / n, 1),
    }
    stats["passed_pct"] = _pct(stats["passed"], n)
    stats["path_clean_pct"] = _pct(stats["path_clean"], n)
    if answered:
        stats["abstained"] = sum(1 for r in answered if r["abstained"])
        stats["phrase_clean"] = sum(1 for r in answered if r["phrase_clean"])
        stats["cited_clean"] = sum(1 for r in answered if r["cited_clean"])
        stats["abstained_pct"] = _pct(stats["abstained"], len(answered))
        stats["phrase_clean_pct"] = _pct(stats["phrase_clean"], len(answered))
        stats["cited_clean_pct"] = _pct(stats["cited_clean"], len(answered))
        # 환각률: 유보하지 않고 답을 만들어낸 비율
        stats["hallucinated"] = sum(1 for r in answered if not r["abstained"])
        stats["hallucinated_pct"] = _pct(stats["hallucinated"], len(answered))
    return stats


def _group_stats(eval_results: list[dict[str, Any]], key: str) -> dict[str, Any]:
    """임의 키(category/vendor/negative_flavor)별로 극성을 나눠 집계합니다."""
    out: dict[str, Any] = {}
    for value in dict.fromkeys(r.get(key) for r in eval_results if r.get(key)):
        items = [r for r in eval_results if r.get(key) == value]
        pos = [r for r in items if r["polarity"] == "positive"]
        neg = [r for r in items if r["polarity"] == "negative"]
        out[value] = {
            "total": len(items),
            "passed": sum(1 for r in items if r["passed"]),
            "passed_pct": _pct(sum(1 for r in items if r["passed"]), len(items)),
            "positive": _positive_stats(pos),
            "negative": _negative_stats(neg),
        }
    return out


def aggregate_results(
    eval_results: list[dict[str, Any]],
) -> dict[str, Any]:
    """극성별/카테고리별/벤더별 집계를 계산합니다.

    정답 케이스와 부정 케이스는 채점 축이 달라 별도로 집계한 뒤,
    전체 통과율만 두 축을 합산해 보여줍니다.
    """
    positives = [r for r in eval_results if r["polarity"] == "positive"]
    negatives = [r for r in eval_results if r["polarity"] == "negative"]
    n_total = len(eval_results)

    overall = {
        "total": n_total,
        "passed": sum(1 for r in eval_results if r["passed"]),
        "avg_elapsed_ms": round(
            sum(r["elapsed_ms"] for r in eval_results) / n_total, 1
        ) if n_total else 0.0,
    }
    overall["passed_pct"] = _pct(overall["passed"], n_total)

    # 하위 호환: 기존 리포트 소비자를 위해 정답 케이스 회수 지표를 overall에도 노출
    pos_stats = _positive_stats(positives)
    for key in ["hit_at_1", "hit_at_3", "hit_at_5", "keyword_match", "avg_mrr"]:
        if key in pos_stats:
            overall[key] = pos_stats[key]
            if f"{key}_pct" in pos_stats:
                overall[f"{key}_pct"] = pos_stats[f"{key}_pct"]

    return {
        "overall": overall,
        "positive": pos_stats,
        "negative": _negative_stats(negatives),
        "by_category": _group_stats(eval_results, "category"),
        "by_vendor": _group_stats(eval_results, "vendor"),
        "by_negative_flavor": {
            k: v["negative"] for k, v in _group_stats(negatives, "negative_flavor").items()
        },
    }


CAT_LABELS = {
    "rfc": "IETF RFC",
    "ccie": "Cisco CCIE",
    "ko": "한국어 매뉴얼",
    "edge": "교차/엣지",
    "spec_value": "제원·기본값",
    "command_syntax": "명령어 문법",
    "diagnostics": "진단·상태확인",
    "negative": "부정 케이스",
}
FLAVOR_LABELS = {
    "missing_doc_type": "문서종류 부재",
    "substring_false_match": "부분문자열 오검색",
    "cross_vendor_syntax": "교차벤더 문법",
    "sibling_model_leak": "형제모델 전이",
    "out_of_corpus_spec": "코퍼스 전체 부재",
}


def print_summary(
    aggregated: dict[str, Any],
    failed_cases: list[dict[str, Any]],
) -> None:
    """평가 결과 요약을 출력합니다."""
    overall = aggregated["overall"]
    pos = aggregated.get("positive") or {}
    neg = aggregated.get("negative") or {}

    print("\n" + "=" * 68)
    print("RAG 검증 결과 요약")
    print("=" * 68)

    print(f"\n[전체] {overall['total']}개 테스트")
    print(f"  통과율    : {overall['passed']}/{overall['total']} ({overall['passed_pct']}%)")
    print(f"  평균 응답 : {overall['avg_elapsed_ms']}ms")

    if pos:
        print(f"\n[정답 케이스] {pos['total']}개 — 기대 문서를 회수했는가")
        print(f"  통과율    : {pos['passed']}/{pos['total']} ({pos['passed_pct']}%)")
        print(f"  Hit@1     : {pos['hit_at_1']}/{pos['total']} ({pos['hit_at_1_pct']}%)")
        print(f"  Hit@3     : {pos['hit_at_3']}/{pos['total']} ({pos['hit_at_3_pct']}%)")
        print(f"  Hit@5     : {pos['hit_at_5']}/{pos['total']} ({pos['hit_at_5_pct']}%)")
        print(f"  키워드 매치: {pos['keyword_match']}/{pos['total']} ({pos['keyword_match_pct']}%)")
        print(f"  평균 MRR  : {pos['avg_mrr']}")
        if "over_abstained" in pos:
            print(
                f"  과잉 유보 : {pos['over_abstained']} "
                f"({pos['over_abstained_pct']}%)  ← 회수했는데 모른다고 답한 건"
            )

    if neg:
        basis = "답변 단계" if neg.get("answer_evaluated") else "검색 단계만"
        print(f"\n[부정 케이스] {neg['total']}개 — 근거 없이 답을 지어내지 않는가 ({basis})")
        print(f"  통과율    : {neg['passed']}/{neg['total']} ({neg['passed_pct']}%)")
        print(
            f"  금지경로 회피: {neg['path_clean']}/{neg['total']} ({neg['path_clean_pct']}%)"
            "  ← 타 벤더/형제모델 문서를 상위에 올리지 않음"
        )
        if neg.get("answer_evaluated"):
            m = neg["answer_evaluated"]
            print(f"  유보율    : {neg['abstained']}/{m} ({neg['abstained_pct']}%)")
            print(
                f"  환각률    : {neg['hallucinated']}/{m} ({neg['hallucinated_pct']}%)"
                "  ← 낮을수록 좋음"
            )
            print(f"  금지문구 회피: {neg['phrase_clean']}/{m} ({neg['phrase_clean_pct']}%)")
            print(f"  금지출처 회피: {neg['cited_clean']}/{m} ({neg['cited_clean_pct']}%)")
        else:
            print("  (유보/환각률은 --with-answer 로 답변을 생성해야 측정됩니다)")

    by_cat = aggregated.get("by_category") or {}
    if by_cat:
        print("\n[카테고리별]")
        print(f"  {'카테고리':<14} {'건수':>5} {'통과':>7} {'Hit@5':>7} {'MRR':>7}")
        print("  " + "-" * 46)
        for cat, s in by_cat.items():
            p = s.get("positive") or {}
            hit5 = f"{p['hit_at_5_pct']:>6.1f}%" if p else f"{'-':>7}"
            mrr = f"{p['avg_mrr']:>7.4f}" if p else f"{'-':>7}"
            label = CAT_LABELS.get(cat, cat)
            print(f"  {label:<14} {s['total']:>5} {s['passed_pct']:>6.1f}% {hit5} {mrr}")

    by_vendor = aggregated.get("by_vendor") or {}
    if by_vendor:
        print("\n[벤더별]")
        print(f"  {'벤더':<14} {'건수':>5} {'통과':>7} {'정답통과':>9} {'부정통과':>9}")
        print("  " + "-" * 48)
        for vendor, s in by_vendor.items():
            p, ng = s.get("positive") or {}, s.get("negative") or {}
            pp = f"{p['passed_pct']:>8.1f}%" if p else f"{'-':>9}"
            np_ = f"{ng['passed_pct']:>8.1f}%" if ng else f"{'-':>9}"
            print(f"  {vendor:<14} {s['total']:>5} {s['passed_pct']:>6.1f}% {pp} {np_}")

    by_flavor = aggregated.get("by_negative_flavor") or {}
    if by_flavor:
        print("\n[부정유형별]")
        print(f"  {'유형':<18} {'건수':>5} {'통과':>7} {'금지경로회피':>13}")
        print("  " + "-" * 46)
        for flavor, s in by_flavor.items():
            if not s:
                continue
            label = FLAVOR_LABELS.get(flavor, flavor)
            print(
                f"  {label:<18} {s['total']:>5} {s['passed_pct']:>6.1f}% "
                f"{s['path_clean_pct']:>12.1f}%"
            )

    if failed_cases:
        print(f"\n[실패 케이스] {len(failed_cases)}개")
        for fc in failed_cases:
            if fc["polarity"] == "negative":
                marks = [f"금지경로={'O' if fc['path_clean'] else 'X'}"]
                if fc.get("answer_evaluated"):
                    marks.append(f"유보={'O' if fc['abstained'] else 'X'}")
                    marks.append(f"금지문구={'O' if fc['phrase_clean'] else 'X'}")
                    marks.append(f"금지출처={'O' if fc['cited_clean'] else 'X'}")
                print(f"  [{fc['id']}] {' '.join(marks)} | {fc['query'][:46]}")
                if fc.get("forbidden_path_hits"):
                    print(f"       위반 인용: {fc['forbidden_path_hits'][0][:60]}")
                if fc.get("forbidden_phrases_found"):
                    print(f"       금지 문구: {fc['forbidden_phrases_found']}")
                if fc.get("answer") and not fc.get("abstained"):
                    print(f"       답변: {fc['answer'][:70].replace(chr(10), ' ')}")
            else:
                h5 = "O" if fc["hit_at_5"] else "X"
                km = "O" if fc["keyword_match"] else "X"
                print(f"  [{fc['id']}] Hit@5={h5} KeyMatch={km} | {fc['query'][:46]}")
                if fc["top_results"]:
                    top = fc["top_results"][0]
                    print(f"       1위: {top['path'][:60]} (score={top['score']})")

    print("=" * 68)


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------


def _build_engine(settings: Settings, mode_override: str | None):
    """공통 builder를 호출해 모드별 검색 엔진을 만든다."""
    effective_mode = mode_override or settings.search_mode
    print(f"검색 엔진 초기화 중... (mode={effective_mode})")
    return build_search_engine(settings, mode_override=mode_override)


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
        default="all",
        help="평가할 카테고리 (기본값: all). 데이터셋에 존재하는 값만 허용",
    )
    parser.add_argument(
        "--polarity",
        choices=["all", "positive", "negative"],
        default="all",
        help="평가할 극성 (기본값: all). negative만 돌려 거절 성능만 볼 수 있음",
    )
    parser.add_argument(
        "--vendor",
        default="all",
        help="평가할 벤더 (기본값: all)",
    )
    parser.add_argument(
        "--with-answer",
        action="store_true",
        help="답변까지 생성해 유보/환각/금지문구를 채점 (LLM 호출 발생). "
             "미지정 시 부정 케이스는 검색 단계(금지경로 회피)만 채점",
    )
    parser.add_argument(
        "--llm-backend",
        choices=["openai", "local"],
        default=None,
        help="--with-answer 시 사용할 LLM 백엔드 (기본값: settings 값)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="--with-answer 시 사용할 모델명 오버라이드",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="결과 JSON 저장 경로 (기본값: scripts/validation_results_<timestamp>.json)",
    )
    parser.add_argument(
        "--export-review",
        action="store_true",
        help="결과에 리뷰 템플릿 정보를 포함하여 저장",
    )
    parser.add_argument(
        "--ontology-mode",
        choices=["off", "vector", "hybrid", "ontology"],
        default=None,
        help="검색 모드 오버라이드. 'ontology'는 OntologyAugmentedSearch 활성화. "
             "'off'는 settings.search_mode 사용(기본).",
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

    # 필터 (카테고리 / 극성 / 벤더)
    if args.category != "all":
        available = sorted({tc["category"] for tc in test_cases})
        if args.category not in available:
            parser.error(
                f"--category '{args.category}' 는 데이터셋에 없습니다. 사용 가능: {', '.join(available)}"
            )
        test_cases = [tc for tc in test_cases if tc["category"] == args.category]
    if args.polarity != "all":
        test_cases = [
            tc for tc in test_cases
            if tc.get("polarity", "positive") == args.polarity
        ]
    if args.vendor != "all":
        test_cases = [tc for tc in test_cases if tc.get("vendor") == args.vendor]

    if not test_cases:
        parser.error("필터 조건에 맞는 테스트 케이스가 없습니다.")

    n_neg = sum(1 for tc in test_cases if tc.get("polarity") == "negative")
    print(
        f"평가 대상: {len(test_cases)}개 테스트 케이스 "
        f"(정답 {len(test_cases) - n_neg} / 부정 {n_neg}, "
        f"카테고리: {args.category}, 극성: {args.polarity}, 벤더: {args.vendor})"
    )
    if n_neg and not args.with_answer:
        print(
            "  주의: --with-answer 미지정 — 부정 케이스는 '금지경로 회피'만 채점됩니다.\n"
            "        유보/환각률을 보려면 --with-answer 를 추가하세요."
        )

    # 검색 엔진 초기화 (프로젝트 루트에서 실행)
    os.chdir(_PROJECT_ROOT)
    try:
        mode_override = (
            None if (args.ontology_mode is None or args.ontology_mode == "off")
            else args.ontology_mode
        )
        engine = _build_engine(settings, mode_override=mode_override)

        rag_engine = None
        if args.with_answer:
            from markdown_rag.cli.ask_cmd import _create_llm_backend
            from markdown_rag.retriever.rag import RAGEngine

            if args.llm_backend:
                settings.llm_backend = args.llm_backend
            llm = _create_llm_backend(settings, model_override=args.model)
            rag_engine = RAGEngine(search_engine=engine, llm_backend=llm)
            print(f"답변 채점 활성화 (llm={llm.model_name})")
    finally:
        os.chdir(original_cwd)

    # 평가 루프
    print(f"\n평가 시작 (top_k={args.top_k})...")
    eval_results: list[dict[str, Any]] = []

    os.chdir(_PROJECT_ROOT)
    try:
        for i, test_case in enumerate(test_cases, start=1):
            result = evaluate_single(
                engine, test_case, top_k=args.top_k, rag_engine=rag_engine
            )
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

    report: dict[str, Any] = {
        "run_at": datetime.now().isoformat(),
        "dataset": str(args.dataset),
        "top_k": args.top_k,
        "category_filter": args.category,
        "polarity_filter": args.polarity,
        "vendor_filter": args.vendor,
        "answer_evaluated": bool(rag_engine),
        "summary": aggregated,
        "failed_count": len(failed_cases),
        "results": eval_results,
    }

    # --export-review 플래그: 리뷰 워크플로우 안내 포함
    if getattr(args, "export_review", False):
        report["review_template"] = {
            "ready_for_review": True,
            "failed_count": len(failed_cases),
            "review_cmd": f"python scripts/review_rag.py --results {output_path.name}",
        }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n리포트 저장: {output_path}")

    if getattr(args, "export_review", False):
        print(f"\n리뷰 시작: python scripts/review_rag.py --results {output_path.name}")


if __name__ == "__main__":
    main()
