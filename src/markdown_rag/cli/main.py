"""Main CLI entry point for Markdown RAG (mdrag).

Provides subcommands for document ingestion, semantic search,
question answering, status inspection, and API server management.
"""

from __future__ import annotations

import argparse
import sys

from markdown_rag.cli.ask_cmd import handle_ask
from markdown_rag.cli.ingest_cmd import handle_ingest
from markdown_rag.cli.search_cmd import handle_search
from markdown_rag.cli.status_cmd import handle_status


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with all subcommands.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="mdrag",
        description="Markdown RAG - Semantic search and QA for Markdown documents",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # -- ingest --
    ingest_parser = subparsers.add_parser(
        "ingest", help="Ingest Markdown documents into the vector store"
    )
    ingest_parser.add_argument("path", help="Path to a .md file or directory to ingest")
    ingest_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show per-file progress"
    )

    # -- search --
    search_parser = subparsers.add_parser(
        "search", help="Semantic search across indexed documents"
    )
    search_parser.add_argument("query", help="Search query string")
    search_parser.add_argument(
        "-k", "--top-k", type=int, default=5, help="Number of results (default: 5)"
    )
    search_parser.add_argument(
        "--backend",
        choices=["local", "openai"],
        default="local",
        help="Embedding backend (default: local)",
    )
    search_parser.add_argument(
        "--doc-type",
        choices=["rfc", "ccie", "telecom_manual"],
        default=None,
        help="Filter by document type",
    )
    search_parser.add_argument(
        "--language",
        choices=["en", "ko"],
        default=None,
        help="Filter by language",
    )

    # -- ask --
    ask_parser = subparsers.add_parser(
        "ask", help="Ask a question using RAG (OpenAI or local SLM)"
    )
    ask_parser.add_argument("question", help="Question to ask")
    ask_parser.add_argument(
        "-k", "--top-k", type=int, default=5, help="Number of context chunks (default: 5)"
    )
    ask_parser.add_argument(
        "-s", "--show-sources", action="store_true", help="Show source documents"
    )
    ask_parser.add_argument(
        "--model", default=None, help="Model name or path override"
    )
    ask_parser.add_argument(
        "--llm-backend",
        choices=["local", "openai"],
        default=None,
        help="LLM backend (default: from settings)",
    )
    ask_parser.add_argument(
        "--doc-type",
        choices=["rfc", "ccie", "telecom_manual"],
        default=None,
        help="Filter by document type",
    )
    ask_parser.add_argument(
        "--language",
        choices=["en", "ko"],
        default=None,
        help="Filter by language",
    )

    # -- status --
    subparsers.add_parser("status", help="Show index status and configuration")

    # -- serve --
    serve_parser = subparsers.add_parser("serve", help="Start the REST API server")
    serve_parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind (default: 0.0.0.0)"
    )
    serve_parser.add_argument(
        "--port", type=int, default=8900, help="Port to bind (default: 8900)"
    )

    return parser


def handle_serve(args: argparse.Namespace) -> None:
    """Start the FastAPI server with uvicorn.

    Args:
        args: Parsed arguments with host and port.
    """
    try:
        import uvicorn
    except ImportError:
        print("Error: uvicorn is required. Install with: pip install uvicorn", file=sys.stderr)
        sys.exit(1)

    print(f"Starting mdrag API server on {args.host}:{args.port}")
    uvicorn.run(
        "markdown_rag.api.app:create_app",
        host=args.host,
        port=args.port,
        factory=True,
    )


def main() -> None:
    """CLI entry point registered as 'mdrag' in pyproject.toml."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(2)

    handlers = {
        "ingest": handle_ingest,
        "search": handle_search,
        "ask": handle_ask,
        "status": handle_status,
        "serve": handle_serve,
    }

    handler = handlers.get(args.command)
    if handler is not None:
        handler(args)
    else:
        parser.print_help()
        sys.exit(2)
