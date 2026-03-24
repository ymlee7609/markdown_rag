"""Tests for SemanticSearch with metadata filtering."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from markdown_rag.models import Chunk, SearchResult
from markdown_rag.retriever.search import SemanticSearch


@pytest.fixture
def mock_embedding() -> MagicMock:
    backend = MagicMock()
    backend.embed_query.return_value = [0.1, 0.2, 0.3]
    return backend


@pytest.fixture
def mock_store() -> MagicMock:
    store = MagicMock()
    store.search.return_value = [
        SearchResult(
            chunk=Chunk(
                content="test",
                doc_path=Path("test.md"),
                chunk_index=0,
            ),
            score=0.9,
        ),
    ]
    return store


class TestSemanticSearchFilter:
    """Test that SemanticSearch passes where filter to vector store."""

    def test_passes_where_filter_to_store(
        self, mock_embedding: MagicMock, mock_store: MagicMock
    ) -> None:
        """where 필터가 벡터 스토어에 올바르게 전달되어야 한다."""
        engine = SemanticSearch(
            embedding_backend=mock_embedding, vector_store=mock_store
        )
        engine.search("query", where={"doc_type": "rfc"})
        mock_store.search.assert_called_once_with(
            query_embedding=[0.1, 0.2, 0.3],
            top_k=5,
            where={"doc_type": "rfc"},
        )

    def test_none_filter_passed_by_default(
        self, mock_embedding: MagicMock, mock_store: MagicMock
    ) -> None:
        """필터를 지정하지 않으면 None이 전달되어야 한다."""
        engine = SemanticSearch(
            embedding_backend=mock_embedding, vector_store=mock_store
        )
        engine.search("query")
        mock_store.search.assert_called_once_with(
            query_embedding=[0.1, 0.2, 0.3],
            top_k=5,
            where=None,
        )

    def test_complex_filter(
        self, mock_embedding: MagicMock, mock_store: MagicMock
    ) -> None:
        """복합 필터($and)가 올바르게 전달되어야 한다."""
        engine = SemanticSearch(
            embedding_backend=mock_embedding, vector_store=mock_store
        )
        where = {"$and": [{"doc_type": "telecom_manual"}, {"language": "ko"}]}
        engine.search("SNMP 설정", where=where)
        mock_store.search.assert_called_once_with(
            query_embedding=[0.1, 0.2, 0.3],
            top_k=5,
            where=where,
        )
