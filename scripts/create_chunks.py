import json
import re
import hashlib
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

MD_DIR = BASE_DIR / "markdown" / "egov43"
CHUNK_DIR = BASE_DIR / "chunks"
OUT_FILE = CHUNK_DIR / "egov43_chunks.jsonl"

MIN_CHARS = 200
MAX_CHARS = 1500
OVERLAP_CHARS = 150


def parse_front_matter(text: str) -> tuple[dict, str]:
    """
    Markdown YAML front matter를 분리한다.
    """
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    raw_meta = parts[1].strip()
    body = parts[2].strip()

    meta = {}
    for line in raw_meta.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        meta[key] = value

    return meta, body


def split_by_headings(text: str) -> list[dict]:
    """
    #, ##, ### 제목 기준으로 섹션 분리.
    """
    lines = text.splitlines()

    sections = []
    current = {
        "heading_level": 0,
        "heading": "문서 개요",
        "content_lines": [],
    }

    heading_pattern = re.compile(r"^(#{1,4})\s+(.+?)\s*$")

    for line in lines:
        match = heading_pattern.match(line)

        if match:
            if current["content_lines"]:
                sections.append(current)

            current = {
                "heading_level": len(match.group(1)),
                "heading": match.group(2).strip(),
                "content_lines": [],
            }
        else:
            current["content_lines"].append(line)

    if current["content_lines"]:
        sections.append(current)

    return sections


def normalize_content(text: str) -> str:
    """
    Chunk 본문 정리.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    return text.strip()


def split_long_text(text: str, max_chars: int = MAX_CHARS, overlap: int = OVERLAP_CHARS) -> list[str]:
    """
    너무 긴 섹션은 문단 기준으로 추가 분할한다.
    """
    text = normalize_content(text)

    if len(text) <= max_chars:
        return [text]

    paragraphs = re.split(r"\n\s*\n", text)

    chunks = []
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        candidate = current + "\n\n" + para if current else para

        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)

            if len(para) > max_chars:
                chunks.extend(split_by_length(para, max_chars, overlap))
                current = ""
            else:
                current = para

    if current:
        chunks.append(current)

    return chunks


def split_by_length(text: str, max_chars: int, overlap: int) -> list[str]:
    """
    코드나 표처럼 문단 분리가 안 되는 긴 텍스트를 길이 기준으로 분할.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(0, end - overlap)

    return chunks


def is_meaningful_chunk(text: str) -> bool:
    """
    너무 짧거나 의미 없는 chunk 제외.
    """
    cleaned = re.sub(r"\s+", "", text)

    if len(cleaned) < MIN_CHARS:
        return False

    if cleaned in {"[이미지]", "[이미지:]", "이미지"}:
        return False

    return True


def infer_tags(meta: dict, heading: str, content: str) -> list[str]:
    """
    간단한 태그 자동 추론.
    """
    tags = set()

    category = meta.get("category")
    if category:
        tags.add(category)

    text = f"{heading}\n{content}".lower()

    keyword_map = {
        "migration": ["migration", "upgrade", "업그레이드", "마이그레이션", "전환"],
        "runtime": ["runtime", "실행환경", "rte"],
        "development": ["development", "개발환경", "dev"],
        "spring": ["spring", "스프링"],
        "mybatis": ["mybatis", "ibatis", "sqlmap"],
        "dao": ["dao", "egovabstractdao", "repository"],
        "maven": ["maven", "pom.xml", "dependency"],
        "jdk": ["jdk", "java 1.8", "java8"],
        "servlet": ["servlet"],
        "log": ["log4j", "logging", "로그"],
        "batch": ["batch", "배치"],
        "security": ["security", "보안"],
        "transaction": ["transaction", "트랜잭션"],
        "exception": ["exception", "예외"],
        "common_component": ["common component", "공통컴포넌트", "common_component"],
    }

    for tag, keywords in keyword_map.items():
        if any(keyword in text for keyword in keywords):
            tags.add(tag)

    return sorted(tags)


def build_chunk(
    meta: dict,
    source_file: Path,
    section: dict,
    content: str,
    chunk_index: int,
    sub_index: int,
) -> dict:
    source_id = meta.get("id") or source_file.stem
    chunk_id = f"{source_id}-{chunk_index:04d}"

    if sub_index > 1:
        chunk_id = f"{chunk_id}-{sub_index}"

    heading = section["heading"]

    return {
        "chunk_id": chunk_id,
        "version": meta.get("version", "4.3"),
        "category": meta.get("category", ""),
        "source": meta.get("source", "eGovFrame Wiki"),
        "source_url": meta.get("source_url", ""),
        "source_file": source_file.name,
        "document_id": source_id,
        "document_title": meta.get("title", ""),
        "heading": heading,
        "heading_level": section["heading_level"],
        "content": content,
        "tags": infer_tags(meta, heading, content),
    }


def create_chunks_from_file(md_file: Path) -> list[dict]:
    text = md_file.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)

    sections = split_by_headings(body)

    chunks = []
    chunk_index = 1

    for section in sections:
        section_text = normalize_content("\n".join(section["content_lines"]))

        if not section_text:
            continue

        split_texts = split_long_text(section_text)

        sub_index = 1

        for part in split_texts:
            if not is_meaningful_chunk(part):
                continue

            chunk = build_chunk(
                meta=meta,
                source_file=md_file,
                section=section,
                content=part,
                chunk_index=chunk_index,
                sub_index=sub_index,
            )

            chunks.append(chunk)
            sub_index += 1
            chunk_index += 1

    return chunks

def create_chunk_hash(chunk: dict) -> str:

    normalized = " ".join(
        (
            chunk.get("heading", "") +
            "\n" +
            chunk.get("content", "")
        ).split()
    )

    return hashlib.md5(
        normalized.encode("utf-8")
    ).hexdigest()

def remove_duplicate_chunks(chunks: list[dict]) -> list[dict]:

    seen_hashes = set()
    unique_chunks = []

    duplicate_count = 0

    for chunk in chunks:

        chunk_hash = create_chunk_hash(chunk)

        if chunk_hash in seen_hashes:
            duplicate_count += 1
            continue

        seen_hashes.add(chunk_hash)
        unique_chunks.append(chunk)

    print()
    print(f"중복 제거: {duplicate_count}개")
    print(f"최종 Chunk 수: {len(unique_chunks)}")

    return unique_chunks


def main() -> None:

    print("create_chunks.py started")
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)

    md_files = sorted(MD_DIR.glob("*.md"))

    if not md_files:
        print(f"Markdown 파일이 없습니다: {MD_DIR}")
        return

    all_chunks = []

    print(f"Chunk 생성 대상 파일 수: {len(md_files)}")

    for md_file in md_files:
        try:
            chunks = create_chunks_from_file(md_file)
            all_chunks.extend(chunks)
            print(f"[OK] {md_file.name} -> {len(chunks)} chunks")
        except Exception as e:
            print(f"[FAIL] {md_file.name} - {e}")

    all_chunks = remove_duplicate_chunks(all_chunks)

    with OUT_FILE.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print()
    print("Chunk 생성 완료")
    print(f"- 입력 Markdown 파일 수: {len(md_files)}")
    print(f"- 생성 Chunk 수: {len(all_chunks)}")
    print(f"- 출력 파일: {OUT_FILE}")


if __name__ == "__main__":
    main()