---
id: concept:acl-extended
type: Concept
name_en: Extended ACL
name_ko: 확장 ACL
parent_protocol: proto:acl
scope: data-structure
aliases:
  - extended access list
  - 5-tuple ACL
defined_by: []
related:
  - proto:acl
  - concept:acl-standard
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-02.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-04.md"
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-05.md"
  - "Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-routing__sec-05.md"
documented_in:
  - "가입자망장비_manual/다산_L2"
  - "가입자망장비_manual/다산_L3"
  - "가입자망장비_manual/유비쿼스_L2"
  - "가입자망장비_manual/유비쿼스_L3"
keywords_en:
  # ACL-specific terms only. Generic tokens like "tcp"/"udp"/"port"/"protocol"
  # were removed to prevent ~28 false-positive matches across non-ACL queries.
  - extended ACL
  - access-list 100-199
  - access-list 2000-2699
  - named access-list
  - 5-tuple ACL
  - wildcard mask
  - ACL inbound
  - ACL outbound
  - established keyword
keywords_ko:
  - 확장 ACL
  - 확장 access-list
  - 5튜플 ACL
  - 와일드카드 마스크
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

Extended ACL은 5-tuple(프로토콜·출발지 IP·목적지 IP·출발지 포트·목적지 포트)로 트래픽을 필터링한다. Cisco IOS에서 번호 100~199 또는 2000~2699가 확장 ACL이며, 적용은 출발지 가까운 인터페이스에 권장된다(불필요한 트래픽을 백본 진입 전에 차단).

## Cisco 명령어 형식

```
access-list <100-199|2000-2699> {permit|deny} <protocol>
    <source> [src-wildcard] [src-operator src-port]
    <destination> [dst-wildcard] [dst-operator dst-port]
    [established] [log]
```

예:
- `access-list 110 permit tcp any host 10.0.0.1 eq 80` → 임의 → 10.0.0.1:80 TCP 허용
- `access-list 110 deny udp host 192.168.1.5 any eq 53` → 특정 호스트 DNS 차단
- `access-list 110 permit tcp any any established` → 기존 세션의 응답만 허용 (스테이트풀 시뮬레이션)

## Operator (포트 비교)

- `eq` (equal): 정확히 일치
- `gt` (greater than): 초과
- `lt` (less than): 미만
- `range`: 범위 (예: `range 1000 2000`)
- `neq`: 같지 않음

## Named ACL (권장)

번호 대신 이름을 사용해 가독성·관리성 향상:
```
ip access-list extended WEB_FILTER
 permit tcp any host 10.0.0.1 eq 80
 deny ip any any log
```

## established 키워드

TCP `established`는 SYN 없이 ACK/RST 비트가 설정된 패킷만 허용 → 외부에서 새 연결을 차단하면서 내부 발신 연결의 응답은 통과시키는 단순 스테이트풀 동작.

진짜 stateful 필터링은 CBAC, ZBF, ASA/Firewall이 담당.

## 적용 권장

출발지 가까이 적용 → 백본·다운스트림 링크의 불필요한 부하 절감.

## 검색 힌트

- "확장 ACL 번호 범위" → 본 카드 (100-199, 2000-2699)
- "5-tuple 필터링" → 본 카드 명령어 형식
- "TCP UDP 포트 차단" → 본 카드 + Operator 섹션
- "Named ACL" → 본 카드 Named ACL 섹션
- "established 키워드" → 본 카드 established 섹션
- "ACL 적용 위치 권장" → 본 카드 (출발지 가까이)
