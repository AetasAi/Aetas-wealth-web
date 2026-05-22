#!/usr/bin/env python3
"""
Diagnostic: show the current date inside each Insights article alongside
what the redate script would set it to. Doesn't change any files.

Run from the repo root:
    py scripts\diagnose-dates.py
"""

import re
import sys
from datetime import date
from pathlib import Path


# Same map as redate-existing-posts.py — keep in sync.
DATE_CHANGES = {
    "pension-schemes-act-2026.html":                  "2026-04-29",
    "inheritance-tax-rising.html":                    "2026-04-15",
    "pension-changes-ahead.html":                     "2026-04-08",
    "isa-investment-strategy-2026.html":              "2026-03-11",
    "how-to-start-investing-uk.html":                 "2026-03-04",
    "uk-property-wealth-inheritance-tax.html":        "2026-01-21",
    "should-i-pay-my-childs-university-fees.html":    "2025-12-17",
    "financial-wellbeing-business-issue-for-smes.html": "2026-01-07",
    "why-your-pension-needs-regular-reviews.html":    "2025-11-19",
    "family-wealth-transfer-2027.html":               "2026-02-04",
    "how-pensions-are-taxed-after-death.html":        "2025-12-10",
}

POSTS_DIR = Path("insights/posts")


def format_display(iso_str):
    d = date.fromisoformat(iso_str)
    return f"{d.day} {d.strftime('%B')} {d.year}"


def find_current_date(html):
    """Find the date currently in the file. Returns string or None."""
    # Try JSON-LD first
    m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    if m:
        iso = m.group(1)[:10]
        try:
            return format_display(iso) + " (from JSON-LD)"
        except ValueError:
            pass

    # Try byline
    m = re.search(r'Published\s+(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})', html)
    if m:
        return m.group(1) + " (from byline)"

    # Try any date-shaped string
    m = re.search(r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})', html)
    if m:
        return m.group(1) + " (from body text)"

    return None


def main():
    repo_root = Path(__file__).resolve().parent.parent
    posts_dir = repo_root / POSTS_DIR

    if not posts_dir.exists():
        sys.stderr.write(f"Posts directory not found: {posts_dir}\n")
        return 1

    print(f"Checking {len(DATE_CHANGES)} files in {posts_dir}\n")
    print(f"{'Filename':<50} {'Current date':<40} {'Target date':<22} {'Match?'}")
    print("-" * 130)

    for filename, target_iso in DATE_CHANGES.items():
        path = posts_dir / filename
        if not path.exists():
            print(f"{filename:<50} {'(NOT FOUND)':<40} {format_display(target_iso):<22} ✗")
            continue
        html = path.read_text(encoding="utf-8")
        current = find_current_date(html) or "(no date found)"
        target = format_display(target_iso)
        match = "✓ already correct" if target in current else "→ needs update"
        print(f"{filename:<50} {current:<40} {target:<22} {match}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
