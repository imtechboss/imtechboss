import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r"c:\Users\aabir\OneDrive\Desktop\website")

with open('js/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse initialArticles
match = re.search(r'var\s+initialArticles\s*=\s*(\[.*\])\s*;?\s*$', content, re.DOTALL)
if not match:
    print("Could not find initialArticles array")
    sys.exit(1)

articles = json.loads(match.group(1))
print(f"Total articles in data.js: {len(articles)}")

# Check top 14 articles published on Oct 1
oct1_articles = articles[:14]
print(f"\nAuditing top {len(oct1_articles)} articles:\n" + "="*80)

banned_words = [
    'delve', 'landscape', 'pivotal', 'testament', 'game-changer', 
    'in conclusion', 'tapestries', 'realm', 'beacon', 'seamlessly'
]

issues_found = []

for i, art in enumerate(oct1_articles, 1):
    art_id = art.get('id', '')
    title = art.get('title', '')
    category = art.get('category', '')
    author = art.get('author', '')
    date = art.get('date', '')
    read_time = art.get('readTime', '')
    image = art.get('image', '')
    body = art.get('body', '')
    excerpt = art.get('excerpt', '')
    
    # Calculate word count in body
    text_content = re.sub(r'<[^>]+>', ' ', body)
    words = len(text_content.split())
    
    print(f"\n[{i}] {title}")
    print(f"    ID: {art_id}")
    print(f"    Category: {category} | Author: {author} | Date: {date} | ReadTime: {read_time}")
    print(f"    Image: {image}")
    print(f"    Word count: ~{words} words")
    
    # Checks
    item_issues = []
    
    # 1. Author check
    if author != "Tech Boss":
        item_issues.append(f"Author is '{author}' (expected 'Tech Boss')")
        
    # 2. Image check
    if not ("w=1200" in image and "images.unsplash.com" in image):
        item_issues.append(f"Image not standard 1200px Unsplash: {image}")
        
    # 3. Banned words check in title, excerpt, body
    full_text = f"{title} {excerpt} {text_content}".lower()
    for bw in banned_words:
        # Check whole word match or boundary
        matches = re.findall(rf'\b{re.escape(bw)}\b', full_text)
        if matches:
            item_issues.append(f"Contains BANNED word: '{bw}' ({len(matches)} time(s))")
            
    # 4. Repeated headings or repeated paragraphs check
    h2s = re.findall(r'<h2>([^<]+)</h2>', body, re.IGNORECASE)
    if len(h2s) != len(set(h2s)):
        duplicates = [h for h in set(h2s) if h2s.count(h) > 1]
        item_issues.append(f"Duplicate <h2> tags detected: {duplicates}")
        
    h3s = re.findall(r'<h3>([^<]+)</h3>', body, re.IGNORECASE)
    if len(h3s) != len(set(h3s)):
        duplicates = [h for h in set(h3s) if h3s.count(h) > 1]
        item_issues.append(f"Duplicate <h3> tags detected: {duplicates}")
        
    # Paragraph duplicate check
    ps = [p.strip() for p in re.findall(r'<p>([^<]+)</p>', body) if len(p.strip()) > 30]
    if len(ps) != len(set(ps)):
        item_issues.append(f"Duplicate paragraphs detected in body!")

    # 5. Length check
    if words < 400:
        item_issues.append(f"Short word count ({words} words)")

    if item_issues:
        print("    ⚠️ ISSUES:")
        for iss in item_issues:
            print(f"       - {iss}")
        issues_found.append((art_id, item_issues))
    else:
        print("    ✅ Clean & Quality Standards Passed")

print("\n" + "="*80)
if not issues_found:
    print("ALL 14 ARTICLES ARE 100% CLEAN AND PASS ALL AUDIT CHECKS!")
else:
    print(f"{len(issues_found)} articles have potential issues to review.")
