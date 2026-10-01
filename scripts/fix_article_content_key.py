import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r"c:\Users\aabir\OneDrive\Desktop\website")

with open('js/data.js', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', text, re.DOTALL)
if not match:
    print("Could not find initialArticles")
    sys.exit(1)

articles = json.loads(match.group(1))
print(f"Loaded {len(articles)} articles.")

fixed_count = 0
for a in articles:
    if 'body' in a and 'content' not in a:
        a['content'] = a.pop('body')
        fixed_count += 1
    elif 'body' in a and 'content' in a:
        # If both exist, keep content or sync
        if not a['content'] and a['body']:
            a['content'] = a.pop('body')
            fixed_count += 1

print(f"Migrated 'body' -> 'content' for {fixed_count} articles.")

# Write back to js/data.js
new_json = json.dumps(articles, indent=2, ensure_ascii=False)
new_data_js = f"var initialArticles = {new_json};\n"

with open('js/data.js', 'w', encoding='utf-8') as f:
    f.write(new_data_js)

print("Successfully updated js/data.js!")
