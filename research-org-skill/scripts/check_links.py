#!/usr/bin/env python3
"""
check_links.py — find dead citations in a research report.

Reports carry 25-80 source links and some rot over time. This checks them and,
crucially, distinguishes "this page is gone" from "this server refused a bot."
Only the first is actionable.

Usage:
  python check_links.py --content report.md
  python check_links.py --page-id 3de5d08590e981fda482f244a4517e09
  python check_links.py --content report.md --all --strict

Classification:
  OK          2xx. Reachable.
  REDIRECT    3xx to a different host. The citation still resolves but the
              destination moved; worth a look on a rebrand.
  DEAD        404 or 410, or DNS failure. Actionable: replace the citation.
  BLOCKED     401, 403, 429, 999. The server refused automated access. This is
              NOT evidence the page is gone. Never drop a citation on a BLOCKED
              result. Hosts behind a login or paywall are labeled as such:
              a browser retry there returns a sign-in page, not the source.
  SERVER_ERR  5xx. Usually transient. Re-check before acting.
  TIMEOUT     No response in time. Usually transient.

Exit code is 0 unless --strict is passed and at least one DEAD link was found.
"""

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Use /usr/bin/python3, or: pip install requests",
          file=sys.stderr)
    sys.exit(1)

NOTION_BASE_URL = "https://api.notion.com/v1"
NOTION_API_VERSION = "2022-06-28"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")

# The full header set a real browser sends on navigation. A browser user-agent
# paired with "Accept: */*" and nothing else is itself a bot signal, so some
# WAFs that 403 the bare request let this one through. It does nothing against
# JavaScript challenges (Cloudflare, Akamai), which need a real browser.
BROWSER_HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

# Hosts where a browser retry cannot help: the page sits behind a login or
# paywall, so Chrome loads a 200 sign-in page that reads as success but is not
# the cited content. LinkedIn would also browse as the user's own account.
LOGIN_WALLED = ("linkedin.com", "pitchbook.com", "crunchbase.com",
                "gartner.com", "forrester.com", "cbinsights.com")


