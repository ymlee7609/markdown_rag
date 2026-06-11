# Markdown RAG

[한국어](README.ko.md)

Semantic search and QA system for internal Markdown documents with multilingual support, metadata filtering, and hybrid search.

## Features

- **Multilingual embeddings**: Korean + English support with `intfloat/multilingual-e5-small`
- **Metadata filtering**: Auto-classify documents by type (rfc/ccie/telecom_manual) and language
- **Hybrid search**: BM25 keyword + vector similarity with Reciprocal Rank Fusion (RRF)
- **Cross-encoder reranking**: Optional reranking with multilingual `BAAI/bge-reranker-v2-m3`
- **Batch ingestion**: Optimized for 27,000+ files with batch embedding and bulk upsert
- **HyDE query processing**: Hypothetical Document Embeddings with adjacent chunk expansion (optional module, not wired into the default pipeline)
- **Ontology-augmented search**: Auxiliary corpus (`input_ontology/`) + referenced-path
  auto-expansion. Lifts CCIE Hit@5 from 60% to 100%, overall Hit@5 from 88% to 100%
  on the 100-case validation set (see Phase 7 below).
- **Search mode** (LLM-free): Semantic/hybrid/ontology search using local embeddings
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

# Hybrid search (BM25 + vector, RRF fusion)
mdrag search "authentication" --mode hybrid

# Ontology-augmented search (auxiliary corpus + referenced-path expansion)
mdrag search "OSPF area" --mode ontology

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
| POST | `/api/v1/search` | Search (vector/hybrid/ontology) |
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
| `MDRAG_SEARCH_MODE` | `vector` | Search mode (`vector` / `hybrid` / `ontology`; `bm25` falls back to vector with a warning) |
| `MDRAG_HYBRID_ALPHA` | `0.7` | Vector weight in hybrid search (0.0-1.0) |
| `MDRAG_BM25_INDEX_PATH` | `./data/bm25_index.pkl` | BM25 index path |
| `MDRAG_RERANK_ENABLED` | `false` | Enable cross-encoder reranking |
| `MDRAG_RERANK_MODEL` | `BAAI/bge-reranker-v2-m3` | Reranker model |
| `MDRAG_INITIAL_TOP_K` | `20` | Candidates for reranking |
| `MDRAG_CHUNK_MAX_SIZE` | `1000` | Max chunk size (characters) |
| `MDRAG_CHUNK_OVERLAP` | `100` | Chunk overlap size (characters) |
| `MDRAG_SEARCH_TOP_K` | `5` | Number of search results |
| `MDRAG_API_PORT` | `8900` | API server port |

### Ontology Augmentation (Phase 7)

Used when `MDRAG_SEARCH_MODE=ontology` or `--mode ontology`.

| Variable | Default | Description |
|----------|---------|-------------|
| `MDRAG_ONTO_CHROMA_PATH` | `./data/chroma_ontology` | Auxiliary corpus ChromaDB path |
| `MDRAG_ONTO_COLLECTION_NAME` | `markdown_docs_ontology` | Auxiliary collection name |
| `MDRAG_ONTO_BM25_PATH` | `./data/bm25_ontology` | Auxiliary BM25 index |
| `MDRAG_ONTO_REFS_PATH` | `./data/ontology/onto_refs.json` | Card → referenced-paths mapping |
| `MDRAG_ONTO_INJECT_TOP_N_CARDS` | `3` | Inject from top-N ontology card hits |
| `MDRAG_ONTO_INJECT_CHUNKS_PER_CARD` | `1` | Main-corpus chunks injected per card |

## Architecture

