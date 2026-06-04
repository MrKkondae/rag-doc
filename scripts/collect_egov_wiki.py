import time
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests
import yaml
from tqdm import tqdm


BASE_DIR = Path(__file__).resolve().parents[1]
URL_FILE = BASE_DIR / "urls" / "egov43_discovered_urls.yml"
RAW_DIR = BASE_DIR / "raw" / "egov43"

REQUEST_DELAY_SECONDS = 1.0
TIMEOUT_SECONDS = 20


def to_export_raw_url(url: str) -> str:
    """
    DokuWiki 페이지 URL을 원문 export URL로 변환한다.
    예:
    doku.php?id=egovframework:dev4.3
    ->
    doku.php?id=egovframework:dev4.3&do=export_raw
    """
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query["do"] = ["export_raw"]
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def load_documents() -> list[dict]:
    if not URL_FILE.exists():
        raise FileNotFoundError(f"URL 파일이 없습니다: {URL_FILE}")

    with URL_FILE.open("r", encoding="utf-8") as f:
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


def save_raw_document(doc: dict, text: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    doc_id = doc["id"]
    out_path = RAW_DIR / f"{doc_id}.txt"

    header = f"""# id: {doc.get("id", "")}
# title: {doc.get("title", "")}
# category: {doc.get("category", "")}
# source_url: {doc.get("url", "")}
# collected_by: collect_egov_wiki.py

"""

    out_path.write_text(header + text, encoding="utf-8")
    return out_path


def main() -> None:
    documents = load_documents()

    print(f"수집 대상 문서 수: {len(documents)}")
    print(f"저장 위치: {RAW_DIR}")

    success_count = 0
    fail_count = 0

    for doc in tqdm(documents, desc="Collecting eGovFrame Wiki"):
        try:
            export_url = to_export_raw_url(doc["url"])
            text = fetch_text(export_url)

            if not text.strip():
                raise ValueError("수집된 본문이 비어 있습니다.")

            out_path = save_raw_document(doc, text)
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


if __name__ == "__main__":
    main()