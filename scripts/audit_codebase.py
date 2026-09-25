import re, json, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def audit():
    print("=== STARTING COMPREHENSIVE CODEBASE AUDIT ===")

    # 1. Audit data.js fields
    with open(os.path.join(base_dir, 'js', 'data.js'), 'r', encoding='utf-8') as f:
        data_raw = f.read()
    m = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', data_raw, re.DOTALL)
    articles = json.loads(m.group(1))

    required_fields = ['id', 'title', 'excerpt', 'content', 'category', 'image', 'date']
    missing_fields = []
    ids = set()
    duplicate_ids = []

    for idx, a in enumerate(articles):
        aid = a.get('id')
        if not aid:
            missing_fields.append((idx, 'id'))
        elif aid in ids:
            duplicate_ids.append(aid)
        else:
            ids.add(aid)

        for field in required_fields:
            if not a.get(field):
                missing_fields.append((aid or idx, field))

    print(f"1. Articles Check: Total = {len(articles)}")
    print(f"   - Duplicate IDs: {len(duplicate_ids)} {duplicate_ids[:3] if duplicate_ids else ''}")
    print(f"   - Missing required fields: {len(missing_fields)} {missing_fields[:3] if missing_fields else ''}")

    # 2. Check DOM IDs in app.js vs index.html
    with open(os.path.join(base_dir, 'index.html'), 'r', encoding='utf-8') as f:
        index_html = f.read()
    with open(os.path.join(base_dir, 'js', 'app.js'), 'r', encoding='utf-8') as f:
        app_js = f.read()

    app_ids = re.findall(r'getElementById\(["\'](.*?)["\']\)', app_js)
    missing_index_ids = []
    for elem_id in set(app_ids):
        if f'id="{elem_id}"' not in index_html and f"id='{elem_id}'" not in index_html:
            missing_index_ids.append(elem_id)

    print(f"2. index.html vs app.js DOM IDs:")
    print(f"   - Referenced IDs in app.js: {len(set(app_ids))}")
    print(f"   - Missing IDs in index.html: {missing_index_ids}")

    # 3. Check DOM IDs in post.js vs post.html
    with open(os.path.join(base_dir, 'post.html'), 'r', encoding='utf-8') as f:
        post_html = f.read()
    with open(os.path.join(base_dir, 'js', 'post.js'), 'r', encoding='utf-8') as f:
        post_js = f.read()

    post_ids = re.findall(r'getElementById\(["\'](.*?)["\']\)', post_js)
    missing_post_ids = []
    for elem_id in set(post_ids):
        if f'id="{elem_id}"' not in post_html and f"id='{elem_id}'" not in post_html:
            missing_post_ids.append(elem_id)

    print(f"3. post.html vs post.js DOM IDs:")
    print(f"   - Referenced IDs in post.js: {len(set(post_ids))}")
    print(f"   - Missing IDs in post.html: {missing_post_ids}")

    # 4. Check all local links across all HTML files
    html_files = [f for f in os.listdir(base_dir) if f.endswith('.html')]
    print(f"4. Checking local links in {len(html_files)} HTML files:")
    all_targets = set(html_files + ['css/style.css', 'favicon.svg', 'manifest.json'])
    broken_links = []

    for hf in html_files:
        with open(os.path.join(base_dir, hf), 'r', encoding='utf-8') as f:
            content = f.read()
        links = re.findall(r'href=["\'](.*?)["\']', content)
        for link in links:
            if link.startswith('http') or link.startswith('#') or link.startswith('mailto:') or link.startswith('javascript:'):
                continue
            clean_link = link.split('?')[0].split('#')[0]
            rel_path = clean_link.lstrip('/')
            exists = (
                clean_link in all_targets or
                os.path.exists(os.path.join(base_dir, rel_path)) or
                os.path.exists(os.path.join(base_dir, rel_path, 'index.html'))
            )
            if clean_link and not exists:
                broken_links.append((hf, link))

    print(f"   - Broken local href links: {broken_links}")

    # 5. Check Search Regex safety
    regex_danger = []
    if 'new RegExp(' in app_js:
        regex_danger.append('app.js uses new RegExp')
    if 'new RegExp(' in post_js:
        regex_danger.append('post.js uses new RegExp')
    print(f"5. Search Regex checks: {regex_danger if regex_danger else 'Safe (no unescaped dynamic RegExp)'}")

    print("=== AUDIT COMPLETE ===")

if __name__ == '__main__':
    audit()
