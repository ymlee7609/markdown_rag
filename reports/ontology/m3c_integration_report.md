# M3-C 통합 리포트 — OntologyAugmentedSearch 운영 클래스화

생성일: 2026-05-22
이전: M3-A ablation Hit@5 100/100 (스크립트 내부 로직)
결과: 운영용 클래스로 동일 효과 재현 — Hit@5 100/100, MRR 0.9158

---

## 결론

ablation 스크립트(`validate_rag_ablation.py`) 내부에서만 동작하던 **referenced-path expansion 로직을 운영 RAG 모듈로 정식 통합**. `OntologyAugmentedSearch` 클래스는 기존 `HybridSearch`와 동일한 `search(query, top_k, where=None)` 시그니처를 가지므로 드롭인 교체 가능.

**검증 결과 (validate_rag_ontoaug.py 100건 평가):**
- Hit@5: **100/100** ✅ (M3-A ablation과 동일)
- MRR: **0.9158** ✅ (정확히 일치)
- via_onto hits: 15 (annotated 보조 카드 + injected 청크 합산)
- direct hits: 85
- 카테고리별 Hit@5: rfc 30/30, ccie 30/30, ko 30/30, edge 10/10

---

## 추가된 컴포넌트

### 1. `scripts/build_ontology_refs.py`
보조 카드 frontmatter에서 referenced paths를 추출해 `data/ontology/onto_refs.json` 생성.

- 입력: `input_ontology/` 카드 frontmatter (`taught_in`/`documented_in`/`corpus_paths`/`manual_paths`)
- 출력: `{card_path: {"injectable": [abs_paths], "directory_hints": [dirs]}}`
- 정규화: `--input-base input_optimized`로 ref path를 절대 경로 변환 (.md 파일만 injectable)
- 현재 인덱스: 48 카드 → 104 injectable paths + 90 directory hints

### 2. `src/markdown_rag/retriever/ontology_aug.py` — `OntologyAugmentedSearch`

운영 RAG에서 ontology corpus를 활용하는 정식 검색 클래스. 동작:

```
search(query, top_k):
  1. main_search.search(query, fetch_k=top_k*3)
  2. onto_search.search(query, fetch_k=top_k*3)
  3. RRF union → fused
  4. 보조 카드(input_ontology/...) hit에 metadata 부착:
     - via_onto_card: True
     - referenced_paths_injectable: [...]
     - referenced_paths_directories: [...]
  5. 상위 inject_top_n_cards (기본 3) 카드의 injectable paths에 대해
     main_store에서 청크 lookup → 결과에 inject (boost score)
     - inject된 청크에는 injected_by_onto_card: <card_filename> 부착
  6. score 재정렬 → top_k 반환
```

기존 `HybridSearch`와 동일한 `search()` 시그니처. 드롭인 교체 가능.

추가 메서드:
- `explain(results)`: 각 결과의 origin (`main_search` / `ontology_card` / `injected`) 추적 정보 반환 — LLM 프롬프트 빌딩이나 디버그용

### 3. `scripts/validate_rag_ontoaug.py`
새 클래스 검증 스크립트. 100건 평가, hit reason 분류.

---

## 운영 RAG 통합 가이드

### 기본 교체

```python
# Before
from markdown_rag.retriever.hybrid import HybridSearch
engine = HybridSearch(semantic_search=sem, bm25_index=bm25, alpha=0.7)
results = engine.search(query, top_k=5)

# After (ontology 증강)
from markdown_rag.retriever.hybrid import HybridSearch
from markdown_rag.retriever.ontology_aug import OntologyAugmentedSearch

main_engine = HybridSearch(semantic_search=main_sem, bm25_index=main_bm25, alpha=0.7)
onto_engine = HybridSearch(semantic_search=onto_sem, bm25_index=onto_bm25, alpha=0.7)

engine = OntologyAugmentedSearch(
    main_search=main_engine,
    onto_search=onto_engine,
    main_store=main_chroma_store,
    onto_refs_path="data/ontology/onto_refs.json",
)
results = engine.search(query, top_k=5)
```

### 결과의 metadata 활용

LLM 프롬프트 빌더는 SearchResult의 `chunk.metadata`를 보고 origin별로 다르게 처리 가능:

