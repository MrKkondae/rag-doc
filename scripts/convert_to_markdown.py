import argparse
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_CHOICES = ["migration", "rte43", "com43", "dev43"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="eGovFrame Wiki raw txt 파일을 Markdown으로 변환합니다."
    )
    parser.add_argument(
        "--source",
        required=True,
        choices=SOURCE_CHOICES,
        help="Markdown으로 변환할 지식베이스 이름",
    )
    return parser.parse_args()


def parse_raw_header(text: str) -> tuple[dict, str]:
    """
    collect_egov_wiki.py에서 붙인 주석형 헤더를 읽는다.

    예:
    # id: egov43-dev-guide
    # title: ...
    # category: ...
    # source_url: ...
    """
    meta = {}
    lines = text.splitlines()
    body_start = 0

    for idx, line in enumerate(lines):
        if line.startswith("# "):
            match = re.match(r"#\s*([^:]+):\s*(.*)", line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                meta[key] = value
            body_start = idx + 1
        elif line.strip() == "":
            body_start = idx + 1
            continue
        else:
            break

    body = "\n".join(lines[body_start:]).strip()
    return meta, body


def convert_code_blocks(text: str) -> str:
    """
    DokuWiki code 태그를 Markdown fenced code block으로 변환.
    """
    text = re.sub(
        r"<code\s+(\w+)>\s*\n?",
        r"```\1\n",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"<code>\s*\n?",
        "```\n",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"</code>",
        "```",
        text,
        flags=re.IGNORECASE,
    )
    return text


def convert_file_blocks(text: str) -> str:
    """
    DokuWiki file 태그도 코드블록으로 변환.
    예: <file java Sample.java>
    """
    text = re.sub(
        r"<file\s+(\w+)(?:\s+[^>]*)?>\s*\n?",
        r"```\1\n",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"<file(?:\s+[^>]*)?>\s*\n?",
        "```\n",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"</file>",
        "```",
        text,
        flags=re.IGNORECASE,
    )
    return text


def convert_headings(text: str) -> str:
    """
    DokuWiki 제목 문법을 Markdown 제목으로 변환.
    ====== H1 ======
    ===== H2 =====
    ==== H3 ====
    === H4 ===
    == H5 ==
    """
    patterns = [
        (r"^\s*======\s*(.*?)\s*======\s*$", r"# \1"),
        (r"^\s*=====\s*(.*?)\s*=====\s*$", r"## \1"),
        (r"^\s*====\s*(.*?)\s*====\s*$", r"### \1"),
        (r"^\s*===\s*(.*?)\s*===\s*$", r"#### \1"),
        (r"^\s*==\s*(.*?)\s*==\s*$", r"##### \1"),
    ]

    for pattern, repl in patterns:
        text = re.sub(pattern, repl, text, flags=re.MULTILINE)

    return text


def convert_lists(text: str) -> str:
    """
    DokuWiki 목록을 Markdown 목록으로 변환.
    공백 2개 이상 + * 또는 - 를 목록으로 처리.
    """
    text = re.sub(r"^\s{2,}\*\s+", "- ", text, flags=re.MULTILINE)
    text = re.sub(r"^\s{2,}-\s+", "- ", text, flags=re.MULTILINE)
    return text


def convert_links(text: str) -> str:
    """
    DokuWiki 링크 변환.
    [[url|label]] -> [label](url)
    [[page_id|label]] -> label
    [[page_id]] -> page_id
    """
    text = re.sub(
        r"\[\[(https?://[^\]|]+)\|([^\]]+)\]\]",
        r"[\2](\1)",
        text,
    )

    text = re.sub(
        r"\[\[([^\]|]+)\|([^\]]+)\]\]",
        r"\2",
        text,
    )

    text = re.sub(
        r"\[\[(https?://[^\]]+)\]\]",
        r"\1",
        text,
    )

    text = re.sub(
        r"\[\[([^\]]+)\]\]",
        r"\1",
        text,
    )

    return text


def convert_images(text: str) -> str:
    """
    DokuWiki 이미지 문법 처리.
    RAG 본문에서는 이미지를 직접 사용하지 않으므로 설명 텍스트만 남긴다.
    {{image.png|설명}} -> [이미지: 설명]
    {{image.png}} -> [이미지]
    """
    text = re.sub(
        r"\{\{[^}|]+\|([^}]+)\}\}",
        r"[이미지: \1]",
        text,
    )
    text = re.sub(
        r"\{\{[^}]+\}\}",
        r"[이미지]",
        text,
    )
    return text


def convert_formatting(text: str) -> str:
    """
    DokuWiki 기본 강조 문법 일부 변환.
    """
    text = re.sub(r"//([^/\n][^/\n]*?)//", r"*\1*", text)
    text = re.sub(r"\*\*([^*\n]+)\*\*", r"**\1**", text)
    text = re.sub(r"__([^_\n]+)__", r"_\1_", text)
    return text


def convert_tables(text: str) -> str:
    """
    DokuWiki 표는 완전 변환이 까다로우므로 1차로 파이프 구조를 유지한다.
    ^ header ^ header ^
    | cell   | cell   |
    """
    lines = text.splitlines()
    converted = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("^") and stripped.endswith("^"):
            cells = [c.strip() for c in stripped.strip("^").split("^")]
            converted.append("| " + " | ".join(cells) + " |")
            converted.append("| " + " | ".join(["---"] * len(cells)) + " |")
        elif stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            converted.append("| " + " | ".join(cells) + " |")
        else:
            converted.append(line)

    return "\n".join(converted)


def cleanup(text: str) -> str:
    """
    불필요한 공백 정리.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # DokuWiki 강제 줄바꿈 제거
    text = re.sub(r"\s*\\\\\s*\n", "\n", text)
    text = re.sub(r"\s*\\\\\s*", " ", text)

    text = re.sub(r"\n{4,}", "\n\n\n", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    return text.strip() + "\n"


def build_yaml_header(meta: dict) -> str:
    """
    Markdown YAML front matter 생성.
    """
    doc_id = meta.get("id", "")
    title = meta.get("title", "")
    category = meta.get("category", "")
    source_url = meta.get("source_url", "")

    return f"""---
id: "{doc_id}"
title: "{title}"
version: "4.3"
category: "{category}"
source: "eGovFrame Wiki"
source_url: "{source_url}"
format: "markdown"
---

"""


def convert_namespace(text: str) -> str:
    """
    DokuWiki namespace를 code span으로 변환.
    """
    pattern = r"(?<!`)(egovframework:[a-zA-Z0-9._:-]+)(?!`)"

    return re.sub(
        pattern,
        r"`\1`",
        text,
    )


def dokuwiki_to_markdown(text: str) -> str:
    text = convert_code_blocks(text)
    text = convert_file_blocks(text)
    text = convert_headings(text)
    text = convert_tables(text)
    text = convert_lists(text)
    text = convert_links(text)
    text = convert_namespace(text)
    text = convert_images(text)
    text = convert_formatting(text)
    text = cleanup(text)
    return text


def convert_file(raw_file: Path, md_dir: Path) -> Path:
    raw_text = raw_file.read_text(encoding="utf-8")
    meta, body = parse_raw_header(raw_text)

    markdown_body = dokuwiki_to_markdown(body)
    yaml_header = build_yaml_header(meta)

    out_file = md_dir / f"{raw_file.stem}.md"
    out_file.write_text(yaml_header + markdown_body, encoding="utf-8")

    return out_file


def main() -> None:
    args = parse_args()
    source = args.source
    raw_dir = BASE_DIR / "raw" / source
    md_dir = BASE_DIR / "markdown" / source
    md_dir.mkdir(parents=True, exist_ok=True)

    raw_files = sorted(raw_dir.glob("*.txt"))

    if not raw_files:
        print(f"source: {source}")
        print(f"입력 위치: {raw_dir.relative_to(BASE_DIR)}")
        print(f"출력 위치: {md_dir.relative_to(BASE_DIR)}")
        print(f"변환할 파일이 없습니다: {raw_dir}")
        return

    success_count = 0
    fail_count = 0

    print(f"source: {source}")
    print(f"입력 위치: {raw_dir.relative_to(BASE_DIR)}")
    print(f"출력 위치: {md_dir.relative_to(BASE_DIR)}")
    print(f"변환 대상 파일 수: {len(raw_files)}")

    for raw_file in raw_files:
        try:
            out_file = convert_file(raw_file, md_dir)
            success_count += 1
            print(f"[OK] {raw_file.name} -> {out_file.name}")
        except Exception as e:
            fail_count += 1
            print(f"[FAIL] {raw_file.name} - {e}")

    print()
    print("Markdown 변환 완료")
    print(f"- 성공: {success_count}")
    print(f"- 실패: {fail_count}")
    print(f"예시: python scripts/convert_to_markdown.py --source {source}")


if __name__ == "__main__":
    main()
