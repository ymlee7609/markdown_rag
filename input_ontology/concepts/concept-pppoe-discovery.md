---
id: concept:pppoe-discovery
type: Concept
name_en: PPPoE Discovery
name_ko: PPPoE 발견 단계
parent_protocol: proto:pppoe
scope: algorithm
aliases:
  - PADI
  - PADO
  - PADR
  - PADS
  - PADT
  - PPPoE discovery stage
defined_by:
  - rfc:2516
related:
  - proto:pppoe
  - concept:pppoe-session
keywords_en:
  - PADI
  - PADO
  - PADR
  - PADS
  - PADT
  - service name
  - access concentrator
  - AC-Cookie
  - Host-Uniq
  - session ID
keywords_ko:
  - PPPoE 발견
  - 광 가입자 인증
  - 세션 ID
  - 액세스 콘센트레이터
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

PPPoE는 Discovery 단계와 Session 단계로 나뉜다. Discovery 단계는 클라이언트(호스트)가 사용 가능한 AC(Access Concentrator)를 찾아 Session ID를 부여받는 4단계 프로토콜이다. 모든 Discovery 패킷은 EtherType 0x8863(Discovery), Session 패킷은 0x8864를 사용한다.

## 4단계 (PADI → PADO → PADR → PADS)

| 단계 | 송신자 | 메시지 | 목적 |
|---|---|---|---|
| 1 | Host | **PADI** (Active Discovery Initiation) | 브로드캐스트로 AC 탐색 |
| 2 | AC | **PADO** (Active Discovery Offer) | AC가 자신을 광고, AC-Name·Service-Name 포함 |
| 3 | Host | **PADR** (Active Discovery Request) | 특정 AC 선택·요청, AC-Cookie echo |
| 4 | AC | **PADS** (Active Discovery Session-confirmation) | Session ID 부여 (1~65535) |

이후 Session 단계로 전환 (LCP/NCP 협상).

## PADT (종료)

세션 종료 시 어느 쪽이든 **PADT** (Active Discovery Terminate)를 보내 세션을 끊는다.

## 핵심 태그 (Type-Length-Value)

- **Service-Name** (0x0101): 요청 서비스 이름 (빈 문자열 가능)
- **AC-Name** (0x0102): AC 식별자
- **AC-Cookie** (0x0104): 재전송 공격 방지
- **Host-Uniq** (0x0103): 호스트가 자신의 응답을 식별
- **Relay-Session-ID** (0x0110): PPPoE relay agent용

## PPPoE Intermediate Agent (PPPoE+)

DSL Forum TR-101이 정의한 확장:
- 액세스 노드(OLT/DSLAM)가 PADI/PADR을 가로채 **Vendor-Specific** 태그(0x0105) 추가
- Circuit-ID, Remote-ID로 가입자 회선·포트 식별 → BRAS/RADIUS가 인증 정책 결정

## 검색 힌트

- "PADI PADO PADR PADS" → 본 카드 4단계 표
- "PPPoE 세션 시작" → 본 카드 + `concept:pppoe-session`
- "AC-Cookie" → 본 카드 핵심 태그 섹션
- "PPPoE intermediate agent" → 본 카드 PPPoE+ 섹션
- "광 가입자 인증 절차" → 본 카드 + `proto:pppoe`
