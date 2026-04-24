"""Tests for E5 model prefix handling in LocalEmbedding."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from markdown_rag.embedding.local import LocalEmbedding, _is_e5_model


class TestIsE5Model:
    """Test E5 model detection."""

    @pytest.mark.parametrize(
        "model_name,expected",
        [
            ("intfloat/multilingual-e5-small", True),
            ("intfloat/multilingual-e5-base", True),
            ("intfloat/multilingual-e5-large", True),
            ("intfloat/e5-small-v2", True),
            ("intfloat/e5-base-v2", True),
            ("all-MiniLM-L6-v2", False),
            ("paraphrase-MiniLM-L3-v2", False),
            ("BAAI/bge-small-en-v1.5", False),
        ],
    )
    def test_detection(self, model_name: str, expected: bool) -> None:
        """E5 모델 이름이 올바르게 감지되어야 한다."""
        assert _is_e5_model(model_name) == expected


class TestE5PrefixHandling:
    """Test that E5 models automatically add correct prefixes."""

    @pytest.fixture
    def mock_model(self) -> MagicMock:
        """Create a mock SentenceTransformer model."""
        import numpy as np

        model = MagicMock()
        model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        return model

    def test_embed_texts_adds_passage_prefix_for_e5(self, mock_model: MagicMock) -> None:
        """E5 모델의 embed_texts는 "passage: " 접두사를 추가해야 한다."""
        backend = LocalEmbedding(model_name="intfloat/multilingual-e5-small")
        backend._model = mock_model

        backend.embed_texts(["hello world"])

        mock_model.encode.assert_called_once()
        actual_texts = mock_model.encode.call_args[0][0]
        assert actual_texts == ["passage: hello world"]

    def test_embed_texts_no_prefix_for_non_e5(self, mock_model: MagicMock) -> None:
        """비-E5 모델의 embed_texts는 접두사를 추가하지 않아야 한다."""
        backend = LocalEmbedding(model_name="all-MiniLM-L6-v2")
        backend._model = mock_model

        backend.embed_texts(["hello world"])

        mock_model.encode.assert_called_once()
        actual_texts = mock_model.encode.call_args[0][0]
        assert actual_texts == ["hello world"]

    def test_embed_query_adds_query_prefix_for_e5(self, mock_model: MagicMock) -> None:
        """E5 모델의 embed_query는 "query: " 접두사를 추가해야 한다."""
        backend = LocalEmbedding(model_name="intfloat/multilingual-e5-small")
        backend._model = mock_model

        backend.embed_query("search term")

        mock_model.encode.assert_called_once()
        actual_texts = mock_model.encode.call_args[0][0]
        assert actual_texts == ["query: search term"]

    def test_embed_query_no_prefix_for_non_e5(self, mock_model: MagicMock) -> None:
        """비-E5 모델의 embed_query는 접두사를 추가하지 않아야 한다."""
        backend = LocalEmbedding(model_name="all-MiniLM-L6-v2")
        backend._model = mock_model

        backend.embed_query("search term")

        mock_model.encode.assert_called_once()
        actual_texts = mock_model.encode.call_args[0][0]
        assert actual_texts == ["search term"]

    def test_embed_query_no_double_prefix(self, mock_model: MagicMock) -> None:
        """E5 모델의 embed_query에서 이중 접두사가 발생하지 않아야 한다."""
        backend = LocalEmbedding(model_name="intfloat/multilingual-e5-small")
        backend._model = mock_model

        backend.embed_query("test query")

        actual_texts = mock_model.encode.call_args[0][0]
        # "passage: query: test query"가 아닌 "query: test query"여야 함
        assert actual_texts == ["query: test query"]
        assert not actual_texts[0].startswith("passage:")

    def test_e5_flag_set_on_init(self) -> None:
        """E5 모델 플래그가 초기화 시 올바르게 설정되어야 한다."""
        e5_backend = LocalEmbedding(model_name="intfloat/multilingual-e5-small")
        assert e5_backend._is_e5 is True

        non_e5_backend = LocalEmbedding(model_name="all-MiniLM-L6-v2")
        assert non_e5_backend._is_e5 is False
