---
id: model:dasan-v3024v
type: DeviceModel
vendor: vendor:dasan
name: V3024V
role: L2
os_version: "UMNnos 1.01"
manual_paths:
  - "가입자망장비_manual/다산_L2/_V3024V__UMNnos1.01_KO_190926_V1.0__sec-01.md"
  - "가입자망장비_manual/다산_L2/_V3024V__UMNnos1.01_KO_190926_V1.0__sec-02.md"
  - "가입자망장비_manual/다산_L2/_V3024V__UMNnos1.01_KO_190926_V1.0__sec-03.md"
  - "가입자망장비_manual/다산_L2/_V3024V__UMNnos1.01_KO_190926_V1.0__sec-04.md"
  - "가입자망장비_manual/다산_L2/_V3024V__UMNnos1.01_KO_190926_V1.0__sec-05.md"
  - "가입자망장비_manual/다산_L2/_V3024V__UMNnos1.01_KO_190926_V1.0__sec-06.md"
  - "가입자망장비_manual/다산_L2/_V3024V__UMNnos1.01_KO_190926_V1.0__sec-07.md"
  - "가입자망장비_manual/다산_L2/_V3024V__UMNnos1.01_KO_190926_V1.0__sec-08.md"
supports_features:
  - feat:dot1q-tunnel
  - feat:port-security
  - feat:storm-control
  - feat:mac-address-table
  - feat:port-mirroring
  - feat:console-access
keywords_en:
  # Model-specific identifiers only.
  - V3024V
  - 다산 V3024V
  - UMNnos 1.01
keywords_ko:
  - V3024V
  - 다산 V3024V
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

다산네트웍스 V3024V는 가입자망용 L2 이더넷 스위치다. 24개 GbE 포트와 업링크 SFP 포트를 제공하며, NOS는 UMNnos 1.01을 사용한다. 한국 통신사업자(KT/SK/LGU+) FTTH 가입자 분배 구간에서 흔히 사용된다.

## 매뉴얼 위치

`input_optimized/가입자망장비_manual/다산_L2/_V3024V__UMNnos1.01_KO_190926_V1.0__sec-*.md` (8개 섹션 분할)

- sec-01 ~ 02: 하드웨어 사양·설치
- sec-03 ~ 05: CLI 기본·시스템 관리
- sec-06 ~ 08: VLAN·STP·포트 보안·QoS·운영

## 지원 기능

L2 스위치 표준 기능:
- VLAN, 802.1Q tagging, Q-in-Q (dot1q-tunnel)
- STP/RSTP/MSTP
- LACP (Link Aggregation)
- Port-security, Storm-control
- DHCP snooping, IGMP snooping
- MAC address table 학습·조회
- Port mirroring (트래픽 모니터링)
- SNMP, Syslog, NTP

## 검색 힌트

- "다산 V3024V" → 본 카드
- "V3024V 포트 설정" → 본 카드 + 매뉴얼 sec-03 이상
- "다산 L2 24포트" → 본 카드
- "UMNnos 1.01" → 본 카드 + `vendor:dasan`
