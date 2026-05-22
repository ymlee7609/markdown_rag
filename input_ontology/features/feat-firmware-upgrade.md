---
id: feat:firmware-upgrade
type: Feature
name_en: Firmware / Software Upgrade
name_ko: 펌웨어 / 소프트웨어 업그레이드
aliases:
  - firmware upgrade
  - software upgrade
  - image upgrade
  - IOS upgrade
  - NOS upgrade
  - OS upgrade
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
  - firmware upgrade
  - software upgrade
  - image
  - boot
  - TFTP
  - FTP
  - SCP
  - HTTP
  - reload
  - reboot
  - backup
  - rollback
keywords_ko:
  - 펌웨어
  - 소프트웨어
  - 업그레이드
  - 업데이트
  - 이미지
  - 부팅
  - 재부팅
  - 백업
  - 롤백
  - 절차
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

펌웨어(또는 소프트웨어/이미지) 업그레이드는 스위치·라우터·OLT의 NOS(Network OS)를 새 버전으로 교체하는 절차다. 보안 패치, 버그 수정, 신규 기능 도입 시 수행. 잘못된 절차는 장비 다운·동작 불능을 초래하므로 단계별 검증이 중요.

## 표준 절차 (공통)

1. **사전 점검**:
   - 현재 버전 확인 (`show version`)
   - 디스크 공간 확인 (`dir flash:`)
   - 설정 백업 (`copy running-config startup-config` + 외부 보관)
2. **이미지 전송**:
   - TFTP/FTP/SCP/HTTP로 새 이미지 다운로드 (`copy tftp://server/image.bin flash:`)
   - 무결성 검증 (MD5/SHA256 체크섬)
3. **부팅 이미지 지정**:
   - `boot system flash:new-image.bin`
4. **재부팅**:
   - `reload` (또는 `reboot`)
5. **사후 검증**:
   - 새 버전 확인 (`show version`)
   - 핵심 기능 동작 확인 (인터페이스 up, 라우팅 수렴 등)
6. **롤백 준비**: 기존 이미지를 일정 기간 보존

## 벤더별 명령어 차이

| Vendor | 이미지 전송 | 부팅 지정 | 재부팅 |
|---|---|---|---|
| Cisco | `copy tftp: flash:` | `boot system flash:` | `reload` |
| Dasan | `copy tftp ...`, `copy ftp ...` | `boot-os ...` (모델별) | `reload` |
| Ubiquoss | `copy tftp ...` | `boot-image ...` | `reload` |

> 모델별 정확한 명령어는 매뉴얼 참조.

## 가입자망 운영 고려사항

- **이중 이미지 구조**: 대다수 장비가 active/backup 이미지 슬롯 2개 제공 → 부팅 실패 시 자동 fallback
- **무중단 업그레이드 (ISSU)**: 일부 고급 장비만 지원 (대부분 가입자망 L2/OLT는 reload 필요)
- **유지보수 시간대 작업**: 가입자 영향 최소화를 위해 새벽 시간에 진행
- **OLT 업그레이드 시 ONU 영향**: PON 링크가 일시적으로 끊김

## 검색 힌트

- "펌웨어 업그레이드" "소프트웨어 업그레이드" → 본 카드
- "스위치 업그레이드 절차" → 본 카드 표준 절차 섹션
- "boot system" → 본 카드
- "TFTP 이미지 다운로드" → 본 카드
- "롤백 fallback" → 본 카드 가입자망 운영 고려사항
