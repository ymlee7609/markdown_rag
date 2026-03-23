"""Semantic search route."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Request

from markdown_rag.api.schemas import (
    ChunkResponse,
    SearchRequest,
    SearchResponse,
    SearchResultResponse,
)
from markdown_rag.config import Settings
from markdown_rag.embedding.local import LocalEmbedding
from markdown_rag.embedding.openai import OpenAIEmbedding
from markdown_rag.retriever.search import SemanticSearch

logger = logging.getLogger(__name__)

router = APIRouter()


def _get_embedding_backend(settings: Settings) -> object:
    """Create an embedding backend based on settings."""
    if settings.embedding_backend == "openai":
        return OpenAIEmbedding(model_name=settings.openai_embedding_model)
    return LocalEmbedding(model_name=settings.local_model)


@router.post("/api/v1/search", response_model=SearchResponse)
def search_documents(body: SearchRequest, request: Request) -> SearchResponse:
    """Run semantic search over indexed documents."""
    settings = request.app.state.settings
    store = request.app.state.vector_store

    try:
        embedding = _get_embedding_backend(settings)
        engine = SemanticSearch(
            embedding_backend=embedding,
            vector_store=store,
            top_k=body.top_k,
        )
        results = engine.search(query=body.query, top_k=body.top_k)
    except Exception as exc:
        logger.exception("Search failed: %s", exc)
        raise HTTPException(
            status_code=500, detail=f"Search failed: {exc}"
        ) from exc

    response_results = [
        SearchResultResponse(
            chunk=ChunkResponse(
                content=r.chunk.content,
                doc_path=str(r.chunk.doc_path),
                headers=r.chunk.headers,
                chunk_index=r.chunk.chunk_index,
            ),
            score=r.score,
            rank=r.rank,
        )
        for r in results
    ]

    return SearchResponse(
        query=body.query,
        results=response_results,
        total=len(response_results),
    )
