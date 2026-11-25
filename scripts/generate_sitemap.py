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

def load_existing_lastmods(sitemap_path):
    """Preserve existing lastmod dates for static pages so rebuilds never fake-bump unchanged routes."""
    existing = {}
    if not os.path.exists(sitemap_path):
        return existing
    try:
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            txt = f.read()
        for m in re.finditer(r'<url>\s*<loc>([^<]+)</loc>\s*<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>', txt):
            existing[m.group(1).strip()] = m.group(2).strip()
    except Exception:
        pass
    return existing

# (loc, rel_file, is_dynamic_hub)
CORE_AND_TOOL_ROUTES = [
    ("https://imtechboss.com/", "index.html", True),
    ("https://imtechboss.com/tools/", "tools/index.html", False),
    ("https://imtechboss.com/tools/pc-bottleneck-calculator/", "tools/pc-bottleneck-calculator/index.html", False),
    ("https://imtechboss.com/tools/llm-vram-calculator/", "tools/llm-vram-calculator/index.html", False),
    ("https://imtechboss.com/tools/can-my-pc-run-it/", "tools/can-my-pc-run-it/index.html", False),
    ("https://imtechboss.com/tools/ai-prompt-studio/", "tools/ai-prompt-studio/index.html", False),
    ("https://imtechboss.com/tools/developer-cheat-sheets/", "tools/developer-cheat-sheets/index.html", False),
    ("https://imtechboss.com/tools/gpu-matcher-quiz/", "tools/gpu-matcher-quiz/index.html", False),
    ("https://imtechboss.com/tools/pc-power-supply-calculator/", "tools/pc-power-supply-calculator/index.html", False),
    ("https://imtechboss.com/tools/wordpress-hosting-calculator/", "tools/wordpress-hosting-calculator/index.html", False),
    ("https://imtechboss.com/tools/monitor-ppi-viewing-distance-calculator/", "tools/monitor-ppi-viewing-distance-calculator/index.html", False),
    ("https://imtechboss.com/tools/windows-bsod-error-code-lookup/", "tools/windows-bsod-error-code-lookup/index.html", False),
    ("https://imtechboss.com/tools/ollama-command-generator/", "tools/ollama-command-generator/index.html", False),
    ("https://imtechboss.com/tools/dual-gpu-vram-split-calculator/", "tools/dual-gpu-vram-split-calculator/index.html", False),
    ("https://imtechboss.com/tools/json-jwt-cron-dev-toolkit/", "tools/json-jwt-cron-dev-toolkit/index.html", False),
    ("https://imtechboss.com/tools/ssd-nvme-pcie-speed-calculator/", "tools/ssd-nvme-pcie-speed-calculator/index.html", False),
    ("https://imtechboss.com/tools/local-ai-electricity-cost-calculator/", "tools/local-ai-electricity-cost-calculator/index.html", False),
    ("https://imtechboss.com/tools/nepal-laptop-budget-finder/", "tools/nepal-laptop-budget-finder/index.html", False),
    ("https://imtechboss.com/tools/nepal-isp-router-mesh-advisor/", "tools/nepal-isp-router-mesh-advisor/index.html", False),
    ("https://imtechboss.com/compare/", "compare/index.html", False),
    ("https://imtechboss.com/archive/", "archive/index.html", True),
    ("https://imtechboss.com/stories/", "stories/index.html", False),
    ("https://imtechboss.com/nepal/", "nepal/index.html", True),
    ("https://imtechboss.com/author/binod-bhatt/", "author/binod-bhatt/index.html", False),
    ("https://imtechboss.com/about/", "about/index.html", False),
]

def generate_sitemap():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'js', 'data.js')
    sitemap_path = os.path.join(base_dir, 'sitemap.xml')
    urls_txt_path = os.path.join(base_dir, 'urls.txt')
    dup_redir_path = os.path.join(base_dir, 'scripts', 'duplicate_redirects.json')

    with open(data_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if not match:
        print('Error: initialArticles not found')
        return

    data = json.loads(match.group(1))
    today = datetime.now().strftime("%Y-%m-%d")
    existing_lastmods = load_existing_lastmods(sitemap_path)

    dup_slugs = set()
    if os.path.exists(dup_redir_path):
        try:
            with open(dup_redir_path, 'r', encoding='utf-8') as df:
                dup_slugs = set(json.load(df).keys())
        except Exception:
            pass

    noindex_slugs = {'top-5-ways-earn-money-online-2026'}
    articles_sorted = []
    for article in data:
        aid = article.get('id', '')
        if not aid or aid.startswith('blogger-') or aid in noindex_slugs or aid in dup_slugs:
            continue
        articles_sorted.append((clean_date(article.get('date', '')), article))

    articles_sorted.sort(key=lambda x: x[0], reverse=True)
    latest_article_date = articles_sorted[0][0] if articles_sorted else today
    nepal_dates = [d for d, a in articles_sorted if 'nepal' in (a.get('category', '') + ' ' + a.get('id', '')).lower()]
    latest_nepal_date = nepal_dates[0] if nepal_dates else latest_article_date

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
        '  <!-- 1. Core Hubs & 17 Interactive Engineering Tools -->',
    ]
    plain_urls = []

    for loc, rel_file, is_dynamic in CORE_AND_TOOL_ROUTES:
        if is_dynamic:
            lmod = latest_nepal_date if loc.endswith('/nepal/') else latest_article_date
        else:
            lmod = existing_lastmods.get(loc, '2026-11-23')
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{loc}</loc>')
        xml_lines.append(f'    <lastmod>{lmod}</lastmod>')
        xml_lines.append('  </url>')
        plain_urls.append(loc)

    xml_lines.append('  <!-- 2. Indexable Technical Guides & Nepal Tech Articles (Newest First) -->')

    first_party_img_count = 0
    global_seen_stock_imgs = set()
    for date, article in articles_sorted:
        aid = article['id']
        loc = f'https://imtechboss.com/{aid}/'
        plain_urls.append(loc)
        title = xml_escape(article.get('title', ''))

        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{loc}</loc>')
        xml_lines.append(f'    <lastmod>{date}</lastmod>')

        # Collect first-party embedded /images/* visuals + unique hero image (avoid repeating stock Unsplash URLs)
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
            is_first_party = hero_url.startswith('https://imtechboss.com/')
            if is_first_party or hero_url not in global_seen_stock_imgs:
                seen_imgs.add(hero_url)
                if not is_first_party:
                    global_seen_stock_imgs.add(hero_url)
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
