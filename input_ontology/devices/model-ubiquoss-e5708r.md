---
id: model:ubiquoss-e5708r
type: DeviceModel
vendor: vendor:ubiquoss
name: E5708R
role: L2
manual_paths:
  - "가입자망장비_manual/유비쿼스_L2/E5708R_HW_Installation Guide.md"
  - "가입자망장비_manual/유비쿼스_L2/E57xxRC_SW_User Guide__sec-01.md"
  - "가입자망장비_manual/유비쿼스_L2/E57xxRC_SW_User Guide__sec-02.md"
  - "가입자망장비_manual/유비쿼스_L2/E57xxRC_SW_User Guide__sec-03.md"
  - "가입자망장비_manual/유비쿼스_L2/E57xxRC_SW_User Guide__sec-04.md"
  - "가입자망장비_manual/유비쿼스_L2/E57xxRC_SW_User Guide__sec-05.md"
  - "가입자망장비_manual/유비쿼스_L2/E57xxRC_SW_User Guide__sec-06.md"
  - "가입자망장비_manual/유비쿼스_L2/E57xxRC_SW_User Guide__sec-07.md"
  - "가입자망장비_manual/유비쿼스_L2/E57xxRC_SW_User Guide__sec-08.md"
supports_features:
  - feat:dot1q-tunnel
  - feat:port-security
  - feat:mac-address-table
  - feat:port-mirroring
  - feat:console-access
keywords_en:
  # Model-specific terms only. Generic "L2 switch"/"GbE"/"LED status" removed
  # to prevent matches on unrelated vendor/model queries.
  - E5708R
  - E5708
  - E57xxRC
  - 유비쿼스 E5708R
keywords_ko:
  - E5708R
  - E5708
  - 유비쿼스 E5708R
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

유비쿼스 E5708R은 8-포트 GbE L2 이더넷 스위치다. E57xxRC 시리즈 소프트웨어를 공유하며, FTTH 가입자 분기·소형 사업장 분배에 사용된다.

## 매뉴얼 위치

- **HW 설치**: `유비쿼스_L2/E5708R_HW_Installation Guide.md` (단일 파일)
- **SW 사용자 가이드 (E57xxRC 공유)**: `유비쿼스_L2/E57xxRC_SW_User Guide__sec-*.md` (sec-01 ~ sec-08)

## LED 표시

전면 패널 LED:
- **PWR** (전원): 녹색 점등 = 정상
- **SYS** (시스템): 부팅 중 점멸, 정상 동작 시 점등
- **포트별 LINK/ACT**: 링크 확립 시 점등, 트래픽 시 점멸
- **속도 표시**: 1G/100M/10M 색상 구분 (모델별 상이)

상세는 `E5708R_HW_Installation Guide.md` 참고.

## 검색 힌트

- "E5708R" → 본 카드
- "유비쿼스 E5708R LED" → 본 카드 LED 표시 섹션
- "유비쿼스 8포트" → 본 카드
- "E57xxRC 시리즈" → 본 카드 (SW 매뉴얼 공유)
