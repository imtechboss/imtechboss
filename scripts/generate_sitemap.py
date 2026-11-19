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

def xml_escape(val):
    return (
        str(val or '')
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
    )

def file_lastmod(base_dir, rel_path, fallback):
    full = os.path.join(base_dir, rel_path)
    if os.path.exists(full):
        return datetime.fromtimestamp(os.path.getmtime(full)).strftime('%Y-%m-%d')
    return fallback

CORE_AND_TOOL_ROUTES = [
    ("https://imtechboss.com/", "index.html"),
    ("https://imtechboss.com/tools/", "tools/index.html"),
    ("https://imtechboss.com/tools/pc-bottleneck-calculator/", "tools/pc-bottleneck-calculator/index.html"),
    ("https://imtechboss.com/tools/llm-vram-calculator/", "tools/llm-vram-calculator/index.html"),
    ("https://imtechboss.com/tools/can-my-pc-run-it/", "tools/can-my-pc-run-it/index.html"),
    ("https://imtechboss.com/tools/ai-prompt-studio/", "tools/ai-prompt-studio/index.html"),
    ("https://imtechboss.com/tools/developer-cheat-sheets/", "tools/developer-cheat-sheets/index.html"),
    ("https://imtechboss.com/tools/gpu-matcher-quiz/", "tools/gpu-matcher-quiz/index.html"),
    ("https://imtechboss.com/tools/pc-power-supply-calculator/", "tools/pc-power-supply-calculator/index.html"),
    ("https://imtechboss.com/tools/wordpress-hosting-calculator/", "tools/wordpress-hosting-calculator/index.html"),
    ("https://imtechboss.com/tools/monitor-ppi-viewing-distance-calculator/", "tools/monitor-ppi-viewing-distance-calculator/index.html"),
    ("https://imtechboss.com/tools/windows-bsod-error-code-lookup/", "tools/windows-bsod-error-code-lookup/index.html"),
    ("https://imtechboss.com/tools/ollama-command-generator/", "tools/ollama-command-generator/index.html"),
    ("https://imtechboss.com/tools/dual-gpu-vram-split-calculator/", "tools/dual-gpu-vram-split-calculator/index.html"),
    ("https://imtechboss.com/tools/json-jwt-cron-dev-toolkit/", "tools/json-jwt-cron-dev-toolkit/index.html"),
    ("https://imtechboss.com/tools/ssd-nvme-pcie-speed-calculator/", "tools/ssd-nvme-pcie-speed-calculator/index.html"),
    ("https://imtechboss.com/tools/local-ai-electricity-cost-calculator/", "tools/local-ai-electricity-cost-calculator/index.html"),
    ("https://imtechboss.com/tools/nepal-laptop-budget-finder/", "tools/nepal-laptop-budget-finder/index.html"),
    ("https://imtechboss.com/tools/nepal-isp-router-mesh-advisor/", "tools/nepal-isp-router-mesh-advisor/index.html"),
    ("https://imtechboss.com/compare/", "compare/index.html"),
    ("https://imtechboss.com/archive/", "archive/index.html"),
    ("https://imtechboss.com/stories/", "stories/index.html"),
    ("https://imtechboss.com/about/", "about/index.html"),
]

def generate_sitemap():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'js', 'data.js')
    sitemap_path = os.path.join(base_dir, 'sitemap.xml')
    urls_txt_path = os.path.join(base_dir, 'urls.txt')

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
        '  <!-- 1. Core Hubs & 17 Interactive Engineering Tools -->',
    ]
    plain_urls = []

    for loc, rel_file in CORE_AND_TOOL_ROUTES:
        lmod = file_lastmod(base_dir, rel_file, today)
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{loc}</loc>')
        xml_lines.append(f'    <lastmod>{lmod}</lastmod>')
        xml_lines.append('  </url>')
        plain_urls.append(loc)

    xml_lines.append('  <!-- 2. Indexable Technical Guides & Nepal Tech Articles (Newest First) -->')

    noindex_slugs = {'top-5-ways-earn-money-online-2026'}
    articles_sorted = []
    for article in data:
        aid = article.get('id', '')
        if not aid or aid.startswith('blogger-') or aid in noindex_slugs:
            continue
        articles_sorted.append((clean_date(article.get('date', '')), article))

    articles_sorted.sort(key=lambda x: x[0], reverse=True)

    first_party_img_count = 0
    for date, article in articles_sorted:
        aid = article['id']
        loc = f'https://imtechboss.com/{aid}/'
        plain_urls.append(loc)
        title = xml_escape(article.get('title', ''))

        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{loc}</loc>')
        xml_lines.append(f'    <lastmod>{date}</lastmod>')

        # Collect first-party embedded /images/*.webp visuals first + featured 1200px image
        img_entries = []
        seen_imgs = set()
        body_html = article.get('content', '') or ''
        for m_img in re.finditer(r'<img\s+[^>]*src="(/images/[^"]+)"[^>]*>', body_html, re.I):
            tag = m_img.group(0)
            src_url = clean_image(m_img.group(1))
            if src_url not in seen_imgs:
                seen_imgs.add(src_url)
                m_alt = re.search(r'alt="([^"]+)"', tag, re.I)
                alt_txt = xml_escape(m_alt.group(1)) if m_alt else title
                img_entries.append((xml_escape(src_url), alt_txt))
                first_party_img_count += 1

        hero_url = clean_image(article.get('image', ''))
        if hero_url and hero_url not in seen_imgs:
            seen_imgs.add(hero_url)
            img_entries.append((xml_escape(hero_url), title))

        for safe_img, img_title in img_entries:
            xml_lines.append('    <image:image>')
            xml_lines.append(f'      <image:loc>{safe_img}</image:loc>')
            xml_lines.append(f'      <image:title>{img_title}</image:title>')
            xml_lines.append('    </image:image>')

        xml_lines.append('  </url>')

    xml_lines.append('</urlset>')
    xml_lines.append('')

    with open(sitemap_path, 'w', encoding='utf-8') as out:
        out.write('\n'.join(xml_lines))

    with open(urls_txt_path, 'w', encoding='utf-8') as uout:
        uout.write('\n'.join(plain_urls) + '\n')

    print(f'Successfully generated clean sitemap.xml ({len(plain_urls)} URLs, {first_party_img_count} first-party original images, {len(xml_lines)} lines) and synced urls.txt.')

if __name__ == '__main__':
    generate_sitemap()
