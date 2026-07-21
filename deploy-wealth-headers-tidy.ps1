# ============================================================
#  Aetas Wealth - Tidy _headers (remove doubled Cache-Control)
#  One cache rule per file type (extension-based), fixes the
#  duplicated header, and restores immutable caching for the
#  self-hosted fonts (woff2/woff). Commits and pushes.
#  Run from repo root:
#      cd C:\Repos\Aetas-wealth-web ; .\deploy-wealth-headers-tidy.ps1
# ============================================================
$ErrorActionPreference = "Stop"
if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "aetas-wealth.com")) {
    Write-Error "Not the Aetas Wealth repo root. Aborting."; exit 1
}
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$headers = @'
# Cloudflare Pages _headers
# Security, performance, and agentic browsing headers
# Applied consistently across all pages.
#
# Note: X-Frame-Options omitted from global rule — it would block third-party
# iframe embeds (GoHighLevel forms, booking widgets). Framing protection is
# handled via CSP frame-ancestors in individual page <head> tags where needed.

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  X-XSS-Protection: 1; mode=block

/*.css
  Cache-Control: public, max-age=3600

/*.js
  Cache-Control: public, max-age=3600

/*.webp
  Cache-Control: public, max-age=31536000, immutable

/*.jpg
  Cache-Control: public, max-age=31536000, immutable

/*.jpeg
  Cache-Control: public, max-age=31536000, immutable

/*.png
  Cache-Control: public, max-age=31536000, immutable

/*.svg
  Cache-Control: public, max-age=31536000, immutable

/*.ico
  Cache-Control: public, max-age=31536000, immutable

/*.woff2
  Cache-Control: public, max-age=31536000, immutable

/*.woff
  Cache-Control: public, max-age=31536000, immutable

/sitemap.xml
  Cache-Control: public, max-age=3600

/robots.txt
  Cache-Control: public, max-age=3600

/llms.txt
  Cache-Control: public, max-age=3600
  Content-Type: text/plain; charset=utf-8

/llms-full.txt
  Cache-Control: public, max-age=3600
  Content-Type: text/plain; charset=utf-8

/*.pdf
  X-Robots-Tag: noindex, nofollow
'@

[System.IO.File]::WriteAllText([System.IO.Path]::GetFullPath('_headers'), $headers + "`n", $utf8NoBom)
Write-Host "Rewrote _headers (extension-based cache rules; fonts immutable)."

git add _headers
if ([string]::IsNullOrWhiteSpace((git status --porcelain))) { Write-Host "No changes to commit." }
else {
    git commit -m "cache: tidy _headers - one rule per file type (no doubled header); restore font caching"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
