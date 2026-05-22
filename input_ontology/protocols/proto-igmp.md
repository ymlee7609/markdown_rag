---
id: proto:igmp
type: Protocol
name_en: IGMP
name_ko: 인터넷 그룹 관리 프로토콜 (IGMP)
aliases:
  - Internet Group Management Protocol
  - IGMPv1
  - IGMPv2
  - IGMPv3
layer: L3
family: multicast
status: active
defined_by:
  - rfc:3376      # IGMPv3 (current)
extends: []
related:
  - proto:mld
  - concept:igmp-snooping
  - concept:igmp-source-specific
references:
  - rfc:1112      # IGMPv1
  - rfc:2236      # IGMPv2 (obsoleted by 3376)
  - rfc:4604      # IGMPv3 for SSM
taught_in:
  - "Cisco_CCIE/CCIE_Vol2/06_part-iv-ip-multicast__sec-01.md"
  - "Cisco_CCIE/CCIE_Vol2/06_part-iv-ip-multicast__sec-02.md"
  - "Cisco_CCIE/CCIE_Vol2/06_part-iv-ip-multicast__sec-03.md"
documented_in:
  - "가입자망장비_manual/다산_L2"
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/다산_OLT"
  - "가입자망장비_manual/유비쿼스_L2"
  - "가입자망장비_manual/유비쿼스_L3"
  - "가입자망장비_manual/유비쿼스_OLT"
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - IGMP
  - IGMPv2
  - IGMPv3
  - multicast
  - membership query
  - membership report
  - leave group
  - IGMP snooping
  - SSM
  - source-specific multicast
  - IGMP proxy
keywords_ko:
  - IGMP
  - 멀티캐스트
  - 그룹 가입
  - IPTV
  - 스누핑
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

IGMP(Internet Group Management Protocol)는 IPv4 호스트가 라우터에 멀티캐스트 그룹 가입·탈퇴를 알리는 L3 프로토콜이다. IPTV·실시간 스트리밍·금융 시세 배포에 사용된다. v1(RFC 1112), v2(RFC 2236), v3(RFC 3376) 버전이 있고, v3가 현행이며 source-specific multicast(SSM)을 지원한다.

## 표준 체인

- **RFC 1112** (1989) — IGMPv1, 멀티캐스트 기본
- **RFC 2236** (1997) — IGMPv2, Leave 메시지 추가 (RFC 3376이 폐기)
- **RFC 3376** (2002) — IGMPv3, SSM 지원 (현행)
- **RFC 4604** (2006) — IGMPv3로 SSM 사용 지침

## 핵심 개념

- [IGMP Snooping](../concepts/concept-igmp-snooping.md) — L2 스위치가 IGMP를 들여다보고 멀티캐스트 포워딩 최적화
- [Source-Specific Multicast](../concepts/concept-igmp-source-specific.md) — IGMPv3 EXCLUDE/INCLUDE 필터

## 가입자망 특화 사용

- **IPTV 가입자 채널 가입**: IGMP join → OLT가 처리 → MPLS/IP 백본 통해 콘텐츠 수신
- **IGMP Snooping on OLT**: 가입자 채널 변경 시 멀티캐스트 트리 즉시 갱신
- **IGMP Proxy / Querier**: OLT가 IGMP Querier 역할 수행, 가입자 응답 집계

## 벤더 구현 매핑

| Vendor | 주요 명령어 | 매뉴얼 |
|---|---|---|
| Cisco | `ip igmp version`, `ip igmp join-group`, `ip igmp snooping` | `Cisco_CCIE/CCIE_Vol2/06_part-iv-ip-multicast__sec-*.md` |
| Dasan L2/L3/OLT | `ip igmp snooping`, `ip igmp proxy` | `가입자망장비_manual/다산_*` |
| Ubiquoss L2/L3/OLT | `ip igmp snooping enable`, `ip igmp querier` | `가입자망장비_manual/유비쿼스_*` |

## 검색 힌트

- "IGMP snooping 설정" → 본 카드 + `concept:igmp-snooping` + 벤더 매뉴얼
- "멀티캐스트 그룹 가입" → 본 카드 + `proto:igmp` 표준 체인
- "IPTV 채널 변경 빠르게" → `concept:igmp-snooping` + IGMPv2 Leave
- "SSM" → `concept:igmp-source-specific` + RFC 4604
