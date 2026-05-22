---
id: model:ubiquoss-e5924l
type: DeviceModel
vendor: vendor:ubiquoss
name: E5924L / E5924LB
role: L2
manual_paths:
  - "가입자망장비_manual/유비쿼스_L2/E5924L_HW_Installtion Guide.md"
  - "가입자망장비_manual/유비쿼스_L2/E5924L_SW_User Guide"
  - "가입자망장비_manual/유비쿼스_L2/E5924LB_HW_Installtion Guide.md"
  - "가입자망장비_manual/유비쿼스_L2/E5924LB_SW_User Guide"
supports_features:
  - feat:dot1q-tunnel
  - feat:port-security
  - feat:mac-address-table
  - feat:port-mirroring
  - feat:console-access
  - feat:power-supply
  - feat:firmware-upgrade
keywords_en:
  # Model-specific terms only. Removed generic "battery"/"L2 switch"/"24 port".
  # 배터리 keyword retained for E5924L (battery-backed variant identifier).
  - E5924L
  - E5924LB
  - 유비쿼스 E5924L
  - 유비쿼스 E5924LB
keywords_ko:
  - E5924L
  - E5924LB
  - 유비쿼스 E5924L
  - 유비쿼스 배터리 내장형
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

유비쿼스 E5924L과 E5924LB는 24-포트 L2 스위치다. **L**B는 배터리 내장형(battery-backed) 변형으로, 정전 시 단시간 동작을 지속한다. 다산 V3024VB와 유사한 백업 전원 솔루션. 가입자 분배함·옥외 함체에 사용.

## 매뉴얼 위치

- `유비쿼스_L2/E5924L_HW_Installtion Guide.md` — 기본 모델 HW
- `유비쿼스_L2/E5924L_SW_User Guide/` — 기본 모델 SW
- `유비쿼스_L2/E5924LB_HW_Installtion Guide.md` — 배터리 모델 HW
- `유비쿼스_L2/E5924LB_SW_User Guide/` — 배터리 모델 SW

## E5924L vs E5924LB

| 항목 | E5924L | E5924LB |
|---|---|---|
| 폼팩터 | 표준 | 배터리 수용 공간 확장 |
| 정전 백업 | X | O (내장 배터리) |
| 배터리 상태 모니터링 | - | 잔량/온도/충방전 명령어 지원 |
| 포트 수 | 24 | 24 |
| SW 기능 | 동일 | 동일 (+ 배터리 관리) |

## 검색 힌트

- "E5924L" "E5924LB" → 본 카드
- "유비쿼스 배터리 내장형" → 본 카드
- "유비쿼스 24포트 L2" → 본 카드
- "정전 백업 스위치" → 본 카드 + 다산 V3024VB
