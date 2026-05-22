---
id: concept:vlan-trunk
type: Concept
name_en: VLAN Trunk
name_ko: VLAN 트렁크
parent_protocol: proto:vlan
scope: role
aliases:
  - trunk port
  - trunking
  - 802.1Q trunk
  - tagged port
defined_by:
  - std:ieee-802.1q
related:
  - proto:vlan
  - feat:dot1q-tunnel
  - concept:vlan-tag
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-05.md"
keywords_en:
  - trunk
  - tagged
  - native VLAN
  - allowed VLAN
  - DTP
  - ISL
  - 802.1Q
  - dot1q
keywords_ko:
  - 트렁크
  - 태깅
  - 네이티브
  - 허용 VLAN
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

VLAN Trunk는 단일 물리 링크 위에 다수 VLAN 트래픽을 전달하는 포트 모드다. 프레임에 802.1Q 태그(VID 포함)를 붙여 보내므로 수신 측은 어느 VLAN의 트래픽인지 식별한다. 스위치-스위치 또는 스위치-라우터(Router-on-a-Stick) 사이에서 사용된다. 반대 개념은 Access 포트(단일 VLAN, untagged).

## Access vs Trunk

| 구분 | Access | Trunk |
|---|---|---|
| VLAN 수 | 1개 | 다수 (4094개 가능) |
| 프레임 태깅 | Untagged | Tagged (Native 제외) |
| 용도 | 호스트/단말 연결 | 스위치-스위치 |
| 명령어 (Cisco) | `switchport mode access` | `switchport mode trunk` |

## Native VLAN

802.1Q trunk에서 태그 없이 전송되는 단일 VLAN. 기본값은 VLAN 1.
- 양단 스위치의 native VLAN이 일치해야 함 (불일치 시 CDP 경고)
- 보안 권장: native VLAN을 사용하지 않는 별도 VID로 변경

## 허용 VLAN (Allowed VLAN)

Trunk에서 통과시킬 VLAN 목록 제한:
- Cisco: `switchport trunk allowed vlan 10,20,30`
- 명시하지 않으면 모든 VLAN(1~4094) 허용

## 트렁킹 프로토콜

- **DTP** (Dynamic Trunking Protocol, Cisco 독점): 트렁크 모드 자동 협상
- **VTP** (VLAN Trunking Protocol, Cisco 독점): VLAN 데이터베이스 동기화
- **802.1Q** (표준): 태깅 형식만 정의, 협상 프로토콜 없음

## 검색 힌트

- "Access vs Trunk" → 본 카드 비교 표
- "Native VLAN" → 본 카드 Native 섹션
- "trunk allowed vlan" → 본 카드 허용 VLAN 섹션
- "DTP 트렁크 협상" → 본 카드 트렁킹 프로토콜 섹션
