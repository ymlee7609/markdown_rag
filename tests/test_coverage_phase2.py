"""Phase 2-6 커버리지 갭을 메우는 테스트."""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import MagicMock, patch

from markdown_rag.config import Settings
from markdown_rag.ingest.pipeline import IngestPipeline
from markdown_rag.models import Chunk, SearchResult
from markdown_rag.retriever.search import SemanticSearch
from markdown_rag.store.chroma import ChromaStore

# ============================================================
# api/routes/search.py: _build_where_filter 분기 (39, 41, 45-47)
# ============================================================


class TestApiBuildWhereFilter:
    """API _build_where_filter의 모든 분기를 테스트한다."""

    def test_doc_type_only(self) -> None:
        from markdown_rag.api.routes.search import _build_where_filter

        result = _build_where_filter(doc_type="rfc", language=None)
        assert result == {"doc_type": "rfc"}

    def test_language_only(self) -> None:
        from markdown_rag.api.routes.search import _build_where_filter

        result = _build_where_filter(doc_type=None, language="ko")
        assert result == {"language": "ko"}

    def test_both_filters(self) -> None:
        from markdown_rag.api.routes.search import _build_where_filter

        result = _build_where_filter(doc_type="rfc", language="en")
        assert result == {"$and": [{"doc_type": "rfc"}, {"language": "en"}]}

    def test_no_filters(self) -> None:
        from markdown_rag.api.routes.search import _build_where_filter

        result = _build_where_filter(doc_type=None, language=None)
        assert result is None


# ============================================================
# cli/search_cmd.py: _build_where_filter 분기 (21, 23, 27-29)
# ============================================================


class TestCliBuildWhereFilter:
    """CLI _build_where_filter의 모든 분기를 테스트한다."""

    def test_doc_type_only(self) -> None:
        from markdown_rag.cli.search_cmd import _build_where_filter

        args = argparse.Namespace(doc_type="ccie", language=None)
        result = _build_where_filter(args)
        assert result == {"doc_type": "ccie"}

    def test_language_only(self) -> None:
        from markdown_rag.cli.search_cmd import _build_where_filter

        args = argparse.Namespace(doc_type=None, language="ko")
        result = _build_where_filter(args)
        assert result == {"language": "ko"}

    def test_both_filters(self) -> None:
        from markdown_rag.cli.search_cmd import _build_where_filter

        args = argparse.Namespace(doc_type="telecom_manual", language="ko")
        result = _build_where_filter(args)
        assert result == {
            "$and": [{"doc_type": "telecom_manual"}, {"language": "ko"}]
        }

    def test_no_filters(self) -> None:
        from markdown_rag.cli.search_cmd import _build_where_filter

        args = argparse.Namespace()
        result = _build_where_filter(args)
        assert result is None


# ============================================================
# ingest/pipeline.py: _prepare_chunks 에러 캡처 (152-155)
# ============================================================


class TestPipelineChunkingError:
    """청킹 단계에서 에러가 발생해도 캡처되어야 한다."""

    def test_chunking_error_captured(self, tmp_path: Path) -> None:
        md_file = tmp_path / "doc.md"
        md_file.write_text("# Title\n\nContent")

        mock_embedding = MagicMock()
        mock_store = MagicMock()
        mock_store.delete_by_document.side_effect = RuntimeError("delete failed")

        settings = Settings(
            chroma_path=tmp_path / "chroma",
            collection_name="test",
            chunk_max_size=5000,
            bm25_index_path=tmp_path / "bm25.pkl",
        )

        pipeline = IngestPipeline(
            settings=settings,
            embedding_backend=mock_embedding,
            vector_store=mock_store,
        )

        result = pipeline.ingest(md_file)
        assert len(result.errors) >= 1
        assert any("delete failed" in err for err in result.errors)


# ============================================================
# retriever/bm25.py: kiwipiepy ImportError 폴백 (42-44)
# ============================================================


class TestBM25KiwiFallback:
    """kiwipiepy가 없을 때 공백 토큰화로 폴백되어야 한다."""

    def test_fallback_when_kiwipiepy_missing(self) -> None:
        from markdown_rag.retriever.bm25 import _tokenize_korean

        with patch.dict("sys.modules", {"kiwipiepy": None}):
            # ImportError 발생 시 공백 토큰화로 대체
            with patch(
                "markdown_rag.retriever.bm25._tokenize_simple",
                return_value=["snmp", "트랩"],
            ) as mock_simple:
                result = _tokenize_korean("SNMP 트랩")
                mock_simple.assert_called_once_with("SNMP 트랩")
                assert result == ["snmp", "트랩"]


