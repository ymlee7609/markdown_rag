---
id: feat:port-mirroring
type: Feature
name_en: Port Mirroring (SPAN)
name_ko: 포트 미러링
aliases:
  - SPAN
  - port mirror
  - traffic monitoring
  - monitor session
  - RSPAN
  - ERSPAN
implements: []
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
  - port mirroring
  - SPAN
  - source port
  - destination port
  - monitor session
  - mirror
  - traffic capture
  - sniffer
  - RSPAN
keywords_ko:
  - 포트 미러링
  - 미러링
  - 모니터링
  - 트래픽 캡처
  - 패킷 분석
  - 스니퍼
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

Port Mirroring(Cisco SPAN — Switched Port Analyzer)은 특정 포트(또는 VLAN)의 입출력 트래픽을 다른 포트로 복제해 보내는 기능이다. 패킷 분석기(Wireshark, IDS, NPM)에 연결해 트래픽을 캡처·분석할 때 사용한다. 운영에 영향 없이 트래픽을 관찰할 수 있는 표준 진단 도구.

## 종류

| 종류 | 범위 | 용도 |
|---|---|---|
| **SPAN** (Local) | 같은 스위치 | 일반 패킷 캡처 |
| **RSPAN** (Remote) | 다른 스위치 (VLAN 통해) | 원격 캡처 |
| **ERSPAN** (Encapsulated Remote) | 다른 IP 네트워크 (GRE 캡슐화) | L3 원격 캡처 |
| **VSPAN** | VLAN 전체 | VLAN 단위 모니터링 |

## 핵심 개념

- **Source port (모니터링 대상)**: 트래픽이 발생하는 포트, 다수 가능
- **Destination port (모니터 포트)**: 복제된 트래픽이 나가는 포트, 일반 통신 불가
- **방향**: ingress(rx) / egress(tx) / both 선택 가능

## 주요 명령어 (벤더별)

| Vendor | 명령어 |
|---|---|
| Cisco | `monitor session 1 source interface gi0/1`, `monitor session 1 destination interface gi0/2` |
| Dasan | `port-mirror enable`, `port-mirror source ...`, `port-mirror destination ...` |
| Ubiquoss | `mirror session N source ...`, `mirror session N destination ...` |

> 정확한 syntax는 모델별 매뉴얼 참고.

## 운영 주의사항

- 미러 destination 포트는 일반 트래픽 비차단/송수신 불가
- Source 트래픽이 destination 포트의 대역폭(보통 1G)을 초과하면 패킷 손실
- 다수 source를 단일 destination에 미러링하면 과부하 위험 → 트래픽 샘플링 또는 분할 권장

## 검색 힌트

- "포트 미러링" → 본 카드
- "SPAN 세션" → 본 카드
- "트래픽 캡처 설정" → 본 카드 + 벤더 매뉴얼
- "Wireshark 연결" → 본 카드 핵심 개념 섹션
- "monitor session" → 본 카드 명령어
