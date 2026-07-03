#!/usr/bin/env python3
"""
pre-deploy-check.py
===================
Run before committing to catch common issues that break SEO,
performance, accessibility and agentic browsing.

Usage:
    py pre-deploy-check.py

Exit code 0 = clean. Exit code 1 = issues found (do not deploy).
"""

import os, re, sys, json
from pathlib import Path

ROOT = Path(__file__).parent
ERRORS = []
WARNINGS = []

ASSET_EXTS = re.compile(r'\.(webp|jpg|jpeg|png|gif|svg|css|js|xml|txt|pdf|ico|woff|woff2|ttf|eot)', re.I)
INTERNAL_DOMAINS = re.compile(r'https?://(aetas-wealth|workplace\.aetas-wealth|charities\.aetas-wealth)\.com')

SKIP_DIRS = {'.git', '.github', 'node_modules', 'assets', 'icons', 'scripts', 'docs'}
SKIP_FILES = {'404.html', 'google4bf7b0394b6b5986.html', '05c082a578194ff5a6d02ad11d2a1456.txt'}

def collect_html_files():
    files = []
    for path in ROOT.rglob("*.html"):
        parts = set(path.parts)
        if parts & SKIP_DIRS:
            continue
        if path.name in SKIP_FILES:
            continue
        files.append(path)
    return files

def check_html_file(path):
    rel = path.relative_to(ROOT)
    content = path.read_text(encoding="utf-8", errors="replace")
    
    # 1. No .html in internal href links
    hrefs = re.findall(r'href=["\'](.*?)["\']', content)
    for href in hrefs:
        if ASSET_EXTS.search(href):
            continue
        if href.startswith("mailto:") or href.startswith("#"):
            continue
        # Relative link ending in .html
        if not href.startswith("http") and ".html" in href:
            ERRORS.append(f"{rel}: internal link uses .html → {href}")
        # Absolute internal link ending in .html
        elif INTERNAL_DOMAINS.match(href) and ".html" in href and not ASSET_EXTS.search(href):
            ERRORS.append(f"{rel}: absolute internal link uses .html → {href}")
    
    # 2. Canonical must not contain .html
    canonicals = re.findall(r'<link rel=["\'"]canonical["\'"] href=["\'](.*?)["\']', content)
    for c in canonicals:
        if ".html" in c:
            ERRORS.append(f"{rel}: canonical contains .html → {c}")
    
    # 3. Every indexable page must have a canonical
    if "<html" in content and "noindex" not in content:
        if 'rel="canonical"' not in content and "rel='canonical'" not in content:
            WARNINGS.append(f"{rel}: missing canonical tag")
    
    # 4. Every page must have a <title> inside <head>
    head_match = re.search(r'<head[^>]*>(.*?)</head>', content, re.S | re.I)
    if head_match:
        head = head_match.group(1)
        if "<title>" not in head.lower():
            ERRORS.append(f"{rel}: <title> missing or outside <head>")
        if 'name="description"' not in head and "name='description'" not in head:
            WARNINGS.append(f"{rel}: meta description missing")
    
    # 5. Images must have alt attributes
    imgs = re.findall(r'<img[^>]+>', content, re.I)
    for img in imgs:
        if "alt=" not in img.lower():
            ERRORS.append(f"{rel}: <img> missing alt attribute → {img[:80]}")
    
    # 6. No inline onclick / javascript: hrefs (accessibility + CSP)
    if "javascript:" in content:
        WARNINGS.append(f"{rel}: contains javascript: href (use event listeners instead)")
    
    # 7. Schema: og:url and schema @id must not contain .html
    og_urls = re.findall(r'og:url.*?content=["\'](.*?)["\']', content)
    for u in og_urls:
        if ".html" in u:
            ERRORS.append(f"{rel}: og:url contains .html → {u}")

def check_sitemap():
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        WARNINGS.append("sitemap.xml: missing")
        return
    content = sm.read_text(encoding="utf-8")
    refs = re.findall(r'https?://[^\s<>]+\.html', content)
    asset_refs = [r for r in refs if ASSET_EXTS.search(r)]
    page_refs = [r for r in refs if not ASSET_EXTS.search(r)]
    if page_refs:
        for r in page_refs:
            ERRORS.append(f"sitemap.xml: contains .html URL → {r}")

def check_llms():
    for fname in ["llms.txt", "llms-full.txt"]:
        f = ROOT / fname
        if not f.exists():
            continue
        content = f.read_text(encoding="utf-8")
        refs = re.findall(r'https?://[^\s<>]+\.html', content)
        for r in refs:
            if not ASSET_EXTS.search(r):
                ERRORS.append(f"{fname}: contains .html URL → {r}")

def check_redirects():
    r = ROOT / "_redirects"
    if not r.exists():
        ERRORS.append("_redirects: missing — required for Cloudflare Pages clean URL enforcement")

def check_headers():
    h = ROOT / "_headers"
    if not h.exists():
        WARNINGS.append("_headers: missing — recommended for security and caching headers")

# --- RUN CHECKS ---
print("\nPre-deploy check — Aetas/Finch Theory sites")
print("=" * 50)

html_files = collect_html_files()
print(f"Checking {len(html_files)} HTML files...")

for f in html_files:
    check_html_file(f)

check_sitemap()
check_llms()
check_redirects()
check_headers()

# --- REPORT ---
if ERRORS:
    print(f"\n✗ ERRORS ({len(ERRORS)}) — fix before deploying:\n")
    for e in ERRORS:
        print(f"  ✗ {e}")

if WARNINGS:
    print(f"\n⚠  WARNINGS ({len(WARNINGS)}) — review before deploying:\n")
    for w in WARNINGS:
        print(f"  ⚠  {w}")

if not ERRORS and not WARNINGS:
    print("\n✓ All checks passed. Safe to deploy.")
elif not ERRORS:
    print(f"\n✓ No errors. {len(WARNINGS)} warning(s) — safe to deploy but review warnings.")
else:
    print(f"\n✗ {len(ERRORS)} error(s) found. Do not deploy until resolved.")
    sys.exit(1)
