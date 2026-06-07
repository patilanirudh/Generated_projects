"""
openai-plugin-downloader — discover and download ChatGPT/OpenAI plugin repos
from GitHub by topic search. Saves each plugin as a zip archive locally.
"""

import argparse
import logging
import os
import sys
import time
import zipfile
from pathlib import Path

import requests

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "WARNING"),
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger(__name__)

GITHUB_API   = "https://api.github.com"
PLUGIN_TOPIC = "chatgpt-plugin"
REQUEST_TIMEOUT = 10
MAX_RETRIES     = 3
OUTPUT_DIR      = Path(os.environ.get("OUTPUT_DIR", "./plugins"))


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _headers() -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _get(url: str, params: dict | None = None) -> requests.Response:
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, headers=_headers(), params=params, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            if attempt == MAX_RETRIES - 1:
                raise
            wait = 2 ** attempt
            log.debug("Request failed (%s), retrying in %ds", exc, wait)
            time.sleep(wait)
    raise RuntimeError("unreachable")


# ---------------------------------------------------------------------------
# Plugin discovery
# ---------------------------------------------------------------------------

def search_plugins(query: str = "", limit: int = 20) -> list[dict]:
    """Search GitHub for repos tagged with the chatgpt-plugin topic."""
    q = f"topic:{PLUGIN_TOPIC}"
    if query:
        q += f" {query} in:name,description"

    resp = _get(f"{GITHUB_API}/search/repositories", params={"q": q, "per_page": limit, "sort": "stars"})
    items = resp.json().get("items", [])

    return [
        {
            "name":        item["full_name"],
            "description": item.get("description") or "",
            "stars":       item["stargazers_count"],
            "url":         item["html_url"],
            "zip_url":     f"{GITHUB_API}/repos/{item['full_name']}/zipball/HEAD",
            "language":    item.get("language") or "unknown",
        }
        for item in items
    ]


# ---------------------------------------------------------------------------
# Plugin download
# ---------------------------------------------------------------------------

def download_plugin(plugin: dict, output_dir: Path) -> Path:
    """Download a plugin repo as a zip and save it to output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = plugin["name"].replace("/", "_")
    dest = output_dir / f"{safe_name}.zip"

    if dest.exists():
        log.info("Already downloaded: %s", dest)
        return dest

    log.info("Downloading %s ...", plugin["name"])
    resp = _get(plugin["zip_url"])

    dest.write_bytes(resp.content)

    # Validate it's a real zip
    if not zipfile.is_zipfile(dest):
        dest.unlink()
        raise RuntimeError(f"Downloaded file for {plugin['name']} is not a valid zip.")

    return dest


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> int:
    try:
        plugins = search_plugins(query=args.query, limit=args.limit)
    except requests.RequestException as exc:
        log.error("GitHub search failed: %s", exc)
        return 1

    if not plugins:
        print("No plugins found.")
        return 0

    width = 60
    print(f"\n{'Plugin':<{width}}  {'Stars':>6}  Language")
    print("-" * (width + 20))
    for p in plugins:
        name = p["name"] if len(p["name"]) <= width else p["name"][:width - 3] + "..."
        print(f"{name:<{width}}  {p['stars']:>6}  {p['language']}")
        if p["description"]:
            print(f"  {p['description'][:width + 16]}")
    print()
    return 0


def cmd_download(args: argparse.Namespace) -> int:
    try:
        plugins = search_plugins(query=args.query, limit=args.limit)
    except requests.RequestException as exc:
        log.error("GitHub search failed: %s", exc)
        return 1

    if not plugins:
        print("No plugins found matching your query.")
        return 0

    out = Path(args.output)
    failed = 0
    for plugin in plugins:
        try:
            dest = download_plugin(plugin, out)
            print(f"  OK  {dest}")
        except (requests.RequestException, RuntimeError) as exc:
            log.error("Failed to download %s: %s", plugin["name"], exc)
            failed += 1

    if failed:
        print(f"\n{failed} plugin(s) failed to download.", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Discover and download ChatGPT/OpenAI plugin repos from GitHub.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python app.py list\n"
            "  python app.py list --query weather --limit 10\n"
            "  python app.py download --query weather --output ./plugins\n"
            "  GITHUB_TOKEN=ghp_... python app.py list\n"
        ),
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    list_p = sub.add_parser("list", help="List matching plugins without downloading")
    list_p.add_argument("--query", default="", help="Filter plugins by name/description keyword")
    list_p.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")

    dl_p = sub.add_parser("download", help="Download matching plugin repos as zip archives")
    dl_p.add_argument("--query", default="", help="Filter plugins by keyword")
    dl_p.add_argument("--limit", type=int, default=5, help="Max plugins to download (default: 5)")
    dl_p.add_argument("--output", default=str(OUTPUT_DIR), help=f"Output directory (default: {OUTPUT_DIR})")

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.command == "list":
        return cmd_list(args)
    return cmd_download(args)


if __name__ == "__main__":
    sys.exit(main())
