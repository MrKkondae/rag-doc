import argparse
import re
import time
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup
from tqdm import tqdm


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_CHOICES = ["migration", "rte43", "com43", "dev43"]

BASE_DOMAIN = "www.egovframe.go.kr"
BASE_WIKI_URL = "https://www.egovframe.go.kr/wiki/doku.php"

REQUEST_DELAY_SECONDS = 1.0
TIMEOUT_SECONDS = 20

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
    "common_component",
    "inspection",
    "compa",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover eGovFrame Wiki links for a selected source."
    )
    parser.add_argument(
        "--source",
        required=True,
        choices=SOURCE_CHOICES,
        help="Knowledge base name to discover links from",
    )
    return parser.parse_args()


def normalize_page_id(page_id: str) -> str:
    page_id = page_id.strip()
    page_id = page_id.split("#")[0]
    return page_id


def classify_page_id(page_id: str, source: str) -> tuple[bool, str | None]:
    page_id = normalize_page_id(page_id)

    if not page_id:
        return False, "empty_page_id"

    for keyword in DENY_ID_KEYWORDS:
        if keyword in page_id:
            return False, f"denied_keyword:{keyword}"

    if source == "rte43":
        if page_id.startswith("egovframework:rte2"):
            return False, "excluded_prefix:rte2"
        if page_id.startswith("egovframework:mrte"):
            return False, "excluded_prefix:mrte"
        if page_id.startswith("egovframework:bopr"):
            return False, "excluded_prefix:bopr"
        if page_id.startswith("egovframework:dev"):
            return False, "excluded_prefix:dev"
        if page_id.startswith("egovframework:rte4"):
            return True, None
        if page_id.startswith("egovframework:rte3"):
            return True, None
        return False, "not_in_rte43_allowlist"

    return True, None


def load_seed_documents(seed_file: Path) -> list[dict]:
    if not seed_file.exists():
        raise FileNotFoundError(f"Seed URL file not found: {seed_file}")

    with seed_file.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    documents = config.get("documents", [])
    if not documents:
        raise ValueError("No seed documents found.")

    return documents


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
    doc_id = re.sub(r"[^a-z0-9-]+", "-", doc_id)
    doc_id = re.sub(r"-+", "-", doc_id).strip("-")
    return doc_id


def find_content_root(soup: BeautifulSoup):
    content = soup.find(id="dokuwiki__content")
    if content:
        return content

    page = soup.find(class_="page")
    if page:
        return page

    dokuwiki = soup.find(class_="dokuwiki")
    if dokuwiki:
        return dokuwiki

    print("[WARN] Content root not found. Falling back to the full page.")
    return soup


def remove_toc_blocks(content_root) -> None:
    for toc in content_root.select(".toc, #dw__toc, .tocheader"):
        toc.decompose()


def discover_links_from_page(url: str, source: str) -> tuple[dict[str, str], Counter]:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    content_root = find_content_root(soup)
    remove_toc_blocks(content_root)

    discovered = {}
    excluded_counts = Counter()

    for a in content_root.find_all("a", href=True):
        href = a["href"]
        absolute_url = urljoin(url, href)
        page_id = extract_page_id_from_url(absolute_url)

        if not page_id:
            continue

        is_allowed, reason = classify_page_id(page_id, source)
        if not is_allowed:
            if reason:
                excluded_counts[reason] += 1
            continue

        title = a.get_text(" ", strip=True) or page_id
        discovered[page_id] = title

    return discovered, excluded_counts


def save_discovered_documents(documents: list[dict], out_file: Path) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with out_file.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            {"documents": documents},
            f,
            allow_unicode=True,
            sort_keys=False,
        )


def main() -> None:
    args = parse_args()
    source = args.source
    seed_file = BASE_DIR / "urls" / f"{source}_urls.yml"
    out_file = BASE_DIR / "urls" / f"{source}_discovered_urls.yml"
    seed_docs = load_seed_documents(seed_file)

    print(f"source: {source}")
    print(f"seed file: {seed_file.relative_to(BASE_DIR)}")
    print(f"output file: {out_file.relative_to(BASE_DIR)}")

    discovered_pages: dict[str, dict] = {}
    excluded_counts = Counter()

    for doc in seed_docs:
        seed_page_id = extract_page_id_from_url(doc["url"])
        if seed_page_id:
            is_allowed, reason = classify_page_id(seed_page_id, source)
            if not is_allowed:
                if reason:
                    excluded_counts[f"seed:{reason}"] += 1
                continue
            discovered_pages[seed_page_id] = {
                "id": make_doc_id(seed_page_id),
                "title": doc.get("title", seed_page_id),
                "category": doc.get("category", "seed"),
                "url": to_normal_url(seed_page_id),
                "page_id": seed_page_id,
            }

    for doc in tqdm(seed_docs, desc="Discovering links"):
        try:
            links, page_excluded_counts = discover_links_from_page(doc["url"], source)
            excluded_counts.update(page_excluded_counts)

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
    save_discovered_documents(documents, out_file)

    print()
    print(f"Discovered documents: {len(documents)}")
    print(f"Output file: {out_file.relative_to(BASE_DIR)}")
    if excluded_counts:
        print("Excluded page_id summary:")
        for reason, count in sorted(excluded_counts.items()):
            print(f"- {reason}: {count}")


if __name__ == "__main__":
    main()
