import json
import re

w = open('_worker.js', encoding='utf-8').read()
m = re.search(r'const articlesMeta = ({.*?});\s*const topArticles', w, re.DOTALL)
meta = json.loads(m.group(1))

d = open('js/data.js', encoding='utf-8').read()
arts = json.loads(re.search(r'var initialArticles = (\[.*?\]);', d, re.DOTALL).group(1))

print("Checking content length in _worker.js for top 14 articles:")
all_ok = True
for i, a in enumerate(arts[:14], 1):
    c_len = len(meta.get(a['id'], {}).get('content', ''))
    status = "OK" if c_len > 1000 else "FAIL"
    if status == "FAIL":
        all_ok = False
    print(f" {i:2d}. {a['id'][:50]}... : {c_len} chars [{status}]")

print(f"\nAll 14 articles have full SSR content: {all_ok}")
