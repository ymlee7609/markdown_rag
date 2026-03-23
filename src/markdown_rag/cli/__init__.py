"""CLI interface for Markdown RAG."""

from markdown_rag.cli.ask_cmd import handle_ask
from markdown_rag.cli.ingest_cmd import handle_ingest
from markdown_rag.cli.main import main
from markdown_rag.cli.search_cmd import handle_search
from markdown_rag.cli.status_cmd import handle_status

__all__ = ["handle_ask", "handle_ingest", "handle_search", "handle_status", "main"]
