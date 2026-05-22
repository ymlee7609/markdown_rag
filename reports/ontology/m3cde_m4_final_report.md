# 온톨로지 통합 최종 리포트 — M3-C+, M3-B, M3-D, M3-E, M4 Stage 1

생성일: 2026-05-22
누적 진척: M2(스키마+카드 시작) → M2.5(KO 보강) → M3(ablation) → M3-A(잔여 cover) → M3-C(운영 클래스) → **M3-C+/B/D/E + M4-S1 (이번)**

---

## 종합 결과

`validate_rag.py --ontology-mode ontology` (공식 동일 keyword_match 로직):

| 지표 | A baseline | **B ontology (현행)** | Δ |
|---|---|---|---|
| **Passed** | 86/100 | **98/100** | **+12** |
| Hit@1 | 84 | 84 | 0 |
| Hit@3 | 87 | **99** | +12 |
| **Hit@5** | **88** | **100** ✅ | **+12** |
| Keyword match | 95 | 98 | +3 |
| Avg MRR | 0.856 | **0.8925** | +0.037 |
| 평균 응답 | 1538ms | 1893ms | +355ms |

**카테고리별 Hit@5:** rfc 100% / **ccie 60% → 100%** / ko 100% / edge 100%

남은 실패 2건: CCIE-029 VRF, CCIE-030 VLAN 4094 (Hit@5는 통과, keyword_match만 실패).

---

## 이번 작업 단계별 결과

### M3-C+ — CLI/API 정식 통합

**`mdrag search "OSPF area 설정" --mode ontology` 운영 사용 가능.**

추가 컴포넌트:
- `src/markdown_rag/config.py` — `search_mode: "vector"|"hybrid"|"ontology"` literal 확장 + `onto_*` 설정 8개
- `src/markdown_rag/retriever/builder.py` — `build_search_engine(settings, mode_override)` 팩토리 + `SearchEngine` Protocol
- `src/markdown_rag/cli/main.py` — search/ask 서브명령에 `--mode {vector,hybrid,ontology}` 인자
- `src/markdown_rag/cli/search_cmd.py` — builder 사용 + `[ONTO CARD]` / `[INJECTED via ...]` 출력 태그
- `src/markdown_rag/cli/ask_cmd.py` — builder 사용
- `src/markdown_rag/api/schemas.py` — `SearchRequest.mode` / `AskRequest.mode` / `ChunkResponse.via_onto_card/referenced_paths/injected_by_onto_card`
- `src/markdown_rag/api/routes/search.py` + `ask.py` — builder + ontology metadata serialization

운영 사용 예 (실측 결과):
```
$ mdrag search "OSPF area 설정" --mode ontology -k 5
[1] 다산 OSPF 매뉴얼 (direct)
[2] concept-ospf-area.md  [ONTO CARD]   Refs: ...CCIE_Vol1/...sec-04.md
[3] CCIE Vol1 part-iii sec-04             [INJECTED via concept-ospf-area.md]
[4] CCIE Vol1 sec-03                      [INJECTED via proto-ospf.md]
[5] 유비쿼스 OLT OSPF Area 매뉴얼 (direct)
```

### M3-B — `validate_rag.py` 정식 통합

- `--ontology-mode {off,vector,hybrid,ontology}` 인자 추가
- 기존 평가 로직(keyword_match 등)을 그대로 사용 → **절대값 비교 가능** (ablation 스크립트는 약간 다른 로직이라 절대값 불일치 문제 해결)
- 정식 측정 결과: passed 86 → 98, Hit@5 88 → 100

### M3-D — 응용계층 RFC 카드 9장

| 카드 | 의미 |
|---|---|
| `proto-dns.md` + `concept-dns-record-types.md` + `rfc-1035.md` | DNS (A/MX/CNAME 등) |
| `proto-http.md` + `rfc-2616.md` + `rfc-9110.md` | HTTP/1.1, HTTP semantics |
| `proto-smtp.md` + `rfc-5321.md` | SMTP/ESMTP |
| `rfc-1918.md` | private IP 10/8, 172.16/12, 192.168/16 |

validation_dataset에는 영향 없음 (RFC 카테고리 이미 100%) — 실 사용자 응용계층 질문 cover 목적.

### M3-E — false positive 정리

over-match가 의심됐던 카드의 keywords에서 일반 토큰 제거:

| 카드 | 제거된 일반 토큰 | 남긴 정밀 토큰 |
|---|---|---|
| `concept:acl-extended` | tcp, udp, icmp, permit, deny, port, protocol, 5-tuple, source IP, destination IP | extended ACL, access-list 100-199, wildcard mask, named access-list |
| `concept:acl-standard` | permit, deny, source IP | standard ACL, access-list 1-99 |
| `model:dasan-v3024v/vb/v6824xg/v8500` | "L2 switch", "24 port", "10G", "battery" 등 일반 | 모델 식별자만 |
| `model:ubiquoss-e5708r/e5924l/u9532h/p8624` | "L2 switch", "GbE", "LED status" 등 | 모델 식별자만 |

