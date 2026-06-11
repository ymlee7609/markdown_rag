# Markdown RAG

[English](README.md)

내부 Markdown 문서를 위한 다국어 시맨틱 검색 및 하이브리드 RAG 시스템.

## 주요 기능

- **Search 모드** (LLM-free): 로컬 임베딩 기반 시맨틱 검색
- **Ask 모드** (Full RAG): OpenAI GPT 또는 로컬 SLM을 활용한 질의응답
- **CLI + REST API**: 명령줄과 HTTP API 동시 지원
- **구조 인식 청킹**: Markdown 헤더 계층 기반 문서 분할
- **다국어 지원**: 한국어 + 영어 임베딩 (Phase 1)
- **메타데이터 필터링**: 문서 타입(RFC/CCIE/통신사 매뉴얼) 및 언어별 분류 (Phase 2)
- **하이브리드 검색**: BM25 키워드 검색 + 벡터 임베딩 조합 (Phase 3)
- **크로스 인코더 리랭킹**: 검색 결과 정확도 개선 (Phase 4)
- **배치 인제스트**: 대규모 문서 처리 최적화 (Phase 5)
- **HyDE 쿼리 처리**: 가상 문서 임베딩 모듈 (Phase 6, 선택적 모듈 — 기본 검색 파이프라인에는 미연결)
- **온톨로지 증강 검색**: 보조 코퍼스(`input_ontology/`) + referenced-path 자동 확장으로 CCIE Hit@5 60→100%, 전체 Hit@5 88→100% (Phase 7)

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

# 하이브리드 검색 (벡터 + BM25 RRF 결합)
mdrag search "인증 방식" --mode hybrid

# 온톨로지 증강 검색 (보조 코퍼스 + referenced-path 자동 확장)
mdrag search "OSPF area 설정" --mode ontology

# 메타데이터 필터링
mdrag search "인증" --doc-type rfc --language ko

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
| POST | `/api/v1/search` | 시맨틱/하이브리드 검색 |
| POST | `/api/v1/ask` | RAG 질의응답 |
| DELETE | `/api/v1/documents` | 문서 삭제 |

## 설정

환경 변수(`MDRAG_` 접두사) 또는 `.env` 파일로 설정합니다.

### 기본 설정

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `MDRAG_EMBEDDING_BACKEND` | `local` | 임베딩 백엔드 (`local` / `openai`) |
| `MDRAG_LOCAL_MODEL` | `intfloat/multilingual-e5-small` | 로컬 임베딩 모델 (다국어 지원) |
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

### Phase 2-6 신규 설정

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `MDRAG_SEARCH_MODE` | `vector` | 검색 모드 (`vector` / `hybrid` / `ontology`, `bm25` 설정 시 경고 후 vector로 폴백) |
| `MDRAG_HYBRID_ALPHA` | `0.7` | 하이브리드 검색 벡터 가중치 (0.0-1.0) |
| `MDRAG_BM25_INDEX_PATH` | `./data/bm25_index.pkl` | BM25 인덱스 경로 |
| `MDRAG_RERANK_ENABLED` | `false` | 크로스 인코더 리랭킹 활성화 |
| `MDRAG_RERANK_MODEL` | `BAAI/bge-reranker-v2-m3` | 리랭커 모델 (다국어) |
| `MDRAG_INITIAL_TOP_K` | `20` | 리랭킹 전 검색 결과 수 |

### Phase 7 온톨로지 증강 설정

