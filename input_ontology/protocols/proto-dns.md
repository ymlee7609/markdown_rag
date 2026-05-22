---
id: proto:dns
type: Protocol
name_en: DNS
name_ko: 도메인 네임 시스템 (DNS)
aliases:
  - Domain Name System
layer: L7
family: name-resolution
status: active
defined_by:
  - rfc:1034
  - rfc:1035
extends: []
related:
  - concept:dns-record-types
references:
  - rfc:8499        # DNS Terminology
  - rfc:9499        # DNS Terminology (updated)
taught_in: []
documented_in:
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L3"
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - DNS
  - domain name
  - resolver
  - name server
  - authoritative
  - recursive
  - TLD
  - root server
  - UDP 53
  - TCP 53
  - DoH
  - DoT
keywords_ko:
  - DNS
  - 도메인 네임
  - 이름 해석
  - 네임서버
  - 도메인
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

DNS(Domain Name System)는 사람이 읽기 쉬운 도메인 이름(예: `www.example.com`)을 IP 주소(`93.184.216.34`)로 매핑하는 분산 계층 데이터베이스 시스템이다. UDP 53번 포트가 표준이며, 응답 크기가 512바이트를 넘으면 TCP 53으로 전환. 1983년 표준화(RFC 1034/1035) 이후 인터넷 핵심 인프라.

## 표준 / 정의

- **RFC 1034** — Domain Names: Concepts and Facilities (개념)
- **RFC 1035** — Domain Names: Implementation and Specification (구현)
- **RFC 9499** — DNS Terminology (현행, RFC 8499 폐기)
- 보안 확장: **DNSSEC** (RFC 4033~4035), **DoH** (RFC 8484), **DoT** (RFC 7858)

## 핵심 개념

- [DNS Resource Records (A, AAAA, MX, CNAME, NS, PTR, TXT, SOA)](../concepts/concept-dns-record-types.md)

## 역할별 서버

- **Authoritative**: 특정 zone의 권한 있는 답변
- **Recursive resolver (Caching)**: 클라이언트 대신 권한 서버를 순회 (8.8.8.8, 1.1.1.1 등)
- **Root servers** (13개 그룹, IPv4/IPv6)
- **TLD servers** (.com, .net, .kr 등)
- **Stub resolver**: 클라이언트 라이브러리 (`/etc/resolv.conf`)

## 검색 힌트

- "DNS 종류" "DNS 레코드" → 본 카드 + `concept:dns-record-types`
- "A MX CNAME" → 본 카드 + RFC 1035
- "DNSSEC" → 본 카드 표준 섹션
- "재귀 vs 권한" → 본 카드 역할별 서버
