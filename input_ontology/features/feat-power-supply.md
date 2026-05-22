---
id: feat:power-supply
type: Feature
name_en: Power Supply
name_ko: 전원 공급 장치
aliases:
  - PSU
  - power
  - AC power
  - DC power
  - redundant power
  - PoE
  - battery backup
  - UPS
implements: []
vendors:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
documented_in:
  - "가입자망장비_manual/다산_L2"
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/다산_OLT"
  - "가입자망장비_manual/유비쿼스_L2"
  - "가입자망장비_manual/유비쿼스_L3"
  - "가입자망장비_manual/유비쿼스_OLT"
keywords_en:
  - power supply
  - PSU
  - AC
  - DC
  - 110V
  - 220V
  - -48V
  - redundant
  - dual power
  - hot-swap
  - PoE
  - battery
  - backup
  - installation
keywords_ko:
  - 전원
  - 전원 공급
  - 전원 공급 장치
  - PSU
  - 교류
  - 직류
  - AC
  - DC
  - 배터리
  - 설치
  - 이중화
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

전원 공급 장치(PSU, Power Supply Unit)는 네트워크 장비의 동작 전원을 공급하는 하드웨어 모듈이다. 가입자망 장비는 운영 환경에 따라 AC(110/220V), DC(-48V 통신용), 배터리 내장형 등 다양한 전원 옵션을 제공한다. 고가용성이 필요한 장비는 이중화 PSU와 핫스왑을 지원한다.

## 전원 종류

| 종류 | 전압/규격 | 용도 |
|---|---|---|
| **AC** | 100~240V, 50/60Hz | 일반 사무실·소규모 |
| **DC** | -48V (통신용) | 통신사업자 국사·집중국 |
| **PoE/PoE+** | 802.3af/at (출력) | IP폰·AP·CCTV 급전 |
| **배터리 내장** | Li-ion / 납축전지 | 정전 백업 (V3024VB, E5924LB 등) |

## 설치 절차 (일반)

1. **사전 확인**:
   - 정격 전압·전류 확인 (장비 라벨)
   - 접지(어스) 단자 연결
   - 적합한 전원 케이블 (한국: 220V 3핀)
2. **설치**:
   - PSU 모듈을 슬롯에 삽입 (이중화/핫스왑 장비)
   - 잠금 나사/레버 고정
3. **전원 인가**:
   - 차단기 OFF 상태에서 케이블 연결
   - 차단기 ON, PWR LED 점등 확인
4. **검증**:
   - `show environment power` (Cisco)
   - `show power` (Dasan/Ubiquoss)

## 이중화 PSU

- 두 PSU 모두 동시 동작(로드 셰어링)
- 1개 PSU 장애 시 나머지가 전체 부하 인수 → 무중단
- 한 PSU는 다른 회로(다른 분전반)에서 급전 권장 (분전반 단위 장애 대비)
- 핫스왑(Hot-swap): 동작 중 PSU 교체 가능

## 배터리 내장형 모델

가입자망 옥외 함체·정전 백업이 필요한 환경:
- 다산 [V3024VB](../devices/model-dasan-v3024vb.md)
- 유비쿼스 [E5924L/E5924LB](../devices/model-ubiquoss-e5924l.md)

배터리 상태 모니터링 명령어: 잔량(%), 온도, 충방전 상태, 예상 동작 시간.

## 운영 고려사항

- **접지 필수**: 낙뢰·서지 보호의 기본
- **AC 변동 대응**: UPS와 결합 권장
- **PoE 예산 (Power Budget)**: 모든 PoE 포트 동시 사용 시 합계 출력이 PSU 정격 이내인지 확인
- **배터리 수명**: 통상 3~5년, 정기 교체 권장

## 검색 힌트

- "전원 공급 장치" "PSU" → 본 카드
- "AC 전원 설치" → 본 카드 설치 절차
- "이중화 전원" → 본 카드 이중화 PSU 섹션
- "배터리 내장형 스위치" → 본 카드 + V3024VB/E5924L 카드
- "PoE 예산" → 본 카드 운영 고려사항
- "스위치 전원 설치 절차" → 본 카드 (KO-012 cover)