`MDRAG_SEARCH_MODE=ontology` 또는 `--mode ontology` 사용 시 적용됩니다.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `MDRAG_ONTO_CHROMA_PATH` | `./data/chroma_ontology` | 보조 코퍼스 ChromaDB 경로 |
| `MDRAG_ONTO_COLLECTION_NAME` | `markdown_docs_ontology` | 보조 코퍼스 collection 이름 |
| `MDRAG_ONTO_BM25_PATH` | `./data/bm25_ontology` | 보조 코퍼스 BM25 인덱스 |
| `MDRAG_ONTO_REFS_PATH` | `./data/ontology/onto_refs.json` | 카드 → referenced paths 매핑 |
| `MDRAG_ONTO_INJECT_TOP_N_CARDS` | `3` | 보조 카드 hit 중 상위 N개에서 청크 inject |
| `MDRAG_ONTO_INJECT_CHUNKS_PER_CARD` | `1` | 카드당 inject할 main corpus 청크 수 |

## 아키텍처

### 문서 처리 파이프라인

```
문서 수집:  Markdown 파일 → 파서 → 청커 → 메타데이터 추출
                ↓                           ↓
            임베딩 (다국어)      BM25 인덱스 구축
                ↓                           ↓
            ChromaDB 저장 ←────────── 벌크 upsert
```

### 검색 및 RAG 파이프라인

```
질의 (한국어/영어)
    ↓
[벡터 검색] + [BM25 키워드 검색 + 형태소 분석]
    ↓
RRF (Reciprocal Rank Fusion) 결합
    ↓
크로스 인코더 리랭킹 (선택)
    ↓
컨텍스트 조립 (HyDE·인접 청크 확장은 선택적 모듈)
    ↓
프롬프트 + LLM (OpenAI/로컬)
    ↓
응답 반환
```

## 주요 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| chromadb | >= 1.5 | 벡터 데이터베이스 |
| sentence-transformers | >= 5.0 | 다국어 임베딩 (intfloat/multilingual-e5) |
| openai | >= 2.29 | LLM 및 임베딩 API |
| llama-cpp-python | >= 0.3 | 로컬 SLM (GGUF, CPU) |
| markdown-it-py | >= 4.0 | Markdown AST 파싱 |
| fastapi | >= 0.135 | REST API 프레임워크 |
| pydantic | >= 2.12 | 데이터 유효성 검증 |
| bm25s | >= 0.3.5 | BM25 키워드 검색 (희소 행렬 기반, 저메모리) |
| kiwipiepy | >= 0.18 | 한국어 형태소 분석 |
| tqdm | >= 4.60 | 진행률 표시 |

## 테스트 및 품질

```bash
# 테스트 실행
pytest tests/ -v

# 커버리지 확인 (100%)
pytest tests/ --cov=markdown_rag --cov-report=term-missing

# 린트
ruff check src/ tests/
```

현황: 443개 테스트, 커버리지 100%

## 개발

### Phase 진행 상황

- Phase 1: 다국어 임베딩 (완료) - intfloat/multilingual-e5-small (384차원)
- Phase 2: 메타데이터 필터링 (완료) - doc_type, language 필터
- Phase 3: 하이브리드 검색 (완료) - BM25 + 벡터 RRF
- Phase 4: 크로스 인코더 리랭킹 (완료) - BAAI/bge-reranker-v2-m3
- Phase 5: 배치 인제스트 파이프라인 (완료) - 27,000+ 파일 처리
- Phase 6: HyDE 쿼리 처리 (모듈 구현 완료) - 가상 문서 임베딩 + 인접 청크 확장, 기본 파이프라인 미연결 (선택적 사용)
- Phase 7: 온톨로지 증강 검색 (완료) - 아래 섹션 참조

## 온톨로지 증강 검색 (Phase 7)

12,000여 개의 마크다운 코퍼스(IETF RFC 11,449 / Cisco CCIE 103 / 다산·유비쿼스 가입자망 매뉴얼 579)에서 "표준 ↔ 이론 ↔ CLI 구현" 3계층 교차 검색 품질을 끌어올리기 위해 **온톨로지 카드 보조 코퍼스**를 도입했습니다.

### 효과 (validation_dataset 100건 기준)

