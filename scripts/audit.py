import re

# 1. Audit app.js vs index.html
with open('js/app.js', encoding='utf-8') as f:
    app_code = f.read()

with open('index.html', encoding='utf-8') as f:
    index_html = f.read()

ids_in_app = set(re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", app_code))
missing_index = [i for i in ids_in_app if f'id="{i}"' not in index_html and f"id='{i}'" not in index_html]

print("=== Audit 1: Missing IDs in index.html ===")
for m in sorted(missing_index):
    print(" -", m)

# 2. Audit post.js vs post.html
with open('js/post.js', encoding='utf-8') as f:
    post_code = f.read()

with open('post.html', encoding='utf-8') as f:
    post_html = f.read()

ids_in_post = set(re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", post_code))
missing_post = [i for i in ids_in_post if f'id="{i}"' not in post_html and f"id='{i}'" not in post_html]

print("\n=== Audit 2: Missing IDs in post.html (static elements only) ===")
for m in sorted(missing_post):
    print(" -", m)

# 3. Check Service Worker sw.js
with open('sw.js', encoding='utf-8') as f:
    sw_code = f.read()

cached_assets = re.findall(r"['\"](/[^'\"]+)['\"]", sw_code)
print("\n=== Audit 3: Cached assets in sw.js ===")
for c in cached_assets:
    print(" -", c)
