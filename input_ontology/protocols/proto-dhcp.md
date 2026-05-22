---
id: proto:dhcp
type: Protocol
name_en: DHCP
name_ko: 동적 호스트 구성 프로토콜 (DHCPv4)
aliases:
  - Dynamic Host Configuration Protocol
  - DHCPv4
  - BOOTP successor
layer: L7
family: access
status: active
defined_by:
  - rfc:2131
extends: []
related:
  - proto:dhcpv6
  - concept:dhcp-discover
  - concept:dhcp-lease
references:
  - rfc:2132   # DHCP Options
  - rfc:3046   # Relay Agent Information Option (Option 82)
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-04.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-05.md"
documented_in:
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L3"
  - "가입자망장비_manual/다산_OLT"
  - "가입자망장비_manual/유비쿼스_OLT"
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - DHCP
  - DHCPDISCOVER
  - DHCPOFFER
  - DHCPREQUEST
  - DHCPACK
  - DHCPNAK
  - lease
  - relay agent
  - Option 82
  - DHCP server
  - DHCP snooping
  - giaddr
  - yiaddr
  - siaddr
keywords_ko:
  - DHCP
  - IP 자동 할당
  - 임대
  - 릴레이
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

DHCP(Dynamic Host Configuration Protocol)는 호스트가 IP 주소·서브넷·게이트웨이·DNS 등을 동적으로 할당받는 프로토콜이다. UDP 67/68 포트에서 동작하며, DORA(Discover-Offer-Request-Ack) 4단계 메시지 교환으로 임대(lease)를 받는다. BOOTP(RFC 951)의 후속이며 IPv4 표준은 RFC 2131이 정의한다.

## 표준 / 정의

- **RFC 2131** — DHCPv4 정식 사양 (1997)
- **RFC 2132** — DHCP Options and BOOTP Vendor Extensions
- **RFC 3046** — Relay Agent Information Option (Option 82, 가입자 식별에 활용)
- **RFC 8415** — DHCPv6 (별도 프로토콜 `proto:dhcpv6`)

## 핵심 개념

- [DHCP Discovery (DORA)](../concepts/concept-dhcp-discover.md) — 4단계 메시지 교환
- [DHCP Lease](../concepts/concept-dhcp-lease.md) — 임대 시간, T1/T2 갱신

## 가입자망 특화 사용

가입자망 장비에서 DHCP는 다음 기능과 결합되어 사용된다:
- **DHCP Relay**: 가입자가 다른 서브넷의 DHCP 서버에 접근하도록 중계 (giaddr 채움)
- **Option 82 (DHCP Relay Agent Information)**: 가입자 회선·포트 식별자를 DHCP 서버에 전달
- **DHCP Snooping**: 신뢰 포트만 DHCP 응답 허용, ARP/IP spoofing 방어 기반

## 벤더 구현 매핑

| Vendor | 주요 명령어 | 매뉴얼 |
|---|---|---|
| Cisco | `ip dhcp pool`, `ip helper-address`, `ip dhcp snooping` | `Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-04,05.md` |
| Dasan L3/OLT | `ip dhcp ...`, `ip dhcp relay`, `ip dhcp snooping` | `가입자망장비_manual/다산_L3/`, `다산_OLT/` |
| Ubiquoss L3/OLT | `ip dhcp ...`, `ip dhcp snooping` | `가입자망장비_manual/유비쿼스_L3/`, `유비쿼스_OLT/` |

## 검색 힌트

- "DHCP DORA" → 본 카드 + `concept:dhcp-discover`
- "DHCP relay 설정" → 본 카드 + 벤더 매뉴얼
- "Option 82" → 본 카드 + RFC 3046
- "DHCP snooping" → 본 카드 + 벤더 매뉴얼
- "가입자 IP 할당" → 본 카드 + 다산/유비쿼스 OLT 매뉴얼
