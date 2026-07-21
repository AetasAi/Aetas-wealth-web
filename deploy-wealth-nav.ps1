# ============================================================
#  Aetas Wealth - Nav restructure
#   1) Rename nav item "People" -> "Us" (header AND footer list items)
#   2) Remove "Fees" from the TOP NAV only (kept in the footer)
#  Breadcrumb "People" links are left untouched.
#  Commits and pushes. Run from repo root:
#      cd C:\Repos\Aetas-wealth-web ; .\deploy-wealth-nav.ps1
# ============================================================
$ErrorActionPreference = "Stop"
if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "aetas-wealth.com")) {
    Write-Error "Not the Aetas Wealth repo root. Aborting."; exit 1
}
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# Op1: rename list-item People -> Us (header + footer)
$op1 = [regex]::new('(<li><a href="[^"]*our-people[^"]*"[^>]*>)People(</a></li>)')
# Op2: remove the header Fees (the Fees li immediately after the our-people/Us li)
$op2 = [regex]::new('(<li><a href="[^"]*our-people[^"]*"[^>]*>Us</a></li>)\s*<li><a href="[^"]*fees[^"]*"[^>]*>Fees</a></li>')

$changed = 0
Get-ChildItem -Path . -Recurse -Filter *.html | ForEach-Object {
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    $new = $op1.Replace($raw, '${1}Us${2}')
    $new = $op2.Replace($new, '${1}')
    if ($new -ne $raw) {
        [System.IO.File]::WriteAllText($_.FullName, $new, $utf8NoBom)
        $changed++
        Write-Host ("  updated: " + $_.FullName.Substring((Get-Location).Path.Length + 1))
    }
}
Write-Host ("Updated $changed page(s).")
if ($changed -eq 0) { Write-Warning "Nothing changed - not committing."; exit 0 }

git add -A
if ([string]::IsNullOrWhiteSpace((git status --porcelain))) { Write-Host "No changes to commit." }
else {
    git commit -m "Nav: rename People to Us (header+footer); remove Fees from top nav"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
