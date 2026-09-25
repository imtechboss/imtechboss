import os, json, re, html

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'js', 'data.js')
STORIES_DIR = os.path.join(BASE_DIR, 'stories')

os.makedirs(STORIES_DIR, exist_ok=True)

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);', content)
if not match:
    print("Error: Could not find initialArticles in data.js")
    exit(1)

articles = json.loads(match.group(1))

# Pick top 12 latest/flagship articles for Web Stories
top_articles = articles[:12]

AMP_BOILERPLATE = """<style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>"""

STORY_CUSTOM_CSS = """
amp-story {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #fff;
}
.cover-overlay {
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.4) 0%, rgba(15, 23, 42, 0.95) 85%);
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
.content-overlay {
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.85) 0%, rgba(10, 15, 29, 0.98) 100%);
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.tag-badge {
  display: inline-block;
  align-self: flex-start;
  background: #2563eb;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 4px 10px;
  border-radius: 9999px;
  margin-bottom: 12px;
}
.story-title {
  font-size: 24px;
  font-weight: 800;
  line-height: 1.25;
  color: #ffffff;
  margin-bottom: 12px;
}
.story-lead {
  font-size: 14px;
  line-height: 1.5;
  color: #cbd5e1;
  margin-bottom: 16px;
}
.key-point-card {
  background: rgba(30, 41, 59, 0.85);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 14px;
}
.key-point-title {
  font-size: 15px;
  font-weight: 700;
  color: #60a5fa;
  margin-bottom: 6px;
}
.key-point-desc {
  font-size: 13px;
  line-height: 1.45;
  color: #e2e8f0;
}
.cta-button {
  display: block;
  text-align: center;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  padding: 14px 20px;
  border-radius: 10px;
  text-decoration: none;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
  margin-top: 16px;
}
"""

def extract_paragraphs(html_text):
    clean = re.sub(r'<div[\s\S]*?</div>', '', html_text)
    clean = re.sub(r'<table[\s\S]*?</table>', '', clean)
    clean = re.sub(r'<pre[\s\S]*?</pre>', '', clean)
    items = re.findall(r'<p>(.*?)</p>', clean, re.DOTALL)
    result = []
    for item in items:
        # Strip internal tags
        t = re.sub(r'<.*?>', '', item).strip()
        t = html.unescape(t)
        if len(t) > 60:
            result.append(t)
    return result

def extract_headings(html_text):
    headings = re.findall(r'<h[23]>(.*?)</h[23]>', html_text)
    return [re.sub(r'<.*?>', '', h).strip() for h in headings]

generated_stories = []

for art in top_articles:
    slug = art['id']
    title = art['title']
    safe_title = html.escape(title)
    excerpt = art.get('excerpt', '')
    safe_excerpt = html.escape(excerpt)
    category = art.get('category', 'Tech')
    safe_category = html.escape(category)
    image_url = art['image']
    # Guarantee 1200px crop format
    if 'images.unsplash.com' in image_url and 'w=' in image_url:
        image_url = re.sub(r'w=\d+', 'w=1200', image_url)
    
    canonical_url = f"https://imtechboss.com/post.html?id={slug}"
    story_url = f"https://imtechboss.com/stories/{slug}.html"
    
    paragraphs = extract_paragraphs(art.get('content', ''))
    headings = extract_headings(art.get('content', ''))
    
    p1 = paragraphs[0] if len(paragraphs) > 0 else excerpt
    p2 = paragraphs[1] if len(paragraphs) > 1 else (paragraphs[0] if len(paragraphs) > 0 else "")
    p3 = paragraphs[2] if len(paragraphs) > 2 else ""
    
    h1 = headings[0] if len(headings) > 0 else "Key Architecture & Details"
    h2 = headings[1] if len(headings) > 1 else "Performance & Benchmark Insights"
    h3 = headings[2] if len(headings) > 2 else "Tech Boss Verdict"

    story_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{safe_title} | Tech Boss Web Stories</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <script async custom-element="amp-story" src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>
  {AMP_BOILERPLATE}
  <style amp-custom>
    {STORY_CUSTOM_CSS}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": "{safe_title}",
    "description": "{safe_excerpt}",
    "image": ["{image_url}"],
    "datePublished": "{art.get('date', '2026-09-25')}",
    "author": {{
      "@type": "Person",
      "name": "Tech Boss",
      "url": "https://imtechboss.com"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Tech Boss",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://imtechboss.com/icons/icon-192.png"
      }}
    }}
  }}
  </script>
