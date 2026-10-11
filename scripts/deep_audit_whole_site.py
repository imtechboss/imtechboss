import os, sys, json, re, glob
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(ROOT, 'js', 'data.js')
SITEMAP_XML = os.path.join(ROOT, 'sitemap.xml')
FEED_XML = os.path.join(ROOT, 'feed.xml')
ROBOTS_TXT = os.path.join(ROOT, 'robots.txt')
ADS_TXT = os.path.join(ROOT, 'ads.txt')
WORKER_JS = os.path.join(ROOT, '_worker.js')
HEADERS_FILE = os.path.join(ROOT, '_headers')

BANNED_WORDS = [
    'delve', 'landscape', 'pivotal', 'testament', 'game-changer',
    'in conclusion', 'tapestries', 'realm', 'beacon', 'seamlessly'
]

report = {
    "articles": {
        "total": 0,
        "under_600_words": [],
        "missing_fields": [],
        "banned_words_found": [],
        "invalid_images": [],
        "malformed_html": [],
        "duplicate_titles": [],
        "categories": {},
        "dates_summary": {}
    },
    "static_pages": {},
    "xml_files": {},
    "config_files": {},
    "edge_worker": {},
    "summary": {
        "total_passed_checks": 0,
        "total_issues_found": 0
    }
}

print("=" * 70)
print("STARTING FULL-SPECTRUM AUDIT OF IMTECHBOSS.COM CODEBASE")
print("=" * 70)

# 1. AUDIT JS/DATA.JS (ALL ARTICLES)
print("\n[1/6] Auditing all articles in js/data.js...")
with open(DATA_JS, 'r', encoding='utf-8') as f:
    data_content = f.read()

match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', data_content, re.DOTALL)
if not match:
    print("[CRITICAL ERROR] Could not parse initialArticles from js/data.js!")
    sys.exit(1)

articles = json.loads(match.group(1))
report["articles"]["total"] = len(articles)
seen_titles = {}

for idx, a in enumerate(articles):
    aid = a.get('id', f'idx_{idx}')
    title = a.get('title', '')
    excerpt = a.get('excerpt', '')
    content = a.get('content', '')
    image = a.get('image', '')
    cat = a.get('category', 'Uncategorized')
    date = a.get('date', '')
    author = a.get('author', '')

    # Category count
    report["articles"]["categories"][cat] = report["articles"]["categories"].get(cat, 0) + 1

    # Missing fields
    missing = []
    if not title: missing.append("title")
    if not excerpt: missing.append("excerpt")
    if not content: missing.append("content")
    if not image: missing.append("image")
    if not date: missing.append("date")
    if missing:
        report["articles"]["missing_fields"].append({"id": aid, "missing": missing})
        report["summary"]["total_issues_found"] += 1
    else:
        report["summary"]["total_passed_checks"] += 1

    # Duplicate titles
    if title in seen_titles:
        report["articles"]["duplicate_titles"].append({"title": title, "id1": seen_titles[title], "id2": aid})
        report["summary"]["total_issues_found"] += 1
    else:
        seen_titles[title] = aid
        report["summary"]["total_passed_checks"] += 1

    # Word count check (< 600 words)
    text = re.sub(r'<[^>]+>', ' ', content or '')
    words = len(text.split())
    if words < 600:
        report["articles"]["under_600_words"].append({"id": aid, "words": words, "title": title})
        report["summary"]["total_issues_found"] += 1
    else:
        report["summary"]["total_passed_checks"] += 1

    # Banned words (exact whole words only)
    content_lower = content.lower()
    for bw in BANNED_WORDS:
        if re.search(r'\b' + re.escape(bw) + r'\b', content, re.IGNORECASE):
            report["articles"]["banned_words_found"].append({"id": aid, "banned_word": bw})
            report["summary"]["total_issues_found"] += 1

    # Image standard (must be http/https, ideally 1200px crop)
    if not (image.startswith('http://') or image.startswith('https://') or image.startswith('/')):
        report["articles"]["invalid_images"].append({"id": aid, "image": image, "reason": "invalid URL protocol"})
        report["summary"]["total_issues_found"] += 1
    else:
        report["summary"]["total_passed_checks"] += 1

    # Malformed HTML basic check (tag nesting)
    open_tags = re.findall(r'<([a-zA-Z0-9]+)[^>]*>', content)
    close_tags = re.findall(r'</([a-zA-Z0-9]+)>', content)
    # Exclude void elements like img, br, hr, input
    voids = {'img', 'br', 'hr', 'input', 'meta', 'link'}
    filtered_open = [t.lower() for t in open_tags if t.lower() not in voids]
    if abs(len(filtered_open) - len(close_tags)) > 5:
        report["articles"]["malformed_html"].append({
            "id": aid,
            "open_count": len(filtered_open),
            "close_count": len(close_tags),
            "diff": len(filtered_open) - len(close_tags)
        })

