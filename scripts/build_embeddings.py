import argparse
import json
import pickle
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_CHOICES = ["migration", "rte43", "com43", "dev43"]

MODEL_NAME = "BAAI/bge-m3"
BATCH_SIZE = 16


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build embeddings from eGovFrame Wiki chunk files."
    )
    parser.add_argument(
        "--source",
        required=True,
        choices=SOURCE_CHOICES,
        help="Knowledge base name to embed",
    )
    return parser.parse_args()


def load_chunks(chunk_file: Path) -> list[dict]:
    if not chunk_file.exists():
        raise FileNotFoundError(f"Chunk file not found: {chunk_file}")

    chunks = []

    with chunk_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            chunks.append(json.loads(line))

    if not chunks:
        raise ValueError("Chunk data is empty.")

    return chunks


def build_embedding_text(chunk: dict) -> str:
    """
    Build the text used for embedding.
    Using heading + tags + content tends to improve retrieval quality.
    """
    document_title = chunk.get("document_title", "")
    heading = chunk.get("heading", "")
    tags = ", ".join(chunk.get("tags", []))
    content = chunk.get("content", "")

    return f"""Document: {document_title}
Heading: {heading}
Tags: {tags}

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


def save_embeddings(
    chunks: list[dict],
    embeddings: np.ndarray,
    out_file: Path,
    source: str,
) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "source": source,
        "model_name": MODEL_NAME,
        "embedding_dim": int(embeddings.shape[1]),
        "chunk_count": len(chunks),
        "chunks": chunks,
        "embeddings": embeddings,
    }

    with out_file.open("wb") as f:
        pickle.dump(data, f)

    print(f"Saved: {out_file.relative_to(BASE_DIR)}")


def main() -> None:
    args = parse_args()
    source = args.source
    chunk_file = BASE_DIR / "chunks" / f"{source}_chunks.jsonl"
    embedding_dir = BASE_DIR / "embeddings"
    out_file = embedding_dir / f"{source}_embeddings.pkl"

    print("build_embeddings.py started")
    print(f"source: {source}")
    print(f"input chunk file: {chunk_file.relative_to(BASE_DIR)}")
    print(f"output embedding file: {out_file.relative_to(BASE_DIR)}")

    print("Loading chunks")
    chunks = load_chunks(chunk_file)
    print(f"Chunk count: {len(chunks)}")

    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    print("Model loaded")

    print("Building embeddings")
    embeddings = encode_chunks(model, chunks)

    print("Embeddings built")
    print(f"Embedding shape: {embeddings.shape}")

    save_embeddings(chunks, embeddings, out_file, source)


if __name__ == "__main__":
    main()
