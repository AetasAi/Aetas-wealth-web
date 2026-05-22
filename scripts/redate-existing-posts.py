#!/usr/bin/env python3
"""
Re-date Aetas Wealth Insights articles in bulk.

Reads the DATE_CHANGES dict below — filename -> target ISO date. For each file:
1. Reads the current date (from JSON-LD if present, otherwise from the byline)
2. Compares to the target
3. If different, updates BOTH the JSON-LD datePublished (if present) and the
   byline "Published DD Month YYYY" text

Run from repo root:
    py scripts\\redate-existing-posts.py
"""

import re
import sys
from datetime import date
from pathlib import Path


# ============================================================
# DATE TARGETS - edit this dict to bulk re-date articles
# ============================================================
DATE_CHANGES = {
    # === Original 11 (most/all were already at these dates locally) ===
    "pension-schemes-act-2026.html":                    "2026-04-29",
    "inheritance-tax-rising.html":                      "2026-04-15",
    "pension-changes-ahead.html":                       "2026-04-08",
    "isa-investment-strategy-2026.html":                "2026-03-11",
    "how-to-start-investing-uk.html":                   "2026-03-04",
    "uk-property-wealth-inheritance-tax.html":          "2026-01-21",
    "should-i-pay-my-childs-university-fees.html":      "2025-12-17",
    "financial-wellbeing-business-issue-for-smes.html": "2026-01-07",
    "why-your-pension-needs-regular-reviews.html":      "2025-11-19",
    "family-wealth-transfer-2027.html":                 "2026-02-04",
    "how-pensions-are-taxed-after-death.html":          "2025-12-10",

    # === Fix the new 19 May 2026 cluster (was 4 articles on same date) ===
    "business-owners-pensions-estate-planning.html":    "2026-05-19",  # KEEP - anchor for series
    "pensions-iht-spousal-exemption.html":              "2026-05-21",  # Thu, day before Finance Act
    "pensions-iht-2027-what-is-changing.html":          "2026-05-14",  # Thu mid-May
    "drawing-your-pension-differently-after-2027.html": "2026-04-30",  # Thu late April

    # === The renamed Finance Act article ===
    "finance-act-2026.html":                            "2026-05-22",  # Real legislative date
}

# Files to hide from the index without changing their dates.
# Add filenames here if you ever want to keep an article on disk but not list it.
OPT_OUT_FILES = []


POSTS_DIR = Path("insights/posts")


# ============================================================
# Internal helpers
# ============================================================

def format_display(iso_str):
    """Convert '2026-04-15' to '15 April 2026' (no leading zero)."""
    d = date.fromisoformat(iso_str)
    return f"{d.day} {d.strftime('%B')} {d.year}"


def find_current_date(html):
    """Find date in file. Returns (display_string, source) or (None, None)."""
    # JSON-LD first (most reliable)
    m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    if m:
        iso_str = m.group(1)[:10]
        try:
            return format_display(iso_str), "JSON-LD"
        except ValueError:
            pass

    # Byline
    m = re.search(r'Published\s+(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})', html)
    if m:
        return m.group(1), "byline"

    return None, None


