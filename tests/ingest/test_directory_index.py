"""디렉토리 인덱스 문서 생성 테스트."""

from __future__ import annotations

from pathlib import Path

import pytest

from markdown_rag.ingest.directory_index import (
    _extract_model_name,
    _extract_version_info,
    _scan_vendor_category,
    generate_directory_index,
)


class TestExtractModelName:
    """장비 모델명 추출 테스트."""

    @pytest.mark.parametrize(
        "dir_name,expected",
        [
            ("[V29xxGB]_UMNnos1.01_KO_200423_V1", "V29xxGB"),
            ("[V27xxGB_LGU]_UMNnos1.28_KO_141203_V1", "V27xxGB_LGU"),
            ("_V2708M__UMNnos1.01_KO_180312_V1.0", "V2708M"),
            ("_V3024V__UMNnos1.01_KO_190926_V1.0", "V3024V"),
            ("V5524XG_UMN_3.41_KO_080811", "V5524XG"),
            ("E5924LB_SW_User Guide", "E5924LB"),
            ("E57xxRC_SW_User Guide", "E57xxRC"),
        ],
    )
    def test_extracts_model_from_dir_names(
        self, dir_name: str, expected: str
    ) -> None:
        """다양한 디렉토리 명명 패턴에서 모델명을 추출해야 한다."""
        assert _extract_model_name(dir_name) == expected


class TestExtractVersionInfo:
    """버전 정보 추출 테스트."""

    @pytest.mark.parametrize(
        "dir_name,expected",
        [
            ("[V29xxGB]_UMNnos1.01_KO_200423_V1", "UMN 1.01"),
            ("V5524XG_UMN_3.41_KO_080811", "UMN 3.41"),
            ("[V8500M]_UMN_NOS6.06_KO_190822_V1.0", "UMN 6.06"),
            ("E5924LB_SW_User Guide", ""),
        ],
    )
    def test_extracts_version_info(
        self, dir_name: str, expected: str
    ) -> None:
        """버전 정보를 올바르게 추출해야 한다."""
        assert _extract_version_info(dir_name) == expected


class TestScanVendorCategory:
    """벤더-카테고리 디렉토리 스캔 테스트."""

    def test_scans_directory_contents(self, tmp_path: Path) -> None:
        """디렉토리 내 장비 정보를 수집해야 한다."""
        vendor_dir = tmp_path / "다산_L2"
        vendor_dir.mkdir()

        # 서브디렉토리와 파일 생성
        (vendor_dir / "[V29xxGB]_UMNnos1.01_KO").mkdir()
        (vendor_dir / "_V3024V__UMNnos1.01_KO.md").write_text("test")

        models = _scan_vendor_category(vendor_dir)
        assert len(models) == 2

    def test_skips_images_directories(self, tmp_path: Path) -> None:
        """_images 디렉토리를 무시해야 한다."""
        vendor_dir = tmp_path / "다산_L2"
        vendor_dir.mkdir()
        (vendor_dir / "[V29xxGB]_UMNnos1.01_KO").mkdir()
        (vendor_dir / "[V29xxGB]_UMNnos1.01_KO_images").mkdir()

        models = _scan_vendor_category(vendor_dir)
        assert len(models) == 1

    def test_returns_empty_for_missing_dir(self, tmp_path: Path) -> None:
        """존재하지 않는 디렉토리에 대해 빈 리스트를 반환해야 한다."""
        models = _scan_vendor_category(tmp_path / "nonexistent")
        assert models == []


class TestGenerateDirectoryIndex:
    """디렉토리 인덱스 문서 생성 통합 테스트."""

    def _create_telecom_structure(self, root: Path) -> Path:
        """테스트용 가입자망장비_manual 디렉토리 구조 생성."""
        manual_dir = root / "가입자망장비_manual"
        manual_dir.mkdir()

        # 다산_L2
        dasan_l2 = manual_dir / "다산_L2"
        dasan_l2.mkdir()
        (dasan_l2 / "[V29xxGB]_UMNnos1.01_KO").mkdir()
        (dasan_l2 / "_V3024V__UMNnos1.01_KO.md").write_text("test")

        # 유비쿼스_OLT
        ubiquoss_olt = manual_dir / "유비쿼스_OLT"
        ubiquoss_olt.mkdir()
        (ubiquoss_olt / "E5924L_SW_User Guide").mkdir()

        return root

    def test_generates_vendor_category_docs(self, tmp_path: Path) -> None:
        """벤더-카테고리별 인덱스 문서가 생성되어야 한다."""
        root = self._create_telecom_structure(tmp_path)
        docs = generate_directory_index(root)

        # 다산_L2 + 유비쿼스_OLT + 최상위 요약 = 3개
        assert len(docs) == 3

    def test_vendor_category_doc_content(self, tmp_path: Path) -> None:
        """벤더-카테고리 인덱스 문서 내용이 올바라야 한다."""
        root = self._create_telecom_structure(tmp_path)
        docs = generate_directory_index(root)

        # 다산_L2 문서 찾기
        dasan_docs = [
            d for d in docs
            if d.metadata.get("vendor") == "다산"
            and d.metadata.get("category") == "L2"
        ]
        assert len(dasan_docs) == 1

        doc = dasan_docs[0]
        assert "다산 L2" in doc.content
        assert "장비 모델 목록" in doc.content
        assert doc.metadata["doc_type"] == "directory_index"
        assert doc.metadata["language"] == "ko"

    def test_top_level_summary(self, tmp_path: Path) -> None:
        """최상위 요약 인덱스 문서가 생성되어야 한다."""
        root = self._create_telecom_structure(tmp_path)
        docs = generate_directory_index(root)

        top_docs = [
            d for d in docs
            if "vendor" not in d.metadata and d.metadata.get("doc_type") == "directory_index"
        ]
        assert len(top_docs) == 1
        assert "가입자망 장비 전체 목록" in top_docs[0].content

    def test_no_index_for_non_manual_dirs(self, tmp_path: Path) -> None:
        """가입자망장비_manual이 아닌 디렉토리에서는 문서가 생성되지 않아야 한다."""
        other_dir = tmp_path / "other_docs"
        other_dir.mkdir()
        (other_dir / "readme.md").write_text("test")

        docs = generate_directory_index(tmp_path)
        assert len(docs) == 0

    def test_direct_manual_dir(self, tmp_path: Path) -> None:
        """가입자망장비_manual 디렉토리를 직접 지정해도 동작해야 한다."""
        root = self._create_telecom_structure(tmp_path)
        manual_dir = root / "가입자망장비_manual"
        docs = generate_directory_index(manual_dir)

        # 다산_L2 + 유비쿼스_OLT + 최상위 = 3개
        assert len(docs) == 3

    def test_index_doc_path_uses_virtual_path(self, tmp_path: Path) -> None:
        """인덱스 문서의 경로가 __index__.md를 사용해야 한다."""
        root = self._create_telecom_structure(tmp_path)
        docs = generate_directory_index(root)

        for doc in docs:
            assert doc.path.name == "__index__.md"
