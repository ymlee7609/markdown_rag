"""LocalLLM 백엔드 테스트."""

from __future__ import annotations

import sys
from types import ModuleType
from unittest.mock import MagicMock, patch

import pytest

# llama_cpp가 설치되지 않은 환경에서도 테스트할 수 있도록 mock 모듈 주입
_mock_llama_module = ModuleType("llama_cpp")
_mock_llama_cls = MagicMock()
_mock_llama_module.Llama = _mock_llama_cls  # type: ignore[attr-defined]


@pytest.fixture(autouse=True)
def _patch_llama_cpp():
    """llama_cpp 모듈이 없어도 import 가능하도록 mock 주입."""
    with patch.dict(sys.modules, {"llama_cpp": _mock_llama_module}):
        _mock_llama_cls.reset_mock()
        yield


from markdown_rag.llm.local import LocalLLM  # noqa: E402


class TestLocalLLMInit:
    """LocalLLM 초기화 테스트."""

    def test_model_name_returns_path(self) -> None:
        llm = LocalLLM(model_path="/models/phi-4-mini.gguf")
        assert llm.model_name == "/models/phi-4-mini.gguf"

    def test_default_context_size(self) -> None:
        llm = LocalLLM(model_path="/models/test.gguf")
        assert llm._context_size == 4096

    def test_custom_settings(self) -> None:
        llm = LocalLLM(
            model_path="/models/test.gguf",
            context_size=8192,
            max_tokens=2048,
        )
        assert llm._context_size == 8192
        assert llm._max_tokens == 2048

    def test_model_not_loaded_on_init(self) -> None:
        llm = LocalLLM(model_path="/models/test.gguf")
        assert llm._model is None


class TestLocalLLMGenerate:
    """LocalLLM.generate() 메서드 테스트."""

    def test_generates_response(self) -> None:
        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_chat_completion.return_value = {
            "choices": [{"message": {"content": "로컬 응답"}}]
        }

        llm = LocalLLM(model_path="/models/test.gguf")
        result = llm.generate([{"role": "user", "content": "질문"}])

        assert result == "로컬 응답"

    def test_loads_model_lazily(self) -> None:
        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_chat_completion.return_value = {
            "choices": [{"message": {"content": "ok"}}]
        }

        llm = LocalLLM(model_path="/models/test.gguf", context_size=2048)
        assert llm._model is None

        llm.generate([{"role": "user", "content": "test"}])

        _mock_llama_cls.assert_called_once_with(
            model_path="/models/test.gguf",
            n_ctx=2048,
            verbose=False,
        )
        assert llm._model is not None

    def test_reuses_loaded_model(self) -> None:
        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_chat_completion.return_value = {
            "choices": [{"message": {"content": "ok"}}]
        }

        llm = LocalLLM(model_path="/models/test.gguf")
        llm.generate([{"role": "user", "content": "1"}])
        llm.generate([{"role": "user", "content": "2"}])

        _mock_llama_cls.assert_called_once()

    def test_passes_max_tokens(self) -> None:
        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_chat_completion.return_value = {
            "choices": [{"message": {"content": "ok"}}]
        }

        messages = [{"role": "user", "content": "질문"}]
        llm = LocalLLM(model_path="/models/test.gguf", max_tokens=512)
        llm.generate(messages)

        mock_model.create_chat_completion.assert_called_once_with(
            messages=messages,
            max_tokens=512,
        )

    def test_handles_empty_choices(self) -> None:
        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_chat_completion.return_value = {"choices": []}

        llm = LocalLLM(model_path="/models/test.gguf")
        result = llm.generate([{"role": "user", "content": "test"}])

        assert result == ""

    def test_handles_missing_content(self) -> None:
        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_chat_completion.return_value = {
            "choices": [{"message": {}}]
        }

        llm = LocalLLM(model_path="/models/test.gguf")
        result = llm.generate([{"role": "user", "content": "test"}])

        assert result == ""
