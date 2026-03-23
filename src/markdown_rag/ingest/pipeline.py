"""Document ingestion pipeline for Markdown RAG.

Orchestrates the full ingestion flow: scan -> chunk -> embed -> store.
Supports incremental indexing by deleting existing chunks before re-ingesting.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from markdown_rag.chunker.metadata import extract_frontmatter
from markdown_rag.chunker.splitter import split_markdown
from markdown_rag.config import Settings
from markdown_rag.embedding.local import LocalEmbedding
from markdown_rag.embedding.openai import OpenAIEmbedding
from markdown_rag.ingest.scanner import MarkdownScanner
from markdown_rag.models import Document
from markdown_rag.store.chroma import ChromaStore

logger = logging.getLogger(__name__)


@dataclass
class IngestResult:
    """Result summary from an ingestion run.

    Attributes:
        documents_processed: Number of documents successfully processed.
        chunks_created: Total number of chunks created across all documents.
        errors: List of error messages for any failures encountered.
    """

    documents_processed: int
    chunks_created: int
    errors: list[str] = field(default_factory=list)


class IngestPipeline:
    """Orchestrates the document ingestion pipeline.

    Scans for Markdown files, splits them into chunks,
    generates embeddings, and stores them in a vector store.

    Supports incremental indexing: re-ingesting a document
    deletes its existing chunks before adding new ones.

    Args:
        settings: Application settings for chunk size, overlap, etc.
        embedding_backend: Embedding backend instance.
            If None, creates one based on settings.embedding_backend.
        vector_store: Vector store instance.
            If None, creates a ChromaStore from settings.
    """

    def __init__(
        self,
        settings: Settings,
        embedding_backend: object | None = None,
        vector_store: object | None = None,
    ) -> None:
        self._settings = settings
        self._scanner = MarkdownScanner()

        # Initialize embedding backend
        if embedding_backend is not None:
            self._embedding_backend = embedding_backend
        elif settings.embedding_backend == "openai":
            self._embedding_backend = OpenAIEmbedding(
                model_name=settings.openai_embedding_model
            )
        else:
            self._embedding_backend = LocalEmbedding(
                model_name=settings.local_model
            )

        # Initialize vector store
        if vector_store is not None:
            self._vector_store = vector_store
        else:
            self._vector_store = ChromaStore(
                persist_path=settings.chroma_path,
                collection_name=settings.collection_name,
            )

    def ingest(self, path: Path, verbose: bool = False) -> IngestResult:
        """Ingest Markdown documents from a file or directory.

        Scans the path for Markdown files, then processes each document
        through the chunking, embedding, and storage pipeline.

        Args:
            path: Path to a single .md file or a directory to scan.
            verbose: If True, log detailed progress information.

        Returns:
            IngestResult with processing statistics.

        Raises:
            FileNotFoundError: If the path does not exist.
        """
        documents = self._scanner.scan(path)

        total_chunks = 0
        errors: list[str] = []

        for doc in documents:
            try:
                chunk_count = self.ingest_document(doc)
                total_chunks += chunk_count
                if verbose:
                    logger.info(
                        "Ingested %s: %d chunks", doc.path, chunk_count
                    )
            except Exception as exc:
                error_msg = f"Error processing {doc.path}: {exc}"
                logger.error(error_msg)
                errors.append(error_msg)

        result = IngestResult(
            documents_processed=len(documents),
            chunks_created=total_chunks,
            errors=errors,
        )

        logger.info(
            "Ingestion complete: %d documents, %d chunks, %d errors",
            result.documents_processed,
            result.chunks_created,
            len(result.errors),
        )

        return result

    def ingest_document(self, doc: Document) -> int:
        """Process a single document through the ingestion pipeline.

        Steps:
        1. Delete existing chunks for this document (incremental indexing).
        2. Extract frontmatter metadata.
        3. Split into chunks using structure-aware splitting.
        4. Generate embeddings for all chunks.
        5. Store chunks and embeddings in the vector store.

        Args:
            doc: Document to process.

        Returns:
            Number of chunks created.
        """
        # Step 1: Delete existing chunks for incremental indexing
        self._vector_store.delete_by_document(str(doc.path))

        # Step 2: Extract frontmatter metadata
        fm_metadata, _body = extract_frontmatter(doc.content)
        base_metadata = {**doc.metadata, **fm_metadata}

        # Step 3: Split into chunks
        chunks = split_markdown(
            content=doc.content,
            doc_path=doc.path,
            max_chunk_size=self._settings.chunk_max_size,
            overlap=self._settings.chunk_overlap,
            metadata=base_metadata,
        )

        if not chunks:
            logger.debug("No chunks produced for %s", doc.path)
            return 0

        # Step 4: Generate embeddings
        texts = [chunk.content for chunk in chunks]
        embeddings = self._embedding_backend.embed_texts(texts)

        # Step 5: Store chunks and embeddings
        self._vector_store.add_chunks(chunks, embeddings)

        logger.debug(
            "Stored %d chunks for %s", len(chunks), doc.path
        )

        return len(chunks)
