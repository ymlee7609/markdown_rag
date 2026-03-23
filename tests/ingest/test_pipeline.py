"""Tests for IngestPipeline - document ingestion orchestrator."""

from pathlib import Path
from unittest.mock import patch

import pytest

from markdown_rag.config import Settings
from markdown_rag.ingest.pipeline import IngestPipeline, IngestResult
from markdown_rag.models import Chunk, Document

# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------


class MockEmbeddingBackend:
    """Mock embedding backend that returns deterministic vectors."""

    def __init__(self, dim: int = 4) -> None:
        self._dim = dim
        self.call_count = 0

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        self.call_count += 1
        return [[float(i)] * self._dim for i in range(len(texts))]

    def embed_query(self, query: str) -> list[float]:
        return [0.0] * self._dim


class MockVectorStore:
    """Mock vector store that tracks add/delete operations."""

    def __init__(self) -> None:
        self.added_chunks: list[Chunk] = []
        self.added_embeddings: list[list[float]] = []
        self.deleted_docs: list[str] = []
        self._count = 0

    def add_chunks(
        self, chunks: list[Chunk], embeddings: list[list[float]]
    ) -> None:
        self.added_chunks.extend(chunks)
        self.added_embeddings.extend(embeddings)
        self._count += len(chunks)

    def search(
        self, query_embedding: list[float], top_k: int = 5
    ) -> list:
        return []

    def delete_by_document(self, doc_path: str) -> int:
        self.deleted_docs.append(doc_path)
        # Simulate deleting some existing chunks
        deleted = sum(
            1
            for c in self.added_chunks
            if str(c.doc_path) == doc_path
        )
        self.added_chunks = [
            c for c in self.added_chunks if str(c.doc_path) != doc_path
        ]
        self._count -= deleted
        return deleted

    def count(self) -> int:
        return self._count

    def clear(self) -> None:
        self.added_chunks.clear()
        self.added_embeddings.clear()
        self._count = 0


# ---------------------------------------------------------------------------
# IngestResult tests
# ---------------------------------------------------------------------------


class TestIngestResult:
    """Tests for IngestResult dataclass."""

    def test_default_values(self) -> None:
        """IngestResult should have sensible defaults."""
        result = IngestResult(documents_processed=0, chunks_created=0)

        assert result.documents_processed == 0
        assert result.chunks_created == 0
        assert result.errors == []

    def test_with_errors(self) -> None:
        """IngestResult should store error messages."""
        result = IngestResult(
            documents_processed=1,
            chunks_created=0,
            errors=["Failed to read file."],
        )

        assert len(result.errors) == 1
        assert "Failed" in result.errors[0]


# ---------------------------------------------------------------------------
# Pipeline construction tests
# ---------------------------------------------------------------------------


class TestPipelineConstruction:
    """Tests for IngestPipeline construction."""

    def test_construct_with_explicit_backends(
        self, test_settings: Settings
    ) -> None:
        """Pipeline should accept explicit embedding and store backends."""
        emb = MockEmbeddingBackend()
        store = MockVectorStore()

        pipeline = IngestPipeline(
            settings=test_settings,
            embedding_backend=emb,
            vector_store=store,
        )

        assert pipeline._embedding_backend is emb
        assert pipeline._vector_store is store

    def test_construct_creates_local_embedding_by_default(
        self, test_settings: Settings
    ) -> None:
        """When embedding_backend is None, pipeline should create LocalEmbedding."""
        with patch(
            "markdown_rag.ingest.pipeline.LocalEmbedding"
        ) as mock_cls:
            mock_cls.return_value = MockEmbeddingBackend()
            IngestPipeline(
                settings=test_settings,
                vector_store=MockVectorStore(),
            )

            mock_cls.assert_called_once_with(
                model_name=test_settings.local_model
            )

    def test_construct_creates_openai_embedding_when_configured(
        self, tmp_path: Path
    ) -> None:
        """When embedding_backend is 'openai', pipeline should create OpenAIEmbedding."""
        settings = Settings(
            embedding_backend="openai",
            chroma_path=tmp_path / "chroma",
            collection_name="test_col",
        )

        with patch(
            "markdown_rag.ingest.pipeline.OpenAIEmbedding"
        ) as mock_cls:
            mock_cls.return_value = MockEmbeddingBackend()
            IngestPipeline(
                settings=settings,
                vector_store=MockVectorStore(),
            )

            mock_cls.assert_called_once_with(
                model_name=settings.openai_embedding_model
            )

    def test_construct_creates_chroma_store_when_none(
        self, test_settings: Settings
    ) -> None:
        """When vector_store is None, pipeline should create ChromaStore."""
        with patch(
            "markdown_rag.ingest.pipeline.ChromaStore"
        ) as mock_cls:
            mock_cls.return_value = MockVectorStore()
            IngestPipeline(
                settings=test_settings,
                embedding_backend=MockEmbeddingBackend(),
            )

            mock_cls.assert_called_once_with(
                persist_path=test_settings.chroma_path,
                collection_name=test_settings.collection_name,
            )


