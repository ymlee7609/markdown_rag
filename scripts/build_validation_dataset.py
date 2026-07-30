#!/usr/bin/env python3
"""가입자망장비 매뉴얼 코퍼스에서 RAG 검증 케이스를 생성한다.

설계 원칙:
  - 모든 정답 케이스의 근거(파일/행/원문)는 코퍼스에서 직접 추출한다. 창작하지 않는다.
  - 모든 부정 케이스의 부재 주장은 대상 범위를 실제로 스캔해 매칭 0건을 확인한 것만 채택한다.
  - 손으로 작성한 24개 큐레이션 케이스는 그대로 유지하고(source=curated),
    생성 케이스(source=generated)를 덧붙여 벤더 x 유형별 목표 개수를 채운다.

사용법:
    python3 scripts/build_validation_dataset.py [--per-cell 10] [--out 경로.json]
"""

from __future__ import annotations

import argparse
import json
import random
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "input_optimized/가입자망장비_manual"
CURATED = ROOT / "scripts/validation_dataset_manual.json"

VENDORS = ["다산_L2", "다산_L3", "다산_OLT", "유비쿼스_L2", "유비쿼스_L3", "유비쿼스_OLT"]
VENDOR_BRAND = {v: ("다산" if v.startswith("다산") else "유비쿼스") for v in VENDORS}
PREFIX = {
    "다산_L2": "DSN-L2", "다산_L3": "DSN-L3", "다산_OLT": "DSN-OLT",
    "유비쿼스_L2": "UBQ-L2", "유비쿼스_L3": "UBQ-L3", "유비쿼스_OLT": "UBQ-OLT",
}
CATS = ["spec_value", "command_syntax", "diagnostics", "negative"]
CAT_TAG = {"spec_value": "SPEC", "command_syntax": "CMD", "diagnostics": "DIAG", "negative": "NEG"}

MODEL_RE = re.compile(
    r"(V\d[\dxX]{3}[A-Z0-9]*(?:-10G)?|U9[\dxX]{2,3}[A-Z]*(?:-10G)?|E\d[\dxX]{3}[A-Z]*|P8\d{3}[A-Z]*)"
)
SPEC_ITEMS = ["무게", "소비 전력", "동작 온도", "입력 전압", "저장 온도", "동작 습도", "크기"]

rng = random.Random(20260728)


# ---------------------------------------------------------------- 텍스트 정리

def clean(text: str) -> str:
    """마크다운 잔재와 PDF 추출 아티팩트를 제거해 사람이 읽을 문장으로 만든다."""
    t = unicodedata.normalize("NFC", text)
    t = re.sub(r"<br\s*/?>", " ", t)
    t = re.sub(r"!\[.*?\]\(.*?\)", " ", t)
    t = t.replace("**", "").replace("`", "").replace("_", " ")
    t = re.sub(r"\s+", " ", t).strip(" |")
    return t.strip()


def spaced(text: str) -> str:
    """한글과 영문/숫자가 붙어버린 추출 아티팩트에 공백을 넣는다.

    원문은 'VLAN이름을 지정하여 새로운VLAN을' 처럼 공백이 소실되어 있다.
    질의는 사람이 쓰는 정상 표기여야 하므로 여기서 복원한다(= 검색측 정규화 검증 대상)."""
    t = re.sub(r"([가-힣])([A-Za-z0-9])", r"\1 \2", text)
    t = re.sub(r"([A-Za-z0-9])([가-힣])", r"\1 \2", t)
    return re.sub(r"\s+", " ", t).strip()


def model_of(path: Path) -> str | None:
    for seg in reversed(path.relative_to(CORPUS).parts[1:]):
        m = MODEL_RE.search(seg)
        if m:
            return m.group(1)
    return None


# ---------------------------------------------------------------- 코퍼스 적재

def load_corpus() -> dict:
    """{vendor: [(relpath, model, [lines])]} 형태로 전체 코퍼스를 메모리에 올린다."""
    corpus = defaultdict(list)
    for vendor in VENDORS:
        for f in sorted((CORPUS / vendor).rglob("*.md")):
            rel = f.relative_to(CORPUS).as_posix()
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            corpus[vendor].append((rel, model_of(f), lines))
    return corpus


