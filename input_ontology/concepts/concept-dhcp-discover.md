---
id: concept:dhcp-discover
type: Concept
name_en: DHCP Discovery (DORA)
name_ko: DHCP 발견·할당 절차 (DORA)
parent_protocol: proto:dhcp
scope: algorithm
aliases:
  - DORA
  - DHCPDISCOVER
  - DHCPOFFER
  - DHCPREQUEST
  - DHCPACK
defined_by:
  - rfc:2131
related:
  - proto:dhcp
  - concept:dhcp-lease
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-03.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-04.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-05.md"
documented_in:
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L3"
  - "가입자망장비_manual/다산_OLT"
  - "가입자망장비_manual/유비쿼스_OLT"
keywords_en:
  - DORA
  - DHCPDISCOVER
  - DHCPOFFER
  - DHCPREQUEST
  - DHCPACK
  - DHCPNAK
  - broadcast
  - UDP 67
  - UDP 68
  - xid
keywords_ko:
  - DORA
  - DHCP 할당
  - 발견
  - 제안
  - 요청
  - 응답
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

DORA(Discover-Offer-Request-Acknowledge)는 DHCP 클라이언트가 처음 IP를 할당받는 4단계 메시지 교환이다. UDP 67(서버)/68(클라이언트) 포트에서 동작하며, 모든 메시지는 동일한 트랜잭션 ID(xid)로 묶인다.

## 4단계 절차

| 단계 | 송신자 | 메시지 | 출발지 IP | 목적지 IP | 용도 |
|---|---|---|---|---|---|
| 1 | Client | DHCPDISCOVER | 0.0.0.0 | 255.255.255.255 (브로드캐스트) | 가용 서버 탐색 |
| 2 | Server | DHCPOFFER | 서버 IP | 255.255.255.255 또는 직접 | 임대 후보 제안 |
| 3 | Client | DHCPREQUEST | 0.0.0.0 | 255.255.255.255 | 특정 서버 선택·요청 |
| 4 | Server | DHCPACK | 서버 IP | 클라이언트 IP | 임대 확정 |

여러 서버가 응답하면 클라이언트는 첫 DHCPOFFER를 선택하고, DHCPREQUEST에 server-identifier 옵션으로 선택한 서버를 명시 → 다른 서버들은 자신의 OFFER를 폐기.

## DHCPNAK

서버가 요청을 거부할 때:
- 클라이언트가 요청한 주소가 이미 다른 호스트에 할당됨
- 임대 풀에 없는 주소를 요청
- 클라이언트가 잘못된 subnet으로 이동

## 핵심 필드 (BOOTP 호환)

- **chaddr**: 클라이언트 MAC 주소
- **yiaddr** ("your IP"): 서버가 할당한 IP
- **siaddr**: 서버 IP
- **giaddr** ("gateway IP"): DHCP Relay agent IP (relay 시 채워짐)
- **xid**: 트랜잭션 ID, 4단계 동안 동일

## DHCP Relay와의 상호작용

가입자가 다른 서브넷의 DHCP 서버에 접근하려면 라우터/스위치가 DHCP Relay agent로 동작:
1. DHCPDISCOVER 브로드캐스트 수신
2. giaddr에 자신의 IP 채워 유니캐스트로 DHCP 서버에 전달
3. DHCPOFFER 수신 후 클라이언트에 전달

## 검색 힌트

- "DHCP DORA" → 본 카드 4단계 절차 표
- "DHCPDISCOVER DHCPOFFER" → 본 카드
- "DHCP relay giaddr" → 본 카드 DHCP Relay 섹션
- "DHCPNAK 이유" → 본 카드 DHCPNAK 섹션
