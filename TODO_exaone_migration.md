# TODO: LLM을 EXAONE 4.0 1.2B로 교체

**작성일**: 2026-04-23
**담당**: 재인덱싱 완료 후 실행
**목적**: Qwen2.5-1.5B → EXAONE-4.0-1.2B 전환으로 한국어 품질·컨텍스트 길이 향상

---

## 배경

### 왜 교체하는가
- 현재: `qwen2.5-1.5b-instruct-q4_k_m.gguf` (1.1 GB, context 4K)
- 교체: `EXAONE-4.0-1.2B-Q4_K_M.gguf` (812 MB, context 64K)
- 파라미터 더 작으면서 Qwen3-1.7B 대비 대부분 벤치마크 우위
- **한국어(KMMLU-Pro 37.5 vs 29.5, Ko-LongBench 69.8 vs 57.1)** 우수
- 본 프로젝트는 가입자망장비 매뉴얼(한국어) + RFC/CCIE(영어) 혼합 → 한국어 강점이 중요

### 벤치마크 요약 (공식, 1.2B vs 1.7B)

| | EXAONE 4.0 1.2B | Qwen3 1.7B |
|---|---:|---:|
| MMLU-Redux | **66.9** | 63.4 |
| MMLU-Pro | **52.0** | 43.7 |
| KMMLU-Pro | **37.5** | 29.5 |
| Ko-LongBench | **69.8** | 57.1 |
| AIME 2025 | **23.5** | 9.8 |

---

## Prerequisites (사전 준비)

### [x] 1. GGUF 모델 파일 다운로드 ✅ 완료
- 경로: `models/exaone-4.0-1.2b-q4_k_m.gguf`
- 크기: 812 MB (775 MiB)
- SHA256: `7b5e753540183ae4d56e6febd9b48cdd944de53386e6faa8f51c8f98cb2b47df`

### [x] 2. Chat template 파일 다운로드 ✅ 완료
- 경로: `models/exaone-4.0-chat_template.jinja`
- 크기: 5.3 KB
- SHA256: `c670534b79f38b8ef6e692391cec6e7743793b1528d43e87da93a1e5692b9f64`

### [x] 3. llama-cpp-python 버전 확인 ✅ 0.3.17 (충족)

---

## 교체 작업 Checklist

### Phase 1: 코드 수정 ✅ 완료 (2026-04-24)

#### [x] 1-1. `src/markdown_rag/llm/local.py` 개선
- `chat_template_path`, `temperature`, `stop_tokens` 파라미터 추가
- 외부 chat_template은 jinja2 + loopcontrols 확장으로 사전 렌더 후 `create_completion()` 호출
- llama-cpp 내부 ImmutableSandboxedEnvironment를 모델 로드 시점에 일시 monkey-patch하여
  EXAONE 템플릿의 `{% continue %}`가 GGUF 자동 컴파일 단계에서도 파싱되도록 처리
- temperature 기본값 0.1 (한국어 코드 스위칭 방지)

#### [x] 1-2. `src/markdown_rag/config.py` 확장
- `local_llm_chat_template_path: str = ""` 추가
- `local_llm_temperature: float = 0.1` 추가
- CLI(`ask_cmd.py`) / API(`api/routes/ask.py`) 모두 신규 인자 전달

### Phase 2: 설정 교체 ✅ 완료

- `.env`: 모델 경로 EXAONE으로 교체, CONTEXT_SIZE=16384, CHAT_TEMPLATE_PATH 추가
- `.env.example`: 신규 키 문서화
- 기존 Qwen 파일은 그대로 유지 (롤백 가능)

### Phase 3: 검증 ✅ 완료

- 단위 테스트 31개 통과 (`tests/llm/test_local_llm.py` 19, `tests/cli/test_ask_cmd.py` 12)
- 한국어 질의("BGP AS path attribute가 무엇인가?") → 한국어 답변 확인
- 영어 질의("Explain TCP three-way handshake") → 영어 답변 확인

#### [ ] 3-2. 응답 품질 정성 비교 (선택)
같은 질문 10개를 Qwen2.5 vs EXAONE으로 A/B 비교해 답변 품질 체감 비교.

### Phase 4: 튜닝 (필요 시)

#### [ ] 4-1. 한국어 자연도 조정
코드 스위칭(한국어 답변에 영어 섞임) 발생 시 `temperature=0.1`로 낮춤.

#### [ ] 4-2. Reasoning 모드 활성화 (복잡 질의 대응)
EXAONE 4.0은 dual mode 지원. 복잡 추론 필요 시:
```python
# local.py 내 chat_template_kwargs 전달
{"enable_thinking": True}
```
다만 CPU에서는 thinking 과정이 길어져 응답 시간 증가 — 선택적으로 적용.

#### [ ] 4-3. Context 확대 (선택)
현재 4K → 16K 시작. 긴 매뉴얼 섹션 + 여러 청크를 한꺼번에 넣고 싶다면 32K 또는 64K로 증가.
- 메모리 영향: context 2배 증가 시 KV cache 2배 → 메모리 ~400MB 추가
- 응답 시간: context 2배 증가 시 prefill 시간 2배

---

## 롤백 계획

문제 발생 시:
```bash
# .env에서 경로만 복원
MDRAG_LOCAL_LLM_MODEL_PATH=./models/qwen2.5-1.5b-instruct-q4_k_m.gguf
MDRAG_LOCAL_LLM_CONTEXT_SIZE=4096
```
코드 수정(local.py) 롤백은 git으로.

---

## 라이선스 유의사항

**EXAONE AI Model License Agreement 1.2**
- ✅ 상업적 사용 허용 (이전 NC 제한이 완화됨)
- ✅ 교육·연구 목적 허용
- ✅ 모델 출력물 소유권 사용자에게 귀속
- ❌ 경쟁 LLM 개발 목적 사용 금지
- 출처: https://huggingface.co/LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF/blob/main/LICENSE

---

## 참고 링크

- EXAONE-4.0-1.2B-GGUF HF: https://huggingface.co/LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF
- EXAONE 4.0 GitHub: https://github.com/LG-AI-EXAONE/EXAONE-4.0
- EXAONE 4.0 Technical Report: https://arxiv.org/html/2507.11407v1
- Chat template 파일: https://huggingface.co/LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF/blob/main/chat_template.jinja
- llama.cpp 호환성: b5932 이상
