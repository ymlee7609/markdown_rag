# 온톨로지 M2 검증 리포트 — Top-10 Cover 측정

생성일: 2026-05-22
대상: `input_ontology/` 카드 34장 + `alias_dictionary.yaml` 시드
평가 셋: `scripts/validation_dataset.json` (100건)

---

## 결과 요약

| 카테고리 | 매칭 | 전체 | 비율 | 목표 |
|---|---|---|---|---|
| **전체** | **84** | **100** | **84%** | **80%+ ✅** |
| rfc | 25 | 30 | 83% | - |
| ccie | 28 | 30 | 93% | - |
| ko | 21 | 30 | 70% | - |
| edge | 10 | 10 | 100% | - |

M2 합격 기준(80%+) **통과**. Edge 케이스는 100% 매칭으로 핵심 토픽은 모두 cover.

---

## 카드 구성 (34장)

| 타입 | 수 | 디렉토리 |
|---|---|---|
| Protocol | 10 | `protocols/` (OSPF, BGP, STP, VLAN, DHCP, PPPoE, IGMP, ACL, IPv6, GPON) |
| Concept | 12 | `concepts/` (ospf-area, bgp-as-path, stp-root-bridge, stp-port-states, vlan-trunk, dhcp-discover, pppoe-discovery, igmp-snooping, ipv6-header, acl-standard, acl-extended, gpon-olt-onu) |
| RFC | 8 | `rfcs/` (2328, 4271, 2131, 2516, 3376, 8200, 4861, 1661) |
| Standard | 3 | `standards/` (IEEE 802.1D, 802.1Q, ITU-T G.984) |
| Feature | 1 | `features/` (dot1q-tunnel) |

`alias_dictionary.yaml`에 추가로 ~50개 ID 예약 (시드 alias만 있고 카드는 미작성).

---

## 매칭 빈도 Top 15 (분포)

| 횟수 | 카드 ID | 비고 |
|---|---|---|
| 28 | concept:acl-extended | TCP/UDP/permit/deny 토큰이 광범위하게 매칭 - **false positive 의심**, 키워드 좁히기 필요 |
| 26 | proto:bgp | 정상 |
| 11 | proto:stp | 정상 |
| 10 | rfc:4271 | 정상 |
| 7 | proto:ospf, std:ieee-802.1d | 정상 |
| 6 | rfc:2328, std:itu-t-g.984, concept:gpon-olt-onu, proto:acl | 정상 |
| 5 | proto:nat, proto:gpon, proto:vlan, std:ieee-802.1q, concept:stp-port-states | 정상 |

**경고**: `concept:acl-extended`의 28회 매칭은 keywords에 `tcp`, `udp`, `permit`, `deny`, `5-tuple` 등 일반적 토큰이 들어 있어 over-match. M3에서 `require_context_tokens` 정책으로 좁힐 것.

---

## 매칭 실패 케이스 16건 — 다음 단계 우선순위

### RFC 카테고리 (5건)

| ID | Query | 부족한 카드 |
|---|---|---|
| RFC-003 | DNS resource record types A MX CNAME | `proto:dns`, `rfc:1034`, `rfc:1035` |
| RFC-004 | HTTP persistent connections keep-alive | `proto:http`, `rfc:2616`, `rfc:7230` |
| RFC-010 | SMTP mail transaction | `proto:smtp`, `rfc:5321` |
| RFC-026 | GRE generic routing encapsulation | `proto:gre`, `rfc:2784` |
| RFC-030 | private IP address ranges RFC1918 | `rfc:1918` |

→ **응용계층 프로토콜(DNS, HTTP, SMTP)과 터널/주소 RFC**가 부재. 다음 작성 후보.

### CCIE 카테고리 (2건)

| ID | Query | 부족한 카드 |
|---|---|---|
| CCIE-022 | Frame Relay DLCI PVC LMI | `proto:frame-relay` |
| CCIE-024 | default route propagation | `concept:default-route`, `concept:route-redistribution` |

