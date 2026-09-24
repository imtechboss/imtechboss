import glob, re, json, xml.etree.ElementTree as ET

with open('js/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', content, re.DOTALL)
articles = json.loads(match.group(1))
valid_ids = set(str(a['id']) for a in articles)

print(f'Total valid article IDs in data.js: {len(valid_ids)}')

# Check XML files
for xml_file in ['feed.xml', 'sitemap.xml']:
    with open(xml_file, 'r', encoding='utf-8') as f:
        c = f.read()
    found = re.findall(r'post(?:\.html)?\?id=([a-zA-Z0-9_\-]+)', c)
    invalid_xml = [aid for aid in set(found) if aid not in valid_ids]
    if invalid_xml:
        print(f'INVALID ARTICLE LINK in {xml_file}: {invalid_xml}')
    else:
        print(f'{xml_file} article links: ALL {len(found)} VALID!')

# Check HTML and JS
files = glob.glob('*.html') + glob.glob('js/*.js')
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    found = re.findall(r'post(?:\.html)?\?id=([a-zA-Z0-9_\-]+)', c)
    for article_id in set(found):
        if article_id not in valid_ids:
            print(f'INVALID ARTICLE LINK in {fpath}: id="{article_id}"')

print('Comprehensive link check finished.')
