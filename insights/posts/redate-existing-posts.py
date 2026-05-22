#!/usr/bin/env python3
"""
Re-date existing Aetas Wealth Insights articles.

This script updates the published date in articles that already exist on the
site, without changing any content. It looks for two patterns and updates them:

1. JSON-LD `datePublished` (if present)
2. Human-readable byline: "Published 11 May 2026 · By X · 5 minute read"

Run from the repo root:
    python3 scripts/redate-existing-posts.py

The DATE_CHANGES dict below maps filename → new date.
Edit it and re-run any time you want to bulk-adjust dates.
"""

import re
import sys
from datetime import date
from pathlib import Path


# Map of filename → new date (ISO format, will be reformatted for display)
# Add or edit entries here. Files not listed will be left untouched.
DATE_CHANGES = {
    # Cluster fixes — Wednesday cadence going back from 22 May 2026
    "pension-schemes-act-2026.html":                  "2026-04-29",  # Real Royal Assent date
    "inheritance-tax-rising.html":                    "2026-04-15",  # was 20 April — move out of cluster
    "pension-changes-ahead.html":                     "2026-04-08",  # was 20 April — move out of cluster
    "isa-investment-strategy-2026.html":              "2026-03-11",  # was 15 May — move
    "how-to-start-investing-uk.html":                 "2026-03-04",  # was 15 May — move
    "uk-property-wealth-inheritance-tax.html":        "2026-01-21",  # was 15 May — move
    "should-i-pay-my-childs-university-fees.html":    "2025-12-17",  # was 15 May — move
    "financial-wellbeing-business-issue-for-smes.html": "2026-01-07", # was 15 May — move (new year workplace)
    "why-your-pension-needs-regular-reviews.html":    "2025-11-19",  # was 15 May — move
    "family-wealth-transfer-2027.html":               "2026-02-04",  # spread back
    "how-pensions-are-taxed-after-death.html":        "2025-12-10",  # spread back

    # Fixed dates — uncomment if you want the script to confirm/touch them
    # "finance-act-2026.html":                        "2026-05-22",  # KEEP
    # "business-owners-pensions-and-the-2027-changes.html": "2026-05-19",  # KEEP
    # "bank-of-england-holds-rates-may-2026.html":    "2026-05-11",  # KEEP
    # "market-commentary-may-2026.html":              "2026-05-12",  # KEEP (was 11 May, move 1 day)
    # "market-commentary-april-2026.html":            "2026-04-20",  # KEEP
}


POSTS_DIR = Path("insights/posts")


def format_display_date(iso_str):
    """Convert '2026-04-15' to '15 April 2026' (no leading zero)."""
    d = date.fromisoformat(iso_str)
    return f"{d.day} {d.strftime('%B')} {d.year}"


def update_file(path, new_iso):
    """Update both JSON-LD datePublished and the byline text in one file."""
    html = path.read_text(encoding="utf-8")
    original = html
    new_display = format_display_date(new_iso)

    changes = []

    # 1) Update JSON-LD datePublished. Matches "datePublished": "2025-11-20" or full ISO.
    json_pat = re.compile(r'("datePublished"\s*:\s*")([^"]+)(")')
    def json_repl(m):
        changes.append(f"  JSON-LD datePublished: {m.group(2)[:10]} → {new_iso}")
        return f'{m.group(1)}{new_iso}T08:00:00+00:00{m.group(3)}'
    html = json_pat.sub(json_repl, html, count=1)

    # 2) Update the byline "Published DD Month YYYY"
    byline_pat = re.compile(r'(Published\s+)(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})')
    def byline_repl(m):
        changes.append(f"  Byline date: {m.group(2)} → {new_display}")
        return f'{m.group(1)}{new_display}'
    html = byline_pat.sub(byline_repl, html, count=1)

    if html == original:
        return False, ["No date patterns matched — file unchanged"]
    path.write_text(html, encoding="utf-8")
    return True, changes


def main():
    repo_root = Path(__file__).resolve().parent.parent
    posts_dir = repo_root / POSTS_DIR

    if not posts_dir.exists():
        sys.stderr.write(f"Posts directory not found: {posts_dir}\n")
        return 1

    print(f"Re-dating articles in {posts_dir}\n")

    updated = 0
    skipped = 0
    missing = 0

    for filename, new_iso in DATE_CHANGES.items():
        path = posts_dir / filename
        if not path.exists():
            print(f"  ⚠ {filename} — NOT FOUND")
            missing += 1
            continue

        changed, notes = update_file(path, new_iso)
        if changed:
            new_display = format_display_date(new_iso)
            print(f"  ✓ {filename} → {new_display}")
            for note in notes:
                print(note)
            updated += 1
        else:
            print(f"  · {filename} — no changes needed")
            for note in notes:
                print(note)
            skipped += 1

    print(f"\nSummary: {updated} updated, {skipped} skipped, {missing} not found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
