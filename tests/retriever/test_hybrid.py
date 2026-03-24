"""Tests for HybridSearch (RRF fusion of vector + BM25)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from markdown_rag.models import Chunk, SearchResult
from markdown_rag.retriever.bm25 import BM25Index
from markdown_rag.retriever.hybrid import HybridSearch


def _make_result(content: str, rank: int, score: float = 0.9) -> SearchResult:
    return SearchResult(
        chunk=Chunk(content=content, doc_path=Path(f"{content}.md"), chunk_index=0),
        score=score,
        rank=rank,
    )


class TestHybridSearchInit:
    def test_valid_alpha(self) -> None:
        engine = HybridSearch(MagicMock(), BM25Index(), alpha=0.5)
        assert engine.alpha == 0.5

    def test_invalid_alpha_raises(self) -> None:
        with pytest.raises(ValueError, match="alpha"):
            HybridSearch(MagicMock(), BM25Index(), alpha=1.5)


class TestHybridSearchFusion:
    """Test RRF fusion logic."""

    @pytest.fixture
    def hybrid_engine(self) -> HybridSearch:
        mock_semantic = MagicMock()
        mock_semantic.search.return_value = [
            _make_result("doc_a", rank=1),
            _make_result("doc_b", rank=2),
        ]

        bm25 = BM25Index()
        # BM25 검색 결과를 직접 모킹
        bm25_mock = MagicMock(wraps=bm25)
        bm25_mock.search.return_value = [
            _make_result("doc_b", rank=1),
            _make_result("doc_c", rank=2),
        ]

        return HybridSearch(mock_semantic, bm25_mock, alpha=0.7)

    def test_returns_fused_results(self, hybrid_engine: HybridSearch) -> None:
        results = hybrid_engine.search("test query", top_k=3)
        assert len(results) > 0

    def test_results_have_rank(self, hybrid_engine: HybridSearch) -> None:
        results = hybrid_engine.search("test query", top_k=3)
        for i, result in enumerate(results, start=1):
            assert result.rank == i

    def test_overlapping_results_get_higher_score(
        self, hybrid_engine: HybridSearch
    ) -> None:
        """양쪽 검색에서 모두 나온 doc_b가 가장 높은 점수를 받아야 한다."""
        results = hybrid_engine.search("test query", top_k=3)
        # doc_b는 벡터 rank=2, BM25 rank=1 => 두 점수가 합산됨
        contents = [r.chunk.content for r in results]
        assert "doc_b" in contents
        # doc_b가 상위에 있어야 함 (양쪽에서 모두 등장)
        doc_b_result = next(r for r in results if r.chunk.content == "doc_b")
        assert doc_b_result.rank <= 2

    def test_respects_top_k(self, hybrid_engine: HybridSearch) -> None:
        results = hybrid_engine.search("test query", top_k=1)
        assert len(results) == 1

    def test_passes_where_to_semantic(self, hybrid_engine: HybridSearch) -> None:
        where = {"doc_type": "rfc"}
        hybrid_engine.search("test", top_k=3, where=where)
        hybrid_engine.semantic_search.search.assert_called_once()
        call_kwargs = hybrid_engine.semantic_search.search.call_args
        assert call_kwargs.kwargs.get("where") == where or call_kwargs[1].get("where") == where
