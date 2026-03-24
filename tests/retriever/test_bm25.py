"""Tests for BM25 keyword search engine."""

from __future__ import annotations

from pathlib import Path

import pytest

from markdown_rag.models import Chunk
from markdown_rag.retriever.bm25 import BM25Index, _has_korean, tokenize


class TestTokenization:
    """Test tokenization utilities."""

    def test_has_korean_with_korean_text(self) -> None:
        assert _has_korean("SNMP 트랩 설정") is True

    def test_has_korean_with_english_text(self) -> None:
        assert _has_korean("BGP routing protocol") is False

    def test_tokenize_english(self) -> None:
        tokens = tokenize("BGP routing protocol")
        assert tokens == ["bgp", "routing", "protocol"]

    def test_tokenize_korean(self) -> None:
        tokens = tokenize("SNMP 트랩 설정 방법")
        assert len(tokens) > 0
        # 형태소 분석 결과 토큰이 존재해야 함
        assert isinstance(tokens[0], str)

    def test_tokenize_empty(self) -> None:
        tokens = tokenize("")
        assert tokens == []


class TestBM25Index:
    """Test BM25Index search and persistence."""

    @pytest.fixture
    def sample_chunks(self) -> list[Chunk]:
        return [
            Chunk(
                content="RFC 9110 defines HTTP semantics and status codes.",
                doc_path=Path("rfc9110.md"),
                chunk_index=0,
            ),
            Chunk(
                content="BGP is the Border Gateway Protocol used for routing.",
                doc_path=Path("bgp.md"),
                chunk_index=0,
            ),
            Chunk(
                content="SNMP 트랩 설정 방법을 설명합니다.",
                doc_path=Path("snmp.md"),
                chunk_index=0,
            ),
        ]

    @pytest.fixture
    def index_with_data(self, sample_chunks: list[Chunk]) -> BM25Index:
        index = BM25Index()
        index.add_chunks(sample_chunks)
        return index

    def test_empty_index_search(self) -> None:
        index = BM25Index()
        results = index.search("test query")
        assert results == []

    def test_size(self, index_with_data: BM25Index) -> None:
        assert index_with_data.size == 3

    def test_search_returns_results(self, index_with_data: BM25Index) -> None:
        results = index_with_data.search("HTTP status codes", top_k=2)
        assert len(results) > 0
        assert results[0].chunk.content.startswith("RFC 9110")

    def test_search_respects_top_k(self, index_with_data: BM25Index) -> None:
        results = index_with_data.search("protocol", top_k=1)
        assert len(results) <= 1

    def test_search_korean(self, index_with_data: BM25Index) -> None:
        results = index_with_data.search("SNMP 트랩", top_k=3)
        assert len(results) > 0

    def test_results_have_rank(self, index_with_data: BM25Index) -> None:
        results = index_with_data.search("protocol", top_k=3)
        for i, result in enumerate(results, start=1):
            assert result.rank == i

    def test_save_and_load(
        self, index_with_data: BM25Index, tmp_path: Path
    ) -> None:
        save_path = tmp_path / "bm25.pkl"
        index_with_data.save(save_path)
        assert save_path.exists()

        loaded = BM25Index.load(save_path)
        assert loaded.size == index_with_data.size

        # 검색 결과가 동일해야 함
        original = index_with_data.search("HTTP", top_k=1)
        restored = loaded.search("HTTP", top_k=1)
        assert original[0].chunk.content == restored[0].chunk.content

    def test_clear(self, index_with_data: BM25Index) -> None:
        index_with_data.clear()
        assert index_with_data.size == 0
        assert index_with_data.search("test") == []
