"""RAG 질의응답 라우트."""

from __future__ import annotations

import logging
import os

from fastapi import APIRouter, HTTPException, Request

from markdown_rag.api.schemas import (
    AskRequest,
    AskResponse,
    ChunkResponse,
    SearchResultResponse,
)
from markdown_rag.config import Settings
from markdown_rag.embedding.local import LocalEmbedding
from markdown_rag.embedding.openai import OpenAIEmbedding
from markdown_rag.llm.base import LLMBackend
from markdown_rag.retriever.rag import RAGEngine
from markdown_rag.retriever.search import SemanticSearch

logger = logging.getLogger(__name__)

router = APIRouter()


def _get_embedding_backend(settings: Settings) -> object:
    """설정에 따라 임베딩 백엔드를 생성한다."""
    if settings.embedding_backend == "openai":
        return OpenAIEmbedding(model_name=settings.openai_embedding_model)
    return LocalEmbedding(model_name=settings.local_model)


def _get_llm_backend(settings: Settings, model_override: str | None = None) -> LLMBackend:
    """설정에 따라 LLM 백엔드를 생성한다."""
    if settings.llm_backend == "local":
        from markdown_rag.llm.local import LocalLLM

        if not settings.local_llm_model_path:
            raise HTTPException(
                status_code=400,
                detail="MDRAG_LOCAL_LLM_MODEL_PATH 환경 변수가 설정되지 않았습니다.",
            )
        return LocalLLM(
            model_path=settings.local_llm_model_path,
            context_size=settings.local_llm_context_size,
            max_tokens=settings.local_llm_max_tokens,
        )

    # OpenAI 백엔드
    from markdown_rag.llm.openai import OpenAILLM

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.",
        )
    model = model_override or settings.openai_llm_model
    return OpenAILLM(model=model, api_key=api_key)


@router.post("/api/v1/ask", response_model=AskResponse)
def ask_question(body: AskRequest, request: Request) -> AskResponse:
    """RAG(Retrieval-Augmented Generation) 기반 질의응답."""
    settings = request.app.state.settings
    store = request.app.state.vector_store

    try:
        embedding = _get_embedding_backend(settings)
        llm_backend = _get_llm_backend(settings, model_override=body.model)
        search_engine = SemanticSearch(
            embedding_backend=embedding,
            vector_store=store,
            top_k=body.top_k,
        )
        rag_engine = RAGEngine(
            search_engine=search_engine,
            llm_backend=llm_backend,
        )
        rag_response = rag_engine.ask(
            query=body.query,
            top_k=body.top_k,
            show_sources=body.show_sources,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("RAG 질의 실패: %s", exc)
        raise HTTPException(
            status_code=500, detail=f"RAG 질의 실패: {exc}"
        ) from exc

    response_sources = [
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
        for r in rag_response.sources
    ]

    return AskResponse(
        answer=rag_response.answer,
        query=rag_response.query,
        model=rag_response.model,
        sources=response_sources,
    )
