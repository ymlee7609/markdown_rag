---
id: feat:mac-address-table
type: Feature
name_en: MAC Address Table
name_ko: MAC 주소 테이블
aliases:
  - CAM table
  - MAC table
  - bridge table
  - forwarding table
  - L2 forwarding database
implements:
  - concept:mac-learning
configures: []
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
  - MAC address table
  - CAM table
  - bridge table
  - show mac address-table
  - aging
  - static MAC
  - MAC learning
keywords_ko:
  - MAC 주소 테이블
  - MAC 테이블
  - MAC 주소
  - MAC 학습
  - 조회
  - 확인
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

MAC Address Table(또는 CAM Table, Forwarding Database)은 L2 스위치가 어느 포트에 어떤 MAC 주소의 호스트가 있는지 기록하는 테이블이다. 들어온 프레임의 출발지 MAC을 보고 학습(learning)하며, 목적지 MAC을 테이블에서 찾아 해당 포트로만 포워딩(forwarding)한다. 못 찾으면 같은 VLAN의 모든 포트로 플러딩(flooding).

## 구성 요소

| 필드 | 의미 |
|---|---|
| VLAN ID | 학습된 VLAN |
| MAC Address | 호스트 MAC |
| Type | dynamic (학습) / static (수동 등록) / system |
| Port | 학습된 포트 |
| Age | 마지막 학습 시각으로부터 경과 시간 |

## 주요 명령어 (벤더별)

| Vendor | 조회 | 정적 등록 | 초기화 |
|---|---|---|---|
| Cisco | `show mac address-table` | `mac address-table static H.H.H vlan N interface F0/1` | `clear mac address-table dynamic` |
| Dasan | `show mac-address-table`, `show mac` | `mac-address-table static ...` | `clear mac-address-table` |
| Ubiquoss | `show mac-address-table` | `mac-address-table static ...` | `clear mac-address-table` |

## Aging Time

기본 300초(5분), 마지막 프레임 수신 후 이 시간이 지나면 dynamic 엔트리 삭제. 변경 명령:
- Cisco: `mac address-table aging-time 600`
- 다산/유비쿼스: `mac-address-table aging-time 600`

## 관련 운영 이슈

- **MAC flapping**: 같은 MAC이 짧은 시간에 다른 포트에서 학습 → 루프 또는 듀얼 호밍 의심
- **Table overflow**: 보안 공격(MAC flooding)으로 테이블이 가득 차면 모든 트래픽 플러딩 → `feat:port-security`로 방어
- **Static MAC**: 변하지 않는 서버·게이트웨이 MAC을 정적 등록해 안정성 향상

## 검색 힌트

- "MAC 주소 테이블 조회" → 본 카드 명령어 섹션
- "MAC 학습" → 본 카드 + `concept:mac-learning`
- "show mac address-table" → 본 카드
- "CAM table" → 본 카드
- "MAC flapping" → 본 카드 운영 이슈
