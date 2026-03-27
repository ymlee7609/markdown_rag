"""쿼리 분석 및 자동 메타데이터 필터 생성.

사용자 쿼리에서 벤더, 카테고리, 목록 키워드를 감지하여
ChromaDB 메타데이터 필터를 자동으로 구성한다.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 벤더 키워드 매핑
_VENDOR_KEYWORDS: dict[str, str] = {
    "다산": "다산",
    "dasan": "다산",
    "유비쿼스": "유비쿼스",
    "ubiquoss": "유비쿼스",
}

# 카테고리 키워드 매핑
_CATEGORY_KEYWORDS: dict[str, str] = {
    "l2": "L2",
    "l3": "L3",
    "olt": "OLT",
}

# 한국어 문자 범위 패턴 (가-힣: 완성형 한글)
_KO_PATTERN = re.compile(r"[가-힣]")

# 목록/구조 쿼리 키워드
_LISTING_KEYWORDS: set[str] = {
    "목록",
    "리스트",
    "list",
    "종류",
    "장비",
    "모델",
    "어떤",
}


@dataclass
class QueryIntent:
    """쿼리 분석 결과."""

    original_query: str
    metadata_filter: dict | None = None
    fallback_filter: dict | None = None
    is_listing_query: bool = False
    detected_vendor: str | None = None
    detected_category: str | None = None
    detected_language: str | None = None


class QueryAnalyzer:
    """사용자 쿼리를 분석하여 메타데이터 필터를 자동 생성한다."""

    def analyze(self, query: str) -> QueryIntent:
        """쿼리에서 벤더, 카테고리, 목록 키워드를 감지한다.

        Args:
            query: 사용자 쿼리 문자열.

        Returns:
            분석된 QueryIntent.
        """
        query_lower = query.lower()

        vendor = self._detect_vendor(query_lower)
        category = self._detect_category(query_lower)
        is_listing = self._detect_listing(query_lower)
        language = self._detect_language(query)

        metadata_filter, fallback_filter = self._build_filter(
            vendor, category, is_listing, language,
        )

        intent = QueryIntent(
            original_query=query,
            metadata_filter=metadata_filter,
            fallback_filter=fallback_filter,
            is_listing_query=is_listing,
            detected_vendor=vendor,
            detected_category=category,
            detected_language=language,
        )

        if vendor or category or is_listing or language:
            logger.info(
                "쿼리 분석: vendor=%s, category=%s, listing=%s, language=%s",
                vendor, category, is_listing, language,
            )

        return intent

    def _detect_vendor(self, query_lower: str) -> str | None:
        """쿼리에서 벤더 키워드를 감지한다."""
        for keyword, vendor in _VENDOR_KEYWORDS.items():
            if keyword in query_lower:
                return vendor
        return None

    def _detect_category(self, query_lower: str) -> str | None:
        """쿼리에서 카테고리 키워드를 감지한다."""
        for keyword, category in _CATEGORY_KEYWORDS.items():
            if keyword in query_lower:
                return category
        return None

    def _detect_listing(self, query_lower: str) -> bool:
        """쿼리가 목록/구조 쿼리인지 감지한다."""
        return any(kw in query_lower for kw in _LISTING_KEYWORDS)

    def _detect_language(self, query: str) -> str | None:
        """쿼리 언어를 감지하여 언어 필터 값을 반환한다.

        한국어 문자(가-힣)가 없으면 영어 문서만 검색하도록 "en"을 반환한다.
        한국어 문자가 포함된 경우 언어 필터를 적용하지 않는다(전체 검색).

        Args:
            query: 원본 쿼리 문자열.

        Returns:
            "en" (영어 쿼리), None (한국어 또는 혼합 쿼리).
        """
        if _KO_PATTERN.search(query):
            return None
        return "en"

    @staticmethod
    def _combine_conditions(conditions: list[dict]) -> dict | None:
        """조건 리스트를 ChromaDB where 절로 조합한다."""
        if not conditions:
            return None
        if len(conditions) == 1:
            return conditions[0]
        return {"$and": conditions}

    def _build_filter(
        self,
        vendor: str | None,
        category: str | None,
        is_listing: bool,
        language: str | None = None,
    ) -> tuple[dict | None, dict | None]:
        """감지된 키워드로 ChromaDB where 필터를 구성한다.

        Returns:
            (primary_filter, fallback_filter) 튜플.
            primary_filter: 1차 검색에 사용할 필터.
            fallback_filter: 1차 결과 부족 시 사용할 폴백 필터.
        """
        conditions: list[dict] = []

        if vendor:
            conditions.append({"vendor": vendor})
        if category:
            conditions.append({"category": category})

        # 목록 쿼리이면 directory_index 문서를 우선 검색
        if is_listing:
            conditions.append({"doc_type": "directory_index"})

        # 영어 쿼리 + vendor/category/listing 미감지 → CCIE 우선, 영어 폴백
        if language == "en" and not vendor and not category and not is_listing:
            primary = self._combine_conditions(
                conditions + [{"doc_type": "ccie"}],
            )
            fallback = self._combine_conditions(
                conditions + [{"language": "en"}],
            )
            return primary, fallback

        # vendor/category/listing 감지 → 기존 동작 (language 필터 불필요)
        if conditions:
            return self._combine_conditions(conditions), None

        # 한국어 쿼리 등 → 필터 없음
        return None, None


def merge_filters(
    auto_filter: dict | None,
    user_filter: dict | None,
) -> dict | None:
    """자동 필터와 사용자 필터를 병합한다.

    Args:
        auto_filter: QueryAnalyzer가 생성한 자동 필터.
        user_filter: 사용자가 CLI/API에서 지정한 필터.

    Returns:
        병합된 ChromaDB where 절.
    """
    if auto_filter is None:
        return user_filter
    if user_filter is None:
        return auto_filter

    # 둘 다 존재하면 $and로 결합
    return {"$and": [auto_filter, user_filter]}
