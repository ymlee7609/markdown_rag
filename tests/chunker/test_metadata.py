"""Tests for metadata extraction from Markdown frontmatter.

TDD RED phase: These tests define the expected behavior of the
metadata extractor before implementation.
"""

from pathlib import Path

from markdown_rag.chunker.metadata import extract_frontmatter


class TestExtractFrontmatter:
    """Tests for extract_frontmatter function."""

    def test_returns_tuple_of_dict_and_str(
        self, sample_frontmatter_path: Path
    ) -> None:
        """extract_frontmatter returns (metadata_dict, content_str)."""
        content = sample_frontmatter_path.read_text(encoding="utf-8")
        result = extract_frontmatter(content)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], dict)
        assert isinstance(result[1], str)

    def test_extracts_title(self, sample_frontmatter_path: Path) -> None:
        """Frontmatter title is extracted correctly."""
        content = sample_frontmatter_path.read_text(encoding="utf-8")
        metadata, _ = extract_frontmatter(content)
        assert metadata["title"] == "API Reference"

    def test_extracts_author(self, sample_frontmatter_path: Path) -> None:
        """Frontmatter author is extracted correctly."""
        content = sample_frontmatter_path.read_text(encoding="utf-8")
        metadata, _ = extract_frontmatter(content)
        assert metadata["author"] == "Team"

    def test_extracts_tags(self, sample_frontmatter_path: Path) -> None:
        """Frontmatter tags are extracted as a list."""
        content = sample_frontmatter_path.read_text(encoding="utf-8")
        metadata, _ = extract_frontmatter(content)
        assert metadata["tags"] == ["api", "reference"]

    def test_extracts_date(self, sample_frontmatter_path: Path) -> None:
        """Frontmatter date is extracted correctly."""
        content = sample_frontmatter_path.read_text(encoding="utf-8")
        metadata, _ = extract_frontmatter(content)
        # python-frontmatter may parse date as datetime.date
        assert str(metadata["date"]) == "2024-01-15"

    def test_content_without_frontmatter_delimiter(
        self, sample_frontmatter_path: Path
    ) -> None:
        """Returned content does not contain frontmatter delimiters (---)."""
        content = sample_frontmatter_path.read_text(encoding="utf-8")
        _, body = extract_frontmatter(content)
        # The body should NOT start with ---
        assert not body.lstrip().startswith("---")

    def test_content_preserves_body(
        self, sample_frontmatter_path: Path
    ) -> None:
        """Returned content contains the original body text."""
        content = sample_frontmatter_path.read_text(encoding="utf-8")
        _, body = extract_frontmatter(content)
        assert "# API Reference" in body
        assert "## Authentication" in body
        assert "## Endpoints" in body

    def test_no_frontmatter_returns_empty_dict(self) -> None:
        """Content without frontmatter returns empty metadata dict."""
        content = "# Just a Header\n\nSome text."
        metadata, body = extract_frontmatter(content)
        assert metadata == {}
        assert "# Just a Header" in body

    def test_no_frontmatter_preserves_content(self) -> None:
        """Content without frontmatter is returned unchanged."""
        content = "# Just a Header\n\nSome text."
        _, body = extract_frontmatter(content)
        assert body.strip() == content.strip()

    def test_empty_frontmatter(self) -> None:
        """Empty frontmatter block returns empty dict."""
        content = "---\n---\n# Title\n\nBody text."
        metadata, body = extract_frontmatter(content)
        assert metadata == {}
        assert "# Title" in body

    def test_empty_string_input(self) -> None:
        """Empty string returns empty dict and empty body."""
        metadata, body = extract_frontmatter("")
        assert metadata == {}
        assert body == ""
