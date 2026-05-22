"""Ontology-augmented hybrid search.

OntologyAugmentedSearch wraps two HybridSearch engines:
  1. main_search  — over the primary corpus (e.g. input_optimized)
  2. onto_search  — over the auxiliary ontology corpus (e.g. input_ontology)

On every query it:
  1. Runs both engines (fetch_k each)
  2. Merges with RRF (reciprocal rank fusion)
  3. Detects ontology-card hits in the merged top results
  4. Loads the cards' referenced injectable paths from onto_refs.json
  5. Looks up the corresponding chunks in the main vector store and injects
     them into the result list with a configurable boost score
  6. Attaches `referenced_paths` / `via_onto_card` / `directory_hints` metadata
     to ontology-card SearchResults so callers (LLM RAG, UI) can render them

The class exposes the same `search(query, top_k, where=None)` signature as
HybridSearch, so it is a drop-in replacement when ontology augmentation is
desired.

Build prerequisite: `scripts/build_ontology_refs.py` must have generated
`data/ontology/onto_refs.json` from input_ontology/ frontmatter.
"""

from __future__ import annotations

import json
import logging
from dataclasses import replace
from pathlib import Path
from typing import Any

from markdown_rag.models import Chunk, SearchResult
from markdown_rag.retriever.hybrid import HybridSearch
from markdown_rag.store.chroma import ChromaStore

logger = logging.getLogger(__name__)

_RRF_K = 60


