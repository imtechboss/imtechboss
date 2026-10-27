#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENERATE STATIC ARTICLE ARCHIVE DIRECTORY — TECH BOSS (imtechboss.com)
======================================================================
Pre-renders all 148+ articles into a static HTML Directory / Archive:
- Root: archive.html
- Directory: /archive/index.html
Eliminates crawl depth limits and orphan pages by providing direct static links
to every single published post, grouped into 6 authoritative topical clusters.
"""

import os
import sys
import json
import html
import re
from datetime import datetime

# Enforce UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_PATH = os.path.join(ROOT_DIR, 'posts.json')

def escape(val):
    if val is None:
        return ''
    return html.escape(str(val), quote=True)

def map_to_cluster(cat):
    c = (cat or '').lower()
    if any(k in c for k in ['ai', 'frontier', 'llm', 'deepseek', 'gpt', 'model', 'machine learning']):
        return 'Artificial Intelligence & Local LLMs'
    elif any(k in c for k in ['hardware', 'silicon', 'gpu', 'cpu', 'semiconductor', 'components', 'computing']):
        return 'PC Hardware, GPUs & Next-Gen Silicon'
    elif any(k in c for k in ['cybersecurity', 'security', 'privacy', 'exploit', 'vpn']):
        return 'Cybersecurity, Privacy & Network Defense'
    elif any(k in c for k in ['gaming', 'esports', 'console', 'game']):
        return 'Gaming Hardware, Consoles & Esports'
    elif any(k in c for k in ['software', 'guide', 'windows', 'tool', 'programming', 'dev', 'cloud']):
        return 'Windows OS & Software Optimization Guides'
    else:
        return 'Mobile Technology, Gadgets & Future Tech'

CLUSTER_METADATA = {
    'Artificial Intelligence & Local LLMs': {
        'icon': '🧠',
        'color': 'blue',
        'desc': 'Frontier reasoning architectures, local LLM deployment guides (Ollama, LM Studio), Apple Silicon MLX performance, and private offline inference.'
    },
    'PC Hardware, GPUs & Next-Gen Silicon': {
        'icon': '⚡',
        'color': 'indigo',
        'desc': 'Desktop GPU/CPU architecture breakdowns, power delivery analysis (ATX 3.1, 12V-2x6), memory bandwidth thermals, and independent hardware benchmarks.'
    },
    'Windows OS & Software Optimization Guides': {
        'icon': '🛠️',
        'color': 'emerald',
        'desc': 'In-depth Windows 11 kernel diagnostics, memory leak resolutions, DPC latency tuning, telemetry eradication, and system performance walkthroughs.'
    },
    'Cybersecurity, Privacy & Network Defense': {
        'icon': '🛡️',
        'color': 'purple',
        'desc': 'Zero-day vulnerability tracking, enterprise firmware mitigations, zero-knowledge encryption protocols, and verified firewall / VPN configurations.'
    },
    'Gaming Hardware, Consoles & Esports': {
        'icon': '🎮',
        'color': 'rose',
        'desc': 'Frame-rate pacing analysis, DirectStorage SSD benchmarks, PlayStation 6 / next-gen console silicon projections, and competitive input latency.'
    },
    'Mobile Technology, Gadgets & Future Tech': {
        'icon': '📱',
        'color': 'amber',
        'desc': 'Mobile SoC microarchitectures, battery chemistry innovations, satellite communications, and emerging consumer computing form factors.'
    }
}

def generate_archive():
    with open(POSTS_PATH, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    total_articles = len(articles)
    clusters = {name: [] for name in CLUSTER_METADATA.keys()}

    for a in articles:
        cluster_name = map_to_cluster(a.get('category'))
        if cluster_name in clusters:
            clusters[cluster_name].append(a)
        else:
            clusters['Mobile Technology, Gadgets & Future Tech'].append(a)

    # Build Schema JSON-LD
    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": "https://imtechboss.com/archive/#webpage",
                "url": "https://imtechboss.com/archive/",
                "name": f"Article Archive & Complete Topic Directory ({total_articles}+ Stories) — Tech Boss",
                "description": f"Browse our full directory of {total_articles}+ hardware benchmarks, local AI tutorials, Windows troubleshooting manuals, and cybersecurity audits.",
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": "https://imtechboss.com/#website",
                    "name": "Tech Boss",
                    "url": "https://imtechboss.com/"
                },
                "about": {
                    "@type": "Thing",
                    "name": "Computer Hardware, Artificial Intelligence, and Software Engineering"
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": "https://imtechboss.com/archive/#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://imtechboss.com/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Article Archive",
                        "item": "https://imtechboss.com/archive/"
                    }
                ]
            }
        ]
    }
    schema_json = json.dumps(schema_data, ensure_ascii=False, indent=2)

    # Render cluster sections HTML
    clusters_html = []
    cluster_order = [
        'Artificial Intelligence & Local LLMs',
        'PC Hardware, GPUs & Next-Gen Silicon',
        'Windows OS & Software Optimization Guides',
        'Cybersecurity, Privacy & Network Defense',
        'Gaming Hardware, Consoles & Esports',
        'Mobile Technology, Gadgets & Future Tech'
    ]

    for cl_name in cluster_order:
        cl_posts = clusters[cl_name]
        cl_meta = CLUSTER_METADATA[cl_name]
        cl_slug = re.sub(r'[^a-z0-9]+', '-', cl_name.lower()).strip('-')

        cards_html = []
        for post in cl_posts:
            pid = escape(post['id'])
            title = escape(post['title'])
            excerpt = escape(post.get('excerpt') or post.get('summary') or '')
            cat = escape(post.get('category') or 'Tech')
            date = escape(post.get('date') or 'Recent')
            read_time = escape(post.get('readTime') or '5 min read')
            img = post.get('image') or 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80'

            cards_html.append(f'''
            <article class="archive-card group bg-white dark:bg-slate-900 rounded-2xl border border-gray-200/80 dark:border-slate-800 p-5 shadow-sm hover:shadow-md hover:border-blue-500/50 transition-all flex flex-col justify-between" data-title="{title.lower()}" data-category="{cat.lower()}">
              <div>
                <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 mb-2.5">
                  <span class="px-2.5 py-0.5 rounded-full font-bold text-[11px] bg-blue-50 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 border border-blue-200/50 dark:border-blue-800/50">
                    {cat}
                  </span>
                  <span>{read_time}</span>
                </div>
                <h3 class="font-bold text-base sm:text-lg text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-2 leading-snug">
                  <a href="/{pid}/" class="hover:underline focus:outline-none">
                    {title}
                  </a>
                </h3>
                <p class="text-xs sm:text-sm text-gray-600 dark:text-gray-400 mt-2 line-clamp-2 leading-relaxed">
                  {excerpt}
                </p>
              </div>
              <div class="mt-4 pt-4 border-t border-gray-100 dark:border-slate-800/80 flex items-center justify-between text-xs">
                <span class="text-gray-500 dark:text-gray-400 font-medium">Tech Boss &bull; {date}</span>
                <a href="/{pid}/" class="inline-flex items-center gap-1 font-bold text-blue-600 dark:text-blue-400 hover:underline">
                  <span>Read Guide</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </a>
              </div>
            </article>
            ''')

        rendered_cards = "\n".join(cards_html)
        clusters_html.append(f'''
        <section id="{cl_slug}" class="mb-14 scroll-mt-24 cluster-section">
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 mb-6 pb-4 border-b border-gray-200 dark:border-slate-800">
            <div>
              <div class="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400 mb-1">
                <span>{cl_meta['icon']}</span>
                <span>Topical Cluster</span>
              </div>
              <h2 class="text-2xl sm:text-3xl font-extrabold text-gray-950 dark:text-white tracking-tight">
                {cl_name}
              </h2>
              <p class="text-xs sm:text-sm text-gray-600 dark:text-gray-400 max-w-2xl mt-1 leading-relaxed">
                {cl_meta['desc']}
              </p>
            </div>
            <div class="text-xs font-bold px-3 py-1.5 rounded-full bg-gray-100 dark:bg-slate-800 text-gray-700 dark:text-gray-300 w-max">
              {len(cl_posts)} Articles
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {rendered_cards}
          </div>
        </section>
        ''')

    all_clusters_rendered = "\n".join(clusters_html)

    archive_html = f'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <!-- Google tag (gtag.js) - Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-HQDRHTFW7Q"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-HQDRHTFW7Q');
  </script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Article Archive &amp; Complete Tech Directory — Tech Boss</title>
  <meta name="description" content="Browse our complete chronological index of {total_articles}+ hardware benchmarks, local AI tutorials, Windows troubleshooting manuals, and cybersecurity audits.">
  <link rel="canonical" href="https://imtechboss.com/archive/">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <!-- Open Graph -->
  <meta property="og:title" content="Article Archive &amp; Complete Tech Directory — Tech Boss">
  <meta property="og:description" content="Explore {total_articles}+ technical deep-dives, hardware teardowns, local AI setups, and optimization guides.">
  <meta property="og:image" content="https://imtechboss.com/og-image.png">
  <meta property="og:url" content="https://imtechboss.com/archive/">
  <meta property="og:type" content="website">
  <link rel="alternate" type="application/rss+xml" title="Tech Boss RSS Feed" href="https://imtechboss.com/feed.xml">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <!-- Google AdSense -->
  <meta name="google-adsense-account" content="ca-pub-1043419685176632">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1043419685176632" crossorigin="anonymous"></script>

  <!-- Pure Compiled CSS -->
  <link rel="stylesheet" href="/css/styles.min.css?v=1.0">
  <script>
    try {{
      const savedTheme = localStorage.getItem("pulse_theme");
      const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      if (savedTheme === "dark" || (!savedTheme && systemDark)) {{
        document.documentElement.classList.add("dark");
      }} else {{
        document.documentElement.classList.remove("dark");
      }}
    }} catch (e) {{}}
  </script>
  
  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body class="bg-gray-50 text-gray-900 dark:bg-slate-950 dark:text-gray-100 min-h-screen flex flex-col font-sans transition-colors duration-200">

  <!-- Header -->
  <header class="border-b border-gray-200 dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 backdrop-blur sticky top-0 z-40">
    <div class="max-w-6xl mx-auto px-4 py-3.5 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2.5 group">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white font-extrabold text-base shadow-sm group-hover:scale-105 transition-transform">
          TB
        </div>
        <div class="flex flex-col">
          <span class="text-base font-extrabold tracking-tight text-gray-950 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
            Tech Boss
          </span>
          <span class="text-[10px] font-semibold uppercase tracking-wider text-blue-600 dark:text-blue-400">
            Article Archive &amp; Directory
          </span>
        </div>
      </a>

      <nav class="flex items-center gap-2 sm:gap-4 text-xs font-semibold overflow-x-auto whitespace-nowrap">
        <a href="/" class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Home</a>
        <a href="/tools/" class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Tools</a>
        <a href="/compare/" class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Compare</a>
        <a href="/deals/" class="text-amber-600 dark:text-amber-400 hover:text-amber-500 font-semibold transition-colors">Deals</a>
        <a href="/archive/" class="text-blue-600 dark:text-blue-400 font-bold border-b-2 border-blue-600 pb-0.5">Archive</a>
        <a href="/stories/" class="hidden sm:inline text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 font-semibold transition-colors">Stories</a>
        <a href="/about/" class="hidden sm:inline text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">About</a>
        <a href="/contact/" class="hidden sm:inline text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Contact</a>

        <button 
          id="themeToggleBtn"
          class="p-2 rounded-full text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors ml-1"
          title="Toggle Dark / Light Mode"
          aria-label="Toggle Dark / Light Mode"
        >
          <svg id="sunIcon" class="w-4 h-4 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          <svg id="moonIcon" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
        </button>
      </nav>
    </div>
  </header>

  <!-- Hero Section -->
  <main class="flex-1 max-w-6xl mx-auto px-4 py-8 sm:py-12 w-full">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mb-6" aria-label="Breadcrumb">
      <a href="/" class="hover:text-blue-600 dark:hover:text-blue-400">Home</a>
      <span>/</span>
      <span class="text-gray-900 dark:text-gray-100 font-semibold" aria-current="page">Article Archive</span>
    </nav>

    <div class="text-center max-w-3xl mx-auto mb-10">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 text-xs font-bold uppercase tracking-wider mb-4 border border-blue-200 dark:border-blue-800">
        📚 Complete Topic Directory
      </div>
      <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-gray-950 dark:text-white mb-3">
        Tech Boss Article Archive
      </h1>
      <p class="text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed">
        Full directory of all {total_articles}+ peer-reviewed hardware benchmarks, deep reasoning AI guides, Windows optimization manuals, and security audits published on Tech Boss.
      </p>

      <!-- Instant Live Filter Box -->
      <div class="mt-8 max-w-xl mx-auto">
        <div class="relative">
          <input 
            type="text" 
            id="archiveSearchInput" 
            placeholder="Filter {total_articles} articles by topic, GPU, model, or tool..." 
            class="w-full px-5 py-3 pl-12 rounded-2xl bg-white dark:bg-slate-900 border border-gray-300 dark:border-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
          >
          <svg class="w-5 h-5 absolute left-4 top-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        </div>
      </div>

      <!-- Quick Cluster Jump Links -->
      <div class="flex flex-wrap items-center justify-center gap-2 mt-5 text-xs">
        <a href="#artificial-intelligence-local-llms" class="px-3 py-1.5 rounded-full bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 hover:border-blue-500 text-gray-700 dark:text-gray-300 transition-all font-medium">🧠 AI &amp; LLMs</a>
        <a href="#pc-hardware-gpus-next-gen-silicon" class="px-3 py-1.5 rounded-full bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 hover:border-blue-500 text-gray-700 dark:text-gray-300 transition-all font-medium">⚡ PC Hardware &amp; GPUs</a>
        <a href="#windows-os-software-optimization-guides" class="px-3 py-1.5 rounded-full bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 hover:border-blue-500 text-gray-700 dark:text-gray-300 transition-all font-medium">🛠️ Windows &amp; Software</a>
        <a href="#cybersecurity-privacy-network-defense" class="px-3 py-1.5 rounded-full bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 hover:border-blue-500 text-gray-700 dark:text-gray-300 transition-all font-medium">🛡️ Cybersecurity</a>
        <a href="#gaming-hardware-consoles-esports" class="px-3 py-1.5 rounded-full bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 hover:border-blue-500 text-gray-700 dark:text-gray-300 transition-all font-medium">🎮 Gaming</a>
        <a href="#mobile-technology-gadgets-future-tech" class="px-3 py-1.5 rounded-full bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 hover:border-blue-500 text-gray-700 dark:text-gray-300 transition-all font-medium">📱 Mobile &amp; Gadgets</a>
      </div>
    </div>

    <!-- Cluster Sections -->
    <div id="clustersContainer">
      {all_clusters_rendered}
    </div>

    <!-- No Results Feedback Box -->
    <div id="noResultsBox" class="hidden text-center py-12">
      <div class="text-4xl mb-3">🔍</div>
      <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100">No matching articles found</h3>
      <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Try searching for keywords like "RTX", "Windows 11", "Ollama", or "RAM".</p>
    </div>
  </main>

  <!-- Footer -->
  <footer class="bg-white dark:bg-slate-900 border-t border-gray-200 dark:border-slate-800 mt-16 transition-colors duration-200">
    <div class="max-w-6xl mx-auto px-4 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        <div class="md:col-span-2">
          <div class="flex items-center gap-2 mb-3">
            <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-extrabold text-sm">TB</div>
            <span class="text-lg font-extrabold text-gray-900 dark:text-white">Tech Boss</span>
          </div>
          <p class="text-xs text-gray-600 dark:text-gray-400 leading-relaxed max-w-sm mb-4">
            Independent technology journalism, hardware architecture benchmarking, and systems diagnostics. Every article is peer-analyzed for precision.
          </p>
          <div class="text-xs text-gray-500 dark:text-gray-400">
            Founded &amp; edited by <span class="font-bold text-gray-700 dark:text-gray-300">Binod Bhatt</span>.
          </div>
        </div>
        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-gray-900 dark:text-gray-100 mb-3">Resources &amp; Hubs</h4>
          <ul class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
            <li><a href="/tools/" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Tech Tools Suite</a></li>
            <li><a href="/compare/" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Versus Comparison Engine</a></li>
            <li><a href="/deals/" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Curated Tech Deals</a></li>
            <li><a href="/archive/" class="text-blue-600 dark:text-blue-400 font-bold hover:underline">Complete Topic Directory</a></li>
            <li><a href="/stories/" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Visual Web Stories</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-gray-900 dark:text-gray-100 mb-3">Company &amp; Legal</h4>
          <ul class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
            <li><a href="/about/" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors">About Tech Boss</a></li>
            <li><a href="/contact/" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Contact Editorial Team</a></li>
            <li><a href="/privacy/" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Privacy Policy</a></li>
            <li><a href="/terms/" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Terms of Service</a></li>
            <li><a href="/disclaimer/" class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Editorial Disclaimer</a></li>
          </ul>
        </div>
      </div>
      <div class="pt-8 border-t border-gray-100 dark:border-slate-800 text-center text-xs text-gray-500 dark:text-gray-400">
        &copy; 2026 Tech Boss (imtechboss.com). All rights reserved.
      </div>
    </div>
  </footer>

  <!-- Instant Search Script -->
  <script>
    const searchInput = document.getElementById('archiveSearchInput');
    const cards = document.querySelectorAll('.archive-card');
    const clusterSections = document.querySelectorAll('.cluster-section');
    const noResultsBox = document.getElementById('noResultsBox');

    if (searchInput) {{
      searchInput.addEventListener('input', (e) => {{
        const term = e.target.value.toLowerCase().trim();
        let visibleCount = 0;

        cards.forEach(card => {{
          const title = card.getAttribute('data-title') || '';
          const cat = card.getAttribute('data-category') || '';
          if (!term || title.includes(term) || cat.includes(term)) {{
            card.classList.remove('hidden');
            visibleCount++;
          }} else {{
            card.classList.add('hidden');
          }}
        }});

        clusterSections.forEach(sec => {{
          const visibleInSec = sec.querySelectorAll('.archive-card:not(.hidden)').length;
          if (visibleInSec === 0 && term) {{
            sec.classList.add('hidden');
          }} else {{
            sec.classList.remove('hidden');
          }}
        }});

        if (visibleCount === 0 && term) {{
          noResultsBox.classList.remove('hidden');
        }} else {{
          noResultsBox.classList.add('hidden');
        }}
      }});
    }}

    // Theme toggle
    const themeBtn = document.getElementById('themeToggleBtn');
    const sunIcon = document.getElementById('sunIcon');
    const moonIcon = document.getElementById('moonIcon');

    function syncIcons() {{
      if (document.documentElement.classList.contains('dark')) {{
        sunIcon.classList.remove('hidden');
        moonIcon.classList.add('hidden');
      }} else {{
        sunIcon.classList.add('hidden');
        moonIcon.classList.remove('hidden');
      }}
    }}
    syncIcons();

    if (themeBtn) {{
      themeBtn.addEventListener('click', () => {{
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('pulse_theme', isDark ? 'dark' : 'light');
        syncIcons();
      }});
    }}
  </script>
</body>
</html>
'''

    # Save to archive.html
    archive_file = os.path.join(ROOT_DIR, 'archive.html')
    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(archive_html)

    # Save to archive/index.html
    archive_dir = os.path.join(ROOT_DIR, 'archive')
    os.makedirs(archive_dir, exist_ok=True)
    archive_index_file = os.path.join(archive_dir, 'index.html')
    with open(archive_index_file, 'w', encoding='utf-8') as f:
        f.write(archive_html)

    print(f"Successfully generated /archive/index.html and archive.html with all {total_articles} articles pre-rendered across 6 topical clusters!")

if __name__ == '__main__':
    generate_archive()
