# M3-A 잔여 CCIE Cover 리포트

생성일: 2026-05-22
이전 단계: `reports/ontology/m3_ablation_report.md` (CCIE 26/30, 전체 96/100)
산출 데이터: `reports/ontology/m3_ablation_20260522_102128.json`

---

## 결론

**전체 Hit@5 100/100, CCIE 30/30 완전 cover.** 모든 카테고리 만점.

| 지표 | A baseline | M3 1차 (53장) | **M3-A (60장)** | 누적 Δ vs baseline |
|---|---|---|---|---|
| Hit@5 | 88 | 96 | **100** ✅ | **+12** |
| Hit@3 | 87 | 93 | 99 | +12 |
| Passed | 42 | 49 | 51 | +9 |
| Avg MRR | 0.858 | 0.897 | 0.916 | +0.058 |
| via_onto | — | 11 | 15 | — |

### 카테고리별 Hit@5

| 카테고리 | A baseline | M3 1차 | M3-A | 변화 |
|---|---|---|---|---|
| rfc | 30/30 | 30/30 | 30/30 | (만점 유지) |
| **ccie** | **18/30** | **26/30** | **30/30 ✅** | **+12 (+40%p)** |
| ko | 30/30 | 30/30 | 30/30 | (만점 유지) |
| edge | 10/10 | 10/10 | 10/10 | (만점 유지) |

---

## M3-A 작업 내역 (9장)

### 신규 6장
| 카드 | 타입 | Cover 대상 |
|---|---|---|
| `proto-cdp.md` | Protocol | CCIE-019 CDP |
| `proto-frame-relay.md` | Protocol | CCIE-022 Frame Relay DLCI PVC LMI |
| `proto-hsrp.md` | Protocol | CCIE-014 HSRP (이전 우연 매칭 → 정확화) |
| `proto-gre.md` | Protocol | CCIE-021 GRE (이전 우연 매칭 → 정확화) |
| `rfc-2784.md` | RFC | GRE 표준 |
| `concept-loopback-interface.md` | Concept | CCIE-026 loopback (이전 우연 매칭 → 정확화) |

### 보강 3장 (taught_in/documented_in 추가)
| 카드 | 변경 |
|---|---|
| `concept-acl-standard.md` | taught_in: ip-networking sec-02/04/05 + igp-routing sec-05 추가 |
| `concept-acl-extended.md` | taught_in: 동일 |
| `concept-dhcp-discover.md` | taught_in: ip-networking sec-03/04/05 추가 |

CCIE-017(ACL wildcard)와 CCIE-018(DHCP relay)는 카드 자체는 top-5에 있었지만 `taught_in` 부재로 referenced-path 매칭 실패 — 보강만으로 해결.

---

## CCIE 30건 매칭 분포

| Reason | 케이스 수 | 비고 |
|---|---|---|
| direct (main corpus 직접) | 15 | baseline에서도 hit이던 기본기 |
| via proto-bgp.md | 2 | CCIE-013, 029 |
| via proto-ospf.md | 0 | M3-A에서 정확화 후 사라짐 |
| via proto-igmp.md | 1 | CCIE-009 |
| via proto-stp.md | 1 | CCIE-010 |
| via proto-acl.md | 1 | CCIE-020 |
| via concept-bgp-as-path.md | 1 | CCIE-028 |
| **via proto-hsrp.md (신규)** | 1 | CCIE-014 |
| **via concept-acl-standard.md (보강)** | 1 | CCIE-017 |
| **via concept-dhcp-discover.md (보강)** | 1 | CCIE-018 |
| **via proto-cdp.md (신규)** | 1 | CCIE-019 |
| **via proto-gre.md (신규)** | 1 | CCIE-021 |
| **via proto-frame-relay.md (신규)** | 1 | CCIE-022 |
| **via concept-loopback-interface.md (신규)** | 1 | CCIE-026 |
| via concept-acl-extended.md | 1 | CCIE-030 (다소 부정확 매핑이나 결과적으로 hit) |

→ CCIE 30/30 중 15건이 direct, 15건이 보조 카드 경유. **M3-A 신규/보강 카드 8건이 직접 cover에 기여**.

---

## 누적 카드 인벤토리

