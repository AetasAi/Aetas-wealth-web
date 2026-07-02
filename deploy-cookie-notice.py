#!/usr/bin/env python3
"""
deploy-cookie-notice.py
=======================
Adds the Aetas Wealth cookie consent notice to every HTML file
in C:\\Repos\\Aetas-wealth-web.

Run from the repo root:
    py deploy-cookie-notice.py

Or with an explicit path:
    py deploy-cookie-notice.py C:\\Repos\\Aetas-wealth-web

What it does
------------
1. Walks every .html file in the repo (excluding node_modules, .git).
2. Skips any file that already contains id="cookie-notice".
3. Inserts the cookie notice block immediately before </body>.
4. Writes the file back with UTF-8 encoding, no BOM.

The cookie notice block is defined inline below — edit it here if you
ever need to update the wording or styling.
"""

from __future__ import annotations
import sys
import os
from pathlib import Path

# ── Cookie notice block ────────────────────────────────────────────────────
COOKIE_NOTICE = '''\n<!-- Cookie notice -->
<div id="cookie-notice" role="dialog" aria-label="Cookie notice" style="display:none;position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#00205B;color:#fff;padding:1rem 1.5rem;font-size:0.85rem;line-height:1.6;box-shadow:0 -2px 12px rgba(0,0,0,0.2);">
  <div style="max-width:900px;margin:0 auto;display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;">
    <p style="margin:0;flex:1;min-width:200px;">This site uses Google Analytics and Microsoft Clarity to understand how it is used, with IP addresses anonymised. No personal data is collected through analytics. <a href="/privacy.html" style="color:#00c4c4;text-decoration:underline;">Privacy Policy</a></p>
    <div style="display:flex;gap:0.75rem;flex-shrink:0;">
      <button id="cookie-accept" style="background:#009CA6;color:#fff;border:none;padding:0.5rem 1.25rem;border-radius:2px;cursor:pointer;font-size:0.85rem;font-weight:600;">Accept</button>
      <button id="cookie-decline" style="background:transparent;color:rgba(255,255,255,0.7);border:1px solid rgba(255,255,255,0.3);padding:0.5rem 1.25rem;border-radius:2px;cursor:pointer;font-size:0.85rem;">Decline</button>
    </div>
  </div>
</div>
<script>
(function(){
  var notice = document.getElementById(\'cookie-notice\');
  if (!notice) return;
  var consent = localStorage.getItem(\'aetas-cookie-consent\');
  if (!consent) {
    notice.style.display = \'block\';
  }
  document.getElementById(\'cookie-accept\').addEventListener(\'click\', function(){
    localStorage.setItem(\'aetas-cookie-consent\', \'accepted\');
    notice.style.display = \'none\';
    // Fire analytics immediately on accept (don\'t wait for next interaction)
    if (window.gtag) return;
    var GA4_ID = \'G-MXS6JSC1LE\';
    var CLARITY_ID = \'wtmefby0kh\';
    var s = document.createElement(\'script\');
    s.async = true;
    s.src = \'https://www.googletagmanager.com/gtag/js?id=\' + GA4_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag(){ window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag(\'js\', new Date());
    gtag(\'config\', GA4_ID, { anonymize_ip: true });
    (function(c,l,a,r,i,t,y){
      c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
      t=l.createElement(r);t.async=1;t.src=\'https://www.clarity.ms/tag/\'+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window,document,\'clarity\',\'script\',CLARITY_ID);
  });
  document.getElementById(\'cookie-decline\').addEventListener(\'click\', function(){
    localStorage.setItem(\'aetas-cookie-consent\', \'declined\');
    notice.style.display = \'none\';
  });
})();
</script>
<!-- /Cookie notice -->
'''

TARGET = '</body>'

EXCLUDE_DIRS = {'.git', 'node_modules', '.github', 'scripts', 'docs'}

def process(repo: Path) -> None:
    updated = 0
    skipped_present = 0
    skipped_no_body = 0

    for html in sorted(repo.rglob('*.html')):
        # Skip excluded directories
        if any(part in EXCLUDE_DIRS for part in html.parts):
            continue

        content = html.read_text(encoding='utf-8', errors='replace')

        # Already has cookie notice — skip
        if 'id="cookie-notice"' in content:
            skipped_present += 1
            continue

        # No </body> tag — skip (shouldn't happen but be safe)
        if TARGET not in content:
            skipped_no_body += 1
            print(f'  SKIP (no </body>): {html.relative_to(repo)}')
            continue

        # Insert notice before the LAST </body> in the file
        idx = content.rfind(TARGET)
        new_content = content[:idx] + COOKIE_NOTICE + content[idx:]

        html.write_text(new_content, encoding='utf-8')
        print(f'  UPDATED: {html.relative_to(repo)}')
        updated += 1

    print(f'\nDone. Updated: {updated}  Already present: {skipped_present}  Skipped (no </body>): {skipped_no_body}')

if __name__ == '__main__':
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    if not repo.is_dir():
        print(f'ERROR: {repo} is not a directory')
        sys.exit(1)
    print(f'Repo: {repo.resolve()}\n')
    process(repo)
