import glob
import os

files = glob.glob('js/*.js') + glob.glob('scripts/*.py') + ['_worker.js']
patterns = ['article.body', 'article.content', 'art.body', 'art.content', 'a.get(\'content', 'a.get(\'body', 'a[\'content', 'a[\'body', 'a.content', 'a.body']

for fpath in files:
    if not os.path.exists(fpath):
        continue
    matches = []
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        for idx, line in enumerate(f, 1):
            for p in patterns:
                if p in line:
                    matches.append((idx, p, line.strip()))
                    break
    if matches:
        print(f"=== {fpath} ===")
        for line_no, pat, l in matches[:10]:
            print(f"  Line {line_no}: {l}")
