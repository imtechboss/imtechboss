import os
import shutil
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
redirects_file = os.path.join(base_dir, '_redirects')
redir_json = os.path.join(base_dir, 'scripts', 'duplicate_redirects.json')

with open(redir_json, 'r', encoding='utf-8') as f:
    redirect_map = json.load(f)

lines = [
    "https://www.imtechboss.com/*  https://imtechboss.com/:splat  301"
]

for src, dst in redirect_map.items():
    lines.append(f"/{src}  /{dst}/  301")
    lines.append(f"/{src}/*  /{dst}/  301")

    # Delete old directory if it exists on disk
    src_dir = os.path.join(base_dir, src)
    if os.path.exists(src_dir):
        shutil.rmtree(src_dir)
        print(f"[REMOVED OLD DIR] {src}")

with open(redirects_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print("[OK] Updated _redirects with 301 mappings for all duplicate posts!")
