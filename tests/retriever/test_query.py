"""Tests for HyDE query processor."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from markdown_rag.retriever.query import HyDEProcessor


class TestHyDEProcessor:
    """Test HyDE (Hypothetical Document Embeddings) processor."""

    @pytest.fixture
    def mock_llm(self) -> MagicMock:
        llm = MagicMock()
        llm.generate.return_value = "HTTP is a protocol for web communication."
        return llm

    @pytest.fixture
    def mock_embedding(self) -> MagicMock:
        embedding = MagicMock()
        embedding.embed_query.return_value = [0.1, 0.2, 0.3]
        return embedding

    @pytest.fixture
    def hyde(self, mock_llm: MagicMock, mock_embedding: MagicMock) -> HyDEProcessor:
        return HyDEProcessor(llm_backend=mock_llm, embedding_backend=mock_embedding)

    def test_generates_hypothetical_document(
        self, hyde: HyDEProcessor, mock_llm: MagicMock
    ) -> None:
        hyde.generate_hyde_embedding("What is HTTP?")
        mock_llm.generate.assert_called_once()
        # 프롬프트에 쿼리가 포함되어야 함
        messages = mock_llm.generate.call_args[0][0]
        assert "What is HTTP?" in messages[0]["content"]

    def test_embeds_hypothetical_document(
        self, hyde: HyDEProcessor, mock_embedding: MagicMock
    ) -> None:
        hyde.generate_hyde_embedding("What is HTTP?")
        # LLM 생성 결과를 임베딩해야 함
        mock_embedding.embed_query.assert_called_once_with(
            "HTTP is a protocol for web communication."
        )

    def test_returns_embedding_vector(self, hyde: HyDEProcessor) -> None:
        result = hyde.generate_hyde_embedding("test query")
        assert result == [0.1, 0.2, 0.3]