| 지표 | baseline (hybrid) | **ontology mode** | Δ |
|------|---|---|---|
| Passed | 86 | **98** | **+12** |
| Hit@5 (전체) | 88 | **100** | **+12** |
| **Hit@5 (CCIE)** | **18/30 (60%)** | **30/30 (100%)** | **+40%p** |
| MRR | 0.856 | 0.893 | +0.037 |
| 평균 응답 | 1538ms | 1893ms | +355ms |

### 구성 요소

```
input_ontology/                 # 보조 코퍼스 (68 카드)
├── schema/
│   ├── entity_types.yaml       # 8종 엔티티 (Protocol/RFC/Concept/Feature/...)
│   ├── relation_types.yaml     # 17종 관계 (defined_by/extends/implements/...)
│   └── alias_dictionary.yaml   # 영문/한글 별칭 사전
├── protocols/                  # OSPF, BGP, STP, VLAN, DHCP, IGMP, ACL, GPON, ... (18)
├── concepts/                   # ospf-area, bgp-as-path, vlan-trunk, ... (15)
├── rfcs/                       # 2328, 4271, 8200, 5905, ... (15)
├── standards/                  # IEEE 802.1D/Q, ITU-T G.984 (3)
├── features/                   # mac-address-table, port-mirroring, ... (7)
├── vendors/                    # dasan, ubiquoss (2)
└── devices/                    # V3024V, V8500, U9532H, P8624, ... (8)

data/ontology/
├── onto_refs.json              # 카드 → referenced main corpus 경로 매핑
├── index.json                  # 엔티티 ID → 카드 파일
├── alias_index.json            # 별칭 → canonical ID 역인덱스
└── chunk_enrichment.jsonl.gz   # 515K 청크의 onto 후보 (정규식 + 사전 매칭)
```

### 검색 메커니즘 (`--mode ontology`)

1. **Dual collection 검색**: main corpus(`chroma_optimized`) + ontology corpus(`chroma_ontology`)에서 각각 hybrid 검색
2. **RRF union**: 두 결과를 Reciprocal Rank Fusion으로 결합
3. **Referenced-path injection**: 보조 카드 hit이 있으면 해당 카드의 `taught_in`/`documented_in`/`corpus_paths` frontmatter를 따라가서 main corpus의 청크를 자동 inject
4. **결과에 origin 표시**: `[ONTO CARD]` (보조 카드 자체) / `[INJECTED via <카드명>]` (자동 inject) / 일반 (main 직접 hit)

### 빌드/재인덱싱

카드를 추가하거나 수정한 후:

```bash
# 1. 보조 Chroma + BM25 재빌드
python scripts/reindex_optimized.py --input input_ontology \
  --chroma-path data/chroma_ontology \
  --collection markdown_docs_ontology \
  --bm25-path data/bm25_ontology

# 2. onto_refs.json 재생성
python scripts/build_ontology_refs.py

# 3. (선택) 결정론적 추출 — main 코퍼스 chunk에 onto 후보 부여
python scripts/extract_onto_candidates.py
#   → data/ontology/chunk_enrichment.jsonl.gz (515K records, ~2분)

# 4. 검증
python scripts/validate_rag.py --ontology-mode ontology
```

### 카드 작성 가이드

각 카드는 YAML frontmatter + Markdown 본문. 필수 필드는 `input_ontology/schema/entity_types.yaml` 참조.

예: `input_ontology/protocols/proto-ospf.md`

```yaml
---
id: proto:ospf
type: Protocol
name_en: OSPF
name_ko: 개방형 최단 경로 우선
layer: L3
defined_by: [rfc:2328]
related: [proto:isis, concept:ospf-lsa, concept:ospf-area]
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-03.md"
documented_in:
  - "가입자망장비_manual/다산_L3"
keywords_en: [LSA, area, ABR, ASBR, hello, DR, BDR]
keywords_ko: [영역, 인접관계, 헬로]
source: human
---
```

상세 사양은 `input_ontology/schema/README.md`와 `reports/ontology/m3cde_m4_final_report.md` 참조.

## 라이선스

MIT
