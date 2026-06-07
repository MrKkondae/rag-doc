from __future__ import annotations

from functools import lru_cache
import logging
from typing import Literal

import numpy as np
from mcp.server.fastmcp import FastMCP
from sentence_transformers import SentenceTransformer

from scripts.search_chunks import BASE_DIR, build_query_text, cosine_search, load_embedding_store


mcp = FastMCP("egov-rag")

SOURCE_CHOICES = ("migration", "rte43")
DEFAULT_SOURCE: Literal["migration", "rte43"] = "migration"
DEFAULT_TOP_K = 5
LOG_FILE = BASE_DIR / "logs" / "egov-rag-mcp.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
LOGGER = logging.getLogger("egov_rag_mcp")
LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False

if not LOGGER.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    LOGGER.addHandler(file_handler)


@lru_cache(maxsize=len(SOURCE_CHOICES))
def get_embedding_store(source: str) -> dict:
    embedding_file = BASE_DIR / "embeddings" / f"{source}_embeddings.pkl"
    LOGGER.info("loading embedding store source=%s file=%s", source, embedding_file)
    return load_embedding_store(embedding_file)


@lru_cache(maxsize=4)
def get_model(model_name: str) -> SentenceTransformer:
    LOGGER.info("loading sentence transformer model=%s", model_name)
    return SentenceTransformer(model_name)


def format_result(rank: int, score: float, chunk: dict) -> str:
    title = chunk.get("document_title", "") or ""
    source_file = chunk.get("source_file", "") or ""
    url = chunk.get("source_url") or chunk.get("url") or ""
    heading = chunk.get("heading", "") or ""
    content = chunk.get("content", "") or ""

    return "\n".join(
        [
            f"[RAG_RESULT_{rank}]",
            f"title: {title}",
            f"source_file: {source_file}",
            f"url: {url}",
            f"score: {score:.4f}",
            f"heading: {heading}",
            "content:",
            content,
            f"[/RAG_RESULT_{rank}]",
        ]
    )


def search_chunks_text(
    query: str,
    source: Literal["migration", "rte43"] = DEFAULT_SOURCE,
    top_k: int = DEFAULT_TOP_K,
) -> str:
    LOGGER.info("search_chunks_text called query=%r source=%s top_k=%s", query, source, top_k)

    if source not in SOURCE_CHOICES:
        allowed = ", ".join(SOURCE_CHOICES)
        raise ValueError(f"source must be one of: {allowed}")

    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    data = get_embedding_store(source)
    model_name = data["model_name"]
    chunks = data["chunks"]
    embeddings = np.asarray(data["embeddings"], dtype=np.float32)

    model = get_model(model_name)
    query_text = build_query_text(query)

    query_embedding = model.encode(
        query_text,
        normalize_embeddings=True,
    )
    query_embedding = np.asarray(query_embedding, dtype=np.float32)

    results = cosine_search(query_text, query_embedding, embeddings, chunks, top_k)
    LOGGER.info("search completed source=%s result_count=%s", source, len(results))

    if not results:
        return "\n".join(
            [
                "[RAG_RESULT_1]",
                "title:",
                "source_file:",
                "url:",
                "score:",
                "heading:",
                "content:",
                "No results found.",
                "[/RAG_RESULT_1]",
            ]
        )

    return "\n\n".join(
        format_result(rank, final_score, chunks[idx])
        for rank, (idx, _vector_score, _boost, final_score) in enumerate(results, start=1)
    )


@mcp.tool(name="search_egov_rag")
def search_egov_rag(
    query: str,
    source: Literal["migration", "rte43"] = DEFAULT_SOURCE,
    top_k: int = DEFAULT_TOP_K,
) -> str:
    """
    Search eGovFrame RAG chunks and return text-only formatted results.

    Args:
        query: Search query text.
        source: Knowledge source to search. One of migration or rte43.
        top_k: Number of results to return.
    """
    try:
        return search_chunks_text(query=query, source=source, top_k=top_k)
    except Exception as exc:
        LOGGER.exception(
            "search_egov_rag failed query=%r source=%s top_k=%s",
            query,
            source,
            top_k,
        )
        return "\n".join(
            [
                "[RAG_RESULT_1]",
                "title:",
                "source_file:",
                "url:",
                "score:",
                "heading:",
                "content:",
                f"ERROR: {type(exc).__name__}: {exc}",
                "[/RAG_RESULT_1]",
            ]
        )


if __name__ == "__main__":
    mcp.run(transport="stdio")
