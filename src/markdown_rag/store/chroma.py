"""ChromaDB vector store implementation."""

from __future__ import annotations

import logging
from pathlib import Path

import chromadb

from markdown_rag.models import Chunk, SearchResult

logger = logging.getLogger(__name__)


class ChromaStore:
    """Vector store backed by ChromaDB with file-based persistence.

    Stores chunk content, embeddings, and metadata (headers, doc_path,
    chunk_index, doc_type, language) in a ChromaDB collection.

    Args:
        persist_path: Directory path for ChromaDB persistent storage.
        collection_name: Name of the ChromaDB collection.
            Defaults to 'markdown_docs'.
    """

    def __init__(
        self,
        persist_path: Path | str,
        collection_name: str = "markdown_docs",
    ) -> None:
        self.persist_path = Path(persist_path)
        self.collection_name = collection_name

        # Ensure persistence directory exists
        self.persist_path.mkdir(parents=True, exist_ok=True)

        self._client = chromadb.PersistentClient(path=str(self.persist_path))
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            "ChromaStore initialized: path=%s, collection=%s",
            self.persist_path,
            self.collection_name,
        )

    def add_chunks(
        self, chunks: list[Chunk], embeddings: list[list[float]]
    ) -> None:
        """Add chunks with their embeddings to the store.

        메타데이터에 doc_path, headers, chunk_index 외에
        doc_type, language 등 확장 메타데이터도 저장한다.

        Args:
            chunks: List of Chunk objects to store.
            embeddings: List of embedding vectors, one per chunk.

        Raises:
            ValueError: If chunks and embeddings have different lengths.
        """
        if len(chunks) != len(embeddings):
            msg = (
                f"Chunks and embeddings must have the same length. "
                f"Got {len(chunks)} chunks and {len(embeddings)} embeddings."
            )
            raise ValueError(msg)

        if not chunks:
            return

        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = []
        for chunk in chunks:
            meta = {
                "doc_path": str(chunk.doc_path),
                "headers": "|||".join(chunk.headers),
                "chunk_index": chunk.chunk_index,
            }
            # 확장 메타데이터 (doc_type, language 등)
            for key in ("doc_type", "language"):
                if key in chunk.metadata:
                    meta[key] = chunk.metadata[key]
            metadatas.append(meta)

        self._collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )
        logger.info("Added %d chunks to collection '%s'", len(chunks), self.collection_name)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        """Search for similar chunks by query embedding.

        Args:
            query_embedding: Query vector to search with.
            top_k: Maximum number of results to return.
            where: Optional ChromaDB metadata filter.
                예: {"doc_type": "rfc"} 또는
                {"$and": [{"doc_type": "telecom_manual"}, {"language": "ko"}]}

        Returns:
            List of SearchResult objects sorted by score (highest first).
        """
        total = self._collection.count()
        if total == 0:
            return []

        # Limit top_k to available items
        effective_k = min(top_k, total)

        query_kwargs: dict = {
            "query_embeddings": [query_embedding],
            "n_results": effective_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where is not None:
            query_kwargs["where"] = where

        results = self._collection.query(**query_kwargs)

        search_results: list[SearchResult] = []
        if not results["ids"] or not results["ids"][0]:
            return []

        for i, _chunk_id in enumerate(results["ids"][0]):
            metadata = results["metadatas"][0][i]
            content = results["documents"][0][i]
            distance = results["distances"][0][i]

            # ChromaDB cosine distance: 0 = identical, 2 = opposite
            # Convert to similarity score: 1 - (distance / 2)
            score = 1.0 - (distance / 2.0)

            headers_str = metadata.get("headers", "")
            headers = headers_str.split("|||") if headers_str else []

            chunk = Chunk(
                content=content,
                doc_path=Path(metadata["doc_path"]),
                headers=headers,
                chunk_index=int(metadata["chunk_index"]),
            )

            search_results.append(SearchResult(chunk=chunk, score=score))

        # Sort by score descending
        search_results.sort(key=lambda r: r.score, reverse=True)

        # Assign ranks
        for i, result in enumerate(search_results):
            result.rank = i + 1

        return search_results

    def delete_by_document(self, doc_path: str) -> int:
        """Delete all chunks from a specific document.

        Args:
            doc_path: Document path to match against stored chunks.

        Returns:
            Number of chunks deleted.
        """
        # Query for matching document chunks
        try:
            existing = self._collection.get(
                where={"doc_path": doc_path},
                include=[],
            )
        except Exception:
            # ChromaDB may raise if collection is empty or filter finds nothing
            return 0

        if not existing["ids"]:
            return 0

        count = len(existing["ids"])
        self._collection.delete(ids=existing["ids"])
        logger.info(
            "Deleted %d chunks for document '%s'", count, doc_path
        )
        return count

    def get_adjacent_chunks(
        self,
        doc_path: str,
        chunk_index: int,
        window: int = 1,
    ) -> list[Chunk]:
        """동일 문서의 인접 청크를 반환한다.

        Args:
            doc_path: 문서 경로.
            chunk_index: 기준 청크 인덱스.
            window: 앞뒤로 가져올 청크 수.

        Returns:
            인접 청크 리스트 (chunk_index 순 정렬).
        """
        try:
            existing = self._collection.get(
                where={"doc_path": doc_path},
                include=["documents", "metadatas"],
            )
        except Exception:
            return []

        if not existing["ids"]:
            return []

        adjacent: list[Chunk] = []
        for i, _id in enumerate(existing["ids"]):
            meta = existing["metadatas"][i]
            idx = int(meta["chunk_index"])
            if idx == chunk_index:
                continue
            if abs(idx - chunk_index) <= window:
                headers_str = meta.get("headers", "")
                headers = headers_str.split("|||") if headers_str else []
                adjacent.append(
                    Chunk(
                        content=existing["documents"][i],
                        doc_path=Path(meta["doc_path"]),
                        headers=headers,
                        chunk_index=idx,
                    )
                )

        adjacent.sort(key=lambda c: c.chunk_index)
        return adjacent

    def count(self) -> int:
        """Return total number of stored chunks.

        Returns:
            Total chunk count in the collection.
        """
        return self._collection.count()

    def clear(self) -> None:
        """Remove all data from the store.

        Deletes and recreates the collection.
        """
        self._client.delete_collection(self.collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("Cleared collection '%s'", self.collection_name)
