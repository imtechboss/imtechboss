import os
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for fname in ['post.html', 'index.html', 'tools.html']:
    fpath = os.path.join(base_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match the facebook anchor
    # Remove header facebook icon
    content = re.sub(
        r'<a\s+href="https://facebook\.com"[^>]*title="Facebook"[^>]*>[\s\S]*?</a>\s*',
        '',
        content
    )
    # Remove footer facebook link if present
    content = re.sub(
        r'<li><a\s+href="https://facebook\.com"[^>]*>[\s\S]*?Facebook\s+Page</a></li>\s*',
        '',
        content
    )
    # Remove any other generic facebook.com links
    content = re.sub(
        r'<a\s+href="https://facebook\.com"[^>]*>[\s\S]*?</a>\s*',
        '',
        content
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Cleaned placeholder Facebook links from {fname}")
