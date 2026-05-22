#!/usr/bin/env python3
"""
Aetas Wealth — Insights index auto-builder.

Scans `insights/posts/*.html`, extracts metadata from each article, and
rewrites the article list in `insights/index.html` between the markers:

    <!-- AUTO-INSIGHTS-START -->
    ...content here will be replaced...
    <!-- AUTO-INSIGHTS-END -->

Run locally:
    python scripts/build-insights-index.py

Run via GitHub Actions:
    Triggered automatically on push to insights/posts/** (see workflow file).

Per-article controls (optional, added to article <head>):
    <meta name="aw-listed" content="false">      → hide from the index
    <meta name="aw-categories" content="iht pensions">
                                                  → override filter categories
    <meta name="aw-display-category" content="Inheritance tax">
                                                  → override displayed label

If no overrides are given, the script infers from the existing template:
    - Date: JSON-LD datePublished → "Published X" byline → file mtime
    - Title: <h1> → <title> (with "· Aetas Wealth" stripped)
    - Description: <p class="lead"> → <meta name="description">
    - Category: <span class="eyebrow"> → "Insights" default
"""

import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path


# ---------- Configuration ----------

# Where the script expects things, relative to the repo root.
POSTS_DIR = Path("insights/posts")
INDEX_FILE = Path("insights/index.html")

START_MARKER = "<!-- AUTO-INSIGHTS-START -->"
END_MARKER = "<!-- AUTO-INSIGHTS-END -->"

# Eyebrow text → (display category, filter categories).
# Order matters: longer/more-specific keys checked first.
CATEGORY_MAP = [
    # Exact eyebrow → display + filter
    ("inheritance tax & pensions",   ("Inheritance tax", ["iht", "pensions"])),
    ("inheritance tax & giving",     ("Inheritance tax", ["iht", "planning"])),
    ("inheritance tax & iht",        ("Inheritance tax", ["iht"])),
    ("estate planning & iht",        ("Inheritance tax", ["iht", "planning"])),
    ("pensions & retirement",        ("Pensions", ["pensions"])),
    ("savings & investments",        ("Investments", ["investments"])),
    ("market commentary",            ("Market commentary", ["markets"])),
    ("financial planning",           ("Financial planning", ["planning"])),
    ("estate planning",              ("Estate planning", ["iht", "planning"])),
    ("inheritance tax",              ("Inheritance tax", ["iht"])),
    ("family finances",              ("Family finances", ["planning"])),
    ("pensions",                     ("Pensions", ["pensions"])),
    ("pension",                      ("Pensions", ["pensions"])),
    ("retirement",                   ("Pensions", ["pensions"])),
    ("isas",                         ("ISAs", ["investments"])),
    ("isa",                          ("ISAs", ["investments"])),
    ("investments",                  ("Investments", ["investments"])),
    ("investment",                   ("Investments", ["investments"])),
    ("markets",                      ("Markets", ["markets"])),
    ("workplace",                    ("Workplace", ["workplace"])),
    ("smes",                         ("Workplace", ["workplace"])),
    ("sme",                          ("Workplace", ["workplace"])),
    ("planning",                     ("Financial planning", ["planning"])),
]

DEFAULT_CATEGORY = ("Insights", ["all"])

# Files to skip even if present in posts/
SKIP_FILES = {"index.html", "_template.html"}


# ---------- HTML extraction helpers ----------

def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def first_match(pattern, text, group=1, flags=re.DOTALL | re.IGNORECASE):
    m = re.search(pattern, text, flags)
    return m.group(group).strip() if m else None


def strip_tags(s):
    if not s:
        return s
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    # Decode a few common entities we might encounter
    s = (s.replace("&amp;", "&")
           .replace("&lt;", "<")
           .replace("&gt;", ">")
           .replace("&quot;", '"')
           .replace("&#39;", "'")
           .replace("&pound;", "£")
           .replace("&nbsp;", " ")
           .replace("&mdash;", "—")
           .replace("&ndash;", "–")
           .replace("&rsquo;", "'")
           .replace("&lsquo;", "'")
           .replace("&ldquo;", '"')
           .replace("&rdquo;", '"'))
    return s


def parse_meta(html, name):
    """Read <meta name='X' content='Y'> case-insensitively, single or double quotes."""
    m = re.search(
        rf'<meta\s+name=["\']{re.escape(name)}["\']\s+content=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    )
    return m.group(1).strip() if m else None


def parse_jsonld_date(html):
    """Pull datePublished out of any Article JSON-LD block."""
    for block in re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        html, re.DOTALL,
    ):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        candidates = data if isinstance(data, list) else [data]
        for c in candidates:
            if isinstance(c, dict) and c.get("@type") == "Article":
                if "datePublished" in c:
                    return c["datePublished"][:10]  # YYYY-MM-DD
    return None


def parse_published_text(html):
    """Fallback: read 'Published 8 July 2025' from the byline."""
    m = re.search(
        r"Published\s+(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})",
        html,
    )
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%d %B %Y").date().isoformat()
    except ValueError:
        return None


def parse_h1(html):
    return strip_tags(first_match(r"<h1[^>]*>(.*?)</h1>", html))