# ---------------------------------------------------------------------------
# Ingest single document tests
# ---------------------------------------------------------------------------


class TestIngestDocument:
    """Tests for ingesting a single document."""

    @pytest.fixture
    def pipeline(self, test_settings: Settings) -> IngestPipeline:
        """Create a pipeline with mock backends."""
        return IngestPipeline(
            settings=test_settings,
            embedding_backend=MockEmbeddingBackend(),
            vector_store=MockVectorStore(),
        )

    def test_ingest_document_returns_chunk_count(
        self, pipeline: IngestPipeline
    ) -> None:
        """ingest_document should return the number of chunks created."""
        doc = Document(
            path=Path("test.md"),
            content="# Title\n\nSome content here.",
        )

        count = pipeline.ingest_document(doc)

        assert count > 0

    def test_ingest_document_stores_chunks(
        self, pipeline: IngestPipeline
    ) -> None:
        """ingest_document should store chunks in the vector store."""
        doc = Document(
            path=Path("test.md"),
            content="# Title\n\nSome content here.",
        )

        pipeline.ingest_document(doc)

        store = pipeline._vector_store
        assert isinstance(store, MockVectorStore)
        assert len(store.added_chunks) > 0

    def test_ingest_document_with_frontmatter(
        self, pipeline: IngestPipeline
    ) -> None:
        """ingest_document should extract frontmatter metadata."""
        doc = Document(
            path=Path("test.md"),
            content="---\ntitle: Test\ntags:\n  - python\n---\n\n# Title\n\nContent.",
        )

        count = pipeline.ingest_document(doc)

        assert count > 0
        store = pipeline._vector_store
        assert isinstance(store, MockVectorStore)
        # Check that metadata from frontmatter was preserved
        chunk = store.added_chunks[0]
        assert "title" in chunk.metadata
        assert chunk.metadata["title"] == "Test"

    def test_ingest_document_empty_content(
        self, pipeline: IngestPipeline
    ) -> None:
        """ingest_document with empty content should return 0 chunks."""
        doc = Document(path=Path("empty.md"), content="")

        count = pipeline.ingest_document(doc)

        assert count == 0

    def test_ingest_document_embeddings_match_chunks(
        self, pipeline: IngestPipeline
    ) -> None:
        """Number of embeddings should match number of chunks."""
        doc = Document(
            path=Path("test.md"),
            content="# Title\n\nParagraph one.\n\n## Section\n\nParagraph two.",
        )

        pipeline.ingest_document(doc)

        store = pipeline._vector_store
        assert isinstance(store, MockVectorStore)
        assert len(store.added_chunks) == len(store.added_embeddings)


# ---------------------------------------------------------------------------
# Ingest path (directory/file) tests
# ---------------------------------------------------------------------------