→ **WAN 프로토콜과 라우팅 운영 개념** 부족.

### KO 카테고리 (9건) — **가장 약한 영역**

| ID | Query | 부족한 카드 / 분석 |
|---|---|---|
| KO-001 | 다산 V3024V 포트 설정 방법 | `model:dasan-v3024v` DeviceModel 카드 부재 |
| KO-011 | 콘솔 포트 시리얼 케이블 | 운영 명령어 영역, Feature 카드 부재 |
| KO-012 | 전원 공급 장치 설치 | 하드웨어 운영 영역 |
| KO-016 | MAC 주소 테이블 조회 | `feat:mac-address-table` / `concept:mac-learning` |
| KO-018 | 펌웨어 업그레이드 | `feat:firmware-upgrade` |
| KO-019 | 다산 V3024VB 사양 | `model:dasan-v3024vb` |
| KO-020 | 날짜 시간 clock 설정 | `feat:clock-config`, `proto:ntp` (카드 미작성) |
| KO-026 | 포트 미러링 | `feat:port-mirroring` |
| KO-028 | 다산 V6824XG L3 사양 | `model:dasan-v6824xg` |

→ **DeviceModel 카드**와 **운영 Feature 카드**(MAC 테이블·포트 미러링·펌웨어·클록)가 핵심. 한국어 운영 매뉴얼 영역을 cover하려면 카드 종류 자체를 확장 필요.

---

## 다음 단계 (M3) 권고

검증 결과를 바탕으로 우선순위 재조정:

### A. 응용계층 RFC 카드 보강 (RFC cover 83% → 95%+)
- DNS (RFC 1034/1035), HTTP (RFC 2616/7230), SMTP (RFC 5321)
- 터널: GRE (RFC 2784), IPSec (RFC 4301)
- 주소 표준: RFC 1918 (private IP), RFC 6890 (special-use)

### B. WAN/운영 개념 카드 (CCIE cover 93% → 100%)
- `proto:frame-relay`, `concept:default-route`, `concept:route-redistribution`

### C. 한국어 운영 매뉴얼 영역 보강 (KO cover 70% → 90%+) — **가장 큰 효과**
- DeviceModel 카드 10~20장 (다산 V3024V/V3024VB/V6824XG, 유비쿼스 E61xx/P8624 등)
- 운영 Feature 카드: `feat:mac-address-table`, `feat:port-mirroring`, `feat:firmware-upgrade`, `feat:clock-config`, `feat:console-access`
- Protocol 카드 추가: `proto:ntp` (시간 동기)

### D. False positive 완화
- `concept:acl-extended`의 keywords 좁히기 — `permit`, `deny`, `tcp`, `udp` 같은 일반 토큰 제거
- `alias_dictionary.yaml`의 `require_context_tokens` 정책 본격 적용 (extract_onto_candidates.py에서)

### E. M3 LLM 자동 확장 시작
- Stage 1 결정론적 추출 스크립트(`scripts/extract_onto_candidates.py`) 작성
- 전체 청크에 onto_*_ids 후보 부여
- relations.jsonl 자동 생성

---

## 산출물 인덱스

| 파일 | 역할 |
|---|---|
| `input_ontology/` 34장 md | 카드 본체 |
| `input_ontology/schema/*.yaml` | 스키마 + alias 사전 |
| `data/ontology/index.json` | 34 entity ID → 파일 경로 매핑 |
| `data/ontology/alias_index.json` | 266 alias → canonical ID 역인덱스 |
| 본 리포트 | M2 acceptance 증빙 |

---

## 결론

M2 acceptance 달성. 다음 단계로 진행 가능. 단, **KO 카테고리(가입자망 운영 영역) cover를 80%+로 끌어올리려면 DeviceModel/Feature 카드 추가**가 필요하며, 이는 단순 Protocol 확장보다 효과가 크다.