def count_token(corpus: dict, token: str, vendors: list[str]) -> int:
    """지정 벤더 범위에서 토큰 출현 횟수를 센다(부재 주장 검증용)."""
    low = token.lower()
    return sum(
        1
        for v in vendors
        for _, _, lines in corpus[v]
        for line in lines
        if low in line.lower()
    )


# ---------------------------------------------------------------- 후보 추출기

ROW_RE = re.compile(r"^\|\s*\*\*[`]?\s*([A-Za-z][A-Za-z0-9 \-]{1,44}?)\s*[`]?(?:\*\*|<br>|\|)")
DEFAULT_RE = re.compile(r"Default\s*[:：]\s*([^|<]{1,40})")
RANGE_PROSE_RE = re.compile(
    r"([가-힣A-Za-z][^.。]{2,40}?)(?:는|은|을|를)?\s*<\s*([\d,]+)\s*[-–~]\s*([\d,]+)\s*>\s*범위"
)
DEFAULT_PROSE_RE = re.compile(r"기본값은\s*([^.,]{1,24})\s*(?:입니다|이다)")
SPEC_ROW_RE = re.compile(r"^\|\s*(" + "|".join(SPEC_ITEMS) + r")\s*\|\s*(.{2,120}?)\s*\|?\s*$")
LED_ROW_RE = re.compile(r"^\|\s*\*{0,2}([A-Z][A-Za-z0-9()/ ]{1,20})\*{0,2}\s*\|(.*(?:녹색|주황).*)\|(.+)$")
BULLET_SPEC_RE = re.compile(r"^-\s*(" + "|".join(SPEC_ITEMS) + r")\s*[:：]\s*(.{2,60})$")


def split_row(line: str) -> list[str]:
    return [c for c in line.strip().strip("|").split("|")]


def extract_spec(corpus: dict, vendor: str) -> list[dict]:
    """제원·기본값 후보: 사양표 행, Default 명시 행, 범위 명시 산문."""
    out = []
    for rel, model, lines in corpus[vendor]:
        if not model:
            continue
        for i, raw in enumerate(lines, start=1):
            line = raw.strip()

            m = SPEC_ROW_RE.match(line) or BULLET_SPEC_RE.match(line)
            if m and not re.search(r"[가-힣]{6,}", m.group(2)):
                item, value = m.group(1), clean(m.group(2))
                if value and re.search(r"\d", value):
                    out.append({
                        "kind": "spec_row", "subject": item, "value": value,
                        "file": rel, "line": i, "text": clean(line), "model": model,
                    })
                continue

            m = DEFAULT_RE.search(line)
            if m and line.startswith("|"):
                cells = split_row(line)
                # 명령명만 취한다. <21-100>, {5|60} 같은 파라미터 표기는 잘라낸다.
                head = re.split(r"[<{\[(]", clean(cells[0]))[0]
                cmd = " ".join(head.split())[:40].rstrip(" -")
                if cmd and re.match(r"^[a-zA-Z][a-zA-Z0-9 \-]*$", cmd) and len(cmd) >= 3:
                    out.append({
                        "kind": "default_row", "subject": cmd, "value": clean(m.group(1)),
                        "file": rel, "line": i, "text": clean(line)[:400], "model": model,
                    })
                continue

            m = RANGE_PROSE_RE.search(line)
            if m:
                subj = spaced(clean(m.group(1)))
                if len(subj) > 40:                       # 단어 중간이 아니라 어절 경계에서 자른다
                    subj = subj[-40:].split(" ", 1)[-1]
                subj = subj.lstrip(", ")
                dflt = DEFAULT_PROSE_RE.search(line)
                if len(subj) >= 3:
                    out.append({
                        "kind": "range_prose", "subject": subj,
                        "value": f"{m.group(2)} ~ {m.group(3)}",
                        "default": clean(dflt.group(1)) if dflt else None,
                        "file": rel, "line": i, "text": clean(line)[:400], "model": model,
                    })
    return out


