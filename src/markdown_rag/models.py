"""Domain models for Markdown RAG system."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Document:
    """Represents a Markdown document."""

    path: Path
    content: str
    metadata: dict = field(default_factory=dict)

    @property
    def file_name(self) -> str:
        return self.path.name


@dataclass
class Chunk:
    """A chunk of text extracted from a Markdown document."""

    content: str
    doc_path: Path
    headers: list[str] = field(default_factory=list)
    chunk_index: int = 0
    metadata: dict = field(default_factory=dict)

    @property
    def header_context(self) -> str:
        """Return the header hierarchy as a string."""
        return " > ".join(self.headers) if self.headers else ""

    @property
    def chunk_id(self) -> str:
        """Unique identifier for this chunk."""
        return f"{self.doc_path}::chunk-{self.chunk_index}"


@dataclass
class SearchResult:
    """A single search result from semantic search."""

    chunk: Chunk
    score: float
    rank: int = 0


@dataclass
class RAGResponse:
    """Response from RAG question answering."""

    answer: str
    sources: list[SearchResult] = field(default_factory=list)
    model: str = ""
    query: str = ""
