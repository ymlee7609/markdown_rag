"""Search subcommand for the mdrag CLI.

Performs semantic / hybrid / ontology-augmented search across indexed
Markdown documents.
"""

from __future__ import annotations

import argparse

from markdown_rag.config import get_settings
from markdown_rag.retriever.builder import build_search_engine


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

    Build the appropriate search engine via the retriever builder factory
    (vector / hybrid / ontology), execute the query, and print ranked results.

    Args:
        args: Parsed arguments with query, top_k, mode, doc_type, language,
              vendor, category.
    """
    settings = get_settings()
    # CLI override: --backend (legacy: only affects embedding backend already
    # set via env). --mode controls search backend.
    if getattr(args, "backend", None):
        settings.embedding_backend = args.backend  # type: ignore[assignment]

    mode_override = getattr(args, "mode", None)
    search_engine = build_search_engine(settings, mode_override=mode_override)
    effective_mode = mode_override or settings.search_mode

    where = _build_where_filter(args)
    results = search_engine.search(args.query, top_k=args.top_k, where=where)

    if not results:
        print("No results found.")
        return

    print(f"Found {len(results)} result(s)  [mode={effective_mode}]:\n")

    for result in results:
        chunk = result.chunk
        header_ctx = chunk.header_context
        source = str(chunk.doc_path)

        # Truncate content preview
        content_preview = chunk.content[:200]
        if len(chunk.content) > 200:
            content_preview += "..."

        # Ontology origin tag (when mode == "ontology")
        meta = chunk.metadata or {}
        origin = ""
        if meta.get("via_onto_card"):
            origin = "  [ONTO CARD]"
        elif meta.get("injected_by_onto_card"):
            origin = f"  [INJECTED via {meta['injected_by_onto_card']}]"

        print(f"[{result.rank}] Score: {result.score:.4f}{origin}")
        print(f"    Source: {source}")
        if header_ctx:
            print(f"    Section: {header_ctx}")
        if meta.get("via_onto_card"):
            refs = meta.get("referenced_paths_injectable", [])
            dirs = meta.get("referenced_paths_directories", [])
            if refs:
                print(f"    Refs: {', '.join(refs[:3])}")
            if dirs:
                print(f"    Manual dirs: {', '.join(dirs[:3])}")
        print(f"    {content_preview}")
        print()
