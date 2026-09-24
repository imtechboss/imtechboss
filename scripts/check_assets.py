import os, re

files = ['index.html', 'post.html', 'about.html', 'privacy.html', 'contact.html', 'disclaimer.html', '404.html', 'admin.html']
missing_count = 0
for html_file in files:
    if not os.path.exists(html_file):
        continue
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # find all src and href
    matches = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', content)
    for asset in matches:
        if asset.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'javascript:', 'data:')):
            continue
        clean = asset.split('?')[0].split('#')[0]
        if not clean:
            continue
        if clean.startswith('/'):
            clean = clean[1:]
        clean = os.path.normpath(clean)
        if not os.path.exists(clean):
            print(f"[MISSING ASSET] in {html_file}: {asset} -> resolved to {clean}")
            missing_count += 1

print(f"Total missing assets found: {missing_count}")
