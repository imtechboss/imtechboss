import os, re, json, glob, html

ROOT = r"C:\Users\BOSS\Desktop\IMTECHBOSS\imtechboss-website-backup-2026-10-03"
POSTS_FILE = os.path.join(ROOT, "posts.json")
DATA_JS = os.path.join(ROOT, "js", "data.js")

with open(POSTS_FILE, 'r', encoding='utf-8') as f:
    posts = json.load(f)

print("=" * 60)
print("     COMPREHENSIVE 8-POINT MASTER AUDIT VERIFICATION")
print("=" * 60)

# Check 1: ERR-01 Programmatic Boilerplate Padding
bp_patterns = [
    r'Hardware Acceleration, VRAM Allocations',
    r'In-Depth Hardware Benchmarks, System Stability',
    r'Firmware Architecture, Battery Health',
    r'Security Architecture, Cryptographic Standards',
    r'Technical Architecture, Best Practices',
    r'Frequently Asked Questions \(FAQ\) &amp; Expert Analysis',
    r'Frequently Asked Questions \(FAQ\) & Expert Analysis',
    r'78 degrees Celsius'
]

bp_matches_posts = 0
bp_matches_html = 0

for p in posts:
    c = p.get('content', '')
    for pat in bp_patterns:
        if re.search(pat, c):
            bp_matches_posts += 1
            print(f"  [FAIL ERR-01 in posts.json] {p['id']} matches {pat}")
            break

