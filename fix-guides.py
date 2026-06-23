import os, re

root = r"C:\Repos\Aetas-wealth-web"

# Root-level pages (guides/ prefix)
old1 = '<li><a href="guides/pension-drawdown-vs-annuity.html">Pension Drawdown vs Annuity</a></li>\n<li><a href="guides/inheritance-tax-planning-options.html">IHT Planning Options</a></li>\n<li><a href="guides/financial-adviser-vs-wealth-manager.html">Adviser vs Wealth Manager</a></li>\n<li><a href="guides/why-cashflow-modelling-matters.html">Why Cashflow Modelling Matters</a></li>'

new1 = '<li><a href="guides/pension-drawdown-vs-annuity.html">Pension Drawdown vs Annuity</a></li>\n<li><a href="guides/inheritance-tax-planning-options.html">IHT Planning Options</a></li>\n<li><a href="guides/financial-adviser-vs-wealth-manager.html">Adviser vs Wealth Manager</a></li>\n<li><a href="guides/why-cashflow-modelling-matters.html">Why Cashflow Modelling Matters</a></li>\n<li><a href="guides/business-relief-vs-gifting.html">Business Relief vs Gifting</a></li>\n<li><a href="guides/financial-planning-in-your-30s-and-40s.html">Financial Planning in Your 30s &amp; 40s</a></li>\n<li><a href="guides/financial-planning-vs-investment-management.html">Financial Planning vs Investment Management</a></li>'

# Subdirectory pages (../guides/ prefix)
old2 = '<li><a href="../guides/pension-drawdown-vs-annuity.html">Pension Drawdown vs Annuity</a></li>\n<li><a href="../guides/inheritance-tax-planning-options.html">IHT Planning Options</a></li>\n<li><a href="../guides/financial-adviser-vs-wealth-manager.html">Adviser vs Wealth Manager</a></li>\n<li><a href="../guides/why-cashflow-modelling-matters.html">Why Cashflow Modelling Matters</a></li>'

new2 = '<li><a href="../guides/pension-drawdown-vs-annuity.html">Pension Drawdown vs Annuity</a></li>\n<li><a href="../guides/inheritance-tax-planning-options.html">IHT Planning Options</a></li>\n<li><a href="../guides/financial-adviser-vs-wealth-manager.html">Adviser vs Wealth Manager</a></li>\n<li><a href="../guides/why-cashflow-modelling-matters.html">Why Cashflow Modelling Matters</a></li>\n<li><a href="../guides/business-relief-vs-gifting.html">Business Relief vs Gifting</a></li>\n<li><a href="../guides/financial-planning-in-your-30s-and-40s.html">Financial Planning in Your 30s &amp; 40s</a></li>\n<li><a href="../guides/financial-planning-vs-investment-management.html">Financial Planning vs Investment Management</a></li>'

count = 0
for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Normalise CRLF to LF for matching
        content_lf = content.replace('\r\n', '\n')
        changed = False
        if old1 in content_lf:
            content_lf = content_lf.replace(old1, new1)
            changed = True
        elif old2 in content_lf:
            content_lf = content_lf.replace(old2, new2)
            changed = True
        if changed:
            with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content_lf)
            print(f"Fixed: {fname}")
            count += 1

print(f"\nTotal: {count} files updated")
