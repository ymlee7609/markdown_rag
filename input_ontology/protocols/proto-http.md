---
id: proto:http
type: Protocol
name_en: HTTP
name_ko: 하이퍼텍스트 전송 프로토콜 (HTTP)
aliases:
  - Hypertext Transfer Protocol
  - HTTP/1.1
  - HTTP/2
  - HTTP/3
layer: L7
family: application
status: active
defined_by:
  - rfc:9110
  - rfc:9112
extends: []
related:
  - proto:tls
references:
  - rfc:2616        # HTTP/1.1 (obsoleted)
  - rfc:7230        # HTTP/1.1 Message Syntax (obsoleted by 9112)
  - rfc:9114        # HTTP/2
  - rfc:9114        # HTTP/3
taught_in: []
documented_in: []
vendors_supporting:
  - vendor:cisco
  - vendor:dasan
  - vendor:ubiquoss
keywords_en:
  - HTTP
  - HTTP/1.1
  - HTTP/2
  - HTTP/3
  - persistent connection
  - keep-alive
  - chunked encoding
  - method
  - GET
  - POST
  - PUT
  - DELETE
  - status code
  - header
  - REST
keywords_ko:
  - HTTP
  - 웹
  - 지속 연결
  - 메서드
  - 상태 코드
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

HTTP(Hypertext Transfer Protocol)는 웹의 핵심 응용 계층 프로토콜로, TCP 80(기본) 또는 TCP 443(HTTPS) 위에서 동작한다. 클라이언트-서버 요청·응답 모델. 현행 의미론(RFC 9110)과 메시지 형식(RFC 9112)으로 분리 표준화됨.

## 표준 / 정의

- **RFC 9110** — HTTP Semantics (현행 의미론, 메서드·상태 코드·헤더)
- **RFC 9111** — HTTP Caching
- **RFC 9112** — HTTP/1.1 Message Syntax
- **RFC 9113** — HTTP/2
- **RFC 9114** — HTTP/3 (QUIC)

폐기:
- RFC 2616 (HTTP/1.1, 1999)
- RFC 7230~7235 (HTTP/1.1 분할 표준, 2014)

## Persistent Connection (Keep-Alive)

HTTP/1.0 기본 단방향 요청-응답마다 TCP 연결 새로 맺음. HTTP/1.1부터 **persistent connection** 기본:
- `Connection: keep-alive` 헤더로 명시 (HTTP/1.0에서 옵션)
- HTTP/1.1: 기본이 keep-alive, 끊기 위해 `Connection: close` 명시
- 다수 요청을 같은 TCP 연결로 (pipelining 가능하나 head-of-line blocking)

## 주요 메서드와 상태 코드

| 메서드 | 의미 |
|---|---|
| GET | 자원 조회 |
| POST | 자원 생성/처리 |
| PUT | 자원 교체 |
| DELETE | 자원 삭제 |
| HEAD | GET 응답의 헤더만 |
| OPTIONS | 서버 지원 메서드 조회 (CORS preflight) |
| PATCH | 자원 부분 수정 |

상태 코드 클래스: 1xx (informational), 2xx (success), 3xx (redirect), 4xx (client error), 5xx (server error)

## 검색 힌트

- "HTTP persistent connection keep-alive" → 본 카드 Keep-Alive 섹션
- "HTTP/1.1 표준" → 본 카드 + RFC 9110/9112
- "HTTP 메서드" → 본 카드 주요 메서드 표
- "HTTP/2 HTTP/3" → 본 카드 + RFC 9113/9114
