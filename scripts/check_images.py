import json, re
from collections import Counter

with open('js/data.js', 'r', encoding='utf-8') as f:
    c = f.read()

articles = json.loads(re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', c, re.DOTALL).group(1))

imgs = [a.get('image', '').strip() for a in articles if a.get('image')]
counts = Counter(imgs)
repeated = {img: count for img, count in counts.items() if count > 1}

print(f"Total images: {len(imgs)}")
print(f"Unique images: {len(counts)}")
print(f"Repeated images count: {len(repeated)}")
for img, cnt in sorted(repeated.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  Count: {cnt} | {img}")
