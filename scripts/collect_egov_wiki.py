import argparse
import time
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests
import yaml
from tqdm import tqdm


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_CHOICES = ["migration", "rte43", "com43", "dev43"]

REQUEST_DELAY_SECONDS = 1.0
TIMEOUT_SECONDS = 20


def to_export_raw_url(url: str) -> str:
    """
    DokuWiki 페이지 URL을 본문 export URL로 변환한다.

    doku.php?id=egovframework:dev4.3
    ->
    doku.php?id=egovframework:dev4.3&do=export_raw
    """
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query["do"] = ["export_raw"]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect raw eGovFrame Wiki documents for a selected source."
    )
    parser.add_argument(
        "--source",
        required=True,
        choices=SOURCE_CHOICES,
        help="수집할 지식베이스 이름",
    )
    return parser.parse_args()


def load_documents(url_file: Path) -> list[dict]:
    if not url_file.exists():
        raise FileNotFoundError(f"URL 파일이 없습니다: {url_file}")

    with url_file.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    documents = config.get("documents", [])
    if not documents:
        raise ValueError("수집할 documents 항목이 없습니다.")

    return documents


def fetch_text(url: str) -> str:
    headers = {
        "User-Agent": "egovframe-rag-collector/0.1"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    # eGovFrame Wiki는 보통 UTF-8 기준
    response.encoding = "utf-8"
    return response.text


def save_raw_document(doc: dict, text: str, raw_dir: Path) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)

    doc_id = doc["id"]
    out_path = raw_dir / f"{doc_id}.txt"

    header = f"""# id: {doc.get("id", "")}
# title: {doc.get("title", "")}
# category: {doc.get("category", "")}
# source_url: {doc.get("url", "")}
# collected_by: collect_egov_wiki.py

"""

    out_path.write_text(header + text, encoding="utf-8")
    return out_path


def main() -> None:
    args = parse_args()
    source = args.source
    url_file = BASE_DIR / "urls" / f"{source}_discovered_urls.yml"
    raw_dir = BASE_DIR / "raw" / source
    documents = load_documents(url_file)

    print(f"source: {source}")
    print(f"URL 파일: {url_file.relative_to(BASE_DIR)}")
    print(f"저장 위치: {raw_dir.relative_to(BASE_DIR)}")
    print(f"수집 대상 문서 수: {len(documents)}")

    success_count = 0
    fail_count = 0

    for doc in tqdm(documents, desc="Collecting eGovFrame Wiki"):
        try:
            export_url = to_export_raw_url(doc["url"])
            text = fetch_text(export_url)

            if not text.strip():
                raise ValueError("수집된 본문이 비어 있습니다.")

            out_path = save_raw_document(doc, text, raw_dir)
            success_count += 1

            print(f"[OK] {doc['id']} -> {out_path}")

        except Exception as e:
            fail_count += 1
            print(f"[FAIL] {doc.get('id', 'unknown')} - {e}")

        time.sleep(REQUEST_DELAY_SECONDS)

    print()
    print("수집 완료")
    print(f"- 성공: {success_count}")
    print(f"- 실패: {fail_count}")
    print("예시: python scripts/collect_egov_wiki.py --source migration")


if __name__ == "__main__":
    main()
