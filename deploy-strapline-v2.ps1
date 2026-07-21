# ============================================================
#  Aetas Wealth - Strapline v2 (under logo + sticky)
#  Moves the "Connecting your wealth and wellbeing" strapline
#  from the full-width centred band into the sticky header,
#  left-aligned directly under the logo. Then commits and pushes.
#
#  Safe to run after deploy-strapline.ps1 (it migrates the old band).
#  Run from the repo root:
#      cd C:\Repos\Aetas-wealth-web
#      .\deploy-strapline-v2.ps1
# ============================================================
$ErrorActionPreference = "Stop"

if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "aetas-wealth.com")) {
    Write-Error "This does not look like the Aetas Wealth repo root (CNAME missing or not 'aetas-wealth.com'). Aborting."
    exit 1
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# New strapline band: soft tint, left-aligned under the logo (inside the sticky header)
$band = @'
<div class="brand-strapline" style="background:#f4f6fb;border-top:1px solid #e6e8ee;"><div style="max-width:1200px;margin-inline:auto;padding-inline:clamp(1.25rem,4vw,2.5rem);padding-block:8px;text-align:left;font-size:0.9rem;font-weight:600;letter-spacing:0.02em;color:#00205B;font-family:'Open Sans',-apple-system,BlinkMacSystemFont,sans-serif;">Connecting your <span style="color:#00747E">wealth</span> and <span style="color:#00747E">wellbeing</span></div></div>
'@

# Match the closing header tag immediately followed by the OLD full-width band,
# and rebuild as: new band (inside header) then </header>.
$pattern = '</header>\s*<div class="brand-strapline"[^>]*>.*?</div>'
$rx = [regex]::new($pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
$evaluator = { param($m) $band + "`n</header>" }

$changed = 0
$skipped = 0
Get-ChildItem -Path . -Recurse -Filter *.html | ForEach-Object {
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    if ($rx.IsMatch($raw)) {
        $new = $rx.Replace($raw, $evaluator, 1)
        [System.IO.File]::WriteAllText($_.FullName, $new, $utf8NoBom)
        $changed++
        Write-Host ("  updated: " + $_.FullName.Substring((Get-Location).Path.Length + 1))
    } elseif ($raw -match 'brand-strapline') {
        $skipped++   # already migrated
    }
}
Write-Host ("Migrated $changed page(s) to under-logo sticky strapline. Skipped $skipped already-migrated page(s).")

if ($changed -eq 0) {
    Write-Warning "No pages migrated - nothing to commit."
    exit 0
}

git add -A
$pending = git status --porcelain
if ([string]::IsNullOrWhiteSpace($pending)) {
    Write-Host "No changes to commit."
} else {
    git commit -m "Move strapline under the logo inside the sticky header (left-aligned)"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
