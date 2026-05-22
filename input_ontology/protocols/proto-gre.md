---
id: proto:gre
type: Protocol
name_en: GRE
name_ko: GRE (Generic Routing Encapsulation)
aliases:
  - Generic Routing Encapsulation
  - GREv0
layer: L3
family: tunnel
status: active
defined_by:
  - rfc:2784
extends: []
related: []
references:
  - rfc:1701          # Original GRE (obsoleted)
  - rfc:1702          # GRE over IPv4 (obsoleted)
  - rfc:2890          # Key and Sequence Number Extensions
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-12.md"
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-22.md"
  - "Cisco_CCIE/CCIE_Vol1/08_cd-only__sec-07.md"
documented_in: []
vendors_supporting:
  - vendor:cisco
keywords_en:
  - GRE
  - Generic Routing Encapsulation
  - tunnel
  - tunnel interface
  - tunnel mode gre
  - protocol type 47
  - GRE header
  - keepalive
  - tunnel source
  - tunnel destination
  - IP-in-IP
  - mGRE
  - DMVPN
keywords_ko:
  - GRE
  - 터널
  - 터널 인터페이스
  - 캡슐화
  - VPN 터널
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

GRE(Generic Routing Encapsulation)는 임의의 L3 페이로드를 IP 패킷으로 캡슐화해 터널을 만드는 프로토콜이다. IP 프로토콜 번호 47로 식별되며, IPv4/IPv6/멀티캐스트/라우팅 프로토콜 트래픽 등 다양한 페이로드를 동일 방식으로 전달할 수 있다. site-to-site VPN, 멀티캐스트 over unicast, DMVPN 기반 등에 사용된다.

## 표준 / 정의

- **RFC 2784** — Generic Routing Encapsulation (GRE), 2000-03 (현행)
- 이전: RFC 1701, RFC 1702 (폐기)
- 확장: **RFC 2890** — Key and Sequence Number Extensions

## GRE 헤더 (기본 4바이트)

| 필드 | 크기 | 의미 |
|---|---|---|
| C bit | 1 | Checksum 존재 여부 |
| Flags | 12 | 예약/확장 비트 |
| Version | 3 | 0 = 표준, 1 = PPTP |
| Protocol Type | 16 | 페이로드 타입 (예: 0x0800 IPv4, 0x86DD IPv6) |

확장 시 Checksum/Key/Sequence Number 필드 추가 가능 (RFC 2890).

## Cisco 설정 (point-to-point)

```
interface Tunnel0
 ip address 172.16.0.1 255.255.255.252
 tunnel source GigabitEthernet0/0
 tunnel destination 198.51.100.2
 tunnel mode gre ip          ! 기본값, 명시 생략 가능
 keepalive 10 3              ! 10초 간격, 3회 실패 시 down
```

## 주요 활용

- **Site-to-Site VPN**: GRE + IPSec 결합 (IPSec만으로는 멀티캐스트 못 실음)
- **mGRE** (multipoint GRE): 단일 터널 인터페이스로 다수 원격 endpoint와 통신
- **DMVPN** (Dynamic Multipoint VPN): mGRE + NHRP + IPSec 결합
- **IGP over GRE**: OSPF/EIGRP 등 IGP 인접 관계 멀티캐스트 hello를 터널 통해 전달

## 한계

- 본질적으로 비암호화 (보안 필요 시 IPSec과 결합)
- 추가 헤더 오버헤드 24바이트 (GRE 4B + IP 20B), MTU/MSS 조정 필요
- 터널 endpoint 단일 장애 시 단절 (다중 경로 보호는 별도)

## 검색 힌트

- "GRE 터널 설정" → 본 카드
- "tunnel source destination" → 본 카드 Cisco 설정
- "GRE keepalive" → 본 카드 Cisco 설정
- "IP protocol 47" → 본 카드
- "DMVPN mGRE" → 본 카드 주요 활용 섹션
- "GRE + IPSec" → 본 카드 주요 활용
