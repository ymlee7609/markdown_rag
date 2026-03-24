"""Application configuration with Pydantic Settings."""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Markdown RAG application settings.

    Loaded from environment variables with MDRAG_ prefix,
    or from .env file.
    """

    model_config = SettingsConfigDict(
        env_prefix="MDRAG_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 임베딩 백엔드 선택
    embedding_backend: Literal["local", "openai"] = "local"

    # 로컬 임베딩 모델 (sentence-transformers)
    # multilingual-e5-small: 384차원, 한국어+영어 다국어 지원
    local_model: str = "intfloat/multilingual-e5-small"

    # OpenAI 설정
    openai_embedding_model: str = "text-embedding-3-small"
    openai_llm_model: str = "gpt-4o-mini"

    # LLM 백엔드 선택
    llm_backend: Literal["local", "openai"] = "openai"

    # 로컬 LLM 설정 (llama-cpp-python, GGUF 모델)
    local_llm_model_path: str = ""
    local_llm_context_size: int = 4096
    local_llm_max_tokens: int = 1024

    # ChromaDB settings
    chroma_path: Path = Path("./data/chroma")
    collection_name: str = "markdown_docs"

    # Chunk settings
    chunk_max_size: int = 1000
    chunk_overlap: int = 100

    # Search settings
    search_top_k: int = 5
    search_mode: Literal["vector", "bm25", "hybrid"] = "vector"
    hybrid_alpha: float = 0.7

    # BM25 인덱스 저장 경로
    bm25_index_path: Path = Path("./data/bm25_index.pkl")

    # 리랭킹 설정
    rerank_enabled: bool = False
    rerank_model: str = "BAAI/bge-reranker-v2-m3"
    initial_top_k: int = 20

    # API server settings
    api_host: str = "0.0.0.0"
    api_port: int = 8900


def get_settings(**overrides) -> Settings:
    """Create settings instance with optional overrides."""
    return Settings(**overrides)
