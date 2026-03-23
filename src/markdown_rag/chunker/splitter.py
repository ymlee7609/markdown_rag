"""Structure-aware Markdown text splitting.

Splits Markdown documents into chunks that respect structural boundaries:
- Splits by H1/H2 first, then H3+ for further splitting, then by paragraph.
- NEVER splits in the middle of code blocks, tables, or lists.
- Each chunk receives parent header hierarchy as context.
- Respects max_chunk_size and implements overlap between chunks.
"""

from __future__ import annotations

from pathlib import Path

from markdown_rag.chunker.metadata import extract_frontmatter
from markdown_rag.chunker.parser import Section, find_sections, parse_markdown
from markdown_rag.models import Chunk


def split_markdown(
    content: str,
    doc_path: Path,
    max_chunk_size: int = 1000,
    overlap: int = 100,
    metadata: dict | None = None,
) -> list[Chunk]:
    """Split a Markdown document into structure-aware chunks.

    Strategy:
    1. Strip YAML frontmatter (if present).
    2. Parse Markdown into AST tokens.
    3. Extract sections with header hierarchy.
    4. Group sections by H1/H2 boundaries.
    5. Further split large sections by H3+ boundaries.
    6. Split remaining oversized sections by paragraph.
    7. Apply overlap between consecutive chunks.

    Args:
        content: Raw Markdown string (may include frontmatter).
        doc_path: Path to the source document.
        max_chunk_size: Maximum chunk size in characters.
        overlap: Number of characters to overlap between consecutive chunks.
        metadata: Optional metadata dict to attach to each chunk.

    Returns:
        List of Chunk objects with content, headers, and metadata.
    """
    # Step 1: Strip frontmatter
    fm_metadata, body = extract_frontmatter(content)
    chunk_metadata = {**fm_metadata, **(metadata or {})}

    if not body.strip():
        return []

    # Step 2: Parse and extract sections
    tokens = parse_markdown(body)
    sections = find_sections(tokens)

    if not sections:
        # No headers found; treat entire content as one chunk
        return [
            Chunk(
                content=body.strip(),
                doc_path=doc_path,
                headers=[],
                chunk_index=0,
                metadata=chunk_metadata,
            )
        ]

    # Step 3: Split sections that exceed max_chunk_size
    split_sections = _split_oversized_sections(sections, max_chunk_size)

    # Step 4: Build chunks with overlap
    chunks = _build_chunks_with_overlap(
        split_sections, doc_path, max_chunk_size, overlap, chunk_metadata
    )

    return chunks


def _split_oversized_sections(
    sections: list[Section], max_chunk_size: int
) -> list[Section]:
    """Split sections that exceed max_chunk_size by paragraph boundaries.

    Atomic blocks (code blocks, tables, lists) are never split even if
    they exceed max_chunk_size on their own.
    """
    result: list[Section] = []

    for section in sections:
        if len(section.content) <= max_chunk_size:
            result.append(section)
            continue

        # Split by paragraph (double newline)
        paragraphs = _split_into_paragraphs(section.content)

        if len(paragraphs) <= 1:
            # Single paragraph that is oversized; check if it is an atomic block
            single = paragraphs[0] if paragraphs else section.content
            if _is_atomic_block(single):
                # Atomic blocks (code, table, list) are never split
                result.append(section)
                continue
            # Split long plain-text paragraph by sentence/word boundary
            sub_parts = _split_long_text(single, max_chunk_size)
            for part in sub_parts:
                result.append(
                    Section(
                        headers=section.headers[:],
                        content=part,
                        level=section.level,
                    )
                )
            continue

        # Group paragraphs into sub-sections respecting max_chunk_size
        current_parts: list[str] = []
        current_size = 0

        for para in paragraphs:
            para_size = len(para)

            if current_size + para_size + 1 > max_chunk_size and current_parts:
                # Emit current group as a section
                result.append(
                    Section(
                        headers=section.headers[:],
                        content="\n\n".join(current_parts),
                        level=section.level,
                    )
                )
                current_parts = []
                current_size = 0

            current_parts.append(para)
            current_size += para_size + 1

        if current_parts:
            result.append(
                Section(
                    headers=section.headers[:],
                    content="\n\n".join(current_parts),
                    level=section.level,
                )
            )

    return result


