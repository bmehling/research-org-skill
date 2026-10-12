#!/usr/bin/env python3
"""
find_stale.py — list database entries whose research has gone stale.

An update flag you have to remember to run is a flag that rarely runs. This
produces the worklist: which entries are oldest, which are worth refreshing, and
the exact command to refresh each one.

Usage:
  python find_stale.py                      # default: stale = older than 6 months
  python find_stale.py --months 12
  python find_stale.py --fast               # skip per-page reads, use created time
  python find_stale.py --limit 10 --json

Dating an entry:
  Reports written since the metadata line was introduced carry
  "*Research completed: YYYY-MM-DD. Last updated: YYYY-MM-DD.*" above the first
  heading. That line is authoritative and this reads the latest date on it.
  Older reports have no such line, so the page's Notion creation time is used
  instead and the row is marked `created`.

  --fast skips reading pages entirely and dates everything by creation time. It
  is one API call per hundred rows instead of one per row, but it will call an
  entry stale that was in fact updated last week, because a page's creation time
  never moves. Use it for a rough scan, not for deciding what to spend a run on.

Terminal entries (Stage of Defunct or Acquired) are excluded by default. Their
reports are frozen by design and do not go stale.
"""

import argparse
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Use /usr/bin/python3, or: pip install requests",
          file=sys.stderr)
    sys.exit(1)

NOTION_BASE_URL = "https://api.notion.com/v1"
NOTION_API_VERSION = "2022-06-28"
TERMINAL_STAGES = {"Defunct", "Acquired"}

MONTHS = ("january february march april may june july august september "
          "october november december").split()

DATE_PATTERNS = [
    (re.compile(r'(\d{4})-(\d{2})-(\d{2})'),
     lambda m: (int(m.group(1)), int(m.group(2)), int(m.group(3)))),
    (re.compile(r'([A-Za-z]{3,9})\s+(\d{1,2}),?\s+(\d{4})'),
     lambda m: (int(m.group(3)), _month(m.group(1)), int(m.group(2)))),
    (re.compile(r'(\d{1,2})\s+([A-Za-z]{3,9})\s+(\d{4})'),
     lambda m: (int(m.group(3)), _month(m.group(2)), int(m.group(1)))),
]

RESEARCH_LINE = re.compile(r'research\s+completed', re.I)
MODEL_TAG = re.compile(r'\[([^\]]+)\]')


def _month(name: str) -> int:
    n = name.lower()
    for i, full in enumerate(MONTHS, start=1):
        if full.startswith(n[:3]):
            return i
    return 0


class RateLimiter:
    """Notion allows roughly three requests per second. Exceed it and you get 429s."""

    def __init__(self, per_second: float = 2.5):
        self._interval = 1.0 / per_second
        self._lock = threading.Lock()
        self._next = 0.0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            if now < self._next:
                time.sleep(self._next - now)
                now = time.monotonic()
            self._next = now + self._interval


def load_config(config_path: Optional[Path]) -> Dict:
    config_file = Path(config_path) if config_path else Path(__file__).parent.parent / "config.json"
    if not config_file.exists():
        print(f"ERROR: config.json not found at {config_file}", file=sys.stderr)
        sys.exit(1)
    with open(config_file) as f:
        return json.load(f)


