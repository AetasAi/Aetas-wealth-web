# Fix broken Google Fonts async link tag across all HTML files
$root = "C:\Repos\Aetas-wealth-web"
$files = Get-ChildItem -Path $root -Filter "*.html" -Recurse

$broken    = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&display=swap" media="print" onload="this.media=''all''"> media="print" onload="this.media=''all''">'
$fixed     = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&display=swap" media="print" onload="this.media=''all''">'

$broken2   = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&display=swap" media="print" onload="this.media=''all''">></noscript>'
$fixed2    = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&display=swap" media="print" onload="this.media=''all''"></noscript>'

$count = 0
foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    if ($content -match [regex]::Escape('> media="print"')) {
        $content = $content.Replace($broken, $fixed).Replace($broken2, $fixed2)
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
        Write-Host "Fixed: $($file.Name)"
        $count++
    }
}
Write-Host "`nTotal files fixed: $count"
