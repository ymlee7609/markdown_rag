---
id: concept:bgp-as-path
type: Concept
name_en: BGP AS_PATH
name_ko: BGP AS-PATH 경로 속성
parent_protocol: proto:bgp
scope: data-structure
aliases:
  - AS-PATH
  - AS_PATH
  - autonomous system path
defined_by:
  - rfc:4271
related:
  - proto:bgp
taught_in:
  - "Cisco_CCIE/CCIE_Vol2/03_part-i-ip-bgp-routing__sec-05.md"
keywords_en:
  - AS_PATH
  - AS-PATH
  - path attribute
  - well-known mandatory
  - AS_SEQUENCE
  - AS_SET
  - prepend
  - loop prevention
keywords_ko:
  - 경로 속성
  - 자율시스템 경로
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

AS_PATH는 BGP UPDATE 메시지의 well-known mandatory 경로 속성(Path Attribute)으로, 경로가 거쳐온 자율 시스템(AS) 번호의 순서 목록이다. 두 가지 핵심 역할을 한다: (1) 경로 길이로 BGP 의사결정에 사용(짧을수록 우선), (2) 자신의 AS 번호가 이미 AS_PATH에 있으면 경로를 거부해 루프 방지.

## 구조

AS_PATH는 path segment 목록으로 구성된다:
- **AS_SEQUENCE**: 순서가 있는 AS 번호 목록 (가장 일반적)
- **AS_SET**: 순서 없는 AS 번호 집합 (route aggregation에서 사용)
- **AS_CONFED_SEQUENCE / AS_CONFED_SET**: BGP confederation 내부에서 사용 (RFC 5065)

## BGP 의사결정에서의 역할

BGP best-path 알고리즘 우선순위 중 AS_PATH는 일반적으로 3~4번째 (Weight → Local Pref → Locally originated → Shortest AS_PATH → ...).

## AS_PATH 조작

- **AS path prepending**: 자신의 AS 번호를 여러 번 prepend해 경로를 일부러 길게 만들어 트래픽 분산
- **route-map set as-path prepend** (Cisco) — outbound 정책에 사용
- **AS_PATH filter**: 정규식으로 특정 AS 경로 차단/허용

## 4-Octet AS 지원

- 원래 16비트(0~65535) → **RFC 6793**으로 32비트(0~4,294,967,295) 확장
- 호환성을 위해 AS_TRANS(23456) 매핑 메커니즘 도입

## 검색 힌트

- "AS-PATH 길이" → 본 카드 BGP 의사결정 섹션
- "BGP 루프 방지" → 본 카드 (AS_PATH에 자기 AS 발견 시 거부)
- "AS path prepending" → 본 카드 조작 섹션
- "BGP path attribute" → 본 카드 + `rfc:4271` sec-05
