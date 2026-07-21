# ============================================================
#  Aetas Wealth - Partner page logo update
#  Replaces the CDN-hosted logo on the three partner microsite
#  pages (TLS Solicitors, Gympanzees, Adeus Life) with the same
#  new AETAS WEALTH lockup SVG used site-wide, then commits/pushes.
#  The SVG (assets/images/aetas-wealth-logo.svg) is already in the
#  repo from the main logo update, so this only patches the HTML.
#
#  Run from the repo root:
#      cd C:\Repos\Aetas-wealth-web
#      .\deploy-partner-logos.ps1
# ============================================================
$ErrorActionPreference = "Stop"

if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "aetas-wealth.com")) {
    Write-Error "This does not look like the Aetas Wealth repo root (CNAME missing or not 'aetas-wealth.com'). Aborting."
    exit 1
}
if (-not (Test-Path "assets/images/aetas-wealth-logo.svg")) {
    Write-Error "assets/images/aetas-wealth-logo.svg is missing. Run deploy-logo-update.ps1 first."
    exit 1
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# Match the partner header block (CDN <img> inside brand-mark + AETAS/Wealth text)
$pattern = '<span class="brand-mark">\s*<img[^>]*>\s*</span>\s*<span class="brand-text">\s*<span class="brand-name">AETAS</span><span class="brand-division">Wealth</span>\s*</span>'
$replacement = '<img class="brand-logo" fetchpriority="high" src="/assets/images/aetas-wealth-logo.svg" alt="Aetas Wealth" width="188" height="52" style="height:52px;width:auto;max-width:none;display:block">'
$rx = [regex]::new($pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)

$targets = @(
    "aetas-tls-solicitors/index.html",
    "aetas-gympanzees/index.html",
    "aetas-adeus-life-digital-wills/index.html"
)

$changed = 0
foreach ($rel in $targets) {
    if (-not (Test-Path $rel)) { Write-Warning "  missing: $rel"; continue }
    $full = [System.IO.Path]::GetFullPath($rel)
    $raw = [System.IO.File]::ReadAllText($full)
    if ($rx.IsMatch($raw)) {
        $new = $rx.Replace($raw, $replacement)
        if ($new -ne $raw) {
            [System.IO.File]::WriteAllText($full, $new, $utf8NoBom)
            $changed++
            Write-Host "  patched $rel"
        }
    } else {
        Write-Warning "  no logo match in $rel (already updated?)"
    }
}
Write-Host ("Patched $changed partner page(s).")

if ($changed -eq 0) {
    Write-Warning "Nothing patched - not committing."
    exit 0
}

git add -A
$pending = git status --porcelain
if ([string]::IsNullOrWhiteSpace($pending)) {
    Write-Host "No changes to commit."
} else {
    git commit -m "Update partner page logos to new AETAS WEALTH lockup (SVG)"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
