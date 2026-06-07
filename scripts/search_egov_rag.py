import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    for source in ["migration", "rte43"]:
        print(f"\n===== SOURCE: {source} =====\n")
        subprocess.run([
            "python",
            str(BASE_DIR / "scripts" / "search_chunks.py"),
            "--source",
            source,
            "--query",
            args.query,
            "--top-k",
            str(args.top_k),
        ], cwd=BASE_DIR)

if __name__ == "__main__":
    main()