#!/usr/bin/env python3
"""Publish 3 additional articles (Oct 1 evening) to imtechboss.com"""
import json, re, os, sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r"c:\Users\aabir\OneDrive\Desktop\website")

BATCH_FILE = r"C:\Users\aabir\.gemini\antigravity\brain\605773db-b03a-47ea-a8f2-becbf23b5384\scratch\batch4_articles.js"

print("=" * 60)
print("PUBLISHING 3 ARTICLES - October 1, 2026 (Evening)")
print("=" * 60)

# Load batch
print("\n[1/5] Loading articles...")
with open(BATCH_FILE, 'r', encoding='utf-8') as f:
    content = f.read().strip()
content = re.sub(r'^var\s+\w+\s*=\s*', '', content)
content = re.sub(r';\s*$', '', content)
articles = json.loads(content)
print(f"  Loaded {len(articles)} articles")
for i, a in enumerate(articles, 1):
    print(f"  {i}. {a['title'][:70]}...")

# Fix duplicated body content
for art in articles:
    body = art['body']
    h2s = re.findall(r'<h2>([^<]+)</h2>', body)
    if len(h2s) > len(set(h2s)):
        print(f"  FIXING duplicated body in: {art['id']}")
        first_h2 = h2s[0]
        first_pos = body.find(f'<h2>{first_h2}</h2>')
        second_pos = body.find(f'<h2>{first_h2}</h2>', first_pos + 1)
        if second_pos > 0:
            art['body'] = body[:second_pos].rstrip()

# Update data.js
print("\n[2/5] Updating js/data.js...")
with open('js/data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

new_entries = []
for art in articles:
    body = art['body'].replace("'", "\\'").replace('\n', '\\n')
    entry = '  {\n'
    entry += f'    "id": "{art["id"]}",\n'
    entry += f'    "title": "{art["title"].replace(chr(34), chr(92)+chr(34))}",\n'
    entry += f'    "excerpt": "{art["excerpt"].replace(chr(34), chr(92)+chr(34))}",\n'
    entry += f'    "category": "{art["category"]}",\n'
    entry += f'    "date": "{art["date"]}",\n'
    entry += f'    "author": "{art["author"]}",\n'
    entry += f'    "readTime": "{art["readTime"]}",\n'
    entry += f'    "image": "{art["image"]}",\n'
    entry += f'    "body": {json.dumps(art["body"])}\n'
    entry += '  }'
    new_entries.append(entry)

insert_block = ',\n'.join(new_entries) + ','
data_js = data_js.replace('var initialArticles = [\n', 'var initialArticles = [\n' + insert_block + '\n', 1)

# Fix \' -> ' for JSON compatibility
data_js = data_js.replace("\\'", "'")

with open('js/data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)
total_articles = len(re.findall(r'"id":\s*"', data_js))
print(f"  data.js updated: {total_articles} total articles")

# Update sitemap.xml
print("\n[3/5] Updating sitemap.xml...")
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap = f.read()

sitemap_entries = []
for art in articles:
    img_url = art['image'].replace('&', '&amp;')
    title_esc = art['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    entry = f"""  <url>
    <loc>https://imtechboss.com/post?id={art['id']}</loc>
    <lastmod>2026-10-01</lastmod>
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
print(f"  sitemap.xml updated: {total_urls} total URLs")

# Update feed.xml
print("\n[4/5] Updating feed.xml...")
with open('feed.xml', 'r', encoding='utf-8') as f:
    feed = f.read()

feed_entries = []
for art in articles:
    img_url = art['image'].replace('&', '&amp;')
    title_esc = art['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    excerpt_esc = art['excerpt'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    cat_esc = art['category'].replace('&', '&amp;')
    link = f"https://imtechboss.com/post.html?id={art['id']}"
    entry = f"""    <item>
      <title>{title_esc}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>Wed, 01 Oct 2026 18:00:00 +0000</pubDate>
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
print(f"  feed.xml updated: {total_items} total items")

# Validate XML
print("\n[5/5] Validating XML files...")
errors = 0
for fname in ['sitemap.xml', 'feed.xml']:
    try:
        tree = ET.parse(fname)
        if fname == 'sitemap.xml':
            entries = tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        else:
            entries = tree.findall('.//item')
        print(f"  [PASS] {fname} is valid XML ({len(entries)} entries)")
    except ET.ParseError as e:
        print(f"  [FAIL] {fname}: {e}")
        errors += 1

if errors > 0:
    print(f"\n  ERROR: {errors} XML file(s) have errors!")
    sys.exit(1)

print("\n" + "=" * 60)
print(f"  Articles added:      {len(articles)}")
print(f"  Total in data.js:    {total_articles}")
print(f"  Total sitemap URLs:  {total_urls}")
print(f"  Total feed items:    {total_items}")
print("=" * 60)
print("SUCCESS! Run generate_worker.py, ping_indexnow.js, then deploy.")
