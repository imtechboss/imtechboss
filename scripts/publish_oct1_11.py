#!/usr/bin/env python3
"""
Publish 11 articles (Oct 1, 2026) to imtechboss.com
Batch 1: Gemini 4 Argon, Apple J490, Cisco SD-WAN Zero-Day, Microsoft Copilot Autopilot
Batch 2: Qualcomm TSMC 2nm, Claude Sonnet 5.5, Crew-13, AMD HBM4
Batch 3: Suncatcher Orbital, Ethereum Whale, Tesla Roadster
"""

import json
import re
import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r"c:\Users\aabir\OneDrive\Desktop\website")

SCRATCH = r"C:\Users\aabir\.gemini\antigravity\brain\4158c5a1-1ae8-497a-86bd-7a5db11f6d6d\scratch"

# ─── Load batch files ───
def load_batch(filename, varname):
    filepath = os.path.join(SCRATCH, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove var declaration and trailing semicolon to get pure JSON array
    content = content.strip()
    content = re.sub(r'^var\s+\w+\s*=\s*', '', content)
    content = re.sub(r';\s*$', '', content)
    # Fix escaped quotes in body HTML (\\\" -> \")
    # Parse as JSON
    try:
        articles = json.loads(content)
        return articles
    except json.JSONDecodeError as e:
        print(f"  JSON parse error in {filename}: {e}")
        # Try fixing common issues
        # Replace \\\" with \"
        content = content.replace('\\\\"', '\\"')
        try:
            articles = json.loads(content)
            return articles
        except json.JSONDecodeError as e2:
            print(f"  Still failing: {e2}")
            # Try eval as JavaScript
            print(f"  Attempting eval fallback...")
            return None

print("=" * 60)
print("PUBLISHING 11 ARTICLES - October 1, 2026")
print("=" * 60)

print("\n[1/6] Loading article batches...")
batch1 = load_batch('batch1_articles.js', 'batch1')
batch2 = load_batch('batch2_articles.js', 'batch2')
batch3 = load_batch('batch3_articles.js', 'batch3')

if not batch1 or not batch2 or not batch3:
    print("ERROR: Failed to load one or more batches!")
    sys.exit(1)

all_articles = batch1 + batch2 + batch3
print(f"  Loaded {len(all_articles)} articles total")
for i, a in enumerate(all_articles, 1):
    print(f"  {i}. {a['title'][:70]}...")

# ─── Fix: Remove duplicated body content in Gemini 4 article ───
for art in all_articles:
    body = art['body']
    # Check if body content is duplicated (same h2 appears twice)
    h2_matches = re.findall(r'<h2>([^<]+)</h2>', body)
    if len(h2_matches) > len(set(h2_matches)):
        print(f"  FIXING duplicated body in: {art['id']}")
        # Find the second occurrence of the first h2 and truncate
        first_h2 = h2_matches[0]
        first_pos = body.find(f'<h2>{first_h2}</h2>')
        second_pos = body.find(f'<h2>{first_h2}</h2>', first_pos + 1)
        if second_pos > 0:
            art['body'] = body[:second_pos].rstrip()

# ─── Step 2: Update data.js ───
print("\n[2/6] Updating js/data.js...")
with open('js/data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

# Build article entries for data.js
new_entries = []
for art in all_articles:
    # Escape body for JS string
    body = art['body'].replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
    entry = '''  {
    "id": "''' + art['id'] + '''",
    "title": "''' + art['title'].replace('"', '\\"') + '''",
    "excerpt": "''' + art['excerpt'].replace('"', '\\"') + '''",
    "category": "''' + art['category'] + '''",
    "date": "''' + art['date'] + '''",
    "author": "''' + art['author'] + '''",
    "readTime": "''' + art['readTime'] + '''",
    "image": "''' + art['image'] + '''",
    "body": "''' + body.replace('"', '\\"') + '''"
  }'''
    new_entries.append(entry)

insert_block = ',\n'.join(new_entries) + ','

# Insert after "var initialArticles = ["
data_js = data_js.replace(
    'var initialArticles = [\n',
    'var initialArticles = [\n' + insert_block + '\n',
    1
)

with open('js/data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)

# Count total articles
total_articles = len(re.findall(r'"id":\s*"', data_js))
print(f"  data.js updated: {total_articles} total articles")

# ─── Step 3: Update sitemap.xml ───
print("\n[3/6] Updating sitemap.xml...")
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

sitemap_entries = []
for art in all_articles:
    img_url = art['image'].replace('&', '&amp;')
    title_escaped = art['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    entry = f"""  <url>
    <loc>https://imtechboss.com/post?id={art['id']}</loc>
    <lastmod>2026-10-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
    <image:image>
      <image:loc>{img_url}</image:loc>
      <image:title>{title_escaped}</image:title>
    </image:image>
  </url>"""
    sitemap_entries.append(entry)

sitemap_block = '\n'.join(sitemap_entries)

# Insert after first <urlset...> line
sitemap = sitemap.replace(
    '>\n  <url>',
    '>\n' + sitemap_block + '\n  <url>',
    1
)

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

total_urls = len(re.findall(r'<loc>', sitemap))
print(f"  sitemap.xml updated: {total_urls} total URLs")

# ─── Step 4: Update feed.xml ───
print("\n[4/6] Updating feed.xml...")
with open('feed.xml', 'r', encoding='utf-8') as f:
    feed = f.read()

feed_entries = []
for art in all_articles:
    img_url = art['image'].replace('&', '&amp;')
    title_escaped = art['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    excerpt_escaped = art['excerpt'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    category_escaped = art['category'].replace('&', '&amp;')
    link = f"https://imtechboss.com/post.html?id={art['id']}"

    entry = f"""    <item>
      <title>{title_escaped}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>Wed, 01 Oct 2026 12:00:00 +0000</pubDate>
      <description>{excerpt_escaped}</description>
      <category>{category_escaped}</category>
      <media:content url="{img_url}" medium="image" type="image/jpeg" width="1200" height="800" />
      <media:thumbnail url="{img_url}" width="1200" height="800" />
      <enclosure url="{img_url}" type="image/jpeg" length="0" />
    </item>"""
    feed_entries.append(entry)

feed_block = '\n'.join(feed_entries)

# Insert after <language>en</language> ... before first <item>
feed = feed.replace(
    '\n    <item>',
    '\n' + feed_block + '\n    <item>',
    1
)

with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write(feed)

total_items = len(re.findall(r'<item>', feed))
print(f"  feed.xml updated: {total_items} total items")

# ─── Step 5: Validate XML ───
print("\n[5/6] Validating XML files...")
import xml.etree.ElementTree as ET

errors = 0
for fname in ['sitemap.xml', 'feed.xml']:
    try:
        tree = ET.parse(fname)
        count_tag = 'loc' if fname == 'sitemap.xml' else 'item'
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'} if fname == 'sitemap.xml' else {}
        if fname == 'sitemap.xml':
            entries = tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        else:
            entries = tree.findall('.//item')
        print(f"  [PASS] {fname} is valid XML ({len(entries)} entries)")
    except ET.ParseError as e:
        print(f"  [FAIL] {fname}: {e}")
        errors += 1

if errors > 0:
    print(f"\n  ERROR: {errors} XML file(s) have errors! Aborting.")
    sys.exit(1)

# ─── Step 6: Summary ───
print("\n[6/6] Summary")
print("=" * 60)
print(f"  Articles added:      {len(all_articles)}")
print(f"  Total in data.js:    {total_articles}")
print(f"  Total sitemap URLs:  {total_urls}")
print(f"  Total feed items:    {total_items}")
print(f"  XML validation:      PASSED")
print("=" * 60)
print("\nSUCCESS! All 11 articles published to codebase.")
print("Next: Run generate_worker.py, ping_indexnow.js, then deploy.")
