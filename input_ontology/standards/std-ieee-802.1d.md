---
id: std:ieee-802.1d
type: Standard
sdo: ieee
doc_id: "IEEE 802.1D"
title: "IEEE Standard for Local and metropolitan area networks - Media Access Control (MAC) Bridges"
status: superseded
year: 2004
defines:
  - proto:stp
  - concept:stp-root-bridge
  - concept:stp-port-states
keywords_en:
  - 802.1D
  - MAC Bridges
  - Spanning Tree
  - STP
  - bridge forwarding
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

IEEE 802.1D는 MAC 브리지 동작과 STP(Spanning Tree Protocol)를 정의한 IEEE 표준이다. 2004년 판이 STP의 마지막 독립 정의 버전이며, 이후 IEEE 802.1Q-2014 등에 통합되어 흡수됐다. STP의 BPDU 형식·루트 브리지 선출·포트 상태 전이를 정의한다.

## 정의 대상

- **`proto:stp`** — Spanning Tree Protocol
- **`concept:stp-root-bridge`** — 루트 브리지 선출, Bridge ID 비교
- **`concept:stp-port-states`** — Disabled / Blocking / Listening / Learning / Forwarding 5단계

## 관련 표준

- **IEEE 802.1w** — RSTP (Rapid STP, `proto:rstp`)
- **IEEE 802.1s** — MSTP (Multiple STP, `proto:mstp`)
- **IEEE 802.1Q-2014** — 802.1D를 흡수 통합

## 검색 힌트

- "STP는 어느 표준?" → 본 카드 (IEEE 802.1D)
- "MAC bridge" → 본 카드
- "루트 브리지 선출" → 본 카드 + `concept:stp-root-bridge`

## 참고

CCIE는 본 표준의 STP/RSTP/MSTP를 다음 위치에서 가르친다:
- `Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-*.md`
