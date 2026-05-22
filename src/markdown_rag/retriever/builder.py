"""Search engine builder factory.

Builds the appropriate search engine (SemanticSearch / HybridSearch /
OntologyAugmentedSearch) based on Settings.search_mode, so CLI / API
endpoints can stay backend-agnostic.

The returned object always exposes `search(query, top_k, where=None) ->
list[SearchResult]` so callers (RAGEngine, search_cmd, api routes) do not
need to know which backend is active.
"""

from __future__ import annotations

import logging
from typing import Protocol, runtime_checkable

from markdown_rag.config import Settings
from markdown_rag.embedding.local import LocalEmbedding
from markdown_rag.embedding.openai import OpenAIEmbedding
from markdown_rag.models import SearchResult
from markdown_rag.retriever.bm25 import BM25Index
from markdown_rag.retriever.hybrid import HybridSearch
from markdown_rag.retriever.ontology_aug import OntologyAugmentedSearch
from markdown_rag.retriever.search import SemanticSearch
from markdown_rag.store.chroma import ChromaStore

logger = logging.getLogger(__name__)


@runtime_checkable
class SearchEngine(Protocol):
    """Protocol for any object usable by RAGEngine / CLI / API routes."""

    def search(
        self,
        query: str,
        top_k: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]: ...


def _build_embedding(settings: Settings):
    if settings.embedding_backend == "openai":
        return OpenAIEmbedding(model_name=settings.openai_embedding_model)
    return LocalEmbedding(model_name=settings.local_model)


def build_search_engine(
    settings: Settings,
    mode_override: str | None = None,
) -> SearchEngine:
    """Construct a search engine according to settings.search_mode.

    Args:
        settings: Application settings.
        mode_override: Optional CLI/API override for search mode
            (one of "vector"/"bm25"/"hybrid"/"ontology"). When None,
            uses settings.search_mode.

    Returns:
        Object with `search(...)` method. Mode-specific behavior:

        - "vector":   SemanticSearch only.
        - "bm25":     SemanticSearch fallback (BM25-only retrieval is not
                      directly supported as a primary engine in this
                      codebase; reserved for future).
        - "hybrid":   HybridSearch (Chroma + BM25 RRF).
        - "ontology": OntologyAugmentedSearch wrapping two HybridSearch
                      engines (main + ontology corpora) plus referenced-
                      path expansion.

    Raises:
        FileNotFoundError: For modes that need persisted indexes
            (BM25 file or ontology onto_refs.json) when those are missing.
    """
    mode = mode_override or settings.search_mode

    embedding = _build_embedding(settings)
    main_store = ChromaStore(
        persist_path=settings.chroma_path,
        collection_name=settings.collection_name,
    )

    if mode == "vector":
        return SemanticSearch(
            embedding_backend=embedding,
            vector_store=main_store,
            top_k=settings.search_top_k,
        )

    if mode == "bm25":
        # BM25-only as a primary engine is not wired into RAGEngine here;
        # fall through to vector to preserve existing behavior.
        logger.warning("search_mode='bm25' as a primary engine is not "
                       "implemented; falling back to vector-only.")
        return SemanticSearch(
            embedding_backend=embedding,
            vector_store=main_store,
            top_k=settings.search_top_k,
        )

    if mode == "hybrid":
        semantic = SemanticSearch(
            embedding_backend=embedding,
            vector_store=main_store,
            top_k=settings.search_top_k * 3,
        )
        bm25 = BM25Index.load(settings.bm25_index_path)
        return HybridSearch(
            semantic_search=semantic,
            bm25_index=bm25,
            alpha=settings.hybrid_alpha,
        )

    if mode == "ontology":
        # Main hybrid engine
        main_semantic = SemanticSearch(
            embedding_backend=embedding,
            vector_store=main_store,
            top_k=settings.search_top_k * 3,
        )
        main_bm25 = BM25Index.load(settings.bm25_index_path)
        main_hybrid = HybridSearch(
            semantic_search=main_semantic,
            bm25_index=main_bm25,
            alpha=settings.hybrid_alpha,
        )
        # Ontology side engine
        onto_store = ChromaStore(
            persist_path=settings.onto_chroma_path,
            collection_name=settings.onto_collection_name,
        )
        onto_semantic = SemanticSearch(
            embedding_backend=embedding,
            vector_store=onto_store,
            top_k=settings.search_top_k * 3,
        )
        onto_bm25 = BM25Index.load(settings.onto_bm25_path)
        onto_hybrid = HybridSearch(
            semantic_search=onto_semantic,
            bm25_index=onto_bm25,
            alpha=settings.hybrid_alpha,
        )
        return OntologyAugmentedSearch(
            main_search=main_hybrid,
            onto_search=onto_hybrid,
            main_store=main_store,
            onto_refs_path=settings.onto_refs_path,
            inject_top_n_cards=settings.onto_inject_top_n_cards,
            inject_chunks_per_card=settings.onto_inject_chunks_per_card,
        )

    raise ValueError(f"Unknown search mode: {mode}")