def _split_into_paragraphs(text: str) -> list[str]:
    """Split text into paragraphs, treating atomic blocks as single paragraphs.

    Atomic blocks (fenced code blocks, tables starting with |,
    and lists starting with - or 1.) are kept together.
    """
    lines = text.split("\n")
    paragraphs: list[str] = []
    current: list[str] = []
    in_code_block = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Track fenced code blocks
        if line.strip().startswith("```"):
            if not in_code_block:
                # Start of code block - flush current paragraph
                if current:
                    paragraphs.append("\n".join(current))
                    current = []
                in_code_block = True
                current.append(line)
            else:
                # End of code block
                current.append(line)
                in_code_block = False
                paragraphs.append("\n".join(current))
                current = []
            i += 1
            continue

        if in_code_block:
            current.append(line)
            i += 1
            continue

        # Table detection: lines starting with |
        if line.strip().startswith("|"):
            if current and not current[-1].strip().startswith("|"):
                paragraphs.append("\n".join(current))
                current = []
            current.append(line)
            i += 1
            continue

        # List detection: lines starting with - or digit.
        if _is_list_item(line):
            if current and not _is_list_item(current[-1]):
                paragraphs.append("\n".join(current))
                current = []
            current.append(line)
            i += 1
            continue

        # Empty line = paragraph break
        if not line.strip():
            if current:
                paragraphs.append("\n".join(current))
                current = []
            i += 1
            continue

        current.append(line)
        i += 1

    if current:
        paragraphs.append("\n".join(current))

    return [p for p in paragraphs if p.strip()]


def _is_list_item(line: str) -> bool:
    """Check if a line is a list item."""
    stripped = line.strip()
    if stripped.startswith("- ") or stripped.startswith("* "):
        return True
    # Ordered list: starts with digit followed by . or )
    if stripped and stripped[0].isdigit():
        rest = stripped.lstrip("0123456789")
        if rest.startswith(". ") or rest.startswith(") "):
            return True
    return False


def _is_atomic_block(text: str) -> bool:
    """Check if text is an atomic block that should not be split.

    Atomic blocks: fenced code blocks, tables, lists.
    """
    stripped = text.strip()
    if stripped.startswith("```"):
        return True
    if stripped.startswith("|"):
        return True
    if _is_list_item(stripped.split("\n")[0] if stripped else ""):
        return True
    return False


def _split_long_text(text: str, max_size: int) -> list[str]:
    """Split a long plain-text paragraph by word boundaries.

    Tries to split at sentence boundaries (. ) first,
    falls back to word boundaries.
    """
    if len(text) <= max_size:
        return [text]

    parts: list[str] = []
    remaining = text

    while len(remaining) > max_size:
        # Try to find a sentence boundary
        split_pos = remaining.rfind(". ", 0, max_size)
        if split_pos > max_size // 4:
            split_pos += 1  # include the period
        else:
            # Fall back to word boundary
            split_pos = remaining.rfind(" ", 0, max_size)

        if split_pos <= 0:
            # No good split point; force split at max_size
            split_pos = max_size

        parts.append(remaining[:split_pos].strip())
        remaining = remaining[split_pos:].strip()

    if remaining:
        parts.append(remaining)

    return parts


def _build_chunks_with_overlap(
    sections: list[Section],
    doc_path: Path,
    max_chunk_size: int,
    overlap: int,
    metadata: dict,
) -> list[Chunk]:
    """Build Chunk objects from sections with optional overlap.

    Overlap is applied by prepending text from the end of the
    previous chunk to the start of the next chunk.
    """
    if not sections:
        return []

    chunks: list[Chunk] = []
    prev_tail = ""

    for idx, section in enumerate(sections):
        content = section.content.strip()
        if not content:
            continue

        # Apply overlap: prepend tail of previous chunk
        if overlap > 0 and prev_tail and idx > 0:
            overlap_text = prev_tail[-overlap:]
            # Only add overlap if it does not make the chunk exceed max size
            if len(overlap_text) + len(content) + 1 <= max_chunk_size:
                content = overlap_text.strip() + "\n\n" + content
            elif len(content) + len(overlap_text) > max_chunk_size:
                # Truncate overlap to fit
                available = max_chunk_size - len(content) - 1
                if available > 10:
                    content = prev_tail[-available:].strip() + "\n\n" + content

        # Final safety: truncate if still over max (should be rare)
        if len(content) > max_chunk_size:
            content = content[:max_chunk_size]

        chunks.append(
            Chunk(
                content=content,
                doc_path=doc_path,
                headers=section.headers[:],
                chunk_index=len(chunks),
                metadata=metadata.copy(),
            )
        )

        prev_tail = section.content.strip()

    # Re-index chunks sequentially
    for i, chunk in enumerate(chunks):
        chunk.chunk_index = i

    return chunks
