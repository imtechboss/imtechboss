import re, json, os
from datetime import datetime

months = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
    'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
    'January': '01', 'February': '02', 'March': '03', 'April': '04', 'June': '06',
    'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
}

def clean_date(d_str):
    if not d_str:
        return datetime.now().strftime('%Y-%m-%d')
    d_str = str(d_str).strip()
    if re.match(r'^\d{4}-\d{2}-\d{2}$', d_str):
        return d_str
    m = re.match(r'^([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})$', d_str)
    if m:
        mon = months.get(m.group(1), '01')
        day = f'{int(m.group(2)):02d}'
        yr = m.group(3)
        return f'{yr}-{mon}-{day}'
    return datetime.now().strftime('%Y-%m-%d')

def clean_image(img):
    if not img:
        return ''
    img = img.strip()
    if img.startswith('http://') or img.startswith('https://'):
        return img
    clean_path = img.lstrip('/')
    return f'https://imtechboss.com/{clean_path}'

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

    today = datetime.now().strftime("%Y-%m-%d")
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
        '  <url>',
        '    <loc>https://imtechboss.com/</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://imtechboss.com/about.html</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.7</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://imtechboss.com/contact.html</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.7</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://imtechboss.com/privacy.html</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.5</priority>',
        '  </url>',
        '  <url>',
        '    <loc>https://imtechboss.com/disclaimer.html</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.5</priority>',
        '  </url>',
    ]

    for article in data:
        aid = article.get('id', '')
        date = clean_date(article.get('date', ''))
        raw_image = article.get('image', '')
        image = clean_image(raw_image)
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

    print(f'Successfully generated sitemap.xml with {len(data) + 5} URLs (5 static + {len(data)} articles).')

if __name__ == '__main__':
    generate_sitemap()
