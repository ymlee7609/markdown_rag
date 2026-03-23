"""LLM-free semantic search engine."""

from __future__ import annotations

import logging

from markdown_rag.embedding.base import EmbeddingBackend
from markdown_rag.models import SearchResult
from markdown_rag.store.base import VectorStore

logger = logging.getLogger(__name__)


class SemanticSearch:
    """Semantic search engine that combines embedding and vector store.

    This is the LLM-free search mode: it embeds a query and finds
    the most similar chunks in the vector store without calling any
    language model.
    """

    def __init__(
        self,
        embedding_backend: EmbeddingBackend,
        vector_store: VectorStore,
        top_k: int = 5,
    ) -> None:
        self.embedding_backend = embedding_backend
        self.vector_store = vector_store
        self.top_k = top_k

    def search(
        self, query: str, top_k: int | None = None
    ) -> list[SearchResult]:
        """Search for chunks relevant to the query.

        Args:
            query: The search query string.
            top_k: Number of results to return. Uses instance default
                   if None.

        Returns:
            List of SearchResult sorted by score descending, with
            rank assigned starting from 1.
        """
        effective_top_k = top_k if top_k is not None else self.top_k

        query_embedding = self.embedding_backend.embed_query(query)

        results = self.vector_store.search(
            query_embedding=query_embedding, top_k=effective_top_k
        )

        results.sort(key=lambda r: r.score, reverse=True)

        for i, result in enumerate(results):
            result.rank = i + 1

        return results
