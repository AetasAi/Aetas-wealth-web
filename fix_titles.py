import os, re

root = r"C:\Repos\Aetas-wealth-web"
skip = {"uk-property-wealth-inheritance-tax.html"}
pattern = re.compile(r'((?:og:title|twitter:title)[^>]*content=")([^"]*£)([^"]*")')

fixed = []
for dirpath, _, files in os.walk(root):
    for f in files:
        if not f.endswith(".html") or f in skip:
            continue
        path = os.path.join(dirpath, f)
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        # Only replace £ used as separator (surrounded by spaces), not genuine currency
        new = re.sub(r'(content="[^"]*?) £ (Aetas Wealth[^"]*")', r'\1 · \2', content)
        if new != content:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
            fixed.append(path.replace(root + "\\", ""))

print(f"Fixed {len(fixed)} files:")
for f in fixed:
    print(f" {f}")
