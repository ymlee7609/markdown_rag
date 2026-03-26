"""Tests for document metadata detection in ingestion pipeline."""

from __future__ import annotations

from pathlib import Path

import pytest

from markdown_rag.ingest.pipeline import detect_doc_metadata


class TestDetectDocMetadata:
    """Test document type and language detection from file paths."""

    @pytest.mark.parametrize(
        "path,expected_type,expected_lang",
        [
            (Path("input/IETF_RFC/rfc9110.md"), "rfc", "en"),
            (Path("input/IETF_RFC/rfc1.md"), "rfc", "en"),
            (Path("/abs/path/IETF_RFC/rfc4949.md"), "rfc", "en"),
            (Path("input/Cisco_CCIE/CCIE_Vol1/01_intro.md"), "ccie", "en"),
            (Path("input/Cisco_CCIE/CCIE_Vol2/20_bgp.md"), "ccie", "en"),
            (
                Path("input/가입자망장비_manual/다산_L2/section1.md"),
                "telecom_manual",
                "ko",
            ),
            (
                Path("input/가입자망장비_manual/유비쿼스_OLT/guide.md"),
                "telecom_manual",
                "ko",
            ),
        ],
    )
    def test_known_document_types(
        self, path: Path, expected_type: str, expected_lang: str
    ) -> None:
        """알려진 문서 유형이 경로에서 올바르게 감지되어야 한다."""
        result = detect_doc_metadata(path)
        assert result["doc_type"] == expected_type
        assert result["language"] == expected_lang

    def test_unknown_document_type(self) -> None:
        """알 수 없는 경로는 unknown/en으로 반환되어야 한다."""
        result = detect_doc_metadata(Path("random/path/doc.md"))
        assert result["doc_type"] == "unknown"
        assert result["language"] == "en"

    def test_returns_dict_with_correct_keys(self) -> None:
        """결과 딕셔너리에 doc_type과 language 키가 있어야 한다."""
        result = detect_doc_metadata(Path("any/path.md"))
        assert "doc_type" in result
        assert "language" in result


class TestExtractTelecomMetadata:
    """통신 장비 매뉴얼 확장 메타데이터 추출 테스트."""

    @pytest.mark.parametrize(
        "path,expected_vendor,expected_category",
        [
            (
                Path("input/가입자망장비_manual/다산_L2/[V29xxGB]_UMNnos1.01/doc.md"),
                "다산",
                "L2",
            ),
            (
                Path("input/가입자망장비_manual/유비쿼스_OLT/E5924L_SW/guide.md"),
                "유비쿼스",
                "OLT",
            ),
            (
                Path("input/가입자망장비_manual/다산_L3/V5524XG_UMN_3.41/doc.md"),
                "다산",
                "L3",
            ),
        ],
    )
    def test_extracts_vendor_and_category(
        self,
        path: Path,
        expected_vendor: str,
        expected_category: str,
    ) -> None:
        """벤더와 카테고리를 경로에서 올바르게 추출해야 한다."""
        result = detect_doc_metadata(path)
        assert result["vendor"] == expected_vendor
        assert result["category"] == expected_category

    def test_extracts_model_name(self) -> None:
        """모델명을 경로에서 추출해야 한다."""
        path = Path(
            "input/가입자망장비_manual/다산_L2/[V29xxGB]_UMNnos1.01/doc.md"
        )
        result = detect_doc_metadata(path)
        assert "model_name" in result
        assert result["model_name"] == "V29xxGB"

    def test_no_telecom_metadata_for_rfc(self) -> None:
        """RFC 문서에는 벤더/카테고리가 없어야 한다."""
        result = detect_doc_metadata(Path("input/IETF_RFC/rfc9110.md"))
        assert "vendor" not in result
        assert "category" not in result