def update_dates_in_file(path, target_iso):
    """Returns (status, list_of_messages). Status is 'updated', 'unchanged', or 'no_dates_found'."""
    html = path.read_text(encoding="utf-8")
    original = html
    target_display = format_display(target_iso)
    target_full = f"{target_iso}T08:00:00+00:00"
    messages = []

    # 1) Update JSON-LD datePublished (if present)
    json_pat = re.compile(r'("datePublished"\s*:\s*")([^"]+)(")')
    json_match = json_pat.search(html)
    if json_match:
        old_iso = json_match.group(2)[:10]
        if old_iso != target_iso:
            html = json_pat.sub(f'\\g<1>{target_full}\\g<3>', html, count=1)
            messages.append(f"    JSON-LD datePublished: {old_iso} -> {target_iso}")
        else:
            messages.append(f"    JSON-LD datePublished: already {target_iso}")

    # 2) Update dateModified to today
    today_full = date.today().isoformat() + "T08:00:00+00:00"
    mod_pat = re.compile(r'("dateModified"\s*:\s*")([^"]+)(")')
    if mod_pat.search(html):
        html = mod_pat.sub(f'\\g<1>{today_full}\\g<3>', html, count=1)

    # 3) Update byline "Published DD Month YYYY"
    byline_pat = re.compile(r'(Published\s+)(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})')
    byline_match = byline_pat.search(html)
    if byline_match:
        old_display = byline_match.group(2)
        if old_display != target_display:
            html = byline_pat.sub(f'\\g<1>{target_display}', html, count=1)
            messages.append(f"    Byline: {old_display} -> {target_display}")
        else:
            messages.append(f"    Byline: already {target_display}")

    if not json_match and not byline_match:
        return "no_dates_found", ["    ! No JSON-LD or byline date found in this file"]

    if html == original:
        return "unchanged", messages

    path.write_text(html, encoding="utf-8")
    return "updated", messages


def add_optout_meta(path):
    """Add <meta name='aw-listed' content='false'> to a file's <head>."""
    html = path.read_text(encoding="utf-8")
    if 'name="aw-listed"' in html:
        return "already_opted_out"
    if "</head>" not in html:
        return "no_head_tag"
    new_html = html.replace(
        "</head>",
        '  <meta name="aw-listed" content="false">\n</head>',
        1,
    )
    path.write_text(new_html, encoding="utf-8")
    return "opted_out"


# ============================================================
# Entry point
# ============================================================

def main():
    repo_root = Path(__file__).resolve().parent.parent
    posts_dir = repo_root / POSTS_DIR

    if not posts_dir.exists():
        sys.stderr.write(f"Posts directory not found: {posts_dir}\n")
        return 1

    print(f"Re-dating articles in {posts_dir}\n")
    print("=" * 80)

    counts = {"updated": 0, "unchanged": 0, "no_dates_found": 0, "not_found": 0}

    for filename, target_iso in DATE_CHANGES.items():
        path = posts_dir / filename
        if not path.exists():
            print(f"  [MISS]    {filename}  NOT FOUND")
            counts["not_found"] += 1
            continue

        target_display = format_display(target_iso)
        current_display, source = find_current_date(path.read_text(encoding="utf-8"))
        current = f"{current_display} ({source})" if current_display else "(no date)"

        status, messages = update_dates_in_file(path, target_iso)

        if status == "updated":
            print(f"  [UPDATED] {filename}")
            print(f"    Was: {current}")
            print(f"    Now: {target_display}")
            for msg in messages:
                print(msg)
            counts["updated"] += 1
        elif status == "unchanged":
            print(f"  [OK]      {filename} - already at {target_display}")
            counts["unchanged"] += 1
        else:
            print(f"  [WARN]    {filename} - could not find any date to update")
            for msg in messages:
                print(msg)
            counts["no_dates_found"] += 1

    if OPT_OUT_FILES:
        print("\n" + "=" * 80)
        print("Hiding files from index (aw-listed=false):")
        for filename in OPT_OUT_FILES:
            path = posts_dir / filename
            if not path.exists():
                print(f"  [SKIP]   {filename} - not present (no action needed)")
                continue
            result = add_optout_meta(path)
            if result == "opted_out":
                print(f"  [HIDDEN] {filename} - opted out of index")
            elif result == "already_opted_out":
                print(f"  [OK]     {filename} - already opted out")
            else:
                print(f"  [WARN]   {filename} - could not add meta tag ({result})")

    print("\n" + "=" * 80)
    print(f"Summary: {counts['updated']} updated, "
          f"{counts['unchanged']} already correct, "
          f"{counts['no_dates_found']} no date pattern, "
          f"{counts['not_found']} not found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
