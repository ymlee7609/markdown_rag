---
id: concept:dns-record-types
type: Concept
name_en: DNS Resource Record Types
name_ko: DNS 레코드 종류
parent_protocol: proto:dns
scope: data-structure
aliases:
  - DNS record
  - A record
  - AAAA record
  - MX record
  - CNAME
  - NS
  - PTR
  - TXT
  - SOA
defined_by:
  - rfc:1035
related:
  - proto:dns
keywords_en:
  - A record
  - AAAA
  - MX
  - CNAME
  - NS
  - PTR
  - TXT
  - SOA
  - SRV
  - DNSSEC
  - RRset
  - TTL
keywords_ko:
  - DNS 레코드
  - 레코드 종류
  - 리소스 레코드
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

DNS Resource Record(RR)는 zone 파일을 구성하는 기본 단위로, `<NAME, TYPE, CLASS, TTL, RDATA>` 형식이다. 대표적인 record type을 정리한다.

## 핵심 타입

| Type | 의미 | RDATA 예시 |
|---|---|---|
| **A** | IPv4 주소 매핑 | `93.184.216.34` |
| **AAAA** | IPv6 주소 매핑 | `2606:2800:220:1::1` |
| **CNAME** | 별칭 (canonical name으로 redirect) | `www.example.com.` |
| **MX** | 메일 서버 (우선순위 + 호스트) | `10 mail.example.com.` |
| **NS** | zone의 권한 네임서버 | `ns1.example.com.` |
| **PTR** | 역방향 (IP → 이름), `in-addr.arpa.` zone | `host.example.com.` |
| **TXT** | 자유 텍스트 (SPF/DKIM/도메인 검증) | `"v=spf1 include:..."` |
| **SOA** | zone의 권한 시작 (한 zone당 1개) | primary NS, hostmaster, serial |
| **SRV** | 서비스 위치 (LDAP/Kerberos 등) | `_ldap._tcp` priority weight port target |
| **CAA** | 발급 가능한 CA 명시 | `0 issue "letsencrypt.org"` |

## DNSSEC 관련

DNSSEC을 위한 RR: **DNSKEY**, **RRSIG**, **DS**, **NSEC/NSEC3** (RFC 4033~4035)

## TTL과 캐싱

각 RR에는 TTL(초)이 설정되어 resolver가 캐시 가능 시간 결정. SOA의 minimum TTL이 negative caching에 사용.

## 검색 힌트

- "A record MX CNAME" → 본 카드
- "DNS 레코드 종류" → 본 카드 핵심 타입 표
- "SOA NS" → 본 카드
- "SPF DKIM" → 본 카드 (TXT record)
