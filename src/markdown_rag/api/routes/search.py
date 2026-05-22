"""Semantic / hybrid / ontology-augmented search route."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Request

from markdown_rag.api.schemas import (
    ChunkResponse,
    SearchRequest,
    SearchResponse,
    SearchResultResponse,
)
from markdown_rag.retriever.builder import build_search_engine

logger = logging.getLogger(__name__)

router = APIRouter()


def _build_where_filter(
    doc_type: str | None = None,
    language: str | None = None,
) -> dict | None:
    """메타데이터 필터를 ChromaDB where 절로 변환한다."""
    conditions = []
    if doc_type:
        conditions.append({"doc_type": doc_type})
    if language:
        conditions.append({"language": language})

    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def _to_chunk_response(chunk) -> ChunkResponse:
    """Chunk → ChunkResponse with ontology metadata extraction."""
    meta = chunk.metadata or {}
    refs = (
        meta.get("referenced_paths_injectable", [])
        + meta.get("referenced_paths_directories", [])
    )
    return ChunkResponse(
        content=chunk.content,
        doc_path=str(chunk.doc_path),
        headers=chunk.headers,
        chunk_index=chunk.chunk_index,
        via_onto_card=bool(meta.get("via_onto_card", False)),
        referenced_paths=refs,
        injected_by_onto_card=meta.get("injected_by_onto_card"),
    )


@router.post("/api/v1/search", response_model=SearchResponse)
def search_documents(body: SearchRequest, request: Request) -> SearchResponse:
    """Run semantic / hybrid / ontology-augmented search over indexed documents.

    Per-request `mode` overrides settings.search_mode. Supported values:
    "vector", "hybrid", "ontology".
    """
    settings = request.app.state.settings

    try:
        engine = build_search_engine(settings, mode_override=body.mode)
        where = _build_where_filter(doc_type=body.doc_type, language=body.language)
        results = engine.search(query=body.query, top_k=body.top_k, where=where)
    except Exception as exc:
        logger.exception("Search failed: %s", exc)
        raise HTTPException(
            status_code=500, detail=f"Search failed: {exc}"
        ) from exc

    response_results = [
        SearchResultResponse(
            chunk=_to_chunk_response(r.chunk),
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
