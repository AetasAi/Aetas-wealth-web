#!/usr/bin/env python3
"""
Generate a GHL Social Planner CSV with LinkedIn teasers timed to match
each article's scheduled publication date.

Reads each article in insights/posts/ to extract:
  - datePublished (when the article goes live)
  - title (for fallback)
  - meta description / lead paragraph (for the teaser content)

Outputs: ghl-linkedin-teasers.csv with one row per article.

TEASER GENERATION:
By default, this script generates a SIMPLE auto-teaser from the article's
lead paragraph. For high-quality custom teasers (like the ones in
linkedin-content-pack.md), edit the CUSTOM_TEASERS dict below.

Run from repo root:
    py scripts\\generate-linkedin-csv.py
"""

import csv
import re
import sys
from datetime import datetime
from pathlib import Path


POSTS_DIR = Path("insights/posts")
OUTPUT_CSV = Path("ghl-linkedin-teasers.csv")

# When in the day the LinkedIn teaser should post (UK time)
# Format: "HH:mm"
POST_TIME = "08:00"

# Custom teasers — keyed by filename. If a filename is in here, this teaser is used.
# Otherwise, an auto-teaser is generated from the article's lead paragraph.
CUSTOM_TEASERS = {
    # Example:
    # "pension-iht-2027.html": """Your custom teaser text here...
    #
    # 👉 https://aetas-wealth.com/insights/posts/pension-iht-2027.html
    #
    # #Pensions #IHT""",
}

# Default hashtags appended to auto-generated teasers, by detected category
CATEGORY_HASHTAGS = {
    "Inheritance tax":  "#InheritanceTax #EstatePlanning #FinancialPlanning #UKFinance",
    "Pensions":         "#Pensions #Retirement #FinancialPlanning #UKFinance",
    "Investments":      "#Investing #ISA #FinancialPlanning #UKFinance",
    "Estate planning":  "#EstatePlanning #InheritanceTax #FinancialPlanning",
    "Tax planning":     "#TaxPlanning #UKTax #FinancialPlanning",
    "Workplace":        "#SMEs #BusinessOwners #UKBusinessOwners #FinancialPlanning",
    "Markets":          "#Markets #Investing #UKEconomy",
    "Financial planning": "#FinancialPlanning #UKFinance",
    "Family finances":  "#FamilyFinances #FinancialPlanning #UKFinance",
}


def read_article(path):
    """Extract metadata + content snippets for teaser generation."""
    html = path.read_text(encoding="utf-8")

    # datePublished from JSON-LD
    m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    iso = m.group(1)[:10] if m else None

    # H1
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else None

    # Lead paragraph
    m = re.search(r'<p class="lead"[^>]*>(.*?)</p>', html, re.DOTALL)
    lead = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else None

    # Category (from eyebrow)
    m = re.search(r'<span class="eyebrow"[^>]*>(.*?)</span>', html, re.DOTALL)
    eyebrow = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else None

    # Aw-display-category override
    m = re.search(r'<meta\s+name=["\']aw-display-category["\']\s+content=["\']([^"\']*)["\']', html)
    display_cat = m.group(1).strip() if m else None

    return {
        "filename": path.name,
        "date_iso": iso,
        "h1": h1,
        "lead": lead,
        "eyebrow": eyebrow,
        "display_category": display_cat or eyebrow,
    }


def auto_teaser(article):
    """Generate a simple teaser from article metadata."""
    url = f"https://aetas-wealth.com/insights/posts/{article['filename']}"
    h1 = article["h1"]
    lead = article["lead"]

    # Get hashtags
    cat = article.get("display_category", "")
    hashtags = "#FinancialPlanning #UKFinance"
    for key, tags in CATEGORY_HASHTAGS.items():
        if key.lower() in cat.lower():
            hashtags = tags
            break

    # Build teaser
    lines = []
    if h1:
        lines.append(h1)
        lines.append("")
    if lead:
        lines.append(lead)
        lines.append("")
    lines.append(f"Full article on Aetas Wealth:")
    lines.append("")
    lines.append(f"👉 {url}")
    lines.append("")
    lines.append(hashtags)

    return "\n".join(lines)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    posts_dir = repo_root / POSTS_DIR
    output_path = repo_root / OUTPUT_CSV

    if not posts_dir.exists():
        sys.stderr.write(f"Posts directory not found: {posts_dir}\n")
        return 1

    print(f"Scanning {posts_dir} ...")

    articles = []
    for path in sorted(posts_dir.glob("*.html")):
        if path.name == "index.html":
            continue
        meta = read_article(path)
        if not meta["date_iso"]:
            print(f"  ! {path.name} — no datePublished, skipping")
            continue
        articles.append(meta)

    # Sort by date
    articles.sort(key=lambda a: a["date_iso"])

    print(f"  Found {len(articles)} articles with dates\n")

    # Generate CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["Date", "Content", "OG Meta URL", "Image(s) Link", "Video(s) Link", "GIF"])

        for article in articles:
            # Date in GHL format
            ghl_date = f"{article['date_iso']} {POST_TIME}"

            # Teaser content
            if article["filename"] in CUSTOM_TEASERS:
                content = CUSTOM_TEASERS[article["filename"]]
            else:
                content = auto_teaser(article)

            og_url = f"https://aetas-wealth.com/insights/posts/{article['filename']}"
            writer.writerow([ghl_date, content, og_url, "", "", ""])

            # Show preview
            today = datetime.now().date().isoformat()
            future = "📅 future" if article["date_iso"] > today else "📰 past"
            print(f"  {future}  {ghl_date}  {article['filename']}")

    print(f"\n✓ Wrote {output_path}")
    print(f"\nNext: upload {output_path.name} to GHL Social Planner")
    print(f"     Marketing → Social Planner → + New Post → Upload from CSV → Basic Format")
    return 0


if __name__ == "__main__":
    sys.exit(main())
