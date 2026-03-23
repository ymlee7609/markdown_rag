"""Tests for API route handlers."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from markdown_rag.api.app import create_app
from markdown_rag.config import Settings
from markdown_rag.ingest.pipeline import IngestResult
from markdown_rag.models import Chunk, RAGResponse, SearchResult


@pytest.fixture
def test_settings(tmp_path: Path) -> Settings:
    """Settings for API testing with temp paths."""
    return Settings(
        embedding_backend="local",
        chroma_path=tmp_path / "chroma",
        collection_name="test_api",
        chunk_max_size=500,
        chunk_overlap=50,
    )


@pytest.fixture
def app(test_settings: Settings) -> TestClient:
    """Create a TestClient with a fresh app using test settings."""
    application = create_app(test_settings)
    return TestClient(application)


# --- Health endpoint ---


class TestHealthEndpoint:
    """Tests for GET /health."""

    def test_health_returns_ok(self, app: TestClient) -> None:
        response = app.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


# --- Status endpoint ---


class TestStatusEndpoint:
    """Tests for GET /api/v1/status."""

    def test_status_returns_collection_info(self, app: TestClient) -> None:
        response = app.get("/api/v1/status")
        assert response.status_code == 200
        data = response.json()
        assert "collection_name" in data
        assert "total_chunks" in data
        assert "embedding_backend" in data
        assert isinstance(data["total_chunks"], int)


# --- Ingest endpoint ---


class TestIngestEndpoint:
    """Tests for POST /api/v1/ingest."""

    @patch("markdown_rag.api.routes.ingest.IngestPipeline")
    def test_ingest_success(
        self, mock_pipeline_cls: MagicMock, app: TestClient, tmp_path: Path
    ) -> None:
        # Create a real markdown file
        md_file = tmp_path / "test.md"
        md_file.write_text("# Hello\nWorld")

        mock_pipeline = MagicMock()
        mock_pipeline.ingest.return_value = IngestResult(
            documents_processed=1, chunks_created=3, errors=[]
        )
        mock_pipeline_cls.return_value = mock_pipeline

        response = app.post(
            "/api/v1/ingest",
            json={"path": str(md_file)},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["documents_processed"] == 1
        assert data["chunks_created"] == 3
        assert data["errors"] == []

    @patch("markdown_rag.api.routes.ingest.IngestPipeline")
    def test_ingest_with_verbose(
        self, mock_pipeline_cls: MagicMock, app: TestClient, tmp_path: Path
    ) -> None:
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test")

        mock_pipeline = MagicMock()
        mock_pipeline.ingest.return_value = IngestResult(
            documents_processed=1, chunks_created=2, errors=[]
        )
        mock_pipeline_cls.return_value = mock_pipeline

        response = app.post(
            "/api/v1/ingest",
            json={"path": str(md_file), "verbose": True},
        )
        assert response.status_code == 200
        mock_pipeline.ingest.assert_called_once()

    def test_ingest_missing_path_returns_422(self, app: TestClient) -> None:
        response = app.post("/api/v1/ingest", json={})
        assert response.status_code == 422

    @patch("markdown_rag.api.routes.ingest.IngestPipeline")
    def test_ingest_nonexistent_path_returns_400(
        self, mock_pipeline_cls: MagicMock, app: TestClient
    ) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.ingest.side_effect = FileNotFoundError("not found")
        mock_pipeline_cls.return_value = mock_pipeline

        response = app.post(
            "/api/v1/ingest",
            json={"path": "/nonexistent/path"},
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    @patch("markdown_rag.api.routes.ingest.IngestPipeline")
    def test_ingest_pipeline_error_returns_500(
        self, mock_pipeline_cls: MagicMock, app: TestClient
    ) -> None:
        mock_pipeline = MagicMock()
        mock_pipeline.ingest.side_effect = RuntimeError("unexpected error")
        mock_pipeline_cls.return_value = mock_pipeline

        response = app.post(
            "/api/v1/ingest",
            json={"path": "/some/path"},
        )
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data


# --- Search endpoint ---


class TestSearchEndpoint:
    """Tests for POST /api/v1/search."""

    @patch("markdown_rag.api.routes.search.SemanticSearch")
    @patch("markdown_rag.api.routes.search._get_embedding_backend")
    def test_search_success(
        self,
        mock_get_emb: MagicMock,
        mock_search_cls: MagicMock,
        app: TestClient,
    ) -> None:
        mock_emb = MagicMock()
        mock_get_emb.return_value = mock_emb

        mock_search = MagicMock()
        mock_search.search.return_value = [
            SearchResult(
                chunk=Chunk(
                    content="test content",
                    doc_path=Path("test.md"),
                    headers=["H1"],
                    chunk_index=0,
                ),
                score=0.95,
                rank=1,
            )
        ]
        mock_search_cls.return_value = mock_search

        response = app.post(
            "/api/v1/search",
            json={"query": "how to install?"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "how to install?"
        assert len(data["results"]) == 1
        assert data["total"] == 1
        assert data["results"][0]["score"] == 0.95

    @patch("markdown_rag.api.routes.search.SemanticSearch")
    @patch("markdown_rag.api.routes.search._get_embedding_backend")
    def test_search_empty_results(
        self,
        mock_get_emb: MagicMock,
        mock_search_cls: MagicMock,
        app: TestClient,
    ) -> None:
        mock_emb = MagicMock()
        mock_get_emb.return_value = mock_emb

        mock_search = MagicMock()
        mock_search.search.return_value = []
        mock_search_cls.return_value = mock_search

        response = app.post(
            "/api/v1/search",
            json={"query": "nonexistent"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["results"] == []
        assert data["total"] == 0

    @patch("markdown_rag.api.routes.search.SemanticSearch")
    @patch("markdown_rag.api.routes.search._get_embedding_backend")
    def test_search_custom_top_k(
        self,
        mock_get_emb: MagicMock,
        mock_search_cls: MagicMock,
        app: TestClient,
    ) -> None:
        mock_emb = MagicMock()
        mock_get_emb.return_value = mock_emb

        mock_search = MagicMock()
        mock_search.search.return_value = []
        mock_search_cls.return_value = mock_search

        response = app.post(
            "/api/v1/search",
            json={"query": "test", "top_k": 10},
        )
        assert response.status_code == 200

    def test_search_missing_query_returns_422(self, app: TestClient) -> None:
        response = app.post("/api/v1/search", json={})
        assert response.status_code == 422

    @patch("markdown_rag.api.routes.search.SemanticSearch")
    @patch("markdown_rag.api.routes.search._get_embedding_backend")
    def test_search_internal_error_returns_500(
        self,
        mock_get_emb: MagicMock,
        mock_search_cls: MagicMock,
        app: TestClient,
    ) -> None:
        mock_emb = MagicMock()
        mock_get_emb.return_value = mock_emb

        mock_search = MagicMock()
        mock_search.search.side_effect = RuntimeError("search failed")
        mock_search_cls.return_value = mock_search

        response = app.post(
            "/api/v1/search",
            json={"query": "test"},
        )
        assert response.status_code == 500


# --- Ask endpoint ---


class TestAskEndpoint:
    """Tests for POST /api/v1/ask."""

    @patch("markdown_rag.api.routes.ask.RAGEngine")
    @patch("markdown_rag.api.routes.ask.SemanticSearch")
    @patch("markdown_rag.api.routes.ask._get_embedding_backend")
    @patch("markdown_rag.api.routes.ask._get_llm_backend")
    def test_ask_success(
        self,
        mock_get_llm: MagicMock,
        mock_get_emb: MagicMock,
        mock_search_cls: MagicMock,
        mock_rag_cls: MagicMock,
        app: TestClient,
    ) -> None:
        mock_get_emb.return_value = MagicMock()
        mock_get_llm.return_value = MagicMock()

        mock_rag = MagicMock()
        mock_rag.ask.return_value = RAGResponse(
            answer="The answer is 42.",
            sources=[
                SearchResult(
                    chunk=Chunk(
                        content="context",
                        doc_path=Path("doc.md"),
                        headers=["Section"],
                        chunk_index=0,
                    ),
                    score=0.9,
                    rank=1,
                )
            ],
            model="gpt-4o-mini",
            query="What is the answer?",
        )
        mock_rag_cls.return_value = mock_rag

        response = app.post(
            "/api/v1/ask",
            json={"query": "What is the answer?"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "The answer is 42."
        assert data["model"] == "gpt-4o-mini"
        assert len(data["sources"]) == 1

    @patch("markdown_rag.api.routes.ask.RAGEngine")
    @patch("markdown_rag.api.routes.ask.SemanticSearch")
    @patch("markdown_rag.api.routes.ask._get_embedding_backend")
    @patch("markdown_rag.api.routes.ask._get_llm_backend")
    def test_ask_custom_model(
        self,
        mock_get_llm: MagicMock,
        mock_get_emb: MagicMock,
        mock_search_cls: MagicMock,
        mock_rag_cls: MagicMock,
        app: TestClient,
    ) -> None:
        mock_get_emb.return_value = MagicMock()
        mock_get_llm.return_value = MagicMock()

        mock_rag = MagicMock()
        mock_rag.ask.return_value = RAGResponse(
            answer="answer",
            sources=[],
            model="gpt-4o",
            query="q",
        )
        mock_rag_cls.return_value = mock_rag

        response = app.post(
            "/api/v1/ask",
            json={"query": "q", "model": "gpt-4o"},
        )
        assert response.status_code == 200

    @patch("markdown_rag.api.routes.ask._get_llm_backend")
    def test_ask_missing_api_key_returns_400(
        self, mock_get_llm: MagicMock, app: TestClient
    ) -> None:
        mock_get_llm.side_effect = HTTPException(
            status_code=400,
            detail="OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.",
        )

        response = app.post(
            "/api/v1/ask",
            json={"query": "test"},
        )
        assert response.status_code == 400

    def test_ask_missing_query_returns_422(self, app: TestClient) -> None:
        response = app.post("/api/v1/ask", json={})
        assert response.status_code == 422

    @patch("markdown_rag.api.routes.ask.RAGEngine")
    @patch("markdown_rag.api.routes.ask.SemanticSearch")
    @patch("markdown_rag.api.routes.ask._get_embedding_backend")
    @patch("markdown_rag.api.routes.ask._get_llm_backend")
    def test_ask_internal_error_returns_500(
        self,
        mock_get_llm: MagicMock,
        mock_get_emb: MagicMock,
        mock_search_cls: MagicMock,
        mock_rag_cls: MagicMock,
        app: TestClient,
    ) -> None:
        mock_get_emb.return_value = MagicMock()
        mock_get_llm.return_value = MagicMock()

        mock_rag = MagicMock()
        mock_rag.ask.side_effect = RuntimeError("LLM error")
        mock_rag_cls.return_value = mock_rag

        response = app.post(
            "/api/v1/ask",
            json={"query": "test"},
        )
        assert response.status_code == 500


# --- Delete endpoint ---


class TestDeleteEndpoint:
    """Tests for DELETE /api/v1/documents."""

    def test_delete_success(self, app: TestClient, test_settings: Settings) -> None:
        # Access the underlying app to mock the store
        with patch.object(
            app.app.state, "vector_store", create=True
        ) as mock_store:
            mock_store.delete_by_document.return_value = 3

            response = app.request(
                "DELETE",
                "/api/v1/documents",
                json={"doc_path": "test.md"},
            )
            assert response.status_code == 200
            data = response.json()
            assert data["doc_path"] == "test.md"
            assert data["chunks_deleted"] == 3

    def test_delete_missing_doc_path_returns_422(self, app: TestClient) -> None:
        response = app.request(
            "DELETE",
            "/api/v1/documents",
            json={},
        )
        assert response.status_code == 422

    def test_delete_not_found_returns_zero(
        self, app: TestClient, test_settings: Settings
    ) -> None:
        with patch.object(
            app.app.state, "vector_store", create=True
        ) as mock_store:
            mock_store.delete_by_document.return_value = 0

            response = app.request(
                "DELETE",
                "/api/v1/documents",
                json={"doc_path": "nonexistent.md"},
            )
            assert response.status_code == 200
            data = response.json()
            assert data["chunks_deleted"] == 0


# --- Validation error format ---


class TestValidationErrors:
    """Tests for request validation error format."""

    def test_ingest_validation_error_format(self, app: TestClient) -> None:
        response = app.post("/api/v1/ingest", json={})
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_search_validation_error_format(self, app: TestClient) -> None:
        response = app.post("/api/v1/search", json={})
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_ask_validation_error_format(self, app: TestClient) -> None:
        response = app.post("/api/v1/ask", json={})
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
