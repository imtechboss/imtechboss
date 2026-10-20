import re, json

with open('js/data.js', 'r', encoding='utf-8') as f:
    c = f.read()

articles = json.loads(re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', c, re.DOTALL).group(1))
q_post = next((a for a in articles if 'quantum' in a['id']), None)
if q_post:
    print("Found quantum post:", q_post['id'])
    content = q_post.get('content') or q_post.get('body') or ''
    # Check for AWQ, 78, GPU, quantization
    matches = [line for line in content.split('\n') if any(w in line.lower() for w in ['awq', 'junction', '78°c', 'quantization', 'gpu'])]
    print(f"Suspicious lines found ({len(matches)}):")
    for m in matches:
        print("  -", m[:120])
else:
    print("Quantum post not found!")
