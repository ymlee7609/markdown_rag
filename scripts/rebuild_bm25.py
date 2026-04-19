#!/usr/bin/env python3
"""ChromaDB 전체 청크로부터 BM25 인덱스를 재구축한다.

메모리 효율을 위해:
1. 배치 단위로 ChromaDB에서 청크 로드
2. Kiwi 인스턴스를 전역으로 1회만 생성 (이전: 매 호출마다 재생성)
3. 토큰만 누적한 뒤 마지막에 BM25Okapi를 단 한 번 구축
4. 각 배치 후 명시적 가비지 컬렉션
"""
from __future__ import annotations

import gc
import logging
import re
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markdown_rag.config import get_settings  # noqa: E402
from markdown_rag.models import Chunk  # noqa: E402
from markdown_rag.retriever.bm25 import BM25Index  # noqa: E402
from markdown_rag.store.chroma import ChromaStore  # noqa: E402

BATCH_SIZE = 5000  # ChromaDB 쿼리 제한 및 메모리 여유 확보
KOREAN_RE = re.compile(r"[\uac00-\ud7af]")

# Kiwi 전역 싱글톤 (대량 토큰화 시 메모리 및 CPU 절감)
_KIWI = None


def _get_kiwi():
    global _KIWI
    if _KIWI is None:
        from kiwipiepy import Kiwi
        _KIWI = Kiwi()
    return _KIWI


def fast_tokenize(text: str) -> list[str]:
    """한국어 포함 시 Kiwi 싱글톤 사용, 영문은 공백 분할."""
    if KOREAN_RE.search(text):
        kiwi = _get_kiwi()
        tokens = kiwi.tokenize(text)
        return [t.form.lower() for t in tokens if len(t.form) > 1]
    return text.lower().split()


def main() -> None:
    settings = get_settings()
    store = ChromaStore(
        persist_path=settings.chroma_path,
        collection_name=settings.collection_name,
    )
    col = store._collection

    total = col.count()
    logger.info("ChromaDB 전체 청크 수: %d", total)

    bm25 = BM25Index()

    offset = 0
    progress_interval = 50000
    next_progress = progress_interval
    while offset < total:
        batch_limit = min(BATCH_SIZE, total - offset)
        results = col.get(
            limit=batch_limit,
            offset=offset,
            include=["documents", "metadatas"],
        )

        docs = results["documents"] or []
        metas = results["metadatas"] or []

        for doc_text, meta in zip(docs, metas):
            meta = meta or {}
            headers_raw = meta.get("headers", "")
            headers = [headers_raw] if headers_raw else []
            chunk = Chunk(
                content=doc_text or "",
                doc_path=Path(meta.get("doc_path", "")),
                headers=headers,
                chunk_index=int(meta.get("chunk_index", 0)),
                metadata=meta,
            )
            tokens = fast_tokenize(chunk.content)
            bm25._chunks.append(chunk)
            bm25._tokenized_corpus.append(tokens)

        offset += batch_limit

        if offset >= next_progress or offset >= total:
            logger.info("진행: %d/%d", offset, total)
            next_progress += progress_interval
            gc.collect()

    logger.info("토큰화 완료: %d 청크", len(bm25._chunks))

    logger.info("BM25Okapi 인덱스 구축 중...")
    bm25._rebuild_index()
    logger.info("BM25Okapi 인덱스 구축 완료")

    bm25.save(settings.bm25_index_path)
    logger.info("저장 완료: %s", settings.bm25_index_path)


if __name__ == "__main__":
    main()
