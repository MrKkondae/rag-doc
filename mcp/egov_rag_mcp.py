import logging
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("egov-rag")

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "egov-rag-mcp.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
LOGGER = logging.getLogger("egov_rag_mcp_legacy")
LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False

if not LOGGER.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    LOGGER.addHandler(file_handler)


@mcp.tool()
def search_egov_rag(query: str, top_k: int = 5) -> str:
    """
    Search eGovFrame RAG documents for migration and rte43 sources.
    Use this before converting eGovFrame 3.x code to eGovFrame 4.3.
    """
    LOGGER.info("search_egov_rag called query=%r top_k=%s", query, top_k)
    outputs = []

    for source in ["migration", "rte43"]:
        cmd = [
            sys.executable,
            str(BASE_DIR / "scripts" / "search_chunks.py"),
            "--source",
            source,
            "--query",
            query,
            "--top-k",
            str(top_k),
        ]

        LOGGER.info("running source=%s cmd=%s", source, cmd)

        try:
            result = subprocess.run(
                cmd,
                cwd=BASE_DIR,
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception:
            LOGGER.exception("subprocess failed source=%s", source)
            raise

        LOGGER.info(
            "source=%s returncode=%s stdout_len=%s stderr_len=%s",
            source,
            result.returncode,
            len(result.stdout),
            len(result.stderr),
        )

        outputs.append(f"\n===== SOURCE: {source} =====\n")
        outputs.append(result.stdout)

        if result.stderr:
            outputs.append("\n[stderr]\n")
            outputs.append(result.stderr)

    return "\n".join(outputs)


if __name__ == "__main__":
    mcp.run()
