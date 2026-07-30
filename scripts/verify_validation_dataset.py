#!/usr/bin/env python3
"""검증 데이터셋의 근거와 부재 주장을 코퍼스에 대해 재검증한다.

생성기를 신뢰하지 않고 독립적으로 다시 확인한다:
  1) 구조    - ID 중복, 질의 중복, 벤더 x 유형 커버리지
  2) 근거    - 파일 실존, 행 범위, 인용 원문이 실제 그 행과 일치
  3) 귀속    - expected_path_contains 가 근거 파일을 실제로 가리킴
  4) 키워드  - expected_keywords 가 근거 파일 안에 실제로 존재
  5) 부재    - 부정 케이스의 "0건" 주장을 실제 스캔으로 재확인

사용법:
    python3 scripts/verify_validation_dataset.py [데이터셋.json]
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "input_optimized/가입자망장비_manual"
VENDORS = ["다산_L2", "다산_L3", "다산_OLT", "유비쿼스_L2", "유비쿼스_L3", "유비쿼스_OLT"]
CATS = ["spec_value", "command_syntax", "diagnostics", "negative"]

_cache: dict[str, list[str]] = {}


def lines_of(rel: str) -> list[str] | None:
    if rel not in _cache:
        f = CORPUS / rel
        if not f.exists():
            return None
        _cache[rel] = f.read_text(encoding="utf-8", errors="replace").splitlines()
    return _cache[rel]


def norm(s: str) -> str:
    """비교용 정규화: 마크다운 장식/공백 제거."""
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"<br\s*/?>", "", s)
    for ch in "*`_|- ":
        s = s.replace(ch, "")
    return s.lower()


def scan_count(token: str, scope: list[str]) -> int:
    low = token.lower()
    n = 0
    for vendor in scope:
        for f in (CORPUS / vendor).rglob("*.md"):
            rel = f.relative_to(CORPUS).as_posix()
            for line in lines_of(rel) or []:
                if low in line.lower():
                    n += 1
    return n


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "scripts/validation_dataset_manual_full.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    cases = data["test_cases"]
    fail: list[str] = []
    warn: list[str] = []

    # 1) 구조 ---------------------------------------------------------------
    dup_id = [k for k, n in Counter(c["id"] for c in cases).items() if n > 1]
    dup_q = [k for k, n in Counter(c["query"] for c in cases).items() if n > 1]
    if dup_id:
        fail.append(f"ID 중복 {len(dup_id)}건: {dup_id[:5]}")
    if dup_q:
        fail.append(f"질의 중복 {len(dup_q)}건: {dup_q[:3]}")

    grid = Counter((c["vendor"], c["category"]) for c in cases)
    target = max(grid.values())
    holes = [f"{v}/{c}={grid[(v, c)]}" for v in VENDORS for c in CATS if grid[(v, c)] != target]
    if holes:
        fail.append(f"커버리지 불균형(목표 {target}): {holes}")

    # 2~4) 정답 케이스 근거 --------------------------------------------------
    ev_total = ev_text_ok = kw_checked = kw_ok = 0
    for c in cases:
        if c["polarity"] != "positive":
            continue
        files = []
        for ev in c.get("evidence", []):
            ev_total += 1
            ls = lines_of(ev["file"])
            if ls is None:
                fail.append(f"{c['id']}: 근거 파일 없음 {ev['file']}")
                continue
            files.append(ev["file"])
            if not (1 <= ev["line"] <= ev.get("line_end", ev["line"]) <= len(ls)):
                fail.append(f"{c['id']}: 행 범위 초과 {ev['file']}:{ev['line']} (총 {len(ls)})")
                continue
            # 인용 검증: verbatim은 축자 포함, summary(여러 행 병합 요약)는 토큰 중첩률로 확인
            end = ev.get("line_end", ev["line"])
            window = norm("".join(ls[max(0, ev["line"] - 3): end + 2]))
            if ev.get("quote_type") == "summary":
                toks = [t for t in re.findall(r"[A-Za-z0-9가-힣]{2,}", ev["text"])][:20]
                hit = sum(1 for t in toks if norm(t) in window)
                if toks and hit / len(toks) >= 0.5:
                    ev_text_ok += 1
                else:
                    fail.append(
                        f"{c['id']}: 요약 인용의 토큰 중첩률 부족 "
                        f"({hit}/{len(toks)}) @ {ev['file']}:{ev['line']}"
                    )
            elif norm(ev["text"])[:60] in window:
                ev_text_ok += 1
            else:
                fail.append(f"{c['id']}: 축자 인용 불일치 @ {ev['file']}:{ev['line']}")
        if not files:
            fail.append(f"{c['id']}: 근거 0건")
            continue

        # 경로 귀속
        pc = c.get("expected_path_contains", "")
        if pc and not any(pc in f for f in files):
            fail.append(f"{c['id']}: expected_path_contains('{pc}')가 근거 파일과 불일치")

        # 키워드 실존
        blob = "\n".join("\n".join(lines_of(f) or []) for f in files)
        nb = norm(blob)
        for kw in c.get("expected_keywords", []):
            kw_checked += 1
            if norm(kw) in nb:
                kw_ok += 1
            else:
                warn.append(f"{c['id']}: 키워드 '{kw}' 가 근거 파일에 없음")

    # 5) 부정 케이스 부재 재검증 ---------------------------------------------
    neg = [c for c in cases if c["polarity"] == "negative"]
    neg_ok = 0
    for c in neg:
        ab = c.get("absence_evidence") or {}
        cmd = ab.get("command", "")
        m = re.search(r"grep -r[in]*\s+'([^']+)'", cmd)
        if not m:
            warn.append(f"{c['id']}: 부재 근거 명령 파싱 불가")
            continue
        token = m.group(1)
        # 스코프 결정: 명령 끝의 벤더 디렉터리, 없으면 전체
        scope = [v for v in VENDORS if re.search(rf"{re.escape(v)}(\s|/|$|#)", cmd)]
        if not scope:
            scope = VENDORS
        flavor = c.get("negative_flavor")
        if flavor == "sibling_model_leak":
            # 항목이 벤더 전체엔 있으나 대상 모델 문서엔 없어야 함
            model = re.search(r"([A-Z]\w{3,}[\w\-]*)", c["query"])
            hits = 0
            for vendor in scope:
                for f in (CORPUS / vendor).rglob("*.md"):
                    if model and model.group(1) not in f.name and model.group(1) not in str(f.parent):
                        continue
                    rel = f.relative_to(CORPUS).as_posix()
                    hits += sum(1 for l in lines_of(rel) or [] if token.lower() in l.lower())
            actual = hits
        else:
            actual = scan_count(token, scope)
        if actual == 0:
            neg_ok += 1
        else:
            fail.append(f"{c['id']}: 부재 주장 실패 — '{token}' 이 {scope} 에서 {actual}건 발견됨")

    # 결과 ------------------------------------------------------------------
    print(f"데이터셋      : {src.name}  (v{data.get('version')})")
    print(f"케이스        : {len(cases)}  (정답 {len(cases)-len(neg)} / 부정 {len(neg)})")
    print(f"출처          : {dict(Counter(c.get('source','?') for c in cases))}")
    print(f"커버리지      : {len(VENDORS)}벤더 x {len(CATS)}유형 x {target}건")
    print(f"근거 인용 일치: {ev_text_ok}/{ev_total}")
    print(f"키워드 실존   : {kw_ok}/{kw_checked}")
    print(f"부재 재확인   : {neg_ok}/{len(neg)}")
    print(f"\n실패(FAIL): {len(fail)}")
    for x in fail[:20]:
        print("  -", x)
    print(f"경고(WARN): {len(warn)}")
    for x in warn[:15]:
        print("  -", x)
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
