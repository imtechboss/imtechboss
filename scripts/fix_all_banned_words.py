import json, re

f = open('js/data.js', encoding='utf-8').read()
start = f.find('[')
end = f.rfind(']') + 1
articles = json.loads(f[start:end])

def clean_text(html):
    # Case-insensitive replacements
    # 1. landscape
    html = re.sub(r'\bthe AI landscape\b', 'the AI sector', html, flags=re.IGNORECASE)
    html = re.sub(r'\btech landscape\b', 'tech industry', html, flags=re.IGNORECASE)
    html = re.sub(r'\bcompetitive landscape\b', 'competitive ecosystem', html, flags=re.IGNORECASE)
    html = re.sub(r'\blandscape\b', 'ecosystem', html, flags=re.IGNORECASE)

    # 2. seamlessly
    html = re.sub(r'\bseamlessly\b', 'smoothly', html, flags=re.IGNORECASE)

    # 3. in conclusion
    html = re.sub(r'\bin conclusion\b', 'in summary', html, flags=re.IGNORECASE)

    # 4. realm
    html = re.sub(r'\bin the realm of\b', 'in the field of', html, flags=re.IGNORECASE)
    html = re.sub(r'\bwithin the realm of\b', 'within the domain of', html, flags=re.IGNORECASE)
    html = re.sub(r'\brealm\b', 'domain', html, flags=re.IGNORECASE)

    # 5. Other banned words if present
    html = re.sub(r'\bdelve into\b', 'examine', html, flags=re.IGNORECASE)
    html = re.sub(r'\bdelve\b', 'explore', html, flags=re.IGNORECASE)
    html = re.sub(r'\bpivotal\b', 'crucial', html, flags=re.IGNORECASE)
    html = re.sub(r'\btestament to\b', 'evidence of', html, flags=re.IGNORECASE)
    html = re.sub(r'\btestament\b', 'proof', html, flags=re.IGNORECASE)
    html = re.sub(r'\bgame-changer\b', 'major advance', html, flags=re.IGNORECASE)
    html = re.sub(r'\bgame changer\b', 'major advance', html, flags=re.IGNORECASE)
    html = re.sub(r'\btapestries\b', 'complex systems', html, flags=re.IGNORECASE)
    html = re.sub(r'\btapestry\b', 'complex system', html, flags=re.IGNORECASE)
    html = re.sub(r'\bbeacon of\b', 'leader in', html, flags=re.IGNORECASE)
    html = re.sub(r'\bbeacon\b', 'guide', html, flags=re.IGNORECASE)

    return html

modified = 0
for a in articles:
    old_c = a.get('content', '')
    new_c = clean_text(old_c)
    if old_c != new_c:
        a['content'] = new_c
        modified += 1

print(f"Cleaned banned words across {modified} articles.")
new_data_js = "var initialArticles = " + json.dumps(articles, ensure_ascii=False, indent=2) + ";\n"
open('js/data.js', 'w', encoding='utf-8').write(new_data_js)
print("Updated js/data.js successfully.")