재검증 결과: Hit@5 100/100 **유지** (false positive 제거에도 성능 손실 없음 = 정확한 카드만 cover에 기여).

### M4 Stage 1 — 결정론적 onto-id 후보 추출

전체 main corpus 515,043 chunks에 onto 후보 부여 (~2분).

산출물:
- `scripts/extract_onto_candidates.py` (~280 LOC)
- `data/ontology/chunk_enrichment.jsonl.gz` (4.6MB, 515,043 records)
- `data/ontology/chunk_enrichment.jsonl.stats.json`

**커버리지 통계:**
- ANY onto tag 부여: 332,362 chunks (**64.5%**)
- Corpus tier: standard(RFC) 94.3%, implementation(벤더) 4.8%, theory(CCIE) 1.0%
- Vendor: dasan 17,070 / ubiquoss 7,415 / cisco 5,023

**Top 매칭 (Protocol):** proto:nat 138K, proto:rip 50K, proto:ipv6 25K, proto:tcp 23K, proto:bgp 9.8K, proto:ospf 6.6K
**Top 매칭 (Concept):** concept:ospf-area 1764, concept:ospf-lsa 1702, concept:mac-learning 952
**Top 매칭 (Feature):** feat:power-supply 26K, feat:port-mirroring 3.6K, feat:clock-config 3.3K

**False positive 의심 (Stage 2 LLM 검증 대상):**
- `proto:nat` 138K: "NAT" 약어가 RFC 본문에 자주 등장 → 일부 false positive 가능
- `proto:rip` 50K: 영어 일반어 "rip" 매칭 의심
- `feat:power-supply` 26K: "power" 일반어 매칭 의심

이들은 alias_dictionary의 `require_context_tokens`에 추가하면 좁힐 수 있다 (다음 작업 후보).

---

## 누적 산출물

### 카드 인벤토리 (69장)

| 타입 | 수 | 변화 |
|---|---|---|
| Protocol | 18 (+3) | + DNS, HTTP, SMTP |
| Concept | 14 (+1) | + DNS record types |
| RFC | 13 (+4) | + 1035, 2616, 9110, 5321, 1918 (단, 9110 sec-* 분할 없음) |
| Standard | 3 | (M2 그대로) |
| Feature | 7 | (M2.5 그대로) |
| Vendor | 2 | (M2.5 그대로) |
| DeviceModel | 8 | (M2.5 그대로) |
| **합계** | **69** | (M3-A 60 + M3-D 9) |

ontology Chroma index: 69 docs / 392 chunks.

### 코드 컴포넌트

| 파일 | 역할 | LOC |
|---|---|---|
| `src/markdown_rag/config.py` | onto_* 설정 + literal 확장 | +12 |
| `src/markdown_rag/retriever/builder.py` | 모드별 빌더 팩토리 + Protocol | 150 |
| `src/markdown_rag/retriever/ontology_aug.py` | OntologyAugmentedSearch | 280 |
| `src/markdown_rag/cli/main.py` | --mode 인자 | +14 |
| `src/markdown_rag/cli/search_cmd.py` | builder 사용 + ontology 출력 | -25/+45 |
| `src/markdown_rag/cli/ask_cmd.py` | builder 사용 | -20/+10 |
| `src/markdown_rag/api/schemas.py` | mode field + ontology metadata | +12 |
| `src/markdown_rag/api/routes/search.py` | builder + serializer | -10/+30 |
| `src/markdown_rag/api/routes/ask.py` | builder + serializer | -20/+10 |
| `scripts/build_ontology_refs.py` | 빌드: 카드 → onto_refs.json | 130 |
| `scripts/extract_onto_candidates.py` | M4 Stage 1 추출 | 280 |
| `scripts/validate_rag.py` | --ontology-mode 인자 | -40/+25 |
| `scripts/validate_rag_ablation.py` | (M3 ablation, 보관용) | 280 |
| `scripts/validate_rag_ontoaug.py` | (M3-C 검증, 보관용) | 230 |

### 데이터 산출물

