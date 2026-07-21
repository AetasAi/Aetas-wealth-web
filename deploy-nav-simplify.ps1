<#
  deploy-nav-simplify.ps1
  Removes the "Life Stages" and "Services" dropdowns from the main (top) nav
  on every page. Both remain fully maintained in the footer:
    - Life Stages: hub /life-stage/ + all 6 life-stage pages (footer hub column)
    - Services:    all service pages (footer Services column)
  (The old "Services" nav parent pointed at /services/, which 404s - so nothing
   of value is lost.) The footer is intentionally left unchanged.

  Idempotent. RUN FROM THE REPO ROOT:
    git pull
    .\deploy-nav-simplify.ps1
#>

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$utf8 = New-Object System.Text.UTF8Encoding($false)   # UTF-8, no BOM

Write-Host "== Aetas Wealth :: simplify main nav (remove Life Stages + Services dropdowns) ==" -ForegroundColor Cyan

# Remove each top-nav dropdown <li> block (dropdowns never appear in the footer).
$pattern = '\s*<li class="nav-has-dropdown">.*?</ul></li>'

$files = Get-ChildItem -Path $PSScriptRoot -Recurse -Filter *.html |
  Where-Object { $_.FullName -notmatch '\\node_modules\\' }

$pagesChanged = 0
$blocksRemoved = 0
foreach ($f in $files) {
  $c = [System.IO.File]::ReadAllText($f.FullName)
  if ($c -notmatch 'nav-has-dropdown') { continue }
  $matches = [regex]::Matches($c, $pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
  $n = [regex]::Replace($c, $pattern, '', [System.Text.RegularExpressions.RegexOptions]::Singleline)
  if ($n -ne $c) {
    [System.IO.File]::WriteAllText($f.FullName, $n, $utf8)
    $pagesChanged++
    $blocksRemoved += $matches.Count
  }
}
Write-Host ("  removed {0} dropdown block(s) across {1} page(s)" -f $blocksRemoved, $pagesChanged) -ForegroundColor Green

Write-Host "== git ==" -ForegroundColor Cyan
git add -A
git commit -m "Simplify main nav: remove Life Stages and Services dropdowns (retained in footer)"
git push
Write-Host "== done ==" -ForegroundColor Cyan
