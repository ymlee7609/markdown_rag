---
id: vendor:dasan
type: Vendor
name_en: Dasan Networks
name_ko: 다산네트웍스
country: KR
website: "https://www.dasannetworks.com"
corpus_path_prefix: "가입자망장비_manual/다산_"
product_lines:
  - L2
  - L3
  - OLT
aliases:
  - Dasan
  - DSN
  - 다산
  - 다산네트웍스
keywords_ko:
  - 다산
  - 다산네트웍스
keywords_en:
  - Dasan
  - Dasan Networks
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

다산네트웍스(Dasan Networks)는 한국의 통신·가입자망 장비 제조사로, 국내 통신사업자(KT/SK브로드밴드/LG U+) FTTH·xDSL 가입자망에 L2 스위치, L3 스위치, GPON OLT를 공급한다. 자체 NOS(`UMNnos`)를 사용한다.

## 코퍼스 매핑

`input_optimized/가입자망장비_manual/`에서 다음 디렉토리로 분류:

| 제품군 | 디렉토리 | 대표 모델 |
|---|---|---|
| L2 스위치 | `다산_L2/` | V2708M, V3024V, V3024VB, V27xxGB_LGU, V29xxGB |
| L3 스위치 | `다산_L3/` | V5524XG, V6824XG, V6848XG |
| GPON OLT | `다산_OLT/` | V8500, V8500M, V5724G-10G_LGU |

## 매뉴얼 파일명 규칙

`[모델명]_UMNnos<버전>_KO_<날짜>_V<버전>__sec-NN.md` 형식.
예: `[V3024V]_UMNnos1.01_KO_190926_V1.0__sec-03.md`

- 모델명은 대괄호로 둘러싸일 수 있음
- `UMN` = Universal Multi-service Network OS
- `KO` = 한국어판
- `__sec-NN` = 섹션 분할 인덱스 (긴 매뉴얼이 청크로 분할된 경우)

## DeviceModel 카드

이 벤더의 모델 카드:
- [model:dasan-v3024v](../devices/model-dasan-v3024v.md) — L2 24포트 GbE
- [model:dasan-v3024vb](../devices/model-dasan-v3024vb.md) — L2 배터리 내장형
- [model:dasan-v6824xg](../devices/model-dasan-v6824xg.md) — L3 10G 24포트
- [model:dasan-v8500](../devices/model-dasan-v8500.md) — GPON OLT

## 명령어 체계 특징

- Linux 기반 NOS, `configure terminal` / `interface` / `exit` 계층 구조
- VLAN: `bridge vlan add`
- L3: `router ospf`, `router bgp` (Cisco 유사)
- OLT: `gpon`, `onu`, `tcont`, `gem-port`, `dba-profile`

## 검색 힌트

- "다산 매뉴얼" → 본 카드 + 코퍼스 매핑 섹션
- "다산 V*** 모델" → 본 카드 + 해당 DeviceModel 카드
- "UMNnos 명령어" → 본 카드 명령어 체계 특징
