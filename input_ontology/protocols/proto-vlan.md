---
id: proto:vlan
type: Protocol
name_en: VLAN
name_ko: 가상 LAN (VLAN)
aliases:
  - Virtual LAN
  - 802.1Q
  - dot1q
layer: L2
family: bridging
status: active
defined_by:
  - std:ieee-802.1q
extends: []
related:
  - concept:vlan-trunk
  - concept:vlan-tag
  - feat:dot1q-tunnel
references: []
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-04.md"
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-05.md"
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-07.md"
documented_in:
  - "가입자망장비_manual/다산_L2"
  - "가입자망장비_manual/유비쿼스_L2"
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L3"
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - VLAN
  - 802.1Q
  - dot1q
  - VID
  - trunk
  - access port
  - tagged
  - untagged
  - native VLAN
  - voice VLAN
  - TPID
  - PCP
keywords_ko:
  - VLAN
  - 가상랜
  - 트렁크
  - 액세스 포트
  - 태깅
  - 네이티브
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

VLAN(Virtual LAN)은 동일 물리 매체 위에 여러 논리적 LAN을 구성하는 L2 기술이다. IEEE 802.1Q 표준이 정의하는 4바이트 태그(TPID 0x8100 + VID 12비트)를 이더넷 프레임에 삽입해 VLAN ID 0~4095로 분리한다. Access 포트(단일 VLAN, untagged)와 Trunk 포트(다중 VLAN, tagged)로 운용된다.

## 표준 / 정의

- **IEEE 802.1Q** — VLAN 태깅, Bridges and Bridged Networks
- 확장: 802.1ad (Q-in-Q), 802.1ah (MAC-in-MAC)
- 흡수: 802.1D (STP), 802.1w (RSTP), 802.1s (MSTP)

## 핵심 개념

- [VLAN Trunk](../concepts/concept-vlan-trunk.md) — 다중 VLAN 전송, 802.1Q tagged
- [VLAN Tag](../concepts/concept-vlan-tag.md) — 4바이트 802.1Q 헤더 구조

## 벤더 구현 매핑

| Vendor | VLAN 생성 | Trunk 설정 | 매뉴얼 |
|---|---|---|---|
| Cisco | `vlan 10`, `name SALES` | `switchport mode trunk`, `switchport trunk allowed vlan 10,20` | `Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-04,05,07.md` |
| Dasan L2 | `bridge vlan add ...` (모델별 상이) | `bridge vlan tag-add ...` | `가입자망장비_manual/다산_L2/` |
| Ubiquoss L2 | `vlan create ...` | `switchport mode trunk` | `가입자망장비_manual/유비쿼스_L2/` |

## 관련 기능

- `feat:dot1q-tunnel` (Q-in-Q) — 서비스 VLAN으로 고객 VLAN 캡슐화
- voice VLAN — VoIP 단말 전용 VLAN
- private VLAN — 같은 VLAN 내 호스트 격리 (RFC 5517)

## 검색 힌트

- "VLAN 설정" → 본 카드 + 벤더 매뉴얼
- "Trunk vs Access" → 본 카드 + `concept:vlan-trunk`
- "VLAN 태그 구조" → 본 카드 + `concept:vlan-tag` + `std:ieee-802.1q`
- "Q-in-Q" → `feat:dot1q-tunnel`
- "다산 OLT VLAN" → 본 카드 documented_in + 가입자망 매뉴얼
