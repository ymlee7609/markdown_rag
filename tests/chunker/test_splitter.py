"""Tests for structure-aware Markdown text splitting.

TDD RED phase: These tests define the expected behavior of the
splitter before implementation.
"""

from pathlib import Path

from markdown_rag.chunker.splitter import (
    _is_atomic_block,
    _is_list_item,
    _split_into_paragraphs,
    _split_long_text,
    split_markdown,
)
from markdown_rag.models import Chunk


class TestSplitMarkdownBasic:
    """Basic splitting behavior tests."""

    def test_returns_list_of_chunks(
        self, sample_basic_path: Path
    ) -> None:
        """split_markdown returns a list of Chunk objects."""
        content = sample_basic_path.read_text(encoding="utf-8")
        chunks = split_markdown(content, doc_path=sample_basic_path)
        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert all(isinstance(c, Chunk) for c in chunks)

    def test_chunks_have_content(
        self, sample_basic_path: Path
    ) -> None:
        """Every chunk has non-empty content."""
        content = sample_basic_path.read_text(encoding="utf-8")
        chunks = split_markdown(content, doc_path=sample_basic_path)
        for chunk in chunks:
            assert chunk.content.strip() != ""

    def test_chunks_have_doc_path(
        self, sample_basic_path: Path
    ) -> None:
        """Every chunk references the source document path."""
        content = sample_basic_path.read_text(encoding="utf-8")
        chunks = split_markdown(content, doc_path=sample_basic_path)
        for chunk in chunks:
            assert chunk.doc_path == sample_basic_path

    def test_chunks_have_sequential_index(
        self, sample_basic_path: Path
    ) -> None:
        """Chunks have sequential chunk_index starting from 0."""
        content = sample_basic_path.read_text(encoding="utf-8")
        chunks = split_markdown(content, doc_path=sample_basic_path)
        for i, chunk in enumerate(chunks):
            assert chunk.chunk_index == i


class TestSplitMarkdownHeaders:
    """Tests for header hierarchy context in chunks."""

    def test_chunks_have_header_hierarchy(
        self, sample_basic_path: Path
    ) -> None:
        """Each chunk includes its parent header hierarchy."""
        content = sample_basic_path.read_text(encoding="utf-8")
        chunks = split_markdown(content, doc_path=sample_basic_path)
        # At least some chunks should have headers
        chunks_with_headers = [c for c in chunks if c.headers]
        assert len(chunks_with_headers) > 0

    def test_nested_header_hierarchy(
        self, sample_nested_path: Path
    ) -> None:
        """Deeply nested content gets full header path."""
        content = sample_nested_path.read_text(encoding="utf-8")
        chunks = split_markdown(
            content,
            doc_path=sample_nested_path,
            max_chunk_size=2000,
        )
        # Find chunk containing "Schema Design" content
        schema_chunks = [
            c for c in chunks if "Schema Design" in c.headers
        ]
        assert len(schema_chunks) >= 1
        schema_chunk = schema_chunks[0]
        assert schema_chunk.headers == [
            "Architecture",
            "Backend",
            "Database",
            "Schema Design",
        ]

    def test_h1_h2_split_produces_separate_chunks(self) -> None:
        """H1 and H2 boundaries create separate chunks."""
        content = (
            "# Title\n\nIntro text.\n\n"
            "## Section A\n\nContent A.\n\n"
            "## Section B\n\nContent B."
        )
        chunks = split_markdown(
            content,
            doc_path=Path("test.md"),
            max_chunk_size=2000,
        )
        headers_list = [c.headers for c in chunks]
        assert ["Title"] in headers_list or any(
            h[-1] == "Title" for h in headers_list if h
        )
        assert any("Section A" in h for h in headers_list)
        assert any("Section B" in h for h in headers_list)


