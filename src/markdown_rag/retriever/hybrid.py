"""하이브리드 검색 엔진 - 벡터 검색과 BM25를 RRF로 결합한다.

Reciprocal Rank Fusion (RRF)을 사용하여 시맨틱 검색과
키워드 검색의 결과를 결합한다.
"""

from __future__ import annotations

import logging

from markdown_rag.models import SearchResult
from markdown_rag.retriever.bm25 import BM25Index
from markdown_rag.retriever.search import SemanticSearch

logger = logging.getLogger(__name__)

# RRF 상수 (원 논문 권장값)
_RRF_K = 60


class HybridSearch:
    """벡터 검색 + BM25 키워드 검색을 RRF로 결합하는 하이브리드 검색 엔진.

    Args:
        semantic_search: 시맨틱(벡터) 검색 엔진.
        bm25_index: BM25 키워드 검색 인덱스.
        alpha: 벡터 검색 가중치 (0.0~1.0). BM25 가중치는 1-alpha.
    """

    def __init__(
        self,
        semantic_search: SemanticSearch,
        bm25_index: BM25Index,
        alpha: float = 0.7,
    ) -> None:
        if not 0.0 <= alpha <= 1.0:
            msg = f"alpha must be between 0.0 and 1.0, got {alpha}"
            raise ValueError(msg)
        self.semantic_search = semantic_search
        self.bm25_index = bm25_index
        self.alpha = alpha

    def search(
        self,
        query: str,
        top_k: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        """하이브리드 검색을 수행한다.

        1. 벡터 검색과 BM25 검색을 각각 수행 (검색 풀은 top_k * 3)
        2. RRF (Reciprocal Rank Fusion)으로 점수 결합
        3. 최종 top_k 결과 반환

        Args:
            query: 검색 쿼리 문자열.
            top_k: 반환할 최대 결과 수.
            where: 벡터 검색용 메타데이터 필터.

        Returns:
            RRF 점수 기준 내림차순 정렬된 SearchResult 리스트.
        """
        fetch_k = top_k * 3

        # 1. 벡터 검색
        vector_results = self.semantic_search.search(
            query, top_k=fetch_k, where=where
        )

        # 2. BM25 검색
        bm25_results = self.bm25_index.search(query, top_k=fetch_k)

        # 3. RRF 결합
        return self._fuse_results(vector_results, bm25_results, top_k)

    def _fuse_results(
        self,
        vector_results: list[SearchResult],
        bm25_results: list[SearchResult],
        top_k: int,
    ) -> list[SearchResult]:
        """RRF (Reciprocal Rank Fusion)로 두 결과 리스트를 결합한다."""
        # chunk_id -> (chunk, rrf_score) 매핑
        fused: dict[str, tuple[SearchResult, float]] = {}

        # 벡터 검색 결과의 RRF 점수
        for result in vector_results:
            chunk_id = result.chunk.chunk_id
            rrf_score = self.alpha / (_RRF_K + result.rank)
            fused[chunk_id] = (result, rrf_score)

        # BM25 결과의 RRF 점수 추가
        bm25_weight = 1.0 - self.alpha
        for result in bm25_results:
            chunk_id = result.chunk.chunk_id
            rrf_score = bm25_weight / (_RRF_K + result.rank)
            if chunk_id in fused:
                existing_result, existing_score = fused[chunk_id]
                fused[chunk_id] = (existing_result, existing_score + rrf_score)
            else:
                fused[chunk_id] = (result, rrf_score)

        # RRF 점수 기준 정렬
        sorted_items = sorted(
            fused.values(), key=lambda x: x[1], reverse=True
        )[:top_k]

        # SearchResult 생성 (RRF 점수를 score로 사용)
        final_results: list[SearchResult] = []
        for rank, (result, rrf_score) in enumerate(sorted_items, start=1):
            final_results.append(
                SearchResult(
                    chunk=result.chunk,
                    score=rrf_score,
                    rank=rank,
                )
            )

        return final_results
