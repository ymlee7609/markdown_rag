# 마크다운 RAG 온톨로지 스키마

본 디렉토리는 `input_ontology/` 보조 코퍼스의 **스키마 정의**와 **별칭 사전**을 담는다. 12,131개 마크다운(Cisco_CCIE / IETF_RFC / 가입자망장비_manual) 코퍼스 위에 RFC↔이론↔CLI 3계층 관계를 잇는 온톨로지 카드를 얹어 RAG 검색 품질을 끌어올리는 것이 목적이다.

상위 설계 문서: `/home/ymlee/.claude/plans/markdown-eager-glacier.md`

---

## 파일 구성

| 파일 | 역할 |
|---|---|
| `entity_types.yaml` | 8종 엔티티 타입(Protocol, RFC, Concept, Feature, Command, Vendor, DeviceModel, Standard) 스키마. 카드 frontmatter 필수/선택 필드, ID prefix 규칙. |
| `relation_types.yaml` | 14종 관계 타입(defined_by, obsoletes, extends, implements, ...) 정의. domain/range 제약, inverse 관계, 추출 정책, 검증 규칙. |
| `alias_dictionary.yaml` | canonical ID ↔ 약어/별칭/한국어 동의어 매핑. 결정론적 추출(Stage 1)이 이 사전을 토큰 매칭에 사용. |
| `README.md` | (이 문서) 스키마 개요와 카드 작성 가이드. |

---

## 엔티티 타입 요약

| Type | ID Prefix | 1차 우선순위 |
|---|---|---|
| Protocol | `proto:` | Tier 1 |
| RFC | `rfc:` | Tier 1 |
| Concept | `concept:` | Tier 1 |
| Feature | `feat:` | Tier 2 |
| Vendor | `vendor:` | Tier 2 |
| DeviceModel | `model:` | Tier 2 |
| Command | `cmd:` | Tier 3 (2차 확장) |
| Standard | `std:` | Tier 3 (선택) |

`entity_types.yaml`의 `priority` 키 참고.

---

## 관계 타입 요약

| 관계 | 의미 | 추출 |
|---|---|---|
| `defined_by` / `defines` | Protocol↔RFC 표준 정의 | LLM + 인간 검수 |
| `obsoletes` / `obsoleted_by` | RFC 폐기 체인 | 정규식 + RFC 헤더 |
| `updates` / `updated_by` | RFC 부분 갱신 | 정규식 + RFC 헤더 |
| `extends` | Protocol 확장 (OSPFv3 extends OSPF) | LLM + 인간 검수 |
| `part_of` | Concept이 Protocol에 속함 | LLM (parent_protocol 필드) |
| `implements` | Feature가 Protocol 구현 | LLM |
| `configures` | Command가 Feature/Concept 설정 | LLM |
| `available_on` | Command/Feature 지원 모델 | LLM |
| `references` | 본문 참조 (약한 관계) | 정규식 "RFC NNNN" |
| `taught_in` | 학습 자료 위치 | 파일 경로 기반 |
| `documented_in` | 매뉴얼 위치 | 파일 경로 기반 |
| `related_to` | 약한 연관 (expansion용) | LLM |
| `alias_of` | 동의어 매핑 | 사전 기반 |
| `depends_on` | 동작 선행 조건 | LLM + 인간 검수 |

`relation_types.yaml`의 `extraction_policy` 키 참고.

---

## 카드 작성 가이드

### ID 명명 규칙

- 형식: `<prefix>:<slug>`
- slug: 영어 lowercase-kebab-case canonical 명칭
  - `proto:ospf` (◯), `proto:OSPF` (✗), `proto:open-shortest-path-first` (장황, ✗)
- 약어가 통용되면 약어 그대로 사용 (`proto:bgp`, `proto:stp`)
- 한국어/원어 정식 명칭은 frontmatter의 `name_ko` / `name_en` 필드에 기록

### frontmatter 필수 필드

