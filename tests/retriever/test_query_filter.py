"""쿼리 분석기 및 필터 생성 테스트."""

from __future__ import annotations

import pytest

from markdown_rag.retriever.query_filter import (
    QueryAnalyzer,
    merge_filters,
)


class TestQueryAnalyzer:
    """QueryAnalyzer 쿼리 분석 테스트."""

    def setup_method(self) -> None:
        self.analyzer = QueryAnalyzer()

    # -- 벤더 감지 --

    @pytest.mark.parametrize(
        "query,expected_vendor",
        [
            ("다산 L2 장비 목록", "다산"),
            ("유비쿼스 OLT 장비", "유비쿼스"),
            ("dasan L2 equipment", "다산"),
            ("ubiquoss switch", "유비쿼스"),
        ],
    )
    def test_detects_vendor(self, query: str, expected_vendor: str) -> None:
        """벤더 키워드를 올바르게 감지해야 한다."""
        intent = self.analyzer.analyze(query)
        assert intent.detected_vendor == expected_vendor

    def test_no_vendor_detected(self) -> None:
        """벤더 키워드가 없으면 None을 반환해야 한다."""
        intent = self.analyzer.analyze("RFC 9110 내용 알려줘")
        assert intent.detected_vendor is None

    # -- 카테고리 감지 --

    @pytest.mark.parametrize(
        "query,expected_category",
        [
            ("다산 L2 장비", "L2"),
            ("L3 스위치 설정", "L3"),
            ("OLT 장비 목록", "OLT"),
        ],
    )
    def test_detects_category(
        self, query: str, expected_category: str
    ) -> None:
        """카테고리 키워드를 올바르게 감지해야 한다."""
        intent = self.analyzer.analyze(query)
        assert intent.detected_category == expected_category

    def test_no_category_detected(self) -> None:
        """카테고리 키워드가 없으면 None을 반환해야 한다."""
        intent = self.analyzer.analyze("다산 장비 목록")
        assert intent.detected_category is None

    # -- 목록 쿼리 감지 --

    @pytest.mark.parametrize(
        "query",
        [
            "다산 L2 장비 목록",
            "장비 리스트 알려줘",
            "어떤 모델이 있나",
            "list all equipment",
        ],
    )
    def test_detects_listing_query(self, query: str) -> None:
        """목록 쿼리 키워드를 감지해야 한다."""
        intent = self.analyzer.analyze(query)
        assert intent.is_listing_query is True

    def test_non_listing_query(self) -> None:
        """목록 쿼리가 아닌 경우 False를 반환해야 한다."""
        intent = self.analyzer.analyze("RSTP 설정 방법 알려줘")
        assert intent.is_listing_query is False

    # -- 필터 생성 --

    def test_vendor_only_filter(self) -> None:
        """벤더만 감지 시 단일 필터를 생성해야 한다."""
        intent = self.analyzer.analyze("다산 스위치 설정")
        assert intent.metadata_filter == {"vendor": "다산"}

    def test_vendor_category_listing_filter(self) -> None:
        """벤더+카테고리+목록 감지 시 $and 필터를 생성해야 한다."""
        intent = self.analyzer.analyze("다산 L2 장비 목록")
        assert intent.metadata_filter is not None
        assert "$and" in intent.metadata_filter
        conditions = intent.metadata_filter["$and"]
        # vendor + category + directory_index
        assert {"vendor": "다산"} in conditions
        assert {"category": "L2"} in conditions
        assert {"doc_type": "directory_index"} in conditions

    def test_no_filter_for_generic_query(self) -> None:
        """일반 쿼리에는 필터가 생성되지 않아야 한다."""
        intent = self.analyzer.analyze("RSTP 설정 방법")
        assert intent.metadata_filter is None

    # -- 언어 자동 감지 --

    # -- CCIE 우선 검색 (영어 쿼리) --

    @pytest.mark.parametrize(
        "query",
        [
            "TCP three-way handshake",
            "BGP autonomous system path",
            "OSPF hello packet neighbor",
            "IPv6 addressing architecture",
            "HTTP persistent connections keep-alive",
        ],
    )
    def test_english_query_gets_ccie_primary_filter(self, query: str) -> None:
        """영어 쿼리는 doc_type ∈ {ccie, rfc} 1차 필터 + language=en 폴백을 생성해야 한다.

        RFC 콘텐츠가 추가된 후 영어 기술 문서 둘 다 우선 검색 대상에 포함된다.
        """
        intent = self.analyzer.analyze(query)
        assert intent.detected_language == "en"
        assert intent.metadata_filter == {"doc_type": {"$in": ["ccie", "rfc"]}}
        assert intent.fallback_filter == {"language": "en"}

    @pytest.mark.parametrize(
        "query",
        [
            "다산 L2 스위치 VLAN 설정",
            "IGMP QRV 설정 방법",
            "유비쿼스 OLT 업링크 구성",
            "스패닝트리 Root 스위치",
        ],
    )
    def test_korean_query_no_language_filter(self, query: str) -> None:
        """한국어 쿼리는 language 필터를 생성하지 않아야 한다."""
        intent = self.analyzer.analyze(query)
        assert intent.detected_language is None
        assert intent.fallback_filter is None

    def test_english_vendor_query_uses_vendor_filter(self) -> None:
        """영어 벤더 쿼리는 vendor/category 필터만 사용하고 CCIE 우선을 건너뛰어야 한다."""
        intent = self.analyzer.analyze("dasan L2 equipment")
        assert intent.detected_vendor == "다산"
        assert intent.detected_language == "en"
        assert intent.metadata_filter is not None
        assert "$and" in intent.metadata_filter
        conditions = intent.metadata_filter["$and"]
        assert {"vendor": "다산"} in conditions
        assert {"category": "L2"} in conditions
        # vendor 감지 시 CCIE 우선 및 language 필터 미적용
        assert intent.fallback_filter is None

    def test_mixed_query_no_language_filter(self) -> None:
        """한국어 문자가 포함된 혼합 쿼리는 언어 필터를 생성하지 않아야 한다."""
        intent = self.analyzer.analyze("OSPF 설정 how to configure")
        assert intent.detected_language is None
        assert intent.fallback_filter is None

    def test_original_query_preserved(self) -> None:
        """원본 쿼리가 보존되어야 한다."""
        query = "다산 L2 장비 목록"
        intent = self.analyzer.analyze(query)
        assert intent.original_query == query


class TestMergeFilters:
    """필터 병합 테스트."""

    def test_both_none(self) -> None:
        """둘 다 None이면 None을 반환해야 한다."""
        assert merge_filters(None, None) is None

    def test_auto_only(self) -> None:
        """자동 필터만 있으면 자동 필터를 반환해야 한다."""
        auto = {"vendor": "다산"}
        assert merge_filters(auto, None) == auto

    def test_user_only(self) -> None:
        """사용자 필터만 있으면 사용자 필터를 반환해야 한다."""
        user = {"doc_type": "telecom_manual"}
        assert merge_filters(None, user) == user

    def test_both_present(self) -> None:
        """둘 다 있으면 $and로 결합해야 한다."""
        auto = {"vendor": "다산"}
        user = {"language": "ko"}
        result = merge_filters(auto, user)
        assert result == {"$and": [auto, user]}
