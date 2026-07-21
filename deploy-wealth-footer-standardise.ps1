# ============================================================
#  Aetas Wealth - Footer standardisation
#  Replaces every page footer with one canonical footer (absolute
#  links, works at any depth), unifying the ~9 footer layouts.
#  EXCLUDES the 3 partner microsites (intentional minimal footers).
#  Commits and pushes.  Run from repo root:
#      cd C:\Repos\Aetas-wealth-web ; .\deploy-wealth-footer-standardise.ps1
# ============================================================
$ErrorActionPreference = "Stop"
if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "aetas-wealth.com")) {
    Write-Error "Not the Aetas Wealth repo root. Aborting."; exit 1
}
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$footer = @'
<footer class="site-footer">
<div class="container">
<div class="footer-grid">
<div>
<h3>Site</h3>
<ul>
<li><a href="/">Home</a></li>
<li><a href="/you/">You</a></li>
<li><a href="/our-approach">Approach</a></li>
<li><a href="/our-people">Us</a></li>
<li><a href="/entity/aetas-wealth">Company Profile</a></li>
<li><a href="/life-stage/">Life Stages</a></li>
<li><a href="/fees">Fees</a></li>
<li><a href="/insights/">Insights</a></li>
<li><a href="/contact">Contact</a></li>
</ul>
</div>
<div>
<h3>Services</h3>
<ul>
<li><a href="/services/pensions-retirement">Pensions &amp; Retirement</a></li>
<li><a href="/services/investment-management">Investments</a></li>
<li><a href="/services/inheritance-tax">Inheritance Tax Planning</a></li>
<li><a href="/services/later-life-planning">Later Life Planning</a></li>
<li><a href="/services/financial-planning">Financial Planning</a></li>
<li><a href="/services/cash-flow-planning">Cash Flow Planning</a></li>
<li><a href="/services/protection-planning">Protection Planning</a></li><li><a href="/services/director-owner-advisory">Director &amp; Owner Advisory</a></li><li><a href="/services/pension-inheritance-tax-planning">Pension IHT Planning</a></li><li><a href="/business-owners">Business Owners</a></li>
</ul>
</div>
<div>
<h3>Useful</h3>
<ul>
<li><a href="/working-with-us">Working with Us</a></li>
<li><a href="/glossary/">Glossary</a></li>
<li><a href="/professional-introducers">Professional Introducers</a></li>
<li><a href="/lifetime-to-legacy">Our Philosophy</a></li>
</ul>
<h3 style="margin-top:1.5rem;">The Aetas Group</h3>
<ul>
<li><a href="https://aetas-wealth.com/" target="_blank" rel="noopener">Aetas Wealth</a></li>
<li><a href="https://performance.aetas-wealth.com/" target="_blank" rel="noopener">Aetas Performance</a></li>
<li><a href="https://impact.aetas-wealth.com/" target="_blank" rel="noopener">Aetas Impact</a></li>
</ul>
</div>
<div>
<h3>Offices</h3>
<p style="margin: 0 0 0.4rem 0; font-weight: 600; color: #fff;">London</p>
<ul style="margin-bottom: 1.25rem;">
<li>13 Hanover Square</li>
<li>Mayfair, London</li>
<li>W1S 1HN</li>
</ul>
<p style="margin: 0 0 0.4rem 0; font-weight: 600; color: #fff;">Norwich</p>
<ul>
<li>Insight House</li>
<li>7a Alkmaar Way</li>
<li>Norwich International Business Park</li>
<li>NR6 6BF</li>
</ul>
</div>
</div>
<div class="footer-grid footer-grid-hubs" style="margin-top: 0.5rem; padding-top: 0.75rem; padding-bottom: 0.5rem; border-top: 1px solid rgba(255,255,255,0.08);">
<div>
<h3 ><a href="/case-studies/" style="color: #fff; text-decoration: none; font-weight: 700; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em;">Case Studies</a></h3>
</div>
<div>
<h3 ><a href="/life-stage/" style="color: #fff; text-decoration: none; font-weight: 700; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em;">Life Stage Planning</a></h3>
<ul>
<li><a href="/young-professionals/">Young Professionals</a></li>
<li><a href="/planning-in-your-30s-and-40s/">Planning in Your 30s &amp; 40s</a></li>
<li><a href="/mid-life/">Mid-Life Planning</a></li>
<li><a href="/approaching-retirement/">Approaching Retirement</a></li>
<li><a href="/in-retirement/">In Retirement</a></li>
<li><a href="/leaving-a-legacy/">Leaving a Legacy</a></li>
</ul>
</div>
<div>
<h3 ><a href="/guides/" style="color: #fff; text-decoration: none; font-weight: 700; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em;">Guides</a></h3>
<ul>
<li><a href="/guides/pension-drawdown-vs-annuity">Pension Drawdown vs Annuity</a></li>
<li><a href="/guides/inheritance-tax-planning-options">IHT Planning Options</a></li>
<li><a href="/guides/financial-adviser-vs-wealth-manager">Adviser vs Wealth Manager</a></li>
<li><a href="/guides/why-cashflow-modelling-matters">Why Cashflow Modelling Matters</a></li>
<li><a href="/guides/business-relief-vs-gifting">Business Relief vs Gifting</a></li>
<li><a href="/guides/financial-planning-in-your-30s-and-40s">Financial Planning in Your 30s &amp; 40s</a></li>
<li><a href="/guides/financial-planning-vs-investment-management">Financial Planning vs Investment Management</a></li>
</ul>
</div>
</div>
<div style="text-align:center;padding:0.75rem var(--gutter);border-top:1px solid rgba(255,255,255,0.06);">
  <span style="font-size:0.72rem;letter-spacing:0.16em;text-transform:uppercase;color:rgba(255,255,255,0.25);font-weight:500;">Lifetime to Legacy™</span>
