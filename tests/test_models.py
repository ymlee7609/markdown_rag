"""Tests for domain models."""

from pathlib import Path

from markdown_rag.models import Chunk, Document, RAGResponse, SearchResult


class TestDocument:
    def test_create_document(self):
        doc = Document(path=Path("test.md"), content="Hello")
        assert doc.path == Path("test.md")
        assert doc.content == "Hello"
        assert doc.metadata == {}

    def test_file_name(self):
        doc = Document(path=Path("/docs/test.md"), content="")
        assert doc.file_name == "test.md"

    def test_metadata(self):
        doc = Document(path=Path("t.md"), content="", metadata={"title": "Test"})
        assert doc.metadata["title"] == "Test"


class TestChunk:
    def test_create_chunk(self):
        chunk = Chunk(content="text", doc_path=Path("test.md"))
        assert chunk.content == "text"
        assert chunk.headers == []
        assert chunk.chunk_index == 0

    def test_header_context(self):
        chunk = Chunk(
            content="text",
            doc_path=Path("test.md"),
            headers=["Architecture", "Backend", "Auth"],
        )
        assert chunk.header_context == "Architecture > Backend > Auth"

    def test_header_context_empty(self):
        chunk = Chunk(content="text", doc_path=Path("test.md"))
        assert chunk.header_context == ""

    def test_chunk_id(self):
        chunk = Chunk(content="text", doc_path=Path("test.md"), chunk_index=3)
        assert chunk.chunk_id == "test.md::chunk-3"


class TestSearchResult:
    def test_create_search_result(self):
        chunk = Chunk(content="text", doc_path=Path("test.md"))
        result = SearchResult(chunk=chunk, score=0.95, rank=1)
        assert result.score == 0.95
        assert result.rank == 1


class TestRAGResponse:
    def test_create_rag_response(self):
        resp = RAGResponse(answer="The answer is 42", query="What is it?")
        assert resp.answer == "The answer is 42"
        assert resp.sources == []
        assert resp.query == "What is it?"
