"""Tests for LocalEmbedding backend using sentence-transformers."""

from __future__ import annotations

import pytest

from markdown_rag.embedding.base import EmbeddingBackend
from markdown_rag.embedding.local import LocalEmbedding


class TestLocalEmbeddingInit:
    """Test LocalEmbedding initialization and lazy loading."""

    def test_default_model_name(self) -> None:
        """Default model should be all-MiniLM-L6-v2."""
        backend = LocalEmbedding()
        assert backend.model_name == "all-MiniLM-L6-v2"

    def test_custom_model_name(self) -> None:
        """Should accept a custom model name."""
        backend = LocalEmbedding(model_name="paraphrase-MiniLM-L3-v2")
        assert backend.model_name == "paraphrase-MiniLM-L3-v2"

    def test_model_not_loaded_at_init(self) -> None:
        """Model should not be loaded until first use (lazy loading)."""
        backend = LocalEmbedding()
        assert backend._model is None

    def test_implements_protocol(self) -> None:
        """LocalEmbedding should implement EmbeddingBackend protocol."""
        backend = LocalEmbedding()
        assert isinstance(backend, EmbeddingBackend)


class TestLocalEmbeddingEmbedTexts:
    """Test embed_texts method."""

    @pytest.fixture(autouse=True)
    def setup_backend(self) -> None:
        self.backend = LocalEmbedding()

    def test_single_text(self) -> None:
        """Should return embeddings for a single text."""
        result = self.backend.embed_texts(["hello world"])
        assert len(result) == 1
        assert isinstance(result[0], list)
        assert len(result[0]) > 0
        assert all(isinstance(v, float) for v in result[0])

    def test_multiple_texts(self) -> None:
        """Should return embeddings for multiple texts."""
        texts = ["hello world", "foo bar", "test sentence"]
        result = self.backend.embed_texts(texts)
        assert len(result) == 3
        # All embeddings should have the same dimension
        dims = {len(emb) for emb in result}
        assert len(dims) == 1

    def test_empty_list(self) -> None:
        """Should handle empty input list."""
        result = self.backend.embed_texts([])
        assert result == []

    def test_embedding_dimension(self) -> None:
        """all-MiniLM-L6-v2 produces 384-dimensional embeddings."""
        result = self.backend.embed_texts(["test"])
        assert len(result[0]) == 384

    def test_model_loaded_after_first_call(self) -> None:
        """Model should be loaded after first embed_texts call."""
        assert self.backend._model is None
        self.backend.embed_texts(["trigger load"])
        assert self.backend._model is not None


class TestLocalEmbeddingEmbedQuery:
    """Test embed_query method."""

    @pytest.fixture(autouse=True)
    def setup_backend(self) -> None:
        self.backend = LocalEmbedding()

    def test_returns_single_vector(self) -> None:
        """Should return a single embedding vector for a query."""
        result = self.backend.embed_query("search query")
        assert isinstance(result, list)
        assert len(result) == 384
        assert all(isinstance(v, float) for v in result)

    def test_different_queries_produce_different_embeddings(self) -> None:
        """Different queries should produce different embeddings."""
        emb1 = self.backend.embed_query("machine learning")
        emb2 = self.backend.embed_query("cooking recipe")
        assert emb1 != emb2

    def test_model_loaded_after_query(self) -> None:
        """Model should be loaded after first embed_query call."""
        assert self.backend._model is None
        self.backend.embed_query("trigger load")
        assert self.backend._model is not None