모든 카드 공통:
- `id` — canonical ID
- `type` — 엔티티 타입 (entity_types.yaml의 키)
- `source` — `human` | `llm` | `llm-reviewed`

타입별 추가 필수 필드는 `entity_types.yaml`의 `required_fields` 참고.

### 본문 구조 (Protocol/Concept/Feature 표준)

1. **개요** — 1~3문장 정의(한국어 우선, 영어 핵심 용어 병기)
2. **표준 / 정의** — `defined_by` RFC/Standard, 폐기/갱신 체인 (RFC 카드에서는 "정의 대상" + "표준 체인"으로 변형)
3. **핵심 개념** 또는 **동작 개념** — Concept 카드 링크 또는 짧은 설명
4. **벤더 구현 매핑** — Vendor × 명령어/Feature 표 + `documented_in` 경로
5. **교차 참조** — 관련 카드 링크
6. **검색 힌트** (선택) — RAG가 이 카드를 활용할 질문 패턴 예시

### 코퍼스 경로 표기

`taught_in`, `documented_in`, `corpus_paths` 필드는 항상 `input_optimized/` 기준 상대 경로:

```yaml
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-03.md"
documented_in:
  - "가입자망장비_manual/다산_L3"     # 디렉토리 단위도 허용
corpus_paths:
  - "IETF_RFC/rfc2328__sec-01.md"
```

### `confidence`와 `source`

- `source: human` → `confidence: 1.0` (수작업 카드)
- `source: llm` → `confidence: 0.5~0.9` (자동 추출, 검수 전)
- `source: llm-reviewed` → `confidence: 0.85~1.0` (인간 검수 통과)
- `confidence < 0.5` 카드는 인덱스 빌드에서 제외 (relations.jsonl도 동일)

---

## 검증 (M1 acceptance)

M1 단계 완료 기준:
1. `entity_types.yaml`, `relation_types.yaml`, `alias_dictionary.yaml` 파일 lint 통과 (YAML syntax)
2. ID prefix 충돌 없음 (`scripts/build_ontology_schema.py --validate` 추후 추가)
3. 샘플 카드 3개(`protocols/proto-ospf.md`, `rfcs/rfc-2328.md`, `features/feat-dot1q-tunnel.md`) 모두 entity_types.yaml의 required_fields 충족

---

## 디렉토리 구조 (`input_ontology/`)

```
input_ontology/
├── schema/                        # 본 스키마 디렉토리
│   ├── entity_types.yaml
│   ├── relation_types.yaml
│   ├── alias_dictionary.yaml
│   └── README.md
├── protocols/                     # proto-*.md
├── concepts/                      # concept-*.md
├── rfcs/                          # rfc-*.md
├── features/                      # feat-*.md
├── commands/                      # cmd-*.md   (2차 확장)
├── vendors/                       # vendor-*.md
├── devices/                       # model-*.md
├── standards/                     # std-*.md  (RFC 외 표준: IEEE/ITU-T 등)
└── _relations/
    └── relations.jsonl            # 5-tuple 관계 인스턴스
```

별도로 `data/ontology/`에는 검색/인덱스용 보조 데이터가 생성된다:
- `index.json` — 전체 엔티티 ID → 파일 경로 매핑
- `alias_index.json` — 약어/한국어 → canonical ID 역인덱스
- `chunk_enrichment.parquet` — chunk_id ↔ onto_ids 매핑

이 두 파일은 빌드 산출물이므로 카드 작성자는 직접 만지지 않는다 (`scripts/build_ontology_schema.py` 가 생성).

---

## 다음 단계 (M2)

- 1차 핵심 프로토콜 30개 수작업 카드 작성 (`/home/ymlee/.claude/plans/markdown-eager-glacier.md` 의 "1차 핵심 프로토콜 후보 45개" 참고)
- Protocol 카드 작성 시 동반 RFC 카드와 핵심 Concept 카드도 같이 생성
- 작성 후 validation_dataset.json 100건 중 onto-id 매칭 80%+ 달성 여부 확인
