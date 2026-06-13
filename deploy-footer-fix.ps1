# ---------------------------------------------------------------
# Aetas Wealth - Footer fix deployment
# Fixes Life Stage Planning under Services + h4 subheadings
# Run from repo root: cd C:\Repos\Aetas-Wealth-Website
#                     .\deploy-footer-fix.ps1
# ---------------------------------------------------------------

$repoRoot = "C:\Repos\Aetas-Wealth-Website"
$base = "https://raw.githubusercontent.com/AetasAi/Aetas-Wealth-Web/main"
$updated = 0

function Fix-Footer {
    param([string]$content, [string]$type)

    # Fix 1: Replace p-tag subheadings with h4 tags
    $content = [regex]::Replace($content,
        '<p style="margin: 1rem 0 0\.4rem 0; font-weight: 600; color: #fff;">(.*?)</p>',
        '<h4 style="margin-top:1.5rem;">$1</h4>')

    # Fix 2: Fix h3 column headers to h4 for consistency
    $content = $content.Replace('<h3>Useful</h3>', '<h4>Useful</h4>')
    $content = $content.Replace('<h3>Services</h3>', '<h4>Services</h4>')
    $content = $content.Replace('<h3>Site</h3>', '<h4>Site</h4>')
    $content = $content.Replace('<h3>Offices</h3>', '<h4>Offices</h4>')

    # Fix 3: Remove empty <ul> blocks left by previous scripts
    $content = $content.Replace("<ul>`n          </ul>`n        ", "")

    # Fix 4: Add Life Stage Planning under Services and clean Useful
    if ($type -eq "root") {
        $oldSvc = "          <li><a href=""services/protection-planning.html"">Protection Planning</a></li>`n        </ul>`n      </div>`n      <div>`n        <h4>Useful</h4>`n        <ul>"
        $newSvc = "          <li><a href=""services/protection-planning.html"">Protection Planning</a></li>`n        </ul>`n        <h4 style=""margin-top:1.5rem;"">Life Stage Planning</h4>`n        <ul>`n          <li><a href=""young-professionals/"">Young Professionals</a></li>`n          <li><a href=""millennials/"">Financial Planning in Your 30s &amp; 40s</a></li>`n        </ul>`n      </div>`n      <div>`n        <h4>Useful</h4>`n        <ul>"
        $content = $content.Replace($oldSvc, $newSvc)
        # Remove stray LSP items from Useful
        $content = $content.Replace("          <li><a href=""young-professionals/"">Young Professionals</a></li>`n", "")
        $content = $content.Replace("          <li><a href=""millennials/"">Financial Planning in Your 30s &amp; 40s</a></li>`n", "")
    }
    elseif ($type -eq "subdir") {
        $oldSvc = "          <li><a href=""../services/protection-planning.html"">Protection Planning</a></li>`n        </ul>`n      </div>`n      <div>`n        <h4>Useful</h4>`n        <ul>"
        $newSvc = "          <li><a href=""../services/protection-planning.html"">Protection Planning</a></li>`n        </ul>`n        <h4 style=""margin-top:1.5rem;"">Life Stage Planning</h4>`n        <ul>`n          <li><a href=""../young-professionals/"">Young Professionals</a></li>`n          <li><a href=""../millennials/"">Financial Planning in Your 30s &amp; 40s</a></li>`n        </ul>`n      </div>`n      <div>`n        <h4>Useful</h4>`n        <ul>"
        $content = $content.Replace($oldSvc, $newSvc)
        $content = $content.Replace("          <li><a href=""../young-professionals/"">Young Professionals</a></li>`n", "")
        $content = $content.Replace("          <li><a href=""../millennials/"">Financial Planning in Your 30s &amp; 40s</a></li>`n", "")
    }

    return $content
}

# Define files: [url-path, local-dest, type]
$files = @(
    @("index.html",                        "index.html",                          "root"),
    @("individuals.html",                  "individuals.html",                    "root"),
    @("businesses.html",                   "businesses.html",                     "root"),
    @("our-approach.html",                 "our-approach.html",                   "root"),
    @("our-people.html",                   "our-people.html",                     "root"),
    @("fees.html",                         "fees.html",                           "root"),
    @("contact.html",                      "contact.html",                        "root"),
    @("working-with-us.html",              "working-with-us.html",                "root"),
    @("professional-introducers.html",     "professional-introducers.html",       "root"),
    @("lifetime-to-legacy.html",           "lifetime-to-legacy.html",             "root"),
    @("guides/index.html",                 "guides\index.html",                   "subdir"),
    @("millennials/index.html",            "millennials\index.html",              "subdir"),
    @("young-professionals/index.html",    "young-professionals\index.html",      "subdir")
)

foreach ($f in $files) {
    $url     = "$base/$($f[0])"
    $dest    = Join-Path $repoRoot $f[1]
    $type    = $f[2]

    try {
        $content = (New-Object System.Net.WebClient).DownloadString($url)
        $fixed   = Fix-Footer -content $content -type $type
        [System.IO.File]::WriteAllText($dest, $fixed, (New-Object System.Text.UTF8Encoding $false))
        Write-Host "  Fixed: $($f[1])" -ForegroundColor Cyan
        $updated++
    } catch {
        Write-Host "  ERROR: $($f[1]) - $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "$updated files updated." -ForegroundColor Green
Write-Host ""
Write-Host "Now run:" -ForegroundColor Yellow
Write-Host "  git add -A" -ForegroundColor White
Write-Host "  git commit -m `"Fix footer - Life Stage Planning under Services, consistent h4 headings`"" -ForegroundColor White
Write-Host "  git push" -ForegroundColor White
