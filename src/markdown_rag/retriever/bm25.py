"""BM25 키워드 검색 엔진.

한국어 형태소 분석(kiwipiepy)과 영어 공백 토큰화를 지원하는
BM25 기반 키워드 검색을 제공한다.
"""

from __future__ import annotations

import logging
import pickle
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

from markdown_rag.models import Chunk, SearchResult

logger = logging.getLogger(__name__)

# 한국어 문자 범위 정규식
_KOREAN_PATTERN = re.compile(r"[\uac00-\ud7af]")


def _has_korean(text: str) -> bool:
    """텍스트에 한국어가 포함되어 있는지 확인한다."""
    return bool(_KOREAN_PATTERN.search(text))


def _tokenize_simple(text: str) -> list[str]:
    """공백 기반 간단한 토큰화 (영어/일반 텍스트용)."""
    return text.lower().split()


def _tokenize_korean(text: str) -> list[str]:
    """kiwipiepy를 이용한 한국어 형태소 분석 토큰화."""
    try:
        from kiwipiepy import Kiwi

        kiwi = Kiwi()
        tokens = kiwi.tokenize(text)
        return [t.form.lower() for t in tokens if len(t.form) > 1]
    except ImportError:
        logger.warning("kiwipiepy가 설치되지 않아 공백 토큰화로 대체합니다.")
        return _tokenize_simple(text)


def tokenize(text: str) -> list[str]:
    """텍스트를 토큰화한다. 한국어 포함 시 형태소 분석, 아니면 공백 분할."""
    if _has_korean(text):
        return _tokenize_korean(text)
    return _tokenize_simple(text)


class BM25Index:
    """BM25 인덱스. 청크 리스트와 토큰화된 코퍼스를 관리한다."""

    def __init__(self) -> None:
        self._chunks: list[Chunk] = []
        self._tokenized_corpus: list[list[str]] = []
        self._bm25: BM25Okapi | None = None

    @property
    def size(self) -> int:
        """인덱스에 저장된 청크 수."""
        return len(self._chunks)

    def add_chunks(self, chunks: list[Chunk]) -> None:
        """청크를 인덱스에 추가한다."""
        for chunk in chunks:
            tokens = tokenize(chunk.content)
            self._chunks.append(chunk)
            self._tokenized_corpus.append(tokens)
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        """BM25 인덱스를 재구축한다."""
        if self._tokenized_corpus:
            self._bm25 = BM25Okapi(self._tokenized_corpus)
        else:
            self._bm25 = None

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        """BM25 점수 기반으로 청크를 검색한다.

        Args:
            query: 검색 쿼리 문자열.
            top_k: 반환할 최대 결과 수.

        Returns:
            BM25 점수 기준 내림차순 정렬된 SearchResult 리스트.
        """
        if self._bm25 is None or not self._chunks:
            return []

        query_tokens = tokenize(query)
        scores = self._bm25.get_scores(query_tokens)

        # 상위 top_k 인덱스 추출
        scored_indices = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )[:top_k]

        results: list[SearchResult] = []
        for rank, idx in enumerate(scored_indices, start=1):
            if scores[idx] <= 0:
                break
            results.append(
                SearchResult(
                    chunk=self._chunks[idx],
                    score=float(scores[idx]),
                    rank=rank,
                )
            )

        return results

    def save(self, path: Path) -> None:
        """인덱스를 파일로 저장한다."""
        data = {
            "chunks": self._chunks,
            "tokenized_corpus": self._tokenized_corpus,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(data, f)
        logger.info("BM25 인덱스 저장: %s (%d 청크)", path, len(self._chunks))

    @classmethod
    def load(cls, path: Path) -> BM25Index:
        """파일에서 인덱스를 로드한다."""
        index = cls()
        with open(path, "rb") as f:
            data = pickle.load(f)  # noqa: S301
        index._chunks = data["chunks"]
        index._tokenized_corpus = data["tokenized_corpus"]
        index._rebuild_index()
        logger.info("BM25 인덱스 로드: %s (%d 청크)", path, len(index._chunks))
        return index

    def clear(self) -> None:
        """인덱스를 초기화한다."""
        self._chunks.clear()
        self._tokenized_corpus.clear()
        self._bm25 = None
