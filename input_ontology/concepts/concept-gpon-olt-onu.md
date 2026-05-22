---
id: concept:gpon-olt-onu
type: Concept
name_en: GPON OLT-ONU Architecture
name_ko: GPON OLT-ONU 구조
parent_protocol: proto:gpon
scope: role
aliases:
  - OLT
  - ONU
  - ONT
  - PON architecture
  - point-to-multipoint
defined_by:
  - std:itu-t-g.984
related:
  - proto:gpon
  - concept:gpon-tcont
keywords_en:
  - OLT
  - ONU
  - ONT
  - passive splitter
  - point-to-multipoint
  - downstream
  - upstream
  - broadcast
  - TDMA
  - ranging
keywords_ko:
  - OLT
  - ONU
  - ONT
  - 광 분기기
  - 광 종단
  - 가입자측
  - 국사측
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

GPON은 한 OLT가 광 분기기(passive splitter)를 통해 다수(보통 32~128개)의 ONU/ONT와 연결되는 점-다점(P2MP) 구조다. 분기기에는 전원이 필요 없고(passive), 광 신호를 그대로 1:N 분할한다. 하향(downstream)은 OLT가 모든 ONU로 브로드캐스트 후 ONU가 자기 트래픽만 필터링하고, 상향(upstream)은 TDMA로 시간 슬롯을 나눠 충돌을 방지한다.

## 구성 요소

| 구성요소 | 위치 | 역할 |
|---|---|---|
| OLT (Optical Line Terminal) | 국사 (CO) | 가입자망 종단, IP 라우팅·VLAN·인증 처리 |
| Splitter | 중간 (외부함체/맨홀) | 광 신호 1:N 분기 (수동) |
| ONU (Optical Network Unit) | 가입자측 | 광-전기 변환, L2 동작 |
| ONT (Optical Network Terminal) | 가입자측 | ONU + 가입자 인터페이스 (LAN/WiFi/POTS) |

> ONU와 ONT는 ITU-T에서 미묘하게 구분하지만 실무에서는 혼용되는 경우가 많다.

## 하향 (Downstream) 동작

- OLT → 모든 ONU로 브로드캐스트 (2.488 Gbps, 1490nm 파장)
- GEM 프레임의 Port-ID로 ONU가 자기 트래픽 필터링
- AES-128 암호화 (ONU별 키)

## 상향 (Upstream) 동작

- 모든 ONU → OLT (1.244 Gbps, 1310nm 파장)
- TDMA: 각 ONU는 OLT가 할당한 시간 슬롯에만 송신
- **Ranging**: OLT가 각 ONU까지 광 거리(왕복 시간) 측정 → 슬롯 타이밍 동기
- **DBA** (Dynamic Bandwidth Allocation): T-CONT 단위 동적 할당

## OMCI (G.984.4)

OLT가 ONU를 원격 관리·구성:
- ONU 등록·인증·activation
- T-CONT/GEM port 구성
- 가입자 인터페이스 정책 적용
- 펌웨어 업그레이드

## 가입자 식별

- **ONU Serial Number** (S/N): 8자리 ASCII + 4바이트 vendor ID
- **PLOAM messages**: ONU 등록 및 인증 시 사용
- **ONU-ID**: OLT가 동적으로 할당 (0~252)

## 검색 힌트

- "OLT ONU 차이" → 본 카드 구성 요소 표
- "GPON 구조" → 본 카드 (P2MP, splitter)
- "ranging" → 본 카드 상향 동작 섹션
- "OMCI" → 본 카드 OMCI 섹션
- "ONU 등록 절차" → 본 카드 + 다산/유비쿼스 OLT 매뉴얼
- "광 분기기 splitter" → 본 카드
