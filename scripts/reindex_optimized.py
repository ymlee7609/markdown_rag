#!/usr/bin/env python3
# input_optimized/ 를 새 Chroma 경로에 저부하로 인덱싱.
# 원본 data/chroma 는 보존하여 rollback 가능.

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path

# CPU 부하 제어: sentence-transformers 로딩 전에 설정해야 유효
# 아래 값은 main()에서 --threads 인자로 덮어쓸 수 있다
_DEFAULT_THREADS = "2"
os.environ.setdefault("OMP_NUM_THREADS", _DEFAULT_THREADS)
os.environ.setdefault("MKL_NUM_THREADS", _DEFAULT_THREADS)
os.environ.setdefault("OPENBLAS_NUM_THREADS", _DEFAULT_THREADS)
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", _DEFAULT_THREADS)
os.environ.setdefault("NUMEXPR_NUM_THREADS", _DEFAULT_THREADS)
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

_PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "src"))

# Pipeline 모듈의 배치 상수를 덮어쓰기 위해 먼저 import
import markdown_rag.ingest.pipeline as pipeline_mod  # noqa: E402
from markdown_rag.config import Settings  # noqa: E402
from markdown_rag.ingest.pipeline import IngestPipeline  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("reindex_optimized")


def set_torch_threads(n: int) -> None:
    """PyTorch CPU 스레드 수를 런타임에 제한한다."""
    try:
        import torch  # type: ignore[import-not-found]
        torch.set_num_threads(n)
        torch.set_num_interop_threads(max(1, n // 2))
        logger.info("torch threads set to %d (interop=%d)", n, max(1, n // 2))
    except ImportError:
        logger.warning("torch not available; skipping thread tuning")


def main() -> None:
    parser = argparse.ArgumentParser(description="저부하 재인덱싱 래퍼")
    parser.add_argument("--input", default="input_optimized")
    parser.add_argument("--chroma-path", default="data/chroma_optimized")
    parser.add_argument("--collection", default="markdown_docs_optimized")
    parser.add_argument("--bm25-path", default="data/bm25_index_optimized.pkl")
    parser.add_argument("--embed-batch", type=int, default=32,
                        help="임베딩 배치 사이즈 (기본 128 → 32)")
    parser.add_argument("--store-batch", type=int, default=200,
                        help="벡터 스토어 배치 사이즈 (기본 500 → 200)")
    parser.add_argument("--threads", type=int, default=2,
                        help="CPU 스레드 수 제한 (기본 2)")
    parser.add_argument("--sleep-ms", type=int, default=0,
                        help="배치 사이 sleep(ms), 추가 부하 경감용")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    # 스레드 제한 재적용 (env var는 이미 적용됨)
    for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ[var] = str(args.threads)
    set_torch_threads(args.threads)

    # Pipeline 상수 덮어쓰기
    pipeline_mod._EMBED_BATCH_SIZE = args.embed_batch  # type: ignore[attr-defined]
    pipeline_mod._STORE_BATCH_SIZE = args.store_batch  # type: ignore[attr-defined]
    logger.info(
        "batch sizes: embed=%d store=%d", args.embed_batch, args.store_batch,
    )

    # 메모리 효율을 위해 embed→store 인터리브 방식으로 교체.
    # 원본은 모든 임베딩을 메모리에 누적한 뒤 일괄 저장하여 peak 메모리가
    # (청크 수 × 384차원 × 4바이트) 만큼 커진다. 400K 청크면 약 600MB.
    # 인터리브 방식은 store_batch 단위로 embed→store→free를 반복해 peak ~수 MB.
    sleep_sec = max(args.sleep_ms, 0) / 1000.0

    def interleaved(self, chunks):  # type: ignore[no-redef]
        """embed→store 인터리빙으로 peak 메모리 최소화 + 진행률 로깅."""
        total = len(chunks)
        if total == 0:
            return 0
        embed_batch = pipeline_mod._EMBED_BATCH_SIZE
        store_batch = pipeline_mod._STORE_BATCH_SIZE
        stored = 0
        t_start = time.time()
        for s_start in range(0, total, store_batch):
            bucket = chunks[s_start:s_start + store_batch]
            texts = [c.content for c in bucket]
            embeddings: list[list[float]] = []
            for i in range(0, len(texts), embed_batch):
                batch = texts[i:i + embed_batch]
                embeddings.extend(self._embedding_backend.embed_texts(batch))
                if sleep_sec > 0:
                    time.sleep(sleep_sec)
            self._vector_store.add_chunks(bucket, embeddings)
            stored += len(bucket)
            # 메모리 해제 힌트
            del embeddings
            del texts
            # 진행률 로그 (매 버킷)
            elapsed = time.time() - t_start
            rate = stored / elapsed if elapsed > 0 else 0.0
            remain = (total - stored) / rate if rate > 0 else 0.0
            logger.info(
                "stored %d/%d (%.1f%%) rate=%.1f ch/s eta=%.1fmin",
                stored, total, stored * 100 / total, rate, remain / 60,
            )
        return stored

    pipeline_mod.IngestPipeline._batch_embed_and_store = interleaved  # type: ignore[assignment]
    logger.info("interleaved embed→store mode enabled (memory-efficient)")

    # 새 Chroma 경로 + BM25 경로로 설정
    settings = Settings(
        chroma_path=Path(args.chroma_path),
        collection_name=args.collection,
        bm25_index_path=Path(args.bm25_path),
    )
    logger.info("chroma_path=%s collection=%s", settings.chroma_path, settings.collection_name)
    logger.info("bm25_path=%s", settings.bm25_index_path)

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        logger.error("input path not found: %s", input_path)
        sys.exit(1)

    logger.info("ingesting from %s", input_path)
    t0 = time.time()
    pipeline = IngestPipeline(settings=settings)
    result = pipeline.ingest(input_path, verbose=args.verbose)
    elapsed = time.time() - t0

    logger.info("=" * 60)
    logger.info("완료: %d docs, %d chunks, %d errors, %.1fs (%.1f min)",
                result.documents_processed, result.chunks_created,
                len(result.errors), elapsed, elapsed / 60)
    if result.errors:
        logger.warning("첫 5개 에러:")
        for e in result.errors[:5]:
            logger.warning("  - %s", e)


if __name__ == "__main__":
    main()
