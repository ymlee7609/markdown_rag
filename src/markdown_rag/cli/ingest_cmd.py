"""Ingest subcommand for the mdrag CLI.

Handles document ingestion from files or directories into the vector store.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from markdown_rag.config import get_settings
from markdown_rag.ingest.pipeline import IngestPipeline


def handle_ingest(args: argparse.Namespace) -> None:
    """Execute the ingest subcommand.

    Creates an IngestPipeline with default settings and processes
    the specified path. Prints a summary of results.

    Args:
        args: Parsed arguments with path and verbose flag.
    """
    settings = get_settings()
    pipeline = IngestPipeline(settings=settings)

    target_path = Path(args.path)

    try:
        result = pipeline.ingest(target_path, verbose=args.verbose)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Documents processed: {result.documents_processed}")
    print(f"Chunks created:      {result.chunks_created}")

    if result.errors:
        print(f"Errors:              {len(result.errors)}")
        for error in result.errors:
            print(f"  - {error}")
    else:
        print("Errors:              0")
