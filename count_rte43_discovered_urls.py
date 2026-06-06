from collections import Counter
import yaml

path = "urls/rte43_discovered_urls.yml"

with open(path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

print(f"loaded type: {type(data)}")

# YAML이 list인지 dict인지 확인
if isinstance(data, dict):
    print(f"dict keys: {list(data.keys())}")
    docs = data.get("documents") or data.get("urls") or data.get("items") or []
else:
    docs = data or []

print(f"total docs: {len(docs)}")

counter = Counter()

for d in docs:
    page_id = str(d.get("page_id", ""))
    url = str(d.get("url", ""))

    text = f"{page_id} {url}".lower()

    if "dev4.3" in text or "dev43" in text:
        counter["dev4.3"] += 1
    elif "common_component" in text:
        counter["common_component"] += 1
    elif "inspection" in text:
        counter["inspection"] += 1
    elif "compa" in text:
        counter["compa"] += 1
    elif "rte4" in text or "rte4.3" in text:
        counter["rte4"] += 1
    elif "rte3" in text:
        counter["rte3"] += 1
    else:
        counter["other"] += 1
        print("[OTHER]", page_id, url)

print()
print("=== count result ===")
for k, v in counter.items():
    print(f"{k}: {v}")


allowed = []
excluded = []

for d in docs:
    page_id = str(d.get("page_id", "")).lower()

    if page_id.startswith("egovframework:rte4") or page_id.startswith("egovframework:rte3"):
        allowed.append(d)
    else:
        excluded.append(d)

print(f"allowed: {len(allowed)}")
print(f"excluded: {len(excluded)}")

print("\n=== excluded sample ===")
for d in excluded[:30]:
    print(d["page_id"])