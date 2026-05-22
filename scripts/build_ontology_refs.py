"""온톨로지 카드 → referenced main corpus paths 인덱스 빌더.

input_ontology/ 의 모든 카드 frontmatter에서 taught_in / documented_in /
corpus_paths / manual_paths 필드를 추출해, 카드 doc_path를 키로 하는
referenced paths 매핑을 만들어 data/ontology/onto_refs.json 에 저장한다.

OntologyAugmentedSearch가 런타임에 이 파일을 로드해서 보조 카드 hit 시
main corpus의 referenced 청크를 결과에 inject하는 데 사용한다.

사용법:
    python scripts/build_ontology_refs.py
    python scripts/build_ontology_refs.py --onto-dir input_ontology --out data/ontology/onto_refs.json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import yaml

_DEFAULT_FIELDS = ("taught_in", "documented_in", "corpus_paths", "manual_paths")


def extract_card_refs(card_path: Path, fields: tuple[str, ...]) -> list[str]:
    """단일 카드 md에서 referenced paths 리스트 추출."""
    content = card_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", content, re.S)
    if not m:
        return []
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return []
    if not isinstance(fm, dict):
        return []
    collected: list[str] = []
    for f in fields:
        v = fm.get(f)
        if isinstance(v, list):
            collected.extend(str(x) for x in v if x)
    # 중복 제거 (순서 보존)
    seen: set[str] = set()
    deduped: list[str] = []
    for p in collected:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped


def normalize_ref(ref: str, input_base: Path | None) -> str | None:
    """Reference path를 main corpus 청크 lookup용 절대 경로로 정규화.

    - .md 확장자가 없는 경로(디렉토리)는 None 반환 (inject 대상 제외, 정보용으로만 사용)
    - input_base가 주어지면 input_base 하위 절대 경로로 변환
    - 이미 절대 경로면 그대로
    """
    if not ref.endswith(".md"):
        return None
    if input_base is None:
        return ref
    p = Path(ref)
    if p.is_absolute():
        return str(p)
    return str((input_base / ref).resolve())


def build(
    onto_dir: Path,
    fields: tuple[str, ...],
    input_base: Path | None,
) -> dict[str, dict[str, list[str]]]:
    """전체 카드 디렉토리를 스캔해서 매핑 빌드.

    Returns:
        {card_key: {"injectable": [abs_paths], "directory_hints": [dir_paths]}}
        - injectable: ChromaStore lookup으로 청크를 가져올 수 있는 절대 경로 (.md)
        - directory_hints: 디렉토리만 적힌 ref (LLM에게 정보로만 전달)
    """
    refs: dict[str, dict[str, list[str]]] = {}
    project_root = onto_dir.parent
    for md in sorted(onto_dir.rglob("*.md")):
        if md.name == "README.md":
            continue
        if "schema" in md.parts or "_relations" in md.parts:
            continue
        raw_paths = extract_card_refs(md, fields)
        if not raw_paths:
            continue
        injectable: list[str] = []
        dir_hints: list[str] = []
        seen_inj: set[str] = set()
        seen_dir: set[str] = set()
        for r in raw_paths:
            norm = normalize_ref(r, input_base)
            if norm is None:
                if r not in seen_dir:
                    seen_dir.add(r)
                    dir_hints.append(r)
            else:
                if norm not in seen_inj:
                    seen_inj.add(norm)
                    injectable.append(norm)
        entry = {"injectable": injectable, "directory_hints": dir_hints}
        try:
            rel = str(md.relative_to(project_root))
        except ValueError:
            rel = str(md)
        refs[str(md)] = entry
        refs[rel] = entry
    return refs


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ontology referenced-paths index")
    parser.add_argument("--onto-dir", default="input_ontology",
                        help="온톨로지 카드 디렉토리 (기본 input_ontology)")
    parser.add_argument("--input-base", default="input_optimized",
                        help="referenced path 정규화 base (기본 input_optimized)")
    parser.add_argument("--out", default="data/ontology/onto_refs.json",
                        help="출력 JSON 경로")
    parser.add_argument("--fields", default=",".join(_DEFAULT_FIELDS),
                        help="추출할 frontmatter 필드 (CSV)")
    args = parser.parse_args()

    onto_dir = Path(args.onto_dir).resolve()
    if not onto_dir.exists():
        raise SystemExit(f"onto-dir not found: {onto_dir}")

    input_base = Path(args.input_base).resolve() if args.input_base else None
    if input_base and not input_base.exists():
        raise SystemExit(f"input-base not found: {input_base}")

    fields = tuple(f.strip() for f in args.fields.split(",") if f.strip())
    refs = build(onto_dir, fields, input_base)

    unique_cards = len({k for k in refs if not k.startswith("/")})
    payload = {
        "version": "2.0.0",
        "generated_at": datetime.now().isoformat(),
        "onto_dir": str(onto_dir),
        "input_base": str(input_base) if input_base else None,
        "fields": list(fields),
        "card_count": unique_cards,
        "total_keys": len(refs),
        "refs": refs,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"saved: {out}")
    print(f"  cards with refs: {unique_cards}")
    print(f"  total key entries (abs + rel): {len(refs)}")
    # 통계
    rel_only = [v for k, v in refs.items() if not k.startswith("/")]
    if rel_only:
        inj_total = sum(len(v["injectable"]) for v in rel_only)
        dir_total = sum(len(v["directory_hints"]) for v in rel_only)
        max_inj = max(len(v["injectable"]) for v in rel_only)
        print(f"  injectable paths: total={inj_total}, max/card={max_inj}, avg={inj_total/len(rel_only):.1f}")
        print(f"  directory hints:  total={dir_total}, avg={dir_total/len(rel_only):.1f}")


if __name__ == "__main__":
    main()
