---
id: proto:bgp
type: Protocol
name_en: BGP
name_ko: 경계 경로 프로토콜 (BGP-4)
aliases:
  - BGP-4
  - BGPv4
  - Border Gateway Protocol
layer: L3
family: EGP
status: active
defined_by:
  - rfc:4271
extends: []
related:
  - proto:ospf
  - concept:bgp-as-path
  - concept:bgp-update-message
  - concept:bgp-finite-state-machine
references:
  - rfc:1771   # BGP-4 이전 버전 (obsoleted)
  - rfc:6286
  - rfc:6793
  - rfc:7606
taught_in:
  - "Cisco_CCIE/CCIE_Vol2/03_part-i-ip-bgp-routing__sec-01.md"
  - "Cisco_CCIE/CCIE_Vol2/03_part-i-ip-bgp-routing__sec-02.md"
  - "Cisco_CCIE/CCIE_Vol2/03_part-i-ip-bgp-routing__sec-07.md"
documented_in:
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L3"
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - BGP
  - AS
  - AS_PATH
  - peer
  - neighbor
  - EBGP
  - IBGP
  - UPDATE
  - KEEPALIVE
  - NOTIFICATION
  - route-map
  - prefix-list
keywords_ko:
  - BGP
  - 경계
  - 자율시스템
  - 피어
  - 인접
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

BGP(Border Gateway Protocol Version 4)는 자율 시스템(Autonomous System) 간 경로 정보를 교환하는 외부 게이트웨이 프로토콜(EGP)이다. 인터넷 라우팅의 사실상 표준이며, TCP 179번 포트 위에서 동작한다. EBGP(External, 서로 다른 AS 간)와 IBGP(Internal, 같은 AS 내) 두 모드로 동작한다.

## 표준 / 정의

- **RFC 4271** — A Border Gateway Protocol 4 (BGP-4), 2006-01: 현행 정식 사양
- 폐기 체인: RFC 1105 → 1163 → 1267 → 1654 → 1771 → **4271 (현행)**
- 주요 갱신 RFC:
  - RFC 6793 — 4-Octet AS Number Support
  - RFC 7606 — Revised Error Handling for UPDATE
  - RFC 8212 — Default EBGP Route Propagation Behavior

## 핵심 개념

- [AS-PATH](../concepts/concept-bgp-as-path.md) — 경로 속성, 루프 방지
- UPDATE message — 경로 광고/철회
- BGP FSM — Idle → Connect → Active → OpenSent → OpenConfirm → Established

## 벤더 구현 매핑

| Vendor | 주요 명령어 | 매뉴얼/문서 |
|---|---|---|
| Cisco | `router bgp <asn>`, `neighbor`, `network`, `route-map` | `Cisco_CCIE/CCIE_Vol2/03_part-i-ip-bgp-routing__sec-*.md` |
| Dasan L3 | `router bgp`, `neighbor remote-as` | `가입자망장비_manual/다산_L3/` |
| Ubiquoss L3 | `router bgp`, `neighbor` | `가입자망장비_manual/유비쿼스_L3/` |

## 교차 참조

- **이론 학습**: Cisco CCIE Vol2 Part I IP BGP Routing 전체 (sec-01 ~ sec-07)
- **표준 원문**: `input_optimized/IETF_RFC/rfc4271__sec-*.md`
- **관련 프로토콜**:
  - `proto:ospf` — IGP, BGP와 redistribute 가능
  - `proto:tcp` — BGP는 TCP 179 위에서 동작

## 검색 힌트

- "BGP AS-PATH" → 본 카드 + `concept:bgp-as-path`
- "EBGP IBGP 차이" → 본 카드 + CCIE Vol2 sec-01
- "BGP는 어느 RFC?" → `rfc:4271` 역참조
- "다산 BGP 설정" → 본 카드 documented_in + 매뉴얼 청크
