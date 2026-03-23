"""Tests for API request/response schemas."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from markdown_rag.api.schemas import (
    AskRequest,
    AskResponse,
    ChunkResponse,
    DeleteRequest,
    DeleteResponse,
    HealthResponse,
    IngestRequest,
    IngestResponse,
    SearchRequest,
    SearchResponse,
    SearchResultResponse,
    StatusResponse,
)


class TestIngestRequest:
    """Tests for IngestRequest schema."""

    def test_valid_request(self) -> None:
        req = IngestRequest(path="/docs")
        assert req.path == "/docs"
        assert req.verbose is False

    def test_verbose_override(self) -> None:
        req = IngestRequest(path="/docs", verbose=True)
        assert req.verbose is True

    def test_missing_path_raises(self) -> None:
        with pytest.raises(ValidationError):
            IngestRequest()  # type: ignore[call-arg]


class TestSearchRequest:
    """Tests for SearchRequest schema."""

    def test_valid_request(self) -> None:
        req = SearchRequest(query="how to install?")
        assert req.query == "how to install?"
        assert req.top_k == 5

    def test_custom_top_k(self) -> None:
        req = SearchRequest(query="test", top_k=10)
        assert req.top_k == 10

    def test_missing_query_raises(self) -> None:
        with pytest.raises(ValidationError):
            SearchRequest()  # type: ignore[call-arg]


class TestAskRequest:
    """Tests for AskRequest schema."""

    def test_valid_request(self) -> None:
        req = AskRequest(query="What is Markdown RAG?")
        assert req.query == "What is Markdown RAG?"
        assert req.top_k == 5
        assert req.show_sources is True
        assert req.model == "gpt-4o-mini"

    def test_custom_model(self) -> None:
        req = AskRequest(query="test", model="gpt-4o")
        assert req.model == "gpt-4o"

    def test_missing_query_raises(self) -> None:
        with pytest.raises(ValidationError):
            AskRequest()  # type: ignore[call-arg]


class TestDeleteRequest:
    """Tests for DeleteRequest schema."""

    def test_valid_request(self) -> None:
        req = DeleteRequest(doc_path="test.md")
        assert req.doc_path == "test.md"

    def test_missing_doc_path_raises(self) -> None:
        with pytest.raises(ValidationError):
            DeleteRequest()  # type: ignore[call-arg]


class TestChunkResponse:
    """Tests for ChunkResponse schema."""

    def test_valid_chunk(self) -> None:
        chunk = ChunkResponse(
            content="some text",
            doc_path="test.md",
            headers=["H1", "H2"],
            chunk_index=0,
        )
        assert chunk.content == "some text"
        assert chunk.doc_path == "test.md"
        assert chunk.headers == ["H1", "H2"]
        assert chunk.chunk_index == 0


class TestSearchResultResponse:
    """Tests for SearchResultResponse schema."""

    def test_valid_result(self) -> None:
        result = SearchResultResponse(
            chunk=ChunkResponse(
                content="text",
                doc_path="test.md",
                headers=[],
                chunk_index=0,
            ),
            score=0.95,
            rank=1,
        )
        assert result.score == 0.95
        assert result.rank == 1


class TestIngestResponse:
    """Tests for IngestResponse schema."""

    def test_valid_response(self) -> None:
        resp = IngestResponse(
            documents_processed=5,
            chunks_created=20,
            errors=[],
        )
        assert resp.documents_processed == 5
        assert resp.chunks_created == 20
        assert resp.errors == []


class TestSearchResponse:
    """Tests for SearchResponse schema."""

    def test_valid_response(self) -> None:
        resp = SearchResponse(query="test", results=[], total=0)
        assert resp.query == "test"
        assert resp.results == []
        assert resp.total == 0


class TestAskResponse:
    """Tests for AskResponse schema."""

    def test_valid_response(self) -> None:
        resp = AskResponse(
            answer="The answer is 42.",
            query="What is the answer?",
            model="gpt-4o-mini",
            sources=[],
        )
        assert resp.answer == "The answer is 42."
        assert resp.model == "gpt-4o-mini"


class TestStatusResponse:
    """Tests for StatusResponse schema."""

    def test_valid_response(self) -> None:
        resp = StatusResponse(
            collection_name="test",
            total_chunks=100,
            embedding_backend="local",
        )
        assert resp.total_chunks == 100


class TestHealthResponse:
    """Tests for HealthResponse schema."""

    def test_valid_response(self) -> None:
        resp = HealthResponse(status="ok")
        assert resp.status == "ok"


class TestDeleteResponse:
    """Tests for DeleteResponse schema."""

    def test_valid_response(self) -> None:
        resp = DeleteResponse(doc_path="test.md", chunks_deleted=5)
        assert resp.doc_path == "test.md"
        assert resp.chunks_deleted == 5