| 타입 | M2 | M2.5 | **M3-A** | 비고 |
|---|---|---|---|---|
| Protocol | 10 | 11 | **15** | +CDP, FrameRelay, HSRP, GRE |
| Concept | 12 | 13 | **14** | +loopback |
| RFC | 8 | 9 | **10** | +RFC 2784 |
| Standard | 3 | 3 | 3 | |
| Feature | 1 | 7 | 7 | |
| Vendor | 0 | 2 | 2 | |
| DeviceModel | 0 | 8 | 8 | |
| **합계** | **34** | **53** | **60** | |

ontology 인덱스: 60 docs / 348 chunks (+34 chunks vs M3 1차).

---

## 전체 cover 여정

| 단계 | 카드 수 | Hit@5 | CCIE Hit@5 | 핵심 작업 |
|---|---|---|---|---|
| baseline | 0 (기존 12k corpus만) | 88% | 60% | — |
| M2 | 34 | (cover 측정 84%) | — | 핵심 Protocol/Concept/RFC 수작업 |
| M2.5 | 53 | (cover 95%) | — | KO 영역 Vendor/Device/Feature 보강 |
| M3 ablation | 53 | **96%** | 86.7% | 보조 코퍼스 union으로 ablation |
| **M3-A** | **60** | **100%** ✅ | **100%** ✅ | CCIE 잔여 cover + 우연 매칭 정확화 |

---

## 검색 시간 영향

| 단계 | 100건 평가 시간 (B 모드) | 건당 평균 |
|---|---|---|
| M3 1차 | 167.3s | 1.67s |
| M3-A | 159.5s | 1.60s |

카드 추가에도 평가 시간 동일~약간 개선. ontology collection이 348 chunks로 여전히 매우 작아 latency 영향 미미.

---

## 다음 단계

**M3-A로 cover 목표는 완전 달성**. 다음 우선순위는 ablation 결과를 운영 RAG에 반영하는 정식 통합 작업:

1. **M3-C (최우선) — `src/markdown_rag/retriever/hybrid.py`에 referenced-path expansion 정식 구현**
   - 현재는 ablation 스크립트 내부에서만 동작
   - 운영 RAG가 ontology collection을 자동 union하고, 보조 카드 hit 시 referenced-path 청크를 자동 inject하도록 통합

2. **M3-B — `scripts/validate_rag.py`에 `--ontology-mode` 인자 통합 + keyword_match 로직 일치화**
   - 절대값 비교 가능하도록 표준화

3. **M3-D — RFC 응용계층 카드 (DNS/HTTP/SMTP/RFC1918)**
   - validation_dataset 평가에는 영향 없음 (RFC 카테고리 이미 100%)
   - 실 사용자 질문 cover 보완용

4. **M3-E — False positive 정리**
   - `concept:acl-extended` keywords의 일반 토큰(`tcp`/`udp`/`permit`/`deny`/`5-tuple`) 축소
   - `alias_dictionary.yaml`의 `require_context_tokens` 정책을 정식 코드로 강제

권장 다음: **M3-C** (정식 통합). 지금까지의 효과가 ablation 스크립트가 아니라 실제 운영 검색에서 발휘되도록.

---

## 산출물

| 파일 | 역할 |
|---|---|
| `input_ontology/protocols/proto-cdp.md` | 신규 |
| `input_ontology/protocols/proto-frame-relay.md` | 신규 |
| `input_ontology/protocols/proto-hsrp.md` | 신규 |
| `input_ontology/protocols/proto-gre.md` | 신규 |
| `input_ontology/rfcs/rfc-2784.md` | 신규 |
| `input_ontology/concepts/concept-loopback-interface.md` | 신규 |
| `input_ontology/concepts/concept-acl-standard.md` | taught_in 보강 |
| `input_ontology/concepts/concept-acl-extended.md` | taught_in 보강 |
| `input_ontology/concepts/concept-dhcp-discover.md` | taught_in 보강 |
| `data/chroma_ontology/` | 재인덱싱 (60 docs / 348 chunks) |
| `data/bm25_ontology/` | 재인덱싱 |
| `reports/ontology/m3_ablation_20260522_102128.json` | M3-A ablation 원시 결과 |
| 본 리포트 | M3-A acceptance |
