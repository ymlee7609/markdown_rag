"""Pydantic request/response models for the Markdown RAG API."""

from __future__ import annotations

from pydantic import BaseModel

# --- Request models ---


class IngestRequest(BaseModel):
    """Request body for document ingestion."""

    path: str
    verbose: bool = False


class SearchRequest(BaseModel):
    """Request body for semantic search."""

    query: str
    top_k: int = 5


class AskRequest(BaseModel):
    """Request body for RAG question answering."""

    query: str
    top_k: int = 5
    show_sources: bool = True
    model: str = "gpt-4o-mini"


class DeleteRequest(BaseModel):
    """Request body for document deletion."""

    doc_path: str


# --- Response models ---


class ChunkResponse(BaseModel):
    """Serialized representation of a Chunk."""

    content: str
    doc_path: str
    headers: list[str]
    chunk_index: int


class SearchResultResponse(BaseModel):
    """Serialized representation of a SearchResult."""

    chunk: ChunkResponse
    score: float
    rank: int


class IngestResponse(BaseModel):
    """Response from the ingestion endpoint."""

    documents_processed: int
    chunks_created: int
    errors: list[str]


class SearchResponse(BaseModel):
    """Response from the search endpoint."""

    query: str
    results: list[SearchResultResponse]
    total: int


class AskResponse(BaseModel):
    """Response from the RAG ask endpoint."""

    answer: str
    query: str
    model: str
    sources: list[SearchResultResponse]


class StatusResponse(BaseModel):
    """Response from the status endpoint."""

    collection_name: str
    total_chunks: int
    embedding_backend: str


class HealthResponse(BaseModel):
    """Response from the health check endpoint."""

    status: str


class DeleteResponse(BaseModel):
    """Response from the document deletion endpoint."""

    doc_path: str
    chunks_deleted: int
