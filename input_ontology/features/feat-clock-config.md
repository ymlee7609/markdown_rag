---
id: feat:clock-config
type: Feature
name_en: System Clock Configuration
name_ko: 시스템 시간 / 클록 설정
aliases:
  - clock set
  - system time
  - timezone
  - date setting
  - hardware clock
implements: []
configures:
  - proto:ntp
vendors:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
documented_in:
  - "가입자망장비_manual/다산_L2"
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L2"
  - "가입자망장비_manual/유비쿼스_L3"
keywords_en:
  - clock
  - clock set
  - system time
  - timezone
  - NTP
  - date
  - hardware clock
  - RTC
  - UTC
  - KST
keywords_ko:
  - 클록
  - 시간 설정
  - 날짜 설정
  - 시스템 시간
  - 시간대
  - 표준시
  - clock
  - NTP
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

시스템 클록(시간) 설정은 네트워크 장비의 정확한 시각을 유지하는 운영 기본 작업이다. Syslog/AAA/인증서/SNMP trap timestamp의 신뢰성과 분산 시스템 동기화의 기반이 된다. 수동 설정(`clock set`)과 NTP 자동 동기화 두 방법이 있으며, 운영 환경에서는 NTP 권장.

## 설정 방법

### 1. 수동 설정 (`clock set`)

| Vendor | 명령어 |
|---|---|
| Cisco | `clock set HH:MM:SS DAY MONTH YEAR` (exec 모드) |
| Dasan | `clock set YYYY-MM-DD HH:MM:SS` |
| Ubiquoss | `clock set HH:MM:SS DAY MONTH YEAR` |

### 2. 시간대 (Timezone) 설정

한국 표준시(KST = UTC+9):
- Cisco: `clock timezone KST 9`
- Dasan: `clock timezone +9` 또는 `clock timezone Asia/Seoul`
- Ubiquoss: `clock timezone KST 9`

### 3. NTP 자동 동기화 (권장)

```
ntp server <pool.ntp.org 또는 내부 NTP 서버 IP>
```

## 검증

- `show clock` — 현재 시간 표시
- `show ntp status` / `show ntp associations` — NTP 동기화 상태

## 운영 고려사항

- **하드웨어 클록 (RTC)**: 배터리로 전원 단절 시에도 시간 유지 (일부 저가형 장비는 RTC 없음)
- **재부팅 후 시간 리셋**: RTC가 없는 장비는 NTP가 필수
- **시간대 변경 시 로그 영향**: 기존 로그 timestamp 해석 주의
- **NTP 인증**: 운영 환경에서는 MD5/SHA 키로 NTP peer 인증 권장

## 관련 프로토콜

- [proto:ntp](../protocols/proto-ntp.md) — Network Time Protocol, RFC 5905

## 검색 힌트

- "시간 설정" "clock 설정" → 본 카드
- "스위치 날짜 시간" → 본 카드
- "시간대 KST 설정" → 본 카드 timezone 섹션
- "NTP 서버 설정" → 본 카드 + `proto:ntp`
- "재부팅 후 시간 초기화" → 본 카드 운영 고려사항
