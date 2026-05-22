---
id: model:dasan-v8500
type: DeviceModel
vendor: vendor:dasan
name: V8500 / V8500M
role: OLT
os_version: "UMN NOS 5.21 (V8500), NOS 6.06 (V8500M)"
manual_paths:
  - "가입자망장비_manual/다산_OLT/[V8500M]_UMN_NOS6.06_KO_190822_V1.0"
  - "가입자망장비_manual/다산_OLT/_V8500__UMN_NOS5.21_KO_150304_V2"
supports_features:
  - feat:dot1q-tunnel
  - feat:mac-address-table
  - feat:port-mirroring
  - feat:console-access
  - feat:firmware-upgrade
keywords_en:
  # Model-specific identifiers only.
  - V8500
  - V8500M
  - 다산 V8500
  - 다산 V8500M
keywords_ko:
  - V8500
  - V8500M
  - 다산 V8500
  - 다산 V8500M
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

다산네트웍스 V8500/V8500M은 섀시형 GPON OLT(Optical Line Terminal)이다. 다수 PON 라인카드를 수용해 수백~수천 가입자(ONU)를 종단한다. V8500이 초기 모델, V8500M이 후속 NOS 6.x 모델. 한국 통신사업자 FTTH 가입자망의 국사 측 핵심 장비.

## 매뉴얼 위치

- `input_optimized/가입자망장비_manual/다산_OLT/[V8500M]_UMN_NOS6.06_KO_190822_V1.0/` — V8500M (NOS 6.06, 2019-08)
- `input_optimized/가입자망장비_manual/다산_OLT/_V8500__UMN_NOS5.21_KO_150304_V2/` — V8500 (NOS 5.21, 2015-03)

## 주요 사양 (요약)

- 섀시형, 다수 PON 라인카드 슬롯
- 업링크: 10G/40G/100G 이더넷 (모델/카드별)
- PON 포트: GPON 표준 (ITU-T G.984)
- OMCI로 ONU 원격 관리
- T-CONT / GEM port / DBA 프로파일
- IPTV: IGMP snooping/proxy, MVR
- 가입자 인증: PPPoE intermediate agent, RADIUS 연동

## 지원 프로토콜

- `proto:gpon` (G.984)
- `proto:vlan`, `feat:dot1q-tunnel` (S-VLAN/C-VLAN)
- `proto:dhcp` (DHCP snooping, Option 82)
- `proto:igmp` (IPTV 멀티캐스트)
- `proto:pppoe` (가입자 인증)

## 검색 힌트

- "V8500" "V8500M" → 본 카드
- "다산 OLT" → 본 카드 + `vendor:dasan`
- "다산 OLT PON 포트" → 본 카드 + `proto:gpon`
- "FTTH 국사 장비" → 본 카드 + `proto:gpon`