| Metadata 키 | 의미 | 활용 |
|---|---|---|
| `via_onto_card: True` | 결과 chunk가 ontology 보조 카드 자체 | "관련 개념 카드" 섹션에 표시 |
| `referenced_paths_injectable` | 카드의 ref 절대 경로 | LLM에 추가 컨텍스트 힌트 |
| `referenced_paths_directories` | 카드의 ref 디렉토리 | "관련 매뉴얼 디렉토리" 안내 |
| `injected_by_onto_card: <name>` | ref path 따라 자동 inject된 청크 | 출처 표시 (XX 카드 참고) |

### `explain()` 사용 예

```python
results = engine.search("OSPF area 설정 방법", top_k=5)
trace = engine.explain(results)
# trace = [
#   {"doc_path": "...", "origin": "main_search", "score": ...},
#   {"doc_path": "...proto-ospf.md", "origin": "ontology_card",
#    "referenced_paths_injectable": [...], ...},
#   {"doc_path": "...CCIE_Vol1/...sec-04.md", "origin": "injected",
#    "injected_by_onto_card": "proto-ospf.md", ...},
# ]
```

---

## 성능

| 단계 | 100건 평가 시간 | 건당 평균 |
|---|---|---|
| ablation 스크립트 (M3-A) | 159.5s | 1.60s |
| OntologyAugmentedSearch (M3-C) | 201.1s | 2.01s |

차이 +0.4s/건. inject lookup(ChromaStore.get with where)이 추가 비용. inject_chunks_per_card=1 기본값에서 카드당 1회 추가 query. inject_top_n_cards=3이라 최대 카드당 3 query (3 inject_top × 1 chunk).

추가 비용은 운영 가능 수준. 더 엄격한 latency 목표가 있다면:
- `inject_top_n_cards=2`로 낮춤 (가장 점수 높은 보조 카드 2개만)
- `inject_chunks_per_card=0`로 lookup 비활성화 (annotation만, MRR 효과는 유지)

---

## 다음 단계 권고

M3-C 완료. 운영 RAG에 통합 가능한 상태. 다음:

1. **M3-C+ (선택)** — `cli/search_cmd.py`나 `api/app.py`에 `--ontology` 플래그/파라미터 추가 → 사용자가 옵션으로 활성화
2. **M3-B** — `scripts/validate_rag.py`에 `--ontology-mode` 인자 통합 + keyword_match 로직 일치화 (절대값 비교 가능하도록)
3. **M3-D** — RFC 응용계층 카드 (DNS/HTTP/SMTP/RFC1918) — validation_dataset 평가에는 영향 없지만 실 사용자 질문 cover 보완
4. **M3-E** — False positive 정리 (acl-extended 28회 over-match 등)
5. **M4 — LLM 자동 확장 파이프라인** (원 plan의 M3) — `extract_onto_candidates.py` / `llm_tag_chunks.py` / `extract_relations.py` 등 longtail 자동 추출

권장: **M3-C+** (CLI/API 노출)이 가장 즉시 가치. 그다음 M3-B(평가 통합).

---

## 산출물

| 파일 | 역할 |
|---|---|
| `scripts/build_ontology_refs.py` | 빌드: 카드 frontmatter → onto_refs.json |
| `data/ontology/onto_refs.json` | 48 카드, 104 injectable + 90 directory hints |
| `src/markdown_rag/retriever/ontology_aug.py` | OntologyAugmentedSearch 클래스 (~280 LOC) |
| `scripts/validate_rag_ontoaug.py` | 신규 클래스 검증 스크립트 |
| `reports/ontology/m3c_ontoaug_20260522_103544.json` | 검증 원시 결과 |
| 본 리포트 | M3-C acceptance |

---

## 누적 진척도

| 단계 | 산출물 | Hit@5 |
|---|---|---|
| baseline | (기존 12k corpus) | 88% |
| M2 (스키마 + 샘플 카드) | 34장 + 스키마 | (cover 84%) |
| M2.5 (KO 보강) | 53장 | (cover 95%) |
| M3 (ablation) | + ablation 스크립트 | 96% |
| M3-A (CCIE 잔여) | 60장 | **100%** |
| **M3-C (정식 통합)** | + OntologyAugmentedSearch 클래스 | **100% (운영 가능)** |

총 코드/문서 작성:
- 카드 60장 (input_ontology/)
- 스키마/사전 4개
- 빌드 스크립트 2개 (`build_ontology_refs.py`, 기존 `reindex_optimized.py` 재사용)
- 평가 스크립트 2개 (`validate_rag_ablation.py`, `validate_rag_ontoaug.py`)
- 통합 모듈 1개 (`retriever/ontology_aug.py`)
- 리포트 4건 (M2.5, M3, M3-A, M3-C)