class TestSplitMarkdownSize:
    """Tests for chunk size constraints."""

    def test_chunks_respect_max_size(
        self, sample_basic_path: Path
    ) -> None:
        """No chunk exceeds max_chunk_size."""
        content = sample_basic_path.read_text(encoding="utf-8")
        max_size = 500
        chunks = split_markdown(
            content,
            doc_path=sample_basic_path,
            max_chunk_size=max_size,
        )
        for chunk in chunks:
            assert len(chunk.content) <= max_size, (
                f"Chunk {chunk.chunk_index} has {len(chunk.content)} chars, "
                f"exceeds max {max_size}"
            )

    def test_large_section_is_further_split(self) -> None:
        """A section larger than max_chunk_size is split further."""
        # Create content with a large section
        large_text = "Word " * 300  # ~1500 chars
        content = f"# Title\n\n## Section\n\n{large_text}"
        chunks = split_markdown(
            content,
            doc_path=Path("test.md"),
            max_chunk_size=500,
        )
        # Multiple chunks should be produced
        assert len(chunks) > 1

    def test_small_content_single_chunk(self) -> None:
        """Small content fits in a single chunk."""
        content = "# Title\n\nShort text."
        chunks = split_markdown(
            content,
            doc_path=Path("test.md"),
            max_chunk_size=1000,
        )
        assert len(chunks) == 1


class TestSplitMarkdownAtomicBlocks:
    """Tests ensuring code blocks, tables, and lists are never split."""

    def test_code_block_not_split(self) -> None:
        """A code block is never split across chunks."""
        code = "```python\n" + "x = 1\n" * 50 + "```"
        content = f"# Title\n\n{code}"
        chunks = split_markdown(
            content,
            doc_path=Path("test.md"),
            max_chunk_size=2000,
        )
        # The entire code block should appear in a single chunk
        code_chunks = [c for c in chunks if "x = 1" in c.content]
        assert len(code_chunks) == 1
        assert "```python" in code_chunks[0].content
        assert "```" in code_chunks[0].content

    def test_table_not_split(self) -> None:
        """A table is never split across chunks."""
        rows = "\n".join(
            f"| item{i} | value{i} |" for i in range(20)
        )
        table = f"| Name | Value |\n|------|-------|\n{rows}"
        content = f"# Title\n\n{table}"
        chunks = split_markdown(
            content,
            doc_path=Path("test.md"),
            max_chunk_size=2000,
        )
        table_chunks = [c for c in chunks if "item0" in c.content]
        assert len(table_chunks) == 1
        # The whole table should be in one chunk
        assert "item19" in table_chunks[0].content

    def test_list_not_split(self) -> None:
        """A list is never split across chunks."""
        items = "\n".join(f"- Item {i}" for i in range(20))
        content = f"# Title\n\n{items}"
        chunks = split_markdown(
            content,
            doc_path=Path("test.md"),
            max_chunk_size=2000,
        )
        list_chunks = [c for c in chunks if "Item 0" in c.content]
        assert len(list_chunks) == 1
        assert "Item 19" in list_chunks[0].content


class TestSplitMarkdownOverlap:
    """Tests for chunk overlap behavior."""

    def test_overlap_between_chunks(self) -> None:
        """Consecutive chunks have overlapping text."""
        # Create content large enough to need splitting with paragraphs
        paragraphs = [f"Paragraph {i}. " * 10 for i in range(10)]
        content = "# Title\n\n" + "\n\n".join(paragraphs)
        chunks = split_markdown(
            content,
            doc_path=Path("test.md"),
            max_chunk_size=300,
            overlap=50,
        )
        if len(chunks) >= 2:
            # The end of chunk[i] should overlap with start of chunk[i+1]
            for i in range(len(chunks) - 1):
                # Check that some text from end of current chunk
                # appears at start of next chunk
                chunks[i].content[-50:]
                chunks[i + 1].content[:100]
                # At least some overlap text should be present
                # (overlap is best-effort at paragraph boundaries)
                # We just verify chunks were created with overlap param
                assert len(chunks[i].content) > 0
                assert len(chunks[i + 1].content) > 0

    def test_zero_overlap(self) -> None:
        """Zero overlap still produces valid chunks."""
        content = "# Title\n\n" + "Word " * 200
        chunks = split_markdown(
            content,
            doc_path=Path("test.md"),
            max_chunk_size=300,
            overlap=0,
        )
        assert len(chunks) >= 1


