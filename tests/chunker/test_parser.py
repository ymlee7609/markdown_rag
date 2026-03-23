"""Tests for Markdown AST parsing and header hierarchy extraction.

TDD RED phase: These tests define the expected behavior of the
parser before implementation.
"""

from pathlib import Path

from markdown_rag.chunker.parser import (
    HeaderNode,
    extract_header_tree,
    find_sections,
    parse_markdown,
)


class TestParseMarkdown:
    """Tests for parse_markdown function."""

    def test_returns_list_of_tokens(self) -> None:
        """parse_markdown returns a list of markdown-it tokens."""
        tokens = parse_markdown("# Hello\n\nWorld")
        assert isinstance(tokens, list)
        assert len(tokens) > 0

    def test_identifies_heading(self) -> None:
        """parse_markdown produces heading_open tokens for headers."""
        tokens = parse_markdown("# Hello")
        heading_tokens = [t for t in tokens if t.type == "heading_open"]
        assert len(heading_tokens) == 1
        assert heading_tokens[0].tag == "h1"

    def test_identifies_code_block(self) -> None:
        """parse_markdown identifies fenced code blocks."""
        content = "```python\nprint('hello')\n```"
        tokens = parse_markdown(content)
        fence_tokens = [t for t in tokens if t.type == "fence"]
        assert len(fence_tokens) == 1

    def test_identifies_table(self) -> None:
        """parse_markdown identifies table structures."""
        content = "| A | B |\n|---|---|\n| 1 | 2 |"
        tokens = parse_markdown(content)
        # markdown-it-py uses "table_open" type
        table_tokens = [t for t in tokens if t.type == "table_open"]
        assert len(table_tokens) == 1

    def test_identifies_list(self) -> None:
        """parse_markdown identifies list structures."""
        content = "- item 1\n- item 2\n- item 3"
        tokens = parse_markdown(content)
        list_tokens = [
            t
            for t in tokens
            if t.type in ("bullet_list_open", "ordered_list_open")
        ]
        assert len(list_tokens) == 1

    def test_basic_fixture_parsing(
        self, sample_basic_path: Path
    ) -> None:
        """sample_basic.md parses without errors."""
        content = sample_basic_path.read_text(encoding="utf-8")
        tokens = parse_markdown(content)
        assert len(tokens) > 0


class TestHeaderNode:
    """Tests for HeaderNode dataclass."""

    def test_header_node_creation(self) -> None:
        """HeaderNode can be created with level, text, children."""
        node = HeaderNode(level=1, text="Title", children=[])
        assert node.level == 1
        assert node.text == "Title"
        assert node.children == []

    def test_header_node_with_children(self) -> None:
        """HeaderNode supports nested children."""
        child = HeaderNode(level=2, text="Section", children=[])
        parent = HeaderNode(level=1, text="Title", children=[child])
        assert len(parent.children) == 1
        assert parent.children[0].text == "Section"


