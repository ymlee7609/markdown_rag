"""Tests for the status subcommand."""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import MagicMock, patch

from markdown_rag.cli.status_cmd import handle_status


class TestHandleStatus:
    def test_prints_status_header(self, capsys):
        mock_store = MagicMock()
        mock_store.count.return_value = 42

        with (
            patch("markdown_rag.cli.status_cmd.get_settings") as mock_settings,
            patch("markdown_rag.cli.status_cmd.ChromaStore", return_value=mock_store),
        ):
            mock_settings.return_value.collection_name = "test_col"
            mock_settings.return_value.chroma_path = Path("/tmp/chroma")
            mock_settings.return_value.embedding_backend = "local"

            handle_status(argparse.Namespace())

        output = capsys.readouterr().out
        assert "Markdown RAG Status" in output
        assert "=" * 40 in output

    def test_shows_collection_name(self, capsys):
        mock_store = MagicMock()
        mock_store.count.return_value = 0

        with (
            patch("markdown_rag.cli.status_cmd.get_settings") as mock_settings,
            patch("markdown_rag.cli.status_cmd.ChromaStore", return_value=mock_store),
        ):
            mock_settings.return_value.collection_name = "my_docs"
            mock_settings.return_value.chroma_path = Path("/data")
            mock_settings.return_value.embedding_backend = "local"

            handle_status(argparse.Namespace())

        output = capsys.readouterr().out
        assert "my_docs" in output

    def test_shows_chunk_count(self, capsys):
        mock_store = MagicMock()
        mock_store.count.return_value = 150

        with (
            patch("markdown_rag.cli.status_cmd.get_settings") as mock_settings,
            patch("markdown_rag.cli.status_cmd.ChromaStore", return_value=mock_store),
        ):
            mock_settings.return_value.collection_name = "test"
            mock_settings.return_value.chroma_path = Path("/tmp")
            mock_settings.return_value.embedding_backend = "local"

            handle_status(argparse.Namespace())

        output = capsys.readouterr().out
        assert "150" in output

    def test_shows_chroma_path(self, capsys):
        mock_store = MagicMock()
        mock_store.count.return_value = 0

        with (
            patch("markdown_rag.cli.status_cmd.get_settings") as mock_settings,
            patch("markdown_rag.cli.status_cmd.ChromaStore", return_value=mock_store),
        ):
            mock_settings.return_value.collection_name = "test"
            mock_settings.return_value.chroma_path = Path("/custom/chroma/path")
            mock_settings.return_value.embedding_backend = "openai"

            handle_status(argparse.Namespace())

        output = capsys.readouterr().out
        assert "/custom/chroma/path" in output

    def test_shows_embedding_backend(self, capsys):
        mock_store = MagicMock()
        mock_store.count.return_value = 0

        with (
            patch("markdown_rag.cli.status_cmd.get_settings") as mock_settings,
            patch("markdown_rag.cli.status_cmd.ChromaStore", return_value=mock_store),
        ):
            mock_settings.return_value.collection_name = "test"
            mock_settings.return_value.chroma_path = Path("/tmp")
            mock_settings.return_value.embedding_backend = "openai"

            handle_status(argparse.Namespace())

        output = capsys.readouterr().out
        assert "openai" in output

    def test_creates_store_with_settings(self):
        mock_store = MagicMock()
        mock_store.count.return_value = 0

        with (
            patch("markdown_rag.cli.status_cmd.get_settings") as mock_settings,
            patch("markdown_rag.cli.status_cmd.ChromaStore", return_value=mock_store) as mock_cls,
        ):
            mock_settings.return_value.collection_name = "docs"
            mock_settings.return_value.chroma_path = Path("/data/chroma")
            mock_settings.return_value.embedding_backend = "local"

            handle_status(argparse.Namespace())

        mock_cls.assert_called_once_with(
            persist_path=Path("/data/chroma"),
            collection_name="docs",
        )
