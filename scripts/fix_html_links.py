"""
Bulk fix: Remove .html extensions from all internal navigation links across all HTML files.
This prevents 308 redirect chains that Google flags as low-quality signals.

Targets:
- href="about.html" → href="about"
- href="contact.html" → href="contact"
- href="privacy.html" → href="privacy"
- href="disclaimer.html" → href="disclaimer"
- href="tools.html" → href="tools"
- href="tools.html?tool=vram" → href="tools?tool=vram"
- href="compare.html" → href="compare"
- href="deals.html" → href="deals"
- canonical URLs: imtechboss.com/xxx.html → imtechboss.com/xxx
- og:url content: imtechboss.com/xxx.html → imtechboss.com/xxx

Does NOT touch:
- post.html?id=xxx links (handled by client-side JS, Cloudflare worker intercepts these)
- External links
- admin.html references
"""

import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pages to convert (not post.html, not admin.html, not index.html which is already /)
PAGES = ['about', 'contact', 'privacy', 'disclaimer', 'tools', 'compare', 'deals']

# All HTML files to process
html_files = glob.glob(os.path.join(ROOT, '*.html'))

total_replacements = 0

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    file_changes = 0
    
    for page in PAGES:
        # href="page.html" → href="page"
        old = f'href="{page}.html"'
        new = f'href="{page}"'
        count = content.count(old)
        if count:
            content = content.replace(old, new)
            file_changes += count
        
        # href="page.html? → href="page? (for query params like tools.html?tool=vram)
        old = f'href="{page}.html?'
        new = f'href="{page}?'
        count = content.count(old)
        if count:
            content = content.replace(old, new)
            file_changes += count
        
        # canonical and og:url: imtechboss.com/page.html" → imtechboss.com/page"
        old = f'https://imtechboss.com/{page}.html"'
        new = f'https://imtechboss.com/{page}"'
        count = content.count(old)
        if count:
            content = content.replace(old, new)
            file_changes += count
    
    # Also fix post.html in og:url/twitter:url meta tags (but NOT href="post.html?id=")
    # These are the default meta values in post.html that get SSR-overridden
    old_og = 'content="https://imtechboss.com/post.html"'
    new_og = 'content="https://imtechboss.com/post"'
    count = content.count(old_og)
    if count:
        content = content.replace(old_og, new_og)
        file_changes += count
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] {filename}: {file_changes} replacements")
        total_replacements += file_changes
    else:
        print(f"  [-] {filename}: no changes needed")

print(f"\n{'='*60}")
print(f"Total replacements across all files: {total_replacements}")
print(f"{'='*60}")
