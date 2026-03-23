"""Ask CLI 서브커맨드 테스트."""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_rag.cli.ask_cmd import handle_ask
from markdown_rag.models import Chunk, RAGResponse, SearchResult


@pytest.fixture
def ask_args() -> argparse.Namespace:
    """기본 ask 인자 생성."""
    return argparse.Namespace(
        command="ask",
        question="What is markdown rag?",
        top_k=5,
        show_sources=False,
        model=None,
        llm_backend=None,
    )


@pytest.fixture
def ask_args_with_sources() -> argparse.Namespace:
    """소스 표시 옵션이 켜진 ask 인자."""
    return argparse.Namespace(
        command="ask",
        question="How to install?",
        top_k=3,
        show_sources=True,
        model=None,
        llm_backend=None,
    )


@pytest.fixture
def mock_rag_response() -> RAGResponse:
    """Mock RAG 응답."""
    return RAGResponse(
        answer="Markdown RAG is a semantic search and QA system.",
        sources=[
            SearchResult(
                chunk=Chunk(
                    content="Markdown RAG provides semantic search.",
                    doc_path=Path("docs/readme.md"),
                    headers=["Overview"],
                    chunk_index=0,
                ),
                score=0.95,
                rank=1,
            ),
        ],
        model="gpt-4o-mini",
        query="What is markdown rag?",
    )


