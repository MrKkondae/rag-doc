import pickle
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[1]

EMBEDDING_FILE = BASE_DIR / "embeddings" / "egov43_embeddings.pkl"
TOP_K = 5


def load_embedding_store() -> dict:
    if not EMBEDDING_FILE.exists():
        raise FileNotFoundError(f"Embedding 파일이 없습니다: {EMBEDDING_FILE}")

    with EMBEDDING_FILE.open("rb") as f:
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
    ]

    for term in important_terms:
        if term in query_lower and term in text:
            boost += 0.08

    # 패키지명 변경 질문일 때 Maven/POM/dependency 관련 chunk 우대
    if "패키지명" in query_lower and "변경" in query_lower:
        heading = chunk.get("heading", "").lower()
        content = chunk.get("content", "").lower()
        category = chunk.get("category", "").lower()

        # migration 문서 우대
        if category == "migration":
            boost += 0.04

        # 제목이 Maven을 사용하는 경우면 강하게 우대
        if "maven을 사용하는 경우" in heading:
            boost += 0.12

        # 정확한 패키지명 근거가 있으면 우대
        if "org.egovframe.rte" in content:
            boost += 0.08

        # groupId/artifactId는 둘 다 있을 때만 우대
        if "groupid" in content and "artifactid" in content:
            boost += 0.05

        # 단순 maven/pom.xml은 약하게만 우대
        if "pom.xml" in content:
            boost += 0.02

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
        final_score = float(vector_score) + boost

        results.append((idx, float(vector_score), boost, final_score))

    results.sort(key=lambda x: x[3], reverse=True)

    return results[:top_k]


def print_result(rank: int, score: float, chunk: dict) -> None:
    content = chunk.get("content", "")
    preview = content[:500].replace("\n", " ")

    print("=" * 100)
    print(f"[{rank}] score: {score:.4f}")
    print(f"문서명: {chunk.get('document_title', '')}")
    print(f"제목: {chunk.get('heading', '')}")
    print(f"카테고리: {chunk.get('category', '')}")
    print(f"태그: {', '.join(chunk.get('tags', []))}")
    print(f"소스파일: {chunk.get('source_file', '')}")
    print(f"URL: {chunk.get('source_url', '')}")
    print("-" * 100)
    print(preview)
    print()


def search(query: str, top_k: int = TOP_K) -> None:
    data = load_embedding_store()

    model_name = data["model_name"]
    chunks = data["chunks"]
    embeddings = data["embeddings"]

    print(f"모델 로딩: {model_name}")
    model = SentenceTransformer(model_name)

    query_text = build_query_text(query)

    query_embedding = model.encode(
        query_text,
        normalize_embeddings=True,
    )

    query_embedding = np.asarray(query_embedding, dtype=np.float32)

    results = cosine_search(query, query_embedding, embeddings, chunks, top_k)

    print()
    print(f"질문: {query}")
    print(f"검색 결과 Top {top_k}")
    print()

    for rank, (idx, vector_score, boost, final_score) in enumerate(results, start=1):
        print_result(rank, final_score, chunks[idx])
        print(f"vector_score: {vector_score:.4f}, keyword_boost: {boost:.4f}, final_score: {final_score:.4f}")

def main() -> None:
    print("eGovFrame 4.3 Chunk 검색 테스트")
    print("종료하려면 빈 값 입력")
    print()

    while True:
        query = input("질문> ").strip()

        if not query:
            print("종료합니다.")
            break

        search(query, TOP_K)


if __name__ == "__main__":
    main()