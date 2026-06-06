import argparse
import pickle
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_CHOICES = ["migration", "rte43", "com43", "dev43"]
TOP_K = 5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interactive search test for eGovFrame chunk embeddings."
    )
    parser.add_argument(
        "--source",
        required=True,
        choices=SOURCE_CHOICES,
        help="Knowledge base name to search",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=TOP_K,
        help="Number of search results to show",
    )
    return parser.parse_args()


def load_embedding_store(embedding_file: Path) -> dict:
    if not embedding_file.exists():
        raise FileNotFoundError(f"Embedding file not found: {embedding_file}")

    with embedding_file.open("rb") as f:
        data = pickle.load(f)

    return data


def build_query_text(query: str) -> str:
    return query.strip()


def keyword_boost(query: str, chunk: dict) -> float:
    text = (
        chunk.get("heading", "") + "\n" +
        chunk.get("content", "") + "\n" +
        " ".join(chunk.get("tags", []))
    ).lower()

    query_lower = query.lower()
    boost = 0.0

    for term in query_lower.split():
        if term in text:
            boost += 0.03

    important_terms = [
        "org.egovframe.rte",
        "egovframework.rte",
        "패키지명",
        "groupid",
        "artifactid",
        "maven",
        "pom.xml",
        "log4j2",
        "egovpropertyservice",
        "propertyservice",
        "property service",
        "idgeneration",
        "id generation",
        "egovidgnrservice",
        "transaction",
        "transactionmanager",
        "mybatis",
        "sqlmap",
        "egovabstractdao",
        "aop",
        "aspect",
        "exception",
        "exceptionhandler",
        "batch",
        "quartz",
        "spring mvc",
        "controller",
        "datasource",
        "fileupload",
        "multipart",
        "validation",
        "validator",
    ]

    for term in important_terms:
        if term in query_lower and term in text:
            boost += 0.08

    # Prefer migration/package rename evidence for migration-style questions.
    if "패키지명" in query_lower and "변경" in query_lower:
        heading = chunk.get("heading", "").lower()
        content = chunk.get("content", "").lower()
        category = chunk.get("category", "").lower()

        if category == "migration":
            boost += 0.04

        if "maven을 사용하는 경우" in heading:
            boost += 0.12

        if "org.egovframe.rte" in content:
            boost += 0.08

        if "groupid" in content and "artifactid" in content:
            boost += 0.05

        if "pom.xml" in content:
            boost += 0.02

        boost += concept_heading_boost(query, chunk)

    return boost


def cosine_search(
    query: str,
    query_embedding: np.ndarray,
    embeddings: np.ndarray,
    chunks: list[dict],
    top_k: int = TOP_K,
):
    vector_scores = embeddings @ query_embedding

    results = []

    for idx, vector_score in enumerate(vector_scores):
        chunk = chunks[idx]
        boost = keyword_boost(query, chunk)

        if chunk.get("document_title") == "ItemWriter":
            print(
                chunk.get("heading"),
                vector_score,
                boost
            )

        final_score = float(vector_score) + boost

        results.append((idx, float(vector_score), boost, final_score))

    results.sort(key=lambda x: x[3], reverse=True)

    return results[:top_k]


def print_result(rank: int, score: float, chunk: dict) -> None:
    content = chunk.get("content", "")
    preview = content[:500].replace("\n", " ")

    print("=" * 100)
    print(f"[{rank}] score: {score:.4f}")
    print(f"document_title: {chunk.get('document_title', '')}")
    print(f"heading: {chunk.get('heading', '')}")
    print(f"category: {chunk.get('category', '')}")
    print(f"tags: {', '.join(chunk.get('tags', []))}")
    print(f"source_file: {chunk.get('source_file', '')}")
    print(f"url: {chunk.get('source_url', '')}")
    print("-" * 100)
    print(preview)
    print()


def search(query: str, embedding_file: Path, top_k: int = TOP_K) -> None:
    data = load_embedding_store(embedding_file)

    store_source = data.get("source", "")
    model_name = data["model_name"]
    chunks = data["chunks"]
    embeddings = data["embeddings"]

    if store_source:
        print(f"embedding source: {store_source}")

    print(f"loading model: {model_name}")
    model = SentenceTransformer(model_name)

    query_text = build_query_text(query)

    query_embedding = model.encode(
        query_text,
        normalize_embeddings=True,
    )

    query_embedding = np.asarray(query_embedding, dtype=np.float32)

    results = cosine_search(query, query_embedding, embeddings, chunks, top_k)

    print()
    print(f"query: {query}")
    print(f"Top {top_k} results")
    print()

    for rank, (idx, vector_score, boost, final_score) in enumerate(results, start=1):
        print_result(rank, final_score, chunks[idx])
        print(
            f"vector_score: {vector_score:.4f}, "
            f"keyword_boost: {boost:.4f}, "
            f"final_score: {final_score:.4f}"
        )

def normalize_text(text: str) -> str:
    return text.lower().replace(" ", "").replace("-", "").replace("_", "")


def concept_heading_boost(query: str, chunk: dict) -> float:
    query_norm = normalize_text(query)
    title_norm = normalize_text(chunk.get("document_title", ""))
    heading = chunk.get("heading", "").strip().lower()

    boost = 0.0

    # query가 document_title과 정확히 같은 경우 기본 설명/개요 heading 우선
    if query_norm and query_norm == title_norm:
        if heading in ["설명", "개요", "소개"]:
            boost += 0.06

        # 상세 구현체 설명은 약간만 감점
        if "flatfile" in heading or "dbitemwriter" in heading or "listener" in heading:
            boost -= 0.02

    return boost

def main() -> None:
    args = parse_args()
    source = args.source
    top_k = args.top_k
    embedding_file = BASE_DIR / "embeddings" / f"{source}_embeddings.pkl"

    print("eGovFrame chunk search")
    print(f"source: {source}")
    print(f"embedding file: {embedding_file.relative_to(BASE_DIR)}")
    print("Press Enter on an empty prompt to exit.")
    print()

    while True:
        query = input("query> ").strip()

        if not query:
            print("Exiting.")
            break

        search(query, embedding_file, top_k)


if __name__ == "__main__":
    main()
