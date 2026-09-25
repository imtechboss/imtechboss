import os, json, re, html, urllib.parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'js', 'data.js')
PINS_DIR = os.path.join(BASE_DIR, 'pins')

os.makedirs(PINS_DIR, exist_ok=True)

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);', content)
if not match:
    print("Error: Could not find initialArticles in data.js")
    exit(1)

articles = json.loads(match.group(1))

# Select top 15 flagship articles for Pinterest Pins
top_articles = articles[:15]

def clean_html_tags(text):
    clean = re.sub(r'<[^>]+>', '', text)
    return html.unescape(clean).strip()

def extract_bullets(art):
    content = art.get('content', '')
    lis = re.findall(r'<li>(.*?)</li>', content, re.DOTALL)
    if lis:
        return [clean_html_tags(l)[:120] for l in lis[:4]]
    ps = re.findall(r'<p>(.*?)</p>', content, re.DOTALL)
    if ps:
        return [clean_html_tags(p)[:110] + '...' for p in ps[:3]]
    return [art.get('excerpt', '')]

pin_cards = []

for art in top_articles:
    slug = art['id']
    title = art['title']
    excerpt = art.get('excerpt', '')
    category = art.get('category', 'Tech')
    img = art.get('image', 'https://imtechboss.com/og-image.png')
    if 'images.unsplash.com' in img:
        img = re.sub(r'w=\d+', 'w=1200', img)
    
    article_url = f"https://imtechboss.com/post.html?id={slug}"
    bullets = extract_bullets(art)
    
    # Pinterest hashtags
    tags = [t.lower().replace(' ', '').replace('-', '') for t in art.get('tags', ['tech', 'gaming', 'pcbuild'])]
    hashtags = " ".join([f"#{t}" for t in tags[:6]])
    pin_desc = f"{title}. {excerpt} Read the complete technical benchmarks & guide on Tech Boss! {hashtags} #techboss #pcgaming #hardware"
    
    # Official 1-Click Pinterest Pin Create URL
    encoded_url = urllib.parse.quote(article_url)
    encoded_img = urllib.parse.quote(img)
    encoded_desc = urllib.parse.quote(pin_desc)
    pin_share_url = f"https://pinterest.com/pin/create/button/?url={encoded_url}&media={encoded_img}&description={encoded_desc}"
    
    pin_cards.append({
        'slug': slug,
        'title': title,
        'excerpt': excerpt,
        'category': category,
        'image': img,
        'bullets': bullets,
        'share_url': pin_share_url,
        'article_url': article_url,
        'hashtags': hashtags
    })