MODE_VOCAB = re.compile(
    r"^(Global|Bridge|Enable|Interface|Privileged|Config[\w\-\[\]]*|Router|Pon[\w\-]*|View|"
    r"Onu-profile|EXEC|User|VLAN|Line)\b", re.I
)
STEP_RE = re.compile(r"^step\s*\d+$", re.I)
# 명령어 유형에서 제외할 설명(삭제/복귀/해제 계열) - 원본 명령과 짝을 이루는 잉여 항목
DROP_DESC = re.compile(r"(삭제|해제|복귀|되돌|취소|초기화)")
# 서술형 종결어미 -> 관형형. "보여준다" -> "보여주는" 처럼 자연스러운 질문으로 만든다.
ENDINGS = [
    ("확인합니다", "확인하는"), ("설정합니다", "설정하는"), ("출력합니다", "출력하는"),
    ("보여줍니다", "보여주는"), ("적용합니다", "적용하는"), ("등록합니다", "등록하는"),
    ("지정합니다", "지정하는"), ("변경합니다", "변경하는"), ("활성화합니다", "활성화하는"),
    ("만듭니다", "만드는"), ("합니다", "하는"), ("됩니다", "되는"),
    ("보여준다", "보여주는"), ("출력한다", "출력하는"), ("확인한다", "확인하는"),
    ("설정한다", "설정하는"), ("사용한다", "사용하는"), ("표시한다", "표시하는"),
    ("한다", "하는"), ("된다", "되는"), ("이다", "인"),
]


def to_modifier(desc: str) -> str:
    """설명문 종결어미를 관형형으로 바꿔 '~하는 명령어는?' 질문에 자연스럽게 붙인다."""
    d = desc.rstrip(" .。")
    for src, dst in ENDINGS:
        if d.endswith(src):
            return d[: -len(src)] + dst
    return d


def parse_cmd_row(line: str):
    """표 행에서 (명령, 모드, 설명)을 뽑는다.

    벤더마다 열 배치가 다르다:
      다산     |**cmd**|모드|설명|
      유비쿼스 |**cmd**|설명|모드|   또는  |**StepN**|**cmd**|설명|
    따라서 위치가 아니라 내용으로 판별한다 - 한글이 가장 많은 셀이 설명, 모드 어휘에
    맞는 셀이 모드다."""
    cells = [clean(c) for c in split_row(line)]
    if len(cells) < 2:
        return None
    head = cells[0]
    body = cells[1:]
    if STEP_RE.match(head):                       # Step 라벨 열이면 다음 셀이 명령
        if not body:
            return None
        head, body = body[0], body[1:]
    if not re.match(r"^[A-Za-z][A-Za-z0-9 \-]{1,44}$", head):
        return None
    cmd = " ".join(head.split())

    def hangul(s):
        return len(re.findall(r"[가-힣]", s))

    desc_cell = max(body, key=hangul) if body else ""
    if hangul(desc_cell) < 4:
        return None
    mode = next((c for c in body if c is not desc_cell and MODE_VOCAB.match(c)), "")
    return cmd, mode, spaced(desc_cell)


def extract_commands(corpus: dict, vendor: str, want_show: bool) -> list[dict]:
    """명령어 정의 표 행. want_show=True면 show/monitor/debug 계열만 골라 진단 유형에 쓴다."""
    out = []
    for rel, model, lines in corpus[vendor]:
        if not model:
            continue
        for i, raw in enumerate(lines, start=1):
            line = raw.strip()
            if not line.startswith("|") or "---" in line or "**" not in line:
                continue
            parsed = parse_cmd_row(line)
            if not parsed:
                continue
            cmd, mode, desc = parsed
            if cmd.lower().startswith("no ") or DROP_DESC.search(desc):
                continue
            is_show = cmd.lower().startswith(("show", "monitor", "debug"))
            if is_show != want_show:
                continue
            if not (12 <= len(desc) <= 110):
                continue
            out.append({
                "kind": "cmd_row", "command": cmd, "mode": mode, "desc": to_modifier(desc),
                "file": rel, "line": i, "text": clean(line)[:400], "model": model,
            })

    # 같은 설명이 서로 다른 명령에 붙어 있으면 질문이 중의적이 되므로 통째로 버린다.
    # (예: "설정 내용을 확인하는" -> show running-config / show auto-reset status / ...)
    by_desc = defaultdict(set)
    for c in out:
        by_desc[c["desc"]].add(c["command"].lower())
    return [c for c in out if len(by_desc[c["desc"]]) == 1]


