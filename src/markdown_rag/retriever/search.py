"""LLM-free semantic search engine with optional reranking."""

from __future__ import annotations

import logging

from markdown_rag.embedding.base import EmbeddingBackend
from markdown_rag.models import SearchResult
from markdown_rag.retriever.query_filter import QueryAnalyzer, merge_filters
from markdown_rag.retriever.reranker import CrossEncoderReranker
from markdown_rag.store.base import VectorStore

logger = logging.getLogger(__name__)


class SemanticSearch:
    """Semantic search engine that combines embedding and vector store.

    This is the LLM-free search mode: it embeds a query and finds
    the most similar chunks in the vector store without calling any
    language model. 선택적으로 크로스 인코더 리랭킹을 지원한다.
    """

    def __init__(
        self,
        embedding_backend: EmbeddingBackend,
        vector_store: VectorStore,
        top_k: int = 5,
        reranker: CrossEncoderReranker | None = None,
        initial_top_k: int = 20,
    ) -> None:
        self.embedding_backend = embedding_backend
        self.vector_store = vector_store
        self.top_k = top_k
        self.reranker = reranker
        self.initial_top_k = initial_top_k

    def search(
        self,
        query: str,
        top_k: int | None = None,
        where: dict | None = None,
    ) -> list[SearchResult]:
        """Search for chunks relevant to the query.

        리랭커가 설정된 경우:
        1. initial_top_k로 넓은 후보 검색
        2. 크로스 인코더로 정밀 리랭킹
        3. 최종 top_k 결과 반환

        Args:
            query: The search query string.
            top_k: Number of results to return. Uses instance default
                   if None.
            where: Optional metadata filter (ChromaDB where clause).

        Returns:
            List of SearchResult sorted by score descending, with
            rank assigned starting from 1.
        """
        effective_top_k = top_k if top_k is not None else self.top_k

        # 쿼리 분석 및 자동 필터 생성
        analyzer = QueryAnalyzer()
        intent = analyzer.analyze(query)
        effective_where = merge_filters(intent.metadata_filter, where)

        query_embedding = self.embedding_backend.embed_query(query)

        # 리랭킹 활성화 시 더 넓은 후보를 검색
        fetch_k = self.initial_top_k if self.reranker else effective_top_k

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=fetch_k,
            where=effective_where,
        )

        # 자동 필터 결과가 부족하면 폴백 필터로 재검색
        if len(results) < effective_top_k and intent.metadata_filter is not None:
            fallback_where = merge_filters(intent.fallback_filter, where)
            fallback_results = self.vector_store.search(
                query_embedding=query_embedding,
                top_k=fetch_k,
                where=fallback_where,
            )
            # 기존 결과에 없는 것만 추가
            existing_ids = {r.chunk.chunk_id for r in results}
            for r in fallback_results:
                if r.chunk.chunk_id not in existing_ids:
                    results.append(r)
                    if len(results) >= fetch_k:
                        break

        # 리랭킹
        if self.reranker and results:
            results = self.reranker.rerank(
                query=query,
                results=results,
                top_k=effective_top_k,
            )
        else:
            results.sort(key=lambda r: r.score, reverse=True)
            results = results[:effective_top_k]
            for i, result in enumerate(results):
                result.rank = i + 1

        return results
