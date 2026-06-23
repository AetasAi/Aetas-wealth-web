"""
fix-arrows-and-guides.py
Fixes two issues across Aetas-wealth-web:
1. Mangled arrow characters (â££££ → →) in 4 pages
2. Missing 'Business Relief vs Gifting' and 'Financial Planning vs Investment Management'
   guide links from footer on pages that only had 4-5 guides
"""

import glob, os

ROOT = r"C:\Repos\Aetas-wealth-web"

# ── 1. Fix mangled arrows ────────────────────────────────────────────────────
arrow_fixed = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True) + \
         glob.glob(os.path.join(ROOT, "*.html")):
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()
    if "â££££" in content:
        content = content.replace("â££££", "→")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(content)
        arrow_fixed += 1
        print(f"  ✓ Arrow fixed: {os.path.relpath(f, ROOT)}")

print(f"\n✓ Arrow fix: {arrow_fixed} files updated")

# ── 2. Fix missing guide links ───────────────────────────────────────────────
# Three patterns depending on file location

# Pattern A — life-stage pages (millennials/, young-professionals/ etc.)
A_OLD = '<li><a href="../guides/financial-planning-in-your-30s-and-40s.html">Planning in Your 30s and 40s</a></li>'
A_NEW = A_OLD + """
          <li><a href="../guides/business-relief-vs-gifting.html">Business Relief vs Gifting</a></li>
          <li><a href="../guides/financial-planning-vs-investment-management.html">Financial Planning vs Investment Management</a></li>"""

# Pattern B — subdirectory pages using &amp; (case-studies/, guides/, etc.)
B_OLD = '<li><a href="../guides/financial-planning-in-your-30s-and-40s.html">Planning in Your 30s &amp; 40s</a></li>'
B_NEW = B_OLD + """
<li><a href="../guides/business-relief-vs-gifting.html">Business Relief vs Gifting</a></li>
<li><a href="../guides/financial-planning-vs-investment-management.html">Financial Planning vs Investment Management</a></li>"""

# Pattern C — guides/ pages (no ../ prefix, relative)
C_OLD = '<li><a href="financial-planning-in-your-30s-and-40s.html">Planning in Your 30s and 40s</a></li>'
C_NEW = C_OLD + """
          <li><a href="business-relief-vs-gifting.html">Business Relief vs Gifting</a></li>
          <li><a href="financial-planning-vs-investment-management.html">Financial Planning vs Investment Management</a></li>"""

# Pattern D — insights/index.html (ends with why-cashflow)
D_OLD = '<li><a href="../guides/why-cashflow-modelling-matters.html">Why Cashflow Modelling Matters</a></li>\n\n</ul>'
D_NEW = '''<li><a href="../guides/why-cashflow-modelling-matters.html">Why Cashflow Modelling Matters</a></li>

<li><a href="../guides/financial-planning-in-your-30s-and-40s.html">Planning in Your 30s &amp; 40s</a></li>

<li><a href="../guides/business-relief-vs-gifting.html">Business Relief vs Gifting</a></li>

<li><a href="../guides/financial-planning-vs-investment-management.html">Financial Planning vs Investment Management</a></li>

</ul>'''

guides_fixed = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True) + \
         glob.glob(os.path.join(ROOT, "*.html")):
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()

    if "business-relief-vs-gifting" in content:
        continue  # already has it

    new_content = content
    for old, new in [(A_OLD, A_NEW), (B_OLD, B_NEW), (C_OLD, C_NEW), (D_OLD, D_NEW)]:
        if old in content:
            new_content = content.replace(old, new)
            break

    if new_content != content:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(new_content)
        guides_fixed += 1
        print(f"  ✓ Guides fixed: {os.path.relpath(f, ROOT)}")

print(f"\n✓ Guide fix: {guides_fixed} files updated")
print("\nDone. Now run:")
print("  git add -A")
print('  git commit -m "Fix mangled arrows + add missing 2 guide links to all footers"')
print("  git push")
