"""llama-cpp-python 기반 로컬 LLM 백엔드."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from jinja2 import Template
    from llama_cpp import Llama

logger = logging.getLogger(__name__)


# @MX:ANCHOR: GGUF 모델 추론 진입점 (CLI/API 양쪽에서 사용)
# @MX:REASON: fan_in 2 (cli/ask_cmd.py, api/routes/ask.py) + chat_template 주입 계약 보유
class LocalLLM:
    """GGUF 모델을 CPU에서 실행하는 로컬 LLM 백엔드.

    llama-cpp-python 라이브러리를 사용하여 GGUF 포맷 모델을 로드하고
    추론을 수행한다. 모델은 최초 사용 시 지연 로드된다.

    EXAONE 4.0처럼 전용 Jinja chat template을 요구하는 모델은
    chat_template_path로 .jinja 파일 경로를 주입한다. 템플릿은
    loopcontrols 확장이 활성화된 Jinja 환경에서 직접 렌더링되어
    프롬프트 문자열로 변환된 뒤 create_completion()에 전달된다.
    이 방식은 llama-cpp-python의 내장 Jinja 환경이 일부 확장
    (예: {% continue %})을 지원하지 않는 한계를 우회한다.

    chat_template_path가 None이면 표준 ChatCompletion 경로
    (GGUF 메타데이터 내장 템플릿)를 사용한다.

    Args:
        model_path: GGUF 모델 파일 경로.
        context_size: 컨텍스트 윈도우 크기 (기본: 4096).
        max_tokens: 최대 생성 토큰 수 (기본: 1024).
        chat_template_path: 외부 Jinja chat template 파일 경로 (선택).
        temperature: 샘플링 온도. 한국어 코드 스위칭 방지용 기본 0.1.
        stop_tokens: create_completion 사용 시 정지 토큰 목록.
            None이면 EXAONE 기본값 ["[|endofturn|]"] 사용.
    """

    # EXAONE 4.0 turn 종료 토큰. 다른 모델은 stop_tokens로 오버라이드.
    _DEFAULT_STOP_TOKENS = ["[|endofturn|]"]

    def __init__(
        self,
        model_path: str,
        context_size: int = 4096,
        max_tokens: int = 1024,
        chat_template_path: str | None = None,
        temperature: float = 0.1,
        stop_tokens: list[str] | None = None,
    ) -> None:
        self._model_path = model_path
        self._context_size = context_size
        self._max_tokens = max_tokens
        self._chat_template_path = chat_template_path
        self._temperature = temperature
        self._stop_tokens = (
            list(stop_tokens) if stop_tokens is not None else list(self._DEFAULT_STOP_TOKENS)
        )
        self._chat_template_source: str | None = None
        self._jinja_template: Template | None = None
        # chat_template 파일은 초기화 시점에 한 번만 컴파일해 캐싱한다.
        if chat_template_path:
            template_path = Path(chat_template_path)
            if not template_path.is_file():
                raise FileNotFoundError(
                    f"chat template 파일을 찾을 수 없습니다: {chat_template_path}"
                )
            self._chat_template_source = template_path.read_text(encoding="utf-8")
            self._jinja_template = self._compile_template(self._chat_template_source)
        self._model: Llama | None = None

    @property
    def model_name(self) -> str:
        """현재 사용 중인 모델 파일 경로."""
        return self._model_path

    @staticmethod
    def _compile_template(source: str) -> Template:
        """loopcontrols 확장이 활성화된 Jinja 환경으로 템플릿 컴파일.

        EXAONE 공식 chat_template은 {% continue %} 등을 사용하므로
        Jinja2 loopcontrols 확장을 명시적으로 활성화한다.
        """
        from jinja2 import Environment

        env = Environment(
            extensions=["jinja2.ext.loopcontrols"],
            trim_blocks=False,
            lstrip_blocks=False,
            keep_trailing_newline=True,
        )

        # EXAONE 템플릿이 사용하는 raise_exception 헬퍼 등록.
        def _raise_exception(msg: str) -> str:
            raise ValueError(msg)

        env.globals["raise_exception"] = _raise_exception
        return env.from_string(source)

    @staticmethod
    def _patch_sandbox_env_with_loopcontrols() -> tuple[Any, Any]:
        """ImmutableSandboxedEnvironment에 loopcontrols 확장을 임시 주입.

        llama-cpp-python은 GGUF 메타데이터의 chat_template을 Llama 생성 시점에
        ImmutableSandboxedEnvironment로 컴파일하는데, 이 환경에는 loopcontrols
        확장이 활성화되어 있지 않아 EXAONE 템플릿의 {% continue %}가 파싱되지
        않는다. Llama 생성 직전에 __init__을 패치해 모든 새 환경에 loopcontrols
        확장이 추가되도록 한다. 반환된 (sandbox_cls, original_init)은 원복용.
        """
        from jinja2.sandbox import ImmutableSandboxedEnvironment

        original_init = ImmutableSandboxedEnvironment.__init__

        def patched_init(self: Any, *args: Any, **kwargs: Any) -> None:
            exts = list(kwargs.get("extensions") or [])
            if "jinja2.ext.loopcontrols" not in exts:
                exts.append("jinja2.ext.loopcontrols")
            kwargs["extensions"] = exts
            original_init(self, *args, **kwargs)

        ImmutableSandboxedEnvironment.__init__ = patched_init  # type: ignore[method-assign]
        return ImmutableSandboxedEnvironment, original_init

    def _load_model(self) -> Llama:
        """모델을 최초 사용 시 로드한다."""
        if self._model is None:
            import os
            from contextlib import redirect_stderr

            from llama_cpp import Llama

            logger.info("로컬 LLM 모델 로드 중: %s", self._model_path)
            sandbox_cls, original_init = self._patch_sandbox_env_with_loopcontrols()
            try:
                # llama.cpp C 레벨 stderr 경고 억제
                with open(os.devnull, "w") as devnull, redirect_stderr(devnull):
                    self._model = Llama(
                        model_path=self._model_path,
                        n_ctx=self._context_size,
                        verbose=False,
                    )
            finally:
                sandbox_cls.__init__ = original_init  # type: ignore[method-assign]
        return self._model

    def _render_prompt(self, messages: list[dict[str, str]]) -> str:
        """외부 chat_template으로 prompt 문자열을 사전 렌더링한다."""
        assert self._jinja_template is not None
        return self._jinja_template.render(
            messages=messages,
            add_generation_prompt=True,
        )

    def generate(self, messages: list[dict[str, str]]) -> str:
        """로컬 모델로 응답을 생성한다.

        외부 chat_template이 주입된 경우: messages → prompt 직접 렌더 후
        create_completion 호출. 그렇지 않은 경우: GGUF 내장 템플릿 기반
        create_chat_completion 호출.

        Args:
            messages: ChatCompletion 형식의 메시지 목록.

        Returns:
            생성된 응답 텍스트.
        """
        model = self._load_model()

        if self._jinja_template is not None:
            prompt = self._render_prompt(messages)
            response: Any = model.create_completion(
                prompt=prompt,
                max_tokens=self._max_tokens,
                temperature=self._temperature,
                stop=self._stop_tokens,
            )
            choices = response.get("choices", []) if isinstance(response, dict) else []
            if not choices:
                return ""
            text = choices[0].get("text")
            return text.strip() if isinstance(text, str) else ""

        # GGUF 내장 chat_template 경로
        # llama_cpp의 ChatCompletionRequestMessage TypedDict 스텁이 엄격하므로
        # 런타임 호환성을 유지하면서 Pyright 경고를 무시한다.
        chat_response: Any = model.create_chat_completion(  # type: ignore[arg-type]
            messages=messages,  # type: ignore[arg-type]
            max_tokens=self._max_tokens,
            temperature=self._temperature,
        )
        chat_choices = (
            chat_response.get("choices", []) if isinstance(chat_response, dict) else []
        )
        if not chat_choices:
            return ""
        content = chat_choices[0].get("message", {}).get("content")
        return content if isinstance(content, str) else ""
