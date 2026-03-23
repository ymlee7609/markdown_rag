"""Shared test fixtures for Markdown RAG."""

from pathlib import Path

import pytest

from markdown_rag.config import Settings
from markdown_rag.models import Chunk, Document

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def sample_basic_path() -> Path:
    return FIXTURES_DIR / "sample_basic.md"


@pytest.fixture
def sample_frontmatter_path() -> Path:
    return FIXTURES_DIR / "sample_frontmatter.md"


@pytest.fixture
def sample_nested_path() -> Path:
    return FIXTURES_DIR / "sample_nested.md"


@pytest.fixture
def sample_basic_content(sample_basic_path: Path) -> str:
    return sample_basic_path.read_text(encoding="utf-8")


@pytest.fixture
def sample_document(sample_basic_path: Path) -> Document:
    return Document(
        path=sample_basic_path,
        content=sample_basic_path.read_text(encoding="utf-8"),
    )


@pytest.fixture
def sample_chunks() -> list[Chunk]:
    return [
        Chunk(
            content="This is a sample document for testing.",
            doc_path=Path("test.md"),
            headers=["Getting Started"],
            chunk_index=0,
        ),
        Chunk(
            content="Run the following command: pip install markdown-rag",
            doc_path=Path("test.md"),
            headers=["Getting Started", "Installation"],
            chunk_index=1,
        ),
        Chunk(
            content="Set up your environment with embedding and model settings.",
            doc_path=Path("test.md"),
            headers=["Getting Started", "Configuration"],
            chunk_index=2,
        ),
    ]


@pytest.fixture
def test_settings(tmp_path: Path) -> Settings:
    return Settings(
        embedding_backend="local",
        chroma_path=tmp_path / "chroma",
        collection_name="test_collection",
        chunk_max_size=500,
        chunk_overlap=50,
    )
