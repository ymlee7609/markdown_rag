"""Tests for CrossEncoderReranker."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pytest

from markdown_rag.models import Chunk, SearchResult
from markdown_rag.retriever.reranker import CrossEncoderReranker


def _make_result(content: str, score: float, rank: int) -> SearchResult:
    return SearchResult(
        chunk=Chunk(content=content, doc_path=Path("test.md"), chunk_index=0),
        score=score,
        rank=rank,
    )


class TestCrossEncoderReranker:
    """Test cross-encoder reranking."""

    @pytest.fixture
    def mock_model(self) -> MagicMock:
        model = MagicMock()
        # 리랭킹 점수: 역순으로 설정 (원래 rank 3이 가장 높은 점수)
        model.predict.return_value = np.array([0.2, 0.5, 0.9])
        return model

    @pytest.fixture
    def reranker(self, mock_model: MagicMock) -> CrossEncoderReranker:
        r = CrossEncoderReranker(model_name="test-model")
        r._model = mock_model
        return r

    def test_rerank_reorders_results(self, reranker: CrossEncoderReranker) -> None:
        results = [
            _make_result("low", score=0.9, rank=1),
            _make_result("mid", score=0.7, rank=2),
            _make_result("high", score=0.3, rank=3),
        ]
        reranked = reranker.rerank("test query", results, top_k=3)

        # 크로스 인코더 점수 기준 재정렬됨
        assert reranked[0].chunk.content == "high"  # score 0.9
        assert reranked[1].chunk.content == "mid"   # score 0.5
        assert reranked[2].chunk.content == "low"   # score 0.2

    def test_rerank_respects_top_k(self, reranker: CrossEncoderReranker) -> None:
        results = [
            _make_result("a", 0.9, 1),
            _make_result("b", 0.7, 2),
            _make_result("c", 0.3, 3),
        ]
        reranked = reranker.rerank("test", results, top_k=1)
        assert len(reranked) == 1

    def test_rerank_assigns_new_ranks(self, reranker: CrossEncoderReranker) -> None:
        results = [
            _make_result("a", 0.9, 1),
            _make_result("b", 0.7, 2),
            _make_result("c", 0.3, 3),
        ]
        reranked = reranker.rerank("test", results, top_k=3)
        for i, result in enumerate(reranked, start=1):
            assert result.rank == i

    def test_rerank_empty_results(self, reranker: CrossEncoderReranker) -> None:
        reranked = reranker.rerank("test", [], top_k=5)
        assert reranked == []

    def test_rerank_passes_correct_pairs(
        self, reranker: CrossEncoderReranker, mock_model: MagicMock
    ) -> None:
        results = [
            _make_result("content A", 0.9, 1),
            _make_result("content B", 0.7, 2),
        ]
        mock_model.predict.return_value = np.array([0.8, 0.3])

        reranker.rerank("my query", results, top_k=2)

        pairs = mock_model.predict.call_args[0][0]
        assert pairs == [["my query", "content A"], ["my query", "content B"]]

    def test_lazy_model_loading(self) -> None:
        r = CrossEncoderReranker(model_name="test")
        assert r._model is None
