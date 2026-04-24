#!/usr/bin/env python3
# input/ 디렉토리 md 파일 사이즈 분석 및 재구조화 후보 산출
# 사용법: python scripts/analyze_file_sizes.py [--out reports/]

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# 권장 사이즈 정책
MIN_OPTIMAL = 8 * 1024           # 8 KB
MAX_OPTIMAL = 80 * 1024          # 80 KB
MERGE_THRESHOLD = 2 * 1024       # < 2 KB: 병합 후보
SPLIT_THRESHOLD = 100 * 1024     # > 100 KB: 분할 후보

# 버킷 경계 (bytes)
BUCKETS = [
    ("0-1KB",      0,         1024),
    ("1-5KB",      1024,      5 * 1024),
    ("5-10KB",     5 * 1024,  10 * 1024),
    ("10-20KB",    10 * 1024, 20 * 1024),
    ("20-50KB",    20 * 1024, 50 * 1024),
    ("50-100KB",   50 * 1024, 100 * 1024),
    ("100-500KB",  100 * 1024, 500 * 1024),
    ("500KB-1MB",  500 * 1024, 1024 * 1024),
    ("1MB+",       1024 * 1024, None),
]


@dataclass
class DirStats:
    path: str
    file_count: int = 0
    total_bytes: int = 0
    small_files: list[Path] = field(default_factory=list)  # < MERGE_THRESHOLD
    large_files: list[Path] = field(default_factory=list)  # > SPLIT_THRESHOLD

    @property
    def avg_kb(self) -> float:
        return self.total_bytes / self.file_count / 1024 if self.file_count else 0.0

    @property
    def total_mb(self) -> float:
        return self.total_bytes / 1024 / 1024


def bucket_of(size: int) -> str:
    for name, lo, hi in BUCKETS:
        if hi is None or size < hi:
            if size >= lo:
                return name
    return "unknown"


def collect(input_root: Path) -> tuple[list[Path], dict[str, DirStats]]:
    files = sorted(input_root.rglob("*.md"))
    by_leaf: dict[str, DirStats] = {}
    for f in files:
        # 매뉴얼 1권 = leaf 디렉토리 (가입자망장비_manual/벤더_카테고리/제품매뉴얼/)
        # IETF_RFC, CCIE는 파일이 바로 하위에 있음
        parent = f.parent
        key = str(parent.relative_to(input_root))
        stats = by_leaf.setdefault(key, DirStats(path=key))
        size = f.stat().st_size
        stats.file_count += 1
        stats.total_bytes += size
        if size < MERGE_THRESHOLD:
            stats.small_files.append(f.relative_to(input_root))
        if size > SPLIT_THRESHOLD:
            stats.large_files.append(f.relative_to(input_root))
    return files, by_leaf


def distribution(files: list[Path]) -> dict[str, int]:
    dist = defaultdict(int)
    for f in files:
        dist[bucket_of(f.stat().st_size)] += 1
    return dict(dist)


def main() -> None:
    parser = argparse.ArgumentParser(description="md 파일 사이즈 분석 + 재구조화 후보 산출")
    parser.add_argument("--input", default="input", help="입력 루트 디렉토리")
    parser.add_argument("--out", default="reports", help="리포트 출력 디렉토리")
    args = parser.parse_args()

    input_root = Path(args.input).resolve()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not input_root.exists():
        raise SystemExit(f"[ERROR] 입력 경로가 없습니다: {input_root}")

    print(f"[1/4] 수집 중... ({input_root})")
    files, by_leaf = collect(input_root)
    total_files = len(files)
    total_bytes = sum(f.stat().st_size for f in files)
    print(f"      md 파일 {total_files}개 / {total_bytes/1024/1024:.2f} MB")

    print("[2/4] 분포 계산...")
    dist = distribution(files)

    # 병합 후보: leaf 디렉토리 중 small_files 비율이 80% 이상이고 평균 < MERGE_THRESHOLD
    merge_candidates = []
    for st in by_leaf.values():
        if st.file_count < 5:
            continue
        small_ratio = len(st.small_files) / st.file_count
        if small_ratio >= 0.5 and st.avg_kb * 1024 < MERGE_THRESHOLD:
            # 몇 개 파일로 쪼갤지 계산 (목표 30 KB 세그먼트)
            target_segments = max(1, round(st.total_bytes / (30 * 1024)))
            merge_candidates.append({
                "dir": st.path,
                "file_count": st.file_count,
                "total_mb": round(st.total_mb, 2),
                "avg_kb": round(st.avg_kb, 2),
                "small_file_ratio": round(small_ratio, 2),
                "suggested_segments": target_segments,
            })
    merge_candidates.sort(key=lambda x: x["file_count"], reverse=True)

    # 분할 후보: 파일 하나 크기가 SPLIT_THRESHOLD 초과
    split_candidates = []
    for f in files:
        size = f.stat().st_size
        if size > SPLIT_THRESHOLD:
            target_parts = max(2, round(size / (40 * 1024)))
            split_candidates.append({
                "file": str(f.relative_to(input_root)),
                "size_kb": round(size / 1024, 1),
                "suggested_parts": target_parts,
            })
    split_candidates.sort(key=lambda x: x["size_kb"], reverse=True)

    print("[3/4] 리포트 생성...")
    in_optimal = sum(
        1 for f in files
        if MIN_OPTIMAL <= f.stat().st_size <= MAX_OPTIMAL
    )
    summary = {
        "input_root": str(input_root),
        "total_files": total_files,
        "total_mb": round(total_bytes / 1024 / 1024, 2),
        "avg_kb": round(total_bytes / total_files / 1024, 2) if total_files else 0.0,
        "in_optimal_range_8_to_80kb": {
            "count": in_optimal,
            "ratio": round(in_optimal / total_files, 3) if total_files else 0.0,
            "target_min_ratio": 0.85,
        },
        "distribution": dist,
        "merge_candidate_dirs": len(merge_candidates),
        "split_candidate_files": len(split_candidates),
    }

    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out_dir / "merge_candidates.json").write_text(
        json.dumps(merge_candidates, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out_dir / "split_candidates.json").write_text(
        json.dumps(split_candidates, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("[4/4] 결과")
    optimal_ratio = summary["in_optimal_range_8_to_80kb"]["ratio"] * 100
    print(f"  - 8~80 KB 범위: {in_optimal}/{total_files} ({optimal_ratio:.1f}%)")
    print(f"  - 병합 후보 디렉토리: {len(merge_candidates)}개")
    print(f"  - 분할 후보 파일: {len(split_candidates)}개")
    print(f"  - 리포트: {out_dir}/")
    print("    * summary.json")
    print("    * merge_candidates.json")
    print("    * split_candidates.json")


if __name__ == "__main__":
    main()