class TestExtractHeaderTree:
    """Tests for extract_header_tree function."""

    def test_single_h1(self) -> None:
        """Single H1 produces one root node."""
        tokens = parse_markdown("# Title")
        tree = extract_header_tree(tokens)
        assert len(tree) == 1
        assert tree[0].level == 1
        assert tree[0].text == "Title"

    def test_h1_with_h2_children(self) -> None:
        """H2 headers are children of the preceding H1."""
        content = "# Title\n\n## Section A\n\n## Section B"
        tokens = parse_markdown(content)
        tree = extract_header_tree(tokens)
        assert len(tree) == 1
        assert len(tree[0].children) == 2
        assert tree[0].children[0].text == "Section A"
        assert tree[0].children[1].text == "Section B"

    def test_nested_hierarchy(
        self, sample_nested_path: Path
    ) -> None:
        """sample_nested.md produces a deeply nested header tree."""
        content = sample_nested_path.read_text(encoding="utf-8")
        tokens = parse_markdown(content)
        tree = extract_header_tree(tokens)
        # H1: Architecture
        assert len(tree) == 1
        assert tree[0].text == "Architecture"
        # H2 children: Backend, Frontend
        assert len(tree[0].children) == 2
        assert tree[0].children[0].text == "Backend"
        assert tree[0].children[1].text == "Frontend"
        # H3 children under Backend: Database, Authentication
        backend = tree[0].children[0]
        assert len(backend.children) == 2
        assert backend.children[0].text == "Database"
        assert backend.children[1].text == "Authentication"

    def test_h4_under_h3(
        self, sample_nested_path: Path
    ) -> None:
        """H4 headers are nested under H3."""
        content = sample_nested_path.read_text(encoding="utf-8")
        tokens = parse_markdown(content)
        tree = extract_header_tree(tokens)
        # Architecture > Backend > Database > [Schema Design, Migrations]
        database = tree[0].children[0].children[0]
        assert database.text == "Database"
        assert len(database.children) == 2
        assert database.children[0].text == "Schema Design"
        assert database.children[1].text == "Migrations"

    def test_basic_fixture_header_tree(
        self, sample_basic_path: Path
    ) -> None:
        """sample_basic.md header tree has correct structure."""
        content = sample_basic_path.read_text(encoding="utf-8")
        tokens = parse_markdown(content)
        tree = extract_header_tree(tokens)
        # H1: Getting Started
        assert len(tree) == 1
        assert tree[0].text == "Getting Started"
        # H2: Installation, Configuration, Usage
        h2_texts = [c.text for c in tree[0].children]
        assert "Installation" in h2_texts
        assert "Configuration" in h2_texts
        assert "Usage" in h2_texts

    def test_empty_content_returns_empty_tree(self) -> None:
        """Empty content returns an empty header tree."""
        tokens = parse_markdown("")
        tree = extract_header_tree(tokens)
        assert tree == []

    def test_no_headers_returns_empty_tree(self) -> None:
        """Content with no headers returns an empty tree."""
        tokens = parse_markdown("Just some text without headers.")
        tree = extract_header_tree(tokens)
        assert tree == []


class TestFindSections:
    """Tests for find_sections function."""

    def test_sections_have_header_hierarchy(self) -> None:
        """Each section includes its parent header hierarchy."""
        content = "# Root\n\n## Child\n\nSome text."
        tokens = parse_markdown(content)
        sections = find_sections(tokens)
        # The section under "Child" should have headers ["Root", "Child"]
        child_sections = [s for s in sections if "Child" in s.headers]
        assert len(child_sections) >= 1
        assert child_sections[0].headers == ["Root", "Child"]

    def test_nested_headers_have_full_hierarchy(
        self, sample_nested_path: Path
    ) -> None:
        """Deeply nested sections include full header path."""
        content = sample_nested_path.read_text(encoding="utf-8")
        tokens = parse_markdown(content)
        sections = find_sections(tokens)
        # Find "Schema Design" section
        schema_sections = [
            s for s in sections if "Schema Design" in s.headers
        ]
        assert len(schema_sections) >= 1
        assert schema_sections[0].headers == [
            "Architecture",
            "Backend",
            "Database",
            "Schema Design",
        ]

    def test_section_content_is_not_empty(
        self, sample_basic_path: Path
    ) -> None:
        """Sections extracted from basic fixture have content."""
        content = sample_basic_path.read_text(encoding="utf-8")
        tokens = parse_markdown(content)
        sections = find_sections(tokens)
        # At least some sections should have non-whitespace content
        sections_with_content = [
            s for s in sections if s.content.strip()
        ]
        assert len(sections_with_content) > 0

    def test_code_blocks_are_preserved(
        self, sample_basic_path: Path
    ) -> None:
        """Code blocks appear intact within sections."""
        content = sample_basic_path.read_text(encoding="utf-8")
        tokens = parse_markdown(content)
        sections = find_sections(tokens)
        all_content = " ".join(s.content for s in sections)
        assert "pip install markdown-rag" in all_content

    def test_table_is_preserved(
        self, sample_basic_path: Path
    ) -> None:
        """Table content appears intact within a section."""
        content = sample_basic_path.read_text(encoding="utf-8")
        tokens = parse_markdown(content)
        sections = find_sections(tokens)
        all_content = " ".join(s.content for s in sections)
        assert "chunk_max_size" in all_content

    def test_section_level_matches_header(self) -> None:
        """Section level reflects the header level."""
        content = "# H1\n\nText\n\n## H2\n\nMore text"
        tokens = parse_markdown(content)
        sections = find_sections(tokens)
        h1_sections = [s for s in sections if s.level == 1]
        h2_sections = [s for s in sections if s.level == 2]
        assert len(h1_sections) >= 1
        assert len(h2_sections) >= 1
