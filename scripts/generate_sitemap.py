import re, json, os
from datetime import datetime

def generate_sitemap():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'js', 'data.js')
    sitemap_path = os.path.join(base_dir, 'sitemap.xml')

    with open(data_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if not match:
        print('Error: initialArticles not found')
        return

    data = json.loads(match.group(1))

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
        '  <url>',
        '    <loc>https://imtechboss.com/</loc>',
        f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
    ]

    for article in data:
        aid = article.get('id', '')
        date = article.get('date', datetime.now().strftime('%Y-%m-%d'))
        image = article.get('image', '')
        title = article.get('title', '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>https://imtechboss.com/post?id={aid}</loc>')
        xml_lines.append(f'    <lastmod>{date}</lastmod>')
        xml_lines.append('    <changefreq>weekly</changefreq>')
        xml_lines.append('    <priority>0.8</priority>')

        if image:
            safe_image = image.replace('&', '&amp;')
            xml_lines.append('    <image:image>')
            xml_lines.append(f'      <image:loc>{safe_image}</image:loc>')
            xml_lines.append(f'      <image:title>{title}</image:title>')
            xml_lines.append('    </image:image>')

        xml_lines.append('  </url>')

    xml_lines.append('</urlset>')
    xml_lines.append('')

    with open(sitemap_path, 'w', encoding='utf-8') as out:
        out.write('\n'.join(xml_lines))

    print(f'Successfully generated sitemap.xml with {len(data) + 1} URLs (homepage + {len(data)} articles).')

if __name__ == '__main__':
    generate_sitemap()
