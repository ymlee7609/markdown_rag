"""Markdown AST parsing and header hierarchy extraction.

Uses markdown-it-py to parse Markdown into an AST token stream,
then extracts a header hierarchy tree and section boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from markdown_it import MarkdownIt
from markdown_it.token import Token


@dataclass
class HeaderNode:
    """A node in the header hierarchy tree.

    Attributes:
        level: Header level (1 for H1, 2 for H2, etc.)
        text: Header text content.
        children: Child header nodes.
    """

    level: int
    text: str
    children: list[HeaderNode] = field(default_factory=list)


@dataclass
class Section:
    """A section of Markdown content bounded by headers.

    Attributes:
        headers: Full header hierarchy path (e.g. ["Architecture", "Backend", "Auth"]).
        content: The raw Markdown text of this section (excluding the header itself).
        level: The header level that defines this section.
    """

    headers: list[str]
    content: str
    level: int


def parse_markdown(content: str) -> list[Token]:
    """Parse Markdown content into a list of markdown-it-py tokens.

    Args:
        content: Raw Markdown string.

    Returns:
        List of markdown-it Token objects representing the AST.
    """
    md = MarkdownIt("commonmark").enable("table")
    return md.parse(content)


def _get_heading_text(tokens: list[Token], idx: int) -> str:
    """Extract the text content of a heading from the token stream.

    The heading_open token is followed by an inline token that holds
    the heading text, then a heading_close token.
    """
    if idx + 1 < len(tokens) and tokens[idx + 1].type == "inline":
        return tokens[idx + 1].content
    return ""


def extract_header_tree(tokens: list[Token]) -> list[HeaderNode]:
    """Build a header hierarchy tree from markdown-it tokens.

    Args:
        tokens: List of markdown-it Token objects.

    Returns:
        List of root HeaderNode objects (typically H1 headers).
        H2 nodes are children of H1, H3 of H2, etc.
    """
    roots: list[HeaderNode] = []
    # Stack keeps track of (level, node) pairs for nesting
    stack: list[HeaderNode] = []

    for i, token in enumerate(tokens):
        if token.type != "heading_open":
            continue

        level = int(token.tag[1])  # "h1" -> 1, "h2" -> 2, etc.
        text = _get_heading_text(tokens, i)
        node = HeaderNode(level=level, text=text)

        # Pop stack until we find a parent with a smaller level
        while stack and stack[-1].level >= level:
            stack.pop()

        if stack:
            stack[-1].children.append(node)
        else:
            roots.append(node)

        stack.append(node)

    return roots


def _render_tokens_to_text(tokens: list[Token], start: int, end: int) -> str:
    """Render a range of tokens back to approximate Markdown text.

    Reconstructs readable text from the token stream, preserving
    code blocks, tables, and lists as atomic blocks.
    """
    parts: list[str] = []
    i = start
    while i < end:
        token = tokens[i]

        if token.type == "fence":
            # Fenced code block: reconstruct with markers
            info = token.info.strip() if token.info else ""
            parts.append(f"```{info}\n{token.content}```")
        elif token.type == "code_block":
            parts.append(f"```\n{token.content}```")
        elif token.type == "table_open":
            # Collect the entire table as raw text
            table_parts: list[str] = []
            j = i
            while j < end and tokens[j].type != "table_close":
                if tokens[j].type == "inline":
                    table_parts.append(tokens[j].content)
                elif tokens[j].type == "th_open":
                    pass  # handled via inline
                elif tokens[j].type == "tr_open":
                    table_parts.append("|")
                elif tokens[j].type == "tr_close":
                    pass
                elif tokens[j].type == "th_close" or tokens[j].type == "td_close":
                    table_parts.append("|")
                j += 1
            # Reconstruct simple table representation
            parts.append(_reconstruct_table(tokens, i, min(j + 1, end)))
            i = j  # skip to table_close
        elif token.type == "bullet_list_open" or token.type == "ordered_list_open":
            # Collect the entire list as raw text
            close_type = token.type.replace("_open", "_close")
            j = i + 1
            nesting = 1
            while j < end and nesting > 0:
                if tokens[j].type == token.type:
                    nesting += 1
                elif tokens[j].type == close_type:
                    nesting -= 1
                j += 1
            parts.append(_reconstruct_list(tokens, i, j))
            i = j - 1  # will be incremented at end of loop
        elif token.type == "inline":
            parts.append(token.content)
        elif token.type == "paragraph_open":
            pass  # content comes in the inline token
        elif token.type == "paragraph_close":
            parts.append("")  # paragraph separator
        elif token.type in (
            "heading_open",
            "heading_close",
            "bullet_list_close",
            "ordered_list_close",
            "list_item_open",
            "list_item_close",
            "blockquote_open",
            "blockquote_close",
            "hr",
        ):
            pass  # structural tokens handled elsewhere

        i += 1

    return "\n".join(parts).strip()


def _reconstruct_table(tokens: list[Token], start: int, end: int) -> str:
    """Reconstruct a Markdown table from tokens."""
    rows: list[list[str]] = []
    current_row: list[str] = []
    is_header = False
    header_row_count = 0

    for i in range(start, end):
        token = tokens[i]
        if token.type == "tr_open":
            current_row = []
        elif token.type == "tr_close":
            rows.append(current_row)
            if is_header:
                header_row_count += 1
        elif token.type == "thead_open":
            is_header = True
        elif token.type == "thead_close":
            is_header = False
        elif token.type == "inline":
            current_row.append(token.content)

    if not rows:
        return ""

    lines: list[str] = []
    for idx, row in enumerate(rows):
        lines.append("| " + " | ".join(row) + " |")
        if idx == header_row_count - 1 and header_row_count > 0:
            lines.append("| " + " | ".join("---" for _ in row) + " |")

    return "\n".join(lines)


def _reconstruct_list(tokens: list[Token], start: int, end: int) -> str:
    """Reconstruct a Markdown list from tokens."""
    items: list[str] = []
    is_ordered = tokens[start].type == "ordered_list_open"

    for i in range(start, end):
        token = tokens[i]
        if token.type == "inline":
            items.append(token.content)

    lines: list[str] = []
    for idx, item in enumerate(items):
        if is_ordered:
            lines.append(f"{idx + 1}. {item}")
        else:
            lines.append(f"- {item}")

    return "\n".join(lines)


def find_sections(tokens: list[Token]) -> list[Section]:
    """Split token stream into sections, each with header hierarchy context.

    Each section starts at a heading and extends to the next heading
    of equal or higher level (or end of document).

    Args:
        tokens: List of markdown-it Token objects.

    Returns:
        List of Section objects, each with:
        - headers: Full header hierarchy path
        - content: Markdown text of the section body
        - level: Header level of the section
    """
    # First pass: find heading positions and build hierarchy context
    heading_positions: list[tuple[int, int, str]] = []  # (token_idx, level, text)
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            level = int(token.tag[1])
            text = _get_heading_text(tokens, i)
            heading_positions.append((i, level, text))

    if not heading_positions:
        return []

    # Build sections
    sections: list[Section] = []
    # Track header stack for hierarchy context
    header_stack: list[tuple[int, str]] = []  # (level, text)

    for h_idx, (token_idx, level, text) in enumerate(heading_positions):
        # Update header stack
        while header_stack and header_stack[-1][0] >= level:
            header_stack.pop()
        header_stack.append((level, text))

        # Determine content range: from after heading_close to next heading_open
        # heading_open is at token_idx, heading_close is typically token_idx+2
        content_start = token_idx + 3  # skip heading_open, inline, heading_close

        if h_idx + 1 < len(heading_positions):
            content_end = heading_positions[h_idx + 1][0]
        else:
            content_end = len(tokens)

        # Render content tokens to text
        content = _render_tokens_to_text(tokens, content_start, content_end)

        headers = [h_text for _, h_text in header_stack]
        sections.append(Section(headers=headers, content=content, level=level))

    return sections
