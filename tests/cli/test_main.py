"""Tests for CLI main entry point and argument parsing."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from markdown_rag.cli.main import build_parser, main


class TestBuildParser:
    """Test argparse configuration."""

    def test_parser_has_description(self) -> None:
        parser = build_parser()
        assert parser.description is not None

    def test_parser_ingest_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest", "/some/path"])
        assert args.command == "ingest"
        assert args.path == "/some/path"

    def test_parser_ingest_verbose(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest", "/some/path", "--verbose"])
        assert args.verbose is True

    def test_parser_ingest_verbose_short(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest", "/some/path", "-v"])
        assert args.verbose is True

    def test_parser_search_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["search", "test query"])
        assert args.command == "search"
        assert args.query == "test query"

    def test_parser_search_top_k(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["search", "query", "--top-k", "10"])
        assert args.top_k == 10

    def test_parser_search_top_k_short(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["search", "query", "-k", "3"])
        assert args.top_k == 3

    def test_parser_search_backend(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["search", "query", "--backend", "openai"])
        assert args.backend == "openai"

    def test_parser_search_backend_default(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["search", "query"])
        assert args.backend == "local"

    def test_parser_ask_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ask", "what is this?"])
        assert args.command == "ask"
        assert args.question == "what is this?"

    def test_parser_ask_top_k(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ask", "question", "-k", "7"])
        assert args.top_k == 7

    def test_parser_ask_show_sources(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ask", "question", "--show-sources"])
        assert args.show_sources is True

    def test_parser_ask_show_sources_short(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ask", "question", "-s"])
        assert args.show_sources is True

    def test_parser_ask_model(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ask", "question", "--model", "gpt-4o"])
        assert args.model == "gpt-4o"

    def test_parser_status_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["status"])
        assert args.command == "status"

    def test_parser_serve_subcommand(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["serve"])
        assert args.command == "serve"

    def test_parser_serve_host(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["serve", "--host", "127.0.0.1"])
        assert args.host == "127.0.0.1"

    def test_parser_serve_port(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["serve", "--port", "9000"])
        assert args.port == 9000

    def test_parser_serve_defaults(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["serve"])
        assert args.host == "0.0.0.0"
        assert args.port == 8900


class TestMainDispatch:
    """Test that main() dispatches to the correct subcommand handler."""

    @patch("markdown_rag.cli.main.handle_ingest")
    def test_main_dispatches_ingest(self, mock_handle: MagicMock) -> None:
        with patch("sys.argv", ["mdrag", "ingest", "/tmp/docs"]):
            main()
        mock_handle.assert_called_once()
        args = mock_handle.call_args[0][0]
        assert args.command == "ingest"
        assert args.path == "/tmp/docs"

    @patch("markdown_rag.cli.main.handle_search")
    def test_main_dispatches_search(self, mock_handle: MagicMock) -> None:
        with patch("sys.argv", ["mdrag", "search", "my query"]):
            main()
        mock_handle.assert_called_once()
        args = mock_handle.call_args[0][0]
        assert args.command == "search"

    @patch("markdown_rag.cli.main.handle_ask")
    def test_main_dispatches_ask(self, mock_handle: MagicMock) -> None:
        with patch("sys.argv", ["mdrag", "ask", "what?"]):
            main()
        mock_handle.assert_called_once()
        args = mock_handle.call_args[0][0]
        assert args.command == "ask"

    @patch("markdown_rag.cli.main.handle_status")
    def test_main_dispatches_status(self, mock_handle: MagicMock) -> None:
        with patch("sys.argv", ["mdrag", "status"]):
            main()
        mock_handle.assert_called_once()

    @patch("markdown_rag.cli.main.handle_serve")
    def test_main_dispatches_serve(self, mock_handle: MagicMock) -> None:
        with patch("sys.argv", ["mdrag", "serve"]):
            main()
        mock_handle.assert_called_once()

    def test_main_no_args_prints_help(self, capsys: pytest.CaptureFixture[str]) -> None:
        with patch("sys.argv", ["mdrag"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code in (0, 2)
