---
id: proto:smtp
type: Protocol
name_en: SMTP
name_ko: 단순 메일 전송 프로토콜 (SMTP)
aliases:
  - Simple Mail Transfer Protocol
  - ESMTP
layer: L7
family: application
status: active
defined_by:
  - rfc:5321
extends: []
related: []
references:
  - rfc:821         # 원본 SMTP (obsoleted)
  - rfc:2821        # 이전 SMTP (obsoleted by 5321)
  - rfc:5322        # Internet Message Format
taught_in: []
documented_in: []
vendors_supporting: []
keywords_en:
  - SMTP
  - ESMTP
  - MAIL FROM
  - RCPT TO
  - DATA
  - HELO
  - EHLO
  - QUIT
  - TCP 25
  - TCP 587
  - TCP 465
  - STARTTLS
  - SPF
  - DKIM
  - DMARC
keywords_ko:
  - SMTP
  - 메일
  - 메일 전송
  - 발신
confidence: 1.0
source: human
last_reviewed: 2026-05-22
---

## 개요

SMTP(Simple Mail Transfer Protocol)는 인터넷 이메일 전송 표준 프로토콜이다. TCP 25(server-to-server), 587(submission, MSA), 465(implicit TLS)에서 동작. 현행 RFC 5321(2008)이 정식 사양이며 ESMTP(Extended SMTP) 확장을 포함한다.

## 표준 / 정의

- **RFC 5321** — Simple Mail Transfer Protocol (현행)
- **RFC 5322** — Internet Message Format (메일 본문/헤더 형식)
- 폐기: RFC 821 (1982) → RFC 2821 (2001) → **RFC 5321** (2008)
- 인증/보안: SPF (RFC 7208), DKIM (RFC 6376), DMARC (RFC 7489)

## 핵심 트랜잭션

SMTP 메일 송신 절차 (한 메일 한 트랜잭션):

```
S: 220 mail.example.com ESMTP ready
C: EHLO client.example.org
S: 250-mail.example.com Hello
   250 STARTTLS
C: STARTTLS
... (TLS handshake)
C: MAIL FROM:<sender@example.org>
S: 250 OK
C: RCPT TO:<recipient@example.com>
S: 250 OK
C: DATA
S: 354 Start mail input; end with <CRLF>.<CRLF>
C: From: ...
   To: ...
   Subject: ...
   <본문>
   .
S: 250 OK queued as ABCD1234
C: QUIT
S: 221 Bye
```

## 주요 ESMTP 확장

- `STARTTLS` — TLS 업그레이드 (RFC 3207)
- `AUTH` — SASL 인증 (RFC 4954)
- `8BITMIME` — 8비트 본문
- `PIPELINING` — 다수 명령 한 번에
- `SIZE` — 최대 메시지 크기 광고

## 관련 프로토콜

- POP3 (RFC 1939): 메일함 가져오기 (단순)
- IMAP (RFC 3501): 메일함 원격 관리 (현대 메일 클라이언트 표준)

## 검색 힌트

- "SMTP 트랜잭션 절차" → 본 카드 핵심 트랜잭션
- "MAIL FROM RCPT TO" → 본 카드
- "SMTP 포트 25 587 465" → 본 카드 개요
- "ESMTP" "STARTTLS" → 본 카드
- "SPF DKIM DMARC" → 본 카드 표준 섹션
