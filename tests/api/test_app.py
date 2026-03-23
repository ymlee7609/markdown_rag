"""Tests for FastAPI application factory."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from markdown_rag.api.app import create_app
from markdown_rag.config import Settings


class TestCreateApp:
    """Tests for the create_app factory function."""

    def test_returns_fastapi_instance(self, tmp_path: Path) -> None:
        settings = Settings(
            chroma_path=tmp_path / "chroma",
            collection_name="test_app",
        )
        app = create_app(settings)
        assert isinstance(app, FastAPI)

    def test_app_title(self, tmp_path: Path) -> None:
        settings = Settings(
            chroma_path=tmp_path / "chroma",
            collection_name="test_title",
        )
        app = create_app(settings)
        assert app.title == "Markdown RAG API"

    def test_app_version(self, tmp_path: Path) -> None:
        settings = Settings(
            chroma_path=tmp_path / "chroma",
            collection_name="test_version",
        )
        app = create_app(settings)
        assert app.version == "0.1.0"

    def test_settings_stored_in_state(self, tmp_path: Path) -> None:
        settings = Settings(
            chroma_path=tmp_path / "chroma",
            collection_name="test_state",
        )
        app = create_app(settings)
        assert app.state.settings is settings

    def test_cors_headers(self, tmp_path: Path) -> None:
        settings = Settings(
            chroma_path=tmp_path / "chroma",
            collection_name="test_cors",
        )
        app = create_app(settings)
        client = TestClient(app)
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.headers.get("access-control-allow-origin") is not None

    def test_health_endpoint_registered(self, tmp_path: Path) -> None:
        settings = Settings(
            chroma_path=tmp_path / "chroma",
            collection_name="test_health_reg",
        )
        app = create_app(settings)
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200

    def test_default_settings_when_none(self) -> None:
        """create_app should work with default settings when None passed."""
        app = create_app(settings=None)
        assert isinstance(app, FastAPI)
        assert app.state.settings is not None
