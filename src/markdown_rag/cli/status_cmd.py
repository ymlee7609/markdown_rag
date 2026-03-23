"""Status subcommand for the mdrag CLI.

Shows current index status and configuration.
"""

from __future__ import annotations

import argparse

from markdown_rag.config import get_settings
from markdown_rag.store.chroma import ChromaStore


def handle_status(args: argparse.Namespace) -> None:
    """Execute the status subcommand.

    Shows the current state of the vector store and configuration.

    Args:
        args: Parsed arguments (no additional options needed).
    """
    settings = get_settings()

    store = ChromaStore(
        persist_path=settings.chroma_path,
        collection_name=settings.collection_name,
    )

    total_chunks = store.count()

    print("Markdown RAG Status")
    print("=" * 40)
    print(f"Collection:       {settings.collection_name}")
    print(f"Total chunks:     {total_chunks}")
    print(f"Chroma path:      {settings.chroma_path}")
    print(f"Embedding backend: {settings.embedding_backend}")
