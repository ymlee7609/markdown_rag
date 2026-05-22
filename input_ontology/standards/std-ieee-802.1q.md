---
id: std:ieee-802.1q
type: Standard
sdo: ieee
doc_id: "IEEE 802.1Q"
title: "IEEE Standard for Local and metropolitan area networks - Bridges and Bridged Networks"
status: active
year: 2022
defines:
  - proto:vlan
  - concept:vlan-trunk
  - concept:vlan-tag
keywords_en:
  - 802.1Q
  - VLAN
  - VLAN tagging
  - dot1q
  - trunk
  - VID
  - TPID
  - PCP
  - DEI
  - QinQ
  - 802.1ad
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

IEEE 802.1Q는 VLAN(Virtual LAN) 태깅과 가상 브리지된 네트워크를 정의하는 IEEE 표준이다. 이더넷 프레임에 4바이트 802.1Q 태그(TPID 0x8100 + TCI: PCP/DEI/VID)를 삽입해 동일 물리 매체 위에 여러 논리 LAN을 구성한다. 2014년 판부터 STP/RSTP/MSTP까지 흡수했고, 2022년 판이 현행이다.

## 정의 대상

- **`proto:vlan`** — VLAN 프로토콜
- **`concept:vlan-trunk`** — Trunk 포트, 다중 VLAN 전송
- **`concept:vlan-tag`** — 802.1Q 태그 구조 (4바이트, TPID+TCI)

## 관련 표준

- **IEEE 802.1ad** (Provider Bridges) — Q-in-Q (`feat:dot1q-tunnel`)
- **IEEE 802.1ah** (Provider Backbone Bridges) — MAC-in-MAC
- 흡수된 표준: 802.1D (STP), 802.1w (RSTP), 802.1s (MSTP)

## 핵심 구조

802.1Q 태그(4바이트):
- TPID (16b) = 0x8100
- TCI:
  - PCP (3b) — Priority Code Point (QoS, 802.1p)
  - DEI (1b) — Drop Eligible Indicator
  - VID (12b) — VLAN ID (0~4095, 0/4095 예약)

## 검색 힌트

- "VLAN 표준" → 본 카드 (IEEE 802.1Q)
- "802.1Q 태그 구조" → 본 카드 핵심 구조 섹션
- "VLAN ID 범위" → 본 카드 (0~4095)
- "Q-in-Q" → 본 카드 + `feat:dot1q-tunnel` + IEEE 802.1ad