# ============================================================
# retriever/bm25.py: _rebuild_index 빈 코퍼스 (80)
# ============================================================


class TestBM25RebuildEmpty:
    """빈 코퍼스로 인덱스를 재구축하면 None이 되어야 한다."""

    def test_rebuild_with_empty_corpus(self) -> None:
        from markdown_rag.retriever.bm25 import BM25Index

        index = BM25Index()
        index._rebuild_index()
        assert index._bm25 is None


# ============================================================
# retriever/reranker.py: _load_model 실제 로드 (38-41)
# ============================================================


class TestRerankerModelLoad:
    """크로스 인코더 모델 로드를 테스트한다."""

    def test_load_model_called_on_first_use(self) -> None:
        from markdown_rag.retriever.reranker import CrossEncoderReranker

        reranker = CrossEncoderReranker(model_name="test-model")

        mock_cross_encoder_cls = MagicMock()
        mock_model_instance = MagicMock()
        mock_cross_encoder_cls.return_value = mock_model_instance

        with patch(
            "markdown_rag.retriever.reranker.CrossEncoder",
            mock_cross_encoder_cls,
            create=True,
        ):
            # sentence_transformers 모듈 모킹
            import types

            mock_st = types.ModuleType("sentence_transformers")
            mock_st.CrossEncoder = mock_cross_encoder_cls
            with patch.dict("sys.modules", {"sentence_transformers": mock_st}):
                model = reranker._load_model()
                assert model is not None


# ============================================================
# retriever/search.py: reranker 활성화 분기 (75)
# ============================================================


class TestSemanticSearchWithReranker:
    """리랭커가 활성화된 SemanticSearch를 테스트한다."""

    def test_search_with_reranker(self) -> None:
        mock_embedding = MagicMock()
        mock_embedding.embed_query.return_value = [0.1, 0.2, 0.3]

        mock_store = MagicMock()
        initial_results = [
            SearchResult(
                chunk=Chunk(
                    content=f"doc {i}",
                    doc_path=Path("test.md"),
                    chunk_index=i,
                ),
                score=0.9 - i * 0.1,
                rank=i + 1,
            )
            for i in range(3)
        ]
        mock_store.search.return_value = initial_results

        mock_reranker = MagicMock()
        mock_reranker.rerank.return_value = [
            SearchResult(
                chunk=Chunk(
                    content="doc 2",
                    doc_path=Path("test.md"),
                    chunk_index=2,
                ),
                score=0.95,
                rank=1,
            ),
        ]

        engine = SemanticSearch(
            embedding_backend=mock_embedding,
            vector_store=mock_store,
            top_k=1,
            reranker=mock_reranker,
            initial_top_k=20,
        )

        # 한국어 쿼리: QueryAnalyzer가 자동 필터를 만들지 않으므로 where=None 그대로 전달
        results = engine.search("스패닝트리 설정")

        # 리랭커가 호출되어야 함
        mock_reranker.rerank.assert_called_once()
        # initial_top_k로 벡터 검색
        mock_store.search.assert_called_once_with(
            query_embedding=[0.1, 0.2, 0.3], top_k=20, where=None
        )
        assert len(results) == 1
        assert results[0].chunk.content == "doc 2"


# ============================================================
# store/chroma.py: get_adjacent_chunks 예외 처리 (216-217)
# ============================================================


class TestChromaAdjacentException:
    """get_adjacent_chunks에서 예외 발생 시 빈 리스트를 반환해야 한다."""

    def test_exception_returns_empty(self, tmp_path: Path) -> None:
        store = ChromaStore(
            persist_path=tmp_path / "exc_test",
            collection_name="exc_test",
        )
        # 컬렉션이 비어있어도 예외 없이 동작해야 함
        result = store.get_adjacent_chunks("nonexistent.md", chunk_index=0)
        assert result == []

    def test_collection_get_exception(self, tmp_path: Path) -> None:
        store = ChromaStore(
            persist_path=tmp_path / "exc_test2",
            collection_name="exc_test2",
        )
        # _collection.get 에서 예외 발생 시
        store._collection.get = MagicMock(side_effect=RuntimeError("db error"))
        result = store.get_adjacent_chunks("any.md", chunk_index=0)
        assert result == []
