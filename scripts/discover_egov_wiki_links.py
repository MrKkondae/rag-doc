#링크 추출 스크립트

import re
import time
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

import requests
import yaml
from bs4 import BeautifulSoup
from tqdm import tqdm


BASE_DIR = Path(__file__).resolve().parents[1]

SEED_FILE = BASE_DIR / "urls" / "egov43_urls.yml"
OUT_FILE = BASE_DIR / "urls" / "egov43_discovered_urls.yml"

BASE_DOMAIN = "www.egovframe.go.kr"
BASE_WIKI_URL = "https://www.egovframe.go.kr/wiki/doku.php"

REQUEST_DELAY_SECONDS = 1.0
TIMEOUT_SECONDS = 20

# 너무 넓게 긁지 않도록 4.3 관련 namespace 중심으로 제한
ALLOW_ID_PATTERNS = [
    r"^egovframework:dev4\.3",
    r"^egovframework:rte4\.3",
    r"^egovframework:rtemigration4\.3",
    r"^egovframework:com:v4\.3",
    r"^egovframework:dev:",
    r"^egovframework:rte:",
]

# 불필요한 action / 미디어 / 관리자 링크 제외
DENY_QUERY_KEYS = {
    "do", "rev", "idx", "media", "image", "ns", "sectok",
}

DENY_ID_KEYWORDS = [
    "wiki:",
    "playground:",
    "sidebar",
    "syntax",
    "login",
    "register",
]


def normalize_page_id(page_id: str) -> str:
    page_id = page_id.strip()
    page_id = page_id.split("#")[0]
    return page_id


def is_allowed_page_id(page_id: str) -> bool:
    page_id = normalize_page_id(page_id)

    if not page_id:
        return False

    for keyword in DENY_ID_KEYWORDS:
        if keyword in page_id:
            return False

    return any(re.search(pattern, page_id) for pattern in ALLOW_ID_PATTERNS)


def load_seed_documents() -> list[dict]:
    with SEED_FILE.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config.get("documents", [])


def fetch_html(url: str) -> str:
    response = requests.get(
        url,
        headers={"User-Agent": "egovframe-rag-link-discoverer/0.1"},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def extract_page_id_from_url(url: str) -> str | None:
    parsed = urlparse(url)

    if parsed.netloc and parsed.netloc != BASE_DOMAIN:
        return None

    if not parsed.path.endswith("/wiki/doku.php") and "doku.php" not in parsed.path:
        return None

    query = parse_qs(parsed.query)

    # do, media, image 등 액션 URL 제외
    if any(key in query for key in DENY_QUERY_KEYS):
        return None

    page_ids = query.get("id")
    if not page_ids:
        return None

    return normalize_page_id(page_ids[0])


def to_normal_url(page_id: str) -> str:
    query = urlencode({"id": page_id})
    return f"{BASE_WIKI_URL}?{query}"


def make_doc_id(page_id: str) -> str:
    doc_id = page_id.lower()
    doc_id = doc_id.replace(":", "-")
    doc_id = doc_id.replace(".", "-")
    doc_id = re.sub(r"[^a-z0-9가-힣_-]+", "-", doc_id)
    doc_id = re.sub(r"-+", "-", doc_id).strip("-")
    return doc_id


def discover_links_from_page(url: str) -> dict[str, str]:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    discovered = {}

    for a in soup.find_all("a", href=True):
        href = a["href"]
        absolute_url = urljoin(url, href)
        page_id = extract_page_id_from_url(absolute_url)

        if not page_id:
            continue

        if not is_allowed_page_id(page_id):
            continue

        title = a.get_text(" ", strip=True) or page_id
        discovered[page_id] = title

    return discovered


def main() -> None:
    seed_docs = load_seed_documents()

    discovered_pages: dict[str, dict] = {}

    # seed 자체도 포함
    for doc in seed_docs:
        seed_page_id = extract_page_id_from_url(doc["url"])
        if seed_page_id and is_allowed_page_id(seed_page_id):
            discovered_pages[seed_page_id] = {
                "id": make_doc_id(seed_page_id),
                "title": doc.get("title", seed_page_id),
                "category": doc.get("category", "seed"),
                "url": to_normal_url(seed_page_id),
                "page_id": seed_page_id,
            }

    for doc in tqdm(seed_docs, desc="Discovering links"):
        try:
            links = discover_links_from_page(doc["url"])

            for page_id, title in links.items():
                if page_id not in discovered_pages:
                    discovered_pages[page_id] = {
                        "id": make_doc_id(page_id),
                        "title": title,
                        "category": doc.get("category", "discovered"),
                        "url": to_normal_url(page_id),
                        "page_id": page_id,
                    }

            print(f"[OK] {doc['id']} - discovered {len(links)} links")

        except Exception as e:
            print(f"[FAIL] {doc.get('id', 'unknown')} - {e}")

        time.sleep(REQUEST_DELAY_SECONDS)

    documents = sorted(discovered_pages.values(), key=lambda x: x["page_id"])

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            {"documents": documents},
            f,
            allow_unicode=True,
            sort_keys=False,
        )

    print()
    print(f"발견된 문서 수: {len(documents)}")
    print(f"저장 파일: {OUT_FILE}")


if __name__ == "__main__":
    main()