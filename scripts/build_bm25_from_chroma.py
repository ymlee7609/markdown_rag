#!/usr/bin/env python3
# Chroma DB에서 청크를 읽어 BM25 인덱스만 재구축.
# Kiwi 싱글톤 적용 이후 전용. data/chroma_optimized는 건드리지 않음.
# 사용: python scripts/build_bm25_from_chroma.py

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "src"))

import chromadb  # noqa: E402

from markdown_rag.models import Chunk  # noqa: E402
from markdown_rag.retriever.bm25 import BM25Index, tokenize  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("build_bm25")


def fetch_chunks_from_chroma(
    chroma_path: Path,
    collection_name: str,
    batch_size: int = 5000,
) -> tuple[list[Chunk], int]:
    """Chroma DB에서 모든 청크를 배치로 가져온다."""
    client = chromadb.PersistentClient(path=str(chroma_path))
    collection = client.get_collection(collection_name)
    total = collection.count()
    logger.info("Chroma 컬렉션 '%s'에서 %d개 청크 발견", collection_name, total)

    chunks: list[Chunk] = []
    for offset in range(0, total, batch_size):
        res = collection.get(
            limit=batch_size,
            offset=offset,
            include=["documents", "metadatas"],
        )
        ids = res.get("ids") or []
        docs = res.get("documents") or []
        metas = res.get("metadatas") or []
        for cid, content, meta in zip(ids, docs, metas):
            if content is None:
                continue
            m = dict(meta) if meta else {}
            headers_raw = m.pop("headers", "")
            headers_str = headers_raw if isinstance(headers_raw, str) else ""
            headers = headers_str.split("|||") if headers_str else []
            doc_path_raw = m.pop("doc_path", cid)
            doc_path = Path(str(doc_path_raw))
            ci_raw = m.pop("chunk_index", 0)
            try:
                chunk_index = int(ci_raw)  # type: ignore[arg-type]
            except (TypeError, ValueError):
                chunk_index = 0
            chunks.append(Chunk(
                content=content,
                doc_path=doc_path,
                headers=headers,
                chunk_index=chunk_index,
                metadata=m,
            ))
        logger.info("fetched %d/%d", min(offset + batch_size, total), total)
    return chunks, total


def build_bm25_with_progress(
    chunks: list[Chunk],
    output_path: Path,
    log_every: int = 2000,
) -> None:
    """BM25Index 구축. add_chunks는 내부적으로 _rebuild_index를 1회만 호출."""
    index = BM25Index()
    t0 = time.time()
    total = len(chunks)

    # 토큰화는 add_chunks 내부에서 진행되지만, 진행률을 보려면 직접 반복
    # (BM25Index 내부 구조 재사용을 위해 미리 토큰화 후 마지막에 _rebuild_index)
    tokenized: list[list[str]] = []
    for i, chunk in enumerate(chunks, start=1):
        tokens = tokenize(chunk.content)
        tokenized.append(tokens)
        if i % log_every == 0 or i == total:
            elapsed = time.time() - t0
            rate = i / elapsed if elapsed > 0 else 0
            remain = (total - i) / rate if rate > 0 else 0
            logger.info(
                "tokenize %d/%d (%.1f%%) rate=%.1f ch/s eta=%.1fmin",
                i, total, i * 100 / total, rate, remain / 60,
            )

    # BM25Index 내부 필드에 직접 주입 (add_chunks 루프 재실행 방지)
    index._chunks = list(chunks)  # type: ignore[attr-defined]
    index._tokenized_corpus = tokenized  # type: ignore[attr-defined]

    logger.info("BM25Okapi IDF 계산 중... (시간 소요 가능)")
    t1 = time.time()
    index._rebuild_index()  # type: ignore[attr-defined]
    logger.info("BM25Okapi 구축 완료 (%.1fs)", time.time() - t1)

    logger.info("pickle 저장: %s", output_path)
    t2 = time.time()
    index.save(output_path)
    logger.info("저장 완료 (%.1fs, 파일 크기: %.1f MB)",
                time.time() - t2, output_path.stat().st_size / 1024 / 1024)


def main() -> None:
    parser = argparse.ArgumentParser(description="Chroma에서 BM25 인덱스만 재빌드")
    parser.add_argument("--chroma-path", default="data/chroma_optimized")
    parser.add_argument("--collection", default="markdown_docs_optimized")
    parser.add_argument("--output", default="data/bm25_index_optimized.pkl")
    parser.add_argument("--batch-size", type=int, default=5000)
    args = parser.parse_args()

    chroma_path = Path(args.chroma_path)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    if not chroma_path.exists():
        logger.error("Chroma 경로 없음: %s", chroma_path)
        sys.exit(1)

    t_total = time.time()
    logger.info("=== Phase 1: Chroma에서 청크 로드 ===")
    chunks, _total = fetch_chunks_from_chroma(chroma_path, args.collection, args.batch_size)
    logger.info("로드 완료: %d 청크 (%.1fs)", len(chunks), time.time() - t_total)

    if not chunks:
        logger.error("청크 없음. 종료.")
        sys.exit(1)

    logger.info("=== Phase 2: BM25 인덱스 빌드 ===")
    build_bm25_with_progress(chunks, output)

    logger.info("=== 완료 ===")
    logger.info("총 소요: %.1fmin", (time.time() - t_total) / 60)


if __name__ == "__main__":
    main()