```
Ingestion:  Markdown files → Parser → Chunker → Embedding → ChromaDB + BM25 Index
Search:     Query → [Vector Search + BM25] → RRF Fusion → Reranking → Results
RAG:        Query → Search → Context Assembly → LLM → Answer
            (HyDE / adjacent-chunk expansion available as optional modules)
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
| bm25s | >= 0.3.5 | BM25 keyword search (sparse-matrix, low memory) |
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

## Ontology-Augmented Search (Phase 7)

For a ~12,000-document corpus spanning IETF RFCs (11,449), Cisco CCIE (103) and
Korean telco subscriber-network manuals (579 by Dasan/Ubiquoss), cross-corpus
retrieval ("standard ↔ theory ↔ CLI implementation") is hard. An **auxiliary
ontology corpus** is added on top of the main hybrid retriever to solve this.

### Measured impact (100-case validation set)

| Metric | baseline (hybrid) | **ontology mode** | Δ |
|--------|---|---|---|
| Passed | 86 | **98** | **+12** |
| Hit@5 (overall) | 88 | **100** | **+12** |
| **Hit@5 (CCIE)** | **18/30 (60%)** | **30/30 (100%)** | **+40 pp** |
| MRR | 0.856 | 0.893 | +0.037 |
| Avg latency | 1538 ms | 1893 ms | +355 ms |

### Layout

```
input_ontology/                 # Auxiliary corpus (68 cards)
├── schema/
│   ├── entity_types.yaml       # 8 types: Protocol / RFC / Concept / Feature / ...
│   ├── relation_types.yaml     # 17 relations: defined_by / extends / implements / ...
│   └── alias_dictionary.yaml   # EN + KO alias seeds
├── protocols/   # OSPF, BGP, STP, VLAN, DHCP, IGMP, ACL, GPON, ... (18)
├── concepts/    # ospf-area, bgp-as-path, vlan-trunk, ... (15)
├── rfcs/        # 2328, 4271, 8200, 5905, ... (15)
├── standards/   # IEEE 802.1D/Q, ITU-T G.984 (3)
├── features/    # mac-address-table, port-mirroring, ... (7)
├── vendors/     # dasan, ubiquoss (2)
└── devices/     # V3024V, V8500, U9532H, P8624, ... (8)

data/ontology/
├── onto_refs.json              # Card → referenced main-corpus paths
├── index.json                  # Entity ID → card file
├── alias_index.json            # Alias → canonical ID reverse index
└── chunk_enrichment.jsonl.gz   # 515K main-corpus chunks tagged with onto candidates
```

### How `--mode ontology` works

1. **Dual hybrid search**: query both `chroma_optimized` (main) and
   `chroma_ontology` (auxiliary) collections.
2. **RRF union**: fuse both result lists by Reciprocal Rank Fusion.
3. **Referenced-path injection**: for each top-N ontology-card hit, look up the
   card's `taught_in`/`documented_in`/`corpus_paths` frontmatter fields and
   inject the corresponding chunks from the main store.
4. **Origin tagging on results**: `[ONTO CARD]` (card itself),
   `[INJECTED via <card>]` (auto-injected chunk), or unmarked (direct main hit).

### Build / re-index

After adding or editing cards:

```bash
# 1. Rebuild auxiliary Chroma + BM25
python scripts/reindex_optimized.py --input input_ontology \
  --chroma-path data/chroma_ontology \
  --collection markdown_docs_ontology \
  --bm25-path data/bm25_ontology

# 2. Regenerate onto_refs.json
python scripts/build_ontology_refs.py

# 3. (optional) Stage 1 deterministic extraction over the main corpus
python scripts/extract_onto_candidates.py
#   → data/ontology/chunk_enrichment.jsonl.gz (515K rows, ~2 min)

# 4. Validate
python scripts/validate_rag.py --ontology-mode ontology
```

### Authoring a card

Each card = YAML frontmatter + Markdown body. Required fields per type are in
`input_ontology/schema/entity_types.yaml`.

Example `input_ontology/protocols/proto-ospf.md`:

```yaml
---
id: proto:ospf
type: Protocol
name_en: OSPF
name_ko: 개방형 최단 경로 우선
layer: L3
defined_by: [rfc:2328]
related: [proto:isis, concept:ospf-lsa, concept:ospf-area]
taught_in:
  - "Cisco_CCIE/CCIE_Vol1/04_part-ii-ip-networking__sec-03.md"
documented_in:
  - "가입자망장비_manual/다산_L3"
keywords_en: [LSA, area, ABR, ASBR, hello, DR, BDR]
source: human
---
```

Full schema in `input_ontology/schema/README.md`; build history and ablation
details in `reports/ontology/m3cde_m4_final_report.md`.

## License

MIT
