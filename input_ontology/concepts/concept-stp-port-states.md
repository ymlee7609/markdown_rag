---
id: concept:stp-port-states
type: Concept
name_en: STP Port States
name_ko: STP 포트 상태
parent_protocol: proto:stp
scope: state
aliases:
  - port states
  - blocking
  - listening
  - learning
  - forwarding
  - disabled
defined_by:
  - std:ieee-802.1d
related:
  - proto:stp
  - proto:rstp
  - concept:stp-root-bridge
keywords_en:
  - port state
  - blocking
  - listening
  - learning
  - forwarding
  - disabled
  - PortFast
  - BPDU Guard
  - convergence
keywords_ko:
  - 포트 상태
  - 차단
  - 청취
  - 학습
  - 전송
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

STP는 각 포트를 5가지 상태로 관리한다. 새 링크 활성화 시 Blocking → Listening → Learning → Forwarding 순으로 전이하며, 총 30~50초의 수렴 시간이 걸린다. RSTP(802.1w)는 이를 3상태로 단순화하고 proposal/agreement 메커니즘으로 1초 이내 수렴을 달성한다.

## STP 5 상태

| 상태 | 데이터 전송 | MAC 학습 | BPDU 처리 | 기본 지속 시간 |
|---|---|---|---|---|
| Disabled | X | X | X | (관리자 셧다운) |
| Blocking | X | X | 수신만 | 20초 max-age |
| Listening | X | X | 송수신 | 15초 forward delay |
| Learning | X | O | 송수신 | 15초 forward delay |
| Forwarding | O | O | 송수신 | - |

총 수렴: Listening 15s + Learning 15s = 30초 (Blocking에서 시작 시 +20s)

## RSTP 3 상태 (단순화)

- **Discarding** (= Disabled + Blocking + Listening 통합)
- **Learning**
- **Forwarding**

RSTP는 또한 별도 port role(Root, Designated, Alternate, Backup)을 도입.

## 수렴 시간 단축 기능 (Cisco)

- **PortFast**: 에지 포트(호스트 연결)는 즉시 Forwarding으로 전환
- **BPDU Guard**: PortFast 포트에서 BPDU 수신 시 err-disabled (STP loop 방지)
- **UplinkFast / BackboneFast**: 액세스 스위치 빠른 절체 (전통 STP용)
- **Root Guard**: 특정 포트에서 우월한 BPDU 수신 시 root-inconsistent 상태

## 검색 힌트

- "STP 포트 상태 순서" → 본 카드 STP 5 상태 표
- "STP 수렴 시간" → 본 카드 (30~50초)
- "RSTP 상태" → 본 카드 RSTP 3 상태 섹션
- "PortFast BPDU Guard" → 본 카드 수렴 시간 단축 기능
