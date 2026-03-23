"""Tests for OpenAIEmbedding backend using openai library."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from markdown_rag.embedding.base import EmbeddingBackend
from markdown_rag.embedding.openai import OpenAIEmbedding


class TestOpenAIEmbeddingInit:
    """Test OpenAIEmbedding initialization."""

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    def test_default_model(self) -> None:
        """Default model should be text-embedding-3-small."""
        backend = OpenAIEmbedding()
        assert backend.model_name == "text-embedding-3-small"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    def test_custom_model(self) -> None:
        """Should accept a custom model name."""
        backend = OpenAIEmbedding(model_name="text-embedding-3-large")
        assert backend.model_name == "text-embedding-3-large"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    def test_implements_protocol(self) -> None:
        """OpenAIEmbedding should implement EmbeddingBackend protocol."""
        backend = OpenAIEmbedding()
        assert isinstance(backend, EmbeddingBackend)

    @patch.dict("os.environ", {}, clear=True)
    def test_raises_error_without_api_key(self) -> None:
        """Should raise a clear error when OPENAI_API_KEY is not set."""
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            OpenAIEmbedding()

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    def test_accepts_explicit_api_key(self) -> None:
        """Should accept an explicit API key parameter."""
        backend = OpenAIEmbedding(api_key="explicit-key")
        assert backend._api_key == "explicit-key"


class TestOpenAIEmbeddingEmbedTexts:
    """Test embed_texts method with mocked API calls."""

    def _make_mock_response(self, texts: list[str], dim: int = 1536) -> MagicMock:
        """Create a mock OpenAI embeddings response."""
        mock_response = MagicMock()
        mock_data = []
        for i, _text in enumerate(texts):
            mock_embedding = MagicMock()
            mock_embedding.embedding = [0.1 * (i + 1)] * dim
            mock_embedding.index = i
            mock_data.append(mock_embedding)
        mock_response.data = mock_data
        return mock_response

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("markdown_rag.embedding.openai.openai_module.OpenAI")
    def test_single_text(self, mock_openai_cls: MagicMock) -> None:
        """Should return embeddings for a single text."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.embeddings.create.return_value = self._make_mock_response(["hello"])

        backend = OpenAIEmbedding()
        result = backend.embed_texts(["hello"])

        assert len(result) == 1
        assert isinstance(result[0], list)
        assert len(result[0]) == 1536
        mock_client.embeddings.create.assert_called_once()

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("markdown_rag.embedding.openai.openai_module.OpenAI")
    def test_multiple_texts(self, mock_openai_cls: MagicMock) -> None:
        """Should return embeddings for multiple texts."""
        texts = ["hello", "world", "test"]
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.embeddings.create.return_value = self._make_mock_response(texts)

        backend = OpenAIEmbedding()
        result = backend.embed_texts(texts)

        assert len(result) == 3
        # Verify API was called with correct model
        call_kwargs = mock_client.embeddings.create.call_args
        assert call_kwargs.kwargs["model"] == "text-embedding-3-small"
        assert call_kwargs.kwargs["input"] == texts

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("markdown_rag.embedding.openai.openai_module.OpenAI")
    def test_empty_list(self, mock_openai_cls: MagicMock) -> None:
        """Should handle empty input list without calling API."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        backend = OpenAIEmbedding()
        result = backend.embed_texts([])

        assert result == []
        mock_client.embeddings.create.assert_not_called()


class TestOpenAIEmbeddingEmbedQuery:
    """Test embed_query method with mocked API calls."""

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("markdown_rag.embedding.openai.openai_module.OpenAI")
    def test_returns_single_vector(self, mock_openai_cls: MagicMock) -> None:
        """Should return a single embedding vector for a query."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        mock_response = MagicMock()
        mock_embedding = MagicMock()
        mock_embedding.embedding = [0.5] * 1536
        mock_embedding.index = 0
        mock_response.data = [mock_embedding]
        mock_client.embeddings.create.return_value = mock_response

        backend = OpenAIEmbedding()
        result = backend.embed_query("search query")

        assert isinstance(result, list)
        assert len(result) == 1536
        assert all(isinstance(v, float) for v in result)

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("markdown_rag.embedding.openai.openai_module.OpenAI")
    def test_calls_embed_texts_internally(self, mock_openai_cls: MagicMock) -> None:
        """embed_query should delegate to embed_texts."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        mock_response = MagicMock()
        mock_embedding = MagicMock()
        mock_embedding.embedding = [0.1] * 1536
        mock_embedding.index = 0
        mock_response.data = [mock_embedding]
        mock_client.embeddings.create.return_value = mock_response

        backend = OpenAIEmbedding()
        backend.embed_query("test query")

        # Should call API with single-element list
        call_kwargs = mock_client.embeddings.create.call_args
        assert call_kwargs.kwargs["input"] == ["test query"]