def extract_led(corpus: dict, vendor: str) -> list[dict]:
    """LED 색상-의미 매핑 행."""
    out = []
    for rel, model, lines in corpus[vendor]:
        if not model:
            continue
        for i, raw in enumerate(lines, start=1):
            line = raw.strip()
            m = LED_ROW_RE.match(line)
            if not m:
                continue
            name, states, meanings = m.group(1).strip(), clean(m.group(2)), clean(m.group(3))
            if not re.search(r"[가-힣]{4,}", meanings) or len(meanings) < 8:
                continue
            out.append({
                "kind": "led_row", "led": name, "states": states, "meanings": spaced(meanings),
                "file": rel, "line": i, "text": clean(line)[:400], "model": model,
            })
    return out


# ---------------------------------------------------------------- 케이스 조립

def spread(cands: list[dict], n: int, keyfn) -> list[dict]:
    """모델/주제가 한쪽에 쏠리지 않도록 라운드로빈으로 n개를 고른다."""
    buckets = defaultdict(list)
    for c in cands:
        buckets[c["model"]].append(c)
    for b in buckets.values():
        rng.shuffle(b)
    picked, seen = [], set()
    order = sorted(buckets, key=lambda m: -len(buckets[m]))
    while len(picked) < n and any(buckets.values()):
        for model in order:
            if not buckets[model]:
                continue
            c = buckets[model].pop()
            k = keyfn(c)
            if k in seen:
                continue
            seen.add(k)
            picked.append(c)
            if len(picked) >= n:
                break
    return picked


