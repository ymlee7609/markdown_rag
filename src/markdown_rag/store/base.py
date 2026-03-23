"""Vector store protocol definition."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from markdown_rag.models import Chunk, SearchResult


@runtime_checkable
class VectorStore(Protocol):
    """Protocol for vector storage backends."""

    def add_chunks(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """Add chunks with their embeddings to the store."""
        ...

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[SearchResult]:
        """Search for similar chunks by query embedding."""
        ...

    def delete_by_document(self, doc_path: str) -> int:
        """Delete all chunks from a specific document. Returns count deleted."""
        ...

    def count(self) -> int:
        """Return total number of stored chunks."""
        ...

    def clear(self) -> None:
        """Remove all data from the store."""
        ...
