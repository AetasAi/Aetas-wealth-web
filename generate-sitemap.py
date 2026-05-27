#!/usr/bin/env python3
"""
Generate sitemap.xml for the Aetas Wealth static site.

Walks the repo, finds every .html file, applies sensible priority and
changefreq values based on where the page sits in the site structure, and
writes a fresh sitemap.xml to the repo root.

Usage (from the repo root):
    python generate-sitemap.py

Or with an explicit path:
    python generate-sitemap.py C:\\Repos\\Aetas-wealth-web

Notes
-----
* lastmod values use the file's filesystem modification time. If you've just
  done a `git clone` or `git pull` these will be the download time, not the
  original commit time. That's fine — Google uses lastmod as a hint, not a
  source of truth.
* Add new exclusions to EXCLUDE_NAMES if you ever create local-only HTML
  files (e.g. test pages).
* The homepage is emitted as `https://aetas-wealth.com/` (trailing slash, no
  `index.html`) which matches what users actually type and what your
  canonical tag says.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

BASE_URL = "https://aetas-wealth.com"

# Files (by filename, anywhere) to exclude from the sitemap
EXCLUDE_NAMES = {
    "404.html",   # noindex error page
    "home.html",  # noindex redirect stub
}

# Directories (relative to repo root) to exclude entirely
EXCLUDE_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "scripts",
    "Posts",      # legacy capitalised folder; remove this line if you don't have it
    "docs",       # if your repo has /docs for working notes only
}

# Classification rules. First matching rule wins.
# Each rule is: (test_function, priority_float, changefreq_or_None)
def _is_top_level_marketing(rel: Path) -> bool:
    return rel.parent == Path(".") and rel.name in {
        "individuals.html",
        "businesses.html",
        "our-people.html",
        "our-approach.html",
        "fees.html",
    }

def _is_important_subpage(rel: Path) -> bool:
    return rel.parent == Path(".") and rel.name in {
        "business-owners.html",
        "workplace.html",
        "working-with-us.html",
        "professional-introducers.html",
        "lifetime-to-legacy.html",
        "pensions-iht-2027.html",
        "inheritance-tax.html",   # flagship topical landing page
        "contact.html",
    }

def _is_legal(rel: Path) -> bool:
    return rel.parent == Path(".") and rel.name in {
        "privacy.html",
        "terms.html",
        "complaints.html",
    }

RULES: list[tuple] = [
    # Homepage
    (lambda r: r == Path("index.html"),                          1.0, "monthly"),
    # Section indexes
    (lambda r: r == Path("insights/index.html"),                 0.8, "weekly"),
    (lambda r: r == Path("case-studies/index.html"),             0.8, "monthly"),
    # Insight posts
    (lambda r: r.parent == Path("insights/posts"),               0.7, None),
    # Case study posts
    (lambda r: r.parent == Path("case-studies"),                 0.7, None),
    # Team profile pages
    (lambda r: r.parent == Path("team"),                         0.8, None),
    # Service pages
    (lambda r: r.parent == Path("services"),                     0.7, "monthly"),
    # Partner / co-branded sub-site pages (anything under aetas-*/)
    (lambda r: r.parts[0].startswith("aetas-"),                  0.7, None),
    # Top-level marketing pages (high priority)
    (_is_top_level_marketing,                                    0.9, "monthly"),
    # Important subpages
    (_is_important_subpage,                                      0.8, "monthly"),
    # Legal / compliance
    (_is_legal,                                                  0.4, None),
]

# Default for anything not matched above (warn so you can decide)
DEFAULT_PRIORITY = 0.5
DEFAULT_CHANGEFREQ: str | None = None

# --------------------------------------------------------------------------
# Logic
# --------------------------------------------------------------------------

def classify(rel: Path) -> tuple[float, str | None]:
    for matcher, priority, changefreq in RULES:
        if matcher(rel):
            return priority, changefreq
    return DEFAULT_PRIORITY, DEFAULT_CHANGEFREQ


def build_url_entry(rel: Path, repo_root: Path) -> str:
    """Build the <url>...</url> block for a single page."""
    # Hub index pages: use trailing-slash form, not /index.html.
    # The homepage and the two section hubs (insights, case-studies) all
    # canonicalise to the trailing-slash form to match what users actually
    # see in their browser and what GitHub Pages serves at the directory URL.
    TRAILING_SLASH_INDEXES = {
        Path("index.html"),
        Path("insights/index.html"),
        Path("case-studies/index.html"),
    }
    if rel in TRAILING_SLASH_INDEXES:
        parent = rel.parent.as_posix()
        if parent == ".":
            loc = BASE_URL + "/"
        else:
            loc = f"{BASE_URL}/{parent}/"
    else:
        loc = f"{BASE_URL}/{rel.as_posix()}"

    priority, changefreq = classify(rel)

    # lastmod from filesystem mtime
    mtime = (repo_root / rel).stat().st_mtime
    lastmod = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%d")

    parts = [
        "  <url>",
        f"    <loc>{loc}</loc>",
        f"    <lastmod>{lastmod}</lastmod>",
    ]
    if changefreq:
        parts.append(f"    <changefreq>{changefreq}</changefreq>")
    parts.append(f"    <priority>{priority}</priority>")
    parts.append("  </url>")
    return "\n".join(parts)


def should_include(rel: Path) -> bool:
    # Skip excluded directories anywhere in the path
    for part in rel.parts:
        if part in EXCLUDE_DIRS or part.startswith("."):
            return False
    # Skip excluded filenames
    if rel.name in EXCLUDE_NAMES:
        return False
    return True


def main():
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    if not repo_root.is_dir():
        print(f"ERROR: {repo_root} is not a directory.")
        sys.exit(1)

    # Find every .html file in the repo
    candidates = sorted(repo_root.rglob("*.html"))
    included: list[Path] = []
    excluded: list[Path] = []
    for p in candidates:
        rel = p.relative_to(repo_root)
        if should_include(rel):
            included.append(rel)
        else:
            excluded.append(rel)

    # Sort with a stable, sensible order:
    # 1. Homepage first
    # 2. Top-level pages (parent == .)
    # 3. team/, then services/, then case-studies/, then insights/
    def sort_key(rel: Path):
        if rel == Path("index.html"):
            return (0, "")
        depth = len(rel.parts)
        # Top-level pages
        if depth == 1:
            return (1, rel.name)
        # Subdirectory pages
        section_order = {
            "team": 2,
            "services": 3,
            "case-studies": 4,
            "insights": 5,
        }
        order = section_order.get(rel.parts[0], 9)
        return (order, str(rel))

    included.sort(key=sort_key)

    # Build the XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    current_section = None
    for rel in included:
        # Optional section comments for readability
        section = rel.parts[0] if len(rel.parts) > 1 else "root"
        if section != current_section:
            xml_lines.append(f"  <!-- {section} -->")
            current_section = section
        xml_lines.append(build_url_entry(rel, repo_root))
    xml_lines.append("</urlset>")
    xml_lines.append("")  # trailing newline

    out_path = repo_root / "sitemap.xml"
    out_path.write_text("\n".join(xml_lines), encoding="utf-8")

    # Report
    print(f"Wrote {out_path}")
    print(f"  Included: {len(included)} URLs")
    print(f"  Excluded: {len(excluded)} files")
    if excluded:
        print("\nExcluded files (verify these should really be skipped):")
        for rel in excluded[:20]:
            print(f"  - {rel}")
        if len(excluded) > 20:
            print(f"  ... and {len(excluded) - 20} more")

    # Warn about any files using the default classification (means rules
    # didn't match anything specific — usually a sign you have a new page
    # type that needs a rule).
    default_hits = [rel for rel in included if classify(rel) == (DEFAULT_PRIORITY, DEFAULT_CHANGEFREQ)]
    if default_hits:
        print(f"\nWARNING: {len(default_hits)} pages fell through to the default")
        print(f"priority ({DEFAULT_PRIORITY}). Consider adding a rule for these:")
        for rel in default_hits[:10]:
            print(f"  - {rel}")


if __name__ == "__main__":
    main()