</div>
<div class="footer-bottom">
<p><strong>Aetas Wealth</strong> is a trading style of Insight Financial Associates Limited, which is authorised and regulated by the Financial Conduct Authority (FCA) under registration number 458421. Insight Financial Associates Limited is a company incorporated in England and Wales with company number 05054886. Registered office: Insight House, 7a Alkmaar Way, Norwich International Business Park, Norwich, NR6 6BF.</p>
<p>The Financial Conduct Authority does not regulate Wills, Trusts, Tax advice or Cash Flow Planning. The value of your investments can go down as well as up, so you could get back less than you invested. The guidance contained on this website is subject to the UK regulatory regime and is therefore primarily targeted at consumers based in the UK.</p>
<p>&copy; <span id="yr"></span> Aetas Wealth. All rights reserved. <a href="/privacy">Privacy &amp; Cookies</a> &middot; <a href="/terms">Terms of Use</a> &middot; <a href="/complaints">Complaints</a></p>
</div>
</div>
</footer>
'@

$rx = [regex]::new('<footer class="site-footer">.*?</footer>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
$eval = { param($m) $footer }

$changed = 0
Get-ChildItem -Path . -Recurse -Filter *.html | ForEach-Object {
    if ($_.FullName -match 'aetas-adeus-life-digital-wills|aetas-gympanzees|aetas-tls-solicitors') { return }  # partner microsites
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    if (-not $rx.IsMatch($raw)) { return }
    $new = $rx.Replace($raw, $eval, 1)
    if ($new -ne $raw) {
        [System.IO.File]::WriteAllText($_.FullName, $new, $utf8NoBom)
        $changed++
        Write-Host ("  standardised: " + $_.FullName.Substring((Get-Location).Path.Length + 1))
    }
}
Write-Host ("Standardised footer on $changed page(s).")
if ($changed -eq 0) { Write-Warning "Nothing changed - not committing."; exit 0 }

git add -A
if ([string]::IsNullOrWhiteSpace((git status --porcelain))) { Write-Host "No changes to commit." }
else {
    git commit -m "Standardise site footer across all pages (unify ~9 layouts into one)"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
