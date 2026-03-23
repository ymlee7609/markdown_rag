"""Directory and file scanner for Markdown documents.

Scans file system paths to discover Markdown (.md) files and
creates Document objects with their content loaded.
"""

from __future__ import annotations

import logging
from pathlib import Path

from markdown_rag.models import Document

logger = logging.getLogger(__name__)


class MarkdownScanner:
    """Scans directories and files to discover Markdown documents.

    Recursively walks directories to find all .md files,
    skipping hidden files and directories (those starting with '.').
    Results are sorted by file path for deterministic ordering.
    """

    def scan(self, path: Path) -> list[Document]:
        """Scan a file or directory for Markdown documents.

        Args:
            path: Path to a single .md file or a directory to scan recursively.

        Returns:
            List of Document objects sorted by file path.

        Raises:
            FileNotFoundError: If the path does not exist.
        """
        if not path.exists():
            msg = f"Path does not exist: {path}"
            raise FileNotFoundError(msg)

        if path.is_file():
            return [self._read_document(path)]

        # Directory: recursively find all .md files
        md_files = self._find_markdown_files(path)
        documents = [self._read_document(f) for f in md_files]

        # Sort by file path for deterministic ordering
        documents.sort(key=lambda d: d.path)

        return documents

    def _find_markdown_files(self, directory: Path) -> list[Path]:
        """Recursively find all .md files, skipping hidden entries.

        Args:
            directory: Root directory to search.

        Returns:
            List of Path objects for discovered .md files.
        """
        md_files: list[Path] = []

        for item in sorted(directory.rglob("*.md")):
            # Skip hidden files and directories
            if self._is_hidden(item, directory):
                continue
            md_files.append(item)

        return md_files

    def _is_hidden(self, path: Path, root: Path) -> bool:
        """Check if a path or any of its parent directories is hidden.

        A path component is considered hidden if its name starts with '.'.

        Args:
            path: The file path to check.
            root: The root directory (components above root are not checked).

        Returns:
            True if any component in the path (relative to root) is hidden.
        """
        try:
            rel = path.relative_to(root)
        except ValueError:
            return False

        for part in rel.parts:
            if part.startswith("."):
                return True
        return False

    def _read_document(self, path: Path) -> Document:
        """Read a Markdown file and create a Document object.

        Args:
            path: Path to the .md file.

        Returns:
            Document with path and content loaded.
        """
        content = path.read_text(encoding="utf-8")
        logger.debug("Read document: %s (%d chars)", path, len(content))
        return Document(path=path, content=content)
