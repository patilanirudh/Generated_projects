"""
openai-board-news-feeder — surfaces the latest OpenAI news from Hacker News
and the OpenAI blog, with optional local caching.
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

CACHE_PATH = Path.home() / ".cache" / "openai-news.json"
CACHE_TTL_SECONDS = 1800
HN_API = "https://hn.algolia.com/api/v1/search"
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "WARNING"),
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger(__name__)


def _get_with_retry(url: str, params: dict | None = None) -> requests.Response:
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            if attempt == MAX_RETRIES - 1:
                raise
            wait = 2 ** attempt
            log.debug("Request failed (%s), retrying in %ds", exc, wait)
            time.sleep(wait)
    raise RuntimeError("unreachable")  # satisfies type checker


def _load_cache() -> Optional[list[dict]]:
    if not CACHE_PATH.exists():
        return None
    try:
        data = json.loads(CACHE_PATH.read_text())
        if time.time() - data.get("ts", 0) < CACHE_TTL_SECONDS:
            return data["articles"]
    except (json.JSONDecodeError, KeyError, OSError):
        pass
    return None


def _save_cache(articles: list[dict]) -> None:
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(json.dumps({"ts": time.time(), "articles": articles}))
    except OSError as exc:
        log.warning("Could not write cache: %s", exc)


def fetch_hn_articles(query: str = "OpenAI", count: int = 20) -> list[dict]:
    resp = _get_with_retry(HN_API, params={"query": query, "tags": "story", "hitsPerPage": count})
    articles = []
    for hit in resp.json().get("hits", []):
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}"
        articles.append({
            "title": hit.get("title", ""),
            "url": url,
            "source": "Hacker News",
            "points": hit.get("points", 0),
            "comments": hit.get("num_comments", 0),
            "date": hit.get("created_at", ""),
        })
    return articles


def fetch_openai_blog(count: int = 10) -> list[dict]:
    try:
        resp = _get_with_retry("https://openai.com/blog")
        soup = BeautifulSoup(resp.text, "html.parser")
        seen_urls: set[str] = set()
        articles = []
        for tag in soup.select("a[href^='/blog/']"):
            href = tag["href"]
            title = tag.get_text(strip=True)
            full_url = f"https://openai.com{href}"
            if title and len(title) > 5 and full_url not in seen_urls:
                seen_urls.add(full_url)
                articles.append({
                    "title": title,
                    "url": full_url,
                    "source": "OpenAI Blog",
                    "points": None,
                    "comments": None,
                    "date": "",
                })
            if len(articles) >= count:
                break
        return articles
    except requests.RequestException as exc:
        log.warning("Could not fetch OpenAI blog: %s", exc)
        return []


def get_articles(query: str = "OpenAI", use_cache: bool = True, count: int = 20) -> list[dict]:
    if use_cache:
        cached = _load_cache()
        if cached is not None:
            log.debug("Returning %d articles from cache", len(cached))
            return cached

    articles: list[dict] = []
    try:
        articles.extend(fetch_hn_articles(query=query, count=count))
    except requests.RequestException as exc:
        log.error("Hacker News fetch failed: %s", exc)

    seen = {a["url"] for a in articles}
    for a in fetch_openai_blog(count=10):
        if a["url"] not in seen:
            articles.append(a)
            seen.add(a["url"])

    if use_cache and articles:
        _save_cache(articles)

    return articles


def print_articles(articles: list[dict], limit: int = 15, fmt: str = "text") -> None:
    displayed = articles[:limit]

    if fmt == "json":
        print(json.dumps(displayed, indent=2))
        return

    if not displayed:
        print("No articles found.", file=sys.stderr)
        return

    width = 80
    print("=" * width)
    print(f"  OpenAI News Feed")
    print("=" * width)

    for i, article in enumerate(displayed, 1):
        title = article.get("title") or "(no title)"
        if len(title) > width - 6:
            title = title[: width - 9] + "..."
        print(f"\n{i:2}. {title}")
        print(f"    {article['url']}")
        meta: list[str] = [f"[{article['source']}]"]
        if article.get("points") is not None:
            meta.append(f"{article['points']} pts")
        if article.get("comments") is not None:
            meta.append(f"{article['comments']} comments")
        if article.get("date"):
            meta.append(article["date"][:10])
        print(f"    {' · '.join(meta)}")

    print("\n" + "=" * width)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch and display the latest OpenAI news.",
    )
    parser.add_argument("-n", "--count", type=int, default=15,
                        help="Number of articles to display (default: 15)")
    parser.add_argument("-q", "--query", default="OpenAI",
                        help="Hacker News search query (default: OpenAI)")
    parser.add_argument("--no-cache", action="store_true",
                        help="Skip local cache and fetch fresh results")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose logging")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        articles = get_articles(
            query=args.query,
            use_cache=not args.no_cache,
            count=args.count,
        )
    except Exception as exc:
        log.error("Failed to fetch articles: %s", exc)
        return 1

    print_articles(articles, limit=args.count, fmt=args.format)
    return 0


if __name__ == "__main__":
    sys.exit(main())
