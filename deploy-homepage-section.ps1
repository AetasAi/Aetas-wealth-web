<#
  deploy-homepage-section.ps1
  Homepage: rebalance hero + replace 'Why Aetas' with 'What Makes Aetas Different'.

  1. Removes the four client-outcome ticks from the hero's left column.
  2. Adds them back as a full-width proof band beneath the hero (4-up desktop,
     2x2 tablet, stacked mobile).
  3. Replaces the thin 'Why Aetas was created' section with a formatted
     'What Makes Aetas Different' section.
  Idempotent. Homepage only. RUN FROM REPO ROOT:  git pull ; .\deploy-homepage-section.ps1
#>

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$utf8 = New-Object System.Text.UTF8Encoding($false)
$path = Join-Path $PSScriptRoot 'index.html'
$c = [System.IO.File]::ReadAllText($path)

# match whatever newline the working copy uses (LF or CRLF)
$nl = if ($c.Contains("`r`n")) { "`r`n" } else { "`n" }
function ToNl($s) { return $s.Replace("`r`n","`n").Replace("`n",$nl) }

$checklistRaw = @'
        <div style="margin-top:1.5rem;display:flex;flex-wrap:wrap;gap:0.6rem 1.25rem;">
          <span style="font-size:0.88rem;color:var(--ink-soft);display:flex;align-items:center;gap:0.4rem;"><span style="color:var(--aetas-turquoise);font-weight:700;">✓</span> Clients who retired earlier than they thought possible</span>
          <span style="font-size:0.88rem;color:var(--ink-soft);display:flex;align-items:center;gap:0.4rem;"><span style="color:var(--aetas-turquoise);font-weight:700;">✓</span> Families who significantly reduced their inheritance tax</span>
          <span style="font-size:0.88rem;color:var(--ink-soft);display:flex;align-items:center;gap:0.4rem;"><span style="color:var(--aetas-turquoise);font-weight:700;">✓</span> Business owners who structured exits with confidence</span>
          <span style="font-size:0.88rem;color:var(--ink-soft);display:flex;align-items:center;gap:0.4rem;"><span style="color:var(--aetas-turquoise);font-weight:700;">✓</span> People who simply feel more in control of their financial future</span>
        </div>
'@
$whyaetasRaw = @'
<section class="section-tight section-soft">
  <div class="container-narrow">
    <div style="max-width:680px;margin:0 auto;">
      <span class="eyebrow">Why Aetas was created</span>
      <p style="font-size:1.25rem;line-height:1.7;color:var(--ink-soft);margin:1.25rem 0 0.75rem;font-weight:300;">Financial planning has become increasingly product-led.</p>
      <p style="font-size:1.25rem;line-height:1.7;color:var(--ink);margin:0 0 1.5rem;font-weight:300;">We believe clients deserve something different.</p>
      <div style="display:flex;flex-direction:column;gap:0.5rem;margin:0 0 2rem;padding-left:1.5rem;border-left:2px solid var(--aetas-gold);">
        <p style="margin:0;font-size:1.1rem;font-weight:600;color:var(--aetas-blue);">Clear advice.</p>
        <p style="margin:0;font-size:1.1rem;font-weight:600;color:var(--aetas-blue);">Long-term relationships.</p>
        <p style="margin:0;font-size:1.1rem;font-weight:600;color:var(--aetas-blue);">Planning that evolves with life.</p>
      </div>
      <p style="font-size:1.1rem;line-height:1.7;color:var(--ink-soft);margin:0 0 2rem;">That's why Aetas was created.</p>
      <p style="font-size:1rem;line-height:1.75;color:var(--ink-soft);margin:0;">Most people don't come to us because they enjoy financial planning. They come because they're approaching retirement, selling a business, receiving an inheritance, or simply wondering whether they're making the right decisions. That's exactly where we start.</p>
    </div>
  </div>
