# ============================================================
#  Aetas Wealth - Cache fix so CSS changes reach returning visitors
#   1) Bump styles-v4.css -> styles-v5.css (new URL flushes the stuck
#      1-year immutable cache; carries the a11y fixes already in v4)
#   2) Repoint every page's stylesheet link to styles-v5.css
#   3) _headers: CSS/JS -> short revalidating cache (max-age=3600);
#      images stay long-immutable (they are genuinely static)
#  Commits and pushes.  Run from repo root:
#      cd C:\Repos\Aetas-wealth-web ; .\deploy-wealth-cache-fix.ps1
# ============================================================
$ErrorActionPreference = "Stop"
if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "aetas-wealth.com")) {
    Write-Error "Not the Aetas Wealth repo root. Aborting."; exit 1
}
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# --- 1) Create styles-v5.css from current styles-v4.css (has the a11y fixes) ---
if (-not (Test-Path "assets/css/styles-v4.css")) { Write-Error "styles-v4.css missing."; exit 1 }
Copy-Item "assets/css/styles-v4.css" "assets/css/styles-v5.css" -Force
Write-Host "Created assets/css/styles-v5.css"

# --- 2) Repoint stylesheet links across all HTML ---
$changed = 0
Get-ChildItem -Path . -Recurse -Filter *.html | ForEach-Object {
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    if ($raw.Contains('styles-v4.css')) {
        $new = $raw.Replace('styles-v4.css', 'styles-v5.css')
        [System.IO.File]::WriteAllText($_.FullName, $new, $utf8NoBom)
        $changed++
    }
}
Write-Host "Repointed stylesheet link on $changed page(s)."

# --- 3) _headers: CSS/JS revalidating, images immutable ---
$hp = [System.IO.Path]::GetFullPath('_headers')
$h = [System.IO.File]::ReadAllText($hp)
$opt = [System.Text.RegularExpressions.RegexOptions]::None
$h = [regex]::Replace($h, '/assets/\*\r?\n\s*Cache-Control: public, max-age=31536000, immutable',
    "/assets/css/*`n  Cache-Control: public, max-age=3600`n`n/assets/js/*`n  Cache-Control: public, max-age=3600`n`n/assets/images/*`n  Cache-Control: public, max-age=31536000, immutable")
$h = [regex]::Replace($h, '/\*\.css\r?\n\s*Cache-Control: public, max-age=31536000, immutable',
    "/*.css`n  Cache-Control: public, max-age=3600")
$h = [regex]::Replace($h, '/\*\.js\r?\n\s*Cache-Control: public, max-age=31536000, immutable',
    "/*.js`n  Cache-Control: public, max-age=3600")
[System.IO.File]::WriteAllText($hp, $h, $utf8NoBom)
Write-Host "Updated _headers cache rules (CSS/JS revalidating; images immutable)."

# --- Commit & push ---
git add -A
if ([string]::IsNullOrWhiteSpace((git status --porcelain))) { Write-Host "No changes to commit." }
else {
    git commit -m "cache: bump CSS to styles-v5.css and set CSS/JS to revalidating cache so updates reach returning visitors"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
