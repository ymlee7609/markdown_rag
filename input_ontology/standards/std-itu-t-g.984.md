---
id: std:itu-t-g.984
type: Standard
sdo: itu-t
doc_id: "ITU-T G.984"
title: "Gigabit-capable Passive Optical Networks (GPON)"
status: active
year: 2008
defines:
  - proto:gpon
  - concept:gpon-olt-onu
  - concept:gpon-tcont
keywords_en:
  - GPON
  - G.984
  - Passive Optical Network
  - OLT
  - ONU
  - ONT
  - T-CONT
  - GEM
  - upstream
  - downstream
  - 2.488 Gbps
  - 1.244 Gbps
keywords_ko:
  - GPON
  - 광 가입자망
  - 광망
  - 광 회선
  - 가입자망
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

ITU-T G.984는 GPON(Gigabit-capable Passive Optical Network)의 표준이다. 한 OLT(Optical Line Terminal)가 광 분기기(passive splitter)를 통해 다수의 ONU/ONT(Optical Network Unit/Terminal)와 점-다점(P2MP) 광 가입자망을 구성한다. 하향(downstream) 2.488 Gbps, 상향(upstream) 1.244 Gbps가 표준이며, 한국 FTTH 가입자망의 핵심 기술이다.

## 정의 대상

- **`proto:gpon`** — GPON 프로토콜
- **`concept:gpon-olt-onu`** — OLT-ONU 구조, P2MP 토폴로지
- **`concept:gpon-tcont`** — T-CONT (Transmission Container), 대역 할당 단위

## 표준 family (G.984 시리즈)

- G.984.1 — General characteristics
- G.984.2 — Physical Media Dependent (PMD) layer
- G.984.3 — Transmission Convergence (TC) layer
- G.984.4 — ONT Management and Control Interface (OMCI)
- G.984.5 — Enhancement band
- G.984.6 — Reach extension
- G.984.7 — Long reach

## 후속 표준

- **ITU-T G.987** — XG-PON (10G GPON 하향)
- **ITU-T G.989** — NG-PON2 (40G TWDM-PON)
- **ITU-T G.9807** — XGS-PON (10G 대칭)

## 벤더 구현

- 다산 OLT — `가입자망장비_manual/다산_OLT/`
- 유비쿼스 OLT — `가입자망장비_manual/유비쿼스_OLT/`

## 검색 힌트

- "GPON 표준" → 본 카드
- "OLT와 ONU 차이" → 본 카드 + `concept:gpon-olt-onu`
- "T-CONT 대역 할당" → 본 카드 + `concept:gpon-tcont`
- "FTTH 가입자망" → 본 카드 + 다산/유비쿼스 OLT 매뉴얼
