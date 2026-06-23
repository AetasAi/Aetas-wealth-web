import os

root = r"C:\Repos\Aetas-wealth-web"

# Fix 1: Reduce font weights from 5 to 3 (drop 500 and 700)
old_fonts = 'family=Open+Sans:wght@300;400;500;600;700&display=swap'
new_fonts = 'family=Open+Sans:wght@300;400;600&display=swap'

# Fix 2: Add preconnect for backend.leadconnectorhq.com
# Insert after the existing preload line
old_preload = '<link rel="preload" href="https://fonts.gstatic.com/s/opensans/v40/memSYaGs126MiZpBA-UvWbX2vVnXBbObj2OVZyOOSr4dVJWUgsjZ0C11.woff2" as="font" type="font/woff2" crossorigin>'
new_preload = '<link rel="preload" href="https://fonts.gstatic.com/s/opensans/v40/memSYaGs126MiZpBA-UvWbX2vVnXBbObj2OVZyOOSr4dVJWUgsjZ0C11.woff2" as="font" type="font/woff2" crossorigin>\n  <link rel="preconnect" href="https://backend.leadconnectorhq.com" crossorigin>'

count = 0
for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        content_lf = content.replace('\r\n', '\n')
        changed = False
        if old_fonts in content_lf:
            content_lf = content_lf.replace(old_fonts, new_fonts)
            changed = True
        if old_preload in content_lf and 'leadconnectorhq.com" crossorigin>' not in content_lf:
            content_lf = content_lf.replace(old_preload, new_preload)
            changed = True
        if changed:
            with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content_lf)
            print(f"Fixed: {fname}")
            count += 1

print(f"\nTotal: {count} files updated")
