---
id: concept:loopback-interface
type: Concept
name_en: Loopback Interface
name_ko: 루프백 인터페이스
parent_protocol: proto:ipv4
scope: state
aliases:
  - loopback
  - loopback0
  - logical interface
  - virtual interface
defined_by: []
related:
  - proto:ospf
  - proto:bgp
keywords_en:
  - loopback
  - loopback interface
  - router-id
  - stability
  - virtual
  - logical
  - always up
  - administrative
  - 127.0.0.1
keywords_ko:
  - 루프백
  - 루프백 인터페이스
  - 가상 인터페이스
  - 라우터 ID
  - 안정성
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-04.md"
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-05.md"
  - "Cisco_CCIE/CCIE_Vol2/03_part-i-ip-bgp-routing__sec-02.md"
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

Loopback Interface는 라우터/스위치에 생성하는 논리(가상) 인터페이스다. 물리 포트와 무관하게 라우터가 살아 있는 한 **항상 up 상태**를 유지하며, 물리 인터페이스 장애에 영향받지 않는다. OSPF/BGP 등 라우팅 프로토콜의 router-id, BGP peer source, 관리 IP, mGRE source 등 안정적인 식별자가 필요한 곳에 사용된다.

## 주요 용도

| 용도 | 설명 |
|---|---|
| **OSPF / BGP router-id** | 라우터 식별자 (가장 높은 loopback IP 자동 선택, 또는 명시 설정) |
| **iBGP peer source** | iBGP peer를 loopback으로 잡으면 다중 경로 중 하나가 끊겨도 BGP 세션 유지 |
| **Management IP** | 어느 물리 포트로 접속해도 동일 IP로 도달 → SSH/SNMP/Syslog 안정성 |
| **mGRE / DMVPN tunnel source** | 다중 path 중 하나가 죽어도 터널 유지 |
| **PIM RP** (Rendezvous Point) | 멀티캐스트 RP 주소 |
| **테스트** | 자가 ping/loopback 테스트 |

## Cisco 설정

```
interface Loopback0
 description Router-ID and Mgmt
 ip address 10.255.255.1 255.255.255.255    ! /32 권장 (주소 절약)
!
router ospf 1
 router-id 10.255.255.1
!
router bgp 65001
 neighbor 10.255.255.2 remote-as 65001
 neighbor 10.255.255.2 update-source Loopback0   ! iBGP peer 안정성
```

## 주의

- `127.0.0.0/8`은 호스트 OS의 loopback 대역, 라우터의 loopback 인터페이스 주소는 별도 IP 할당
- loopback 다수 생성 가능 (Loopback0, Loopback1, ...)
- IGP에 광고하지 않으면 외부에서 도달 불가

## 검색 힌트

- "loopback 인터페이스" → 본 카드
- "router-id 설정" → 본 카드 + OSPF/BGP 카드
- "iBGP update-source loopback" → 본 카드 주요 용도
- "라우팅 프로토콜 안정성" → 본 카드
- "관리 IP loopback" → 본 카드
