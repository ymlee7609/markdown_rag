---
id: proto:ipv6
type: Protocol
name_en: IPv6
name_ko: 인터넷 프로토콜 버전 6 (IPv6)
aliases:
  - Internet Protocol version 6
  - IP version 6
layer: L3
family: internet
status: active
defined_by:
  - rfc:8200
extends: []
related:
  - proto:ipv4
  - proto:ndp
  - proto:ospfv3
  - proto:dhcpv6
  - concept:ipv6-header
  - concept:ipv6-extension-header
references:
  - rfc:2460   # IPv6 이전 표준 (obsoleted)
  - rfc:4291   # IPv6 Addressing Architecture
  - rfc:4862   # SLAAC
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-01.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-02.md"
documented_in:
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L3"
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - IPv6
  - 128-bit
  - extension header
  - link-local
  - global unicast
  - multicast
  - anycast
  - FE80::
  - ::1
  - flow label
  - SLAAC
keywords_ko:
  - IPv6
  - 128비트
  - 확장 헤더
  - 링크 로컬
  - 글로벌 유니캐스트
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

IPv6(Internet Protocol Version 6)는 IPv4를 잇는 차세대 인터넷 프로토콜이다. 128비트 주소 공간(약 3.4×10³⁸개), 단순화된 40바이트 고정 헤더, 확장 헤더 체계, NDP를 통한 자동 구성을 특징으로 한다. RFC 8200(STD 86)이 현행 표준이며 이전 RFC 2460을 폐기했다.

## 표준 / 정의

- **RFC 8200** — IPv6 본체 사양 (STD 86, 2017)
- **RFC 4291** — IPv6 Addressing Architecture
- **RFC 4862** — IPv6 SLAAC (Stateless Address Autoconfiguration)
- **RFC 4861** — NDP (`proto:ndp`)
- 폐기: RFC 1883 → RFC 2460 → **RFC 8200**

## 핵심 개념

- [IPv6 Header](../concepts/concept-ipv6-header.md) — 40바이트 고정 헤더 (Version/TC/Flow Label/Payload Length/NextHeader/Hop Limit/Src/Dst)
- [Extension Header](../concepts/concept-ipv6-extension-header.md) — Hop-by-Hop / Routing / Fragment / AH / ESP / Destination Options

## 주소 종류

- **Link-local** (`fe80::/10`) — 동일 링크 내에서만 유효, 자동 생성
- **Global Unicast** (`2000::/3`) — 글로벌 라우팅 가능
- **Unique Local** (`fc00::/7`) — 사이트 내부용 (IPv4 사설망 대응)
- **Multicast** (`ff00::/8`) — 멀티캐스트 (IPv6는 브로드캐스트 없음)
- **Anycast** — 다수 노드 중 가장 가까운 1곳에 전달

## 자동 구성 / 인접 탐색

- **SLAAC**: RA(Router Advertisement)로 받은 prefix + EUI-64 또는 random IID로 주소 자동 생성
- **DHCPv6**: 상태 보존(Stateful) 또는 정보용(Stateless) 자동 구성 (`proto:dhcpv6`)
- **NDP** (RFC 4861): ARP 대체, 라우터 발견·주소 해석·DAD (`proto:ndp`)

## 벤더 구현 매핑

| Vendor | 주요 명령어 | 매뉴얼 |
|---|---|---|
| Cisco | `ipv6 unicast-routing`, `ipv6 address ...`, `ipv6 router ospf` | `Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-01,02.md` |
| Dasan L3 | `ipv6 enable`, `ipv6 address ...` | `가입자망장비_manual/다산_L3/` |
| Ubiquoss L3 | `ipv6 enable`, `ipv6 address ...` | `가입자망장비_manual/유비쿼스_L3/` |

## 검색 힌트

- "IPv6 헤더" → 본 카드 + `concept:ipv6-header`
- "IPv6는 어느 RFC?" → `rfc:8200` (STD 86)
- "SLAAC" → 본 카드 자동 구성 섹션 + RFC 4862
- "link-local 주소" → 본 카드 주소 종류 (fe80::/10)
- "IPv4 IPv6 차이" → 본 카드 + `proto:ipv4`