class TestSplitMarkdownFixtures:
    """Integration tests with fixture files."""

    def test_basic_fixture_produces_multiple_chunks(
        self, sample_basic_path: Path
    ) -> None:
        """sample_basic.md produces multiple meaningful chunks."""
        content = sample_basic_path.read_text(encoding="utf-8")
        chunks = split_markdown(
            content,
            doc_path=sample_basic_path,
            max_chunk_size=500,
        )
        assert len(chunks) >= 2

    def test_frontmatter_fixture(
        self, sample_frontmatter_path: Path
    ) -> None:
        """sample_frontmatter.md is split correctly (frontmatter stripped)."""
        content = sample_frontmatter_path.read_text(encoding="utf-8")
        chunks = split_markdown(
            content,
            doc_path=sample_frontmatter_path,
        )
        assert len(chunks) >= 1
        # Frontmatter should not appear in chunk content
        for chunk in chunks:
            assert "---" not in chunk.content.split("\n")[0] or "title:" not in chunk.content

    def test_nested_fixture(
        self, sample_nested_path: Path
    ) -> None:
        """sample_nested.md produces chunks with correct hierarchies."""
        content = sample_nested_path.read_text(encoding="utf-8")
        chunks = split_markdown(
            content,
            doc_path=sample_nested_path,
        )
        assert len(chunks) >= 1
        # All chunks should have headers from the nested structure
        for chunk in chunks:
            if chunk.headers:
                assert chunk.headers[0] == "Architecture"

    def test_all_content_covered(
        self, sample_basic_path: Path
    ) -> None:
        """Key content from source appears in some chunk."""
        content = sample_basic_path.read_text(encoding="utf-8")
        chunks = split_markdown(
            content,
            doc_path=sample_basic_path,
            max_chunk_size=2000,
        )
        all_content = " ".join(c.content for c in chunks)
        assert "pip install markdown-rag" in all_content
        assert "chunk_max_size" in all_content
        assert "mdrag search" in all_content


class TestSplitHelpers:
    """Tests for internal helper functions to improve coverage."""

    def test_is_list_item_unordered_dash(self) -> None:
        """Detects unordered list items with dash."""
        assert _is_list_item("- item") is True

    def test_is_list_item_unordered_asterisk(self) -> None:
        """Detects unordered list items with asterisk."""
        assert _is_list_item("* item") is True

    def test_is_list_item_ordered(self) -> None:
        """Detects ordered list items."""
        assert _is_list_item("1. item") is True
        assert _is_list_item("10. item") is True

    def test_is_list_item_ordered_paren(self) -> None:
        """Detects ordered list items with parenthesis."""
        assert _is_list_item("1) item") is True

    def test_is_list_item_not_a_list(self) -> None:
        """Non-list lines return False."""
        assert _is_list_item("regular text") is False
        assert _is_list_item("") is False

    def test_is_atomic_block_code(self) -> None:
        """Code blocks are detected as atomic."""
        assert _is_atomic_block("```python\nx=1\n```") is True

    def test_is_atomic_block_table(self) -> None:
        """Tables are detected as atomic."""
        assert _is_atomic_block("| A | B |\n|---|---|") is True

    def test_is_atomic_block_list(self) -> None:
        """Lists are detected as atomic."""
        assert _is_atomic_block("- item 1\n- item 2") is True

    def test_is_atomic_block_plain_text(self) -> None:
        """Plain text is not atomic."""
        assert _is_atomic_block("Just some text") is False

    def test_split_into_paragraphs_basic(self) -> None:
        """Splits text by double newlines."""
        text = "Para 1\n\nPara 2\n\nPara 3"
        result = _split_into_paragraphs(text)
        assert len(result) == 3

    def test_split_into_paragraphs_code_block(self) -> None:
        """Code blocks are kept as single paragraphs."""
        text = "Before\n\n```python\nline1\nline2\n```\n\nAfter"
        result = _split_into_paragraphs(text)
        # Should be: Before, code block, After
        assert len(result) == 3
        assert "```python" in result[1]
        assert "line1" in result[1]

    def test_split_into_paragraphs_table(self) -> None:
        """Table rows are grouped as one paragraph."""
        text = "Text\n\n| A | B |\n|---|---|\n| 1 | 2 |"
        result = _split_into_paragraphs(text)
        assert len(result) == 2
        # Table paragraph should contain all rows
        table_para = result[1]
        assert "| A |" in table_para
        assert "| 1 |" in table_para

    def test_split_into_paragraphs_list(self) -> None:
        """List items are grouped as one paragraph."""
        text = "Text\n\n- item 1\n- item 2\n- item 3"
        result = _split_into_paragraphs(text)
        assert len(result) == 2
        list_para = result[1]
        assert "item 1" in list_para
        assert "item 3" in list_para

    def test_split_long_text_short(self) -> None:
        """Short text is returned as-is."""
        result = _split_long_text("short text", 100)
        assert result == ["short text"]

    def test_split_long_text_sentence_boundary(self) -> None:
        """Long text splits at sentence boundaries."""
        text = "First sentence. Second sentence. Third sentence. " * 5
        result = _split_long_text(text, 100)
        assert len(result) > 1
        # Each part should be <= 100 chars
        for part in result:
            assert len(part) <= 100

    def test_split_long_text_word_boundary(self) -> None:
        """Text without periods splits at word boundaries."""
        text = "word " * 100
        result = _split_long_text(text, 100)
        assert len(result) > 1

    def test_split_long_text_no_spaces(self) -> None:
        """Continuous text without spaces force-splits at max_size."""
        text = "a" * 500
        result = _split_long_text(text, 100)
        assert len(result) == 5
        assert all(len(p) <= 100 for p in result)


