"""RAG 질의응답 라우트."""

from __future__ import annotations

import logging
import os

from fastapi import APIRouter, HTTPException, Request

from markdown_rag.api.routes.search import _build_where_filter, _to_chunk_response
from markdown_rag.api.schemas import (
    AskRequest,
    AskResponse,
    SearchResultResponse,
)
from markdown_rag.config import Settings
from markdown_rag.llm.base import LLMBackend
from markdown_rag.retriever.builder import build_search_engine
from markdown_rag.retriever.rag import RAGEngine

logger = logging.getLogger(__name__)

router = APIRouter()


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
            chat_template_path=settings.local_llm_chat_template_path or None,
            temperature=settings.local_llm_temperature,
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

    try:
        llm_backend = _get_llm_backend(settings, model_override=body.model)
        # 검색 엔진은 builder가 mode에 따라 SemanticSearch/Hybrid/OntologyAug 자동 선택
        search_engine = build_search_engine(settings, mode_override=body.mode)
        rag_engine = RAGEngine(
            search_engine=search_engine,
            llm_backend=llm_backend,
        )
        where = _build_where_filter(doc_type=body.doc_type, language=body.language)
        rag_response = rag_engine.ask(
            query=body.query,
            top_k=body.top_k,
            show_sources=body.show_sources,
            where=where,
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
            chunk=_to_chunk_response(r.chunk),
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
