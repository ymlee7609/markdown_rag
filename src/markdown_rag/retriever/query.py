"""쿼리 전처리 모듈 - HyDE (Hypothetical Document Embeddings).

LLM이 가상의 답변 문서를 생성하고, 그 임베딩을 사용하여
검색 정확도를 향상시킨다.
"""

from __future__ import annotations

import logging

from markdown_rag.embedding.base import EmbeddingBackend
from markdown_rag.llm.base import LLMBackend

logger = logging.getLogger(__name__)

_HYDE_PROMPT = (
    "Please write a short paragraph that would be a good answer to the "
    "following question. Write it as if it were a passage from a technical "
    "document. Do not include any preamble, just the passage.\n\n"
    "Question: {query}"
)


class HyDEProcessor:
    """HyDE (Hypothetical Document Embeddings) 쿼리 프로세서.

    LLM으로 가상 답변을 생성한 뒤, 그 텍스트를 임베딩하여
    원본 쿼리 임베딩 대신 사용한다. 이를 통해 쿼리-문서 간
    임베딩 공간 불일치를 줄인다.

    Args:
        llm_backend: 가상 답변 생성에 사용할 LLM 백엔드.
        embedding_backend: 가상 답변을 임베딩할 백엔드.
    """

    def __init__(
        self,
        llm_backend: LLMBackend,
        embedding_backend: EmbeddingBackend,
    ) -> None:
        self.llm_backend = llm_backend
        self.embedding_backend = embedding_backend

    def generate_hyde_embedding(self, query: str) -> list[float]:
        """쿼리에 대한 HyDE 임베딩을 생성한다.

        Args:
            query: 원본 사용자 쿼리.

        Returns:
            가상 답변의 임베딩 벡터.
        """
        # LLM으로 가상 답변 생성
        prompt = _HYDE_PROMPT.format(query=query)
        messages = [{"role": "user", "content": prompt}]
        hypothetical_doc = self.llm_backend.generate(messages)

        logger.debug("HyDE generated document: %s...", hypothetical_doc[:100])

        # 가상 답변을 임베딩
        return self.embedding_backend.embed_query(hypothetical_doc)
