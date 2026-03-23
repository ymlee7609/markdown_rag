"""OpenAILLM 백엔드 테스트."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from markdown_rag.llm.openai import OpenAILLM


class TestOpenAILLMInit:
    """OpenAILLM 초기화 테스트."""

    def test_default_model(self) -> None:
        llm = OpenAILLM()
        assert llm.model_name == "gpt-4o-mini"

    def test_custom_model(self) -> None:
        llm = OpenAILLM(model="gpt-4o")
        assert llm.model_name == "gpt-4o"

    def test_stores_api_key(self) -> None:
        llm = OpenAILLM(api_key="sk-test")
        assert llm._api_key == "sk-test"


class TestOpenAILLMGenerate:
    """OpenAILLM.generate() 메서드 테스트."""

    @patch("markdown_rag.llm.openai.openai")
    def test_calls_openai_api(self, mock_openai: MagicMock) -> None:
        mock_client = MagicMock()
        mock_openai.OpenAI.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_completion("답변")

        llm = OpenAILLM(model="gpt-4o-mini", api_key="sk-test")
        result = llm.generate([{"role": "user", "content": "질문"}])

        assert result == "답변"
        mock_openai.OpenAI.assert_called_once_with(api_key="sk-test")

    @patch("markdown_rag.llm.openai.openai")
    def test_passes_messages(self, mock_openai: MagicMock) -> None:
        mock_client = MagicMock()
        mock_openai.OpenAI.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_completion("ok")

        messages = [
            {"role": "system", "content": "시스템"},
            {"role": "user", "content": "사용자"},
        ]
        llm = OpenAILLM(api_key="sk-test")
        llm.generate(messages)

        call_kwargs = mock_client.chat.completions.create.call_args
        assert call_kwargs.kwargs["messages"] == messages
        assert call_kwargs.kwargs["model"] == "gpt-4o-mini"

    @patch("markdown_rag.llm.openai.openai")
    def test_handles_none_content(self, mock_openai: MagicMock) -> None:
        mock_client = MagicMock()
        mock_openai.OpenAI.return_value = mock_client
        completion = MagicMock()
        completion.choices = [MagicMock()]
        completion.choices[0].message.content = None
        mock_client.chat.completions.create.return_value = completion

        llm = OpenAILLM(api_key="sk-test")
        result = llm.generate([{"role": "user", "content": "질문"}])

        assert result == ""


def _mock_completion(content: str) -> MagicMock:
    """OpenAI ChatCompletion mock 응답 생성."""
    completion = MagicMock()
    completion.choices = [MagicMock()]
    completion.choices[0].message.content = content
    return completion
