import json, re

with open('js/data.js', 'r', encoding='utf-8') as f:
    c = f.read()

articles = json.loads(re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', c, re.DOTALL).group(1))

for aid in ['intel-core-ultra-9-285k-vs-amd-ryzen-9-9950x3d-gaming-benchmarks-2026', 'best-free-vpns-gaming-streaming-no-logs-zero-lag-2026']:
    a = next(x for x in articles if x['id'] == aid)
    for p in (a.get('content') or '').split('</p>'):
        if any(w in p.lower() for w in ['torture', 'hardware lab']):
            print(f"[{aid}]")
            print(re.sub(r'<[^>]+>', '', p).strip())
