---
id: proto:ntp
type: Protocol
name_en: NTP
name_ko: 네트워크 시간 프로토콜 (NTP)
aliases:
  - Network Time Protocol
  - NTPv4
  - NTPv3
layer: L7
family: management
status: active
defined_by:
  - rfc:5905
extends: []
related:
  - feat:clock-config
references:
  - rfc:1305     # NTPv3 (obsoleted)
  - rfc:5906     # NTP Autokey
  - rfc:5907     # NTP MIB
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-05.md"
documented_in:
  - "가입자망장비_manual/다산_L2"
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L2"
  - "가입자망장비_manual/유비쿼스_L3"
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - NTP
  - NTPv4
  - stratum
  - peer
  - server
  - client
  - broadcast
  - multicast
  - offset
  - jitter
  - poll interval
  - synchronization
  - clock
keywords_ko:
  - NTP
  - 시간 동기화
  - 시간 동기
  - 시각 동기화
  - 스트라텀
  - 시계 동기
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

NTP(Network Time Protocol)는 네트워크 노드의 시간을 표준 시각원과 동기화하는 L7 프로토콜이다. UDP 123번 포트에서 동작하며, 인터넷 환경에서 수십 밀리초 이내, LAN에서는 1ms 이내 정확도를 제공한다. 현행 표준은 RFC 5905(NTPv4, 2010). 로그 timestamp·인증서 검증·분산 시스템 정합성의 기반이다.

## 표준 / 정의

- **RFC 5905** — Network Time Protocol Version 4: Protocol and Algorithms Specification (2010)
- **RFC 5906** — NTP Autokey (보안 인증)
- **RFC 5907** — NTP MIB
- 폐기: RFC 958 → 1059 → 1119 → 1305 (NTPv3) → **5905 (NTPv4)**

## Stratum 계층

| Stratum | 의미 |
|---|---|
| 0 | 정확한 시각원 (원자시계, GPS 수신기) — 직접 동기 불가 |
| 1 | Stratum 0에 직접 연결된 1차 서버 |
| 2 | Stratum 1에서 동기화된 2차 서버 |
| ... | 최대 15까지 |
| 16 | "동기화 안 됨" 표시 |

낮은 stratum이 더 신뢰. 일반 운영망 장비는 Stratum 2~4 NTP 서버에서 동기화.

## 동작 모드

- **Server**: 다른 클라이언트에 시각 제공
- **Client**: 서버에서 시각 받음 (가장 흔함)
- **Peer (Symmetric Active)**: 양방향 동기 (대칭, 사업자 NTP 코어 망)
- **Broadcast / Multicast**: 한 서버가 다수 클라이언트에 일방향 송신

## 시간 동기 알고리즘

1. 클라이언트가 NTP 패킷에 t1(송신 시각) 기록 후 송신
2. 서버가 t2(수신), t3(송신) 기록 후 응답
3. 클라이언트가 t4(수신) 기록
4. **Offset**: ((t2-t1) + (t3-t4)) / 2  (시각차)
5. **Round-trip delay**: (t4-t1) - (t3-t2)
6. NTP는 다수 서버의 offset을 통계적으로 결합해 최적값 선택

## 벤더 구현

| Vendor | 클라이언트 설정 | 서버 모드 |
|---|---|---|
| Cisco | `ntp server 1.2.3.4` | `ntp master <stratum>` |
| Dasan | `ntp server 1.2.3.4` | `ntp master ...` |
| Ubiquoss | `ntp server 1.2.3.4` | `ntp master ...` |

## 보안

- **MD5/SHA 키 인증** (전통): 키 ID 매칭, 매뉴얼 키 분배
- **Autokey** (RFC 5906): 자동 키 교환, 구현 복잡도로 보급 저조
- **NTS** (Network Time Security, RFC 8915): TLS 기반, NTPv4 차세대 인증

## 관련 기능

- [feat:clock-config](../features/feat-clock-config.md) — 시스템 시각 설정 (NTP 자동 동기 vs 수동 `clock set`)

## 검색 힌트

- "NTP 설정" → 본 카드 + `feat:clock-config`
- "시간 동기화" → 본 카드
- "stratum 개념" → 본 카드 Stratum 계층 섹션
- "NTP 서버 인증" → 본 카드 보안 섹션
- "NTPv3 vs NTPv4" → 본 카드 표준 체인