for p in posts:
    idx_path = os.path.join(ROOT, p['id'], "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, 'r', encoding='utf-8', errors='ignore') as f:
            c_html = f.read()
        for pat in bp_patterns:
            if re.search(pat, c_html):
                bp_matches_html += 1
                print(f"  [FAIL ERR-01 in static HTML] {p['id']} matches {pat}")
                break

print(f"ERR-01 Boilerplate Matches: posts.json={bp_matches_posts}, static_html={bp_matches_html} (PASS if 0)")

# Check 2: ERR-02 Duplicate FAQ Blocks
dup_faqs = 0
for p in posts:
    idx_path = os.path.join(ROOT, p['id'], "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, 'r', encoding='utf-8', errors='ignore') as f:
            c_html = f.read()
        faq_headers = re.findall(r'<h[23][^>]*>(?:Frequently Asked Questions|FAQ)[\s\S]*?</h[23]>', c_html, re.IGNORECASE)
        if len(faq_headers) > 1:
            dup_faqs += 1
            print(f"  [FAIL ERR-02] Duplicate FAQ in {p['id']}: found {len(faq_headers)} headers")

print(f"ERR-02 Duplicate FAQ Headers: {dup_faqs} (PASS if 0)")

# Check 3: ERR-03 Cross-Wired Article Slugs
mismatched_titles = 0
for p in posts:
    idx_path = os.path.join(ROOT, p['id'], "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, 'r', encoding='utf-8', errors='ignore') as f:
            c_html = f.read()
        m = re.search(r'<title id="pageTitle">(.*?)</title>', c_html)
        if m:
            html_title = html.unescape(m.group(1).replace(' — Tech Boss', '').strip())
            json_title = html.unescape(p['title'].strip())
            w1 = re.sub(r'[^\w\s]', '', html_title.lower()).split()[:6]
            w2 = re.sub(r'[^\w\s]', '', json_title.lower()).split()[:6]
            if w1 != w2:
                mismatched_titles += 1
                print(f"  [FAIL ERR-03] Mismatch in {p['id']}:\n    HTML: {html_title}\n    JSON: {json_title}")
        else:
            mismatched_titles += 1

print(f"ERR-03 Cross-Wired Slugs / Title Mismatches: {mismatched_titles} (PASS if 0)")

# Check 4: ERR-04 301 Redirects for Duplicate and Query Patterns
with open(os.path.join(ROOT, "functions", "[[path]].js"), 'r', encoding='utf-8') as f:
    funcs_code = f.read()
query_redirect_ok = "/post.html" in funcs_code and "/post" in funcs_code and "301" in funcs_code
print(f"ERR-04 Query & Duplicate URL 301 Redirect Shield in Edge Function: {'PASS' if query_redirect_ok else 'FAIL'}")

# Check 5: ERR-05 Header Navigation & Stray '0' Badge
with open(os.path.join(ROOT, "index.html"), 'r', encoding='utf-8') as f:
    index_html = f.read()

stray_zero = '<span id="bookmarksCountBadge"' in index_html and '>0</span>' in index_html
drawer_nosnippet = '<div id="mobileDrawer" data-nosnippet="" aria-hidden="true"' in index_html
badge_nosnippet = '<span id="bookmarksCountBadge" data-nosnippet="" aria-hidden="true"' in index_html

print(f"ERR-05 Stray '0' in raw HTML: {'FAIL (found stray 0)' if stray_zero else 'PASS (clean)'}")
print(f"ERR-05 Mobile Drawer nosnippet & aria-hidden: {'PASS' if drawer_nosnippet else 'FAIL'}")
print(f"ERR-05 Bookmarks Badge nosnippet & aria-hidden: {'PASS' if badge_nosnippet else 'FAIL'}")

# Check 6: ERR-06 Duplicated TOC and Summary Lists
raw_h2_in_takeaways = 0
for p in posts:
    idx_path = os.path.join(ROOT, p['id'], "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, 'r', encoding='utf-8', errors='ignore') as f:
            c_html = f.read()
        capsule_m = re.search(r'id="aioAnswerCapsule"[\s\S]*?</div>\s*<!-- In-Depth Table of Contents -->', c_html)
        if capsule_m:
            capsule_text = capsule_m.group(0)
            raw_items = re.findall(r'<li[^>]*>\s*<span[^>]*></span>\s*<span[^>]*><strong>([^:<]+)</strong>\s*</span>\s*</li>', capsule_text)
            if raw_items:
                raw_h2_in_takeaways += 1

print(f"ERR-06 Raw H2 Duplicate Takeaways in Capsule: {raw_h2_in_takeaways} (PASS if 0)")

# Check 7: ERR-07 Consistent Human-Readable Dates
iso_dates_found = 0
for p in posts:
    d = p.get('date', '')
    if re.match(r'^\d{4}-\d{2}-\d{2}$', d):
        iso_dates_found += 1
        print(f"  [FAIL ERR-07] Raw ISO date in {p['id']}: {d}")

print(f"ERR-07 Raw ISO Date Strings in posts.json: {iso_dates_found} (PASS if 0)")

# Check 8: ERR-08 UI Elements masked with data-nosnippet
unmasked_ui = 0
for p in posts:
    idx_path = os.path.join(ROOT, p['id'], "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, 'r', encoding='utf-8', errors='ignore') as f:
            c_html = f.read()
        if 'id="articleAudioBar"' in c_html and 'id="articleAudioBar" data-nosnippet=""' not in c_html:
            unmasked_ui += 1
        if 'id="searchModal"' in c_html and 'id="searchModal" data-nosnippet=""' not in c_html:
            unmasked_ui += 1
        if 'id="toastNotification"' in c_html and 'id="toastNotification" data-nosnippet=""' not in c_html:
            unmasked_ui += 1

print(f"ERR-08 Unmasked UI Controls in Static Pages: {unmasked_ui} (PASS if 0)")

# Additional Check: Robots Directives on Active Articles
noindex_on_active = 0
for p in posts:
    idx_path = os.path.join(ROOT, p['id'], "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, 'r', encoding='utf-8', errors='ignore') as f:
            c_html = f.read()
        if 'content="noindex' in c_html:
            noindex_on_active += 1
            print(f"  [FAIL ROBOTS] Active post has noindex: {p['id']}")

print(f"Robots Tag Check: Active Posts with 'noindex': {noindex_on_active} (PASS if 0)")

# Contact Email Check
wrong_emails = 0
for check_file in ["index.html", "about.html", "contact.html", "privacy.html", "terms.html", "disclaimer.html"]:
    path = os.path.join(ROOT, check_file)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        matches = re.findall(r'[\w\.-]+@imtechboss\.com', content)
        for m in set(matches):
            if m != "founder@imtechboss.com":
                wrong_emails += 1
                print(f"  [FAIL EMAIL] Found {m} in {check_file}")

print(f"Official Contact Email Check (founder@imtechboss.com): Wrong Emails={wrong_emails} (PASS if 0)")
print("=" * 60)
