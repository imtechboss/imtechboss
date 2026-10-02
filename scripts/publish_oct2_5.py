#!/usr/bin/env python3
"""
Publish 5 trending articles for October 2, 2026 to imtechboss.com.
Follows all rules in AGENTS.md / GEMINI.md strictly.
"""

import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = r"c:\Users\aabir\OneDrive\Desktop\website"
os.chdir(BASE_DIR)

BATCH_FILE = os.path.join(BASE_DIR, "scripts", "batch_oct2_5.json")

print("=" * 60)
print("PUBLISHING 5 ARTICLES — October 2, 2026")
print("=" * 60)

with open(BATCH_FILE, 'r', encoding='utf-8') as f:
    new_articles = json.load(f)

print(f"Loaded {len(new_articles)} articles.")

# 1. Update js/data.js
print("\n[Step 1] Updating js/data.js...")
with open('js/data.js', 'r', encoding='utf-8') as f:
    data_content = f.read()

m = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', data_content, re.DOTALL)
if not m:
    print("[FAIL] Could not find initialArticles in js/data.js")
    sys.exit(1)

existing_articles = json.loads(m.group(1))

# Check for duplicates
existing_ids = set(a['id'] for a in existing_articles)
for a in new_articles:
    if a['id'] in existing_ids:
        print(f"[FAIL] Duplicate article ID detected: {a['id']}")
        sys.exit(1)

# Prepend new articles
combined_articles = new_articles + existing_articles

new_json_str = json.dumps(combined_articles, indent=2, ensure_ascii=False)
new_data_content = f"var initialArticles = {new_json_str};\n"

with open('js/data.js', 'w', encoding='utf-8') as f:
    f.write(new_data_content)

print(f"  js/data.js updated: {len(combined_articles)} total articles.")

# 2. Update sitemap.xml
print("\n[Step 2] Updating sitemap.xml...")
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

sitemap_entries = []
for art in new_articles:
    img_url = art['image'].replace('&', '&amp;')
    title_esc = art['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    entry = f"""  <url>
    <loc>https://imtechboss.com/post?id={art['id']}</loc>
    <lastmod>2026-10-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
    <image:image>
      <image:loc>{img_url}</image:loc>
      <image:title>{title_esc}</image:title>
    </image:image>
  </url>"""
    sitemap_entries.append(entry)

sitemap_block = '\n'.join(sitemap_entries)
sitemap = sitemap.replace('>\n  <url>', '>\n' + sitemap_block + '\n  <url>', 1)

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

total_urls = len(re.findall(r'<loc>', sitemap))
print(f"  sitemap.xml updated: {total_urls} total URLs.")

# 3. Update feed.xml
print("\n[Step 3] Updating feed.xml...")
with open('feed.xml', 'r', encoding='utf-8') as f:
    feed = f.read()

feed_entries = []
for art in new_articles:
    img_url = art['image'].replace('&', '&amp;')
    title_esc = art['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    excerpt_esc = art['excerpt'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    cat_esc = art['category'].replace('&', '&amp;')
    link = f"https://imtechboss.com/post.html?id={art['id']}"
    entry = f"""    <item>
      <title>{title_esc}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>Thu, 02 Oct 2026 10:00:00 +0000</pubDate>
      <description>{excerpt_esc}</description>
      <category>{cat_esc}</category>
      <media:content url="{img_url}" medium="image" type="image/jpeg" width="1200" height="800" />
      <media:thumbnail url="{img_url}" width="1200" height="800" />
      <enclosure url="{img_url}" type="image/jpeg" length="0" />
    </item>"""
    feed_entries.append(entry)

feed_block = '\n'.join(feed_entries)
feed = feed.replace('\n    <item>', '\n' + feed_block + '\n    <item>', 1)

with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write(feed)

total_items = len(re.findall(r'<item>', feed))
print(f"  feed.xml updated: {total_items} total items.")

print("\n[Step 4] Running Master Pre-Flight Validator...")
import subprocess
result = subprocess.run([sys.executable, "scripts/validate_all.py"], cwd=BASE_DIR)
if result.returncode != 0:
    print("\n[BLOCKED] Master validation failed!")
    sys.exit(1)

print("\n" + "=" * 60)
print(f"All 5 articles successfully added and validated!")
print("=" * 60)
