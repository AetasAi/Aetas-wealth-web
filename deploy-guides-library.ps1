# ---------------------------------------------------------------
# Aetas Wealth — Guides library deployment (fixed)
# Run from repo root: cd C:\Repos\Aetas-Wealth-Website
#                     .\deploy-guides-library.ps1
# ---------------------------------------------------------------

$repoRoot = "C:\Repos\Aetas-Wealth-Website"

# 1. sitemap.xml
$sitemapPath = Join-Path $repoRoot "sitemap.xml"
$sitemapContent = Get-Content $sitemapPath -Raw
$newEntry = "`n  <!-- guides library index - added June 2026 -->`n  <url>`n    <loc>https://aetas-wealth.com/guides/</loc>`n    <lastmod>2026-06-13</lastmod>`n    <changefreq>monthly</changefreq>`n    <priority>0.8</priority>`n  </url>`n"
$sitemapContent = $sitemapContent -replace "</urlset>", "$newEntry</urlset>"
Set-Content $sitemapPath -Value $sitemapContent -NoNewline -Encoding UTF8
Write-Host "sitemap.xml updated." -ForegroundColor Green

# 2. Root-level pages - add All Guides link
$rootPages = Get-ChildItem $repoRoot -Filter "*.html" -File
$updated = 0
$needle = '<li><a href="guides/pension-drawdown-vs-annuity.html">Pension Drawdown vs Annuity</a></li>'
$replacement = '<li><a href="guides/"><strong>All Guides</strong></a></li>' + "`r`n          " + $needle

foreach ($page in $rootPages) {
    $content = Get-Content $page.FullName -Raw
    if ($content.Contains($needle)) {
        $content = $content.Replace($needle, $replacement)
        Set-Content $page.FullName -Value $content -NoNewline -Encoding UTF8
        Write-Host "  Updated: $($page.Name)" -ForegroundColor Cyan
        $updated++
    }
}

# 3. guides/*.html pages
$guidePages = Get-ChildItem (Join-Path $repoRoot "guides") -Filter "*.html" -File
$needle2 = '<li><a href="pension-drawdown-vs-annuity.html">Pension Drawdown vs Annuity</a></li>'
$replacement2 = '<li><a href="./"><strong>All Guides</strong></a></li>' + "`r`n          " + $needle2

foreach ($page in $guidePages) {
    $content = Get-Content $page.FullName -Raw
    if ($content.Contains($needle2)) {
        $content = $content.Replace($needle2, $replacement2)
        Set-Content $page.FullName -Value $content -NoNewline -Encoding UTF8
        Write-Host "  Updated guide: $($page.Name)" -ForegroundColor Cyan
        $updated++
    }
}

Write-Host ""
Write-Host "$updated pages updated." -ForegroundColor Green
Write-Host ""
Write-Host "Now run:" -ForegroundColor Yellow
Write-Host "  git add -A" -ForegroundColor White
Write-Host "  git commit -m `"Add guides library, update footer and sitemap`"" -ForegroundColor White
Write-Host "  git push" -ForegroundColor White
