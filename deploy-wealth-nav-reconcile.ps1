# ============================================================
#  Aetas Wealth - Nav/footer reconcile + duplicate consolidation
#   1) Business Owners: remove from Life Stages nav dropdown; add to Services (nav + footer)
#   2) Footer Life Stage column reconciled to 6 true stages (adds Leaving a Legacy),
#      for both the standard and the legacy plain-<h3> footer templates
#   3) Footer Services: add Director & Owner Advisory + Pension IHT Planning
#   4) Retire duplicates: repoint millennials/ -> planning-in-your-30s-and-40s/ and
#      business-planning/ -> business-owners everywhere; 301-redirect; remove pages; sitemap
#  Commits and pushes.  Run from repo root:
#      cd C:\Repos\Aetas-wealth-web ; .\deploy-wealth-nav-reconcile.ps1
# ============================================================
$ErrorActionPreference = "Stop"
if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "aetas-wealth.com")) {
    Write-Error "Not the Aetas Wealth repo root. Aborting."; exit 1
}
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$optS = [System.Text.RegularExpressions.RegexOptions]::Singleline

$LS6 = @(
  @('young-professionals/','Young Professionals'),
  @('planning-in-your-30s-and-40s/','Planning in Your 30s &amp; 40s'),
  @('mid-life/','Mid-Life Planning'),
  @('approaching-retirement/','Approaching Retirement'),
  @('in-retirement/','In Retirement'),
  @('leaving-a-legacy/','Leaving a Legacy')
)
function Get-LSItems([string]$pre){
  $sb=''
  foreach($x in $LS6){ $sb += "`n<li><a href=""$pre$($x[0])"">$($x[1])</a></li>" }
  return $sb + "`n"
}

$rx1 = [regex]::new('(<li><a href="[^"]*mid-life/">Mid-Life Planning</a></li>)\s*<li><a href="[^"]*business-owners">Business Owners</a></li>')
$rx2 = [regex]::new('(<li><a href="([^"]*)services/pension-inheritance-tax-planning\.html">Pension IHT Planning</a></li>)(?!<li><a href="[^"]*business-owners">Business Owners)')
$rx3 = [regex]::new('(<h3\s*><a href="([^"]*)life-stage/"[^>]*>Life Stage Planning</a></h3>\s*)<ul>.*?</ul>', $optS)
$rx4 = [regex]::new('(<li><a href="([^"]*)services/protection-planning">Protection Planning</a></li>)')
$rx6 = [regex]::new('(<h3[^>]*>Life Stage Planning</h3>\s*<ul>)\s*<li><a href="([^"]*)young-professionals/"[^>]*>.*?</ul>', $optS)

$changed = 0
Get-ChildItem -Path . -Recurse -Filter *.html | ForEach-Object {
    if ($_.FullName -like '*\millennials\*' -or $_.FullName -like '*\business-planning\*') { return }  # being deleted
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    $c = $raw
    $c = $rx1.Replace($c, '$1', 1)                                                        # 1 remove BO from Life Stages
    $c = $rx2.Replace($c, '$1<li><a href="$2business-owners">Business Owners</a></li>', 1) # 2 add BO to Services nav
    $c = $rx3.Replace($c, { param($m) $m.Groups[1].Value + '<ul>' + (Get-LSItems $m.Groups[2].Value) + '</ul>' })  # 3 std footer LS
    $fi = $c.IndexOf('<footer')                                                           # 4 footer Services add
    if ($fi -ge 0 -and -not $c.Substring($fi).Contains('services/director-owner-advisory')) {
        $c = $rx4.Replace($c, '$1<li><a href="$2services/director-owner-advisory">Director &amp; Owner Advisory</a></li><li><a href="$2services/pension-inheritance-tax-planning">Pension IHT Planning</a></li><li><a href="$2business-owners">Business Owners</a></li>', 1)
    }
    $c = [regex]::Replace($c, 'href="([^"]*)millennials/"', 'href="$1planning-in-your-30s-and-40s/"')  # 5 repoint dups
    $c = [regex]::Replace($c, 'href="([^"]*)business-planning/"', 'href="$1business-owners"')
    $c = $rx6.Replace($c, { param($m) $m.Groups[1].Value + (Get-LSItems $m.Groups[2].Value) + '</ul>' })  # 6 legacy footer LS
    if ($c -ne $raw) {
        [System.IO.File]::WriteAllText($_.FullName, $c, $utf8NoBom)
        $changed++
    }
}
Write-Host "Transformed $changed page(s)."

# ---- Retire duplicate pages ----
git rm -rf --ignore-unmatch --quiet millennials business-planning | Out-Null
Write-Host "Removed duplicate pages millennials/ and business-planning/."

# ---- 301 redirects ----
$rd = [System.IO.File]::ReadAllText('_redirects')
if (-not $rd.Contains('Retired duplicate/orphan pages')) {
    $block = "# Retired duplicate/orphan pages -> canonical`n/millennials/book /book 301`n/millennials/book.html /book 301`n/millennials/* /planning-in-your-30s-and-40s/ 301`n/business-planning/* /business-owners 301`n`n"
    $rd = $rd.Replace('# Splat redirect: any', $block + '# Splat redirect: any')
    [System.IO.File]::WriteAllText([System.IO.Path]::GetFullPath('_redirects'), $rd, $utf8NoBom)
    Write-Host "Added 301 redirects."
}

# ---- Sitemap cleanup ----
$sm = [System.IO.File]::ReadAllText('sitemap.xml')
$sm = [regex]::Replace($sm, '<!--[^\r\n]*millennials[^\r\n]*-->', '')
$sm = [regex]::Replace($sm, '\s*<url>\s*<loc>https://aetas-wealth\.com/millennials/</loc>.*?</url>', '', $optS)
$sm = [regex]::Replace($sm, '\s*<url>\s*<loc>https://aetas-wealth\.com/business-planning/</loc>.*?</url>', '', $optS)
[System.IO.File]::WriteAllText([System.IO.Path]::GetFullPath('sitemap.xml'), $sm, $utf8NoBom)
Write-Host "Cleaned sitemap."

# ---- Commit & push ----
git add -A
if ([string]::IsNullOrWhiteSpace((git status --porcelain))) { Write-Host "No changes to commit." }
else {
    git commit -m "Reclassify Business Owners to Services; reconcile footer life stages; retire duplicate pages (301s)"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
