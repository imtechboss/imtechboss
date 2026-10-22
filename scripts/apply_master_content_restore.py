import subprocess, re, json, datetime, os

ROOT = r"C:\Users\BOSS\Desktop\IMTECHBOSS\imtechboss-website-backup-2026-10-03"
POSTS_FILE = os.path.join(ROOT, "posts.json")
DATA_JS = os.path.join(ROOT, "js", "data.js")

# 1. Fetch clean articles from git commit cb331e9 (the commit right before boilerplate injection)
print("Fetching clean baseline articles from git commit cb331e9...")
p = subprocess.run(['git', 'show', 'cb331e9:js/data.js'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
m = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', p.stdout, re.DOTALL)
if not m:
    raise RuntimeError("Could not extract initialArticles from cb331e9:js/data.js")

clean_articles_map = {a['id']: a for a in json.loads(m.group(1))}
print(f"Loaded {len(clean_articles_map)} pristine baseline articles.")

# 2. Load current posts.json (123 active posts)
with open(POSTS_FILE, 'r', encoding='utf-8') as f:
    current_posts = json.load(f)

print(f"Loaded {len(current_posts)} current active posts from posts.json.")

# Date normalizer helper
def normalize_date(date_str):
    if not date_str:
        return "October 18, 2026"
    date_str = date_str.strip()
    m_iso = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', date_str)
    if m_iso:
        y, m, d = int(m_iso.group(1)), int(m_iso.group(2)), int(m_iso.group(3))
        dt = datetime.date(y, m, d)
        return dt.strftime('%B %d, %Y').replace(' 0', ' ')
    for fmt in ('%b %d, %Y', '%B %d, %Y', '%b %d %Y', '%B %d %Y'):
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return dt.strftime('%B %d, %Y').replace(' 0', ' ')
        except ValueError:
            pass
    return date_str

BOILERPLATE_PATTERNS = [
    r'<h2[^>]*>Hardware Acceleration, VRAM Allocations[\s\S]*',
    r'<h2[^>]*>In-Depth Hardware Benchmarks, System Stability[\s\S]*',
    r'<h2[^>]*>Firmware Architecture, Battery Health[\s\S]*',
    r'<h2[^>]*>Security Architecture, Cryptographic Standards[\s\S]*',
    r'<h2[^>]*>Technical Architecture, Best Practices[\s\S]*',
    r'<h2[^>]*>Frequently Asked Questions \(FAQ\) &amp; Expert Analysis[\s\S]*',
    r'<h2[^>]*>Frequently Asked Questions \(FAQ\) & Expert Analysis[\s\S]*'
]

def clean_boilerplate(html):
    if not html:
        return ""
    cleaned = html
    for pat in BOILERPLATE_PATTERNS:
        m = re.search(pat, cleaned)
        if m:
            cleaned = cleaned[:m.start()].strip()
    return cleaned

restored_from_cb = 0
retained_newer = 0
cleaned_posts = []

for post in current_posts:
    pid = post['id']
    title = post['title']
    
    # Normalize Date
    post['date'] = normalize_date(post.get('date', ''))
    
    # Restore content
    if pid in clean_articles_map:
        clean_entry = clean_articles_map[pid]
        clean_content = clean_entry.get('content', '')
        # Verify clean content has no boilerplate
        clean_content = clean_boilerplate(clean_content)
        post['content'] = clean_content
        restored_from_cb += 1
    else:
        # Newer post, ensure any potential boilerplate is stripped
        post['content'] = clean_boilerplate(post.get('content', ''))
        retained_newer += 1
    
    cleaned_posts.append(post)

print(f"Restored from pristine baseline: {restored_from_cb} posts.")
print(f"Retained & verified newer posts: {retained_newer} posts.")

# Verification check
def word_count(html):
    text = re.sub(r'<[^>]+>', ' ', html or '')
    return len(text.split())

bp_check_failures = 0
empty_check_failures = 0

for p in cleaned_posts:
    c = p.get('content', '')
    wc = word_count(c)
    if wc == 0:
        print(f"[ERROR] Post {p['id']} has EMPTY content!")
        empty_check_failures += 1
    for pat in BOILERPLATE_PATTERNS:
        if re.search(pat, c):
            print(f"[ERROR] Post {p['id']} STILL contains boilerplate matching {pat}!")
            bp_check_failures += 1

if bp_check_failures > 0 or empty_check_failures > 0:
    raise RuntimeError(f"Sanitization validation failed: bp_errors={bp_check_failures}, empty_errors={empty_check_failures}")

print("[VERIFICATION PASSED] All 123 posts verified: 0 boilerplate matches, 0 empty contents!")

# Save to posts.json
with open(POSTS_FILE, 'w', encoding='utf-8') as f:
    json.dump(cleaned_posts, f, ensure_ascii=False, indent=2)
print("Updated posts.json successfully.")

# Save to js/data.js
data_js_content = "var initialArticles = " + json.dumps(cleaned_posts, ensure_ascii=False, indent=2) + ";\n"
with open(DATA_JS, 'w', encoding='utf-8') as f:
    f.write(data_js_content)
print("Updated js/data.js successfully.")
