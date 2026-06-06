import argparse
import hashlib
import json
import re
from pathlib import Path
from statistics import median
from urllib.parse import parse_qs, urlparse


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_CHOICES = ["migration", "rte43", "com43", "dev43"]

MIN_CHARS = 200
MAX_CHARS = 1500
OVERLAP_CHARS = 150
TITLE_STOPWORDS = {
    "\uB2E4\uC74C",
    "\uC774\uC804",
    "\uBAA9\uCC28",
    "\uAC80\uC0C9",
    "\uBB38\uC11C \uB3C4\uAD6C",
}
CODE_FENCE_PATTERN = re.compile(r"^\s*(```|~~~)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Markdown documents into search chunk JSONL."
    )
    parser.add_argument(
        "--source",
        required=True,
        choices=SOURCE_CHOICES,
        help="Knowledge base name to chunk",
    )
    return parser.parse_args()


def parse_front_matter(text: str) -> tuple[dict, str]:
    """
    Split Markdown YAML front matter.
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
    Split sections by #, ##, ###, #### headings.
    """
    lines = text.splitlines()

    sections = []
    current = {
        "heading_level": 0,
        "heading": "Document Overview",
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
    Normalize chunk body text.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    return text.strip()


def is_code_fence(line: str) -> bool:
    return bool(CODE_FENCE_PATTERN.match(line))


def split_into_blocks(text: str) -> list[dict]:
    """
    Split a section into semantic blocks while preserving code fences.
    """
    lines = normalize_content(text).splitlines()
    blocks = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if is_code_fence(line):
            code_lines = [line]
            i += 1

            while i < len(lines):
                code_lines.append(lines[i])
                if is_code_fence(lines[i]):
                    i += 1
                    break
                i += 1

            blocks.append({
                "type": "code",
                "text": "\n".join(code_lines).strip(),
            })
            continue

        if stripped.startswith("|"):
            table_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            blocks.append({
                "type": "table",
                "text": "\n".join(table_lines).strip(),
            })
            continue

        if re.match(r"^\s*([-*+]|\d+\.)\s+", line):
            list_lines = [line]
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if not next_line.strip():
                    if i + 1 < len(lines) and re.match(r"^\s*([-*+]|\d+\.)\s+", lines[i + 1]):
                        list_lines.append(next_line)
                        i += 1
                        continue
                    break
                if re.match(r"^\s*([-*+]|\d+\.)\s+", next_line) or next_line.startswith("  "):
                    list_lines.append(next_line)
                    i += 1
                    continue
                break
            blocks.append({
                "type": "list",
                "text": "\n".join(list_lines).strip(),
            })
            continue

        para_lines = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            next_stripped = next_line.strip()

            if not next_stripped:
                break
            if is_code_fence(next_line):
                break
            if next_stripped.startswith("|"):
                break
            if re.match(r"^\s*([-*+]|\d+\.)\s+", next_line):
                break

            para_lines.append(next_line)
            i += 1

        blocks.append({
            "type": "paragraph",
            "text": "\n".join(para_lines).strip(),
        })

    return [block for block in blocks if block["text"]]


def split_by_sentence(text: str, max_chars: int) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", normalize_content(text))
    parts = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        candidate = f"{current} {sentence}".strip() if current else sentence
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                parts.append(current)
            if len(sentence) > max_chars:
                parts.extend(split_by_length(sentence, max_chars))
                current = ""
            else:
                current = sentence

    if current:
        parts.append(current)

    return parts


def split_by_length(text: str, max_chars: int) -> list[str]:
    """
    Final fallback when no semantic boundary fits.
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

        start = max(0, end - OVERLAP_CHARS)

    return chunks


def split_oversized_code_block(text: str, max_chars: int) -> list[dict]:
    """
    Oversized code blocks are split only as a last resort, while keeping fence balance.
    """
    lines = text.splitlines()
    if len(lines) < 2 or not is_code_fence(lines[0]):
        return [{"text": part, "split_reason": "length_fallback"} for part in split_by_length(text, max_chars)]

    opening_fence = lines[0]
    closing_fence = lines[-1] if is_code_fence(lines[-1]) else opening_fence
    inner_lines = lines[1:-1] if is_code_fence(lines[-1]) else lines[1:]
    parts = []
    current = []

    for line in inner_lines:
        candidate_lines = [opening_fence] + current + [line] + [closing_fence]
        candidate_text = "\n".join(candidate_lines).strip()

        if len(candidate_text) <= max_chars or not current:
            current.append(line)
            continue

        parts.append({
            "text": "\n".join([opening_fence] + current + [closing_fence]).strip(),
            "split_reason": "code_block_oversized",
        })
        current = [line]

    if current:
        parts.append({
            "text": "\n".join([opening_fence] + current + [closing_fence]).strip(),
            "split_reason": "code_block_oversized",
        })

    return parts


def split_oversized_block(block: dict, max_chars: int) -> list[dict]:
    text = normalize_content(block["text"])
    block_type = block["type"]

    if block_type == "code":
        return split_oversized_code_block(text, max_chars)

    if block_type == "table":
        lines = text.splitlines()
        parts = []
        current = []
        for line in lines:
            candidate = "\n".join(current + [line]).strip()
            if len(candidate) <= max_chars or not current:
                current.append(line)
            else:
                parts.append({"text": "\n".join(current).strip(), "split_reason": "table_row_boundary"})
                current = [line]
        if current:
            parts.append({"text": "\n".join(current).strip(), "split_reason": "table_row_boundary"})
        return parts

    if block_type == "list":
        items = [item.strip() for item in re.split(r"\n(?=\s*(?:[-*+]|\d+\.))", text) if item.strip()]
        parts = []
        current = ""
        for item in items:
            candidate = f"{current}\n{item}".strip() if current else item
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    parts.append({"text": current, "split_reason": "list_item_boundary"})
                current = item
        if current:
            parts.append({"text": current, "split_reason": "list_item_boundary"})
        return parts

    sentence_parts = split_by_sentence(text, max_chars)
    if len(sentence_parts) > 1:
        return [{"text": part, "split_reason": "sentence_boundary"} for part in sentence_parts]

    return [{"text": part, "split_reason": "length_fallback"} for part in split_by_length(text, max_chars)]


def split_long_text(
    text: str,
    max_chars: int = MAX_CHARS,
) -> list[dict]:
    """
    Split long text by semantic blocks first, then narrower boundaries.
    """
    text = normalize_content(text)

    if len(text) <= max_chars:
        return [{"text": text, "split_reason": "section_boundary"}]

    blocks = split_into_blocks(text)
    parts = []
    current = ""
    current_reason = "paragraph_boundary"

    for block in blocks:
        block_text = block["text"]
        if len(block_text) > max_chars:
            if current:
                parts.append({"text": current, "split_reason": current_reason})
                current = ""

            parts.extend(split_oversized_block(block, max_chars))
            continue

        candidate = f"{current}\n\n{block_text}".strip() if current else block_text
        if len(candidate) <= max_chars:
            current = candidate
            current_reason = f"{block['type']}_boundary"
        else:
            if current:
                parts.append({"text": current, "split_reason": current_reason})
            current = block_text
            current_reason = f"{block['type']}_boundary"

    if current:
        parts.append({"text": current, "split_reason": current_reason})

    return parts


def is_meaningful_chunk(text: str) -> bool:
    """
    Skip chunks that are too short or not meaningful.
    """
    cleaned = re.sub(r"\s+", "", text)

    if len(cleaned) < MIN_CHARS:
        return False

    if cleaned in {"[image]", "[image:]", "image"}:
        return False

    return True


def infer_tags(meta: dict, heading: str, content: str) -> list[str]:
    """
    Infer lightweight search tags from heading and content.
    """
    tags = set()

    category = meta.get("category")
    if category:
        tags.add(category)

    text = f"{heading}\n{content}".lower()

    keyword_map = {
        "migration": ["migration", "upgrade"],
        "runtime": ["runtime", "rte"],
        "development": ["development", "dev"],
        "spring": ["spring", "spring framework"],
        "mybatis": ["mybatis", "ibatis", "sqlmap"],
        "dao": ["dao", "egovabstractdao", "repository"],
        "maven": ["maven", "pom.xml", "dependency"],
        "jdk": ["jdk", "java 1.8", "java8", "java 8"],
        "servlet": ["servlet"],
        "log": ["log4j", "logging", "slf4j"],
        "batch": ["batch"],
        "security": ["security", "authentication", "authorization"],
        "transaction": ["transaction"],
        "exception": ["exception"],
        "common_component": ["common component", "common_component"],
        "fdl": ["fdl", "foundation", "foundation layer"],
        "psl": ["psl", "persistence", "persistence layer"],
        "ptl": ["ptl", "presentation", "presentation layer"],
        "itl": ["itl", "integration", "integration layer"],
        "property": ["property", "propertyservice", "egovpropertyservice"],
        "id_generation": ["id generation", "idgeneration", "egovidgnrservice", "idgnr"],
        "aop": ["aop", "aspect", "aspectj"],
        "cache": ["cache", "ehcache"],
        "scheduling": ["scheduling", "scheduler", "quartz"],
        "file": ["file", "multipart", "upload"],
        "validation": ["validation", "validator"],
        "rest": ["rest", "restful", "api"],
        "webmvc": ["spring mvc", "mvc", "controller", "requestmapping"],
        "datasource": ["datasource", "data source", "dbcp", "connection pool"],
        "sql": ["sql", "query"],
        "xml": ["xml", "context", "bean", "beans"],
    }

    for tag, keywords in keyword_map.items():
        if any(keyword in text for keyword in keywords):
            tags.add(tag)

    return sorted(tags)


def extract_page_id(meta: dict) -> str:
    source_url = meta.get("source_url", "")
    if not source_url:
        return ""

    parsed = urlparse(source_url)
    page_ids = parse_qs(parsed.query).get("id", [])
    return page_ids[0] if page_ids else ""


def find_heading_candidates(body: str) -> tuple[str, str]:
    first_h1 = ""
    first_h2 = ""

    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not first_h1:
            first_h1 = stripped[2:].strip()
        elif stripped.startswith("## ") and not first_h2:
            first_h2 = stripped[3:].strip()

        if first_h1 and first_h2:
            break

    return first_h1, first_h2


def is_bad_title(title: str) -> bool:
    return not title or title.strip() in TITLE_STOPWORDS


def resolve_document_title(meta: dict, body: str, source_file: Path) -> str:
    yaml_title = meta.get("title", "").strip()
    first_h1, first_h2 = find_heading_candidates(body)
    page_id = extract_page_id(meta)
    page_segment = page_id.split(":")[-1] if page_id else ""
    file_title = source_file.stem.replace("-", " ")

    if not is_bad_title(first_h1):
        return first_h1
    if not is_bad_title(first_h2):
        return first_h2
    if not is_bad_title(yaml_title):
        return yaml_title
    if page_segment:
        return page_segment
    return file_title


def build_chunk(
    meta: dict,
    source_file: Path,
    section: dict,
    content: str,
    chunk_index: int,
    sub_index: int,
    document_title: str,
    split_reason: str,
) -> dict:
    source_id = meta.get("id") or source_file.stem
    chunk_id = f"{source_id}-{chunk_index:04d}"

    if sub_index > 1:
        chunk_id = f"{chunk_id}-{sub_index}"

    heading = section["heading"]
    page_id = extract_page_id(meta)
    source_url = meta.get("source_url", "")

    return {
        "chunk_id": chunk_id,
        "version": meta.get("version", "4.3"),
        "category": meta.get("category", ""),
        "source": meta.get("source", "eGovFrame Wiki"),
        "source_url": source_url,
        "source_file": source_file.name,
        "document_id": source_id,
        "document_title": document_title,
        "heading": heading,
        "heading_level": section["heading_level"],
        "content": content,
        "tags": infer_tags(meta, heading, content),
        "page_id": page_id,
        "url": source_url,
        "text": content,
        "chunk_index": chunk_index,
        "section_title": heading,
        "heading_path": heading,
        "char_count": len(content),
        "split_reason": split_reason,
    }


def create_chunks_from_file(md_file: Path) -> list[dict]:
    text = md_file.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)
    document_title = resolve_document_title(meta, body, md_file)

    sections = split_by_headings(body)

    chunks = []
    chunk_index = 1

    for section in sections:
        section_text = normalize_content("\n".join(section["content_lines"]))

        if not section_text:
            continue

        split_parts = split_long_text(section_text)
        sub_index = 1

        for part in split_parts:
            content = normalize_content(part["text"])

            if not is_meaningful_chunk(content):
                continue

            chunk = build_chunk(
                meta=meta,
                source_file=md_file,
                section=section,
                content=content,
                chunk_index=chunk_index,
                sub_index=sub_index,
                document_title=document_title,
                split_reason=part["split_reason"],
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

    return hashlib.md5(normalized.encode("utf-8")).hexdigest()


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
    print(f"Duplicate chunks removed: {duplicate_count}")
    print(f"Final chunk count: {len(unique_chunks)}")

    return unique_chunks


def has_unbalanced_code_fence(text: str) -> bool:
    fences = [line for line in text.splitlines() if is_code_fence(line)]
    return len(fences) % 2 != 0


def print_quality_summary(chunks: list[dict]) -> None:
    if not chunks:
        return

    lengths = [len(chunk.get("content", "")) for chunk in chunks]
    doc_chunk_counts = {}

    for chunk in chunks:
        doc_id = chunk.get("document_id", "")
        doc_chunk_counts[doc_id] = doc_chunk_counts.get(doc_id, 0) + 1

    exact_max_count = sum(1 for length in lengths if length == MAX_CHARS)
    fence_imbalance_count = sum(1 for chunk in chunks if has_unbalanced_code_fence(chunk.get("content", "")))
    bad_title_count = sum(1 for chunk in chunks if is_bad_title(chunk.get("document_title", "")))
    short_chunk_count = sum(1 for length in lengths if length < MIN_CHARS)

    print()
    print("Chunk quality summary")
    print(f"- Total chunks: {len(chunks)}")
    print(f"- Total documents: {len(doc_chunk_counts)}")
    print(f"- Avg chunk length: {sum(lengths) / len(lengths):.1f}")
    print(f"- Median chunk length: {median(lengths):.1f}")
    print(f"- Min chunk length: {min(lengths)}")
    print(f"- Max chunk length: {max(lengths)}")
    print(f"- Chunks at max_chars ({MAX_CHARS}): {exact_max_count}")
    print(f"- Unbalanced code fence chunks: {fence_imbalance_count}")
    print(f"- Blocklisted document titles: {bad_title_count}")
    print(f"- Short chunks (< {MIN_CHARS} chars): {short_chunk_count}")
    print("- Top 10 documents by chunk count:")

    for doc_id, count in sorted(doc_chunk_counts.items(), key=lambda item: item[1], reverse=True)[:10]:
        print(f"  {doc_id}: {count}")


def main() -> None:
    args = parse_args()
    source = args.source
    md_dir = BASE_DIR / "markdown" / source
    chunk_dir = BASE_DIR / "chunks"
    out_file = chunk_dir / f"{source}_chunks.jsonl"

    print("create_chunks.py started")
    print(f"source: {source}")
    print(f"input dir: {md_dir.relative_to(BASE_DIR)}")
    print(f"output file: {out_file.relative_to(BASE_DIR)}")
    print("Validation metrics are printed after chunk generation.")

    chunk_dir.mkdir(parents=True, exist_ok=True)

    md_files = sorted(md_dir.glob("*.md"))

    if not md_files:
        print(f"No Markdown files found: {md_dir}")
        return

    all_chunks = []

    print(f"Markdown files to chunk: {len(md_files)}")

    for md_file in md_files:
        try:
            chunks = create_chunks_from_file(md_file)
            all_chunks.extend(chunks)
            print(f"[OK] {md_file.name} -> {len(chunks)} chunks")
        except Exception as e:
            print(f"[FAIL] {md_file.name} - {e}")

    all_chunks = remove_duplicate_chunks(all_chunks)

    with out_file.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print_quality_summary(all_chunks)

    print()
    print("Chunk generation complete")
    print(f"- Input Markdown files: {len(md_files)}")
    print(f"- Generated chunks: {len(all_chunks)}")
    print(f"- Output file: {out_file.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
