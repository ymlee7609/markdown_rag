"""Tests for the search CLI subcommand."""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_rag.cli.search_cmd import handle_search
from markdown_rag.models import Chunk, SearchResult


@pytest.fixture
def search_args() -> argparse.Namespace:
    """Create a basic search args namespace."""
    return argparse.Namespace(
        command="search",
        query="how to install",
        top_k=5,
        backend="local",
    )


@pytest.fixture
def mock_search_results() -> list[SearchResult]:
    """Create mock search results for testing output."""
    return [
        SearchResult(
            chunk=Chunk(
                content="Run pip install markdown-rag to install the package. "
                "Make sure you have Python 3.11 or later.",
                doc_path=Path("docs/install.md"),
                headers=["Getting Started", "Installation"],
                chunk_index=0,
            ),
            score=0.92,
            rank=1,
        ),
        SearchResult(
            chunk=Chunk(
                content="Configure your environment variables before running.",
                doc_path=Path("docs/config.md"),
                headers=["Configuration"],
                chunk_index=0,
            ),
            score=0.78,
            rank=2,
        ),
    ]


class TestHandleSearch:
    """Test the search subcommand handler."""

    @patch("markdown_rag.cli.search_cmd.ChromaStore")
    @patch("markdown_rag.cli.search_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.search_cmd.get_settings")
    def test_successful_search_local(
        self,
        mock_get_settings: MagicMock,
        mock_local_embedding: MagicMock,
        mock_chroma: MagicMock,
        search_args: argparse.Namespace,
        mock_search_results: list[SearchResult],
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_settings = MagicMock()
        mock_settings.chroma_path = Path("/tmp/chroma")
        mock_settings.collection_name = "test"
        mock_settings.local_model = "all-MiniLM-L6-v2"
        mock_get_settings.return_value = mock_settings

        mock_embedding_instance = MagicMock()
        mock_local_embedding.return_value = mock_embedding_instance

        mock_store_instance = MagicMock()
        mock_chroma.return_value = mock_store_instance

        with patch("markdown_rag.cli.search_cmd.SemanticSearch") as mock_search_class:
            mock_engine = MagicMock()
            mock_engine.search.return_value = mock_search_results
            mock_search_class.return_value = mock_engine

            handle_search(search_args)

        captured = capsys.readouterr()
        # Should display rank, score, source, and content preview
        assert "1" in captured.out  # rank
        assert "0.92" in captured.out or "92" in captured.out  # score
        assert "install.md" in captured.out  # source
        assert "pip install" in captured.out  # content preview

    @patch("markdown_rag.cli.search_cmd.ChromaStore")
    @patch("markdown_rag.cli.search_cmd.OpenAIEmbedding")
    @patch("markdown_rag.cli.search_cmd.get_settings")
    def test_search_openai_backend(
        self,
        mock_get_settings: MagicMock,
        mock_openai_embedding: MagicMock,
        mock_chroma: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_settings = MagicMock()
        mock_settings.chroma_path = Path("/tmp/chroma")
        mock_settings.collection_name = "test"
        mock_settings.openai_embedding_model = "text-embedding-3-small"
        mock_get_settings.return_value = mock_settings

        mock_embedding_instance = MagicMock()
        mock_openai_embedding.return_value = mock_embedding_instance

        mock_store_instance = MagicMock()
        mock_chroma.return_value = mock_store_instance

        args = argparse.Namespace(
            command="search",
            query="test query",
            top_k=3,
            backend="openai",
        )

        with patch("markdown_rag.cli.search_cmd.SemanticSearch") as mock_search_class:
            mock_engine = MagicMock()
            mock_engine.search.return_value = []
            mock_search_class.return_value = mock_engine

            handle_search(args)

        mock_openai_embedding.assert_called_once()

    @patch("markdown_rag.cli.search_cmd.ChromaStore")
    @patch("markdown_rag.cli.search_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.search_cmd.get_settings")
    def test_search_no_results(
        self,
        mock_get_settings: MagicMock,
        mock_local_embedding: MagicMock,
        mock_chroma: MagicMock,
        search_args: argparse.Namespace,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_settings = MagicMock()
        mock_settings.chroma_path = Path("/tmp/chroma")
        mock_settings.collection_name = "test"
        mock_settings.local_model = "all-MiniLM-L6-v2"
        mock_get_settings.return_value = mock_settings

        mock_store_instance = MagicMock()
        mock_chroma.return_value = mock_store_instance

        with patch("markdown_rag.cli.search_cmd.SemanticSearch") as mock_search_class:
            mock_engine = MagicMock()
            mock_engine.search.return_value = []
            mock_search_class.return_value = mock_engine

            handle_search(search_args)

        captured = capsys.readouterr()
        assert "no result" in captured.out.lower() or "0 result" in captured.out.lower()

    @patch("markdown_rag.cli.search_cmd.ChromaStore")
    @patch("markdown_rag.cli.search_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.search_cmd.get_settings")
    def test_search_displays_header_context(
        self,
        mock_get_settings: MagicMock,
        mock_local_embedding: MagicMock,
        mock_chroma: MagicMock,
        search_args: argparse.Namespace,
        mock_search_results: list[SearchResult],
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_settings = MagicMock()
        mock_settings.chroma_path = Path("/tmp/chroma")
        mock_settings.collection_name = "test"
        mock_settings.local_model = "all-MiniLM-L6-v2"
        mock_get_settings.return_value = mock_settings

        mock_store_instance = MagicMock()
        mock_chroma.return_value = mock_store_instance

        with patch("markdown_rag.cli.search_cmd.SemanticSearch") as mock_search_class:
            mock_engine = MagicMock()
            mock_engine.search.return_value = mock_search_results
            mock_search_class.return_value = mock_engine

            handle_search(search_args)

        captured = capsys.readouterr()
        assert "Getting Started" in captured.out or "Installation" in captured.out

    @patch("markdown_rag.cli.search_cmd.ChromaStore")
    @patch("markdown_rag.cli.search_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.search_cmd.get_settings")
    def test_search_content_preview_truncated(
        self,
        mock_get_settings: MagicMock,
        mock_local_embedding: MagicMock,
        mock_chroma: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_settings = MagicMock()
        mock_settings.chroma_path = Path("/tmp/chroma")
        mock_settings.collection_name = "test"
        mock_settings.local_model = "all-MiniLM-L6-v2"
        mock_get_settings.return_value = mock_settings

        mock_store_instance = MagicMock()
        mock_chroma.return_value = mock_store_instance

        long_content = "A" * 500
        results = [
            SearchResult(
                chunk=Chunk(
                    content=long_content,
                    doc_path=Path("test.md"),
                    headers=[],
                    chunk_index=0,
                ),
                score=0.5,
                rank=1,
            ),
        ]

        args = argparse.Namespace(
            command="search",
            query="test",
            top_k=5,
            backend="local",
        )

        with patch("markdown_rag.cli.search_cmd.SemanticSearch") as mock_search_class:
            mock_engine = MagicMock()
            mock_engine.search.return_value = results
            mock_search_class.return_value = mock_engine

            handle_search(args)

        captured = capsys.readouterr()
        # Content should be truncated (first 200 chars)
        assert "..." in captured.out
        # Full 500-char content should not appear
        assert long_content not in captured.out

    @patch("markdown_rag.cli.search_cmd.ChromaStore")
    @patch("markdown_rag.cli.search_cmd.LocalEmbedding")
    @patch("markdown_rag.cli.search_cmd.get_settings")
    def test_search_passes_top_k(
        self,
        mock_get_settings: MagicMock,
        mock_local_embedding: MagicMock,
        mock_chroma: MagicMock,
    ) -> None:
        mock_settings = MagicMock()
        mock_settings.chroma_path = Path("/tmp/chroma")
        mock_settings.collection_name = "test"
        mock_settings.local_model = "all-MiniLM-L6-v2"
        mock_get_settings.return_value = mock_settings

        mock_store_instance = MagicMock()
        mock_chroma.return_value = mock_store_instance

        args = argparse.Namespace(
            command="search",
            query="test",
            top_k=10,
            backend="local",
        )

        with patch("markdown_rag.cli.search_cmd.SemanticSearch") as mock_search_class:
            mock_engine = MagicMock()
            mock_engine.search.return_value = []
            mock_search_class.return_value = mock_engine

            handle_search(args)

            mock_engine.search.assert_called_once_with("test", top_k=10, where=None)
