#!/usr/bin/env python3
"""CCIE_Vol1 병합 후 RAG 인덱스 업데이트 스크립트.

1. ChromaDB에서 이전 CCIE_Vol1 청크 삭제
2. 새 병합 파일 인덱싱
3. BM25 인덱스 전체 재구축
"""
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# 프로젝트 루트를 기준으로 import
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markdown_rag.config import get_settings  # noqa: E402
from markdown_rag.ingest.pipeline import IngestPipeline  # noqa: E402
from markdown_rag.retriever.bm25 import BM25Index  # noqa: E402
from markdown_rag.store.chroma import ChromaStore  # noqa: E402


def main() -> None:
    settings = get_settings()
    store = ChromaStore(
        persist_path=settings.chroma_path,
        collection_name=settings.collection_name,
    )
    col = store._collection

    # 1단계: 이전 CCIE_Vol1 청크 삭제
    logger.info("=== 1단계: 이전 CCIE_Vol1 청크 삭제 ===")
    results = col.get(where={"doc_type": "ccie"}, include=["metadatas"])
    old_vol1_ids = [
        id_
        for id_, meta in zip(results["ids"], results["metadatas"])
        if "CCIE_Vol1" in meta.get("doc_path", "")
    ]
    if old_vol1_ids:
        # ChromaDB는 한 번에 최대 수천 개 삭제 가능, 배치로 처리
        batch_size = 5000
        for i in range(0, len(old_vol1_ids), batch_size):
            batch = old_vol1_ids[i : i + batch_size]
            col.delete(ids=batch)
            logger.info("  삭제: %d/%d", min(i + batch_size, len(old_vol1_ids)), len(old_vol1_ids))
        logger.info("  총 %d개 이전 청크 삭제 완료", len(old_vol1_ids))
    else:
        logger.info("  삭제할 이전 청크 없음")

    # 2단계: 새 CCIE_Vol1 파일 인덱싱
    logger.info("\n=== 2단계: 새 CCIE_Vol1 파일 인덱싱 ===")
    pipeline = IngestPipeline(settings=settings)
    vol1_path = Path("input/Cisco_CCIE/CCIE_Vol1")
    result = pipeline.ingest(vol1_path, verbose=True)
    logger.info("  문서 처리: %d개", result.documents_processed)
    logger.info("  청크 생성: %d개", result.chunks_created)
    if result.errors:
        for err in result.errors:
            logger.error("  오류: %s", err)

    # 3단계: BM25 인덱스 전체 재구축
    logger.info("\n=== 3단계: BM25 인덱스 전체 재구축 ===")
    all_data = col.get(include=["documents", "metadatas"])
    from markdown_rag.models import Chunk

    all_chunks = []
    for doc_text, meta in zip(all_data["documents"], all_data["metadatas"]):
        chunk = Chunk(
            content=doc_text or "",
            metadata=meta or {},
        )
        all_chunks.append(chunk)

    logger.info("  전체 청크 수: %d", len(all_chunks))
    bm25 = BM25Index()
    bm25.add_chunks(all_chunks)
    bm25.save(settings.bm25_index_path)
    logger.info("  BM25 인덱스 저장 완료: %s", settings.bm25_index_path)

    # 결과 확인
    final_count = col.count()
    logger.info("\n=== 완료 ===")
    logger.info("  ChromaDB 전체 청크: %d", final_count)


if __name__ == "__main__":
    main()
