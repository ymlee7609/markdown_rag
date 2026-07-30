"""validate_rag.py 의 negative 분기 채점 로직 테스트.

실제 인덱스/LLM 없이 가짜 엔진으로 채점 규칙만 검증한다.

validate_rag 는 모듈 임포트 시점에 Settings(pydantic-settings)와 검색 엔진 빌더를
끌어오지만, 채점 함수 자체는 이들과 무관한 순수 함수다. 검증 환경에 무거운
런타임 의존성이 없어도 채점 규칙을 테스트할 수 있도록 두 모듈만 스텁으로 대체한다.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "src"))

from markdown_rag.models import Chunk, RAGResponse, SearchResult  # noqa: E402


def _stub(name: str, **attrs) -> None:
    """이미 로드돼 있지 않은 경우에만 스텁 모듈을 심는다."""
    if name in sys.modules:
        return
    mod = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(mod, key, value)
    sys.modules[name] = mod


_stub("markdown_rag.config", Settings=object)
_stub("markdown_rag.retriever.builder", build_search_engine=lambda *a, **k: None)

_spec = importlib.util.spec_from_file_location(
    "validate_rag", _ROOT / "scripts/validate_rag.py"
)
validate_rag = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_rag)


# ---------------------------------------------------------------- 테스트 더블

def make_results(paths: list[str]) -> list[SearchResult]:
    return [
        SearchResult(
            chunk=Chunk(content=f"content of {p}", doc_path=Path(p), headers=["H"]),
            score=1.0 - i * 0.1,
            rank=i + 1,
        )
        for i, p in enumerate(paths)
    ]


class FakeSearch:
    def __init__(self, paths: list[str]) -> None:
        self._results = make_results(paths)

    def search(self, query, top_k=None, where=None):  # noqa: ARG002
        return self._results[: (top_k or len(self._results))]


class FakeRAG:
    def __init__(self, answer: str, sources: list[str]) -> None:
        self._answer = answer
        self._sources = make_results(sources)

    def ask(self, query, top_k=None, show_sources=True):  # noqa: ARG002
        return RAGResponse(
            answer=self._answer,
            sources=self._sources if show_sources else [],
            model="fake",
            query=query,
        )


NEG_CASE = {
    "id": "T-NEG-001",
    "category": "negative",
    "polarity": "negative",
    "vendor": "다산_L2",
    "negative_flavor": "cross_vendor_syntax",
    "query": "다산 V3024V에서 self-loop-detection 설정 방법은?",
    "expected_behavior": "reject_premise",
    "fail_if_answer_contains": ["self-loop-detection", "no self-loop"],
    "must_not_cite_path_contains": ["유비쿼스_L2"],
}

POS_CASE = {
    "id": "T-POS-001",
    "category": "spec_value",
    "polarity": "positive",
    "vendor": "유비쿼스_OLT",
    "query": "U9500H의 소비 전력은?",
    "expected_path_contains": "유비쿼스_OLT/U9500H",
    "expected_keywords": ["U9500H"],
}


# ---------------------------------------------------------------- 판정 헬퍼

def test_abstain_detection_ko_and_en():
    assert validate_rag.check_abstained("제공된 매뉴얼에서 찾을 수 없습니다.")
    assert validate_rag.check_abstained("해당 명령이 없습니다.")
    assert validate_rag.check_abstained("No information is available in the manual.")
    assert not validate_rag.check_abstained("소비 전력은 1550W입니다.")
    assert not validate_rag.check_abstained("")


def test_forbidden_paths_detects_violation():
    results = make_results(["유비쿼스_L2/E57xxRC.md", "다산_L2/V3024V.md"])
    ok, hits = validate_rag.check_forbidden_paths(results, ["유비쿼스_L2"], k=5)
    assert not ok
    assert hits == ["유비쿼스_L2/E57xxRC.md"]


def test_forbidden_paths_passes_when_clean():
    results = make_results(["다산_L2/V3024V.md"])
    ok, hits = validate_rag.check_forbidden_paths(results, ["유비쿼스_L2"], k=5)
    assert ok and hits == []


def test_forbidden_phrases_case_insensitive():
    ok, found = validate_rag.check_forbidden_phrases(
        "Switch(config)# SELF-LOOP-DETECTION 을 입력합니다", ["self-loop-detection"]
    )
    assert not ok
    assert found == ["self-loop-detection"]


# ---------------------------------------------------------------- 부정 케이스

def test_negative_retrieval_only_passes_when_path_clean():
    """--with-answer 없이 금지 경로만 피하면 통과."""
    r = validate_rag.evaluate_single(FakeSearch(["다산_L2/V3024V.md"]), NEG_CASE, top_k=5)
    assert r["polarity"] == "negative"
    assert r["passed"] is True
    assert r["pass_basis"] == "retrieval_only"
    assert r["answer_evaluated"] is False
    # 회수 지표는 의미가 없으므로 None
    assert r["hit_at_5"] is None and r["mrr"] is None


def test_negative_retrieval_only_fails_on_forbidden_path():
    r = validate_rag.evaluate_single(
        FakeSearch(["유비쿼스_L2/E57xxRC.md"]), NEG_CASE, top_k=5
    )
    assert r["passed"] is False
    assert r["forbidden_path_hits"]


def test_negative_answer_pass_when_abstained():
    rag = FakeRAG("다산 V3024V에는 해당 명령이 없습니다.", ["다산_L2/V3024V.md"])
    r = validate_rag.evaluate_single(
        FakeSearch(["다산_L2/V3024V.md"]), NEG_CASE, top_k=5, rag_engine=rag
    )
    assert r["passed"] is True
    assert r["pass_basis"] == "answer"
    assert r["abstained"] is True


def test_negative_answer_fails_on_hallucination():
    """유보하지 않고 절차를 지어내면 실패."""
    rag = FakeRAG("Switch(config)# self-loop-detection 으로 설정합니다.", ["다산_L2/V3024V.md"])
    r = validate_rag.evaluate_single(
        FakeSearch(["다산_L2/V3024V.md"]), NEG_CASE, top_k=5, rag_engine=rag
    )
    assert r["passed"] is False
    assert r["abstained"] is False
    assert r["phrase_clean"] is False
    assert "self-loop-detection" in r["forbidden_phrases_found"]


def test_negative_answer_fails_when_citing_forbidden_source():
    """유보했더라도 금지 경로를 출처로 인용하면 실패."""
    rag = FakeRAG("찾을 수 없습니다.", ["유비쿼스_L2/E57xxRC.md"])
    r = validate_rag.evaluate_single(
        FakeSearch(["다산_L2/V3024V.md"]), NEG_CASE, top_k=5, rag_engine=rag
    )
    assert r["abstained"] is True
    assert r["cited_clean"] is False
    assert r["passed"] is False


# ---------------------------------------------------------------- 정답 케이스

def test_positive_unchanged_without_polarity_field():
    """polarity 필드가 없는 기존 데이터셋도 positive로 동작."""
    legacy = {k: v for k, v in POS_CASE.items() if k != "polarity"}
    r = validate_rag.evaluate_single(
        FakeSearch(["유비쿼스_OLT/U9500H_HW.md"]), legacy, top_k=5
    )
    assert r["polarity"] == "positive"
    assert r["passed"] is True
    assert r["hit_at_1"] is True


def test_positive_over_abstain_flagged():
    """회수는 됐는데 모른다고 답하면 과잉 유보로 표시."""
    rag = FakeRAG("찾을 수 없습니다.", ["유비쿼스_OLT/U9500H_HW.md"])
    r = validate_rag.evaluate_single(
        FakeSearch(["유비쿼스_OLT/U9500H_HW.md"]), POS_CASE, top_k=5, rag_engine=rag
    )
    assert r["hit_at_5"] is True
    assert r["over_abstained"] is True


# ---------------------------------------------------------------- 집계

def test_aggregate_separates_polarity():
    results = [
        validate_rag.evaluate_single(FakeSearch(["유비쿼스_OLT/U9500H_HW.md"]), POS_CASE, 5),
        validate_rag.evaluate_single(FakeSearch(["유비쿼스_L2/E57xxRC.md"]), NEG_CASE, 5),
    ]
    agg = validate_rag.aggregate_results(results)
    assert agg["overall"]["total"] == 2
    assert agg["positive"]["total"] == 1
    assert agg["negative"]["total"] == 1
    assert agg["negative"]["path_clean"] == 0
    # 부정 케이스가 Hit@k 평균을 오염시키지 않아야 한다
    assert agg["positive"]["hit_at_5_pct"] == 100.0
    assert "cross_vendor_syntax" in agg["by_negative_flavor"]
    assert set(agg["by_vendor"]) == {"유비쿼스_OLT", "다산_L2"}


def test_aggregate_handles_negative_only_run():
    """--polarity negative 로 부정 케이스만 돌려도 집계가 깨지지 않아야 한다."""
    results = [validate_rag.evaluate_single(FakeSearch(["다산_L2/V3024V.md"]), NEG_CASE, 5)]
    agg = validate_rag.aggregate_results(results)
    assert agg["positive"] == {}
    assert agg["negative"]["passed_pct"] == 100.0
    validate_rag.print_summary(agg, [])  # 출력 경로에 예외가 없어야 한다


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