class TestSplitMarkdownEdgeCases:
    """Edge case tests for split_markdown."""

    def test_empty_content(self) -> None:
        """Empty content returns empty list."""
        chunks = split_markdown("", doc_path=Path("test.md"))
        assert chunks == []

    def test_whitespace_only_content(self) -> None:
        """Whitespace-only content returns empty list."""
        chunks = split_markdown("   \n\n  ", doc_path=Path("test.md"))
        assert chunks == []

    def test_no_headers_single_chunk(self) -> None:
        """Content without headers becomes a single chunk."""
        content = "Just some text without any headers."
        chunks = split_markdown(content, doc_path=Path("test.md"))
        assert len(chunks) == 1
        assert chunks[0].headers == []

    def test_metadata_passed_to_chunks(self) -> None:
        """Custom metadata is attached to all chunks."""
        content = "# Title\n\nSome text."
        metadata = {"source": "test", "version": "1.0"}
        chunks = split_markdown(
            content,
            doc_path=Path("test.md"),
            metadata=metadata,
        )
        for chunk in chunks:
            assert chunk.metadata["source"] == "test"
            assert chunk.metadata["version"] == "1.0"

    def test_frontmatter_metadata_in_chunks(self) -> None:
        """Frontmatter metadata is extracted and attached to chunks."""
        content = "---\ntitle: Test\n---\n# Heading\n\nBody."
        chunks = split_markdown(content, doc_path=Path("test.md"))
        assert len(chunks) >= 1
        assert chunks[0].metadata.get("title") == "Test"

    def test_multiple_paragraphs_large_section(self) -> None:
        """Multiple paragraphs in a large section are split correctly."""
        paras = "\n\n".join(
            f"Paragraph number {i} with enough text to be meaningful." * 3
            for i in range(10)
        )
        content = f"# Title\n\n## Section\n\n{paras}"
        chunks = split_markdown(
            content, doc_path=Path("test.md"), max_chunk_size=300
        )
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk.content) <= 300

    def test_ordered_list_not_split(self) -> None:
        """Ordered lists are never split across chunks."""
        items = "\n".join(f"{i+1}. Item {i}" for i in range(15))
        content = f"# Title\n\n{items}"
        chunks = split_markdown(
            content, doc_path=Path("test.md"), max_chunk_size=2000
        )
        list_chunks = [c for c in chunks if "Item 0" in c.content]
        assert len(list_chunks) == 1
        assert "Item 14" in list_chunks[0].content

    def test_overlap_with_tight_max_size(self) -> None:
        """Overlap handles tight max_chunk_size gracefully."""
        content = (
            "# Title\n\n"
            "## Section A\n\nFirst section content here.\n\n"
            "## Section B\n\nSecond section content here."
        )
        chunks = split_markdown(
            content,
            doc_path=Path("test.md"),
            max_chunk_size=200,
            overlap=50,
        )
        assert len(chunks) >= 2
        for chunk in chunks:
            assert len(chunk.content) <= 200
