import os
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for fname in ['post.html', 'index.html']:
    fpath = os.path.join(base_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match the noscript block
    noscript_pattern = r'\s*<!-- Noscript Fallback -->\s*<noscript>[\s\S]*?</noscript>'
    new_content = re.sub(noscript_pattern, '', content)

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[OK] Removed 'JavaScript is required' <noscript> from {fname}")
    else:
        # Fallback direct replace
        fallback_pattern = r'<noscript>[\s\S]*?JavaScript is required[\s\S]*?</noscript>'
        new_content = re.sub(fallback_pattern, '', content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[OK] Removed fallback <noscript> from {fname}")
        else:
            print(f"[WARN] No noscript matched in {fname}")
