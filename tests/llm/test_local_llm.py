"""LocalLLM 백엔드 테스트."""

from __future__ import annotations

import sys
from pathlib import Path
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

    def test_default_temperature_for_korean(self) -> None:
        llm = LocalLLM(model_path="/models/test.gguf")
        assert llm._temperature == 0.1

    def test_default_stop_tokens_include_exaone_endofturn(self) -> None:
        llm = LocalLLM(model_path="/models/test.gguf")
        assert "[|endofturn|]" in llm._stop_tokens


class TestLocalLLMChatTemplate:
    """외부 chat_template 로드 및 컴파일 테스트."""

    def test_chat_template_source_loaded_from_file(self, tmp_path: Path) -> None:
        template_file = tmp_path / "chat.jinja"
        template_body = "{{ messages[0].content }}"
        template_file.write_text(template_body, encoding="utf-8")

        llm = LocalLLM(
            model_path="/models/test.gguf",
            chat_template_path=str(template_file),
        )

        assert llm._chat_template_source == template_body
        assert llm._jinja_template is not None

    def test_missing_chat_template_raises(self, tmp_path: Path) -> None:
        missing = tmp_path / "nope.jinja"

        with pytest.raises(FileNotFoundError):
            LocalLLM(
                model_path="/models/test.gguf",
                chat_template_path=str(missing),
            )

    def test_loopcontrols_extension_supports_continue(self, tmp_path: Path) -> None:
        # EXAONE 공식 템플릿이 사용하는 {% continue %} 구문을 컴파일·렌더링할 수 있어야 한다.
        template_file = tmp_path / "chat.jinja"
        template_body = (
            "{%- for m in messages %}"
            "{%- if m.role == 'system' %}{%- continue %}{%- endif %}"
            "{{ m.role }}:{{ m.content }};"
            "{%- endfor %}"
        )
        template_file.write_text(template_body, encoding="utf-8")

        llm = LocalLLM(
            model_path="/models/test.gguf",
            chat_template_path=str(template_file),
        )
        rendered = llm._render_prompt(
            [
                {"role": "system", "content": "ignore"},
                {"role": "user", "content": "hi"},
            ]
        )

        assert "system:" not in rendered
        assert "user:hi;" in rendered


class TestLocalLLMGenerate:
    """LocalLLM.generate() 메서드 테스트."""

    def test_generates_response_via_chat_completion(self) -> None:
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

    def test_external_template_uses_create_completion(self, tmp_path: Path) -> None:
        template_file = tmp_path / "chat.jinja"
        template_file.write_text(
            "{%- for m in messages %}{{ m.role }}:{{ m.content }}\n{%- endfor %}"
            "{%- if add_generation_prompt %}assistant:{%- endif %}",
            encoding="utf-8",
        )

        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_completion.return_value = {
            "choices": [{"text": "  EXAONE 답변  "}]
        }

        llm = LocalLLM(
            model_path="/models/test.gguf",
            context_size=2048,
            chat_template_path=str(template_file),
            max_tokens=256,
            temperature=0.2,
        )
        result = llm.generate([{"role": "user", "content": "질문"}])

        assert result == "EXAONE 답변"
        # chat 경로가 아닌 raw completion 경로가 사용되어야 한다.
        mock_model.create_chat_completion.assert_not_called()
        mock_model.create_completion.assert_called_once()
        kwargs = mock_model.create_completion.call_args.kwargs
        assert "user:질문" in kwargs["prompt"]
        assert kwargs["prompt"].rstrip().endswith("assistant:")
        assert kwargs["max_tokens"] == 256
        assert kwargs["temperature"] == 0.2
        assert kwargs["stop"] == ["[|endofturn|]"]

    def test_external_template_handles_empty_choices(self, tmp_path: Path) -> None:
        template_file = tmp_path / "chat.jinja"
        template_file.write_text("{{ messages[0].content }}", encoding="utf-8")

        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_completion.return_value = {"choices": []}

        llm = LocalLLM(
            model_path="/models/test.gguf",
            chat_template_path=str(template_file),
        )
        assert llm.generate([{"role": "user", "content": "x"}]) == ""

    def test_custom_stop_tokens_passed_through(self, tmp_path: Path) -> None:
        template_file = tmp_path / "chat.jinja"
        template_file.write_text("{{ messages[0].content }}", encoding="utf-8")

        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_completion.return_value = {
            "choices": [{"text": "ok"}]
        }

        llm = LocalLLM(
            model_path="/models/test.gguf",
            chat_template_path=str(template_file),
            stop_tokens=["</s>", "<|im_end|>"],
        )
        llm.generate([{"role": "user", "content": "x"}])

        kwargs = mock_model.create_completion.call_args.kwargs
        assert kwargs["stop"] == ["</s>", "<|im_end|>"]

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

    def test_passes_max_tokens_to_chat_completion(self) -> None:
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
            temperature=0.1,
        )

    def test_passes_custom_temperature_to_chat_completion(self) -> None:
        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_chat_completion.return_value = {
            "choices": [{"message": {"content": "ok"}}]
        }

        messages = [{"role": "user", "content": "질문"}]
        llm = LocalLLM(
            model_path="/models/test.gguf",
            max_tokens=256,
            temperature=0.7,
        )
        llm.generate(messages)

        mock_model.create_chat_completion.assert_called_once_with(
            messages=messages,
            max_tokens=256,
            temperature=0.7,
        )

    def test_handles_empty_choices_chat_path(self) -> None:
        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_chat_completion.return_value = {"choices": []}

        llm = LocalLLM(model_path="/models/test.gguf")
        result = llm.generate([{"role": "user", "content": "test"}])

        assert result == ""

    def test_handles_missing_content_chat_path(self) -> None:
        mock_model = MagicMock()
        _mock_llama_cls.return_value = mock_model
        mock_model.create_chat_completion.return_value = {
            "choices": [{"message": {}}]
        }

        llm = LocalLLM(model_path="/models/test.gguf")
        result = llm.generate([{"role": "user", "content": "test"}])

        assert result == ""
