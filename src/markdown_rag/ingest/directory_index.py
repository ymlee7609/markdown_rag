"""디렉토리 구조 기반 인덱스 문서 생성.

가입자망장비_manual 디렉토리의 계층 구조를 분석하여
벤더-카테고리별 합성 요약 문서를 생성한다.
이 문서들은 "장비 목록" 같은 구조적 쿼리에 대응하기 위해 인덱싱된다.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from markdown_rag.models import Document

logger = logging.getLogger(__name__)

# 벤더-카테고리 디렉토리 패턴 (예: 다산_L2, 유비쿼스_OLT)
_VENDOR_CATEGORY_PATTERN = re.compile(
    r"^(?P<vendor>다산|유비쿼스)_(?P<category>L2|L3|OLT)$"
)

# 모델명 추출 패턴 (대괄호 또는 언더스코어로 감싼 모델명)
_MODEL_PATTERNS = [
    re.compile(r"\[(?P<model>[A-Za-z0-9]+[A-Za-z0-9_\-]*)\]"),
    re.compile(r"^_(?P<model>[A-Za-z0-9]+[A-Za-z0-9\-]*)_"),
    re.compile(r"^(?P<model>[A-Z][A-Za-z0-9]*\d+[A-Za-z0-9]*)"),
]


def _extract_model_name(dir_name: str) -> str:
    """디렉토리 또는 파일 이름에서 장비 모델명을 추출한다."""
    for pattern in _MODEL_PATTERNS:
        match = pattern.search(dir_name)
        if match:
            return match.group("model")
    return dir_name


def _extract_version_info(dir_name: str) -> str:
    """디렉토리 이름에서 버전/날짜 정보를 추출한다."""
    # UMN 버전 추출 (예: UMNnos1.01, UMN_3.41, UMN_NOS6.06)
    version_match = re.search(
        r"UMN[_\s]?(?:nos|NOS)?[_\s]?(\d+\.\d+[A-Za-z]?)", dir_name
    )
    if version_match:
        return f"UMN {version_match.group(1)}"
    return ""


def _scan_vendor_category(vendor_cat_path: Path) -> list[dict[str, str]]:
    """벤더-카테고리 디렉토리 하위의 장비 모델 정보를 수집한다."""
    models: list[dict[str, str]] = []

    if not vendor_cat_path.is_dir():
        return models

    for entry in sorted(vendor_cat_path.iterdir()):
        # _images 디렉토리 무시
        if entry.name.endswith("_images"):
            continue

        name = entry.name
        # .md 확장자 제거
        if name.endswith(".md"):
            name = name[:-3]

        model = _extract_model_name(name)
        version = _extract_version_info(name)

        models.append({
            "model": model,
            "version": version,
            "name": name,
            "is_dir": str(entry.is_dir()),
        })

    return models


def generate_directory_index(root_path: Path) -> list[Document]:
    """가입자망장비_manual 디렉토리 구조를 분석하여 인덱스 문서를 생성한다.

    Args:
        root_path: 스캔할 루트 경로 (input/ 또는 가입자망장비_manual/).

    Returns:
        합성 인덱스 Document 리스트.
    """
    documents: list[Document] = []

    # 가입자망장비_manual 디렉토리 탐색
    manual_dirs = _find_manual_dirs(root_path)

    for manual_dir in manual_dirs:
        # 벤더-카테고리 디렉토리 순회
        vendor_summaries: list[str] = []

        for entry in sorted(manual_dir.iterdir()):
            if not entry.is_dir():
                continue

            match = _VENDOR_CATEGORY_PATTERN.match(entry.name)
            if not match:
                continue

            vendor = match.group("vendor")
            category = match.group("category")

            # 벤더-카테고리별 인덱스 문서 생성
            models = _scan_vendor_category(entry)
            if models:
                doc = _build_vendor_category_doc(
                    vendor, category, models, entry
                )
                documents.append(doc)

                vendor_summaries.append(
                    f"- {vendor} {category}: {len(models)}개 장비 모델"
                )

        # 최상위 요약 인덱스 문서 생성
        if vendor_summaries:
            top_doc = _build_top_level_doc(vendor_summaries, manual_dir)
            documents.append(top_doc)

    logger.info("디렉토리 인덱스 문서 %d개 생성", len(documents))
    return documents


def _find_manual_dirs(root_path: Path) -> list[Path]:
    """루트 경로에서 가입자망장비_manual 디렉토리를 찾는다."""
    # 루트 자체가 가입자망장비_manual인 경우
    if root_path.name == "가입자망장비_manual":
        return [root_path]

    # 하위에서 탐색
    results = []
    if root_path.is_dir():
        for child in root_path.iterdir():
            if child.is_dir() and child.name == "가입자망장비_manual":
                results.append(child)
    return results


def _build_vendor_category_doc(
    vendor: str,
    category: str,
    models: list[dict[str, str]],
    dir_path: Path,
) -> Document:
    """벤더-카테고리별 합성 인덱스 문서를 생성한다."""
    lines = [
        f"# 가입자망 장비 목록 - {vendor} {category}",
        "",
        f"벤더: {vendor}",
        f"카테고리: {category}",
        f"장비 수: {len(models)}개",
        "",
        "## 장비 모델 목록",
        "",
    ]

    for m in models:
        version = f" ({m['version']})" if m["version"] else ""
        lines.append(f"- {m['model']}{version}")

    content = "\n".join(lines)

    return Document(
        path=dir_path / "__index__.md",
        content=content,
        metadata={
            "doc_type": "directory_index",
            "language": "ko",
            "vendor": vendor,
            "category": category,
        },
    )


def _build_top_level_doc(
    vendor_summaries: list[str],
    manual_dir: Path,
) -> Document:
    """가입자망 전체 요약 인덱스 문서를 생성한다."""
    lines = [
        "# 가입자망 장비 전체 목록",
        "",
        "## 벤더별 카테고리 요약",
        "",
        *vendor_summaries,
    ]

    content = "\n".join(lines)

    return Document(
        path=manual_dir / "__index__.md",
        content=content,
        metadata={
            "doc_type": "directory_index",
            "language": "ko",
        },
    )
