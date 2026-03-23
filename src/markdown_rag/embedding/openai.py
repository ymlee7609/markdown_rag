"""OpenAI embedding backend using the openai library."""

from __future__ import annotations

import logging
import os

import openai as openai_module

logger = logging.getLogger(__name__)


class OpenAIEmbedding:
    """Embedding backend using OpenAI's embedding API.

    Requires the OPENAI_API_KEY environment variable or an explicit
    api_key parameter.

    Args:
        model_name: OpenAI embedding model name.
            Defaults to 'text-embedding-3-small'.
        api_key: Optional explicit API key. If not provided,
            reads from OPENAI_API_KEY environment variable.

    Raises:
        ValueError: If no API key is available.
    """

    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
        api_key: str | None = None,
    ) -> None:
        self.model_name = model_name
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")

        if not self._api_key:
            msg = (
                "OPENAI_API_KEY environment variable is not set. "
                "Please set it or provide an explicit api_key parameter."
            )
            raise ValueError(msg)

        self._client = openai_module.OpenAI(api_key=self._api_key)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of texts using OpenAI's embedding API.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of embedding vectors, one per input text.
        """
        if not texts:
            return []

        response = self._client.embeddings.create(
            model=self.model_name,
            input=texts,
        )

        # Sort by index to ensure correct ordering
        sorted_data = sorted(response.data, key=lambda x: x.index)
        return [item.embedding for item in sorted_data]

    def embed_query(self, query: str) -> list[float]:
        """Embed a single query text.

        Args:
            query: Query string to embed.

        Returns:
            Single embedding vector.
        """
        result = self.embed_texts([query])
        return result[0]
