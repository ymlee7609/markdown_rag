"""Document ingestion pipeline for Markdown RAG.

Orchestrates the full ingestion flow: scan -> chunk -> embed -> store.
Supports incremental indexing, batch embedding, and BM25 index building.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from markdown_rag.chunker.metadata import extract_frontmatter
from markdown_rag.chunker.splitter import split_markdown
from markdown_rag.config import Settings
from markdown_rag.embedding.local import LocalEmbedding
from markdown_rag.embedding.openai import OpenAIEmbedding
from markdown_rag.ingest.scanner import MarkdownScanner
from markdown_rag.models import Chunk, Document
from markdown_rag.retriever.bm25 import BM25Index
from markdown_rag.store.chroma import ChromaStore

logger = logging.getLogger(__name__)

# 경로 패턴 기반 문서 유형 감지 규칙
_DOC_TYPE_PATTERNS: list[tuple[str, str, str]] = [
    # (경로에 포함되어야 할 문자열, doc_type, language)
    ("IETF_RFC", "rfc", "en"),
    ("Cisco_CCIE", "ccie", "en"),
    ("가입자망장비_manual", "telecom_manual", "ko"),
]

# 배치 처리 설정
_EMBED_BATCH_SIZE = 128
_STORE_BATCH_SIZE = 500


def detect_doc_metadata(doc_path: Path) -> dict[str, str]:
    """문서 경로에서 doc_type과 language를 자동 추론한다.

    Args:
        doc_path: 문서 파일 경로.

    Returns:
        doc_type, language 키를 포함하는 메타데이터 딕셔너리.
    """
    path_str = str(doc_path)
    for pattern, doc_type, language in _DOC_TYPE_PATTERNS:
        if pattern in path_str:
            return {"doc_type": doc_type, "language": language}
    return {"doc_type": "unknown", "language": "en"}


@dataclass
class IngestResult:
    """Result summary from an ingestion run.

    Attributes:
        documents_processed: Number of documents successfully processed.
        chunks_created: Total number of chunks created across all documents.
        errors: List of error messages for any failures encountered.
    """

    documents_processed: int
    chunks_created: int
    errors: list[str] = field(default_factory=list)


class IngestPipeline:
    """Orchestrates the document ingestion pipeline.

    Scans for Markdown files, splits them into chunks,
    generates embeddings, and stores them in a vector store.

    Supports:
    - Incremental indexing (re-ingest deletes old chunks)
    - Batch embedding for throughput optimization
    - BM25 index building for hybrid search

    Args:
        settings: Application settings for chunk size, overlap, etc.
        embedding_backend: Embedding backend instance.
            If None, creates one based on settings.embedding_backend.
        vector_store: Vector store instance.
            If None, creates a ChromaStore from settings.
    """

    def __init__(
        self,
        settings: Settings,
        embedding_backend: object | None = None,
        vector_store: object | None = None,
    ) -> None:
        self._settings = settings
        self._scanner = MarkdownScanner()

        # Initialize embedding backend
        if embedding_backend is not None:
            self._embedding_backend = embedding_backend
        elif settings.embedding_backend == "openai":
            self._embedding_backend = OpenAIEmbedding(
                model_name=settings.openai_embedding_model
            )
        else:
            self._embedding_backend = LocalEmbedding(
                model_name=settings.local_model
            )

        # Initialize vector store
        if vector_store is not None:
            self._vector_store = vector_store
        else:
            self._vector_store = ChromaStore(
                persist_path=settings.chroma_path,
                collection_name=settings.collection_name,
            )

    def ingest(self, path: Path, verbose: bool = False) -> IngestResult:
        """Ingest Markdown documents from a file or directory.

        Scans the path for Markdown files, then processes each document
        through the chunking, embedding, and storage pipeline.
        배치 처리로 임베딩 생성과 벡터 스토어 저장을 최적화한다.

        Args:
            path: Path to a single .md file or a directory to scan.
            verbose: If True, log detailed progress information.

        Returns:
            IngestResult with processing statistics.

        Raises:
            FileNotFoundError: If the path does not exist.
        """
        documents = self._scanner.scan(path)

        total_chunks = 0
        errors: list[str] = []

        # 모든 문서의 청크를 배치로 수집
        all_chunks: list[Chunk] = []
        bm25_index = BM25Index()

        for doc in documents:
            try:
                chunks = self._prepare_chunks(doc)
                all_chunks.extend(chunks)
                if verbose:
                    logger.info(
                        "Chunked %s: %d chunks", doc.path, len(chunks)
                    )
            except Exception as exc:
                error_msg = f"Error processing {doc.path}: {exc}"
                logger.error(error_msg)
                errors.append(error_msg)

        # 배치 임베딩 + 저장
        if all_chunks:
            try:
                total_chunks = self._batch_embed_and_store(all_chunks)
            except Exception as exc:
                error_msg = f"Error during batch embedding/storage: {exc}"
                logger.error(error_msg)
                errors.append(error_msg)
            else:
                # BM25 인덱스 구축 (임베딩 성공 시에만)
                bm25_index.add_chunks(all_chunks)
                bm25_index.save(self._settings.bm25_index_path)

        result = IngestResult(
            documents_processed=len(documents),
            chunks_created=total_chunks,
            errors=errors,
        )

        logger.info(
            "Ingestion complete: %d documents, %d chunks, %d errors",
            result.documents_processed,
            result.chunks_created,
            len(result.errors),
        )

        return result

    def _prepare_chunks(self, doc: Document) -> list[Chunk]:
        """문서를 청크로 분할하고 메타데이터를 추가한다 (임베딩 없이).

        Args:
            doc: 처리할 문서.

        Returns:
            메타데이터가 포함된 Chunk 리스트.
        """
        # 기존 청크 삭제 (증분 인덱싱)
        self._vector_store.delete_by_document(str(doc.path))

        # 프론트매터 추출
        fm_metadata, _body = extract_frontmatter(doc.content)
        base_metadata = {**doc.metadata, **fm_metadata}

        # 문서 유형/언어 자동 추론
        doc_meta = detect_doc_metadata(doc.path)
        base_metadata.update(doc_meta)

        # 구조 인식 청킹
        chunks = split_markdown(
            content=doc.content,
            doc_path=doc.path,
            max_chunk_size=self._settings.chunk_max_size,
            overlap=self._settings.chunk_overlap,
            metadata=base_metadata,
        )

        return chunks

    def _batch_embed_and_store(self, chunks: list[Chunk]) -> int:
        """청크를 배치로 임베딩하고 벡터 스토어에 저장한다.

        Args:
            chunks: 임베딩할 청크 리스트.

        Returns:
            저장된 청크 수.
        """
        texts = [chunk.content for chunk in chunks]
        all_embeddings: list[list[float]] = []

        # 배치 단위로 임베딩 생성
        for i in range(0, len(texts), _EMBED_BATCH_SIZE):
            batch = texts[i : i + _EMBED_BATCH_SIZE]
            embeddings = self._embedding_backend.embed_texts(batch)
            all_embeddings.extend(embeddings)
            logger.debug(
                "Embedded batch %d-%d of %d",
                i, min(i + _EMBED_BATCH_SIZE, len(texts)), len(texts),
            )

        # 배치 단위로 벡터 스토어에 저장
        for i in range(0, len(chunks), _STORE_BATCH_SIZE):
            batch_chunks = chunks[i : i + _STORE_BATCH_SIZE]
            batch_embeddings = all_embeddings[i : i + _STORE_BATCH_SIZE]
            self._vector_store.add_chunks(batch_chunks, batch_embeddings)

        logger.info("Batch stored %d chunks", len(chunks))
        return len(chunks)

    def ingest_document(self, doc: Document) -> int:
        """Process a single document through the ingestion pipeline.

        하위 호환성을 위해 유지. 단일 문서 처리 시 사용.

        Args:
            doc: Document to process.

        Returns:
            Number of chunks created.
        """
        chunks = self._prepare_chunks(doc)

        if not chunks:
            logger.debug("No chunks produced for %s", doc.path)
            return 0

        return self._batch_embed_and_store(chunks)
