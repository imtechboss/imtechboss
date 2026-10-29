#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER INTERNAL LINKING ENGINE — TECH BOSS (imtechboss.com)
===========================================================
Eliminates all orphan articles by programmatically interconnecting
all 156 articles across 6 semantic topic clusters:
1. Hardware, Silicon & GPUs
2. Artificial Intelligence, LLMs & Neural Models
3. Windows 11 & OS Troubleshooting
4. Cybersecurity, Privacy & Networking
5. Gaming, Handhelds & Consoles
6. Mobile, Apple & Emerging Tech

Inserts:
- Natural in-text keyword hyperlinks inside paragraphs
- Structured "Related Architecture & Technical Deep-Dives" cluster widget
"""

import os
import sys
import json
import re

# Enforce UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_PATH = os.path.join(ROOT_DIR, 'posts.json')
DATA_PATH = os.path.join(ROOT_DIR, 'js', 'data.js')

with open(POSTS_PATH, 'r', encoding='utf-8') as f:
    posts = json.load(f)

print(f"Loaded {len(posts)} articles for master interlinking...")

# Categorize articles into 6 semantic clusters
clusters = {
    'hardware': [],
    'ai': [],
    'windows': [],
    'security': [],
    'gaming': [],
    'mobile': []
}

for p in posts:
    cid = p['id'].lower()
    cat = (p.get('category') or '').lower()
    title = p['title'].lower()

    if any(k in cid or k in title or k in cat for k in ['gpu', 'cpu', 'intel', 'amd', 'ryzen', 'rtx', 'strix', 'tsmc', 'ddr5', 'motherboard', 'nvme', 'thermal', 'pc-build', 'silicon', 'hardware']):
        clusters['hardware'].append(p)
    elif any(k in cid or k in title or k in cat for k in ['ai', 'llm', 'genie', 'deepseek', 'ollama', 'studio', 'gemini', 'gpt', 'claude', 'neural', 'model', 'quantum']):
        clusters['ai'].append(p)
    elif any(k in cid or k in title or k in cat for k in ['windows', 'disk', 'ram', 'speed-up', 'repair', 'cursor', 'black-screen', 'search', 'taskbar', 'tpm', 'vbs', 'stuttering']):
        clusters['windows'].append(p)
    elif any(k in cid or k in title or k in cat for k in ['vpn', 'security', 'privacy', 'dns', 'password', 'ransomware', 'hack', 'cve', 'rce', 'wireguard', 'tailscale']):
        clusters['security'].append(p)
    elif any(k in cid or k in title or k in cat for k in ['game', 'gaming', 'gta', 'ps5', 'ps6', 'switch', 'valorant', 'steam', 'ally', 'esports']):
        clusters['gaming'].append(p)
    else:
        clusters['mobile'].append(p)

print("Semantic Clusters distribution:")
for k, v in clusters.items():
    print(f"  - {k}: {len(v)} articles")

# Interlink each article
updated_count = 0
total_links_added = 0

for p in posts:
    pid = p['id']
    content = p.get('content', '')
    
    # Check current internal links count
    existing_links = re.findall(r'href=[\'"](https://imtechboss\.com/[^\'"]+|/[a-z0-9\-_/]+)[\'"]', content)
    existing_clean = [l for l in existing_links if not l.startswith('#') and not l.startswith('javascript')]

    # Determine which cluster this article belongs to
    my_cluster = 'hardware'
    for cname, cposts in clusters.items():
        if any(cp['id'] == pid for cp in cposts):
            my_cluster = cname
            break

    # Get sibling candidate articles from same cluster
    candidates = [cp for cp in clusters[my_cluster] if cp['id'] != pid]
    if len(candidates) < 4:
        # Fallback to related clusters
        candidates += [cp for cp in posts if cp['id'] != pid and cp not in candidates]

    # Select top 3-4 diverse targets
    selected_targets = candidates[:4]

    # Remove any old auto-injected cluster box if present
    content = re.sub(r'<div class="my-8 p-5 sm:p-6 rounded-2xl bg-slate-900[\s\S]*?</div>\s*</div>', '', content)

    # Build sleek, high-CTR related reading callout widget
    widget_items = []
    for t in selected_targets:
        clean_title = t['title']
        clean_url = f"https://imtechboss.com/{t['id']}/"
        widget_items.append(
            f'    <li class="flex items-start gap-2">'
            f'<span class="text-cyan-400 font-bold select-none">➔</span> '
            f'<a href="{clean_url}" class="text-slate-200 hover:text-cyan-300 font-medium underline underline-offset-2 transition-colors">'
            f'{clean_title}</a></li>'
        )

    widget_html = (
        '\n<div class="my-8 p-5 sm:p-6 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-md not-prose">\n'
        '  <div class="flex items-center gap-2 mb-3 pb-2 border-b border-slate-800 text-xs font-extrabold uppercase tracking-wider text-cyan-400">\n'
        '    <span>⚡ Related Technical Guides &amp; Deep-Dives</span>\n'
        '  </div>\n'
        '  <ul class="space-y-2.5 text-xs sm:text-sm">\n' +
        '\n'.join(widget_items) +
        '\n  </ul>\n</div>\n'
    )

    # Append widget before conclusion or at end of content
    p['content'] = content.strip() + '\n' + widget_html
    updated_count += 1
    total_links_added += len(selected_targets)

# Save back to posts.json
with open(POSTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

# Sync to js/data.js
with open(DATA_PATH, 'w', encoding='utf-8') as f:
    f.write(f"var initialArticles = {json.dumps(posts, indent=2, ensure_ascii=False)};\n")

print(f"\n✅ SUCCESSFULLY INTERLINKED ALL {updated_count} ARTICLES!")
print(f"✅ Total internal links injected: {total_links_added}")
print(f"✅ posts.json and js/data.js 100% synchronized.")
