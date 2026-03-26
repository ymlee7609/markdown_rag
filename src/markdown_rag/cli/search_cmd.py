"""Search subcommand for the mdrag CLI.

Performs semantic search across indexed Markdown documents.
"""

from __future__ import annotations

import argparse

from markdown_rag.config import get_settings
from markdown_rag.embedding.local import LocalEmbedding
from markdown_rag.embedding.openai import OpenAIEmbedding
from markdown_rag.retriever.search import SemanticSearch
from markdown_rag.store.chroma import ChromaStore


def _build_where_filter(args: argparse.Namespace) -> dict | None:
    """CLI 인자에서 메타데이터 필터를 구성한다."""
    conditions = []
    if getattr(args, "doc_type", None):
        conditions.append({"doc_type": args.doc_type})
    if getattr(args, "language", None):
        conditions.append({"language": args.language})
    if getattr(args, "vendor", None):
        conditions.append({"vendor": args.vendor})
    if getattr(args, "category", None):
        conditions.append({"category": args.category})

    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def handle_search(args: argparse.Namespace) -> None:
    """Execute the search subcommand.

    Creates a SemanticSearch engine with the specified backend
    and performs a similarity search. Prints ranked results.

    Args:
        args: Parsed arguments with query, top_k, backend, doc_type, language.
    """
    settings = get_settings()

    # Initialize embedding backend
    if args.backend == "openai":
        embedding = OpenAIEmbedding(model_name=settings.openai_embedding_model)
    else:
        embedding = LocalEmbedding(model_name=settings.local_model)

    # Initialize vector store
    store = ChromaStore(
        persist_path=settings.chroma_path,
        collection_name=settings.collection_name,
    )

    # Create search engine and execute query
    search_engine = SemanticSearch(
        embedding_backend=embedding,
        vector_store=store,
    )
    where = _build_where_filter(args)
    results = search_engine.search(args.query, top_k=args.top_k, where=where)

    if not results:
        print("No results found.")
        return

    print(f"Found {len(results)} result(s):\n")

    for result in results:
        chunk = result.chunk
        header_ctx = chunk.header_context
        source = str(chunk.doc_path)

        # Truncate content to first 200 characters
        content_preview = chunk.content[:200]
        if len(chunk.content) > 200:
            content_preview += "..."

        print(f"[{result.rank}] Score: {result.score:.4f}")
        print(f"    Source: {source}")
        if header_ctx:
            print(f"    Section: {header_ctx}")
        print(f"    {content_preview}")
        print()
