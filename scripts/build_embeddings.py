import json
import pickle
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


BASE_DIR = Path(__file__).resolve().parents[1]

CHUNK_FILE = BASE_DIR / "chunks" / "egov43_chunks.jsonl"
EMBEDDING_DIR = BASE_DIR / "embeddings"
OUT_FILE = EMBEDDING_DIR / "egov43_embeddings.pkl"

MODEL_NAME = "BAAI/bge-m3"
BATCH_SIZE = 16


def load_chunks() -> list[dict]:
    if not CHUNK_FILE.exists():
        raise FileNotFoundError(f"Chunk 파일이 없습니다: {CHUNK_FILE}")

    chunks = []

    with CHUNK_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            chunks.append(json.loads(line))

    if not chunks:
        raise ValueError("Chunk 데이터가 비어 있습니다.")

    return chunks


def build_embedding_text(chunk: dict) -> str:
    """
    임베딩에 사용할 텍스트 구성.
    heading + tags + content를 함께 사용하면 검색 품질이 좋아진다.
    """
    document_title = chunk.get("document_title", "")
    heading = chunk.get("heading", "")
    tags = ", ".join(chunk.get("tags", []))
    content = chunk.get("content", "")

    return f"""문서명: {document_title}
제목: {heading}
태그: {tags}

{content}
""".strip()


def encode_chunks(model: SentenceTransformer, chunks: list[dict]) -> np.ndarray:
    texts = [build_embedding_text(chunk) for chunk in chunks]

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    return np.asarray(embeddings, dtype=np.float32)


def save_embeddings(chunks: list[dict], embeddings: np.ndarray) -> None:
    EMBEDDING_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        "model_name": MODEL_NAME,
        "embedding_dim": int(embeddings.shape[1]),
        "chunk_count": len(chunks),
        "chunks": chunks,
        "embeddings": embeddings,
    }

    with OUT_FILE.open("wb") as f:
        pickle.dump(data, f)

    print(f"저장 완료: {OUT_FILE}")


def main() -> None:
    print("Chunk 로딩 시작")
    chunks = load_chunks()
    print(f"Chunk 개수: {len(chunks)}")

    print(f"모델 로딩 시작: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    print("모델 로딩 완료")

    print("임베딩 생성 시작")
    embeddings = encode_chunks(model, chunks)

    print("임베딩 생성 완료")
    print(f"Embedding shape: {embeddings.shape}")

    save_embeddings(chunks, embeddings)


if __name__ == "__main__":
    main()