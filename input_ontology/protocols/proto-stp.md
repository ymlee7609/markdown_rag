---
id: proto:stp
type: Protocol
name_en: STP
name_ko: 스패닝 트리 프로토콜
aliases:
  - Spanning Tree Protocol
  - 802.1D
layer: L2
family: bridging
status: active
defined_by:
  - std:ieee-802.1d
extends: []
related:
  - proto:rstp
  - proto:mstp
  - concept:stp-root-bridge
  - concept:stp-port-states
  - concept:stp-bpdu
references: []
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-01.md"
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-02.md"
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-03.md"
documented_in:
  - "가입자망장비_manual/다산_L2"
  - "가입자망장비_manual/유비쿼스_L2"
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - STP
  - 802.1D
  - root bridge
  - BPDU
  - blocking
  - listening
  - learning
  - forwarding
  - bridge ID
  - path cost
  - PortFast
  - BPDU Guard
keywords_ko:
  - 스패닝트리
  - 루트 브리지
  - 루트 스위치
  - 포트 상태
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

STP(Spanning Tree Protocol, IEEE 802.1D)는 L2 이더넷 네트워크에서 브리지/스위치 간 루프를 방지하는 프로토콜이다. 모든 스위치 중 가장 낮은 Bridge ID를 가진 스위치를 루트 브리지로 선출하고, 루트로부터의 최단 경로 외의 중복 링크를 Blocking 상태로 막아 루프 없는 트리 위상을 만든다. 수렴 속도가 느려(30~50초) 현장에서는 RSTP(802.1w) 또는 MSTP(802.1s)로 대체되는 추세.

## 표준 / 정의

- **IEEE 802.1D-2004** — STP 마지막 독립 표준판
- IEEE 802.1Q-2014 이후로 802.1D가 흡수 통합됨

## 핵심 개념

- [Root Bridge Election](../concepts/concept-stp-root-bridge.md) — Bridge ID(우선순위+MAC) 비교
- [Port States](../concepts/concept-stp-port-states.md) — Disabled/Blocking/Listening/Learning/Forwarding 5단계
- [BPDU](../concepts/concept-stp-bpdu.md) — Bridge Protocol Data Unit, Hello 2초 간격

## 벤더 구현 매핑

| Vendor | 주요 명령어 | 매뉴얼/문서 |
|---|---|---|
| Cisco | `spanning-tree mode pvst|rapid-pvst|mst`, `spanning-tree vlan ... priority` | `Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-01~03.md` |
| Dasan L2 | `spanning-tree`, `spanning-tree priority` | `가입자망장비_manual/다산_L2/` |
| Ubiquoss L2 | `spanning-tree enable`, `spanning-tree priority` | `가입자망장비_manual/유비쿼스_L2/` |

## 변형 프로토콜

- `proto:rstp` — IEEE 802.1w, 빠른 수렴 (<1초)
- `proto:mstp` — IEEE 802.1s, 다중 인스턴스로 VLAN별 로드 밸런싱
- PVST/Rapid-PVST — Cisco 독점, VLAN당 STP/RSTP 1개

## 검색 힌트

- "STP 루트 브리지 선출" → 본 카드 + `concept:stp-root-bridge`
- "스패닝트리 포트 상태" → 본 카드 + `concept:stp-port-states`
- "BPDU" → `concept:stp-bpdu`
- "STP RSTP 차이" → 본 카드 + `proto:rstp`
- "다산 스위치 spanning-tree 설정" → 본 카드 documented_in + 매뉴얼