</head>
<body>
  <amp-story standalone
    title="{safe_title}"
    publisher="Tech Boss"
    publisher-logo-src="https://imtechboss.com/icons/icon-192.png"
    poster-portrait-src="{image_url}">

    <!-- Page 1: Cover Page -->
    <amp-story-page id="cover-page">
      <amp-story-grid-layer template="fill">
        <amp-img src="{image_url}" width="720" height="1280" layout="responsive" alt="{safe_title}"></amp-img>
      </amp-story-grid-layer>
      <amp-story-grid-layer template="vertical" class="cover-overlay">
        <span class="tag-badge">{safe_category}</span>
        <h1 class="story-title">{safe_title}</h1>
        <p class="story-lead">{safe_excerpt}</p>
      </amp-story-grid-layer>
    </amp-story-page>

    <!-- Page 2: Key Breakthrough -->
    <amp-story-page id="breakthrough-page">
      <amp-story-grid-layer template="fill">
        <amp-img src="{image_url}" width="720" height="1280" layout="responsive" alt="{safe_title}"></amp-img>
      </amp-story-grid-layer>
      <amp-story-grid-layer template="vertical" class="content-overlay">
        <div>
          <span class="tag-badge">Deep Dive</span>
          <h2 class="story-title">{html.escape(h1)}</h2>
        </div>
        <div class="key-point-card">
          <div class="key-point-title">Core Diagnostic Finding</div>
          <div class="key-point-desc">{html.escape(p1[:300])}...</div>
        </div>
        <div class="key-point-card">
          <div class="key-point-title">System Impact</div>
          <div class="key-point-desc">{html.escape(p2[:280]) if p2 else safe_excerpt}...</div>
        </div>
      </amp-story-grid-layer>
    </amp-story-page>

    <!-- Page 3: Benchmark & Engineering Verdict -->
    <amp-story-page id="benchmark-page">
      <amp-story-grid-layer template="fill">
        <amp-img src="{image_url}" width="720" height="1280" layout="responsive" alt="{safe_title}"></amp-img>
      </amp-story-grid-layer>
      <amp-story-grid-layer template="vertical" class="content-overlay">
        <div>
          <span class="tag-badge">Analysis</span>
          <h2 class="story-title">{html.escape(h2)}</h2>
        </div>
        <div class="key-point-card">
          <div class="key-point-title">{html.escape(h3)}</div>
          <div class="key-point-desc">{html.escape(p3[:320]) if p3 else html.escape(p1[:320])}...</div>
        </div>
        <div>
          <a href="{canonical_url}" class="cta-button" target="_blank" rel="noopener">
            Read Full Article &amp; Benchmarks &rarr;
          </a>
        </div>
      </amp-story-grid-layer>
      <amp-story-page-outlink layout="nodisplay">
        <a href="{canonical_url}">Read Full In-Depth Guide on Tech Boss</a>
      </amp-story-page-outlink>
    </amp-story-page>

  </amp-story>
</body>
</html>
"""
    file_path = os.path.join(STORIES_DIR, f"{slug}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(story_html)
    
    generated_stories.append({
        'slug': slug,
        'title': title,
        'excerpt': excerpt,
        'category': category,
        'image': image_url,
        'date': art.get('date', '2026-09-25'),
        'story_file': f"stories/{slug}.html"
    })
    print(f"Generated Web Story: stories/{slug}.html")

# Create stories/index.html (Web Stories Hub page for users and crawlers)
story_cards_html = ""
for s in generated_stories:
    story_cards_html += f"""
    <a href="/stories/{s['slug']}.html" class="group block bg-slate-900/80 rounded-2xl overflow-hidden border border-slate-800 hover:border-blue-500 transition-all duration-300 transform hover:-translate-y-1 shadow-lg">
      <div class="relative h-64 overflow-hidden">
        <img src="{s['image']}" alt="{html.escape(s['title'])}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent"></div>
        <span class="absolute top-3 left-3 bg-blue-600 text-white text-xs font-bold px-2.5 py-1 rounded-full uppercase tracking-wider">{html.escape(s['category'])}</span>
      </div>
      <div class="p-5">
        <h3 class="text-white font-bold text-base line-clamp-2 group-hover:text-blue-400 transition-colors mb-2">{html.escape(s['title'])}</h3>
        <p class="text-slate-400 text-xs line-clamp-2 mb-4">{html.escape(s['excerpt'])}</p>
        <div class="flex items-center justify-between text-xs text-blue-400 font-semibold">
          <span>Tap to View Story</span>
          <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        </div>
      </div>
    </a>
    """

hub_html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Visual Web Stories | Tech Boss</title>
  <meta name="description" content="Immersive, fast-loading visual Web Stories breaking down the latest PC hardware benchmarks, Windows troubleshooting guides, and AI breakthroughs.">
  <link rel="canonical" href="https://imtechboss.com/stories/">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            primary: '#2563eb',
          }}
        }}
      }}
    }}
  </script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased">
  <!-- Header -->
  <header class="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2 text-xl font-black text-white tracking-tight">
        <span class="text-blue-500">TECH</span>BOSS
      </a>
      <div class="flex items-center gap-4 text-sm font-semibold">
        <a href="/" class="text-slate-300 hover:text-white transition">Home</a>
        <a href="/tools.html" class="text-slate-300 hover:text-white transition">Tools</a>
        <a href="/stories/" class="text-blue-400 font-bold">Web Stories</a>
      </div>
    </div>
  </header>

  <!-- Hero -->
  <main class="max-w-6xl mx-auto px-4 py-12">
    <div class="text-center max-w-2xl mx-auto mb-12">
      <span class="bg-blue-600/20 text-blue-400 text-xs font-bold px-3 py-1.5 rounded-full uppercase tracking-wider border border-blue-500/30">Google Web Stories</span>
      <h1 class="text-3xl sm:text-5xl font-extrabold text-white mt-4 mb-4 tracking-tight">Visual Tech Stories</h1>
      <p class="text-slate-400 text-sm sm:text-base leading-relaxed">Swipe through visual breakdowns of modern GPU benchmarks, hardware engineering diagnostics, and Windows optimization guides.</p>
    </div>

    <!-- Stories Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {story_cards_html}
    </div>
  </main>

  <footer class="border-t border-slate-800 py-8 text-center text-xs text-slate-500 mt-16">
    <p>&copy; 2026 Tech Boss. All rights reserved.</p>
    <div class="mt-2 space-x-4">
      <a href="/privacy.html" class="hover:underline">Privacy Policy</a>
      <a href="/about.html" class="hover:underline">About</a>
      <a href="/contact.html" class="hover:underline">Contact</a>
    </div>
  </footer>
</body>
</html>
"""

with open(os.path.join(STORIES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(hub_html)

print("Created stories/index.html hub page.")
print(f"Total Web Stories generated: {len(generated_stories)}")
