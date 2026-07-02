#!/usr/bin/env python3
"""
deploy-cookie-script-workplace.py
==================================
Updates the cookie notice <script> block in every HTML file in
C:\\Repos\\AetasInTheWorkplace to the GDPR-compliant version.

The old script stored consent but did not gate analytics.
The new script adds an immediate analytics fire on accept.

Run from the repo root:
    py deploy-cookie-script-workplace.py

Or with an explicit path:
    py deploy-cookie-script-workplace.py C:\\Repos\\AetasInTheWorkplace
"""

from __future__ import annotations
import sys
from pathlib import Path

OLD_SCRIPT = '''<script>
(function(){
  var notice = document.getElementById('cookie-notice');
  if (!notice) return;
  var consent = localStorage.getItem('aetas-cookie-consent');
  if (!consent) {
    notice.style.display = 'block';
  }
  document.getElementById('cookie-accept').addEventListener('click', function(){
    localStorage.setItem('aetas-cookie-consent', 'accepted');
    notice.style.display = 'none';
  });
  document.getElementById('cookie-decline').addEventListener('click', function(){
    localStorage.setItem('aetas-cookie-consent', 'declined');
    notice.style.display = 'none';
    // Note: GA4 already defers until interaction — declining just prevents future prompts
  });
})();
</script>'''

NEW_SCRIPT = '''<script>
(function(){
  var notice = document.getElementById('cookie-notice');
  if (!notice) return;
  var consent = localStorage.getItem('aetas-cookie-consent');
  if (!consent) {
    notice.style.display = 'block';
  }
  document.getElementById('cookie-accept').addEventListener('click', function(){
    localStorage.setItem('aetas-cookie-consent', 'accepted');
    notice.style.display = 'none';
    // Fire analytics immediately on accept (don't wait for next interaction)
    if (window.gtag) return;
    var GA4_ID = 'G-HNH05BKNFX';
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag(){ window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA4_ID, { anonymize_ip: true });
  });
  document.getElementById('cookie-decline').addEventListener('click', function(){
    localStorage.setItem('aetas-cookie-consent', 'declined');
    notice.style.display = 'none';
  });
})();
</script>'''

EXCLUDE_DIRS = {'.git', 'node_modules', '.github', 'scripts'}

def process(repo: Path) -> None:
    updated = 0
    skipped = 0

    for html in sorted(repo.rglob('*.html')):
        if any(part in EXCLUDE_DIRS for part in html.parts):
            continue

        content = html.read_text(encoding='utf-8', errors='replace')

        if OLD_SCRIPT not in content:
            skipped += 1
            continue

        new_content = content.replace(OLD_SCRIPT, NEW_SCRIPT, 1)
        html.write_text(new_content, encoding='utf-8')
        print(f'  UPDATED: {html.relative_to(repo)}')
        updated += 1

    print(f'\nDone. Updated: {updated}  Skipped (old script not found): {skipped}')

if __name__ == '__main__':
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    if not repo.is_dir():
        print(f'ERROR: {repo} is not a directory')
        sys.exit(1)
    print(f'Repo: {repo.resolve()}\n')
    process(repo)
