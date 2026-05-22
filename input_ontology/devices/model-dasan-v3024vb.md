---
id: model:dasan-v3024vb
type: DeviceModel
vendor: vendor:dasan
name: V3024VB
role: L2
os_version: "UMNnos (V3024VB)"
manual_paths:
  - "가입자망장비_manual/다산_L2/다산_배터리 내장형 V3024VB_명령어메뉴얼_230413_V1__sec-01.md"
  - "가입자망장비_manual/다산_L2/다산_배터리 내장형 V3024VB_명령어메뉴얼_230413_V1__sec-02.md"
  - "가입자망장비_manual/다산_L2/다산_배터리 내장형 V3024VB_명령어메뉴얼_230413_V1__sec-03.md"
  - "가입자망장비_manual/다산_L2/다산_배터리 내장형 V3024VB_명령어메뉴얼_230413_V1__sec-04.md"
  - "가입자망장비_manual/다산_L2/다산_배터리 내장형 V3024VB_명령어메뉴얼_230413_V1__sec-05.md"
  - "가입자망장비_manual/다산_L2/다산_배터리 내장형 V3024VB_명령어메뉴얼_230413_V1__sec-06.md"
  - "가입자망장비_manual/다산_L2/다산_배터리 내장형 V3024VB_명령어메뉴얼_230413_V1__sec-07.md"
  - "가입자망장비_manual/다산_L2/다산_배터리 내장형 V3024VB_명령어메뉴얼_230413_V1__sec-08.md"
supports_features:
  - feat:dot1q-tunnel
  - feat:port-security
  - feat:mac-address-table
  - feat:port-mirroring
  - feat:console-access
  - feat:power-supply
  - feat:firmware-upgrade
keywords_en:
  # Model-specific identifiers only (general "battery"/"24 port" removed).
  - V3024VB
  - 다산 V3024VB
keywords_ko:
  - V3024VB
  - 다산 V3024VB
  - 다산 배터리 내장형
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

다산네트웍스 V3024VB는 V3024V의 **배터리 내장형(battery-backed)** 변형 모델이다. 정전 시 일정 시간 동작을 지속할 수 있도록 내장 배터리를 갖춰, 정전 백업이 필요한 가입자 분배함·옥외 함체에 사용된다. 24개 GbE 포트는 V3024V와 동일.

## 매뉴얼 위치

`input_optimized/가입자망장비_manual/다산_L2/다산_배터리 내장형 V3024VB_명령어메뉴얼_230413_V1__sec-*.md` (8개 섹션)

매뉴얼 날짜: 2023-04-13.

## V3024V 대비 차이

- **배터리 모듈 내장**: 정전 시 단시간 동작 지속
- **배터리 상태 모니터링 명령어**: 잔량·온도·충방전 상태 조회
- **하드웨어**: 배터리 수용 공간 추가로 폼팩터 차이
- 소프트웨어 기능은 V3024V와 거의 동일

## 검색 힌트

- "V3024VB" → 본 카드
- "다산 배터리 내장형" → 본 카드
- "V3024VB 사양" → 본 카드 + 매뉴얼 sec-01
- "정전 시 동작 스위치" → 본 카드 + `feat:power-supply`
