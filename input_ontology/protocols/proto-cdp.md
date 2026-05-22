---
id: proto:cdp
type: Protocol
name_en: CDP
name_ko: Cisco 발견 프로토콜 (CDP)
aliases:
  - Cisco Discovery Protocol
  - CDPv2
layer: L2
family: management
status: active
defined_by: []        # Cisco 독점 (IETF 표준 없음), LLDP는 IEEE 802.1AB
extends: []
related:
  - proto:lldp
references: []
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-01.md"
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-02.md"
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-04.md"
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-05.md"
documented_in: []     # 비-Cisco 벤더는 LLDP 사용
vendors_supporting:
  - vendor:cisco
keywords_en:
  - CDP
  - Cisco Discovery Protocol
  - CDPv2
  - neighbor
  - device
  - capabilities
  - platform
  - port ID
  - hold time
  - multicast 01:00:0C:CC:CC:CC
keywords_ko:
  - CDP
  - 시스코 발견
  - 이웃
  - 장비 발견
  - 네이버
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

CDP(Cisco Discovery Protocol)는 직접 연결된 Cisco 장비끼리 자동으로 서로의 정보(장비 이름·플랫폼·IOS 버전·인터페이스·IP·VLAN·capabilities)를 교환하는 Cisco 독점 L2 프로토콜이다. SNAP 캡슐화로 멀티캐스트(01:00:0C:CC:CC:CC)에 송신되며, 기본 60초마다 광고하고 180초 holdtime을 유지한다. 비-Cisco 벤더는 IEEE 표준인 **LLDP**(802.1AB)를 사용한다.

## 표준 위치

- **Cisco 독점**: IETF/IEEE 표준화 안 됨
- 호환 표준: **IEEE 802.1AB** (LLDP, Link Layer Discovery Protocol, `proto:lldp`)
- 일부 비-Cisco 장비도 CDP를 부분 지원하나 비공식

## 주요 동작

- L2 SNAP 프레임 (EtherType 0x2000)
- 송신 주소: 멀티캐스트 `01:00:0C:CC:CC:CC` (스위치 CPU로 전달, 일반 포트로 flooded 안 됨)
- 기본 광고 주기 60초, holdtime 180초
- CDPv2 (현행): 추가 TLV (Native VLAN, Trust Bitmap 등)

## 운영 명령어 (Cisco)

```
cdp run                            ! 전역 활성화 (기본 on)
no cdp run                         ! 전역 비활성화
cdp enable / no cdp enable         ! 인터페이스 단위
show cdp neighbors                 ! 이웃 요약
show cdp neighbors detail          ! 이웃 상세 (IP·플랫폼·IOS·capabilities)
show cdp entry <name>              ! 특정 이웃
clear cdp counters                 ! 카운터 초기화
```

## 보안 고려

CDP는 정보 노출이 큼 (IOS 버전·플랫폼이 평문). 외부 노출 인터페이스나 미신뢰 구간에서는 비활성화 권장. 인터페이스 단위 `no cdp enable` 사용.

## CDP vs LLDP

| 항목 | CDP | LLDP |
|---|---|---|
| 표준 | Cisco 독점 | IEEE 802.1AB |
| 멀티 벤더 | X | O |
| Cisco IOS 기본값 | on | off (활성화 필요) |
| 광고 주기 | 60s | 30s |
| Holdtime | 180s | 120s |

## 검색 힌트

- "CDP" "Cisco Discovery Protocol" → 본 카드
- "show cdp neighbors" → 본 카드 운영 명령어
- "Cisco 이웃 발견" → 본 카드
- "CDP vs LLDP" → 본 카드 비교 표
- "01:00:0C:CC:CC:CC" → 본 카드 주요 동작
