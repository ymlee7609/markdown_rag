"""LLM 백엔드 프로토콜 정의."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMBackend(Protocol):
    """LLM 백엔드 프로토콜.

    RAGEngine에 주입되어 질의에 대한 응답을 생성한다.
    임베딩 백엔드(EmbeddingBackend)와 동일한 Protocol 패턴 사용.
    """

    @property
    def model_name(self) -> str:
        """현재 사용 중인 모델 이름."""
        ...

    def generate(self, messages: list[dict[str, str]]) -> str:
        """메시지 목록을 입력받아 응답 텍스트를 생성한다.

        Args:
            messages: OpenAI ChatCompletion 형식의 메시지 목록.
                각 메시지는 {"role": "system"|"user"|"assistant", "content": "..."}

        Returns:
            생성된 응답 텍스트.
        """
        ...
