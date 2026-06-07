#!/usr/bin/env python3
"""
Aetas Wealth — Insights index auto-builder.

Scans insights/posts/*.html, extracts metadata, and rebuilds the insights
list in insights/index.html between markers:

    <!-- AUTO-INSIGHTS-START -->
    ...replaced automatically...
    <!-- AUTO-INSIGHTS-END -->

Articles with a datePublished in the FUTURE are excluded from the index.
Upload future-dated articles and they appear automatically on their
scheduled date via the daily GitHub Action.

Run locally from repo root:
    py scripts\\build-insights-index.py

Per-article controls (optional, add to <head>):
    <meta name="aw-listed"      content="false">         hide from index
    <meta name="aw-categories"  content="iht pensions">  filter pills
    <meta name="aw-label"       content="Inheritance Tax"> card label
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

POSTS_DIR   = Path("insights/posts")
INDEX_FILE  = Path("insights/index.html")

START_MARKER = "<!-- AUTO-INSIGHTS-START -->"
END_MARKER   = "<!-- AUTO-INSIGHTS-END -->"


def extract_meta(html, name):
    m = re.search(rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"', html)
    return m.group(1).strip() if m else None

def extract_og(html, prop):
    m = re.search(rf'<meta\s+property="{re.escape(prop)}"\s+content="([^"]*)"', html)
    return m.group(1).strip() if m else None

def extract_json_ld_date(html):
    m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    return m.group(1)[:10] if m else None

def extract_h1(html):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else None

def format_display_date(iso_str):
    d = date.fromisoformat(iso_str)
    return f"{d.day} {d.strftime('%B')} {d.year}"

def parse_articles(posts_dir):
    articles = []
    today = date.today()

    for path in sorted(posts_dir.glob("*.html")):
        if path.name == "index.html":
            continue
        html = path.read_text(encoding="utf-8")

        # Hidden override
        listed = extract_meta(html, "aw-listed")
        if listed and listed.lower() == "false":
            continue

        # Date gating
        pub_iso = extract_json_ld_date(html)
        if pub_iso:
            pub_date = date.fromisoformat(pub_iso)
            if pub_date > today:
                print(f"  Skipping (future): {path.name} — scheduled {pub_iso}")
                continue
        else:
            pub_iso  = today.isoformat()
            pub_date = today

        title      = extract_h1(html) or extract_og(html, "og:title") or path.stem
        desc       = extract_meta(html, "description") or extract_og(html, "og:description") or ""
        label      = extract_meta(html, "aw-label") or "Insights"
        categories = extract_meta(html, "aw-categories") or ""

        articles.append({
            "slug":       path.name,
            "title":      title,
            "desc":       desc,
            "label":      label,
            "categories": categories,
            "pub_date":   pub_date,
            "pub_display": format_display_date(pub_iso),
        })

    articles.sort(key=lambda a: a["pub_date"], reverse=True)
    return articles

def build_list_items(articles):
    if not articles:
        return '      <li><p style="font-size:14px;color:var(--text-muted);padding:32px 0;">No articles published yet.</p></li>'

    items = []
    for a in articles:
        cat_attr = f' data-categories="{a["categories"]}"' if a["categories"] else ""
        item = f'''      <li{cat_attr}>
        <a href="posts/{a["slug"]}" class="post-card" style="display: block;">
          <div class="post-meta">{a["pub_display"]} · {a["label"]}</div>
          <h3>{a["title"]}</h3>
          <p>{a["desc"]}</p>
          <span class="card-link">Read article</span>
        </a>
      </li>'''
        items.append(item)
    return "\n\n".join(items)

def main():
    repo_root  = Path(__file__).resolve().parent.parent
    posts_dir  = repo_root / POSTS_DIR
    index_path = repo_root / INDEX_FILE

    if not posts_dir.exists():
        sys.stderr.write(f"Posts directory not found: {posts_dir}\n")
        return 1
    if not index_path.exists():
        sys.stderr.write(f"Index not found: {index_path}\n")
        return 1

    print("Aetas Wealth — Insights Index Builder")
    print(f"Scanning: {posts_dir}")
    print()

    articles = parse_articles(posts_dir)
    print(f"Found {len(articles)} published article(s)")
    for a in articles:
        print(f"  + {a['slug']} — {a['pub_display']}")

    items_html = build_list_items(articles)

    index_html = index_path.read_text(encoding="utf-8")
    if START_MARKER not in index_html or END_MARKER not in index_html:
        sys.stderr.write(f"Markers not found in {INDEX_FILE}.\n")
        sys.stderr.write(f"Add these inside the <ul> tag:\n")
        sys.stderr.write(f"  {START_MARKER}\n  {END_MARKER}\n")
        return 1

    before = index_html[:index_html.index(START_MARKER) + len(START_MARKER)]
    after  = index_html[index_html.index(END_MARKER):]
    new_index = before + "\n" + items_html + "\n\n    " + after

    index_path.write_text(new_index, encoding="utf-8")
    print()
    print(f"✓ {INDEX_FILE} updated with {len(articles)} article(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