cards_html = ""
for p in pin_cards:
    bullets_html = "".join([f"<li class='flex items-start gap-2 text-xs text-slate-300'><span class='text-blue-400 font-bold'>✓</span><span>{html.escape(b)}</span></li>" for b in p['bullets']])
    cards_html += f"""
    <div class="bg-slate-900/90 rounded-3xl overflow-hidden border border-slate-800 shadow-xl flex flex-col justify-between group hover:border-red-500/50 transition-all duration-300">
      <!-- 2:3 Vertical Pin Preview -->
      <div class="relative overflow-hidden aspect-[2/3]">
        <img src="{p['image']}" alt="{html.escape(p['title'])}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/60 to-transparent"></div>
        
        <div class="absolute top-4 left-4 right-4 flex items-center justify-between">
          <span class="bg-red-600 text-white text-[11px] font-black uppercase px-3 py-1 rounded-full tracking-wider shadow">PINTEREST PIN</span>
          <span class="bg-black/60 backdrop-blur text-white text-[11px] font-bold px-2.5 py-1 rounded-full">{html.escape(p['category'])}</span>
        </div>

        <div class="absolute bottom-4 left-4 right-4">
          <span class="text-blue-400 font-mono text-[10px] uppercase font-bold tracking-widest block mb-1">TECH BOSS BENCHMARKS</span>
          <h3 class="text-white font-extrabold text-base sm:text-lg leading-snug line-clamp-3 mb-3">{html.escape(p['title'])}</h3>
          <ul class="space-y-1.5 mb-2 hidden sm:block">
            {bullets_html}
          </ul>
        </div>
      </div>

      <!-- Action Footer -->
      <div class="p-4 bg-slate-950 border-t border-slate-800/80 flex flex-col gap-2.5">
        <a href="{p['share_url']}" target="_blank" rel="noopener noreferrer" class="w-full py-2.5 px-4 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-md hover:shadow-red-600/30 transition-all active:scale-95">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0a12 12 0 0 0-4.37 23.17c-.07-.63-.13-1.6.03-2.29.14-.61.94-3.99.94-3.99s-.24-.48-.24-1.19c0-1.12.65-1.95 1.45-1.95.69 0 1.02.51 1.02 1.13 0 .69-.44 1.72-.67 2.68-.19.8.4 1.45 1.18 1.45 1.42 0 2.51-1.5 2.51-3.66 0-1.91-1.38-3.25-3.34-3.25-2.44 0-3.87 1.83-3.87 3.72 0 .74.28 1.53.64 1.96.07.08.08.16.06.25-.07.28-.22.88-.25 1-.04.16-.13.2-.3.12-1.12-.52-1.82-2.15-1.82-3.46 0-2.82 2.05-5.41 5.91-5.41 3.1 0 5.52 2.21 5.52 5.17 0 3.08-1.94 5.56-4.64 5.56-.91 0-1.76-.47-2.05-1.03l-.56 2.13c-.2.78-.75 1.75-1.12 2.34A12 12 0 1 0 12 0z"/></svg>
          <span>Save to Pinterest (1-Click)</span>
        </a>
        <a href="{p['article_url']}" target="_blank" class="text-center text-xs text-slate-400 hover:text-white transition-colors">
          View Original Article &rarr;
        </a>
      </div>
    </div>
    """

dashboard_html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pinterest Pins &amp; Infographics Kit | Tech Boss</title>
  <meta name="description" content="1-Click Pinterest Pin creator and visual infographics kit for Tech Boss hardware guides and benchmarks.">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased">
  <header class="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2 text-xl font-black text-white tracking-tight">
        <span class="text-red-500">PINTEREST</span>HUB
      </a>
      <div class="flex items-center gap-4 text-xs font-semibold">
        <a href="/" class="text-slate-300 hover:text-white transition">Home</a>
        <a href="/tools.html" class="text-slate-300 hover:text-white transition">Tools</a>
        <a href="/stories/" class="text-slate-300 hover:text-white transition">Web Stories</a>
      </div>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-4 py-12">
    <div class="text-center max-w-2xl mx-auto mb-12">
      <span class="bg-red-600/20 text-red-400 text-xs font-bold px-3 py-1.5 rounded-full uppercase tracking-wider border border-red-500/30">Pinterest Traffic Engine</span>
      <h1 class="text-3xl sm:text-5xl font-extrabold text-white mt-4 mb-4 tracking-tight">1-Click Pinterest Pins</h1>
      <p class="text-slate-400 text-sm sm:text-base leading-relaxed">
        Click <strong class="text-red-400">Save to Pinterest</strong> on any card below to launch Pinterest with optimal high-res 1200px images, titles, and SEO hashtags pre-filled!
      </p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {cards_html}
    </div>
  </main>

  <footer class="border-t border-slate-800 py-8 text-center text-xs text-slate-500 mt-16">
    <p>&copy; 2026 Tech Boss. All rights reserved.</p>
  </footer>
</body>
</html>
"""

with open(os.path.join(PINS_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(dashboard_html)

print("Generated Pinterest dashboard: pins/index.html")
print(f"Total Pinterest cards prepared: {len(pin_cards)}")
