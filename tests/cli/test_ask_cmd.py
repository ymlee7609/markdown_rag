"""Ask CLI 서브커맨드 테스트."""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_rag.cli.ask_cmd import _create_llm_backend, handle_ask
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


def _mock_settings(**overrides):
    """테스트용 Settings mock 생성."""
    defaults = {
        "chroma_path": Path("/tmp/chroma"),
        "collection_name": "test",
        "local_model": "all-MiniLM-L6-v2",
        "embedding_backend": "local",
        "llm_backend": "openai",
        "openai_llm_model": "gpt-4o-mini",
        "local_llm_model_path": "",
        "local_llm_context_size": 4096,
        "local_llm_max_tokens": 1024,
    }
    defaults.update(overrides)
    settings = MagicMock()
    for k, v in defaults.items():
        setattr(settings, k, v)
    return settings


class TestCreateLLMBackend:
    """_create_llm_backend 함수 테스트."""

    def test_openai_backend_returns_openai_llm(self, monkeypatch) -> None:
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        settings = _mock_settings(llm_backend="openai")
        llm = _create_llm_backend(settings)
        assert llm.model_name == "gpt-4o-mini"

    def test_openai_backend_with_model_override(self, monkeypatch) -> None:
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        settings = _mock_settings(llm_backend="openai")
        llm = _create_llm_backend(settings, model_override="gpt-4o")
        assert llm.model_name == "gpt-4o"

    def test_openai_backend_missing_api_key_exits(self, monkeypatch) -> None:
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        settings = _mock_settings(llm_backend="openai")
        with pytest.raises(SystemExit) as exc:
            _create_llm_backend(settings)
        assert exc.value.code == 1

    @patch("markdown_rag.llm.local.LocalLLM")
    def test_local_backend_returns_local_llm(self, mock_local_cls) -> None:
        mock_local_cls.return_value = MagicMock()
        settings = _mock_settings(
            llm_backend="local",
            local_llm_model_path="/models/test.gguf",
        )
        _create_llm_backend(settings)
        mock_local_cls.assert_called_once_with(
            model_path="/models/test.gguf",
            context_size=4096,
            max_tokens=1024,
        )

    def test_local_backend_missing_model_path_exits(self) -> None:
        settings = _mock_settings(llm_backend="local", local_llm_model_path="")
        with pytest.raises(SystemExit) as exc:
            _create_llm_backend(settings)
        assert exc.value.code == 1


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
        mock_get_settings,
        mock_create_llm,
        mock_local_embedding,
        mock_chroma,
        mock_search,
        mock_rag_class,
        ask_args,
        mock_rag_response,
        capsys,
    ) -> None:
        mock_get_settings.return_value = _mock_settings()
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
    def test_ask_with_sources_and_headers(
        self,
        mock_get_settings,
        mock_create_llm,
        mock_local_embedding,
        mock_chroma,
        mock_search,
        mock_rag_class,
        ask_args_with_sources,
        mock_rag_response,
        capsys,
    ) -> None:
        mock_get_settings.return_value = _mock_settings()
        mock_create_llm.return_value = MagicMock()

        mock_rag = MagicMock()
        mock_rag.ask.return_value = mock_rag_response
        mock_rag_class.return_value = mock_rag

        handle_ask(ask_args_with_sources)

        captured = capsys.readouterr()
        assert "--- Sources ---" in captured.out
        assert "readme.md" in captured.out
        assert "Overview" in captured.out
        assert "0.9500" in captured.out

    @patch("markdown_rag.cli.ask_cmd.RAGEngine")
    @patch("markdown_rag.cli.ask_cmd.SemanticSearch")
    @patch("markdown_rag.cli.ask_cmd.ChromaStore")
    @patch("markdown_rag.cli.ask_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.ask_cmd._create_llm_backend")
    @patch("markdown_rag.cli.ask_cmd.get_settings")
    def test_ask_sources_without_headers(
        self,
        mock_get_settings,
        mock_create_llm,
        mock_local_embedding,
        mock_chroma,
        mock_search,
        mock_rag_class,
        capsys,
    ) -> None:
        mock_get_settings.return_value = _mock_settings()
        mock_create_llm.return_value = MagicMock()

        response = RAGResponse(
            answer="answer",
            sources=[
                SearchResult(
                    chunk=Chunk(
                        content="text",
                        doc_path=Path("doc.md"),
                        headers=[],
                        chunk_index=0,
                    ),
                    score=0.5,
                    rank=1,
                ),
            ],
            model="m",
            query="q",
        )
        mock_rag = MagicMock()
        mock_rag.ask.return_value = response
        mock_rag_class.return_value = mock_rag

        args = argparse.Namespace(
            command="ask", question="q", top_k=5,
            show_sources=True, model=None, llm_backend=None,
        )
        handle_ask(args)

        captured = capsys.readouterr()
        assert "doc.md" in captured.out
        assert "Section" not in captured.out

    @patch("markdown_rag.cli.ask_cmd.RAGEngine")
    @patch("markdown_rag.cli.ask_cmd.SemanticSearch")
    @patch("markdown_rag.cli.ask_cmd.ChromaStore")
    @patch("markdown_rag.cli.ask_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.ask_cmd._create_llm_backend")
    @patch("markdown_rag.cli.ask_cmd.get_settings")
    def test_llm_backend_cli_override(
        self,
        mock_get_settings,
        mock_create_llm,
        mock_local_embedding,
        mock_chroma,
        mock_search,
        mock_rag_class,
        capsys,
    ) -> None:
        settings = _mock_settings(llm_backend="openai")
        mock_get_settings.return_value = settings
        mock_create_llm.return_value = MagicMock()

        mock_rag = MagicMock()
        mock_rag.ask.return_value = RAGResponse(
            answer="ok", sources=[], model="m", query="q"
        )
        mock_rag_class.return_value = mock_rag

        args = argparse.Namespace(
            command="ask", question="q", top_k=5,
            show_sources=False, model=None, llm_backend="local",
        )
        handle_ask(args)

        assert settings.llm_backend == "local"

    @patch("markdown_rag.cli.ask_cmd.RAGEngine")
    @patch("markdown_rag.cli.ask_cmd.SemanticSearch")
    @patch("markdown_rag.cli.ask_cmd.ChromaStore")
    @patch("markdown_rag.cli.ask_cmd.OpenAIEmbedding")
    @patch("markdown_rag.cli.ask_cmd._create_llm_backend")
    @patch("markdown_rag.cli.ask_cmd.get_settings")
    def test_openai_embedding_branch(
        self,
        mock_get_settings,
        mock_create_llm,
        mock_openai_emb,
        mock_chroma,
        mock_search,
        mock_rag_class,
        ask_args,
        capsys,
    ) -> None:
        mock_get_settings.return_value = _mock_settings(embedding_backend="openai")
        mock_create_llm.return_value = MagicMock()

        mock_rag = MagicMock()
        mock_rag.ask.return_value = RAGResponse(
            answer="ok", sources=[], model="m", query="q"
        )
        mock_rag_class.return_value = mock_rag

        handle_ask(ask_args)

        mock_openai_emb.assert_called_once()

    @patch("markdown_rag.cli.ask_cmd.RAGEngine")
    @patch("markdown_rag.cli.ask_cmd.SemanticSearch")
    @patch("markdown_rag.cli.ask_cmd.ChromaStore")
    @patch("markdown_rag.cli.ask_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.ask_cmd._create_llm_backend")
    @patch("markdown_rag.cli.ask_cmd.get_settings")
    def test_ask_without_sources_flag(
        self,
        mock_get_settings,
        mock_create_llm,
        mock_local_embedding,
        mock_chroma,
        mock_search,
        mock_rag_class,
        ask_args,
        capsys,
    ) -> None:
        mock_get_settings.return_value = _mock_settings()
        mock_create_llm.return_value = MagicMock()

        response_no_sources = RAGResponse(
            answer="The answer is 42.",
            sources=[],
            model="gpt-4o-mini",
            query="question",
        )
        mock_rag = MagicMock()
        mock_rag.ask.return_value = response_no_sources
        mock_rag_class.return_value = mock_rag

        handle_ask(ask_args)

        captured = capsys.readouterr()
        assert "The answer is 42." in captured.out
        assert "Sources" not in captured.out