</section>
'@
$replacementRaw = @'
<!-- Client outcomes proof bar (moved out of hero for balance) -->
<style>.hero-proof{display:grid;grid-template-columns:repeat(4,1fr);gap:1.1rem 2rem;}.hero-proof>div{display:flex;align-items:flex-start;gap:0.55rem;font-size:0.92rem;color:var(--ink-soft);line-height:1.5;}.hero-proof .pt{color:var(--aetas-turquoise);font-weight:700;flex-shrink:0;}@media(max-width:1000px){.hero-proof{grid-template-columns:1fr 1fr;gap:1rem 2rem;}}@media(max-width:560px){.hero-proof{grid-template-columns:1fr;}}</style>
<section style="background:#fff;border-top:1px solid var(--line);">
  <div class="container" style="padding-block:1.75rem;">
    <div class="hero-proof">
      <div><span class="pt">&#10003;</span> Clients who retired earlier than they thought possible</div>
      <div><span class="pt">&#10003;</span> Families who significantly reduced their inheritance tax</div>
      <div><span class="pt">&#10003;</span> Business owners who structured exits with confidence</div>
      <div><span class="pt">&#10003;</span> People who simply feel more in control of their financial future</div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container-narrow">
    <div style="max-width:720px;margin:0 auto;">
      <span class="eyebrow">What makes Aetas different</span>
      <h2 style="font-weight:400;margin:1rem 0 1.5rem;">Advice built around <em style="font-style:normal;font-weight:700;">you</em>, not products</h2>
      <p style="font-size:1.05rem;line-height:1.75;color:var(--ink-soft);margin:0 0 1.25rem;">Your finances are personal. Behind every financial decision is your family, your ambitions, your business, your priorities and the future you are working hard to create.</p>
      <p style="font-size:1.05rem;line-height:1.75;color:var(--ink-soft);margin:0 0 1.25rem;">That is why we start by understanding you &mdash; what matters most and what you want to achieve &mdash; before we ever consider solutions.</p>
      <p style="font-size:1.05rem;line-height:1.75;color:var(--ink-soft);margin:0 0 1.25rem;">We take the time to listen, explain complex financial matters in plain English and help you make confident decisions without pressure, unnecessary jargon or advice that is not relevant to you.</p>
      <p style="font-size:1.05rem;line-height:1.75;color:var(--ink-soft);margin:0 0 1.25rem;">Whether you are taking your first financial steps, planning for retirement, building your wealth, growing your business, protecting your family or passing on your legacy, we work alongside you as a long-term partner, adapting your financial plan as your life changes.</p>
      <p style="font-size:1.05rem;line-height:1.75;color:var(--ink-soft);margin:0 0 1.75rem;">Technology helps us deliver an efficient service, but it will never replace personal relationships. You will always have access to experienced advisers who take the time to understand your circumstances and provide advice based on your goals.</p>
      <p style="font-size:1.2rem;line-height:1.6;color:var(--aetas-blue);font-weight:300;margin:0 0 1.75rem;padding-left:1.5rem;border-left:2px solid var(--aetas-gold);">Because when your adviser understands your life, they can help you make better financial decisions.</p>
      <p style="font-size:1.1rem;font-weight:700;color:var(--aetas-blue);margin:0;">Helping you build, protect and transfer wealth with confidence.</p>
    </div>
  </div>
</section>
'@

$checklist   = ToNl($checklistRaw)
$whyaetas    = ToNl($whyaetasRaw)
$replacement = ToNl($replacementRaw)

$changed = $false
if ($c.Contains($checklist)) { $c = $c.Replace($checklist + $nl, ''); $changed = $true; Write-Host '  [hero] removed inline ticks' -ForegroundColor Green }
else { Write-Host '  [hero] ticks already moved - skipped' -ForegroundColor DarkGray }
if ($c.Contains($whyaetas)) { $c = $c.Replace($whyaetas, $replacement); $changed = $true; Write-Host '  [sec]  proof band + What Makes Aetas Different added' -ForegroundColor Green }
else { Write-Host '  [sec]  section already replaced - skipped' -ForegroundColor DarkGray }
$c = $c.Replace('     WHY AETAS', '     WHAT MAKES AETAS DIFFERENT')

if ($changed) {
  [System.IO.File]::WriteAllText($path, $c, $utf8)
  Write-Host '  [write] index.html updated' -ForegroundColor Green
} else { Write-Host '  nothing to do' -ForegroundColor DarkGray }

Write-Host '== git ==' -ForegroundColor Cyan
git add -A
git commit -m "Homepage: rebalance hero (full-width proof band) and replace Why-Aetas with What-Makes-Aetas-Different"
git push
Write-Host '== done ==' -ForegroundColor Cyan
