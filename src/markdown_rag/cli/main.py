"""Main CLI entry point for Markdown RAG (mdrag).

Provides subcommands for document ingestion, semantic search,
question answering, status inspection, and API server management.
"""

from __future__ import annotations

import argparse
import sys

from markdown_rag.cli.ask_cmd import handle_ask
from markdown_rag.cli.ingest_cmd import handle_ingest
from markdown_rag.cli.search_cmd import handle_search
from markdown_rag.cli.status_cmd import handle_status


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with all subcommands.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="mdrag",
        description="Markdown RAG - Semantic search and QA for Markdown documents",
    )

    # -- global debug/logging options --
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="디버그 모드 활성화 (DEBUG 레벨 로그 + 라이브러리 경고 표시)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=None,
        help="로그 레벨 지정 (--debug가 없을 때 유효, 기본: WARNING)",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        help="로그를 지정 파일에도 저장 (기본: stderr만 출력)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # -- ingest --
    ingest_parser = subparsers.add_parser(
        "ingest", help="Ingest Markdown documents into the vector store"
    )
    ingest_parser.add_argument("path", help="Path to a .md file or directory to ingest")
    ingest_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show per-file progress"
    )

    # -- search --
    search_parser = subparsers.add_parser(
        "search", help="Semantic search across indexed documents"
    )
    search_parser.add_argument("query", help="Search query string")
    search_parser.add_argument(
        "-k", "--top-k", type=int, default=5, help="Number of results (default: 5)"
    )
    search_parser.add_argument(
        "--backend",
        choices=["local", "openai"],
        default="local",
        help="Embedding backend (default: local)",
    )
    search_parser.add_argument(
        "--doc-type",
        choices=["rfc", "ccie", "telecom_manual"],
        default=None,
        help="Filter by document type",
    )
    search_parser.add_argument(
        "--language",
        choices=["en", "ko"],
        default=None,
        help="Filter by language",
    )
    search_parser.add_argument(
        "--vendor",
        choices=["다산", "유비쿼스"],
        default=None,
        help="Filter by vendor",
    )
    search_parser.add_argument(
        "--category",
        choices=["L2", "L3", "OLT"],
        default=None,
        help="Filter by equipment category",
    )

    # -- ask --
    ask_parser = subparsers.add_parser(
        "ask", help="Ask a question using RAG (OpenAI or local SLM)"
    )
    ask_parser.add_argument("question", help="Question to ask")
    ask_parser.add_argument(
        "-k", "--top-k", type=int, default=5, help="Number of context chunks (default: 5)"
    )
    ask_parser.add_argument(
        "-s", "--show-sources", action="store_true", help="Show source documents"
    )
    ask_parser.add_argument(
        "--model", default=None, help="Model name or path override"
    )
    ask_parser.add_argument(
        "--llm-backend",
        choices=["local", "openai"],
        default=None,
        help="LLM backend (default: from settings)",
    )
    ask_parser.add_argument(
        "--doc-type",
        choices=["rfc", "ccie", "telecom_manual"],
        default=None,
        help="Filter by document type",
    )
    ask_parser.add_argument(
        "--language",
        choices=["en", "ko"],
        default=None,
        help="Filter by language",
    )
    ask_parser.add_argument(
        "--vendor",
        choices=["다산", "유비쿼스"],
        default=None,
        help="Filter by vendor",
    )
    ask_parser.add_argument(
        "--category",
        choices=["L2", "L3", "OLT"],
        default=None,
        help="Filter by equipment category",
    )

    # -- status --
    subparsers.add_parser("status", help="Show index status and configuration")

    # -- serve --
    serve_parser = subparsers.add_parser("serve", help="Start the REST API server")
    serve_parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind (default: 0.0.0.0)"
    )
    serve_parser.add_argument(
        "--port", type=int, default=8900, help="Port to bind (default: 8900)"
    )

    return parser


def handle_serve(args: argparse.Namespace) -> None:
    """Start the FastAPI server with uvicorn.

    Args:
        args: Parsed arguments with host and port.
    """
    try:
        import uvicorn
    except ImportError:
        print("Error: uvicorn is required. Install with: pip install uvicorn", file=sys.stderr)
        sys.exit(1)

    print(f"Starting mdrag API server on {args.host}:{args.port}")
    uvicorn.run(
        "markdown_rag.api.app:create_app",
        host=args.host,
        port=args.port,
        factory=True,
    )


