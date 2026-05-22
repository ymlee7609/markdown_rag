---
id: concept:ipv6-header
type: Concept
name_en: IPv6 Header
name_ko: IPv6 헤더
parent_protocol: proto:ipv6
scope: data-structure
aliases:
  - IPv6 header
  - fixed header
defined_by:
  - rfc:8200
related:
  - proto:ipv6
  - concept:ipv6-extension-header
keywords_en:
  - IPv6 header
  - 40 bytes
  - version
  - traffic class
  - flow label
  - payload length
  - next header
  - hop limit
  - source address
  - destination address
keywords_ko:
  - IPv6 헤더
  - 40바이트
  - 흐름 라벨
  - 다음 헤더
  - 홉 제한
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

IPv6 헤더는 40바이트 고정 길이로, IPv4(가변 20~60바이트)에 비해 단순화됐다. Checksum 필드가 제거되고(L4와 L2가 무결성 책임), 옵션은 확장 헤더(extension header)로 분리됐다. 결과적으로 라우터가 헤더를 더 빠르게 처리한다.

## 헤더 구조 (40바이트)

| 필드 | 크기 | 용도 |
|---|---|---|
| Version | 4b | 항상 6 |
| Traffic Class | 8b | DSCP + ECN (QoS) |
| Flow Label | 20b | 동일 흐름의 패킷 식별 (ECMP/QoS 힌트) |
| Payload Length | 16b | 페이로드+확장헤더 길이 (64KB 한계) |
| Next Header | 8b | 다음 헤더/프로토콜 타입 (TCP=6, UDP=17, ICMPv6=58, ...) |
| Hop Limit | 8b | TTL 대응, 라우터마다 -1 |
| Source Address | 128b | 출발지 IPv6 주소 |
| Destination Address | 128b | 목적지 IPv6 주소 |

## IPv4 헤더와의 주요 차이

| 항목 | IPv4 | IPv6 |
|---|---|---|
| 헤더 길이 | 20~60바이트 가변 | 40바이트 고정 |
| 주소 길이 | 32비트 | 128비트 |
| Checksum | 있음 (라우터마다 재계산) | 없음 |
| Fragmentation | 라우터에서 가능 | 송신자만 (Fragment 확장 헤더) |
| Options | 헤더 내 IHL 가변 옵션 | 확장 헤더로 분리 |
| Broadcast | 있음 | 없음 (multicast 사용) |

## Jumbogram (4G+ 페이로드)

Payload Length가 16비트라 64KB 한계가 있지만, Hop-by-Hop 확장 헤더의 **Jumbo Payload Option** (RFC 2675)으로 32비트(최대 4GB) 확장 가능. 일부 백본·HPC에서만 사용.

## 검색 힌트

- "IPv6 헤더 구조" → 본 카드 헤더 구조 표
- "IPv4 IPv6 헤더 차이" → 본 카드 비교 표
- "IPv6 Flow Label" → 본 카드 헤더 구조 섹션
- "IPv6 헤더 길이" → 본 카드 (40바이트 고정)
- "Hop Limit" → 본 카드 (IPv4 TTL 대응)
