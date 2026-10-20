import os
import re
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, 'js', 'data.js')

with open(data_path, 'r', encoding='utf-8') as f:
    content = f.read()

match_array = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', content, re.DOTALL)
articles = json.loads(match_array.group(1))

found_links = []
for a in articles:
    body = a.get('content') or a.get('body') or ''
    # Look for any post?id or post.html?id links
    links = re.findall(r'href=["\'](?:(?:\.?\/)?post(?:\.html)?\?id=)([^"\'&]+)', body, re.IGNORECASE)
    if links:
        found_links.extend(links)
        print(f"Article '{a['id']}' has {len(links)} links: {links}")

print(f"\nTotal in-article post?id links found: {len(found_links)}")
