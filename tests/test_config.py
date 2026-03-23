"""Tests for configuration module."""

from pathlib import Path

from markdown_rag.config import Settings, get_settings


class TestSettings:
    def test_default_settings(self):
        settings = Settings()
        assert settings.embedding_backend == "local"
        assert settings.local_model == "all-MiniLM-L6-v2"
        assert settings.chunk_max_size == 1000
        assert settings.chunk_overlap == 100
        assert settings.search_top_k == 5
        assert settings.api_port == 8900

    def test_custom_settings(self):
        settings = Settings(
            embedding_backend="openai",
            chunk_max_size=2000,
            api_port=9000,
        )
        assert settings.embedding_backend == "openai"
        assert settings.chunk_max_size == 2000
        assert settings.api_port == 9000

    def test_chroma_path_is_path(self):
        settings = Settings()
        assert isinstance(settings.chroma_path, Path)

    def test_get_settings_with_overrides(self):
        settings = get_settings(chunk_max_size=500)
        assert settings.chunk_max_size == 500
