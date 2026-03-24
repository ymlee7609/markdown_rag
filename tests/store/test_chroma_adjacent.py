"""Tests for ChromaStore.get_adjacent_chunks method."""

from __future__ import annotations

from pathlib import Path

import pytest

from markdown_rag.models import Chunk
from markdown_rag.store.chroma import ChromaStore


@pytest.fixture
def store_with_sequence(tmp_path: Path) -> ChromaStore:
    """연속된 chunk_index를 가진 청크들이 저장된 스토어."""
    store = ChromaStore(
        persist_path=tmp_path / "adj_test",
        collection_name="adj_test",
    )
    chunks = [
        Chunk(
            content=f"Chunk {i} content",
            doc_path=Path("docs/sequential.md"),
            headers=["Section"],
            chunk_index=i,
        )
        for i in range(5)
    ]
    embeddings = [[float(i) / 10] * 384 for i in range(5)]
    store.add_chunks(chunks, embeddings)
    return store


class TestGetAdjacentChunks:
    def test_returns_adjacent_chunks(self, store_with_sequence: ChromaStore) -> None:
        adjacent = store_with_sequence.get_adjacent_chunks(
            "docs/sequential.md", chunk_index=2, window=1
        )
        indices = [c.chunk_index for c in adjacent]
        assert 1 in indices
        assert 3 in indices
        assert 2 not in indices  # 자기 자신 제외

    def test_window_2(self, store_with_sequence: ChromaStore) -> None:
        adjacent = store_with_sequence.get_adjacent_chunks(
            "docs/sequential.md", chunk_index=2, window=2
        )
        indices = [c.chunk_index for c in adjacent]
        assert 0 in indices
        assert 1 in indices
        assert 3 in indices
        assert 4 in indices

    def test_edge_chunk_index_0(self, store_with_sequence: ChromaStore) -> None:
        adjacent = store_with_sequence.get_adjacent_chunks(
            "docs/sequential.md", chunk_index=0, window=1
        )
        indices = [c.chunk_index for c in adjacent]
        assert 1 in indices
        assert len(indices) == 1

    def test_nonexistent_document(self, store_with_sequence: ChromaStore) -> None:
        adjacent = store_with_sequence.get_adjacent_chunks(
            "nonexistent.md", chunk_index=0, window=1
        )
        assert adjacent == []

    def test_sorted_by_chunk_index(self, store_with_sequence: ChromaStore) -> None:
        adjacent = store_with_sequence.get_adjacent_chunks(
            "docs/sequential.md", chunk_index=2, window=2
        )
        indices = [c.chunk_index for c in adjacent]
        assert indices == sorted(indices)