def build_spec_cases(vendor, cands, n, start):
    cases = []
    for idx, c in enumerate(spread(cands, n, lambda x: (x["subject"].lower(), x["model"])), start):
        brand, model = VENDOR_BRAND[vendor], c["model"]
        if c["kind"] == "spec_row":
            query = f"{brand} {model}의 {c['subject']}은(는) 얼마인가?"
            answer = f"{c['subject']}: {c['value']}"
            keywords = [model, c["subject"]] + re.findall(r"[\d.]+", c["value"])[:2]
        elif c["kind"] == "default_row":
            query = f"{brand} {model}에서 `{c['subject']}` 명령의 기본값(Default)은?"
            answer = f"Default: {c['value']}"
            keywords = [model, c["subject"].split()[0], "Default"] + re.findall(r"[\d.]+", c["value"])[:1]
        else:
            dflt = f", 기본값은 {c['default']}" if c.get("default") else ""
            query = f"{brand} {model}에서 {c['subject']}의 설정 가능 범위는?"
            answer = f"{c['value']} 범위에서 설정 가능{dflt}."
            keywords = ([model] + c["value"].replace(" ", "").split("~")[:2]
                        + [w for w in re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", c["subject"])[:2]])
        cases.append(_case(vendor, "spec_value", idx, query, answer, c, keywords,
                           "표/산문에서 수치 제원을 정확히 회수하는지 확인."))
    return cases


def build_cmd_cases(vendor, cands, n, start, category):
    cases = []
    for idx, c in enumerate(spread(cands, n, lambda x: (x["command"].lower(), x["model"])), start):
        brand, model = VENDOR_BRAND[vendor], c["model"]
        if c["desc"].endswith(("다", "요")):
            # 종결어미 변환이 안 된 설명은 인용형으로 질문해 비문을 피한다.
            query = f"{brand} {model} 매뉴얼에서 '{c['desc']}' 로 설명된 기능의 명령어는 무엇인가?"
        else:
            query = f"{brand} {model}에서 {c['desc']} 명령어는 무엇인가?"
        mode = f" ({c['mode']} 모드)" if c["mode"] and len(c["mode"]) < 40 else ""
        answer = f"`{c['command']}`{mode}"
        keywords = [model] + c["command"].split()[:3]
        note = ("질의는 매뉴얼 기능 설명의 종결어미를 관형형으로 바꾸고 공백을 복원한 것이라 "
                "원문 표기와 다름(검색측 정규화 검증). 명령 토큰 순서까지 일치해야 정답.")
        cases.append(_case(vendor, category, idx, query, answer, c, keywords, note))
    return cases


def build_led_cases(vendor, cands, n, start):
    cases = []
    for idx, c in enumerate(spread(cands, n, lambda x: (x["led"].lower(), x["model"])), start):
        brand, model = VENDOR_BRAND[vendor], c["model"]
        query = f"{brand} {model}에서 {c['led']} LED의 색상별 표시 상태가 각각 무엇을 의미하나?"
        answer = f"{c['states']} → {c['meanings']}"
        cases.append(_case(vendor, "diagnostics", idx, query, answer, c, [model, c["led"], "LED"],
                           "LED 표는 동작/기능이 다중 매핑된 단일 셀. 색상과 의미의 정렬 순서가 어긋나면 반대 의미로 답하게 됨."))
    return cases


def _case(vendor, category, idx, query, answer, cand, keywords, note):
    kws = [k for k in dict.fromkeys(str(k).strip() for k in keywords) if k and len(k) > 1][:6]
    return {
        "id": f"{PREFIX[vendor]}-{CAT_TAG[category]}-{idx:03d}",
        "vendor": vendor,
        "category": category,
        "polarity": "positive",
        "source": "generated",
        "model": cand["model"],
        "query": re.sub(r"\s+", " ", query).strip(),
        "expected_path_contains": cand["file"].rsplit(".md", 1)[0],
        "expected_keywords": kws,
        "expected_behavior": "answer",
        "expected_answer": answer,
        "evidence": [{"file": cand["file"], "line": cand["line"], "text": cand["text"]}],
        "notes": note,
    }


# ---------------------------------------------------------------- 부정 케이스

CORPUS_ABSENT_CANDIDATES = [
    ("MTBF(평균 고장 간격)", "MTBF"),
    ("IP 방진방수 등급", "IP65"),
    ("음향 소음(dBA) 수치", "dBA"),
    ("제품 보증 기간", "보증 기간"),
    ("RoHS 인증 여부", "RoHS"),
    ("최대 처리 지연(latency) 규격", "지연 시간 규격"),
]


def build_negative_cases(corpus, vendor, n, start, cmd_index, spec_index):
    """4가지 부재 유형을 섞어 부정 케이스를 만든다. 모든 부재는 실제 스캔으로 확인한다."""
    brand = VENDOR_BRAND[vendor]
    models = [m for m, _ in Counter(
        mm for _, mm, _ in corpus[vendor] if mm).most_common()]
    cases, others = [], [v for v in VENDORS if v != vendor]

    # (1) 교차벤더 문법: 다른 벤더에만 존재하는 명령을 이 벤더 것으로 전제
    foreign = [
        (tok, owner) for tok, owners in cmd_index.items()
        if len(owners) == 1 and (owner := next(iter(owners))) != vendor
        and VENDOR_BRAND[owner] != brand and " " in tok and len(tok) > 9
    ]
    rng.shuffle(foreign)
    for tok, owner in foreign:
        if len(cases) >= n // 2:
            break
        if count_token(corpus, tok, [vendor]) != 0:
            continue
        model = models[len(cases) % len(models)]
        act = "조회하는" if tok.lower().startswith(("show", "monitor", "debug")) else "설정하는"
        cases.append({
            "negative_flavor": "cross_vendor_syntax",
            "model": model,
            "query": f"{brand} {model}에서 `{tok}` 명령으로 {act} 방법은?",
            "expected_behavior": "reject_premise",
            "expected_answer": (
                f"{brand} {model}에는 `{tok}` 명령이 없습니다. "
                f"해당 문법은 {VENDOR_BRAND[owner]} {owner.split('_', 1)[1]} 계열({owner})입니다."
            ),
            "absence_evidence": {
                "command": f"grep -rin '{tok}' --include='*.md' {vendor}",
                "match_count": 0,
                "correct_owner": owner,
            },
            "fail_if_answer_contains": [tok],
            "must_not_cite_path_contains": [owner],
            "wrong_answer_example": f"`{tok}` 를 입력해 {act.replace('는', '면 됩니다')}.",
            "notes": (
                f"교차벤더 문법 트랩. `{tok}` 는 {owner} 에만 존재하고 {vendor} 에는 0건이므로, "
                "벤더 필터가 없으면 타 벤더 청크를 근거로 답하게 됨."
            ),
        })

    # (2a) 문서종류 부재: 이 벤더 전체에 아예 없는 사양 항목(다산은 HW 설치가이드가 없음)
    quota_missing = n // 4 + 1
    made = 0
    for item in SPEC_ITEMS:
        if made >= quota_missing:
            break
        if count_token(corpus, item, [vendor]) != 0:
            continue
        model = models[(len(cases) + made) % len(models)]
        made += 1
        cases.append({
            "negative_flavor": "missing_doc_type",
            "model": model,
            "query": f"{brand} {model}의 {item}은(는) 얼마인가?",
            "expected_behavior": "abstain",
            "expected_answer": f"제공된 {vendor} 매뉴얼에는 {item} 사양이 포함되어 있지 않아 확인할 수 없습니다.",
            "absence_evidence": {
                "command": f"grep -rn '{item}' --include='*.md' {vendor}",
                "match_count": 0,
                "note": f"{vendor} 전체 문서에 '{item}' 0건 — 해당 종류의 문서(HW 설치가이드)가 부재.",
            },
            "fail_if_answer_contains": [],
            "must_not_cite_path_contains": [v for v in VENDORS if VENDOR_BRAND[v] != brand],
            "wrong_answer_example": f"{model}의 {item}은 동급 장비와 유사한 수준입니다.",
            "notes": (f"문서 종류 부재 트랩. 타 벤더 HW 설치가이드의 {item} 사양표가 의미상 유사해 "
                      "상위 랭크될 수 있음. 벤더 경계를 넘어 답하는지 확인."),
        })

    # (2b) 형제 모델 전이: 같은 벤더 내 다른 모델에만 있는 사양 항목을 이 모델에 묻기
    quota_sibling = len(cases) + n // 4 + 1
    for model in models:
        if len(cases) >= quota_sibling:
            break
        have = spec_index[vendor].get(model, set())
        for item in SPEC_ITEMS:
            if len(cases) >= quota_sibling:
                break
            siblings = [m for m in models if m != model and item in spec_index[vendor].get(m, set())]
            if item in have or not siblings:
                continue
            if count_token(corpus, item, [vendor]) and _model_has(corpus, vendor, model, item):
                continue
            cases.append({
                "negative_flavor": "sibling_model_leak",
                "model": model,
                "query": f"{brand} {model}의 {item}은(는) 얼마인가?",
                "expected_behavior": "abstain",
                "expected_answer": f"{model} 문서에는 {item} 사양이 기재되어 있지 않아 확인할 수 없습니다.",
                "absence_evidence": {
                    "command": f"grep -rn '{item}' --include='*.md' {vendor}  # {model} 문서 한정 0건",
                    "match_count": 0,
                    "note": f"형제 모델 {', '.join(siblings[:3])} 문서에는 존재.",
                },
                "fail_if_answer_contains": [],
                "must_not_cite_path_contains": [],
                "wrong_answer_example": f"{model}의 {item}은 형제 모델과 동일합니다.",
                "notes": f"형제 모델 정보 전이 트랩. 같은 {vendor} 안의 {siblings[0]} 사양표가 높은 유사도로 검색되지만 {model} 값은 아님. 모델 단위 귀속 검증.",
            })

    # (3) 코퍼스 전체 부재 사양
    for label, token in CORPUS_ABSENT_CANDIDATES:
        if len(cases) >= n:
            break
        if count_token(corpus, token, VENDORS) != 0:
            continue
        model = models[len(cases) % len(models)]
        cases.append({
            "negative_flavor": "out_of_corpus_spec",
            "model": model,
            "query": f"{brand} {model}의 {label}은(는) 어떻게 되나?",
            "expected_behavior": "abstain",
            "expected_answer": "제공된 매뉴얼에서 해당 정보를 찾을 수 없습니다.",
            "absence_evidence": {
                "command": f"grep -rin '{token}' --include='*.md' .",
                "match_count": 0,
                "note": "코퍼스 579개 문서 전체 0건.",
            },
            "fail_if_answer_contains": [],
            "must_not_cite_path_contains": [],
            "wrong_answer_example": f"{model}의 {label}은 업계 표준 수준입니다.",
            "notes": "코퍼스 전체 부재. 모델 사양표 청크가 높은 유사도로 검색되지만 해당 항목은 없음. 검색 성공을 정답 존재로 오인하는지 확인.",
        })

    out = []
    for idx, c in enumerate(cases[:n], start):
        c.update({
            "id": f"{PREFIX[vendor]}-NEG-{idx:03d}",
            "vendor": vendor, "category": "negative", "polarity": "negative",
            "source": "generated", "expected_keywords": [],
        })
        out.append(c)
    return out


def _model_has(corpus, vendor, model, item):
    return any(
        item in line
        for rel, mm, lines in corpus[vendor] if mm == model
        for line in lines
    )


def build_indexes(corpus):
    """명령 토큰 -> 보유 벤더 집합, 벤더/모델 -> 보유 사양 항목 집합."""
    cmd_index, spec_index = defaultdict(set), defaultdict(lambda: defaultdict(set))
    for vendor in VENDORS:
        for rel, model, lines in corpus[vendor]:
            for line in lines:
                s = line.strip()
                if s.startswith("|"):
                    m = ROW_RE.match(s)
                    if m:
                        cmd_index[" ".join(m.group(1).split()).lower()].add(vendor)
                if model:
                    for item in SPEC_ITEMS:
                        if re.match(rf"^[-|]\s*\*{{0,2}}{re.escape(item)}\*{{0,2}}\s*[:|]", s):
                            spec_index[vendor][model].add(item)
    return cmd_index, spec_index


# ---------------------------------------------------------------- 메인

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-cell", type=int, default=10, help="벤더 x 유형 셀당 목표 케이스 수")
    ap.add_argument("--out", default=str(ROOT / "scripts/validation_dataset_manual_full.json"))
    args = ap.parse_args()

    corpus = load_corpus()
    cmd_index, spec_index = build_indexes(corpus)
    curated = json.loads(CURATED.read_text(encoding="utf-8"))

    kept = defaultdict(list)
    for c in curated["test_cases"]:
        c["source"] = "curated"
        kept[(c["vendor"], c["category"])].append(c)

    all_cases, _seen_queries = [], set()
    for vendor in VENDORS:
        for cat in CATS:
            base = kept[(vendor, cat)]
            need = args.per_cell - len(base)
            if cat == "spec_value":
                gen = build_spec_cases(vendor, extract_spec(corpus, vendor), need, 101)
            elif cat == "command_syntax":
                gen = build_cmd_cases(vendor, extract_commands(corpus, vendor, False), need, 101, cat)
            elif cat == "diagnostics":
                led = extract_led(corpus, vendor)
                take_led = min(len(led), need // 3)
                gen = build_led_cases(vendor, led, take_led, 101)
                gen += build_cmd_cases(vendor, extract_commands(corpus, vendor, True),
                                       need - len(gen), 201, cat)
            else:
                gen = build_negative_cases(corpus, vendor, need, 101, cmd_index, spec_index)
            for c in base + gen:                 # 전역 질의 중복 방지
                if c["query"] in _seen_queries:
                    continue
                _seen_queries.add(c["query"])
                all_cases.append(c)
            got = sum(1 for c in all_cases if c["vendor"] == vendor and c["category"] == cat)
            if got < args.per_cell:
                print(f"  [부족] {vendor}/{cat}: {got}/{args.per_cell}")

    data = {
        "version": "2.0.0",
        "description": (
            f"가입자망장비 매뉴얼 RAG 검증 데이터셋 - 벤더 6종 x 유형 4종 x {args.per_cell}건 = {len(all_cases)} 케이스. "
            "정답 케이스 근거는 코퍼스에서 직접 추출, 부정 케이스 부재는 실제 스캔으로 0건 확인."
        ),
        "corpus_root": "input_optimized/가입자망장비_manual",
        "vendors": VENDORS,
        "categories": dict(Counter(c["category"] for c in all_cases)),
        "sources": dict(Counter(c["source"] for c in all_cases)),
        "category_definitions": curated["category_definitions"],
        "negative_flavors": curated["negative_flavors"],
        "pass_criteria": curated["pass_criteria"],
        "test_cases": all_cases,
    }
    Path(args.out).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"생성: {args.out}  ({len(all_cases)} 케이스)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