def _suppress_library_warnings(debug: bool = False) -> None:
    """서드파티 라이브러리의 불필요한 경고 메시지를 억제한다.

    Args:
        debug: True이면 라이브러리 로그/경고 억제를 완화하여
            디버깅에 유용한 정보를 볼 수 있도록 한다.
    """
    import logging
    import os
    import warnings

    if debug:
        # 디버그 모드: 라이브러리 로그 살려서 실행 과정 확인 가능하게 함
        os.environ.setdefault("TRANSFORMERS_VERBOSITY", "info")
        os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
        logging.getLogger("huggingface_hub").setLevel(logging.INFO)
        logging.getLogger("sentence_transformers").setLevel(logging.INFO)
        # FutureWarning은 시끄러울 수 있어 기본 억제 유지
        warnings.filterwarnings("ignore", category=FutureWarning)
        return

    # tqdm 진행바 억제 (Loading weights 등)
    os.environ.setdefault("TQDM_DISABLE", "1")

    # transformers 라이브러리 로그 레벨 조정 (LOAD REPORT 억제)
    os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

    # tokenizers 병렬 처리 경고 억제
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    # HuggingFace Hub 인증 경고 억제 (로거 레벨)
    logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

    # sentence-transformers 로그 레벨 조정
    logging.getLogger("sentence_transformers").setLevel(logging.WARNING)

    # FutureWarning 및 HF Hub 인증 경고 필터링
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", module="huggingface_hub.*")


def _configure_logging(
    debug: bool,
    log_level: str | None,
    log_file: str | None,
) -> None:
    """CLI 전역 로깅을 구성한다.

    - ``debug=True``이면 markdown_rag 네임스페이스는 DEBUG 레벨,
      루트(외부 라이브러리)는 INFO 레벨로 설정된다.
    - ``debug=False``이면서 ``log_level``이 주어지면 해당 레벨을
      markdown_rag 네임스페이스에 적용한다.
    - 기본값: WARNING (기존 동작과 동일하게 조용함).

    Args:
        debug: 디버그 모드 on/off.
        log_level: 명시적 로그 레벨 (DEBUG/INFO/WARNING/ERROR/CRITICAL).
        log_file: 로그를 추가로 기록할 파일 경로. 없으면 stderr만 사용.
    """
    import logging
    from pathlib import Path

    if debug:
        pkg_level = logging.DEBUG
        root_level = logging.INFO
    else:
        pkg_level = getattr(logging, log_level, logging.WARNING) if log_level else logging.WARNING
        root_level = logging.WARNING

    if debug or log_level == "DEBUG":
        fmt = "%(asctime)s [%(levelname)-7s] %(name)s:%(lineno)d | %(message)s"
        datefmt = "%H:%M:%S"
    else:
        fmt = "%(levelname)s: %(name)s - %(message)s"
        datefmt = None

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    # 핸들러는 pkg/root 중 더 낮은 레벨까지 받아들여야
    # markdown_rag(DEBUG)와 외부(INFO) 모두 통과시킬 수 있다.
    # 외부 로거는 root_logger.level을 상속받아 자체적으로 필터링된다.
    handler_level = min(pkg_level, root_level)

    root_logger = logging.getLogger()
    # root_logger.level이 외부 라이브러리의 effective level이 된다.
    root_logger.setLevel(root_level)

    # 기존 핸들러 제거 (중복 방지)
    for existing in list(root_logger.handlers):
        root_logger.removeHandler(existing)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(handler_level)
    root_logger.addHandler(stream_handler)

    if log_file:
        log_path = Path(log_file).expanduser()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(handler_level)
        root_logger.addHandler(file_handler)

    # markdown_rag 패키지는 별도 레벨 적용 (DEBUG 등 루트보다 낮은 수준 가능)
    pkg_logger = logging.getLogger("markdown_rag")
    pkg_logger.setLevel(pkg_level)
    pkg_logger.propagate = True

    if debug:
        # 디버그 모드에서도 너무 시끄러운 라이브러리는 WARNING으로 제한
        for noisy in ("urllib3", "httpx", "httpcore", "chromadb.telemetry", "asyncio"):
            logging.getLogger(noisy).setLevel(logging.WARNING)

    if debug:
        pkg_logger.debug(
            "Debug mode enabled: markdown_rag=DEBUG, root=INFO, log_file=%s",
            log_file or "<stderr only>",
        )


def main() -> None:
    """CLI entry point registered as 'mdrag' in pyproject.toml."""
    parser = build_parser()
    args = parser.parse_args()

    debug = getattr(args, "debug", False)
    log_level = getattr(args, "log_level", None)
    log_file = getattr(args, "log_file", None)

    _suppress_library_warnings(debug=debug)
    _configure_logging(debug=debug, log_level=log_level, log_file=log_file)

    if args.command is None:
        parser.print_help()
        sys.exit(2)

    handlers = {
        "ingest": handle_ingest,
        "search": handle_search,
        "ask": handle_ask,
        "status": handle_status,
        "serve": handle_serve,
    }

    handler = handlers.get(args.command)
    if handler is not None:
        handler(args)
    else:
        parser.print_help()
        sys.exit(2)
