# ============================================================
#  Aetas Wealth - Strapline v3 ("wealth" solid / "wellbeing" script)
#  Restyles the header strapline: "wellbeing" in Dancing Script with
#  a hand-drawn underline, gentle fade-in on load. Loads the web font
#  and adds the needed CSS into each page head. Commits and pushes.
#
#  Run after the strapline is already under the logo (v2). From repo root:
#      cd C:\Repos\Aetas-wealth-web
#      .\deploy-strapline-v3.ps1
# ============================================================
$ErrorActionPreference = "Stop"

if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "aetas-wealth.com")) {
    Write-Error "This does not look like the Aetas Wealth repo root (CNAME missing or not 'aetas-wealth.com'). Aborting."
    exit 1
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# Head block: web font + keyframes + strapline classes (inserted before </head>)
$head = @'
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
<style id="aetas-strap-style">
@keyframes aetasStrapIn{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
.aetas-strap{animation:aetasStrapIn 1s ease .15s both}
.aetas-strap .w{color:#00205B;font-weight:700}
.aetas-strap .wb{font-family:'Dancing Script',cursive;font-weight:700;font-size:1.55em;color:#00747E;line-height:1;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='130' height='9' viewBox='0 0 130 9'%3E%3Cpath d='M2 6 C 34 2, 96 2, 128 5' stroke='%2300aabb' stroke-width='2.4' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:left 100%;background-size:100% 7px;padding:0 2px 5px}
</style>
'@

$inner = 'Connecting your <span class="w">wealth</span> and <span class="wb">wellbeing</span>'

# Match the existing (v2) strapline band: outer div + inner container div.
$bandRx = [regex]::new('(<div class="brand-strapline"[^>]*>)\s*<div([^>]*)>.*?</div>\s*</div>',
                       [System.Text.RegularExpressions.RegexOptions]::Singleline)
$bandEval = { param($m) $m.Groups[1].Value + '<div' + $m.Groups[2].Value + ' class="aetas-strap">' + $inner + '</div></div>' }

$changed = 0
$skipped = 0
Get-ChildItem -Path . -Recurse -Filter *.html | ForEach-Object {
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    if ($raw -match 'aetas-strap') { $skipped++; return }        # already styled
    if (-not $bandRx.IsMatch($raw)) { return }                   # no strapline on this page

    $new = $raw
    if ($new -notmatch 'aetas-strap-style') {
        $new = [regex]::Replace($new, '</head>', ($head -replace '\$','$$$$') + "`n</head>", 1)
    }
    $new = $bandRx.Replace($new, $bandEval, 1)

    [System.IO.File]::WriteAllText($_.FullName, $new, $utf8NoBom)
    $changed++
    Write-Host ("  restyled: " + $_.FullName.Substring((Get-Location).Path.Length + 1))
}
Write-Host ("Restyled $changed page(s). Skipped $skipped already-styled page(s).")

if ($changed -eq 0) { Write-Warning "Nothing changed - not committing."; exit 0 }

git add -A
$pending = git status --porcelain
if ([string]::IsNullOrWhiteSpace($pending)) {
    Write-Host "No changes to commit."
} else {
    git commit -m "Restyle strapline: 'wellbeing' in script with flourish + fade-in"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