class OntologyAugmentedSearch:
    """Hybrid search augmented with an ontology side corpus.

    Args:
        main_search: HybridSearch over the primary corpus.
        onto_search: HybridSearch over the ontology auxiliary corpus.
        main_store:  ChromaStore for the primary corpus (used to look up
                     injected chunks by their doc_path).
        onto_refs_path: Path to the JSON produced by build_ontology_refs.py.
        inject_top_n_cards: How many top ontology-card hits to expand
                            (default 3). Higher = more recall but more chunks.
        inject_chunks_per_card: How many chunks per referenced path to inject
                                (default 1, which is doc_path's first chunk).
                                Capped by Chroma get() pagination.
        inject_score_boost: Score assigned to injected chunks. Should be
                            comparable to the smallest RRF score so they
                            appear in the result list without dominating.
    """

    def __init__(
        self,
        main_search: HybridSearch,
        onto_search: HybridSearch,
        main_store: ChromaStore,
        onto_refs_path: Path | str,
        inject_top_n_cards: int = 3,
        inject_chunks_per_card: int = 1,
        inject_score_boost: float = 1.0 / (_RRF_K + 1),
    ) -> None:
        self.main_search = main_search
        self.onto_search = onto_search
        self.main_store = main_store
        self.inject_top_n_cards = inject_top_n_cards
        self.inject_chunks_per_card = inject_chunks_per_card
        self.inject_score_boost = inject_score_boost
        self._onto_refs = self._load_refs(Path(onto_refs_path))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        """Run augmented search and return top_k SearchResult."""
        fetch_k = top_k * 3
        main_results = self.main_search.search(query, top_k=fetch_k, where=where)
        onto_results = self.onto_search.search(query, top_k=fetch_k)

        fused = self._rrf_union(main_results, onto_results, top_k=fetch_k)
        with_meta = self._annotate_onto_cards(fused)
        injected = self._inject_referenced_chunks(with_meta)
        return injected[:top_k]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_refs(path: Path) -> dict[str, dict[str, list[str]]]:
        if not path.exists():
            logger.warning("onto_refs.json not found at %s — ontology expansion disabled", path)
            return {}
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("refs", {})

    @staticmethod
    def _rrf_union(
        main: list[SearchResult],
        onto: list[SearchResult],
        top_k: int,
        k_const: int = _RRF_K,
    ) -> list[SearchResult]:
        """Fuse two result lists with RRF; preserve original SearchResult.chunk."""
        scored: dict[str, tuple[SearchResult, float]] = {}
        for rank, r in enumerate(main, start=1):
            key = r.chunk.chunk_id
            scored[key] = (r, 1.0 / (k_const + rank))
        for rank, r in enumerate(onto, start=1):
            key = r.chunk.chunk_id
            inc = 1.0 / (k_const + rank)
            if key in scored:
                existing, sc = scored[key]
                scored[key] = (existing, sc + inc)
            else:
                scored[key] = (r, inc)
        ranked = sorted(scored.values(), key=lambda x: -x[1])[:top_k]
        out: list[SearchResult] = []
        for new_rank, (r, sc) in enumerate(ranked, start=1):
            out.append(SearchResult(chunk=r.chunk, score=sc, rank=new_rank))
        return out

    def _ref_entry(self, doc_path: str) -> dict[str, list[str]] | None:
        """Lookup onto_refs entry by doc_path (abs or rel keys both supported)."""
        if doc_path in self._onto_refs:
            return self._onto_refs[doc_path]
        # Try project-root-relative form
        try:
            rel = str(Path(doc_path).resolve().relative_to(Path.cwd()))
            if rel in self._onto_refs:
                return self._onto_refs[rel]
        except (ValueError, OSError):
            pass
        return None

    def _annotate_onto_cards(self, results: list[SearchResult]) -> list[SearchResult]:
        """Attach via_onto_card / referenced_paths / directory_hints to onto-card chunks."""
        annotated: list[SearchResult] = []
        for r in results:
            entry = self._ref_entry(str(r.chunk.doc_path))
            if entry is None:
                annotated.append(r)
                continue
            new_meta = dict(r.chunk.metadata or {})
            new_meta["via_onto_card"] = True
            new_meta["referenced_paths_injectable"] = list(entry.get("injectable", []))
            new_meta["referenced_paths_directories"] = list(entry.get("directory_hints", []))
            new_chunk = replace(r.chunk, metadata=new_meta)
            annotated.append(SearchResult(chunk=new_chunk, score=r.score, rank=r.rank))
        return annotated

    def _inject_referenced_chunks(
        self,
        fused: list[SearchResult],
    ) -> list[SearchResult]:
        """For top-N onto-card hits, look up their referenced chunks in main store."""
        existing_ids = {r.chunk.chunk_id for r in fused}
        existing_doc_paths = {str(r.chunk.doc_path) for r in fused}

        # Pick top-N ontology cards (already RRF-ordered)
        onto_hits: list[SearchResult] = [
            r for r in fused if r.chunk.metadata and r.chunk.metadata.get("via_onto_card")
        ][: self.inject_top_n_cards]

        if not onto_hits:
            return fused

        injected_chunks: list[tuple[Chunk, int]] = []  # (chunk, src_rank)
        for src_idx, card_hit in enumerate(onto_hits):
            ref_paths = (card_hit.chunk.metadata or {}).get(
                "referenced_paths_injectable", []
            )
            via_id = Path(str(card_hit.chunk.doc_path)).name
            for ref_path in ref_paths:
                # Skip if a chunk of this doc already in results
                if ref_path in existing_doc_paths:
                    continue
                chunks = self._lookup_chunks_by_doc(
                    ref_path, limit=self.inject_chunks_per_card
                )
                for c in chunks:
                    if c.chunk_id in existing_ids:
                        continue
                    existing_ids.add(c.chunk_id)
                    # Tag chunk with provenance
                    new_meta = dict(c.metadata or {})
                    new_meta["injected_by_onto_card"] = via_id
                    tagged = replace(c, metadata=new_meta)
                    injected_chunks.append((tagged, src_idx))

        # Build new combined list:
        # original fused (in order) + injected (assigned a boosted score so
        # they appear within top_k but never above original direct hits)
        boost = self.inject_score_boost
        injected_results: list[SearchResult] = []
        for inj_idx, (chunk, src_idx) in enumerate(injected_chunks):
            # Earlier ontology source → slightly higher score
            score = boost * (1.0 - 0.01 * src_idx) - 1e-6 * inj_idx
            injected_results.append(SearchResult(chunk=chunk, score=score, rank=0))

        # Combine and re-rank by score descending
        all_results = list(fused) + injected_results
        all_results.sort(key=lambda r: r.score, reverse=True)
        # Re-assign ranks 1..N
        for i, r in enumerate(all_results, start=1):
            r.rank = i
        return all_results

    def _lookup_chunks_by_doc(self, doc_path: str, limit: int) -> list[Chunk]:
        """Fetch chunks from main_store filtered by exact doc_path match.

        Returns at most `limit` chunks, ordered by chunk_index ascending.
        """
        try:
            existing = self.main_store._collection.get(  # noqa: SLF001
                where={"doc_path": doc_path},
                include=["documents", "metadatas"],
                limit=max(limit * 4, 4),  # over-fetch a bit then trim
            )
        except Exception as e:  # noqa: BLE001
            logger.debug("onto chunk lookup failed for %s: %s", doc_path, e)
            return []
        if not existing or not existing.get("ids"):
            return []
        ids = existing.get("ids") or []
        metas = existing.get("metadatas") or []
        docs = existing.get("documents") or []
        items: list[tuple[int, Chunk]] = []
        for i in range(len(ids)):
            meta = metas[i] if i < len(metas) and metas[i] else {}
            content = docs[i] if i < len(docs) and docs[i] else ""
            raw_idx = meta.get("chunk_index", 0)
            try:
                idx = int(raw_idx) if isinstance(raw_idx, (int, float, str)) else 0
            except (TypeError, ValueError):
                idx = 0
            headers_raw = meta.get("headers", "")
            headers_str = headers_raw if isinstance(headers_raw, str) else ""
            headers = headers_str.split("|||") if headers_str else []
            stored_dp = meta.get("doc_path", doc_path)
            if not isinstance(stored_dp, str):
                stored_dp = doc_path
            chunk = Chunk(
                content=str(content),
                doc_path=Path(stored_dp),
                headers=headers,
                chunk_index=idx,
                metadata={k: v for k, v in meta.items()
                          if k not in ("doc_path", "headers", "chunk_index")},
            )
            items.append((idx, chunk))
        items.sort(key=lambda x: x[0])
        return [c for _, c in items[:limit]]

    # ------------------------------------------------------------------
    # Introspection helpers (useful for debugging / RAG prompt building)
    # ------------------------------------------------------------------

    def explain(self, results: list[SearchResult]) -> list[dict[str, Any]]:
        """Return a serializable trace of each result's provenance."""
        out: list[dict[str, Any]] = []
        for r in results:
            meta = r.chunk.metadata or {}
            entry: dict[str, Any] = {
                "doc_path": str(r.chunk.doc_path),
                "chunk_index": r.chunk.chunk_index,
                "score": r.score,
                "rank": r.rank,
            }
            if meta.get("via_onto_card"):
                entry["origin"] = "ontology_card"
                entry["referenced_paths_injectable"] = meta.get(
                    "referenced_paths_injectable", []
                )
                entry["referenced_paths_directories"] = meta.get(
                    "referenced_paths_directories", []
                )
            elif meta.get("injected_by_onto_card"):
                entry["origin"] = "injected"
                entry["injected_by_onto_card"] = meta["injected_by_onto_card"]
            else:
                entry["origin"] = "main_search"
            out.append(entry)
        return out
