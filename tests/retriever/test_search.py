"""Tests for SemanticSearch engine."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from markdown_rag.models import Chunk, SearchResult
from markdown_rag.retriever.search import SemanticSearch


@pytest.fixture
def mock_embedding() -> MagicMock:
    """Create a mock EmbeddingBackend."""
    backend = MagicMock()
    backend.embed_query.return_value = [0.1, 0.2, 0.3]
    return backend


@pytest.fixture
def sample_chunks() -> list[Chunk]:
    """Create sample chunks for testing."""
    return [
        Chunk(
            content="Python is a programming language.",
            doc_path=Path("docs/python.md"),
            headers=["Programming", "Python"],
            chunk_index=0,
        ),
        Chunk(
            content="FastAPI is a modern web framework.",
            doc_path=Path("docs/fastapi.md"),
            headers=["Frameworks", "FastAPI"],
            chunk_index=0,
        ),
        Chunk(
            content="Testing is important for quality.",
            doc_path=Path("docs/testing.md"),
            headers=["Quality", "Testing"],
            chunk_index=1,
        ),
    ]


@pytest.fixture
def mock_store(sample_chunks: list[Chunk]) -> MagicMock:
    """Create a mock VectorStore that returns sample search results."""
    store = MagicMock()
    results = [
        SearchResult(chunk=sample_chunks[0], score=0.95, rank=0),
        SearchResult(chunk=sample_chunks[1], score=0.80, rank=0),
        SearchResult(chunk=sample_chunks[2], score=0.60, rank=0),
    ]
    store.search.return_value = results
    return store


@pytest.fixture
def search_engine(mock_embedding: MagicMock, mock_store: MagicMock) -> SemanticSearch:
    """Create a SemanticSearch instance with mocked dependencies."""
    return SemanticSearch(
        embedding_backend=mock_embedding,
        vector_store=mock_store,
        top_k=5,
    )


class TestSemanticSearchInit:
    """Test SemanticSearch initialization."""

    def test_creates_with_defaults(
        self, mock_embedding: MagicMock, mock_store: MagicMock
    ) -> None:
        engine = SemanticSearch(
            embedding_backend=mock_embedding,
            vector_store=mock_store,
        )
        assert engine.top_k == 5

    def test_creates_with_custom_top_k(
        self, mock_embedding: MagicMock, mock_store: MagicMock
    ) -> None:
        engine = SemanticSearch(
            embedding_backend=mock_embedding,
            vector_store=mock_store,
            top_k=10,
        )
        assert engine.top_k == 10


class TestSemanticSearchSearch:
    """Test SemanticSearch.search() method."""

    def test_embeds_query_using_backend(
        self,
        search_engine: SemanticSearch,
        mock_embedding: MagicMock,
    ) -> None:
        search_engine.search("what is Python?")
        mock_embedding.embed_query.assert_called_once_with("what is Python?")

    def test_searches_store_with_embedding(
        self,
        search_engine: SemanticSearch,
        mock_embedding: MagicMock,
        mock_store: MagicMock,
    ) -> None:
        search_engine.search("what is Python?")
        mock_store.search.assert_called_once_with(
            query_embedding=[0.1, 0.2, 0.3], top_k=5, where=None
        )

    def test_returns_list_of_search_results(
        self, search_engine: SemanticSearch
    ) -> None:
        results = search_engine.search("what is Python?")
        assert isinstance(results, list)
        assert all(isinstance(r, SearchResult) for r in results)

    def test_returns_results_sorted_by_score_descending(
        self, search_engine: SemanticSearch
    ) -> None:
        results = search_engine.search("what is Python?")
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_assigns_rank_based_on_position(
        self, search_engine: SemanticSearch
    ) -> None:
        results = search_engine.search("what is Python?")
        for i, result in enumerate(results):
            assert result.rank == i + 1

    def test_respects_method_level_top_k(
        self,
        search_engine: SemanticSearch,
        mock_store: MagicMock,
    ) -> None:
        search_engine.search("query", top_k=3)
        mock_store.search.assert_called_once_with(
            query_embedding=[0.1, 0.2, 0.3], top_k=3, where=None
        )

    def test_uses_default_top_k_when_none(
        self,
        search_engine: SemanticSearch,
        mock_store: MagicMock,
    ) -> None:
        search_engine.search("query", top_k=None)
        mock_store.search.assert_called_once_with(
            query_embedding=[0.1, 0.2, 0.3], top_k=5, where=None
        )

    def test_returns_correct_count(
        self, search_engine: SemanticSearch
    ) -> None:
        results = search_engine.search("what is Python?")
        assert len(results) == 3


class TestSemanticSearchEdgeCases:
    """Test edge cases for SemanticSearch."""

    def test_empty_results_from_store(
        self, mock_embedding: MagicMock
    ) -> None:
        store = MagicMock()
        store.search.return_value = []
        engine = SemanticSearch(
            embedding_backend=mock_embedding, vector_store=store
        )
        results = engine.search("nonexistent topic")
        assert results == []

    def test_single_result(
        self, mock_embedding: MagicMock, sample_chunks: list[Chunk]
    ) -> None:
        store = MagicMock()
        store.search.return_value = [
            SearchResult(chunk=sample_chunks[0], score=0.9, rank=0),
        ]
        engine = SemanticSearch(
            embedding_backend=mock_embedding, vector_store=store
        )
        results = engine.search("Python")
        assert len(results) == 1
        assert results[0].rank == 1
        assert results[0].score == 0.9

    def test_results_with_unsorted_scores_are_sorted(
        self, mock_embedding: MagicMock, sample_chunks: list[Chunk]
    ) -> None:
        store = MagicMock()
        store.search.return_value = [
            SearchResult(chunk=sample_chunks[2], score=0.3, rank=0),
            SearchResult(chunk=sample_chunks[0], score=0.9, rank=0),
            SearchResult(chunk=sample_chunks[1], score=0.6, rank=0),
        ]
        engine = SemanticSearch(
            embedding_backend=mock_embedding, vector_store=store
        )
        results = engine.search("mixed")
        scores = [r.score for r in results]
        assert scores == [0.9, 0.6, 0.3]

    def test_results_preserve_chunk_data(
        self,
        search_engine: SemanticSearch,
        sample_chunks: list[Chunk],
    ) -> None:
        results = search_engine.search("Python")
        assert results[0].chunk.content == "Python is a programming language."
        assert results[0].chunk.doc_path == Path("docs/python.md")
        assert results[0].chunk.header_context == "Programming > Python"
