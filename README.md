# Markdown RAG

[한국어](README.ko.md)

Semantic search and QA system for internal Markdown documents with multilingual support, metadata filtering, and hybrid search.

## Features

- **Multilingual embeddings**: Korean + English support with `intfloat/multilingual-e5-small`
- **Metadata filtering**: Auto-classify documents by type (rfc/ccie/telecom_manual) and language
- **Hybrid search**: BM25 keyword + vector similarity with Reciprocal Rank Fusion (RRF)
- **Cross-encoder reranking**: Optional reranking with multilingual `BAAI/bge-reranker-v2-m3`
- **Batch ingestion**: Optimized for 27,000+ files with batch embedding and bulk upsert
- **HyDE query processing**: Hypothetical Document Embeddings with adjacent chunk expansion
- **Search mode** (LLM-free): Semantic/keyword/hybrid search using local embeddings
- **Ask mode** (Full RAG): Question answering with OpenAI GPT or local SLM
- **CLI + REST API**: Both command-line and HTTP API support
- **Structure-aware chunking**: Document splitting based on Markdown header hierarchy

## Requirements

- Python 3.11+
- OpenAI API key (for OpenAI backend) or GGUF model file (for local SLM)

## Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install (with dev dependencies)
pip install -e ".[dev]"

# Set up environment variables
cp .env.example .env
```

## Usage

### CLI

```bash
# Ingest documents (batch optimized)
mdrag ingest ./docs/

# Semantic search (no LLM required)
mdrag search "authentication"

# Keyword search (BM25)
mdrag search "authentication" --search-mode bm25

# Hybrid search (BM25 + vector)
mdrag search "authentication" --search-mode hybrid

# Filter by document type
mdrag search "authentication" --doc-type rfc

# Filter by language
mdrag search "인증" --language ko

# Question answering - OpenAI (default)
mdrag ask "How does authentication work?"

# Question answering - Local SLM (GGUF model)
mdrag ask "How does authentication work?" --llm-backend local

# Check ingestion status
mdrag status
```

### REST API Server

```bash
mdrag serve
```

Default port: `8900`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/status` | Ingestion status |
| POST | `/api/v1/ingest` | Ingest documents |
| POST | `/api/v1/search` | Search (vector/bm25/hybrid) |
| POST | `/api/v1/ask` | RAG question answering |
| DELETE | `/api/v1/documents` | Delete documents |

## Configuration

Configure via environment variables (`MDRAG_` prefix) or `.env` file.

| Variable | Default | Description |
|----------|---------|-------------|
| `MDRAG_EMBEDDING_BACKEND` | `local` | Embedding backend (`local` / `openai`) |
| `MDRAG_LOCAL_MODEL` | `intfloat/multilingual-e5-small` | Local embedding model (multilingual, 384-dim) |
| `MDRAG_LLM_BACKEND` | `openai` | LLM backend (`openai` / `local`) |
| `MDRAG_OPENAI_LLM_MODEL` | `gpt-4o-mini` | OpenAI LLM model |
| `MDRAG_LOCAL_LLM_MODEL_PATH` | | GGUF model file path |
| `MDRAG_LOCAL_LLM_CONTEXT_SIZE` | `4096` | Local LLM context size |
| `MDRAG_LOCAL_LLM_MAX_TOKENS` | `1024` | Local LLM max generation tokens |
| `MDRAG_CHROMA_PATH` | `./data/chroma` | ChromaDB storage path |
| `MDRAG_SEARCH_MODE` | `vector` | Search mode (`vector` / `bm25` / `hybrid`) |
| `MDRAG_HYBRID_ALPHA` | `0.7` | Vector weight in hybrid search (0.0-1.0) |
| `MDRAG_BM25_INDEX_PATH` | `./data/bm25_index.pkl` | BM25 index path |
| `MDRAG_RERANK_ENABLED` | `false` | Enable cross-encoder reranking |
| `MDRAG_RERANK_MODEL` | `BAAI/bge-reranker-v2-m3` | Reranker model |
| `MDRAG_INITIAL_TOP_K` | `20` | Candidates for reranking |
| `MDRAG_CHUNK_MAX_SIZE` | `1000` | Max chunk size (characters) |
| `MDRAG_CHUNK_OVERLAP` | `100` | Chunk overlap size (characters) |
| `MDRAG_SEARCH_TOP_K` | `5` | Number of search results |
| `MDRAG_API_PORT` | `8900` | API server port |

## Architecture

```
Ingestion:  Markdown files → Parser → Chunker → Embedding → ChromaDB + BM25 Index
Search:     Query → [Vector Search + BM25] → RRF Fusion → Reranking → Results
RAG:        Query → [HyDE] → Search → Context + Adjacent Chunks → LLM → Answer
```

### Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| chromadb | >= 1.5 | Vector database |
| sentence-transformers | >= 5.0 | Multilingual embeddings |
| openai | >= 2.29 | LLM and embedding API |
| llama-cpp-python | >= 0.3 | Local SLM (GGUF, CPU) |
| markdown-it-py | >= 4.0 | Markdown AST parsing |
| fastapi | >= 0.135 | REST API framework |
| pydantic | >= 2.12 | Data validation |
| rank-bm25 | >= 0.2.2 | BM25 keyword search |
| kiwipiepy | >= 0.18 | Korean morphological analysis |
| tqdm | >= 4.60 | Progress display |

## Development

```bash
# Run tests
pytest tests/ -v

# Check coverage (minimum 85%)
pytest tests/ --cov=markdown_rag --cov-report=term-missing

# Lint
ruff check src/ tests/
```

## License

MIT
