"""llama-cpp-python 기반 로컬 LLM 백엔드."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from llama_cpp import Llama

logger = logging.getLogger(__name__)


class LocalLLM:
    """GGUF 모델을 CPU에서 실행하는 로컬 LLM 백엔드.

    llama-cpp-python 라이브러리를 사용하여 GGUF 포맷 모델을 로드하고
    추론을 수행한다. 모델은 최초 사용 시 지연 로드된다.

    Args:
        model_path: GGUF 모델 파일 경로.
        context_size: 컨텍스트 윈도우 크기 (기본: 4096).
        max_tokens: 최대 생성 토큰 수 (기본: 1024).
    """

    def __init__(
        self,
        model_path: str,
        context_size: int = 4096,
        max_tokens: int = 1024,
    ) -> None:
        self._model_path = model_path
        self._context_size = context_size
        self._max_tokens = max_tokens
        self._model: Llama | None = None

    @property
    def model_name(self) -> str:
        """현재 사용 중인 모델 파일 경로."""
        return self._model_path

    def _load_model(self) -> Llama:
        """모델을 최초 사용 시 로드한다."""
        if self._model is None:
            import os
            from contextlib import redirect_stderr

            from llama_cpp import Llama

            logger.info("로컬 LLM 모델 로드 중: %s", self._model_path)
            # llama.cpp C 레벨 stderr 경고(n_ctx_seq < n_ctx_train) 억제
            with open(os.devnull, "w") as devnull, redirect_stderr(devnull):
                self._model = Llama(
                    model_path=self._model_path,
                    n_ctx=self._context_size,
                    verbose=False,
                )
        return self._model

    def generate(self, messages: list[dict[str, str]]) -> str:
        """로컬 모델로 응답을 생성한다.

        Args:
            messages: ChatCompletion 형식의 메시지 목록.

        Returns:
            생성된 응답 텍스트.
        """
        model = self._load_model()
        response = model.create_chat_completion(
            messages=messages,
            max_tokens=self._max_tokens,
        )
        choices = response.get("choices", [])
        if not choices:
            return ""
        return choices[0].get("message", {}).get("content", "")