print(f"  Audited {len(articles)} articles. Passed basic checks.")

# 2. AUDIT STATIC PAGES
print("\n[2/6] Auditing all static HTML pages...")
static_files = glob.glob(os.path.join(ROOT, '*.html'))
for sf in static_files:
    filename = os.path.basename(sf)
    with open(sf, 'r', encoding='utf-8') as f:
        html = f.read()

    page_data = {
        "size_bytes": len(html),
        "lines": len(html.splitlines()),
        "has_canonical": '<link rel="canonical"' in html,
        "has_og_title": 'property="og:title"' in html or 'name="og:title"' in html,
        "has_og_image": 'property="og:image"' in html or 'name="og:image"' in html,
        "has_adsense": 'ca-pub-1043419685176632' in html,
        "has_meta_description": '<meta name="description"' in html,
        "has_broken_html_links": bool(re.search(r'href="[^"]+\.html"', html)) and filename not in ['admin.html']
    }
    report["static_pages"][filename] = page_data
    if page_data["has_broken_html_links"]:
        report["summary"]["total_issues_found"] += 1
    else:
        report["summary"]["total_passed_checks"] += 1

print(f"  Audited {len(static_files)} static HTML pages.")

# 3. AUDIT XML SITEMAP & RSS FEED
print("\n[3/6] Auditing sitemap.xml and feed.xml...")
try:
    sitemap_tree = ET.parse(SITEMAP_XML)
    sitemap_root = sitemap_tree.getroot()
    urls = sitemap_root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    report["xml_files"]["sitemap"] = {
        "valid": True,
        "total_urls": len(urls),
        "root_tag": sitemap_root.tag
    }
    report["summary"]["total_passed_checks"] += 1
except Exception as e:
    report["xml_files"]["sitemap"] = {"valid": False, "error": str(e)}
    report["summary"]["total_issues_found"] += 1

try:
    feed_tree = ET.parse(FEED_XML)
    feed_root = feed_tree.getroot()
    items = feed_root.findall('.//item')
    report["xml_files"]["feed"] = {
        "valid": True,
        "total_items": len(items),
        "root_tag": feed_root.tag
    }
    report["summary"]["total_passed_checks"] += 1
except Exception as e:
    report["xml_files"]["feed"] = {"valid": False, "error": str(e)}
    report["summary"]["total_issues_found"] += 1

# 4. AUDIT ROBOTS.TXT, ADS.TXT, _HEADERS
print("\n[4/6] Auditing robots.txt, ads.txt, and _headers...")
with open(ROBOTS_TXT, 'r', encoding='utf-8') as f:
    robots_content = f.read()

report["config_files"]["robots_txt"] = {
    "has_sitemap": 'sitemap.xml' in robots_content.lower(),
    "allows_googlebot": 'user-agent: googlebot' in robots_content.lower() and 'allow: /' in robots_content.lower(),
    "allows_mediapartners": 'user-agent: mediapartners-google' in robots_content.lower(),
    "disallows_admin": 'disallow: /admin' in robots_content.lower()
}

