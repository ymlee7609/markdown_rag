"""RAGEngine 테스트."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from markdown_rag.models import Chunk, RAGResponse, SearchResult
from markdown_rag.retriever.rag import RAGEngine
from markdown_rag.retriever.search import SemanticSearch


class _MockLLM:
    """테스트용 LLMBackend mock 구현."""

    def __init__(self, response: str = "Test answer", model: str = "mock-model") -> None:
        self._response = response
        self._model = model
        self.last_messages: list[dict[str, str]] = []

    @property
    def model_name(self) -> str:
        return self._model

    def generate(self, messages: list[dict[str, str]]) -> str:
        self.last_messages = messages
        return self._response


@pytest.fixture
def sample_search_results() -> list[SearchResult]:
    """RAG 테스트용 샘플 검색 결과 생성."""
    chunks = [
        Chunk(
            content="Python is a high-level programming language.",
            doc_path=Path("docs/python.md"),
            headers=["Languages", "Python"],
            chunk_index=0,
        ),
        Chunk(
            content="FastAPI uses async/await for performance.",
            doc_path=Path("docs/fastapi.md"),
            headers=["Frameworks", "FastAPI", "Performance"],
            chunk_index=1,
        ),
    ]
    return [
        SearchResult(chunk=chunks[0], score=0.95, rank=1),
        SearchResult(chunk=chunks[1], score=0.80, rank=2),
    ]


@pytest.fixture
def mock_search_engine(sample_search_results: list[SearchResult]) -> MagicMock:
    """SemanticSearch mock 생성."""
    engine = MagicMock(spec=SemanticSearch)
    engine.search.return_value = sample_search_results
    return engine


@pytest.fixture
def mock_llm() -> _MockLLM:
    """LLMBackend mock 생성."""
    return _MockLLM(response="Test answer", model="gpt-4o-mini")


@pytest.fixture
def rag_engine(mock_search_engine: MagicMock, mock_llm: _MockLLM) -> RAGEngine:
    """의존성이 mock된 RAGEngine 생성."""
    return RAGEngine(
        search_engine=mock_search_engine,
        llm_backend=mock_llm,
    )


class TestRAGEngineInit:
    """RAGEngine 초기화 테스트."""

    def test_stores_llm_backend(
        self, mock_search_engine: MagicMock, mock_llm: _MockLLM
    ) -> None:
        engine = RAGEngine(
            search_engine=mock_search_engine,
            llm_backend=mock_llm,
        )
        assert engine.llm_backend is mock_llm

    def test_stores_search_engine(
        self, mock_search_engine: MagicMock, mock_llm: _MockLLM
    ) -> None:
        engine = RAGEngine(
            search_engine=mock_search_engine,
            llm_backend=mock_llm,
        )
        assert engine.search_engine is mock_search_engine


class TestRAGEngineAsk:
    """RAGEngine.ask() 메서드 테스트."""

    def test_calls_search_engine(
        self,
        rag_engine: RAGEngine,
        mock_search_engine: MagicMock,
    ) -> None:
        rag_engine.ask("what is Python?")
        mock_search_engine.search.assert_called_once_with(
            "what is Python?", top_k=None
        )

    def test_passes_top_k_to_search(
        self,
        rag_engine: RAGEngine,
        mock_search_engine: MagicMock,
    ) -> None:
        rag_engine.ask("query", top_k=3)
        mock_search_engine.search.assert_called_once_with("query", top_k=3)

    def test_calls_llm_with_correct_messages(
        self,
        rag_engine: RAGEngine,
        mock_llm: _MockLLM,
    ) -> None:
        rag_engine.ask("query")
        messages = mock_llm.last_messages
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"

    def test_builds_context_with_header_hierarchy(
        self,
        rag_engine: RAGEngine,
        mock_llm: _MockLLM,
    ) -> None:
        rag_engine.ask("query")
        user_msg = mock_llm.last_messages[-1]["content"]
        assert "docs/python.md" in user_msg
        assert "Languages > Python" in user_msg
        assert "Python is a high-level programming language." in user_msg
        assert "docs/fastapi.md" in user_msg
        assert "Frameworks > FastAPI > Performance" in user_msg

    def test_includes_system_prompt(
        self,
        rag_engine: RAGEngine,
        mock_llm: _MockLLM,
    ) -> None:
        rag_engine.ask("query")
        system_msg = mock_llm.last_messages[0]
        assert system_msg["role"] == "system"
        assert "context" in system_msg["content"].lower()

    def test_returns_rag_response(
        self,
        rag_engine: RAGEngine,
    ) -> None:
        response = rag_engine.ask("what is Python?")
        assert isinstance(response, RAGResponse)
        assert response.answer == "Test answer"
        assert response.model == "gpt-4o-mini"
        assert response.query == "what is Python?"

    def test_includes_sources_when_show_sources_true(
        self,
        rag_engine: RAGEngine,
        sample_search_results: list[SearchResult],
    ) -> None:
        response = rag_engine.ask("query", show_sources=True)
        assert len(response.sources) == 2
        assert response.sources[0].score == 0.95
        assert response.sources[1].score == 0.80

    def test_excludes_sources_when_show_sources_false(
        self,
        rag_engine: RAGEngine,
    ) -> None:
        response = rag_engine.ask("query", show_sources=False)
        assert response.sources == []

    def test_model_name_from_llm_backend(
        self,
        mock_search_engine: MagicMock,
    ) -> None:
        llm = _MockLLM(model="custom-model")
        engine = RAGEngine(search_engine=mock_search_engine, llm_backend=llm)
        response = engine.ask("query")
        assert response.model == "custom-model"


class TestRAGEngineEdgeCases:
    """RAGEngine 엣지 케이스 테스트."""

    def test_empty_search_results(
        self,
        mock_search_engine: MagicMock,
    ) -> None:
        mock_search_engine.search.return_value = []
        llm = _MockLLM(response="I don't have enough context.")
        engine = RAGEngine(search_engine=mock_search_engine, llm_backend=llm)
        response = engine.ask("unknown topic")

        assert isinstance(response, RAGResponse)
        assert response.answer == "I don't have enough context."
        assert response.sources == []

    def test_chunk_without_headers(
        self,
        mock_search_engine: MagicMock,
    ) -> None:
        chunk_no_headers = Chunk(
            content="Some content without headers.",
            doc_path=Path("docs/plain.md"),
            headers=[],
            chunk_index=0,
        )
        mock_search_engine.search.return_value = [
            SearchResult(chunk=chunk_no_headers, score=0.7, rank=1),
        ]
        llm = _MockLLM(response="answer")
        engine = RAGEngine(search_engine=mock_search_engine, llm_backend=llm)
        engine.ask("query")

        user_msg = llm.last_messages[-1]["content"]
        assert "docs/plain.md" in user_msg
        assert "Some content without headers." in user_msg


class TestRAGEngineContextBuilding:
    """컨텍스트 구성 로직 상세 테스트."""

    def test_context_format_includes_source_label(
        self,
        rag_engine: RAGEngine,
        mock_llm: _MockLLM,
    ) -> None:
        rag_engine.ask("query")
        user_msg = mock_llm.last_messages[-1]["content"]
        assert "## Source:" in user_msg

    def test_user_query_included_in_messages(
        self,
        rag_engine: RAGEngine,
        mock_llm: _MockLLM,
    ) -> None:
        rag_engine.ask("what is Python?")
        user_msg = mock_llm.last_messages[-1]["content"]
        assert "what is Python?" in user_msg