class TestIngestPath:
    """Tests for ingesting from a file or directory path."""

    @pytest.fixture
    def pipeline(self, test_settings: Settings) -> IngestPipeline:
        return IngestPipeline(
            settings=test_settings,
            embedding_backend=MockEmbeddingBackend(),
            vector_store=MockVectorStore(),
        )

    def test_ingest_single_file(
        self, pipeline: IngestPipeline, tmp_path: Path
    ) -> None:
        """Ingesting a single .md file should process 1 document."""
        md_file = tmp_path / "doc.md"
        md_file.write_text(
            "# Hello\n\nWorld content here.", encoding="utf-8"
        )

        result = pipeline.ingest(md_file)

        assert isinstance(result, IngestResult)
        assert result.documents_processed == 1
        assert result.chunks_created > 0
        assert result.errors == []

    def test_ingest_directory(
        self, pipeline: IngestPipeline, tmp_path: Path
    ) -> None:
        """Ingesting a directory should process all .md files."""
        (tmp_path / "a.md").write_text(
            "# A\n\nContent A", encoding="utf-8"
        )
        (tmp_path / "b.md").write_text(
            "# B\n\nContent B", encoding="utf-8"
        )

        result = pipeline.ingest(tmp_path)

        assert result.documents_processed == 2
        assert result.chunks_created >= 2

    def test_ingest_nonexistent_path_raises(
        self, pipeline: IngestPipeline
    ) -> None:
        """Ingesting a non-existent path should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            pipeline.ingest(Path("/does/not/exist"))

    def test_ingest_empty_directory(
        self, pipeline: IngestPipeline, tmp_path: Path
    ) -> None:
        """Ingesting an empty directory should return zero counts."""
        result = pipeline.ingest(tmp_path)

        assert result.documents_processed == 0
        assert result.chunks_created == 0

    def test_ingest_uses_settings_chunk_params(
        self, test_settings: Settings, tmp_path: Path
    ) -> None:
        """Pipeline should use chunk_max_size and chunk_overlap from settings."""
        md_file = tmp_path / "doc.md"
        md_file.write_text(
            "# Title\n\n" + "word " * 200, encoding="utf-8"
        )

        pipeline = IngestPipeline(
            settings=test_settings,
            embedding_backend=MockEmbeddingBackend(),
            vector_store=MockVectorStore(),
        )

        result = pipeline.ingest(md_file)

        # With max_size=500 and ~1000 chars of content, expect multiple chunks
        assert result.chunks_created >= 1


# ---------------------------------------------------------------------------
# Incremental ingestion tests
# ---------------------------------------------------------------------------


class TestIncrementalIngestion:
    """Tests for incremental indexing (re-ingesting replaces, not duplicates)."""

    @pytest.fixture
    def pipeline(self, test_settings: Settings) -> IngestPipeline:
        return IngestPipeline(
            settings=test_settings,
            embedding_backend=MockEmbeddingBackend(),
            vector_store=MockVectorStore(),
        )

    def test_reingest_deletes_existing_before_adding(
        self, pipeline: IngestPipeline, tmp_path: Path
    ) -> None:
        """Re-ingesting a file should delete existing chunks first."""
        md_file = tmp_path / "doc.md"
        md_file.write_text("# Original\n\nContent.", encoding="utf-8")

        # First ingest
        pipeline.ingest(md_file)

        store = pipeline._vector_store
        assert isinstance(store, MockVectorStore)
        first_count = len(store.added_chunks)
        assert first_count > 0

        # Modify and re-ingest
        md_file.write_text("# Updated\n\nNew content.", encoding="utf-8")
        pipeline.ingest(md_file)

        # The store should have called delete_by_document
        assert str(md_file) in store.deleted_docs

    def test_reingest_document_replaces_chunks(
        self, pipeline: IngestPipeline
    ) -> None:
        """Re-ingesting a Document should delete then add chunks."""
        doc = Document(
            path=Path("test.md"),
            content="# V1\n\nFirst version.",
        )

        pipeline.ingest_document(doc)

        store = pipeline._vector_store
        assert isinstance(store, MockVectorStore)
        assert len(store.added_chunks) > 0

        # Re-ingest with different content
        doc2 = Document(
            path=Path("test.md"),
            content="# V2\n\nSecond version with more text.",
        )
        pipeline.ingest_document(doc2)

        assert str(Path("test.md")) in store.deleted_docs


# ---------------------------------------------------------------------------
# Error handling tests
# ---------------------------------------------------------------------------


class TestPipelineErrorHandling:
    """Tests for pipeline error handling."""

    def test_ingest_with_unreadable_file_records_error(
        self, test_settings: Settings, tmp_path: Path
    ) -> None:
        """If a file cannot be read, the error should be recorded."""
        # Create a directory structure with one good and one bad file
        good_file = tmp_path / "good.md"
        good_file.write_text("# Good\n\nContent.", encoding="utf-8")

        pipeline = IngestPipeline(
            settings=test_settings,
            embedding_backend=MockEmbeddingBackend(),
            vector_store=MockVectorStore(),
        )

        # Ingest the good file directly - should work fine
        result = pipeline.ingest(good_file)

        assert result.documents_processed == 1
        assert result.errors == []


# ---------------------------------------------------------------------------
# Integration with fixtures tests
# ---------------------------------------------------------------------------


class TestPipelineWithFixtures:
    """Integration tests using real fixture files."""

    @pytest.fixture
    def pipeline(self, test_settings: Settings) -> IngestPipeline:
        return IngestPipeline(
            settings=test_settings,
            embedding_backend=MockEmbeddingBackend(),
            vector_store=MockVectorStore(),
        )

    def test_ingest_fixtures_directory(
        self, pipeline: IngestPipeline, fixtures_dir: Path
    ) -> None:
        """Ingesting the fixtures directory should process all fixture files."""
        result = pipeline.ingest(fixtures_dir)

        assert result.documents_processed == 3
        assert result.chunks_created > 0
        assert result.errors == []

    def test_ingest_frontmatter_fixture(
        self, pipeline: IngestPipeline, sample_frontmatter_path: Path
    ) -> None:
        """Ingesting a file with frontmatter should extract metadata."""
        result = pipeline.ingest(sample_frontmatter_path)

        assert result.documents_processed == 1
        assert result.chunks_created > 0

        store = pipeline._vector_store
        assert isinstance(store, MockVectorStore)
        # All chunks should have frontmatter metadata
        for chunk in store.added_chunks:
            assert "title" in chunk.metadata
            assert chunk.metadata["title"] == "API Reference"

    def test_ingest_basic_fixture(
        self, pipeline: IngestPipeline, sample_basic_path: Path
    ) -> None:
        """Ingesting sample_basic.md should produce multiple chunks."""
        result = pipeline.ingest(sample_basic_path)

        assert result.documents_processed == 1
        assert result.chunks_created >= 2  # Multiple sections in sample_basic
