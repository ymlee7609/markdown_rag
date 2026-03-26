"""쿼리 분석 및 자동 메타데이터 필터 생성.

사용자 쿼리에서 벤더, 카테고리, 목록 키워드를 감지하여
ChromaDB 메타데이터 필터를 자동으로 구성한다.
"""

from __future__ import annotations

import logging
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
    is_listing_query: bool = False
    detected_vendor: str | None = None
    detected_category: str | None = None


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

        metadata_filter = self._build_filter(vendor, category, is_listing)

        intent = QueryIntent(
            original_query=query,
            metadata_filter=metadata_filter,
            is_listing_query=is_listing,
            detected_vendor=vendor,
            detected_category=category,
        )

        if vendor or category or is_listing:
            logger.info(
                "쿼리 분석: vendor=%s, category=%s, listing=%s",
                vendor, category, is_listing,
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

    def _build_filter(
        self,
        vendor: str | None,
        category: str | None,
        is_listing: bool,
    ) -> dict | None:
        """감지된 키워드로 ChromaDB where 필터를 구성한다."""
        conditions: list[dict] = []

        if vendor:
            conditions.append({"vendor": vendor})
        if category:
            conditions.append({"category": category})

        # 목록 쿼리이면 directory_index 문서를 우선 검색
        if is_listing:
            conditions.append({"doc_type": "directory_index"})

        if not conditions:
            return None
        if len(conditions) == 1:
            return conditions[0]
        return {"$and": conditions}


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
