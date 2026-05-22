---
id: proto:gpon
type: Protocol
name_en: GPON
name_ko: 기가비트 수동 광 네트워크 (GPON)
aliases:
  - Gigabit-capable PON
  - G.984
  - GPON
layer: L1
family: access
status: active
defined_by:
  - std:itu-t-g.984
extends: []
related:
  - concept:gpon-olt-onu
  - concept:gpon-tcont
  - proto:pppoe
  - proto:dhcp
  - proto:igmp
references: []
taught_in: []          # CCIE에는 GPON 비중이 낮음
documented_in:
  - "가입자망장비_manual/다산_OLT"
  - "가입자망장비_manual/유비쿼스_OLT"
vendors_supporting:
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - GPON
  - G.984
  - OLT
  - ONU
  - ONT
  - T-CONT
  - GEM port
  - downstream
  - upstream
  - 2.488 Gbps
  - 1.244 Gbps
  - PON
  - passive optical network
  - splitter
  - OMCI
keywords_ko:
  - GPON
  - 광 가입자망
  - 광 회선
  - 가입자망
  - 광망
  - 광 분기
  - 광 종단
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

GPON(Gigabit-capable Passive Optical Network)은 ITU-T G.984가 정의하는 광 가입자망 기술이다. 한 OLT(Optical Line Terminal)가 광 분기기(passive splitter)를 통해 다수의 ONU/ONT(Optical Network Unit/Terminal)와 점-다점(P2MP) 구조로 연결된다. 하향(downstream) 2.488 Gbps, 상향(upstream) 1.244 Gbps이 표준 속도이며, 한국 통신사업자(KT/SK/LGU+)의 FTTH 가입자망 핵심 기술이다.

## 표준 / 정의

- **ITU-T G.984.1** — General characteristics
- **ITU-T G.984.2** — Physical Media Dependent layer
- **ITU-T G.984.3** — Transmission Convergence layer (GEM 프레이밍)
- **ITU-T G.984.4** — OMCI (ONT Management and Control Interface)

## 후속 표준

- **ITU-T G.987** — XG-PON (10G 하향, 2.5G 상향)
- **ITU-T G.9807** — XGS-PON (10G 대칭)
- **ITU-T G.989** — NG-PON2 (TWDM-PON 40G)

## 핵심 개념

- [OLT-ONU Architecture](../concepts/concept-gpon-olt-onu.md) — P2MP 구조, 광 분기기 기반
- [T-CONT (Transmission Container)](../concepts/concept-gpon-tcont.md) — 상향 대역 할당 단위

## 상위 계층 프로토콜 (가입자 인증·서비스)

GPON은 L1/L2 가입자망 전송로이고, 그 위에 다음이 동작:
- **`proto:pppoe`** — 가입자 인증
- **`proto:dhcp`** — IP 할당
- **`proto:igmp`** — IPTV 멀티캐스트
- **`proto:vlan`** — S-VLAN(서비스 VLAN)으로 가입자/서비스 분리

## 핵심 동작 메커니즘

- **TDMA 상향 다중화**: OLT가 각 ONU에게 시간슬롯 할당, ONU는 자기 슬롯에만 송신
- **DBA (Dynamic Bandwidth Allocation)**: T-CONT 단위로 동적 대역 재할당
- **OMCI**: OLT가 ONU를 원격 관리·구성 (G.984.4)
- **거리 측정 (Ranging)**: OLT가 각 ONU까지 광 거리 측정, 슬롯 타이밍 보정

## 벤더 구현 매핑

| Vendor | 주요 명령어 영역 | 매뉴얼 |
|---|---|---|
| Dasan OLT (V58xx 등) | `gpon`, `onu`, `tcont`, `gem-port`, `dba-profile` | `가입자망장비_manual/다산_OLT/` |
| Ubiquoss OLT (E61xx, P8624 등) | `gpon`, `onu`, `tcont profile`, `gem profile` | `가입자망장비_manual/유비쿼스_OLT/` |

## 검색 힌트

- "GPON 표준" → 본 카드 + `std:itu-t-g.984`
- "OLT ONU 차이" → `concept:gpon-olt-onu`
- "T-CONT 대역 할당" → `concept:gpon-tcont`
- "DBA" → 본 카드 핵심 동작 메커니즘
- "FTTH 가입자망" → 본 카드 + 다산/유비쿼스 OLT 매뉴얼
- "다산 OLT GPON 설정" → 본 카드 documented_in + 다산_OLT 매뉴얼
- "광 분기기" → 본 카드 (passive splitter)
