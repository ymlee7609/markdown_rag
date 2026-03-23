# Getting Started

This is a sample document for testing.

## Installation

Run the following command:

```bash
pip install markdown-rag
```

## Configuration

Set up your environment:

```yaml
embedding: local
model: all-MiniLM-L6-v2
```

### Advanced Settings

You can customize the chunk size and overlap.

| Setting | Default | Description |
|---------|---------|-------------|
| chunk_max_size | 1000 | Maximum chunk size in characters |
| chunk_overlap | 100 | Overlap between chunks |

## Usage

### Search Mode

Use the search command for LLM-free semantic search:

```bash
mdrag search "authentication"
```

### Ask Mode

Use the ask command for full RAG:

```bash
mdrag ask "How does auth work?"
```
