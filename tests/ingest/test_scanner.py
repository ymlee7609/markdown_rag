"""Tests for MarkdownScanner - directory/file scanning for Markdown documents."""

from pathlib import Path

import pytest

from markdown_rag.ingest.scanner import MarkdownScanner
from markdown_rag.models import Document


class TestMarkdownScannerSingleFile:
    """Tests for scanning a single Markdown file."""

    def test_scan_single_file_returns_one_document(self, tmp_path: Path) -> None:
        """Scanning a single .md file should return a list with one Document."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Hello\n\nWorld", encoding="utf-8")

        scanner = MarkdownScanner()
        result = scanner.scan(md_file)

        assert len(result) == 1
        assert isinstance(result[0], Document)

    def test_scan_single_file_content(self, tmp_path: Path) -> None:
        """Scanning a single file should read its content correctly."""
        content = "# Title\n\nSome content here."
        md_file = tmp_path / "readme.md"
        md_file.write_text(content, encoding="utf-8")

        scanner = MarkdownScanner()
        result = scanner.scan(md_file)

        assert result[0].content == content
        assert result[0].path == md_file

    def test_scan_single_file_preserves_utf8(self, tmp_path: Path) -> None:
        """Scanner should handle UTF-8 content including Korean characters."""
        content = "# Test\n\nHello World"
        md_file = tmp_path / "korean.md"
        md_file.write_text(content, encoding="utf-8")

        scanner = MarkdownScanner()
        result = scanner.scan(md_file)

        assert result[0].content == content


class TestMarkdownScannerDirectory:
    """Tests for scanning a directory recursively."""

    def test_scan_directory_finds_all_md_files(self, tmp_path: Path) -> None:
        """Scanning a directory should find all .md files recursively."""
        (tmp_path / "a.md").write_text("# A", encoding="utf-8")
        (tmp_path / "b.md").write_text("# B", encoding="utf-8")
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "c.md").write_text("# C", encoding="utf-8")

        scanner = MarkdownScanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 3

    def test_scan_directory_ignores_non_md_files(self, tmp_path: Path) -> None:
        """Scanner should only pick up .md files, not .txt or others."""
        (tmp_path / "readme.md").write_text("# README", encoding="utf-8")
        (tmp_path / "notes.txt").write_text("plain text", encoding="utf-8")
        (tmp_path / "data.json").write_text("{}", encoding="utf-8")

        scanner = MarkdownScanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1
        assert result[0].path.name == "readme.md"

    def test_scan_directory_skips_hidden_files(self, tmp_path: Path) -> None:
        """Scanner should skip files starting with a dot."""
        (tmp_path / "visible.md").write_text("# Visible", encoding="utf-8")
        (tmp_path / ".hidden.md").write_text("# Hidden", encoding="utf-8")

        scanner = MarkdownScanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1
        assert result[0].path.name == "visible.md"

    def test_scan_directory_skips_hidden_directories(self, tmp_path: Path) -> None:
        """Scanner should skip directories starting with a dot."""
        (tmp_path / "public.md").write_text("# Public", encoding="utf-8")
        hidden_dir = tmp_path / ".hidden"
        hidden_dir.mkdir()
        (hidden_dir / "secret.md").write_text("# Secret", encoding="utf-8")

        scanner = MarkdownScanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1
        assert result[0].path.name == "public.md"

    def test_scan_directory_results_sorted_by_path(self, tmp_path: Path) -> None:
        """Results should be sorted by file path for deterministic ordering."""
        (tmp_path / "c.md").write_text("# C", encoding="utf-8")
        (tmp_path / "a.md").write_text("# A", encoding="utf-8")
        (tmp_path / "b.md").write_text("# B", encoding="utf-8")

        scanner = MarkdownScanner()
        result = scanner.scan(tmp_path)

        paths = [doc.path.name for doc in result]
        assert paths == ["a.md", "b.md", "c.md"]

    def test_scan_empty_directory_returns_empty(self, tmp_path: Path) -> None:
        """Scanning an empty directory should return an empty list."""
        scanner = MarkdownScanner()
        result = scanner.scan(tmp_path)

        assert result == []

    def test_scan_deeply_nested_directories(self, tmp_path: Path) -> None:
        """Scanner should find files in deeply nested directories."""
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True)
        (deep / "deep.md").write_text("# Deep", encoding="utf-8")

        scanner = MarkdownScanner()
        result = scanner.scan(tmp_path)

        assert len(result) == 1
        assert result[0].path.name == "deep.md"


class TestMarkdownScannerErrorHandling:
    """Tests for error handling in the scanner."""

    def test_scan_nonexistent_path_raises(self) -> None:
        """Scanning a non-existent path should raise FileNotFoundError."""
        scanner = MarkdownScanner()

        with pytest.raises(FileNotFoundError):
            scanner.scan(Path("/nonexistent/path/does/not/exist"))

    def test_scan_empty_file(self, tmp_path: Path) -> None:
        """Scanning an empty file should return a Document with empty content."""
        md_file = tmp_path / "empty.md"
        md_file.write_text("", encoding="utf-8")

        scanner = MarkdownScanner()
        result = scanner.scan(md_file)

        assert len(result) == 1
        assert result[0].content == ""


class TestMarkdownScannerWithFixtures:
    """Tests using the real fixture files."""

    def test_scan_fixtures_directory(self, fixtures_dir: Path) -> None:
        """Scanner should find all fixture Markdown files."""
        scanner = MarkdownScanner()
        result = scanner.scan(fixtures_dir)

        # We know there are 3 fixture files
        assert len(result) == 3

        names = {doc.path.name for doc in result}
        assert "sample_basic.md" in names
        assert "sample_frontmatter.md" in names
        assert "sample_nested.md" in names

    def test_scan_single_fixture_file(self, sample_basic_path: Path) -> None:
        """Scanner should read a fixture file correctly."""
        scanner = MarkdownScanner()
        result = scanner.scan(sample_basic_path)

        assert len(result) == 1
        assert "# Getting Started" in result[0].content
