"""RAG (Retrieval-Augmented Generation) 엔진."""

from __future__ import annotations

import logging

from markdown_rag.llm.base import LLMBackend
from markdown_rag.models import RAGResponse, SearchResult
from markdown_rag.retriever.search import SemanticSearch

logger = logging.getLogger(__name__)

# 시스템 프롬프트: 컨텍스트 기반 답변만 하도록 지시
_SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions based on the "
    "provided context only. If the context does not contain enough "
    "information to answer the question, say 'I don't know based on "
    "the provided context.' When answering, cite the source documents."
)


class RAGEngine:
    """시맨틱 검색과 LLM을 결합한 RAG 엔진.

    SemanticSearch로 관련 청크를 검색한 뒤, LLMBackend를 통해
    응답을 생성한다. OpenAI와 로컬 SLM 모두 지원.
    """

    def __init__(
        self,
        search_engine: SemanticSearch,
        llm_backend: LLMBackend,
    ) -> None:
        self.search_engine = search_engine
        self.llm_backend = llm_backend

    def ask(
        self,
        query: str,
        top_k: int | None = None,
        show_sources: bool = True,
        where: dict | None = None,
    ) -> RAGResponse:
        """질문에 대해 인덱싱된 문서 기반으로 답변을 생성한다.

        Args:
            query: 사용자 질문.
            top_k: 검색할 청크 수. None이면 검색 엔진 기본값 사용.
            show_sources: 응답에 소스 청크를 포함할지 여부.
            where: 선택적 메타데이터 필터 (ChromaDB where 절).

        Returns:
            답변, 소스, 모델명, 질문을 포함하는 RAGResponse.
        """
        search_results = self.search_engine.search(query, top_k=top_k, where=where)

        context = self._build_context(search_results)

        user_message = (
            f"Context:\n{context}\n\nQuestion: {query}"
            if context
            else f"Question: {query}"
        )

        messages = [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        answer = self.llm_backend.generate(messages)

        return RAGResponse(
            answer=answer,
            sources=search_results if show_sources else [],
            model=self.llm_backend.model_name,
            query=query,
        )

    def _build_context(self, results: list[SearchResult]) -> str:
        """검색 결과로부터 컨텍스트 문자열을 구성한다.

        각 청크는 소스 경로, 헤더 계층, 내용으로 포맷팅된다.
        """
        if not results:
            return ""

        parts: list[str] = []
        for result in results:
            chunk = result.chunk
            header = chunk.header_context
            source_line = f"## Source: {chunk.doc_path}"
            if header:
                source_line += f" > {header}"
            parts.append(f"{source_line}\n{chunk.content}")

        return "\n\n".join(parts)
