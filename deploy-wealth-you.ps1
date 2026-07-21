# ============================================================
#  Aetas Wealth - Add "You" page to navigation
#  Adds "You" as the FIRST item in the top nav and after Home in
#  the footer Site column, across all pages. The you/ page itself
#  is already in place. Commits and pushes (includes the new page).
#  Run from repo root:  cd C:\Repos\Aetas-wealth-web ; .\deploy-wealth-you.ps1
# ============================================================
$ErrorActionPreference = "Stop"
if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "aetas-wealth.com")) {
    Write-Error "Not the Aetas Wealth repo root. Aborting."; exit 1
}
if (-not (Test-Path "you/index.html")) {
    Write-Error "you/index.html is missing - place the new page first."; exit 1
}
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# Header: insert You first in nav-links (skip if a You link is already there)
$hdr = [regex]::new('(<ul class="nav-links">)(?!\s*<li><a href="[^"]*you/")')
# Footer: insert You after the Site-column Home link (skip if already there)
$ftr = [regex]::new('(<h3>Site</h3>\s*<ul>\s*<li><a href="[^"]*">Home</a></li>)(?!\s*<li><a href="[^"]*you/")')

$changed = 0
Get-ChildItem -Path . -Recurse -Filter *.html | ForEach-Object {
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    $new = $hdr.Replace($raw, "`$1`n      <li><a href=`"/you/`">You</a></li>", 1)
    $new = $ftr.Replace($new, "`$1`n<li><a href=`"/you/`">You</a></li>", 1)
    if ($new -ne $raw) {
        [System.IO.File]::WriteAllText($_.FullName, $new, $utf8NoBom)
        $changed++
        Write-Host ("  updated: " + $_.FullName.Substring((Get-Location).Path.Length + 1))
    }
}
Write-Host ("Added 'You' to nav on $changed page(s).")

git add -A
if ([string]::IsNullOrWhiteSpace((git status --porcelain))) { Write-Host "No changes to commit." }
else {
    git commit -m "Add You page; add 'You' first in top nav and footer site-wide"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