with open(ADS_TXT, 'r', encoding='utf-8') as f:
    ads_content = f.read()

report["config_files"]["ads_txt"] = {
    "is_valid": 'pub-1043419685176632' in ads_content and 'DIRECT' in ads_content,
    "content": ads_content.strip()
}

with open(HEADERS_FILE, 'r', encoding='utf-8') as f:
    headers_content = f.read()

report["config_files"]["_headers"] = {
    "has_x_frame_options": 'X-Frame-Options' in headers_content,
    "has_x_content_type_options": 'X-Content-Type-Options' in headers_content,
    "has_referrer_policy": 'Referrer-Policy' in headers_content,
    "has_cache_control": 'Cache-Control' in headers_content
}

# 5. AUDIT _WORKER.JS
print("\n[5/6] Auditing Cloudflare Edge Worker (_worker.js)...")
with open(WORKER_JS, 'r', encoding='utf-8') as f:
    worker_content = f.read()

report["edge_worker"] = {
    "size_bytes": len(worker_content),
    "has_homepage_ssr": 'pathname === \'/\'' in worker_content,
    "has_post_ssr": 'pathname === \'/post\'' in worker_content,
    "has_admin_shield": 'ADMIN_SECRET' in worker_content,
    "has_schema_ldjson": '"@context": "https://schema.org"' in worker_content,
    "has_faq_schema": '"@type": "FAQPage"' in worker_content,
    "has_breadcrumb_schema": '"@type": "BreadcrumbList"' in worker_content
}

# 6. OUTPUT COMPREHENSIVE REPORT
print("\n" + "=" * 70)
print("AUDIT RESULTS & STATISTICAL BREAKDOWN")
print("=" * 70)
print(f"Total Articles Audited: {report['articles']['total']}")
print(f"Articles < 600 words: {len(report['articles']['under_600_words'])}")
print(f"Articles with missing fields: {len(report['articles']['missing_fields'])}")
print(f"Banned AI words found: {len(report['articles']['banned_words_found'])}")
print(f"Duplicate titles: {len(report['articles']['duplicate_titles'])}")
print(f"Malformed HTML tags: {len(report['articles']['malformed_html'])}")

print("\n--- Categories Distribution ---")
for cat, cnt in sorted(report['articles']['categories'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {cnt} articles")

print("\n--- Static HTML Pages Audit ---")
for pg, pdata in report['static_pages'].items():
    print(f"  {pg:15} | {pdata['size_bytes']:6} bytes | Canonical: {pdata['has_canonical']} | AdSense: {pdata['has_adsense']} | Meta Desc: {pdata['has_meta_description']} | Old .html links: {pdata['has_broken_html_links']}")

print("\n--- XML Files Audit ---")
print(f"  sitemap.xml: Valid={report['xml_files']['sitemap']['valid']}, URLs={report['xml_files']['sitemap'].get('total_urls')}")
print(f"  feed.xml:    Valid={report['xml_files']['feed']['valid']}, Items={report['xml_files']['feed'].get('total_items')}")

print("\n--- Configuration & Security ---")
print(f"  robots.txt: Mediapartners allowed: {report['config_files']['robots_txt']['allows_mediapartners']}, Googlebot allowed: {report['config_files']['robots_txt']['allows_googlebot']}")
print(f"  ads.txt:    Valid publisher: {report['config_files']['ads_txt']['is_valid']}")
print(f"  _headers:   Security headers present: {report['config_files']['_headers']['has_x_frame_options'] and report['config_files']['_headers']['has_x_content_type_options']}")
print(f"  _worker.js: Edge SSR Active: {report['edge_worker']['has_homepage_ssr'] and report['edge_worker']['has_post_ssr']}, Schema.org LD-JSON: {report['edge_worker']['has_schema_ldjson']}")

with open(os.path.join(ROOT, 'scratch', 'deep_audit_report.json'), 'w', encoding='utf-8') as out:
    json.dump(report, out, indent=2)

print(f"\n[DONE] Full JSON report saved to scratch/deep_audit_report.json")
