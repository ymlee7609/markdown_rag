---
id: concept:stp-root-bridge
type: Concept
name_en: STP Root Bridge
name_ko: STP 루트 브리지
parent_protocol: proto:stp
scope: role
aliases:
  - root bridge
  - root switch
  - root bridge election
defined_by:
  - std:ieee-802.1d
related:
  - proto:stp
  - proto:rstp
  - proto:mstp
  - concept:stp-port-states
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-02.md"
keywords_en:
  - root bridge
  - root switch
  - bridge ID
  - bridge priority
  - root election
  - lowest bridge ID
keywords_ko:
  - 루트 브리지
  - 루트 스위치
  - 브리지 ID
  - 우선순위
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

Root Bridge는 STP 네트워크에서 모든 경로 계산의 기준이 되는 단 하나의 스위치다. 모든 비루트 스위치는 루트까지의 최단 경로를 선택해 다른 모든 경로를 Blocking 상태로 막아 루프 없는 트리 위상을 만든다. Root Bridge는 BPDU 교환 결과 **가장 낮은 Bridge ID** 를 가진 스위치로 선출된다.

## Bridge ID 구조

Bridge ID는 8바이트:
- **Bridge Priority** (2바이트, 0~65535, 기본 32768)
- **Bridge MAC Address** (6바이트)

비교 순서:
1. Priority가 낮은 쪽이 우선
2. Priority가 같으면 MAC이 낮은 쪽이 우선

## 선출 메커니즘

1. 모든 스위치는 자신을 루트라고 가정하고 BPDU 송신
2. 더 낮은 Bridge ID를 가진 BPDU를 받으면 자신의 BPDU 갱신, 그 방향이 root port
3. Hello timer(기본 2초)마다 BPDU 재송신
4. 수렴 후 모든 스위치는 동일한 루트로 합의

## Extended System ID (PVST)

Cisco PVST/RSTP에서 VLAN당 별도 STP 인스턴스를 위해 Bridge Priority의 하위 12비트를 VLAN ID로 사용. 실제 priority 값은 4096 배수만 가능.

## Root Bridge 강제 설정

운영자가 의도한 스위치를 루트로 만들려면 Bridge Priority를 낮춤:
- Cisco: `spanning-tree vlan 10 priority 4096`
- 또는 `spanning-tree vlan 10 root primary` (Cisco가 충분히 낮게 자동 설정)

## 검색 힌트

- "STP 루트 브리지 선출" → 본 카드 선출 메커니즘 섹션
- "Bridge ID 구조" → 본 카드 Bridge ID 섹션
- "STP priority 설정" → 본 카드 + 벤더 매뉴얼
- "root primary" → 본 카드 강제 설정 섹션
