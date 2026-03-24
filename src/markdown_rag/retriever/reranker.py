"""크로스 인코더 기반 리랭킹 모듈.

1차 검색 결과를 크로스 인코더로 정밀 리랭킹하여
최종 결과의 관련성을 향상시킨다.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sentence_transformers import CrossEncoder

from markdown_rag.models import SearchResult

logger = logging.getLogger(__name__)


class CrossEncoderReranker:
    """크로스 인코더 기반 리랭커.

    쿼리-문서 쌍을 크로스 인코더에 입력하여
    더 정밀한 관련성 점수를 계산한다.

    Args:
        model_name: CrossEncoder 모델 이름.
            기본값: 'BAAI/bge-reranker-v2-m3' (다국어 지원).
    """

    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3") -> None:
        self.model_name = model_name
        self._model: CrossEncoder | None = None

    def _load_model(self) -> CrossEncoder:
        """크로스 인코더 모델을 지연 로드한다."""
        if self._model is None:
            from sentence_transformers import CrossEncoder

            logger.info("Loading cross-encoder model: %s", self.model_name)
            self._model = CrossEncoder(self.model_name)
        return self._model

    def rerank(
        self,
        query: str,
        results: list[SearchResult],
        top_k: int = 5,
    ) -> list[SearchResult]:
        """검색 결과를 크로스 인코더로 리랭킹한다.

        Args:
            query: 원본 쿼리 문자열.
            results: 1차 검색 결과 리스트.
            top_k: 리랭킹 후 반환할 최대 결과 수.

        Returns:
            크로스 인코더 점수 기준 내림차순 정렬된 SearchResult 리스트.
        """
        if not results:
            return []

        model = self._load_model()

        # 쿼리-문서 쌍 생성
        pairs = [[query, r.chunk.content] for r in results]

        # 크로스 인코더 점수 계산
        scores = model.predict(pairs)

        # 점수와 결과를 매핑하여 정렬
        scored_results = list(zip(results, scores))
        scored_results.sort(key=lambda x: float(x[1]), reverse=True)

        # 상위 top_k 결과 반환 (새 rank 부여)
        reranked: list[SearchResult] = []
        for rank, (result, score) in enumerate(scored_results[:top_k], start=1):
            reranked.append(
                SearchResult(
                    chunk=result.chunk,
                    score=float(score),
                    rank=rank,
                )
            )

        return reranked
