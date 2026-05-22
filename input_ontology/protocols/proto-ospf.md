---
id: proto:ospf
type: Protocol
name_en: OSPF
name_ko: 개방형 최단 경로 우선 (OSPFv2)
aliases:
  - OSPFv2
  - Open Shortest Path First
layer: L3
family: IGP
status: active
defined_by:
  - rfc:2328
extends: []
related:
  - proto:ospfv3
  - proto:isis
  - concept:ospf-lsa
  - concept:ospf-area
  - concept:ospf-neighbor
references:
  - rfc:1583   # OSPF v2 이전 버전 (obsoleted)
  - rfc:2178   # OSPF v2 이전 버전 (obsoleted)
  - rfc:3101   # NSSA option
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-03.md"
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-04.md"
documented_in:
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L3"
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - LSA
  - area
  - ABR
  - ASBR
  - hello
  - dead-interval
  - DR
  - BDR
  - SPF
  - Dijkstra
  - link-state
keywords_ko:
  - 영역
  - 인접관계
  - 헬로
  - 링크 상태
  - 최단 경로
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

OSPF(Open Shortest Path First)는 링크 상태(link-state) 기반의 IGP(Interior Gateway Protocol) 라우팅 프로토콜이다. 단일 자율 시스템(AS) 내부에서 라우터 간 라우팅 정보를 교환하며, Dijkstra 최단 경로 알고리즘으로 라우팅 테이블을 계산한다. RFC 2328이 IPv4용 OSPFv2를 정의하고, IPv6용은 OSPFv3 (RFC 5340)로 별도 확장되었다.

## 표준 / 정의

- **RFC 2328** — OSPF Version 2 (STD 54, 표준): 현행 OSPFv2 정식 사양
- **RFC 5340** — OSPF for IPv6 (OSPFv3): IPv6 환경 확장 (별도 카드 `proto:ospfv3`)
- 폐기 체인:
  - RFC 1247 → RFC 1583 → RFC 2178 → **RFC 2328** (현행)
- 주요 보완 RFC:
  - RFC 3101 — NSSA (Not-So-Stubby Area) 옵션
  - RFC 5709 — HMAC-SHA 인증
  - RFC 6549 — OSPFv2 다중 인스턴스 확장

## 핵심 개념

- [LSA Types](../concepts/concept-ospf-lsa.md) — Type 1~7 링크 상태 광고
- [OSPF Area](../concepts/concept-ospf-area.md) — backbone / stub / NSSA / totally-stubby
- [Neighbor / Adjacency](../concepts/concept-ospf-neighbor.md) — Hello, DR/BDR 선출, FSM

## 벤더 구현 매핑

| Vendor | 주요 명령어 | 매뉴얼/문서 위치 |
|---|---|---|
| Cisco (CCIE) | `router ospf <pid>`, `network`, `area` | `Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-04.md` |
| Dasan L3 | `router ospf`, `network ... area`, `interface ospf` | `가입자망장비_manual/다산_L3/` (모델별 sec 참조) |
| Ubiquoss L3 | `ip ospf area`, `router ospf` | `가입자망장비_manual/유비쿼스_L3/` |

> 1차 구축에서는 Command 카드를 별도 생성하지 않는다. Feature/Command 수준은 M3 LLM 확장에서 추출 예정.

## 교차 참조

- **이론 학습**: Cisco CCIE Vol1 Part II IP Networking sec-03 (개요), Part III IGP Routing sec-04 (상세)
- **표준 원문**: `input_optimized/IETF_RFC/rfc2328__sec-*.md` (sec-01 ~ sec-NN)
- **IPv6 변형**: `proto:ospfv3` 카드 → RFC 5340
- **관련 프로토콜**:
  - `proto:isis` — 또 다른 link-state IGP, IGP 선택 시 트레이드오프
  - `proto:bgp` — EGP, OSPF와 redistribute 관계
  - `proto:rip` — Distance-vector IGP, OSPF로 대체되는 경향

## 검색 힌트 (RAG용)

이 카드는 다음 유형의 질문에서 활용된다:
- "OSPF area는 무엇인가?" → 본 카드 + `concept:ospf-area`
- "RFC 2328이 정의하는 프로토콜은?" → 본 카드 + `rfc:2328` (defined_by 역참조)
- "다산 V58xx에서 OSPF 설정하는 방법" → 본 카드 documented_in + 매뉴얼 청크
- "OSPF와 IS-IS 차이" → 본 카드 + `proto:isis` (related 확장)
