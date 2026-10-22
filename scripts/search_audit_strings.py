import os

ROOT = r"C:\Users\BOSS\Desktop\IMTECHBOSS\imtechboss-website-backup-2026-10-03"

strings_to_check = [
    'Hardware Acceleration, VRAM Allocations',
    'below 78 degrees Celsius',
    '78 degrees Celsius',
    'In-Depth Hardware Benchmarks, System Stability',
    'do not modify protected kernel modules',
    '1.2K reads',
    'Action completed'
]

for query in strings_to_check:
    matches = []
    for root, dirs, files in os.walk(ROOT):
        if '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.html', '.json', '.js', '.py', '.txt', '.xml', '.md']:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    if query.lower() in content.lower():
                        rel = os.path.relpath(filepath, ROOT)
                        matches.append(rel)
                except Exception:
                    pass
    print(f'Query: "{query}" -> Found in {len(matches)} files')
    for m in matches[:10]:
        print(f'   {m}')
