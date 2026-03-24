"""Tests for ChromaStore metadata filtering."""

from __future__ import annotations

from pathlib import Path

import pytest

from markdown_rag.models import Chunk
from markdown_rag.store.chroma import ChromaStore


@pytest.fixture
def chroma_store(tmp_path: Path) -> ChromaStore:
    """Create a ChromaStore instance with temporary storage."""
    return ChromaStore(
        persist_path=tmp_path / "chroma_filter_test",
        collection_name="filter_test",
    )


@pytest.fixture
def mixed_chunks() -> list[Chunk]:
    """문서 유형과 언어가 다른 청크들을 생성한다."""
    return [
        Chunk(
            content="RFC 9110 defines HTTP semantics.",
            doc_path=Path("input/IETF_RFC/rfc9110.md"),
            headers=["HTTP", "Semantics"],
            chunk_index=0,
            metadata={"doc_type": "rfc", "language": "en"},
        ),
        Chunk(
            content="BGP is a routing protocol.",
            doc_path=Path("input/Cisco_CCIE/CCIE_Vol1/bgp.md"),
            headers=["Routing", "BGP"],
            chunk_index=0,
            metadata={"doc_type": "ccie", "language": "en"},
        ),
        Chunk(
            content="SNMP 트랩 설정 방법을 설명합니다.",
            doc_path=Path("input/가입자망장비_manual/다산_L2/snmp.md"),
            headers=["SNMP", "트랩 설정"],
            chunk_index=0,
            metadata={"doc_type": "telecom_manual", "language": "ko"},
        ),
    ]


@pytest.fixture
def mixed_embeddings() -> list[list[float]]:
    """테스트용 임베딩 벡터."""
    return [
        [0.1] * 384,
        [0.2] * 384,
        [0.3] * 384,
    ]


class TestChromaStoreMetadataStorage:
    """Test that extended metadata is stored correctly."""

    def test_stores_doc_type_metadata(
        self,
        chroma_store: ChromaStore,
        mixed_chunks: list[Chunk],
        mixed_embeddings: list[list[float]],
    ) -> None:
        """doc_type 메타데이터가 저장되어야 한다."""
        chroma_store.add_chunks(mixed_chunks, mixed_embeddings)
        assert chroma_store.count() == 3

    def test_chunks_without_metadata_still_work(
        self, chroma_store: ChromaStore
    ) -> None:
        """메타데이터가 없는 청크도 정상 동작해야 한다."""
        chunk = Chunk(
            content="No metadata chunk",
            doc_path=Path("test.md"),
            chunk_index=0,
        )
        chroma_store.add_chunks([chunk], [[0.5] * 384])
        assert chroma_store.count() == 1


class TestChromaStoreFilterSearch:
    """Test metadata filter search functionality."""

    @pytest.fixture(autouse=True)
    def setup_store(
        self,
        chroma_store: ChromaStore,
        mixed_chunks: list[Chunk],
        mixed_embeddings: list[list[float]],
    ) -> None:
        """모든 테스트에 공통 데이터를 미리 저장한다."""
        self.store = chroma_store
        chroma_store.add_chunks(mixed_chunks, mixed_embeddings)

    def test_filter_by_doc_type(self) -> None:
        """doc_type 필터로 검색하면 해당 유형의 결과만 반환되어야 한다."""
        results = self.store.search(
            [0.1] * 384, top_k=10, where={"doc_type": "rfc"}
        )
        assert len(results) == 1
        assert results[0].chunk.content == "RFC 9110 defines HTTP semantics."

    def test_filter_by_language(self) -> None:
        """language 필터로 검색하면 해당 언어의 결과만 반환되어야 한다."""
        results = self.store.search(
            [0.3] * 384, top_k=10, where={"language": "ko"}
        )
        assert len(results) == 1
        assert "SNMP" in results[0].chunk.content

    def test_filter_by_doc_type_and_language(self) -> None:
        """복합 필터가 올바르게 동작해야 한다."""
        results = self.store.search(
            [0.2] * 384,
            top_k=10,
            where={"$and": [{"doc_type": "ccie"}, {"language": "en"}]},
        )
        assert len(results) == 1
        assert "BGP" in results[0].chunk.content

    def test_no_filter_returns_all(self) -> None:
        """필터 없이 검색하면 모든 결과가 반환되어야 한다."""
        results = self.store.search([0.1] * 384, top_k=10, where=None)
        assert len(results) == 3

    def test_filter_with_no_match(self) -> None:
        """일치하는 결과가 없으면 빈 리스트를 반환해야 한다."""
        results = self.store.search(
            [0.1] * 384, top_k=10, where={"doc_type": "nonexistent"}
        )
        assert results == []
