"""Document ingestion route."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request

from markdown_rag.api.schemas import IngestRequest, IngestResponse
from markdown_rag.ingest.pipeline import IngestPipeline

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/v1/ingest", response_model=IngestResponse)
def ingest_documents(body: IngestRequest, request: Request) -> IngestResponse:
    """Ingest Markdown documents from the specified path."""
    settings = request.app.state.settings

    try:
        pipeline = IngestPipeline(settings=settings)
        result = pipeline.ingest(path=Path(body.path), verbose=body.verbose)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Ingestion failed: %s", exc)
        raise HTTPException(
            status_code=500, detail=f"Ingestion failed: {exc}"
        ) from exc

    return IngestResponse(
        documents_processed=result.documents_processed,
        chunks_created=result.chunks_created,
        errors=result.errors,
    )
