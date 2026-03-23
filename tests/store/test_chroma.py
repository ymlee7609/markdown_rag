"""Tests for ChromaStore vector store using ChromaDB."""

from __future__ import annotations

from pathlib import Path

import pytest

from markdown_rag.models import Chunk, SearchResult
from markdown_rag.store.base import VectorStore
from markdown_rag.store.chroma import ChromaStore


@pytest.fixture
def chroma_store(tmp_path: Path) -> ChromaStore:
    """Create a ChromaStore instance with temporary storage."""
    return ChromaStore(
        persist_path=tmp_path / "chroma_test",
        collection_name="test_collection",
    )


@pytest.fixture
def sample_chunks() -> list[Chunk]:
    """Create sample chunks for testing."""
    return [
        Chunk(
            content="Python is a programming language.",
            doc_path=Path("docs/python.md"),
            headers=["Python", "Overview"],
            chunk_index=0,
        ),
        Chunk(
            content="FastAPI is a modern web framework for Python.",
            doc_path=Path("docs/python.md"),
            headers=["Python", "Frameworks"],
            chunk_index=1,
        ),
        Chunk(
            content="Rust is a systems programming language.",
            doc_path=Path("docs/rust.md"),
            headers=["Rust", "Overview"],
            chunk_index=0,
        ),
    ]


@pytest.fixture
def sample_embeddings() -> list[list[float]]:
    """Create sample embeddings (384-dim for testing)."""
    return [
        [0.1] * 384,
        [0.2] * 384,
        [0.3] * 384,
    ]


class TestChromaStoreInit:
    """Test ChromaStore initialization."""

    def test_creates_store_with_defaults(self, tmp_path: Path) -> None:
        """Should create a store with default collection name."""
        store = ChromaStore(persist_path=tmp_path / "chroma")
        assert store.collection_name == "markdown_docs"

    def test_creates_store_with_custom_collection(self, tmp_path: Path) -> None:
        """Should accept custom collection name."""
        store = ChromaStore(
            persist_path=tmp_path / "chroma",
            collection_name="custom_collection",
        )
        assert store.collection_name == "custom_collection"

    def test_implements_protocol(self, chroma_store: ChromaStore) -> None:
        """ChromaStore should implement VectorStore protocol."""
        assert isinstance(chroma_store, VectorStore)

    def test_creates_persist_directory(self, tmp_path: Path) -> None:
        """Should create the persistence directory."""
        persist_path = tmp_path / "chroma_new"
        ChromaStore(persist_path=persist_path)
        assert persist_path.exists()