| 파일 | 크기 | 내용 |
|---|---|---|
| `data/chroma_ontology/` | (Chroma) | 69 카드 → 392 chunks |
| `data/bm25_ontology/` | (BM25S) | ontology BM25 |
| `data/ontology/onto_refs.json` | ~30KB | 52 카드 → 114 injectable + 92 directory hints |
| `data/ontology/index.json` | ~10KB | 69 엔티티 ID → 파일 매핑 |
| `data/ontology/alias_index.json` | ~12KB | 368+ 별칭 → canonical ID |
| `data/ontology/chunk_enrichment.jsonl.gz` | 4.6MB | 515,043 chunks의 onto 후보 |
| `data/ontology/chunk_enrichment.jsonl.stats.json` | 2.1KB | 매칭 통계 |

### 리포트 (5건)

- `reports/ontology/m2_coverage_report.md` (M2)
- `reports/ontology/m2.5_ko_enhancement_report.md` (KO 보강)
- `reports/ontology/m3_ablation_report.md` (ablation 첫 측정)
- `reports/ontology/m3a_remaining_cover_report.md` (CCIE 잔여 cover)
- `reports/ontology/m3c_integration_report.md` (운영 클래스)
- 본 리포트 (M3-C+/B/D/E + M4-S1)

---

## 운영 사용법

### CLI
```bash
# Vector only (default if settings.search_mode == "vector")
mdrag search "OSPF area" -k 5

# Hybrid (Chroma + BM25 RRF)
mdrag search "OSPF area" --mode hybrid -k 5

# Ontology-augmented (main hybrid + onto hybrid + referenced-path expansion)
mdrag search "OSPF area" --mode ontology -k 5

# Ask
mdrag ask "다산 V58xx에서 OSPF area 설정 방법은?" --mode ontology
```

### API
```http
POST /api/v1/search
{
  "query": "OSPF area 설정",
  "top_k": 5,
  "mode": "ontology"
}
```
응답의 `chunk.via_onto_card`, `chunk.referenced_paths`, `chunk.injected_by_onto_card` 필드로 origin 확인 가능.

### Programmatic
```python
from markdown_rag.config import get_settings
from markdown_rag.retriever.builder import build_search_engine

engine = build_search_engine(get_settings(), mode_override="ontology")
results = engine.search("OSPF area 설정", top_k=5)
```

### 빌드 재실행 (카드 추가/수정 시)
```bash
# 1. ontology Chroma + BM25 재빌드
python scripts/reindex_optimized.py --input input_ontology \
  --chroma-path data/chroma_ontology \
  --collection markdown_docs_ontology \
  --bm25-path data/bm25_ontology

# 2. onto_refs.json 재생성
python scripts/build_ontology_refs.py

# 3. (선택) 검증
python scripts/validate_rag.py --ontology-mode ontology
```

---

## 다음 단계 (M4 Stage 2/3, 미진행)

본 작업으로 운영 RAG 통합은 완료. 다음은 자동 확장 본격화:

### M4 Stage 2 — LLM 검증
`scripts/llm_tag_chunks.py` (미작성):
- `chunk_enrichment.jsonl.gz`의 후보를 EXAONE 4.0 / Claude로 검증
- false positive (proto:nat 138K 중 의심분) 제거
- document-level pre-summarize 후 chunk broadcast 전략

### M4 Stage 3 — 관계 자동 도출
`scripts/extract_relations.py` (미작성):
- 같은 청크에 공출현한 onto_ids 페어를 LLM으로 predicate 분류
- `input_ontology/_relations/relations.jsonl`에 추가

### M4 Stage 4 — Chroma metadata patch
`scripts/enrich_chunks.py` (미작성):
- 검증된 onto_ids를 Chroma collection의 chunk metadata에 patch
- 재인덱싱 없이 metadata-only update
- 이후 검색 시 `where={"onto_protocol_ids": "proto:ospf"}` 같은 filter 가능

### M4 Stage 5 — Query-time onto-id 추출
- 사용자 쿼리에서 onto_id를 추론 → Chroma where filter로 retrieval 정밀화
- `src/markdown_rag/retriever/query_filter.py`에 통합

각 Stage는 별도 계획 후 진행 권장 (LLM 비용·시간 추정 필요).

---

## 결론

| 단계 | Hit@5 | 작업 |
|---|---|---|
| baseline | 88% | (기존) |
| M2 | (cover 84%) | 카드 34장 |
| M2.5 | (cover 95%) | KO 보강 53장 |
| M3 | 96% | ablation 첫 측정 |
| M3-A | 100% | CCIE 잔여 cover, 60장 |
| M3-C | 100% | 운영 클래스화 |
| **M3-C+/B/D/E + M4-S1** | **100% (운영 가능)** | **CLI/API 통합 + 응용계층 + false positive 정리 + 결정론적 추출** |

baseline 대비 전체 Hit@5 **+12%p**, CCIE Hit@5 **+40%p**. **운영 RAG에 완전 통합** 완료. 50만 chunk의 결정론적 onto 후보 추출 완료, 후속 LLM 검증 단계 준비됨.
