# ============================================================
#  Aetas Wealth - Strapline deployment
#  Adds the brand strapline "Connecting your wealth and wellbeing"
#  as a soft band directly under the header on every page, then
#  commits and pushes. Cloudflare Pages redeploys on push.
#
#  Run from the repo root:
#      cd C:\Repos\Aetas-wealth-web
#      .\deploy-strapline.ps1
# ============================================================
$ErrorActionPreference = "Stop"

if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "aetas-wealth.com")) {
    Write-Error "This does not look like the Aetas Wealth repo root (CNAME missing or not 'aetas-wealth.com'). Aborting."
    exit 1
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# The strapline band (inserted immediately after the site header)
$band = @'
<div class="brand-strapline" style="background:#f4f6fb;border-top:1px solid #e6e8ee;text-align:center;padding:9px 12px;font-size:0.9rem;font-weight:600;letter-spacing:0.02em;color:#00205B;font-family:'Open Sans',-apple-system,BlinkMacSystemFont,sans-serif;">Connecting your <span style="color:#00747E">wealth</span> and <span style="color:#00747E">wellbeing</span></div>
'@

# Match the whole site header block; the band goes right after it.
$pattern = '<header class="site-header">.*?</header>'
$rx = [regex]::new($pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
$evaluator = { param($m) $m.Value + "`n" + $band }

$changed = 0
$skipped = 0
Get-ChildItem -Path . -Recurse -Filter *.html | ForEach-Object {
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    if ($raw -match 'brand-strapline') { $skipped++; return }   # already has it
    if ($rx.IsMatch($raw)) {
        $new = $rx.Replace($raw, $evaluator, 1)
        [System.IO.File]::WriteAllText($_.FullName, $new, $utf8NoBom)
        $changed++
        Write-Host ("  strapline added: " + $_.FullName.Substring((Get-Location).Path.Length + 1))
    }
}
Write-Host ("Added strapline to $changed page(s). Skipped $skipped already-done page(s).")

if ($changed -eq 0) {
    Write-Warning "No pages updated - nothing to commit."
    exit 0
}

git add -A
$pending = git status --porcelain
if ([string]::IsNullOrWhiteSpace($pending)) {
    Write-Host "No changes to commit."
} else {
    git commit -m "Add brand strapline band ('Connecting your wealth and wellbeing') to all pages"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
