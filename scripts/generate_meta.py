import re, json, os

def generate_meta():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'js', 'data.js')
    functions_dir = os.path.join(base_dir, 'functions')
    os.makedirs(functions_dir, exist_ok=True)
    out_path = os.path.join(functions_dir, 'articles_meta.js')

    with open(data_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if not match:
        print("Error: initialArticles not found in js/data.js")
        return

    data = json.loads(match.group(1))
    meta = {}
    for a in data:
        meta[a['id']] = {
            'title': a.get('title', ''),
            'excerpt': a.get('excerpt', ''),
            'image': a.get('image', ''),
            'date': a.get('date', '')
        }

    with open(out_path, 'w', encoding='utf-8') as out:
        out.write('// Auto-generated articles metadata for Cloudflare Pages Edge Functions\n')
        out.write('export const articlesMeta = ' + json.dumps(meta, indent=2, ensure_ascii=False) + ';\n')

    print(f"Generated functions/articles_meta.js successfully. Total articles: {len(meta)}")

if __name__ == '__main__':
    generate_meta()
