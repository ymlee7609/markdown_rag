---
id: feat:dot1q-tunnel
type: Feature
name_en: 802.1Q Tunneling (Q-in-Q)
name_ko: Q-in-Q (이중 VLAN 태깅 터널)
aliases:
  - Q-in-Q
  - QinQ
  - 802.1Q tunneling
  - dot1q-tunnel
  - stacked VLAN
  - VLAN stacking
implements:
  - proto:vlan
  - concept:vlan-trunk
configures:
  - proto:vlan
vendors:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
device_scope:
  - model:dasan-v3024v
  # 추가 모델은 M3 LLM 확장에서 documented_in 코퍼스 분석 후 보강
documented_in:
  - "가입자망장비_manual/다산_L2"
  - "가입자망장비_manual/유비쿼스_L2"
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-07.md"
related:
  - proto:vlan
  - std:ieee-802.1q
  - feat:port-security
keywords_en:
  - Q-in-Q
  - dot1q-tunnel
  - service VLAN
  - S-VLAN
  - C-VLAN
  - customer VLAN
  - provider bridge
  - 802.1ad
keywords_ko:
  - Q-in-Q
  - 이중 태깅
  - 서비스 VLAN
  - 고객 VLAN
  - 캐리어 이더넷
confidence: 0.95
source: human
last_reviewed: 2026-05-22
---

## 개요

Q-in-Q(802.1Q tunneling, dot1q-tunnel)은 고객 트래픽의 기존 VLAN 태그(C-VLAN, Customer VLAN)를 보존한 채 상위에 서비스 제공자의 VLAN 태그(S-VLAN, Service VLAN)를 추가로 캡슐화하여 캐리어 이더넷 망을 통과시키는 기능이다. 가입자망 장비에서 서비스 분리·격리에 흔히 사용된다.

## 구현 표준

- **IEEE 802.1Q** — 원본 단일 태깅 표준 (`std:ieee-802.1q`)
- **IEEE 802.1ad** — Provider Bridges, Q-in-Q 표준화 (별도 std 카드 추가 검토 대상)

## 동작 개념

- 가입자 측(Customer-facing) 포트는 `dot1q-tunnel` 모드로 설정
- 들어온 프레임의 기존 802.1Q 태그를 그대로 둔 채, 외곽에 S-VLAN 태그를 push
- 망 내부(Provider 망)에서는 S-VLAN 기준 전송
- 가입자 측 출구에서 S-VLAN 태그 pop, 원본 C-VLAN 태그만 남아 전달
- MTU는 최소 1504바이트 필요(태그 4B × 2)

## 벤더 명령어 매핑 (요약)

| Vendor | 모드 설정 명령어 | 매뉴얼 위치 |
|---|---|---|
| Cisco | `switchport mode dot1q-tunnel` | `Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-07.md` |
| Dasan | `vlan dot1q-tunnel` (모델별 상이) | `가입자망장비_manual/다산_L2/` 모델별 sec |
| Ubiquoss | `switchport access vlan ... tunnel` | `가입자망장비_manual/유비쿼스_L2/` 모델별 sec |

> 구체 모델별 명령어 차이는 M3 LLM 확장 단계에서 Command 카드로 분리 추출 예정.

## 교차 참조

- `proto:vlan` — 기반 프로토콜
- `concept:vlan-trunk` — Trunk port가 S-VLAN 통과 경로
- `std:ieee-802.1q` — 원본 표준
- 관련 보안 기능: `feat:port-security` (가입자 측 보호)

## 검색 힌트

- "Q-in-Q 설정" → 본 카드 + 벤더 매뉴얼 사진
- "이중 VLAN 태깅" → 본 카드 (ko_alias 매칭)
- "S-VLAN과 C-VLAN 차이" → 본 카드 동작 개념 섹션
- "다산 OLT Q-in-Q 명령어" → 본 카드 documented_in + 다산 매뉴얼 청크
