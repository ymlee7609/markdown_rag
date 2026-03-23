# Markdown RAG

[English](README.md)

내부 Markdown 문서를 위한 시맨틱 검색 및 QA 시스템.

## 주요 기능

- **Search 모드** (LLM-free): 로컬 임베딩 기반 시맨틱 검색
- **Ask 모드** (Full RAG): OpenAI GPT 또는 로컬 SLM을 활용한 질의응답
- **CLI + REST API**: 명령줄과 HTTP API 동시 지원
- **구조 인식 청킹**: Markdown 헤더 계층 기반 문서 분할

## 요구 사항

- Python 3.11+
- OpenAI API 키 (OpenAI 백엔드 사용 시) 또는 GGUF 모델 파일 (로컬 SLM 사용 시)

## 설치

```bash
# 가상 환경 생성
python -m venv .venv
source .venv/bin/activate

# 설치 (개발 의존성 포함)
pip install -e ".[dev]"

# 환경 변수 설정
cp .env.example .env
```

## 사용법

### CLI

```bash
# 문서 수집
mdrag ingest ./docs/

# 시맨틱 검색 (LLM 불필요)
mdrag search "인증 방식"

# 질의응답 - OpenAI (기본)
mdrag ask "인증은 어떻게 동작하나요?"

# 질의응답 - 로컬 SLM (GGUF 모델)
mdrag ask "인증은 어떻게 동작하나요?" --llm-backend local

# 수집 상태 확인
mdrag status
```

### REST API 서버

```bash
mdrag serve
```

기본 포트: `8900`

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/health` | 헬스 체크 |
| GET | `/api/v1/status` | 수집 상태 조회 |
| POST | `/api/v1/ingest` | 문서 수집 |
| POST | `/api/v1/search` | 시맨틱 검색 |
| POST | `/api/v1/ask` | RAG 질의응답 |
| DELETE | `/api/v1/documents` | 문서 삭제 |

## 설정

환경 변수(`MDRAG_` 접두사) 또는 `.env` 파일로 설정합니다.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `MDRAG_EMBEDDING_BACKEND` | `local` | 임베딩 백엔드 (`local` / `openai`) |
| `MDRAG_LOCAL_MODEL` | `all-MiniLM-L6-v2` | 로컬 임베딩 모델 |
| `MDRAG_LLM_BACKEND` | `openai` | LLM 백엔드 (`openai` / `local`) |
| `MDRAG_OPENAI_LLM_MODEL` | `gpt-4o-mini` | OpenAI LLM 모델 |
| `MDRAG_LOCAL_LLM_MODEL_PATH` | | GGUF 모델 파일 경로 |
| `MDRAG_LOCAL_LLM_CONTEXT_SIZE` | `4096` | 로컬 LLM 컨텍스트 크기 |
| `MDRAG_LOCAL_LLM_MAX_TOKENS` | `1024` | 로컬 LLM 최대 생성 토큰 |
| `MDRAG_CHROMA_PATH` | `./data/chroma` | ChromaDB 저장 경로 |
| `MDRAG_CHUNK_MAX_SIZE` | `1000` | 청크 최대 크기 (문자) |
| `MDRAG_CHUNK_OVERLAP` | `100` | 청크 간 중첩 크기 (문자) |
| `MDRAG_SEARCH_TOP_K` | `5` | 검색 결과 수 |
| `MDRAG_API_PORT` | `8900` | API 서버 포트 |

## 아키텍처

```
문서 수집:  Markdown 파일 → 파서 → 청커 → 임베딩 → ChromaDB
검색:      질의 → 임베딩 → ChromaDB 유사도 검색 → 결과
RAG:       질의 → 검색 → 컨텍스트 + 프롬프트 → LLM(OpenAI/로컬) → 응답
```

### 주요 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| chromadb | >= 1.5 | 벡터 데이터베이스 |
| sentence-transformers | >= 5.0 | 로컬 임베딩 |
| openai | >= 2.29 | LLM 및 임베딩 API |
| llama-cpp-python | >= 0.3 | 로컬 SLM (GGUF, CPU) |
| markdown-it-py | >= 4.0 | Markdown AST 파싱 |
| fastapi | >= 0.135 | REST API 프레임워크 |
| pydantic | >= 2.12 | 데이터 유효성 검증 |

## 개발

```bash
# 테스트 실행
pytest tests/ -v

# 커버리지 확인 (최소 85%)
pytest tests/ --cov=markdown_rag --cov-report=term-missing

# 린트
ruff check src/ tests/
```

## 라이선스

MIT
