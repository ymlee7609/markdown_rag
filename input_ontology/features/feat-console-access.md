---
id: feat:console-access
type: Feature
name_en: Console Access (Serial)
name_ko: 콘솔 접속 (시리얼)
aliases:
  - console port
  - serial console
  - RS-232
  - RJ-45 console
  - USB console
  - out-of-band access
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
  - console port
  - serial cable
  - RS-232
  - RJ-45
  - USB console
  - 9600 baud
  - terminal emulator
  - putty
  - minicom
  - tera term
  - out-of-band
keywords_ko:
  - 콘솔
  - 콘솔 포트
  - 시리얼 케이블
  - 시리얼
  - 터미널
  - 직접 접속
  - 접속
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

콘솔(Console) 포트는 네트워크 장비의 시리얼 관리 인터페이스다. 네트워크 연결 없이 직접 케이블로 접속해 부팅 메시지·초기 설정·복구 작업을 수행한다. 신규 장비 초기 설정과 IP 분실·접근 불가 상황에서 필수.

## 물리 인터페이스

| 형태 | 비고 |
|---|---|
| **RJ-45 콘솔** (Cisco 전통) | 시리얼-RJ45 변환 케이블(롤오버 케이블) 필요 |
| **DB-9 (RS-232)** | 일부 구형 장비 |
| **USB-C / USB Mini-B** | 최근 장비, USB-Serial 드라이버 필요 |

## 표준 시리얼 설정

| 파라미터 | 값 |
|---|---|
| Baud rate | 9600 (대부분), 일부 115200 |
| Data bits | 8 |
| Parity | None |
| Stop bits | 1 |
| Flow control | None |

## 호스트 측 도구

- **PuTTY** (Windows) — 가장 흔한 시리얼 터미널
- **Tera Term** (Windows) — 한국에서 자주 사용
- **minicom** (Linux) — `minicom -D /dev/ttyUSB0 -b 9600`
- **screen** (macOS/Linux) — `screen /dev/tty.usbserial 9600`

## 접속 절차

1. 호스트와 장비를 콘솔 케이블로 연결 (USB-Serial 변환기 사용 시 드라이버 설치)
2. OS의 시리얼 포트 번호 확인 (Windows: COM*, Linux: /dev/ttyUSB*)
3. 터미널 에뮬레이터에서 위 표준 설정으로 연결
4. Enter 키를 눌러 프롬프트 확인
5. 기본 로그인 (장비별 default 계정/비밀번호 매뉴얼 참조)

## 가입자망 운영 고려사항

- 콘솔 포트는 보안이 약함(평문) → 물리 접근 통제 필수
- IP 관리(SSH/Telnet) 차단 시 콘솔이 마지막 복구 경로
- 비밀번호 분실 시: 콘솔로 부팅 중단 → ROMmon/U-Boot 진입 → 패스워드 리셋

## 검색 힌트

- "콘솔 포트 접속" → 본 카드
- "시리얼 케이블 연결" → 본 카드 + 물리 인터페이스 섹션
- "9600 baud" → 본 카드 시리얼 설정
- "PuTTY 시리얼 접속" → 본 카드 호스트 측 도구
- "비밀번호 분실 복구" → 본 카드 운영 고려사항
