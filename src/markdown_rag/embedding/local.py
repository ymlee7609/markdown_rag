"""Local embedding backend using sentence-transformers."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# E5 모델 계열은 쿼리/문서에 접두사가 필요
_E5_MODEL_PREFIXES = ("e5-", "multilingual-e5-", "intfloat/e5-", "intfloat/multilingual-e5-")


def _is_e5_model(model_name: str) -> bool:
    """E5 모델 계열 여부를 판별한다."""
    name_lower = model_name.lower()
    return any(prefix in name_lower for prefix in _E5_MODEL_PREFIXES)


class LocalEmbedding:
    """Embedding backend using sentence-transformers models.

    Loads the model lazily on first use to avoid unnecessary
    startup cost when the backend is instantiated but not used.

    E5 모델 계열(intfloat/multilingual-e5-*)은 자동으로
    쿼리에 "query: ", 문서에 "passage: " 접두사를 추가한다.

    Args:
        model_name: Name of the sentence-transformers model.
            Defaults to 'intfloat/multilingual-e5-small' (384-dim, multilingual).
    """

    def __init__(self, model_name: str = "intfloat/multilingual-e5-small") -> None:
        self.model_name = model_name
        self._model: SentenceTransformer | None = None
        self._is_e5 = _is_e5_model(model_name)

    def _load_model(self) -> SentenceTransformer:
        """Load the sentence-transformers model on first use."""
        if self._model is None:
            import os
            import sys
            from contextlib import redirect_stderr

            logger.info("Loading sentence-transformers model: %s", self.model_name)
            # HuggingFace Hub 인증 경고 등 불필요한 출력 억제
            devnull = open(os.devnull, "w")  # noqa: SIM115
            old_stdout = sys.stdout
            try:
                sys.stdout = devnull
                with redirect_stderr(devnull):
                    from sentence_transformers import SentenceTransformer

                    self._model = SentenceTransformer(self.model_name)
            finally:
                sys.stdout = old_stdout
                devnull.close()
        return self._model

    def _encode(self, texts: list[str]) -> list[list[float]]:
        """텍스트 리스트를 임베딩 벡터로 인코딩한다 (접두사 처리 없음)."""
        model = self._load_model()
        embeddings = model.encode(texts, convert_to_numpy=True)
        return [emb.tolist() for emb in embeddings]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of texts into vectors.

        E5 모델의 경우 각 텍스트에 "passage: " 접두사를 자동 추가한다.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of embedding vectors, one per input text.
        """
        if not texts:
            return []

        # E5 모델은 문서에 "passage: " 접두사 필요
        if self._is_e5:
            texts = [f"passage: {t}" for t in texts]

        return self._encode(texts)

    def embed_query(self, query: str) -> list[float]:
        """Embed a single query text.

        E5 모델의 경우 "query: " 접두사를 자동 추가한다.

        Args:
            query: Query string to embed.

        Returns:
            Single embedding vector.
        """
        # E5 모델은 쿼리에 "query: " 접두사 필요
        effective_query = f"query: {query}" if self._is_e5 else query
        result = self._encode([effective_query])
        return result[0]
