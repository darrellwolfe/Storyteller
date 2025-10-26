#!/usr/bin/env python3
"""
Generate the posts list inside docs/index.html by scanning docs/posts/*.html.

Usage:
  python3 scripts/generate_index.py

This script looks for markers <!-- POSTS_START --> and <!-- POSTS_END --> in
docs/index.html and replaces the HTML between them with a generated
<ul class="post-list">...</ul> containing one <li> per post file.
"""
from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
POSTS_DIR = DOCS / "posts"
INDEX_HTML = DOCS / "index.html"


def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).strip()


def parse_post(path: Path) -> Tuple[Optional[datetime], str, str, str]:
    """Return (date, title, summary, relpath)

    date is a datetime (or None), title is string, summary is string, relpath is URL path
    """
    text = path.read_text(encoding="utf-8")

    # Title: first <h1> or <h2>
    m = re.search(r"<h[12][^>]*>(.*?)</h[12]>", text, re.S | re.I)
    title = strip_tags(m.group(1)) if m else path.stem

    # Time: <time datetime="YYYY-MM-DD"> or text inside <time>
    time_m = re.search(r"<time[^>]*datetime=[\"']([^\"']+)[\"'][^>]*>(.*?)</time>", text, re.S | re.I)
    date = None
    if time_m:
        dt_text = time_m.group(1)
        try:
            date = datetime.fromisoformat(dt_text)
        except Exception:
            try:
                date = datetime.fromisoformat(dt_text.split()[0])
            except Exception:
                date = None

    # Summary: first paragraph <p> after the intro
    p_m = re.search(r"<p>(.*?)</p>", text, re.S | re.I)
    summary = strip_tags(p_m.group(1)) if p_m else ""

    relpath = f"/docs/posts/{path.name}"
    return date, title, summary, relpath


def find_posts() -> List[Tuple[Optional[datetime], str, str, str]]:
    posts = []
    for f in sorted(POSTS_DIR.glob("*.html")):
        posts.append(parse_post(f))
    # sort by date desc; None dates go last, preserve file order for ties
    posts.sort(key=lambda t: (t[0] is None, t[0] if t[0] is not None else datetime.min), reverse=True)
    return posts


def render_posts_html(posts: List[Tuple[Optional[datetime], str, str, str]]) -> str:
    items = []
    for date, title, summary, relpath in posts:
        date_attr = date.date().isoformat() if date else ""
        date_text = date.date().strftime("%b %d, %Y") if date else ""
        date_html = f"<time datetime=\"{date_attr}\">{date_text}</time>" if date else ""
        summary_html = f"<p>{summary}</p>" if summary else ""
        items.append("""
          <li>
            <article>
              <h3><a href="{relpath}">{title}</a></h3>
              {date_html}
              {summary_html}
            </article>
          </li>""".format(relpath=relpath, title=title, date_html=date_html, summary_html=summary_html))
    return "\n".join(items)


def main() -> int:
    if not INDEX_HTML.exists():
        print(f"Index file not found: {INDEX_HTML}")
        return 2

    s = INDEX_HTML.read_text(encoding="utf-8")

    start_marker = "<!-- POSTS_START -->"
    end_marker = "<!-- POSTS_END -->"

    if start_marker not in s or end_marker not in s:
        print("Markers not found in index.html. Please add <!-- POSTS_START --> and <!-- POSTS_END --> around the posts area.")
        return 3

    posts = find_posts()
    new_items = render_posts_html(posts)

    # Replace content between markers (exclusive)
    pre, rest = s.split(start_marker, 1)
    _, post = rest.split(end_marker, 1)

    new_section = f"{start_marker}\n  <ul class=\"post-list\">\n{new_items}\n  </ul>\n{end_marker}"

    new_s = pre + new_section + post

    INDEX_HTML.write_text(new_s, encoding="utf-8")
    print(f"Updated {INDEX_HTML} with {len(posts)} post(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
