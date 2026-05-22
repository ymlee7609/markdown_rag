---
id: proto:hsrp
type: Protocol
name_en: HSRP
name_ko: HSRP (Hot Standby Router Protocol)
aliases:
  - Hot Standby Router Protocol
  - HSRPv1
  - HSRPv2
layer: L3
family: redundancy
status: active
defined_by:
  - rfc:2281          # HSRP (Informational, Cisco 독점이지만 RFC 형태로 공개)
extends: []
related:
  - proto:vrrp
  - proto:glbp
references: []
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-03.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-04.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-05.md"
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-02.md"
documented_in: []
vendors_supporting:
  - vendor:cisco
keywords_en:
  - HSRP
  - Hot Standby Router Protocol
  - virtual IP
  - VIP
  - active router
  - standby router
  - preempt
  - priority
  - tracking
  - first-hop redundancy
  - FHRP
keywords_ko:
  - HSRP
  - 핫 스탠바이
  - 게이트웨이 이중화
  - 가상 IP
  - 우선순위
  - preempt
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

HSRP(Hot Standby Router Protocol)는 Cisco가 개발한 First-Hop Redundancy Protocol(FHRP)이다. 다수 라우터가 단일 가상 IP(VIP)를 공유해 호스트의 기본 게이트웨이 역할을 이중화한다. 한 라우터가 Active, 나머지는 Standby로 동작하며, Active 장애 시 Standby가 인계받아 호스트 측 트래픽 단절을 최소화한다. RFC 2281이 informational로 공개됐다.

## 표준 / 정의

- **RFC 2281** — Cisco Hot Standby Router Protocol (HSRP), 1998-03 (Informational)
- IETF 표준 FHRP는 **VRRP** (RFC 5798, `proto:vrrp`)
- Cisco 자체 변형: **GLBP** (Gateway Load Balancing Protocol)

## 핵심 개념

| 용어 | 의미 |
|---|---|
| **Virtual IP (VIP)** | 호스트 게이트웨이 IP. 모든 HSRP 라우터가 공유 |
| **Virtual MAC** | HSRPv1: `0000.0C07.ACxx` (xx=group). HSRPv2: `0000.0C9F.Fxxx` |
| **Active router** | 실제 트래픽 처리, ARP 응답 |
| **Standby router** | 백업, Active 장애 시 인계 |
| **Priority** | 0~255 (기본 100). 높을수록 Active 후보 |
| **Preempt** | 더 높은 priority 라우터가 복귀 시 강제로 Active 인계 |
| **Tracking** | 인터페이스/object 장애를 감지해 priority 자동 감소 → 다른 라우터에게 양보 |

## Cisco 설정 (요약)

```
interface Vlan10
 ip address 10.0.0.2 255.255.255.0
 standby version 2
 standby 10 ip 10.0.0.1
 standby 10 priority 110
 standby 10 preempt
 standby 10 track GigabitEthernet0/0 20
```

## HSRP vs VRRP vs GLBP

| 항목 | HSRP | VRRP | GLBP |
|---|---|---|---|
| 표준 | Cisco (RFC 2281 info) | IETF (RFC 5798) | Cisco 독점 |
| Active 라우터 수 | 1 | 1 (Master) | 다수 (load balancing) |
| 헬로 멀티캐스트 | 224.0.0.2 | 224.0.0.18 | 224.0.0.102 |
| 멀티 벤더 | X | O | X |

## 검색 힌트

- "HSRP 설정" → 본 카드
- "first-hop redundancy" → 본 카드 + `proto:vrrp`
- "Active Standby 라우터" → 본 카드
- "HSRP preempt priority" → 본 카드 핵심 개념 표
- "VRRP 차이" → 본 카드 비교 표
- "Virtual IP 게이트웨이" → 본 카드
