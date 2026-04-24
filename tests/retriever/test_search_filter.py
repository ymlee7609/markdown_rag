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
        """사용자 where 필터가 벡터 스토어에 올바르게 전달되어야 한다.

        한국어 쿼리는 자동 필터가 생성되지 않으므로 사용자 필터만 그대로 전달된다.
        """
        engine = SemanticSearch(
            embedding_backend=mock_embedding, vector_store=mock_store
        )
        engine.search("스패닝트리 설정", where={"doc_type": "rfc"})
        mock_store.search.assert_called_once_with(
            query_embedding=[0.1, 0.2, 0.3],
            top_k=5,
            where={"doc_type": "rfc"},
        )

    def test_none_filter_passed_by_default(
        self, mock_embedding: MagicMock, mock_store: MagicMock
    ) -> None:
        """사용자 필터 미지정 + 한국어 쿼리이면 None이 전달되어야 한다.

        QueryAnalyzer는 한국어 쿼리에 자동 필터를 생성하지 않으므로,
        사용자가 where를 주지 않으면 store에는 None이 전달된다.
        """
        engine = SemanticSearch(
            embedding_backend=mock_embedding, vector_store=mock_store
        )
        engine.search("스패닝트리 설정")
        mock_store.search.assert_called_once_with(
            query_embedding=[0.1, 0.2, 0.3],
            top_k=5,
            where=None,
        )

    def test_english_query_auto_injects_doc_type_filter(
        self, mock_embedding: MagicMock, mock_store: MagicMock
    ) -> None:
        """영어 쿼리는 자동으로 doc_type ∈ {ccie, rfc} 1차 필터가 주입되어야 한다.

        1차 결과가 top_k에 못 미치면 폴백(language=en) 재검색이 일어날 수 있으므로
        첫 호출만 검증한다.
        """
        engine = SemanticSearch(
            embedding_backend=mock_embedding, vector_store=mock_store
        )
        engine.search("BGP route reflection")
        first_call = mock_store.search.call_args_list[0]
        assert first_call.kwargs == {
            "query_embedding": [0.1, 0.2, 0.3],
            "top_k": 5,
            "where": {"doc_type": {"$in": ["ccie", "rfc"]}},
        }

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