class TestChromaStoreAddChunks:
    """Test add_chunks method."""

    def test_add_single_chunk(
        self,
        chroma_store: ChromaStore,
    ) -> None:
        """Should add a single chunk with embedding."""
        chunk = Chunk(
            content="Test content",
            doc_path=Path("test.md"),
            headers=["Test"],
            chunk_index=0,
        )
        chroma_store.add_chunks([chunk], [[0.1] * 384])
        assert chroma_store.count() == 1

    def test_add_multiple_chunks(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Should add multiple chunks."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)
        assert chroma_store.count() == 3

    def test_stores_metadata(
        self,
        chroma_store: ChromaStore,
    ) -> None:
        """Should store chunk metadata (headers, doc_path, chunk_index)."""
        chunk = Chunk(
            content="Content with metadata",
            doc_path=Path("docs/meta.md"),
            headers=["Section", "Subsection"],
            chunk_index=5,
        )
        chroma_store.add_chunks([chunk], [[0.5] * 384])

        # Search should return chunk with correct metadata
        results = chroma_store.search([0.5] * 384, top_k=1)
        assert len(results) == 1
        assert results[0].chunk.doc_path == Path("docs/meta.md")
        assert results[0].chunk.headers == ["Section", "Subsection"]
        assert results[0].chunk.chunk_index == 5

    def test_mismatched_lengths_raises_error(
        self,
        chroma_store: ChromaStore,
    ) -> None:
        """Should raise ValueError when chunks and embeddings have different lengths."""
        chunks = [
            Chunk(content="a", doc_path=Path("t.md"), chunk_index=0),
            Chunk(content="b", doc_path=Path("t.md"), chunk_index=1),
        ]
        embeddings = [[0.1] * 384]  # Only 1 embedding for 2 chunks

        with pytest.raises(ValueError, match="length"):
            chroma_store.add_chunks(chunks, embeddings)

    def test_empty_chunks(self, chroma_store: ChromaStore) -> None:
        """Should handle empty input gracefully."""
        chroma_store.add_chunks([], [])
        assert chroma_store.count() == 0


class TestChromaStoreSearch:
    """Test search method."""

    def test_returns_search_results(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Should return SearchResult objects."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)

        results = chroma_store.search([0.1] * 384, top_k=2)

        assert len(results) == 2
        assert all(isinstance(r, SearchResult) for r in results)

    def test_results_have_scores(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Results should include similarity scores."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)

        results = chroma_store.search([0.1] * 384, top_k=3)

        for result in results:
            assert isinstance(result.score, float)
            assert result.score >= 0.0

    def test_results_sorted_by_score_descending(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Results should be sorted by score in descending order (highest first)."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)

        results = chroma_store.search([0.1] * 384, top_k=3)

        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_results_have_rank(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Results should have sequential rank starting from 1."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)

        results = chroma_store.search([0.1] * 384, top_k=3)

        for i, result in enumerate(results):
            assert result.rank == i + 1

    def test_top_k_limits_results(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Should return at most top_k results."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)

        results = chroma_store.search([0.1] * 384, top_k=1)
        assert len(results) == 1

    def test_search_empty_store(
        self,
        chroma_store: ChromaStore,
    ) -> None:
        """Should return empty list when store is empty."""
        results = chroma_store.search([0.1] * 384, top_k=5)
        assert results == []

    def test_results_contain_correct_chunk_content(
        self,
        chroma_store: ChromaStore,
    ) -> None:
        """Returned chunks should contain the correct content."""
        chunk = Chunk(
            content="Unique test content for verification",
            doc_path=Path("verify.md"),
            headers=["Test"],
            chunk_index=0,
        )
        chroma_store.add_chunks([chunk], [[0.9] * 384])

        results = chroma_store.search([0.9] * 384, top_k=1)
        assert results[0].chunk.content == "Unique test content for verification"


class TestChromaStoreDeleteByDocument:
    """Test delete_by_document method."""

    def test_deletes_chunks_by_doc_path(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Should delete all chunks from a specific document."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)
        assert chroma_store.count() == 3

        deleted = chroma_store.delete_by_document("docs/python.md")
        assert deleted == 2
        assert chroma_store.count() == 1

    def test_returns_zero_when_no_match(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Should return 0 when no chunks match the doc_path."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)

        deleted = chroma_store.delete_by_document("nonexistent.md")
        assert deleted == 0

    def test_delete_from_empty_store(
        self,
        chroma_store: ChromaStore,
    ) -> None:
        """Should return 0 when store is empty."""
        deleted = chroma_store.delete_by_document("anything.md")
        assert deleted == 0


class TestChromaStoreCount:
    """Test count method."""

    def test_empty_store_count(self, chroma_store: ChromaStore) -> None:
        """Empty store should have count 0."""
        assert chroma_store.count() == 0

    def test_count_after_add(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Count should reflect added chunks."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)
        assert chroma_store.count() == 3


class TestChromaStoreClear:
    """Test clear method."""

    def test_clear_removes_all_data(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Clear should remove all stored chunks."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)
        assert chroma_store.count() == 3

        chroma_store.clear()
        assert chroma_store.count() == 0

    def test_clear_empty_store(self, chroma_store: ChromaStore) -> None:
        """Clear on empty store should not raise error."""
        chroma_store.clear()
        assert chroma_store.count() == 0

    def test_can_add_after_clear(
        self,
        chroma_store: ChromaStore,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Should be able to add chunks after clearing."""
        chroma_store.add_chunks(sample_chunks, sample_embeddings)
        chroma_store.clear()

        # Add again
        chroma_store.add_chunks(sample_chunks[:1], sample_embeddings[:1])
        assert chroma_store.count() == 1


class TestChromaStorePersistence:
    """Test data persistence across store instances."""

    def test_data_persists_across_instances(
        self,
        tmp_path: Path,
        sample_chunks: list[Chunk],
        sample_embeddings: list[list[float]],
    ) -> None:
        """Data should persist when creating a new store instance with same path."""
        persist_path = tmp_path / "persist_test"

        # First instance: add data
        store1 = ChromaStore(persist_path=persist_path, collection_name="persist_col")
        store1.add_chunks(sample_chunks, sample_embeddings)
        assert store1.count() == 3

        # Second instance: data should still be there
        store2 = ChromaStore(persist_path=persist_path, collection_name="persist_col")
        assert store2.count() == 3
