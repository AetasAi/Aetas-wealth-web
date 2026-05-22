#!/usr/bin/env python3
"""
Assign Tuesday/Thursday publication dates to a batch of articles.

Edit the SCHEDULE list below — filename → optional override date.
Run, and the script:
1. Lists all articles in insights/posts/ in alphabetical order
2. Assigns Tuesday/Thursday dates starting from the START_FROM date
3. Updates each article's JSON-LD datePublished and byline date
4. Reports the new schedule

Run from repo root:
    py scripts\\schedule-articles.py

CONFIGURATION:
    Edit START_FROM (the date the first article publishes)
    Edit ARTICLE_ORDER (filenames in the order you want them released)
    Or use SCHEDULE for per-file specific dates (overrides ARTICLE_ORDER)
"""

import re
import sys
from datetime import date, timedelta
from pathlib import Path


# ============================================================
# CONFIGURATION — edit these
# ============================================================

# Date to start scheduling from. Will be moved to the next Tuesday/Thursday if needed.
START_FROM = date(2026, 5, 26)  # Tuesday 26 May 2026

# Order in which to publish (Tue/Thu cadence starting from START_FROM).
# Add filenames here in your desired publication order.
ARTICLE_ORDER = [
    # Example — edit this list to match the articles you want to schedule
    # "first-article.html",
    # "second-article.html",
    # "third-article.html",
]

# Optional: per-file specific dates that override ARTICLE_ORDER
# Filename → ISO date string (YYYY-MM-DD)
SCHEDULE = {
    # "specific-article.html": "2026-07-15",
}

# Days of the week to publish on (0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri)
PUBLISH_DAYS = [1, 3]  # Tuesday and Thursday

POSTS_DIR = Path("insights/posts")


# ============================================================
# Internal helpers
# ============================================================

def format_display(d):
    """Convert date to '15 April 2026' (no leading zero)."""
    return f"{d.day} {d.strftime('%B')} {d.year}"


def next_publish_day(start, publish_days):
    """Find the next date on a publish day, starting at `start`."""
    d = start
    while d.weekday() not in publish_days:
        d += timedelta(days=1)
    return d


def generate_dates(start, count, publish_days):
    """Generate `count` consecutive publish dates starting from `start`."""
    dates = []
    d = next_publish_day(start, publish_days)
    for _ in range(count):
        dates.append(d)
        # Step forward to next publish day
        d += timedelta(days=1)
        d = next_publish_day(d, publish_days)
    return dates


def update_dates_in_file(path, target_date):
    """Update both JSON-LD datePublished and the byline date in a file."""
    html = path.read_text(encoding="utf-8")
    original = html
    target_iso = target_date.isoformat()
    target_full = f"{target_iso}T08:00:00+00:00"
    target_display = format_display(target_date)
    messages = []

    # JSON-LD datePublished
    json_pat = re.compile(r'("datePublished"\s*:\s*")([^"]+)(")')
    m = json_pat.search(html)
    if m:
        old_iso = m.group(2)[:10]
        if old_iso != target_iso:
            html = json_pat.sub(f'\\g<1>{target_full}\\g<3>', html, count=1)
            messages.append(f"JSON-LD: {old_iso} → {target_iso}")

    # Byline "Published DD Month YYYY"
    byline_pat = re.compile(r'(Published\s+)(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})')
    m = byline_pat.search(html)
    if m:
        old_display = m.group(2)
        if old_display != target_display:
            html = byline_pat.sub(f'\\g<1>{target_display}', html, count=1)
            messages.append(f"Byline: {old_display} → {target_display}")

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True, messages
    return False, []


# ============================================================
# Entry point
# ============================================================

def main():
    repo_root = Path(__file__).resolve().parent.parent
    posts_dir = repo_root / POSTS_DIR

    if not posts_dir.exists():
        sys.stderr.write(f"Posts directory not found: {posts_dir}\n")
        return 1

    print(f"Scheduling articles starting from {format_display(START_FROM)}")
    print(f"Publishing on: {[['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][d] for d in PUBLISH_DAYS]}")
    print()

    if not ARTICLE_ORDER and not SCHEDULE:
        print("WARNING: ARTICLE_ORDER and SCHEDULE are both empty.")
        print("Edit this script and add filenames to ARTICLE_ORDER (in the order you want them released).")
        print()
        print("Currently in posts/:")
        for f in sorted(posts_dir.glob("*.html")):
            print(f"  {f.name}")
        return 1

    # Generate sequential dates for ARTICLE_ORDER items
    sequential_dates = generate_dates(START_FROM, len(ARTICLE_ORDER), PUBLISH_DAYS)

    # Build final filename → date map
    final_schedule = {}
    for filename, d in zip(ARTICLE_ORDER, sequential_dates):
        final_schedule[filename] = d
    for filename, iso_str in SCHEDULE.items():
        final_schedule[filename] = date.fromisoformat(iso_str)

    # Apply
    print(f"{'Filename':<50} {'Date':<22} {'Day':<8} {'Status'}")
    print("-" * 100)
    updated = 0
    missing = 0
    unchanged = 0

    for filename, target_date in final_schedule.items():
        path = posts_dir / filename
        if not path.exists():
            print(f"{filename:<50} {'—':<22} {'—':<8} NOT FOUND")
            missing += 1
            continue

        weekday = target_date.strftime("%A")
        changed, messages = update_dates_in_file(path, target_date)
        if changed:
            print(f"{filename:<50} {format_display(target_date):<22} {weekday:<8} UPDATED")
            updated += 1
        else:
            print(f"{filename:<50} {format_display(target_date):<22} {weekday:<8} no change")
            unchanged += 1

    print()
    print(f"Summary: {updated} updated, {unchanged} already correct, {missing} not found")

    if updated > 0:
        print()
        print("NEXT STEPS:")
        print("1. Run: py scripts\\build-insights-index.py  (to preview the new index)")
        print("2. Commit and push the changes to GitHub")
        print("3. Articles will now appear automatically on their scheduled dates")

    return 0


if __name__ == "__main__":
    sys.exit(main())
