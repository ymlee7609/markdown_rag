#!/usr/bin/env python3
"""CCIE_Vol1 md 파일을 Part 단위로 병합하는 스크립트.

761개의 잘게 쪼개진 파일을 CCIE_Vol2 구조와 유사하게 Part 단위로 병합한다.
"""
import re
import shutil
from pathlib import Path

VOL1_DIR = Path("input/Cisco_CCIE/CCIE_Vol1")
BACKUP_DIR = Path("input/Cisco_CCIE/CCIE_Vol1_backup")

# 병합 그룹 정의: (출력 파일명, 시작 번호, 끝 번호)
MERGE_GROUPS = [
    ("00_front-matter.md", 0, 6),
    ("01_ccie-routing-and-switching-v50-official-cert-guide.md", None, None),  # 특수: file 00만
    ("02_fifth-edition.md", 7, 33),
    ("03_part-i-lan-switching.md", 34, 163),
    ("04_part-ii-ip-networking.md", 164, 248),
    ("05_part-iii-ip-igp-routing.md", 249, 548),
    ("06_part-iv-final-preparation.md", 549, 562),
    ("07_part-v-appendixes.md", 563, 615),
    ("08_cd-only.md", 616, 759),
]


def get_numbered_files(directory: Path) -> dict[int, Path]:
    """디렉토리에서 숫자 접두사가 있는 md 파일을 번호별로 매핑."""
    files = {}
    for f in directory.glob("*.md"):
        if f.name == "INDEX.md":
            continue
        match = re.match(r"^(\d+)_", f.name)
        if match:
            num = int(match.group(1))
            files[num] = f
    return files


def merge_files(files: dict[int, Path], start: int, end: int) -> str:
    """번호 범위의 파일들을 순서대로 합친 내용을 반환."""
    contents = []
    for num in sorted(files.keys()):
        if start <= num <= end:
            text = files[num].read_text(encoding="utf-8").strip()
            if text:
                contents.append(text)
    return "\n\n".join(contents) + "\n"


def main():
    if not VOL1_DIR.exists():
        print(f"오류: {VOL1_DIR} 디렉토리가 없습니다.")
        return

    numbered_files = get_numbered_files(VOL1_DIR)
    print(f"발견된 번호 파일: {len(numbered_files)}개")

    # 백업 생성
    if BACKUP_DIR.exists():
        print(f"기존 백업 제거: {BACKUP_DIR}")
        shutil.rmtree(BACKUP_DIR)

    print(f"백업 생성: {BACKUP_DIR}")
    shutil.copytree(VOL1_DIR, BACKUP_DIR)

    # INDEX.md 보존
    index_content = None
    index_file = VOL1_DIR / "INDEX.md"
    if index_file.exists():
        index_content = index_file.read_text(encoding="utf-8")

    # 기존 md 파일 삭제 (_images 디렉토리는 유지)
    for f in VOL1_DIR.glob("*.md"):
        f.unlink()
    print("기존 md 파일 삭제 완료")

    # 병합 파일 생성
    for output_name, start, end in MERGE_GROUPS:
        output_path = VOL1_DIR / output_name

        if output_name == "01_ccie-routing-and-switching-v50-official-cert-guide.md":
            # 특수 케이스: file 00의 첫 줄(타이틀)만
            if 0 in numbered_files:
                # 실제 파일 내용에서 타이틀 추출
                backup_file = BACKUP_DIR / numbered_files[0].name
                first_line = backup_file.read_text(encoding="utf-8").strip().split("\n")[0]
                output_path.write_text(first_line + "\n", encoding="utf-8")
            print(f"  생성: {output_name} (타이틀 전용)")
            continue

        # 백업에서 읽기 (원본은 이미 삭제)
        backup_files = get_numbered_files(BACKUP_DIR)
        content = merge_files(backup_files, start, end)

        if content.strip():
            output_path.write_text(content, encoding="utf-8")
            file_count = sum(1 for n in backup_files if start <= n <= end)
            lines = content.count("\n")
            print(f"  생성: {output_name} ({file_count}개 파일 병합, {lines}줄)")
        else:
            print(f"  건너뜀: {output_name} (내용 없음)")

    # INDEX.md 복원
    if index_content:
        (VOL1_DIR / "INDEX.md").write_text(index_content, encoding="utf-8")
        print("  복원: INDEX.md")

    # 결과 확인
    print("\n=== 병합 결과 ===")
    for f in sorted(VOL1_DIR.glob("*.md")):
        lines = f.read_text(encoding="utf-8").count("\n")
        print(f"  {f.name}: {lines}줄")

    print(f"\n_images 디렉토리: {'유지됨' if (VOL1_DIR / '_images').exists() else '없음'}")
    print(f"백업 위치: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
