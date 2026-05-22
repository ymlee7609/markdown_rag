---
id: proto:acl
type: Protocol
name_en: ACL
name_ko: 접근 제어 목록 (ACL)
aliases:
  - Access Control List
  - Access List
  - packet filter
layer: multi
family: management
status: active
defined_by: []         # RFC/IEEE 표준이 별도로 없음, 벤더별 기능
extends: []
related:
  - proto:qos
  - concept:acl-standard
  - concept:acl-extended
references: []
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-04.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-05.md"
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
  - ACL
  - access-list
  - permit
  - deny
  - standard ACL
  - extended ACL
  - named ACL
  - wildcard mask
  - ACE
  - packet filter
  - inbound
  - outbound
  - VACL
  - PACL
  - implicit deny
keywords_ko:
  - ACL
  - 접근 제어
  - 패킷 필터
  - 허용
  - 거부
  - 차단
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

ACL(Access Control List)은 라우터/스위치가 트래픽을 조건에 따라 허용(permit)·거부(deny)하는 규칙 목록이다. 표준 ACL(출발지 IP만), 확장 ACL(출발지·목적지 IP + 프로토콜·포트), 명명 ACL 등으로 분류된다. 인터페이스·VLAN·라우팅 경로 분류·QoS 분류 등 다양한 용도로 사용된다. IETF RFC가 정의하는 표준은 별도로 없고 벤더별 구현 명령어 체계가 통용된다.

## 표준

ACL은 단일 RFC/IEEE 표준 없이 다음 관련 표준의 부수적 기능으로 정의된다:
- RFC 2475 — Differentiated Services (DiffServ 분류기로 ACL 활용)
- 벤더 명령어 체계 (Cisco IOS, 다산 NOS, 유비쿼스 NOS)

## 핵심 개념

- [Standard ACL](../concepts/concept-acl-standard.md) — Cisco IOS 1~99, 1300~1999, 출발지 IP만
- [Extended ACL](../concepts/concept-acl-extended.md) — Cisco IOS 100~199, 2000~2699, 5-tuple 매칭

## 핵심 규칙

- **암시적 거부**: ACL 끝에 항상 `deny ip any any` 가 묵시적으로 존재
- **순차 평가**: 규칙은 위에서 아래로 첫 매칭에서 종료
- **방향 적용**: inbound (인터페이스 진입) / outbound (인터페이스 송출)

## 벤더 구현 매핑

| Vendor | 표준 ACL | 확장 ACL | 매뉴얼 |
|---|---|---|---|
| Cisco | `access-list 10 permit ...` | `access-list 110 permit tcp ...` | `Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-04,05.md` |
| Dasan | `access-list ip ...`, `permit/deny` | `access-list extended ...` | `가입자망장비_manual/다산_*` |
| Ubiquoss | `access-list ...`, `ip access-list extended` | `ip access-list extended ...` | `가입자망장비_manual/유비쿼스_*` |

## 관련 기능

- **VACL** (VLAN ACL) — VLAN 내 트래픽에 적용
- **PACL** (Port ACL) — L2 포트에 적용
- **QoS 분류기** — ACL을 트래픽 클래스 분류 기준으로 사용

## 검색 힌트

- "ACL 표준과 확장 차이" → 본 카드 + `concept:acl-standard`, `concept:acl-extended`
- "인터페이스에 ACL 적용" → 본 카드 + 벤더 매뉴얼
- "wildcard mask" → 본 카드 + CCIE Vol1 IP Networking
- "암시적 deny" → 본 카드 핵심 규칙
- "다산 ACL 설정" → 본 카드 documented_in + 다산 매뉴얼
