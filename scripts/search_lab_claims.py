import json, re

with open('js/data.js', 'r', encoding='utf-8') as f:
    c = f.read()

articles = json.loads(re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', c, re.DOTALL).group(1))

suspicious_phrases = [
    'our hardware lab',
    'our lab tested',
    'our test lab',
    'in our lab',
    'our testing lab',
    'torture benchmarks'
]

matches = []
for a in articles:
    text = f"{a.get('title','')} {a.get('excerpt','')} {a.get('content','') or a.get('body','')}".lower()
    for sp in suspicious_phrases:
        if sp in text:
            matches.append((a['id'], sp))

print(f"Found {len(matches)} suspicious lab claims:")
for aid, sp in matches:
    print(f"  {aid}: '{sp}'")
