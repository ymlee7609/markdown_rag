"""Health, status, and document deletion routes."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Request

from markdown_rag.api.schemas import (
    DeleteRequest,
    DeleteResponse,
    HealthResponse,
    StatusResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return a simple health check response."""
    return HealthResponse(status="ok")


@router.get("/api/v1/status", response_model=StatusResponse)
def get_status(request: Request) -> StatusResponse:
    """Return index status with collection statistics."""
    settings = request.app.state.settings
    store = request.app.state.vector_store
    return StatusResponse(
        collection_name=settings.collection_name,
        total_chunks=store.count(),
        embedding_backend=settings.embedding_backend,
    )


@router.delete("/api/v1/documents", response_model=DeleteResponse)
def delete_documents(body: DeleteRequest, request: Request) -> DeleteResponse:
    """Delete all chunks for a given document path."""
    store = request.app.state.vector_store
    deleted = store.delete_by_document(body.doc_path)
    logger.info("Deleted %d chunks for '%s'", deleted, body.doc_path)
    return DeleteResponse(doc_path=body.doc_path, chunks_deleted=deleted)
