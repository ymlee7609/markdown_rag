"""FastAPI application factory for Markdown RAG API."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from markdown_rag import __version__
from markdown_rag.api.routes.ask import router as ask_router
from markdown_rag.api.routes.health import router as health_router
from markdown_rag.api.routes.ingest import router as ingest_router
from markdown_rag.api.routes.search import router as search_router
from markdown_rag.config import Settings, get_settings
from markdown_rag.store.chroma import ChromaStore


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        settings: Application settings. If None, loads defaults
            via get_settings().

    Returns:
        Configured FastAPI application instance.
    """
    if settings is None:
        settings = get_settings()

    app = FastAPI(
        title="Markdown RAG API",
        version=__version__,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Store shared resources on app.state
    app.state.settings = settings
    app.state.vector_store = ChromaStore(
        persist_path=settings.chroma_path,
        collection_name=settings.collection_name,
    )

    # Register routers
    app.include_router(health_router)
    app.include_router(ingest_router)
    app.include_router(search_router)
    app.include_router(ask_router)

    return app
