---
id: proto:frame-relay
type: Protocol
name_en: Frame Relay
name_ko: 프레임 릴레이
aliases:
  - Frame Relay
  - FR
layer: L2
family: wan
status: legacy           # 거의 폐기됨, MPLS/Metro Ethernet으로 대체
defined_by: []           # ITU-T Q.922, ANSI T1.618 (별도 Standard 카드는 생략)
extends: []
related: []
references: []
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-03.md"
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-01.md"
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-04.md"
  - "Cisco_CCIE/CCIE_Vol1/03_part-i-lan-switching__sec-11.md"
  - "Cisco_CCIE/CCIE_Vol2/05_part-iii-wide-area-networks.md"
documented_in: []
vendors_supporting:
  - vendor:cisco
keywords_en:
  - Frame Relay
  - DLCI
  - PVC
  - SVC
  - LMI
  - data link connection identifier
  - permanent virtual circuit
  - local management interface
  - inverse ARP
  - CIR
  - committed information rate
  - BECN
  - FECN
  - DE
keywords_ko:
  - 프레임 릴레이
  - DLCI
  - PVC
  - LMI
  - 가상회선
  - WAN
  - 광역망
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

Frame Relay는 1990년대~2000년대 통신사업자가 제공한 패킷 교환 WAN 기술로, X.25를 대체했다. 가입자는 단일 물리 회선(보통 T1/E1) 위에 **여러 PVC(Permanent Virtual Circuit)**을 가질 수 있고, 각 PVC는 DLCI로 식별된다. 현재는 MPLS L3VPN, Metro Ethernet, IP VPN으로 대부분 대체되어 신규 도입은 거의 없지만 CCIE 시험 범위와 레거시 운영 환경에서는 여전히 다룬다.

## 표준

- ITU-T Q.922 (Annex A)
- ANSI T1.618
- Frame Relay Forum (FRF) Implementation Agreements (FRF.1~FRF.20+)

## 핵심 개념

| 용어 | 의미 |
|---|---|
| **DLCI** (Data Link Connection Identifier) | 각 PVC 식별자 (로컬 의미, 10-1007 사용자 범위) |
| **PVC** (Permanent Virtual Circuit) | 사전 설정된 영구 가상 회선 (가장 흔함) |
| **SVC** (Switched Virtual Circuit) | 호 단위로 설정되는 가상 회선 (잘 쓰지 않음) |
| **LMI** (Local Management Interface) | DTE-DCE 상태 관리 시그널링 (Cisco/ANSI/Q933a 3종) |
| **Inverse ARP** | DLCI ↔ 원격 IP 자동 매핑 |
| **CIR** (Committed Information Rate) | 보장 대역폭 |
| **BECN/FECN** | 혼잡 통지 비트 (Backward/Forward Explicit Congestion Notification) |
| **DE** (Discard Eligible) | 폐기 우선 표시 비트 |

## Cisco 설정 (요약)

```
interface Serial0/0
 encapsulation frame-relay [cisco|ietf]
 frame-relay lmi-type {cisco|ansi|q933a}
 frame-relay interface-dlci 100
!
interface Serial0/0.1 point-to-point
 ip address 10.0.0.1 255.255.255.252
 frame-relay interface-dlci 100
!
interface Serial0/0.2 multipoint
 ip address 10.0.1.1 255.255.255.0
 frame-relay map ip 10.0.1.2 200 broadcast
```

## 검색 힌트

- "Frame Relay DLCI" → 본 카드
- "PVC SVC 차이" → 본 카드 핵심 개념 표
- "LMI 종류" → 본 카드 (cisco / ansi / q933a)
- "Inverse ARP" → 본 카드
- "CIR 대역 보장" → 본 카드
