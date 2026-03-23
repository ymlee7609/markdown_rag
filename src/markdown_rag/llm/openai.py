"""OpenAI LLM 백엔드."""

from __future__ import annotations

import logging

import openai

logger = logging.getLogger(__name__)


class OpenAILLM:
    """OpenAI API 기반 LLM 백엔드.

    Args:
        model: OpenAI 모델 이름 (예: 'gpt-4o-mini').
        api_key: OpenAI API 키. None이면 환경 변수에서 자동 로드.
    """

    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None) -> None:
        self._model = model
        self._api_key = api_key

    @property
    def model_name(self) -> str:
        """현재 사용 중인 모델 이름."""
        return self._model

    def generate(self, messages: list[dict[str, str]]) -> str:
        """OpenAI ChatCompletion API로 응답을 생성한다.

        Args:
            messages: ChatCompletion 형식의 메시지 목록.

        Returns:
            생성된 응답 텍스트.
        """
        client = openai.OpenAI(api_key=self._api_key)
        completion = client.chat.completions.create(
            model=self._model,
            messages=messages,
        )
        return completion.choices[0].message.content or ""
