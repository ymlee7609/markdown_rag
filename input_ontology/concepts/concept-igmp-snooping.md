---
id: concept:igmp-snooping
type: Concept
name_en: IGMP Snooping
name_ko: IGMP 스누핑
parent_protocol: proto:igmp
scope: algorithm
aliases:
  - IGMP snooping
  - L2 multicast snooping
defined_by:
  - rfc:4541    # IGMP/MLD snooping considerations (informational)
related:
  - proto:igmp
  - proto:vlan
keywords_en:
  - IGMP snooping
  - multicast forwarding
  - mrouter port
  - IGMP querier
  - leave latency
  - fast leave
  - immediate leave
  - L2 multicast
keywords_ko:
  - IGMP 스누핑
  - 멀티캐스트
  - 그룹 멤버십
  - IPTV
  - 채널 변경
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

IGMP Snooping은 L2 스위치가 호스트-라우터 간 IGMP 메시지(Membership Query/Report/Leave)를 들여다보고 어느 포트에 어느 멀티캐스트 그룹의 멤버가 있는지 학습하는 기능이다. 학습 결과로 멀티캐스트 트래픽을 해당 포트에만 전달해 불필요한 플러딩을 막는다. IPTV 가입자망에서 가입자별 채널 분배의 필수 기능이다.

## 동작 메커니즘

1. **Membership Query** (라우터 → 호스트, 모든 포트로 전송) 감시 → mrouter port 식별
2. **Membership Report** (호스트 → 라우터) 감시 → 송신 포트를 해당 그룹의 멤버 포트로 등록
3. **Leave Group** (IGMPv2/v3) 감시 → group-specific query 후 응답이 없으면 멤버에서 제거
4. 멀티캐스트 데이터 프레임은 멤버 포트와 mrouter port로만 전달

## 핵심 구성 요소

- **Mrouter port**: 라우터가 연결된 포트. 알려지지 않은 멀티캐스트는 항상 이쪽으로
- **Group port**: 특정 그룹의 멤버가 있는 포트
- **IGMP Querier**: 라우터가 없는 L2-only 환경에서 스위치가 Querier 역할 수행

## Leave Latency 단축

- **Immediate Leave (Fast Leave)**: Leave 메시지 수신 즉시 포트를 그룹에서 제거 (가입자당 1 단말 가정)
  - IPTV에서 채널 변경 시 즉시 이전 채널 트래픽 중단 가능
  - 한 포트에 여러 호스트가 있으면 사용 금지(다른 호스트도 끊김)

## 가입자망 운영

- 다산/유비쿼스 OLT/L2 스위치에서 **IGMP Proxy** 모드도 지원:
  - 스위치가 IGMP Report를 집계해 단일 Report만 상위로 전달
- **MVR** (Multicast VLAN Registration): 별도 멀티캐스트 VLAN으로 IPTV 트래픽 분리

## 표준 위치

- RFC 4541 — Informational, snooping 동작 고려사항
- 실제 동작은 벤더 구현에 의존

## 검색 힌트

- "IGMP snooping 동작" → 본 카드 동작 메커니즘 섹션
- "mrouter port" → 본 카드
- "fast leave immediate leave" → 본 카드 Leave Latency 섹션
- "IPTV 채널 변경 지연" → 본 카드 + Immediate Leave
- "MVR 멀티캐스트 VLAN" → 본 카드 가입자망 운영 섹션
