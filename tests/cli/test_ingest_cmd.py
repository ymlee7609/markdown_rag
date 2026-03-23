"""Tests for the ingest CLI subcommand."""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_rag.cli.ingest_cmd import handle_ingest
from markdown_rag.ingest.pipeline import IngestResult


@pytest.fixture
def ingest_args(tmp_path: Path) -> argparse.Namespace:
    """Create a basic ingest args namespace."""
    return argparse.Namespace(
        command="ingest",
        path=str(tmp_path),
        verbose=False,
    )


@pytest.fixture
def ingest_args_verbose(tmp_path: Path) -> argparse.Namespace:
    """Create a verbose ingest args namespace."""
    return argparse.Namespace(
        command="ingest",
        path=str(tmp_path),
        verbose=True,
    )


class TestHandleIngest:
    """Test the ingest subcommand handler."""

    @patch("markdown_rag.cli.ingest_cmd.IngestPipeline")
    @patch("markdown_rag.cli.ingest_cmd.get_settings")
    def test_successful_ingest(
        self,
        mock_get_settings: MagicMock,
        mock_pipeline_class: MagicMock,
        ingest_args: argparse.Namespace,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.ingest.return_value = IngestResult(
            documents_processed=3,
            chunks_created=15,
            errors=[],
        )
        mock_pipeline_class.return_value = mock_pipeline

        handle_ingest(ingest_args)

        captured = capsys.readouterr()
        assert "3" in captured.out
        assert "15" in captured.out

    @patch("markdown_rag.cli.ingest_cmd.IngestPipeline")
    @patch("markdown_rag.cli.ingest_cmd.get_settings")
    def test_ingest_with_errors(
        self,
        mock_get_settings: MagicMock,
        mock_pipeline_class: MagicMock,
        ingest_args: argparse.Namespace,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.ingest.return_value = IngestResult(
            documents_processed=2,
            chunks_created=8,
            errors=["Error processing bad.md: parse error"],
        )
        mock_pipeline_class.return_value = mock_pipeline

        handle_ingest(ingest_args)

        captured = capsys.readouterr()
        assert "Error" in captured.out or "error" in captured.out.lower()
        assert "bad.md" in captured.out

    @patch("markdown_rag.cli.ingest_cmd.IngestPipeline")
    @patch("markdown_rag.cli.ingest_cmd.get_settings")
    def test_ingest_verbose_mode(
        self,
        mock_get_settings: MagicMock,
        mock_pipeline_class: MagicMock,
        ingest_args_verbose: argparse.Namespace,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.ingest.return_value = IngestResult(
            documents_processed=1,
            chunks_created=5,
            errors=[],
        )
        mock_pipeline_class.return_value = mock_pipeline

        handle_ingest(ingest_args_verbose)

        # Verbose flag should be passed to pipeline.ingest
        mock_pipeline.ingest.assert_called_once()
        call_kwargs = mock_pipeline.ingest.call_args
        # Verbose should be passed as keyword arg or positional
        assert call_kwargs[1].get("verbose") is True or (
            len(call_kwargs[0]) > 1 and call_kwargs[0][1] is True
        )

    @patch("markdown_rag.cli.ingest_cmd.IngestPipeline")
    @patch("markdown_rag.cli.ingest_cmd.get_settings")
    def test_ingest_path_not_found(
        self,
        mock_get_settings: MagicMock,
        mock_pipeline_class: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.ingest.side_effect = FileNotFoundError(
            "Path '/nonexistent' does not exist"
        )
        mock_pipeline_class.return_value = mock_pipeline

        args = argparse.Namespace(
            command="ingest",
            path="/nonexistent",
            verbose=False,
        )

        with pytest.raises(SystemExit) as exc_info:
            handle_ingest(args)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "not" in captured.err.lower() or "error" in captured.err.lower()

    @patch("markdown_rag.cli.ingest_cmd.IngestPipeline")
    @patch("markdown_rag.cli.ingest_cmd.get_settings")
    def test_ingest_creates_pipeline_with_settings(
        self,
        mock_get_settings: MagicMock,
        mock_pipeline_class: MagicMock,
        ingest_args: argparse.Namespace,
    ) -> None:
        mock_settings = MagicMock()
        mock_get_settings.return_value = mock_settings
        mock_pipeline = MagicMock()
        mock_pipeline.ingest.return_value = IngestResult(
            documents_processed=0, chunks_created=0, errors=[]
        )
        mock_pipeline_class.return_value = mock_pipeline

        handle_ingest(ingest_args)

        mock_get_settings.assert_called_once()
        mock_pipeline_class.assert_called_once_with(settings=mock_settings)

    @patch("markdown_rag.cli.ingest_cmd.IngestPipeline")
    @patch("markdown_rag.cli.ingest_cmd.get_settings")
    def test_ingest_passes_path_object(
        self,
        mock_get_settings: MagicMock,
        mock_pipeline_class: MagicMock,
        ingest_args: argparse.Namespace,
    ) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.ingest.return_value = IngestResult(
            documents_processed=0, chunks_created=0, errors=[]
        )
        mock_pipeline_class.return_value = mock_pipeline

        handle_ingest(ingest_args)

        call_args = mock_pipeline.ingest.call_args
        path_arg = call_args[0][0] if call_args[0] else call_args[1].get("path")
        assert isinstance(path_arg, Path)
