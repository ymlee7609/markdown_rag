---
id: concept:acl-standard
type: Concept
name_en: Standard ACL
name_ko: 표준 ACL
parent_protocol: proto:acl
scope: data-structure
aliases:
  - standard access list
  - source-based ACL
defined_by: []
related:
  - proto:acl
  - concept:acl-extended
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-02.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-04.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-05.md"
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-05.md"
documented_in:
  - "가입자망장비_manual/다산_L2"
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L2"
  - "가입자망장비_manual/유비쿼스_L3"
keywords_en:
  - standard ACL
  # ACL-specific terms only. Generic tokens "permit"/"deny" removed (too broad).
  - standard ACL
  - access-list 1-99
  - access-list 1300-1999
  - source-based ACL
  - wildcard mask
keywords_ko:
  - 표준 ACL
  - 표준 access-list
  - 와일드카드 마스크
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

Standard ACL은 출발지 IP 주소만으로 트래픽을 필터링하는 가장 단순한 ACL이다. Cisco IOS에서는 번호 1~99 또는 1300~1999가 표준 ACL이며, 적용은 가능한 한 목적지 가까운 인터페이스에 권장된다(필요 이상 트래픽 차단 방지).

## Cisco 명령어 형식

```
access-list <1-99|1300-1999> {permit|deny} <source> [wildcard-mask]
```

예:
- `access-list 10 permit 192.168.1.0 0.0.0.255` → 192.168.1.0/24 허용
- `access-list 10 deny host 192.168.1.5` → 단일 호스트 거부
- `access-list 10 permit any` → 모든 출발지 허용

## Wildcard Mask

서브넷 마스크의 역수(0/1 반전):
- 서브넷 `255.255.255.0` (/24) → wildcard `0.0.0.255`
- 0 비트는 "정확히 일치", 1 비트는 "무관"

특수 키워드:
- `host A.B.C.D` ≡ `A.B.C.D 0.0.0.0`
- `any` ≡ `0.0.0.0 255.255.255.255`

## 적용 권장

Standard ACL은 출발지만 보기에 목적지에서 너무 멀리 적용하면 의도치 않은 트래픽 차단 발생. 일반 규칙: **출발지 ACL은 목적지 가까이**.

## 한계와 확장

- 출발지만 보기 때문에 "어느 호스트가 어디로 가는 무슨 프로토콜"은 표현 불가
- 더 세밀한 제어가 필요하면 [Extended ACL](./concept-acl-extended.md) 사용

## 검색 힌트

- "표준 ACL 번호 범위" → 본 카드 (1-99, 1300-1999)
- "wildcard mask 계산" → 본 카드 Wildcard Mask 섹션
- "ACL 적용 위치" → 본 카드 적용 권장 섹션
- "host any 키워드" → 본 카드
