---
id: concept:ospf-area
type: Concept
name_en: OSPF Area
name_ko: OSPF 영역
parent_protocol: proto:ospf
scope: state
aliases:
  - area
  - backbone area
  - stub area
  - NSSA
  - totally stubby
defined_by:
  - rfc:2328
related:
  - proto:ospf
  - concept:ospf-lsa
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-04.md"
keywords_en:
  - area
  - backbone
  - ABR
  - ASBR
  - stub
  - totally stubby
  - NSSA
  - area 0
keywords_ko:
  - 영역
  - 백본
  - 스텁
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

OSPF Area는 OSPF 네트워크를 LSDB(Link-State Database) 단위로 분할하는 단위다. 모든 영역은 backbone area(area 0)에 연결되어야 하며, ABR(Area Border Router)이 영역 간 라우팅 정보를 요약·전달한다. 영역 분할은 LSA flooding 범위를 줄여 라우터 부담과 SPF 계산 비용을 낮춘다.

## 영역 유형

| 유형 | 특징 | 허용 LSA |
|---|---|---|
| Backbone (Area 0) | 모든 영역의 중심 | Type 1~5 |
| Standard | 일반 영역 | Type 1~5 |
| Stub | external LSA 차단 | Type 1~3, default route |
| Totally Stubby (Cisco 독점) | inter-area LSA도 차단 | Type 1~2, default route |
| NSSA (RFC 3101) | external LSA를 Type 7로 변환해 진입 | Type 1~3, 7 |
| Totally NSSA | NSSA + inter-area 차단 | Type 1~2, 7, default |

## 라우터 역할 (영역 관점)

- **ABR** (Area Border Router): 둘 이상 영역에 속함
- **ASBR** (Autonomous System Boundary Router): 다른 라우팅 도메인과 redistribute
- **Internal Router**: 단일 영역에만 속함
- **Backbone Router**: area 0에 인터페이스가 있음

## 검색 힌트

- "OSPF area 종류" → 본 카드 영역 유형 표
- "stub area" → 본 카드 (외부 LSA 차단)
- "ABR ASBR 차이" → 본 카드 라우터 역할 섹션
- "area 0 backbone" → 본 카드