class TestHandleAsk:
    """Ask 서브커맨드 핸들러 테스트."""

    @patch("markdown_rag.cli.ask_cmd.RAGEngine")
    @patch("markdown_rag.cli.ask_cmd.SemanticSearch")
    @patch("markdown_rag.cli.ask_cmd.ChromaStore")
    @patch("markdown_rag.cli.ask_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.ask_cmd._create_llm_backend")
    @patch("markdown_rag.cli.ask_cmd.get_settings")
    def test_successful_ask(
        self,
        mock_get_settings: MagicMock,
        mock_create_llm: MagicMock,
        mock_local_embedding: MagicMock,
        mock_chroma: MagicMock,
        mock_search: MagicMock,
        mock_rag_class: MagicMock,
        ask_args: argparse.Namespace,
        mock_rag_response: RAGResponse,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_settings = MagicMock()
        mock_settings.chroma_path = Path("/tmp/chroma")
        mock_settings.collection_name = "test"
        mock_settings.local_model = "all-MiniLM-L6-v2"
        mock_settings.embedding_backend = "local"
        mock_settings.llm_backend = "openai"
        mock_get_settings.return_value = mock_settings
        mock_create_llm.return_value = MagicMock()

        mock_rag = MagicMock()
        mock_rag.ask.return_value = mock_rag_response
        mock_rag_class.return_value = mock_rag

        handle_ask(ask_args)

        captured = capsys.readouterr()
        assert "Markdown RAG is a semantic search" in captured.out

    @patch("markdown_rag.cli.ask_cmd.RAGEngine")
    @patch("markdown_rag.cli.ask_cmd.SemanticSearch")
    @patch("markdown_rag.cli.ask_cmd.ChromaStore")
    @patch("markdown_rag.cli.ask_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.ask_cmd._create_llm_backend")
    @patch("markdown_rag.cli.ask_cmd.get_settings")
    def test_ask_with_sources(
        self,
        mock_get_settings: MagicMock,
        mock_create_llm: MagicMock,
        mock_local_embedding: MagicMock,
        mock_chroma: MagicMock,
        mock_search: MagicMock,
        mock_rag_class: MagicMock,
        ask_args_with_sources: argparse.Namespace,
        mock_rag_response: RAGResponse,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_settings = MagicMock()
        mock_settings.chroma_path = Path("/tmp/chroma")
        mock_settings.collection_name = "test"
        mock_settings.local_model = "all-MiniLM-L6-v2"
        mock_settings.embedding_backend = "local"
        mock_settings.llm_backend = "openai"
        mock_get_settings.return_value = mock_settings
        mock_create_llm.return_value = MagicMock()

        mock_rag = MagicMock()
        mock_rag.ask.return_value = mock_rag_response
        mock_rag_class.return_value = mock_rag

        handle_ask(ask_args_with_sources)

        captured = capsys.readouterr()
        assert "readme.md" in captured.out or "Source" in captured.out
        assert "Overview" in captured.out

    def test_ask_missing_api_key(
        self,
        ask_args: argparse.Namespace,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(SystemExit) as exc_info:
            handle_ask(ask_args)
        assert exc_info.value.code == 1

    @patch("markdown_rag.cli.ask_cmd.RAGEngine")
    @patch("markdown_rag.cli.ask_cmd.SemanticSearch")
    @patch("markdown_rag.cli.ask_cmd.ChromaStore")
    @patch("markdown_rag.cli.ask_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.ask_cmd._create_llm_backend")
    @patch("markdown_rag.cli.ask_cmd.get_settings")
    def test_ask_passes_llm_backend(
        self,
        mock_get_settings: MagicMock,
        mock_create_llm: MagicMock,
        mock_local_embedding: MagicMock,
        mock_chroma: MagicMock,
        mock_search: MagicMock,
        mock_rag_class: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_settings = MagicMock()
        mock_settings.chroma_path = Path("/tmp/chroma")
        mock_settings.collection_name = "test"
        mock_settings.local_model = "all-MiniLM-L6-v2"
        mock_settings.embedding_backend = "local"
        mock_settings.llm_backend = "openai"
        mock_get_settings.return_value = mock_settings

        mock_llm = MagicMock()
        mock_create_llm.return_value = mock_llm

        mock_rag = MagicMock()
        mock_rag.ask.return_value = RAGResponse(
            answer="test", sources=[], model="gpt-4o", query="test"
        )
        mock_rag_class.return_value = mock_rag

        args = argparse.Namespace(
            command="ask",
            question="test",
            top_k=5,
            show_sources=False,
            model="gpt-4o",
            llm_backend=None,
        )

        handle_ask(args)

        # RAGEngine에 llm_backend가 전달됨
        mock_rag_class.assert_called_once()
        call_kwargs = mock_rag_class.call_args.kwargs
        assert call_kwargs["llm_backend"] is mock_llm

    @patch("markdown_rag.cli.ask_cmd.RAGEngine")
    @patch("markdown_rag.cli.ask_cmd.SemanticSearch")
    @patch("markdown_rag.cli.ask_cmd.ChromaStore")
    @patch("markdown_rag.cli.ask_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.ask_cmd._create_llm_backend")
    @patch("markdown_rag.cli.ask_cmd.get_settings")
    def test_ask_without_sources_flag(
        self,
        mock_get_settings: MagicMock,
        mock_create_llm: MagicMock,
        mock_local_embedding: MagicMock,
        mock_chroma: MagicMock,
        mock_search: MagicMock,
        mock_rag_class: MagicMock,
        ask_args: argparse.Namespace,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_settings = MagicMock()
        mock_settings.chroma_path = Path("/tmp/chroma")
        mock_settings.collection_name = "test"
        mock_settings.local_model = "all-MiniLM-L6-v2"
        mock_settings.embedding_backend = "local"
        mock_settings.llm_backend = "openai"
        mock_get_settings.return_value = mock_settings
        mock_create_llm.return_value = MagicMock()

        response_no_sources = RAGResponse(
            answer="The answer is 42.",
            sources=[
                SearchResult(
                    chunk=Chunk(
                        content="Source text",
                        doc_path=Path("hidden.md"),
                        headers=["Secret"],
                        chunk_index=0,
                    ),
                    score=0.8,
                    rank=1,
                ),
            ],
            model="gpt-4o-mini",
            query="question",
        )

        mock_rag = MagicMock()
        mock_rag.ask.return_value = response_no_sources
        mock_rag_class.return_value = mock_rag

        handle_ask(ask_args)

        captured = capsys.readouterr()
        assert "The answer is 42." in captured.out
        # --show-sources 없으면 소스가 표시되지 않아야 함
        assert "hidden.md" not in captured.out
