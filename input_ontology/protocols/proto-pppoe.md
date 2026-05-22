---
id: proto:pppoe
type: Protocol
name_en: PPPoE
name_ko: PPP over Ethernet (PPPoE)
aliases:
  - PPP over Ethernet
layer: L2
family: access
status: active
defined_by:
  - rfc:2516
extends: []
related:
  - proto:ppp
  - proto:radius
  - concept:pppoe-discovery
  - concept:pppoe-session
references: []
depends_on:
  - proto:ppp
taught_in:
  - "Cisco_CCIE/CCIE_Vol2/05_part-iii-wide-area-networks.md"
documented_in:
  - "가입자망장비_manual/다산_OLT"
  - "가입자망장비_manual/유비쿼스_OLT"
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L3"
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - PPPoE
  - PADI
  - PADO
  - PADR
  - PADS
  - PADT
  - access concentrator
  - service name
  - session ID
  - intermediate agent
  - PPPoE+
keywords_ko:
  - PPPoE
  - 가입자 인증
  - 광 가입자
  - PPP 세션
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

PPPoE(PPP over Ethernet)는 이더넷 매체 위에서 PPP 세션을 캡슐화하는 프로토콜이다. 가입자 인증·세션 관리·과금이 필요한 xDSL/FTTH 가입자망에서 표준 인증 방식으로 사용된다. 한국 통신사업자(KT/SK/LGU+)의 광 가입자망에서 PPPoE+(Intermediate Agent)와 결합되어 회선 식별 정보를 인증 서버에 전달한다.

## 표준 / 정의

- **RFC 2516** — A Method for Transmitting PPP Over Ethernet, 1999-02
- 의존: **RFC 1661** (PPP, STD 51), **RFC 1994** (CHAP), **RFC 1334** (PAP)

## 핵심 개념

- [PPPoE Discovery](../concepts/concept-pppoe-discovery.md) — PADI → PADO → PADR → PADS 4단계
- [PPPoE Session](../concepts/concept-pppoe-session.md) — Session ID로 식별, LCP/NCP 협상, PADT로 종료

## 가입자망 특화 기능

- **PPPoE Intermediate Agent (PPPoE+)**: 가입자 회선·포트 식별자를 PADI/PADR에 삽입
  - DSL Forum TR-101 정의
  - Circuit-ID / Remote-ID 태그
- RADIUS 연동: PPPoE 인증을 RADIUS 서버로 위임

## 벤더 구현 매핑

| Vendor | 주요 명령어 | 매뉴얼 |
|---|---|---|
| Cisco | `bba-group pppoe`, `pppoe-client dial-pool-number`, `interface virtual-template` | `Cisco_CCIE/CCIE_Vol2/05_part-iii-wide-area-networks.md` |
| Dasan OLT/L3 | `pppoe intermediate-agent`, `bridge pppoe` | `가입자망장비_manual/다산_OLT/`, `다산_L3/` |
| Ubiquoss OLT/L3 | `pppoe intermediate-agent`, `pppoe enable` | `가입자망장비_manual/유비쿼스_OLT/`, `유비쿼스_L3/` |

## 검색 힌트

- "PPPoE 동작 단계" → 본 카드 + `concept:pppoe-discovery`
- "PADI PADO PADR PADS" → `concept:pppoe-discovery`
- "가입자 인증 광 회선" → 본 카드 + 다산/유비쿼스 OLT 매뉴얼
- "PPPoE intermediate agent" → 본 카드 가입자망 특화 기능 섹션
- "PPPoE+" → 본 카드 (intermediate agent)