def parse_title_tag(html):
    raw = strip_tags(first_match(r"<title[^>]*>(.*?)</title>", html))
    if raw:
        # Strip our suffix variations
        for suffix in (" · Aetas Wealth", " | Aetas Wealth"):
            if raw.endswith(suffix):
                raw = raw[: -len(suffix)]
    return raw


def parse_lead(html):
    return strip_tags(first_match(r'<p class="lead"[^>]*>(.*?)</p>', html))


def parse_meta_description(html):
    return parse_meta(html, "description")


def parse_eyebrow(html):
    return strip_tags(first_match(r'<span class="eyebrow"[^>]*>(.*?)</span>', html))


# ---------- Category mapping ----------

def map_category(eyebrow):
    if not eyebrow:
        return DEFAULT_CATEGORY
    key = eyebrow.lower()
    for needle, value in CATEGORY_MAP:
        if needle in key:
            return value
    return DEFAULT_CATEGORY


# ---------- Article model ----------

class Article:
    def __init__(self, path):
        self.path = path
        self.filename = path.name
        html = read(path)

        # Skip-list opt-out
        listed = parse_meta(html, "aw-listed")
        self.listed = (listed or "true").lower() != "false"

        # Date
        iso = (parse_jsonld_date(html)
               or parse_published_text(html)
               or datetime.fromtimestamp(path.stat().st_mtime).date().isoformat())
        try:
            self.date = date.fromisoformat(iso)
        except ValueError:
            self.date = date.today()

        # Title / description
        self.title = parse_h1(html) or parse_title_tag(html) or self.filename
        self.description = (parse_lead(html)
                            or parse_meta_description(html)
                            or "")

        # Categories
        eyebrow = parse_eyebrow(html)
        override_display = parse_meta(html, "aw-display-category")
        override_filters = parse_meta(html, "aw-categories")

        if override_display or override_filters:
            mapped_display, mapped_filters = map_category(eyebrow)
            self.display_category = override_display or mapped_display
            if override_filters:
                self.filter_categories = override_filters.split()
            else:
                self.filter_categories = mapped_filters
        else:
            self.display_category, self.filter_categories = map_category(eyebrow)

    def date_display(self):
        # "8 July 2025" — no leading zero on day
        return f"{self.date.day} {self.date.strftime('%B')} {self.date.year}"

    def render_li(self):
        cats = " ".join(self.filter_categories) if self.filter_categories else "all"
        return (
            f'      <li data-categories="{cats}">\n'
            f'        <a href="posts/{self.filename}" class="post-card" style="display: block;">\n'
            f'          <div class="post-meta">{self.date_display()} · {self.display_category}</div>\n'
            f'          <h3>{html_escape(self.title)}</h3>\n'
            f'          <p>{html_escape(self.description)}</p>\n'
            f'          <span class="card-link">Read article</span>\n'
            f'        </a>\n'
            f'      </li>'
        )


def html_escape(s):
    if not s:
        return ""
    # Minimal escaping — < and > and & to be safe.
    # Don't escape characters that are already valid in the index (£, em-dash, etc.).
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


# ---------- Indexer ----------

def collect_articles(posts_dir):
    articles = []
    if not posts_dir.exists():
        sys.stderr.write(f"Posts directory not found: {posts_dir}\n")
        return articles
    for path in sorted(posts_dir.glob("*.html")):
        if path.name in SKIP_FILES:
            continue
        try:
            article = Article(path)
        except Exception as e:
            sys.stderr.write(f"  ! Failed to parse {path.name}: {e}\n")
            continue
        if not article.listed:
            continue
        articles.append(article)
    # Newest first
    articles.sort(key=lambda a: a.date, reverse=True)
    return articles


def render_block(articles):
    lines = []
    for a in articles:
        lines.append(a.render_li())
        lines.append("")  # Blank line between entries
    return "\n".join(lines).rstrip() + "\n"


def update_index(index_path, articles):
    if not index_path.exists():
        sys.stderr.write(f"Index file not found: {index_path}\n")
        return False

    html = read(index_path)

    if START_MARKER not in html or END_MARKER not in html:
        sys.stderr.write(
            f"Markers not found in {index_path}. Add this block where the article cards should sit:\n\n"
            f"    {START_MARKER}\n"
            f"    {END_MARKER}\n\n"
        )
        return False

    new_block = render_block(articles)

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    new_html = pattern.sub(
        f"{START_MARKER}\n{new_block}    {END_MARKER}",
        html,
    )

    if new_html == html:
        return False

    index_path.write_text(new_html, encoding="utf-8")
    return True


# ---------- Entry point ----------

def main():
    # Allow running from any working dir — resolve relative to script location's parent.
    here = Path(__file__).resolve().parent
    repo_root = here.parent

    posts_dir = repo_root / POSTS_DIR
    index_path = repo_root / INDEX_FILE

    print(f"Scanning {posts_dir} ...")
    articles = collect_articles(posts_dir)
    print(f"  Found {len(articles)} listed articles")
    for a in articles:
        print(f"   - {a.date_display():25} {a.display_category:22} {a.filename}")

    print(f"\nUpdating {index_path} ...")
    changed = update_index(index_path, articles)
    if changed:
        print("  ✓ Index updated")
    else:
        print("  · No change needed (already up to date)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