def login_walled(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return any(host == d or host.endswith("." + d) for d in LOGIN_WALLED)

MD_LINK = re.compile(r'\[[^\]]*\]\((https?://[^)\s]+)\)')
HTML_HREF = re.compile(r'href=["\'](https?://[^"\']+)["\']')
BARE_URL = re.compile(r'(?<![\(\["\'])\bhttps?://[^\s<>\)\]"\']+')


def load_config(config_path: Optional[Path]) -> Dict:
    """Load config.json. Mirrors upload_to_notion.py's auto-find behavior."""
    config_file = Path(config_path) if config_path else Path(__file__).parent.parent / "config.json"
    if not config_file.exists():
        print(f"ERROR: config.json not found at {config_file}", file=sys.stderr)
        sys.exit(1)
    with open(config_file) as f:
        return json.load(f)


def extract_urls(text: str) -> List[str]:
    """Pull every http(s) URL out of markdown or HTML, preserving first-seen order."""
    found: List[str] = []
    for pat in (MD_LINK, HTML_HREF, BARE_URL):
        for m in pat.finditer(text):
            u = m.group(1) if pat is not BARE_URL else m.group(0)
            found.append(u.rstrip('.,;:'))
    seen, out = set(), []
    for u in found:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def fetch_page_text(page_id: str, api_key: str) -> str:
    """Concatenate all text and link URLs from a Notion page, recursing into children."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_API_VERSION,
    }
    chunks: List[str] = []

    def walk(block_id: str, depth: int = 0) -> None:
        if depth > 4:
            return
        cursor = None
        while True:
            params = {"page_size": 100}
            if cursor:
                params["start_cursor"] = cursor
            r = requests.get(f"{NOTION_BASE_URL}/blocks/{block_id}/children",
                             headers=headers, params=params, timeout=30)
            if r.status_code != 200:
                print(f"ERROR: Notion API {r.status_code}: {r.text[:200]}", file=sys.stderr)
                sys.exit(1)
            data = r.json()
            for b in data.get("results", []):
                body = b.get(b.get("type"), {})
                if isinstance(body, dict):
                    for rt in body.get("rich_text", []) or []:
                        chunks.append(rt.get("plain_text", ""))
                        href = rt.get("href")
                        if href:
                            chunks.append(f" {href} ")
                    for key in ("url", "external"):
                        v = body.get(key)
                        if isinstance(v, str):
                            chunks.append(f" {v} ")
                        elif isinstance(v, dict) and v.get("url"):
                            chunks.append(f" {v['url']} ")
                if b.get("has_children"):
                    walk(b["id"], depth + 1)
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")

    walk(page_id)
    return "\n".join(chunks)


def classify(url: str, timeout: int) -> Tuple[str, str]:
    """Return (status_label, detail). HEAD first; many servers reject it, so fall back to GET."""
    headers = BROWSER_HEADERS
    try:
        r = requests.head(url, headers=headers, timeout=timeout,
                          allow_redirects=True)
        if r.status_code in (403, 405, 400, 501) or 500 <= r.status_code < 600:
            r = requests.get(url, headers=headers, timeout=timeout,
                             allow_redirects=True, stream=True)
            r.close()
    except requests.exceptions.Timeout:
        return "TIMEOUT", "no response"
    except requests.exceptions.SSLError as e:
        return "BLOCKED", f"ssl: {str(e)[:60]}"
    except requests.exceptions.ConnectionError as e:
        msg = str(e)
        if "NameResolutionError" in msg or "nodename nor servname" in msg or "Name or service not known" in msg:
            return "DEAD", "dns: host does not resolve"
        return "UNREACHABLE", f"connection: {msg[:60]}"
    except Exception as e:
        return "UNREACHABLE", f"{type(e).__name__}: {str(e)[:60]}"

    code = r.status_code
    if code in (404, 410):
        return "DEAD", f"HTTP {code}"
    # 451 = legal block. 999 = LinkedIn's bot-block code, which is not a 5xx
    # condition even though it sorts above one.
    if code in (401, 403, 429, 451, 999):
        hint = ("login wall, browser retry will not help" if login_walled(url)
                else "refused automation, not proof of removal")
        return "BLOCKED", f"HTTP {code} ({hint})"
    if code >= 500:
        return "SERVER_ERR", f"HTTP {code}"
    if 200 <= code < 300:
        final = r.url
        if urlparse(final).netloc != urlparse(url).netloc:
            return "REDIRECT", f"-> {final[:90]}"
        return "OK", f"HTTP {code}"
    return "UNREACHABLE", f"HTTP {code}"


ORDER = ["DEAD", "REDIRECT", "BLOCKED", "SERVER_ERR", "TIMEOUT", "UNREACHABLE", "OK"]


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Check report citations for rot.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--content", help="Path to a markdown report")
    src.add_argument("--page-id", help="Notion page UUID to read links from")
    ap.add_argument("--config", help="Path to config.json (default: auto-find)")
    ap.add_argument("--timeout", type=int, default=12, help="Per-request timeout (default 12)")
    ap.add_argument("--concurrency", type=int, default=8, help="Parallel requests (default 8)")
    ap.add_argument("--all", action="store_true", help="List OK links too")
    ap.add_argument("--strict", action="store_true", help="Exit 1 if any DEAD link found")
    args = ap.parse_args()

    if args.content:
        path = Path(args.content)
        if not path.exists():
            print(f"ERROR: {path} not found", file=sys.stderr)
            sys.exit(1)
        text = path.read_text()
        source = str(path)
    else:
        cfg = load_config(Path(args.config) if args.config else None)
        key = cfg.get("notion", {}).get("notion_api")
        if not key:
            print("ERROR: notion.notion_api not set in config.json", file=sys.stderr)
            sys.exit(1)
        text = fetch_page_text(args.page_id.replace("-", ""), key)
        source = f"Notion page {args.page_id}"

    urls = extract_urls(text)
    if not urls:
        print(f"No links found in {source}.")
        return

    print(f"🔗 Checking {len(urls)} unique links from {source}\n")

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        results = list(pool.map(lambda u: (u, *classify(u, args.timeout)), urls))

    buckets: Dict[str, List[Tuple[str, str]]] = {k: [] for k in ORDER}
    for url, label, detail in results:
        buckets[label].append((url, detail))

    for label in ORDER:
        rows = buckets[label]
        if not rows:
            continue
        if label == "OK" and not args.all:
            continue
        print(f"{label}  ({len(rows)})")
        for url, detail in rows:
            print(f"   {url}")
            print(f"      {detail}")
        print()

    dead = len(buckets["DEAD"])
    blocked = len(buckets["BLOCKED"])
    ok = len(buckets["OK"])
    print(f"Summary: {ok} ok · {dead} dead · {blocked} blocked · "
          f"{len(urls) - ok - dead - blocked} other")

    if blocked:
        print("\nNote: BLOCKED means the server refused an automated request. "
              "That is not evidence the page is gone, so never drop a citation "
              "on it. Retry in Chrome only when the link is the sole source "
              "for a load-bearing fact, and never for a login-walled host.")
    if dead:
        print(f"\nAction: {dead} citation(s) need replacing.")

    if args.strict and dead:
        sys.exit(1)


if __name__ == "__main__":
    main()
