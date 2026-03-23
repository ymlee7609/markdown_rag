"""LLMBackend Protocol 테스트."""

from __future__ import annotations

from markdown_rag.llm.base import LLMBackend


class _DummyLLM:
    """테스트용 LLMBackend 구현."""

    @property
    def model_name(self) -> str:
        return "dummy"

    def generate(self, messages: list[dict[str, str]]) -> str:
        return "dummy response"


class TestLLMBackendProtocol:
    """LLMBackend Protocol 검증."""

    def test_dummy_is_instance_of_protocol(self) -> None:
        llm = _DummyLLM()
        assert isinstance(llm, LLMBackend)

    def test_generate_returns_string(self) -> None:
        llm = _DummyLLM()
        result = llm.generate([{"role": "user", "content": "hello"}])
        assert isinstance(result, str)
        assert result == "dummy response"

    def test_model_name_property(self) -> None:
        llm = _DummyLLM()
        assert llm.model_name == "dummy"
