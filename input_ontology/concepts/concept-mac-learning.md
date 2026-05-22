---
id: concept:mac-learning
type: Concept
name_en: MAC Address Learning
name_ko: MAC 주소 학습
parent_protocol: proto:stp
scope: algorithm
aliases:
  - MAC learning
  - source MAC learning
  - transparent bridging
  - L2 learning
defined_by:
  - std:ieee-802.1d
related:
  - proto:stp
  - feat:mac-address-table
  - feat:port-security
keywords_en:
  - MAC learning
  - source MAC
  - transparent bridge
  - flooding
  - forwarding
  - aging
  - unknown unicast
keywords_ko:
  - MAC 학습
  - 출발지 MAC
  - 투명 브리지
  - 플러딩
  - 포워딩
  - 에이징
  - 미지의 유니캐스트
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

MAC 학습(MAC Learning, Source MAC Learning)은 L2 스위치가 들어오는 프레임의 출발지(source) MAC 주소와 수신 포트를 보고 MAC 주소 테이블을 자동으로 갱신하는 핵심 메커니즘이다. 투명 브리지(transparent bridge)의 기본 동작 원리이며, 802.1D가 정의한다.

## 학습 절차 (Receive 시)

1. 프레임 수신
2. **Source MAC 추출**: 어느 포트에 어느 호스트가 있는지 학습
3. MAC 주소 테이블에 (VLAN, source MAC) 키로 lookup
   - 없으면 신규 등록 (Type: dynamic)
   - 있고 같은 포트면 timestamp만 갱신
   - 있고 다른 포트면 → 갱신 (MAC flapping 감지)
4. **Destination MAC lookup**:
   - 있으면 해당 포트로 포워딩
   - 없으면 같은 VLAN의 모든 포트로 플러딩 (unknown unicast flooding)

## 포워딩 결정

| 목적지 MAC | 행위 |
|---|---|
| 알려진 unicast | 학습된 포트로 forward |
| 알려지지 않은 unicast | 같은 VLAN 모든 포트로 flooding |
| Broadcast (FF:FF:FF:FF:FF:FF) | 모든 포트로 flooding |
| Multicast | IGMP snooping 없으면 flooding, 있으면 멤버 포트만 |

## Aging

각 dynamic 엔트리는 마지막 학습 시각 timestamp 보유.
- 기본 aging time: 300초 (5분)
- aging 만료 시 엔트리 삭제 → 다음 트래픽에서 재학습

## 관련 이슈

- **MAC Flapping**: 같은 MAC이 짧은 시간에 여러 포트에서 학습 → 루프·이중화 문제 또는 보안 사고
- **MAC Flooding 공격**: 가짜 MAC을 대량 주입해 테이블 overflow → 모든 트래픽 flooding → 패킷 캡처
  - 방어: `feat:port-security`로 포트당 학습 MAC 수 제한

## 검색 힌트

- "MAC 학습" → 본 카드
- "투명 브리지 동작" → 본 카드
- "unknown unicast flooding" → 본 카드 포워딩 결정 섹션
- "MAC aging" → 본 카드 Aging 섹션
- "MAC flapping" → 본 카드 관련 이슈
- "MAC flooding attack" → 본 카드 관련 이슈
