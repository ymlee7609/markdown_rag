---
id: vendor:ubiquoss
type: Vendor
name_en: Ubiquoss
name_ko: 유비쿼스
country: KR
website: "https://www.ubiquoss.com"
corpus_path_prefix: "가입자망장비_manual/유비쿼스_"
product_lines:
  - L2
  - L3
  - OLT
aliases:
  - Ubiquoss
  - Ubiquoss Inc
  - 유비쿼스
keywords_ko:
  - 유비쿼스
keywords_en:
  - Ubiquoss
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

유비쿼스(Ubiquoss)는 한국의 통신·가입자망 장비 제조사로, 다산네트웍스와 함께 국내 통신사업자 가입자망의 양대 공급사다. L2 스위치(E5xxx 시리즈), L3 스위치(E6xxx, P8xxx), GPON OLT(U9xxx 시리즈)를 공급한다.

## 코퍼스 매핑

`input_optimized/가입자망장비_manual/`에서:

| 제품군 | 디렉토리 | 대표 모델 |
|---|---|---|
| L2 스위치 | `유비쿼스_L2/` | E5708C, E5708R, E57xxRC, E5924L |
| L3 스위치 | `유비쿼스_L3/` | E61xx, P8624 |
| GPON OLT | `유비쿼스_OLT/` | U9024A-10G, U9500H, U9532H, U95xxH |

## 매뉴얼 파일명 규칙

대표 패턴:
- `<모델명>_HW_Installation Guide.md` — 하드웨어 설치 가이드
- `<모델명>_SW_User Guide__sec-NN.md` — 소프트웨어 사용자 가이드 (긴 매뉴얼은 sec 분할)

예:
- `E5708R_HW_Installation Guide.md`
- `E57xxRC_SW_User Guide__sec-04.md`
- `U95xxH_SW_User Guide/...`

## DeviceModel 카드

이 벤더의 모델 카드:
- [model:ubiquoss-e5708r](../devices/model-ubiquoss-e5708r.md) — L2 8포트 GbE
- [model:ubiquoss-e5924l](../devices/model-ubiquoss-e5924l.md) — L2 배터리 내장형
- [model:ubiquoss-u9532h](../devices/model-ubiquoss-u9532h.md) — GPON OLT
- [model:ubiquoss-p8624](../devices/model-ubiquoss-p8624.md) — L3 스위치

## 명령어 체계 특징

- Cisco IOS 유사 명령어 체계 (CLI parser 호환)
- `configure terminal`, `interface`, `vlan` 계층
- L3: `router ospf`, `router bgp`
- OLT: `gpon`, `onu`, `tcont profile`, `gem profile`

## 검색 힌트

- "유비쿼스 매뉴얼" → 본 카드 + 코퍼스 매핑
- "유비쿼스 E***/U*** 모델" → 본 카드 + DeviceModel 카드
- "유비쿼스 OLT 설정" → 본 카드 + `유비쿼스_OLT/` 매뉴얼
