"""Ask 서브커맨드 - RAG 기반 질의응답.

OpenAI 또는 로컬 SLM을 사용하여 질의응답을 수행한다.
"""

from __future__ import annotations

import argparse
import os
import sys

from markdown_rag.cli.search_cmd import _build_where_filter
from markdown_rag.config import get_settings
from markdown_rag.embedding.local import LocalEmbedding
from markdown_rag.embedding.openai import OpenAIEmbedding
from markdown_rag.retriever.rag import RAGEngine
from markdown_rag.retriever.search import SemanticSearch
from markdown_rag.store.chroma import ChromaStore


def _create_llm_backend(settings, model_override: str | None = None):
    """설정에 따라 LLM 백엔드를 생성한다."""
    if settings.llm_backend == "local":
        from markdown_rag.llm.local import LocalLLM

        if not settings.local_llm_model_path:
            print(
                "오류: 로컬 LLM 모델 경로가 설정되지 않았습니다.\n"
                "MDRAG_LOCAL_LLM_MODEL_PATH 환경 변수를 설정하세요.",
                file=sys.stderr,
            )
            sys.exit(1)
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
        print(
            "오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.\n"
            "설정: export OPENAI_API_KEY='your-api-key'",
            file=sys.stderr,
        )
        sys.exit(1)
    model = model_override or settings.openai_llm_model
    return OpenAILLM(model=model, api_key=api_key)


def handle_ask(args: argparse.Namespace) -> None:
    """Ask 서브커맨드를 실행한다.

    SemanticSearch 백엔드로 RAGEngine을 생성하고,
    설정된 LLM 백엔드로 질의응답을 수행한다.

    Args:
        args: question, top_k, show_sources, model을 포함하는 파싱된 인자.
    """
    settings = get_settings()

    # 로컬 LLM이 첫 글자를 누락하는 현상 방지용 더미 공백 추가
    args.question = " " + args.question

    # CLI에서 --llm-backend 옵션으로 오버라이드 가능
    if getattr(args, "llm_backend", None):
        settings.llm_backend = args.llm_backend

    llm_backend = _create_llm_backend(settings, model_override=args.model)

    # 임베딩 백엔드 초기화
    if settings.embedding_backend == "openai":
        embedding = OpenAIEmbedding(model_name=settings.openai_embedding_model)
    else:
        embedding = LocalEmbedding(model_name=settings.local_model)

    # 벡터 스토어 초기화
    store = ChromaStore(
        persist_path=settings.chroma_path,
        collection_name=settings.collection_name,
    )

    # 검색 엔진 생성
    search_engine = SemanticSearch(
        embedding_backend=embedding,
        vector_store=store,
    )

    # RAG 엔진 생성
    rag = RAGEngine(
        search_engine=search_engine,
        llm_backend=llm_backend,
    )

    where = _build_where_filter(args)
    response = rag.ask(
        query=args.question,
        top_k=args.top_k,
        show_sources=args.show_sources,
        where=where,
    )

    # 답변 출력
    print(response.answer)

    # 소스 출력
    if args.show_sources and response.sources:
        print("\n--- Sources ---")
        for src in response.sources:
            chunk = src.chunk
            header_ctx = chunk.header_context
            print(f"  [{src.rank}] {chunk.doc_path}")
            if header_ctx:
                print(f"       Section: {header_ctx}")
            print(f"       Score: {src.score:.4f}")