def api(method: str, path: str, key: str, limiter: RateLimiter, **kw) -> Dict:
    headers = {
        "Authorization": f"Bearer {key}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }
    for attempt in range(4):
        limiter.wait()
        r = requests.request(method, f"{NOTION_BASE_URL}{path}",
                             headers=headers, timeout=30, **kw)
        if r.status_code == 429:
            time.sleep(float(r.headers.get("Retry-After", 2)))
            continue
        if r.status_code != 200:
            raise RuntimeError(f"{r.status_code}: {r.text[:200]}")
        return r.json()
    raise RuntimeError("rate limited after retries")


def fetch_rows(db_id: str, key: str, limiter: RateLimiter) -> List[Dict]:
    rows, cursor = [], None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        d = api("POST", f"/databases/{db_id}/query", key, limiter, data=json.dumps(body))
        for r in d["results"]:
            p = r["properties"]
            title = p.get("Organization", {}).get("title", [])
            rows.append({
                "id": r["id"],
                "name": title[0]["plain_text"] if title else "(untitled)",
                "url": p.get("URL", {}).get("url") or "",
                "stage": [o["name"] for o in p.get("Stage", {}).get("multi_select", [])],
                "created": r["created_time"][:10],
            })
        if not d.get("has_more"):
            break
        cursor = d["next_cursor"]
    return rows


def parse_dates(text: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (latest ISO date on the research line, model tag) or (None, None)."""
    for line in text.splitlines():
        if not RESEARCH_LINE.search(line):
            continue
        found = []
        for pat, conv in DATE_PATTERNS:
            for m in pat.finditer(line):
                y, mo, d = conv(m)
                if 1 <= mo <= 12 and 1 <= d <= 31 and 2000 <= y <= 2100:
                    found.append(f"{y:04d}-{mo:02d}-{d:02d}")
        if found:
            tag = MODEL_TAG.search(line)
            return max(found), (tag.group(1) if tag else None)
    return None, None


def read_metadata(page_id: str, key: str, limiter: RateLimiter) -> Tuple[Optional[str], Optional[str]]:
    """Read the first few blocks of a page looking for the metadata line."""
    try:
        d = api("GET", f"/blocks/{page_id}/children?page_size=5", key, limiter)
    except Exception:
        return None, None
    chunks = []
    for b in d.get("results", []):
        body = b.get(b.get("type"), {})
        if isinstance(body, dict):
            for rt in body.get("rich_text", []) or []:
                chunks.append(rt.get("plain_text", ""))
            chunks.append("\n")
    return parse_dates("".join(chunks))


def months_between(iso: str, now: datetime) -> float:
    d = datetime.strptime(iso, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return (now - d).days / 30.44


def main() -> None:
    ap = argparse.ArgumentParser(
        description="List database entries whose research has gone stale.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--months", type=float, default=6.0,
                    help="Staleness threshold in months (default 6)")
    ap.add_argument("--limit", type=int, help="Show only the N stalest")
    ap.add_argument("--fast", action="store_true",
                    help="Skip per-page reads; date everything by page creation time")
    ap.add_argument("--include-terminal", action="store_true",
                    help="Include entries staged Defunct or Acquired")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--json", action="store_true", help="Machine-readable output")
    ap.add_argument("--config", help="Path to config.json (default: auto-find)")
    args = ap.parse_args()

    cfg = load_config(Path(args.config) if args.config else None)
    key = cfg.get("notion", {}).get("notion_api")
    db_id = (cfg.get("notion", {}).get("databaseId") or "").split("?")[0]
    if not key or not db_id:
        print("ERROR: notion.notion_api and notion.databaseId required in config.json",
              file=sys.stderr)
        sys.exit(1)

    limiter = RateLimiter()
    if not args.json:
        print("Fetching database rows...", file=sys.stderr)
    rows = fetch_rows(db_id, key, limiter)

    terminal = [r for r in rows if set(r["stage"]) & TERMINAL_STAGES]
    if not args.include_terminal:
        rows = [r for r in rows if not set(r["stage"]) & TERMINAL_STAGES]

    now_pre = datetime.now(timezone.utc)
    if not args.fast:
        # Only pages already past the threshold by creation time can possibly be
        # stale: a report's research date is never meaningfully earlier than the
        # page that holds it. Skipping the recent ones cuts the per-page reads
        # sharply, and cuts them further as more entries get updated.
        candidates = [r for r in rows
                      if months_between(r["created"], now_pre) >= args.months]
        for r in rows:
            r["researched"] = r["created"]
            r["source"] = "created"
            r["tag"] = None
        if not args.json:
            print(f"Reading metadata lines from {len(candidates)} candidate pages "
                  f"of {len(rows)} (rate limited, ~{len(candidates)/2.5:.0f}s)...",
                  file=sys.stderr)
        if candidates:
            with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
                metas = list(pool.map(
                    lambda r: read_metadata(r["id"], key, limiter), candidates))
            for r, (date, tag) in zip(candidates, metas):
                if date:
                    r["researched"] = date
                    r["source"] = "metadata"
                r["tag"] = tag
    else:
        for r in rows:
            r["researched"] = r["created"]
            r["source"] = "created"
            r["tag"] = None

    now = datetime.now(timezone.utc)
    for r in rows:
        r["age_months"] = months_between(r["researched"], now)

    stale = sorted([r for r in rows if r["age_months"] >= args.months],
                   key=lambda r: -r["age_months"])
    shown = stale[:args.limit] if args.limit else stale

    if args.json:
        print(json.dumps({
            "scanned": len(rows),
            "threshold_months": args.months,
            "stale_count": len(stale),
            "terminal_skipped": len(terminal) if not args.include_terminal else 0,
            "entries": [{k: r[k] for k in
                         ("name", "url", "id", "stage", "researched", "source",
                          "age_months", "tag")} for r in shown],
        }, indent=2, default=str))
        return

    print()
    print(f"Stale entries: research older than {args.months:g} months "
          f"({len(stale)} of {len(rows)} scanned)")
    if not args.include_terminal and terminal:
        print(f"Skipped {len(terminal)} terminal entries (Defunct or Acquired).")
    print()

    if not shown:
        print("Nothing is stale. Everything has been researched within the threshold.")
        return

    print(f"{'AGE':>5}  {'ORGANIZATION':<28} {'STAGE':<14} {'RESEARCHED':<12} "
          f"{'DATED BY':<9} URL")
    print("-" * 110)
    for r in shown:
        stage = ", ".join(r["stage"]) or "-"
        print(f"{r['age_months']:>4.0f}m  {r['name'][:28]:<28} {stage[:14]:<14} "
              f"{r['researched']:<12} {r['source']:<9} {r['url'][:34]}")

    if args.limit and len(stale) > args.limit:
        print(f"\n... and {len(stale) - args.limit} more.")

    by_created = sum(1 for r in shown if r["source"] == "created")
    if by_created:
        print(f"\nNote: {by_created} of these were dated by page creation time because "
              f"the report predates the metadata line. Their true research date may be "
              f"later, so the age shown is an upper bound.")

    top = shown[0]
    print(f"\nRefresh the stalest with:")
    print(f"  /research-org-skill --update {top['url'] or top['id']}")


if __name__ == "__main__":
    main()
