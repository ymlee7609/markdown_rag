---
id: model:ubiquoss-u9532h
type: DeviceModel
vendor: vendor:ubiquoss
name: U9532H
role: OLT
manual_paths:
  - "가입자망장비_manual/유비쿼스_OLT/U9532H_HW_Installation Guide.md"
  - "가입자망장비_manual/유비쿼스_OLT/U95xxH_SW_User Guide"
supports_features:
  - feat:dot1q-tunnel
  - feat:mac-address-table
  - feat:port-mirroring
  - feat:console-access
  - feat:firmware-upgrade
keywords_en:
  # Model-specific identifiers only.
  - U9532H
  - U95xxH
  - 유비쿼스 U9532H
keywords_ko:
  - U9532H
  - U95xxH
  - 유비쿼스 U9532H
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

유비쿼스 U9532H는 32-포트 GPON OLT다. U95xxH 시리즈의 일원으로 SW 매뉴얼은 시리즈 공통(`U95xxH_SW_User Guide`)을 공유한다. 한 OLT가 최대 32개 PON 분기를 종단하며, 광 분기기(splitter) 1:64 또는 1:128 비율로 가입자 ONU에 연결된다.

## 매뉴얼 위치

- **HW 설치**: `유비쿼스_OLT/U9532H_HW_Installation Guide.md` (단일 파일)
- **SW 사용자 가이드 (U95xxH 시리즈 공유)**: `유비쿼스_OLT/U95xxH_SW_User Guide/` (다수 섹션)

## 주요 사양

- **PON 포트**: 32× GPON SFP (ITU-T G.984)
- **업링크**: 10GbE SFP+ (모델 옵션에 따라 1G 혼합)
- **OMCI**: ONU 원격 관리·구성
- **DBA**: 동적 대역 할당
- **IPTV**: IGMP snooping/proxy, MVR
- **가입자 인증**: PPPoE intermediate agent (PPPoE+), RADIUS 연동
- **VLAN**: S-VLAN/C-VLAN (Q-in-Q)

## 검색 힌트

- "U9532H" → 본 카드
- "유비쿼스 OLT 32포트" → 본 카드
- "유비쿼스 OLT 업링크" → 본 카드 주요 사양
- "U95xxH 시리즈" → 본 카드 (SW 매뉴얼 공유)
