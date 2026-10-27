#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STATIC SITE GENERATOR — TECH BOSS (imtechboss.com)
==================================================
Converts every article in js/data.js into a true static directory:
/<slug>/index.html with 100% pre-rendered HTML, full metadata,
OpenGraph, Twitter cards, and Schema.org JSON-LD.

This completely eliminates client-side rendering dependency for Googlebot,
AdSense crawlers, social share bots, and readers, achieving instant (0ms LCP)
page loads and 100% indexability.
"""

import os
import sys
import json
import re
import html
from datetime import datetime

# Enforce UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, 'js', 'data.js')
POST_TEMPLATE_PATH = os.path.join(ROOT_DIR, 'post.html')

def escape(val):
    if val is None:
        return ''
    return html.escape(str(val), quote=True)

def calculate_read_time(content, excerpt):
    text = re.sub(r'<[^>]+>', ' ', (content or excerpt or ''))
    words = len(text.strip().split())
    mins = max(1, round(words / 180))
    return f"{mins} min read"

def inject_in_article_ads(body_html):
    # Empty ad slots removed during AdSense site review to ensure 100% compliance
    return body_html

def generate_key_takeaways(article):
    # Support custom takeaways or summary from post object (prevents H2 duplication)
    custom_takeaways = article.get('takeaways')
    raw_excerpt = (article.get('summary') or article.get('excerpt') or '').strip()
    excerpt = raw_excerpt
    excerpt_norm = re.sub(r'\s+', ' ', raw_excerpt).strip().lower()
    takeaways = []

    if custom_takeaways:
        raw_list = custom_takeaways if isinstance(custom_takeaways, list) else str(custom_takeaways).splitlines()
        for t in raw_list:
            s_t = str(t).strip()
            if not s_t:
                continue
            norm_t = re.sub(r'<[^>]+>', '', s_t).strip().lower()
            if norm_t and norm_t != excerpt_norm and not excerpt_norm.startswith(norm_t) and not norm_t.startswith(excerpt_norm):
                takeaways.append(s_t)

    if not takeaways:
        content = article.get('content') or article.get('body', '')
        sections = re.split(r'<h2[^>]*>(.*?)</h2>', content, flags=re.IGNORECASE)

        if len(sections) > 1:
            for i in range(1, len(sections), 2):
                h2 = re.sub(r'<[^>]+>', '', sections[i]).strip()
                sec_content = sections[i+1] if i+1 < len(sections) else ''
                p_match = re.search(r'<p[^>]*>(.*?)</p>', sec_content, re.IGNORECASE)
                sent = ''
                if p_match:
                    p_text = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
                    s_split = re.split(r'(?<=[.!?])\s+', p_text)
                    if s_split and len(s_split[0]) > 25:
                        sent = s_split[0].strip()

                clean_h2 = re.sub(r'^(\d+[\.\)]|Fix \d+:?|Section \d+:?)\s*', '', h2).strip()
                norm_sent = sent.lower()
                # Only add if we have a real sentence explanation, never repeat raw H2 heading or duplicate excerpt
                if sent and clean_h2 and norm_sent != excerpt_norm and not excerpt_norm.startswith(norm_sent) and not norm_sent.startswith(excerpt_norm):
                    item = f'<strong>{clean_h2}:</strong> {sent}'
                    if item not in takeaways:
                        takeaways.append(item)
                if len(takeaways) >= 3:
                    break

        # If fewer than 2 takeaways found, extract informative sentences from body paragraphs
        if len(takeaways) < 2:
            ps = re.findall(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE)
            for p in ps:
                p_text = re.sub(r'<[^>]+>', '', p).strip()
                s_split = re.split(r'(?<=[.!?])\s+', p_text)
                for s in s_split:
                    clean_s = s.strip()
                    norm_s = clean_s.lower()
                    if len(clean_s) > 40 and norm_s != excerpt_norm and not excerpt_norm.startswith(norm_s) and not norm_s.startswith(excerpt_norm) and clean_s not in [re.sub(r'<[^>]+>', '', t) for t in takeaways]:
                        takeaways.append(clean_s)
                        if len(takeaways) >= 3:
                            break
                if len(takeaways) >= 3:
                    break

    if not takeaways and not excerpt:
        return ''

    li_items = '\n'.join([
        f'''<li class="flex items-start gap-2.5">
            <span class="w-1.5 h-1.5 rounded-full bg-blue-600 dark:bg-blue-400 mt-2 flex-shrink-0"></span>
            <span class="leading-relaxed">{pt}</span>
          </li>'''
        for pt in takeaways
    ])

    direct_summary = f'''
        <div class="text-xs sm:text-sm font-semibold text-gray-900 dark:text-white leading-relaxed {'mb-4 pb-3 border-b border-gray-100 dark:border-slate-800' if takeaways else ''}">
          <strong>Direct Summary: </strong>{escape(excerpt)}
        </div>
    ''' if excerpt else ''

    takeaways_section = f'''
      <div class="text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-2">
        Core Takeaways &amp; Findings:
      </div>
      <ul class="space-y-2 text-xs sm:text-sm text-gray-800 dark:text-gray-200 list-none pl-0 mb-0">
        {li_items}
      </ul>
    ''' if takeaways else ''

    return f'''
    <div id="aioAnswerCapsule" class="mb-8 p-5 sm:p-6 rounded-3xl bg-gradient-to-br from-blue-50/90 via-indigo-50/50 to-white dark:from-slate-800/90 dark:via-slate-850 dark:to-slate-900 border border-blue-200/80 dark:border-blue-900/50 shadow-sm not-prose">
      <div class="flex items-center justify-between gap-2 mb-3 pb-2.5 border-b border-blue-100 dark:border-slate-700/80">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-blue-600 dark:bg-blue-400 animate-pulse"></span>
          <span class="text-[11px] font-black uppercase tracking-wider text-blue-800 dark:text-blue-300">
            Tech Boss Direct Answer Capsule (AI Overview)
          </span>
        </div>
        <span class="text-[10px] text-gray-400 font-mono hidden sm:inline">GEO Verified • imtechboss.com</span>
      </div>
      {direct_summary}
      {takeaways_section}
    </div>
    '''

def generate_table_of_contents(content_html):
    if not content_html:
        return '', content_html

    headings = []
    idx = 0

    def h2_repl(m):
        nonlocal idx
        idx += 1
        attrs = m.group(1)
        inner = m.group(2)
        plain = re.sub(r'<[^>]+>', '', inner).strip()
        if not plain:
            return m.group(0)

        id_match = re.search(r'id=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if id_match:
            sec_id = id_match.group(1)
        else:
            slug = re.sub(r'[^a-z0-9]+', '-', plain.lower()).strip('-')[:48]
            sec_id = f"section-{idx}-{slug or 'heading'}"
            attrs = f'{attrs} id="{sec_id}"'

        headings.append({'id': sec_id, 'title': plain})
        return f'<h2 {attrs.strip()}>{inner}</h2>'

    updated_body = re.sub(r'<h2\b([^>]*)>([\s\S]*?)</h2>', h2_repl, content_html, flags=re.IGNORECASE)

    if len(headings) < 2:
        return '', content_html

    items = '\n'.join([
        f'''<li class="flex items-start gap-2.5">
          <span class="text-xs font-mono font-bold text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0">{i+1:02d}.</span>
          <a href="#{escape(h["id"])}" class="text-xs sm:text-sm text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors hover:underline">
            {escape(h["title"])}
          </a>
        </li>'''
        for i, h in enumerate(headings)
    ])

    toc_html = f'''
    <div class="my-6 p-4 sm:p-5 rounded-2xl bg-gray-50/90 dark:bg-slate-800/60 border border-gray-200/80 dark:border-slate-800/80 shadow-xs not-prose">
      <details open class="group">
        <summary class="flex items-center justify-between cursor-pointer font-bold text-gray-900 dark:text-gray-100 select-none list-none">
          <span class="flex items-center gap-2 text-xs sm:text-sm uppercase tracking-wider text-gray-800 dark:text-gray-200 font-extrabold">
            <span>📑</span>
            <span>In This Analysis (Table of Contents)</span>
          </span>
          <span class="text-xs text-blue-600 dark:text-blue-400 group-open:rotate-180 transition-transform duration-200">▼</span>
        </summary>
        <ol class="mt-3.5 pt-3.5 border-t border-gray-200/60 dark:border-slate-700/60 space-y-2 list-none pl-0">
          {items}
        </ol>
      </details>
    </div>
    '''
    return toc_html, updated_body

def _format_faq(faqs):
    normalized = []
    for f in faqs:
        q = f.get('q') or f.get('question') or ''
        a = f.get('a') or f.get('answer') or ''
        if q and a:
            normalized.append({'q': q, 'a': a})

    faq_html = f'''
    <div class="my-10 p-6 sm:p-7 rounded-3xl bg-gray-50/90 dark:bg-slate-800/60 border border-gray-200/80 dark:border-slate-800/80 shadow-xs not-prose">
      <div class="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200/60 dark:border-slate-700/60">
        <span class="text-base">💬</span>
        <h3 class="text-sm sm:text-base font-extrabold uppercase tracking-wider text-gray-900 dark:text-white">
          Frequently Asked Questions &amp; Technical Clarifications
        </h3>
      </div>
      <div class="space-y-3">
        {'\n'.join([
            f"""<details class="group p-4 rounded-2xl bg-white dark:bg-slate-800/80 border border-gray-200/80 dark:border-slate-700/80 transition-colors">
              <summary class="flex justify-between items-center font-bold text-xs sm:text-sm text-gray-900 dark:text-gray-100 cursor-pointer select-none">
                <span>{escape(f['q'])}</span>
                <span class="text-gray-400 group-open:rotate-180 transition-transform ml-2 text-xs flex-shrink-0">▼</span>
              </summary>
              <p class="mt-3 text-xs sm:text-sm text-gray-600 dark:text-gray-300 leading-relaxed border-t border-gray-100 dark:border-slate-700/60 pt-2.5">
                {escape(f['a'])}
              </p>
            </details>"""
            for f in normalized
        ])}
      </div>
    </div>
    '''

    schema_faqs = [
        {
            "@type": "Question",
            "name": f['q'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f['a']
            }
        }
        for f in normalized
    ]

    return faq_html, schema_faqs

def generate_faq_data(article):
    # Only render FAQs if custom, authentic, verified FAQs are authored for this specific post.
    # Programmatic synthetic fallback FAQs are completely eliminated to prevent duplicate template boilerplate (BUG-03, BUG-13).
    custom_faqs = article.get('faqs')
    if custom_faqs and isinstance(custom_faqs, list) and len(custom_faqs) > 0:
        return _format_faq(custom_faqs)
    return '', []


    # Branch 1: PC Hardware & Silicon (Check hardware first so CPUs/GPUs aren't swallowed by 'gaming')
    if any(k in cat for k in ['hardware', 'semiconductor']) or any(k in title for k in ['rtx', 'ryzen', 'intel', 'gpu', 'cpu', 'tsmc', 'radeon', 'nvidia', 'amd', 'core ultra', 'motherboard', 'ddr5', 'pcie', 'vram', 'bspdn', 'silicon']):
        if not any(k in title for k in ['playstation', 'ps6', 'ps5', 'xbox', 'nintendo', 'switch']):
            faqs = [
                {
                    "q": "How does this semiconductor or hardware architecture improve performance and efficiency?",
                    "a": "By advancing lithography nodes and implementing backside power delivery networks (BSPDN), silicon designs reduce voltage drop (IR drop), eliminate interconnect congestion, and deliver 15% to 25% lower power consumption alongside double-digit clock frequency gains."
                },
                {
                    "q": "Will this hardware advancement require new motherboard platforms or power standards?",
                    "a": "Next-generation architectures often require updated socket standards, PCIe 5.0/6.0 bandwidth pipelines, and ATX 3.1 certified power delivery to handle aggressive transient power spikes and extreme compute densities."
                },
                {
                    "q": "When will this technology reach commercial hardware availability?",
                    "a": "Advanced process nodes transition from initial foundry risk production to high-volume manufacturing within 6 to 9 months, prioritizing high-performance computing (HPC) and flagship AI accelerators before client consumer rollouts."
                }
            ]
            return _format_faq(faqs)

    # Branch 2: AI & LLMs
    if any(k in cat for k in ['frontier ai', 'quantum']) or any(k in title for k in ['deepseek', 'claude', 'gpt', 'llm', 'chatgpt', 'openai', 'gemini', 'ollama', 'mistral', 'qwen', 'llama', 'copilot', 'lm studio', 'quantum']):
        faqs = [
            {
                "q": "Can this AI model or architecture run locally on consumer hardware?",
                "a": "Quantized versions (such as 4-bit and 8-bit GGUF models) can run locally on consumer GPUs with 12GB to 24GB of VRAM using inference engines like Ollama, llama.cpp, and LM Studio."
            },
            {
                "q": "How does test-time compute reasoning improve model answers?",
                "a": "Reasoning models generate internal chain-of-thought tokens, verifying mathematical intermediate steps and backtracking when encountering logical contradictions before providing the output."
            },
            {
                "q": "Is prompt data kept private when self-hosting local models?",
                "a": "Yes. Running models on local hardware ensures that your prompts, source code, and queries remain on your private machine without transmitting telemetry to third-party cloud APIs."
            }
        ]
        return _format_faq(faqs)

    # Branch 3: Gaming & Consoles
    if any(k in cat for k in ['gaming', 'esports', 'console']) or any(k in title for k in ['playstation', 'ps6', 'ps5', 'xbox', 'switch', 'gta', 'gaming', 'gameplay', 'game pass', 'steam deck', 'fortnite', 'geforce now']):
        faqs = [
            {
                "q": "Will this console or gaming title support backward compatibility and high frame rates?",
                "a": "Modern platforms and next-generation architectures prioritize backward compatibility for legacy libraries while utilizing dynamic resolution scaling, machine learning upscaling (PSSR/FSR/DLSS), and HDMI 2.1 to achieve stable 4K 60 FPS to 120 FPS targets."
            },
            {
                "q": "What storage specifications are required for optimal loading performance?",
                "a": "DirectStorage and custom NVMe PCIe 4.0/5.0 interfaces with read bandwidths exceeding 5,500 MB/s to 7,000 MB/s are recommended to eliminate asset streaming hitches and reduce loading times to near-zero."
            },
            {
                "q": "How does hardware-accelerated machine learning upscaling improve visual fidelity?",
                "a": "Hardware-accelerated neural upscalers analyze motion vectors and temporal frame history to reconstruct sharp native-like 4K resolutions with ray tracing while significantly reducing raw GPU rendering workloads."
            }
        ]
        return _format_faq(faqs)

    # Branch 4: Mobile Tech & Smartphones
    if any(k in cat for k in ['mobile', 'smartphone']) or any(k in title for k in ['iphone', 'galaxy', 'pixel', 'snapdragon', 'ios', 'android', 'xiaomi', 'oneplus', 'smartphone', 'oxygenos', 'one ui', 'airpods', 'smartwatch']):
        faqs = [
            {
                "q": "How do on-device neural processing units (NPUs) impact smartphone battery life and privacy?",
                "a": "Dedicated NPUs execute localized machine learning models directly on the silicon with minimal thermal dissipation, preventing heavy cloud data transmission while preserving battery endurance and user data privacy."
            },
            {
                "q": "What software support lifecycle and security update timeline can users expect?",
                "a": "Modern flagship smartphones offer extended support windows ranging from 5 to 7 years of full operating system upgrades and monthly security vulnerability patches."
            },
            {
                "q": "How does high-wattage fast charging affect long-term battery cell health?",
                "a": "Advanced dual-cell architectures and intelligent thermal charge throttling protect battery health, maintaining over 80% original capacity after 800 to 1,600 complete charging cycles."
            }
        ]
        return _format_faq(faqs)

    # Branch 5: Windows OS & System Troubleshooting
    if any(k in title for k in ['windows 11', 'windows 10', 'windows', 'bsod', 'registry', 'dism', 'dpc latency', 'micro-stutter', 'sysmain', 'antimalware service']):
        faqs = [
            {
                "q": "Are these technical instructions safe to apply on Windows 11?",
                "a": "Yes. The steps detailed in this Tech Boss analysis utilize standard administrative tools and follow official operating system documentation to ensure complete stability."
            },
            {
                "q": "Does this solution require specialized third-party diagnostic software?",
                "a": "The troubleshooting steps utilize built-in administrative tools such as PowerShell, DISM, SFC, and native Windows Diagnostics."
            },
            {
                "q": "What should I do if this issue persists after applying the fix?",
                "a": "Verify hardware stability, run memory integrity diagnostics, and inspect event viewer logs for recurring kernel error codes."
            }
        ]
        return _format_faq(faqs)

    # Branch 6A: Web Hosting, Cloud & Servers
    if any(k in cat for k in ['hosting', 'cloud', 'server', 'web']) or any(k in title for k in ['hosting', 'wordpress', 'vps', 'domain', 'server', 'shared hosting', 'litespeed', 'cpanel']):
        faqs = [
            {
                "q": "Why is LiteSpeed Web Server (LSWS) preferred over Apache for WordPress hosting?",
                "a": "LiteSpeed features an event-driven architecture, native HTTP/3 QUIC support, and built-in LSCache integration, delivering up to 3x faster TTFB and handling significantly higher concurrent traffic with low CPU overhead."
            },
            {
                "q": "What server specifications should I look for in managed WordPress hosting?",
                "a": "Look for NVMe SSD storage in RAID-10 arrays, at least 1GB to 2GB dedicated RAM per PHP worker, isolated container environments (CloudLinux LVE), free SSL certificates, and automated offsite backups."
            },
            {
                "q": "How does server physical location affect website Core Web Vitals?",
                "a": "Proximity to your target demographic reduces Round Trip Time (RTT) latency, directly boosting First Contentful Paint (FCP) and Largest Contentful Paint (LCP) metrics. Pairing the origin host with an Anycast CDN further mitigates regional latency."
            }
        ]
        return _format_faq(faqs)

    # Branch 6B: Online Monetization, Digital Business & Careers
    if any(k in cat for k in ['business', 'money', 'career', 'freelance']) or any(k in title for k in ['earn money', 'freelancing', 'micro-saas', 'monetiz', 'income', 'side hustle', 'digital asset']):
        faqs = [
            {
                "q": "What technical skills offer the highest earning potential for freelancers in 2026?",
                "a": "Skills in AI model integration, prompt engineering, full-stack API workflows, modern web frameworks (Next.js/Tailwind), and cybersecurity auditing command premium rates and retainer contracts."
            },
            {
                "q": "How can digital creators and developers reliably receive international payments?",
                "a": "Global creators use multi-currency merchant platforms like Stripe, Payoneer, Wise Business, and specialized digital marketplaces that offer automated compliance and low-fee cross-border payouts."
            },
            {
                "q": "What is the recommended approach to building and scaling a micro-SaaS?",
                "a": "Identify a painful, recurring problem in a specific niche, build a lightweight MVP using modern serverless platforms, validate with early adopters before scaling, and focus on predictable subscription revenue."
            }
        ]
        return _format_faq(faqs)

    # Branch 6C: Networking, Security & Telecom
    if any(k in cat for k in ['cybersecurity', 'telecom']) or any(k in title for k in ['vpn', 'wifi', 'wi-fi', 'router', 'dns', 'wireguard', 'isp', '5g', 'telecom', 'ntc', 'ncell']):
        faqs = [
            {
                "q": "How does protocol selection (WireGuard vs. OpenVPN) impact connection speed and latency?",
                "a": "WireGuard utilizes a modern, lightweight cryptographic codebase that processes data significantly faster than legacy protocols, reducing CPU overhead, packet jitter, and handshake latency."
            },
            {
                "q": "Does using a secure VPN prevent ISP bandwidth throttling?",
                "a": "Yes. By encrypting all data packets with AES-256 or ChaCha20-Poly1305, your Internet Service Provider cannot inspect packet payloads or selectively throttle bandwidth for streaming, downloads, or gaming."
            },
            {
                "q": "How can I diagnose and resolve local network packet loss or DNS latency?",
                "a": "Flush DNS resolver caches, switch to low-latency verified recursive resolvers (such as 1.1.1.1 or 8.8.8.8), and connect via Cat 6/6e ethernet cables to eliminate 2.4GHz/5GHz radio frequency interference."
            }
        ]
        return _format_faq(faqs)

    # Branch 7: General Tech & Software Editorial Fallback
    faqs = [
        {
            "q": "How does Tech Boss verify the accuracy of its technical analyses?",
            "a": "Tech Boss adheres to strict hands-on testing protocols, cross-referencing official developer documentation, standardized industry benchmarks, and verified system telemetry before publishing."
        },
        {
            "q": "Are Tech Boss interactive tools and comparison calculators free to use?",
            "a": "Yes. All diagnostic tools, hardware versus comparison engines, and interactive calculators on imtechboss.com are 100% free with no login or subscription required."
        },
        {
            "q": "How often are guides and hardware recommendations updated on Tech Boss?",
            "a": "Our editorial team continually monitors software releases, driver updates, and market pricing, refreshing articles dynamically as new test data becomes available."
        }
    ]
    return _format_faq(faqs)

def generate_hubs_cross_promote(article):
    cat = (article.get('category') or '').lower()
    title = (article.get('title') or '').lower()
    is_hardware = 'hard' in cat or 'gam' in cat or 'gpu' in title or 'cpu' in title or 'rtx' in title or 'ryzen' in title
    comp_title = 'Hardware Benchmark Matcher' if is_hardware else 'Spec & Model Comparison'
    comp_desc = 'Compare RTX 5090, 4090, RX 7900 XTX, and Ryzen 9800X3D specs, TDP, and pricing.' if is_hardware else 'Compare processor architectures, memory bandwidth, and compute specs side-by-side.'

    return f'''
    <div class="my-10 p-6 sm:p-7 rounded-3xl bg-gradient-to-br from-gray-50 via-blue-50/30 to-indigo-50/20 dark:from-slate-900 dark:via-slate-800/40 dark:to-slate-900 border border-gray-200/90 dark:border-slate-800 shadow-sm not-prose">
      <div class="flex items-center justify-between mb-4 pb-3 border-b border-gray-200/70 dark:border-slate-800">
        <div class="flex items-center gap-2.5">
          <span class="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white flex items-center justify-center text-xs font-black shadow-sm">TB</span>
          <div>
            <h4 class="font-extrabold text-sm sm:text-base text-gray-950 dark:text-white tracking-tight">Tech Boss Interactive Hubs &amp; Live Radar</h4>
            <p class="text-[11px] text-gray-500 dark:text-gray-400">Explore free diagnostic tools, spec comparison engines, and verified hardware deals.</p>
          </div>
        </div>
        <span class="hidden sm:inline-flex px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-widest rounded-full bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300">Updated Daily</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
        <a href="/compare" class="group p-4 rounded-2xl bg-white dark:bg-slate-800/80 border border-gray-200/80 dark:border-slate-700/70 hover:border-blue-500 dark:hover:border-blue-400 hover:shadow-md transition-all flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-base">⚔️</span>
              <span class="text-[10px] font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-900/30 px-2 py-0.5 rounded-md">Versus Engine</span>
            </div>
            <strong class="block text-xs sm:text-sm font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
              {comp_title}
            </strong>
            <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1 leading-relaxed">
              {comp_desc}
            </p>
          </div>
          <span class="mt-3 text-[11px] font-bold text-blue-600 dark:text-blue-400 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
            <span>Launch Compare Hub</span>
            <span>&rarr;</span>
          </span>
        </a>

        <a href="/tools" class="group p-4 rounded-2xl bg-white dark:bg-slate-800/80 border border-gray-200/80 dark:border-slate-700/70 hover:border-blue-500 dark:hover:border-blue-400 hover:shadow-md transition-all flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-base">🛠️</span>
              <span class="text-[10px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 px-2 py-0.5 rounded-md">Diagnostic Suite</span>
            </div>
            <strong class="block text-xs sm:text-sm font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
              Interactive Tech Tools
            </strong>
            <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1 leading-relaxed">
              Bottleneck calculator, local AI VRAM sizer, hardware matching quiz, and live game checker.
            </p>
          </div>
          <span class="mt-3 text-[11px] font-bold text-blue-600 dark:text-blue-400 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
            <span>Open Tool Studio</span>
            <span>&rarr;</span>
          </span>
        </a>

        <a href="/deals" class="group p-4 rounded-2xl bg-white dark:bg-slate-800/80 border border-gray-200/80 dark:border-slate-700/70 hover:border-amber-500 dark:hover:border-amber-400 hover:shadow-md transition-all flex flex-col justify-between sm:col-span-2 lg:col-span-1">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-base">🏷️</span>
              <span class="text-[10px] font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/30 px-2 py-0.5 rounded-md">Live Price Drops</span>
            </div>
            <strong class="block text-xs sm:text-sm font-bold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
              Curated Hardware Deals
            </strong>
            <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-1 leading-relaxed">
              Price drops, flash sales, and historical lows on GPUs, CPUs, OLED displays, and NVMe drives.
            </p>
          </div>
          <span class="mt-3 text-[11px] font-bold text-amber-600 dark:text-amber-400 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
            <span>Explore Deals</span>
            <span>&rarr;</span>
          </span>
        </a>
      </div>
    </div>
    '''

def generate_author_bio(article):
    safe_author = "Binod Bhatt"
    cat = (article.get('category') or '').lower()
    title = (article.get('title') or '').lower()

    if any(k in cat for k in ['hosting', 'cloud', 'server']) or any(k in title for k in ['hosting', 'wordpress', 'vps', 'domain', 'server', 'cloud', 'cdn', 'litespeed']):
        role = "Cloud &amp; Web Infrastructure Lead"
        bio = "Founder and systems engineer at Tech Boss covering server optimization, LiteSpeed hosting architectures, TTFB latency benchmarks, and enterprise cloud infrastructure."
    elif any(k in cat for k in ['frontier ai', 'ai & technology', 'quantum', 'ai']) or any(k in title for k in ['ai', 'gpt', 'llm', 'claude', 'gemini', 'deepseek', 'model', 'ollama', 'neural']):
        role = "AI Systems &amp; Hardware Engineer"
        bio = "Founder and lead technical editor at Tech Boss, evaluating frontier reasoning models, local LLM quantization, Apple Silicon unified memory architectures, and neural inference acceleration."
    elif any(k in cat for k in ['cybersecurity', 'security', 'privacy']) or any(k in title for k in ['security', 'password', 'vpn', 'ransomware', 'malware', 'phishing', 'encryption', 'zero-day', 'cve']):
        role = "Cybersecurity &amp; Network Researcher"
        bio = "Lead technical investigator at Tech Boss specializing in cryptographic vaults, FIDO2 WebAuthn authentication, network protocol security, and operating system safeguards."
    elif any(k in cat for k in ['gaming', 'esports', 'console']) or any(k in title for k in ['gaming', 'game', 'playstation', 'ps5', 'ps6', 'xbox', 'switch', 'steam deck', 'fps', 'rtx 5090']):
        role = "Gaming Performance &amp; Silicon Analyst"
        bio = "Hardware gaming editor at Tech Boss evaluating frame pacing, DirectStorage NVMe bandwidth, neural reconstruction upscalers, and gaming silicon architectures."
    elif any(k in cat for k in ['hardware', 'semiconductor']) or any(k in title for k in ['gpu', 'cpu', 'intel', 'amd', 'ryzen', 'nvidia', 'rtx', 'tsmc', 'ddr5', 'motherboard', 'pc build']):
        role = "Lead Hardware &amp; Benchmark Engineer"
        bio = "Lead systems investigator at Tech Boss specializing in GPU/CPU silicon nodes, memory latency scaling, DDR5 timings, and high-performance computing hardware."
    else:
        role = "Founder &amp; Lead Technical Editor"
        bio = "Founder and lead technical editor at Tech Boss, delivering verified hardware benchmarks, software diagnostics, and objective technology reporting."

    return f'''
    <div class="my-10 p-5 sm:p-6 rounded-2xl bg-gray-50 dark:bg-slate-800/40 border border-gray-200 dark:border-slate-800 flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
      <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white font-extrabold text-xl shadow flex-shrink-0">
        BB
      </div>
      <div>
        <div class="flex items-center justify-center sm:justify-start gap-2 mb-1">
          <h4 class="font-extrabold text-gray-900 dark:text-white text-sm sm:text-base">Binod Bhatt</h4>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300">{role}</span>
        </div>
        <p class="text-xs text-gray-600 dark:text-gray-400 leading-relaxed mb-2">
          {bio}
        </p>
        <div class="flex items-center justify-center sm:justify-start gap-3 text-xs text-blue-600 dark:text-blue-400 font-semibold" data-nosnippet="" aria-hidden="true">
          <a href="https://binodbhatt.com.np" target="_blank" rel="author me noopener" class="hover:underline flex items-center gap-1">
            <span>🌐 Personal Site</span>
          </a>
          <span>•</span>
          <a href="https://github.com/binodbhatt" target="_blank" rel="me noopener" class="hover:underline flex items-center gap-1">
            <span>💻 GitHub</span>
          </a>
          <span>•</span>
          <a href="https://imtechboss.com/about/" class="hover:underline">About Tech Boss</a>
        </div>
      </div>
    </div>
    '''

def render_article_inner_html(article):
    safe_title = escape(article.get('title', ''))
    safe_cat = escape(article.get('category', 'Technology'))
    safe_author = 'Tech Boss'
    safe_date = escape(article.get('date', 'Recent'))
    safe_views = escape(article.get('views', '1.2K'))
    img_url = article.get('image', '')
    if img_url and not img_url.startswith('http'):
        img_url = 'https://imtechboss.com/' + img_url.lstrip('/')

    read_time = calculate_read_time(article.get('content', ''), article.get('excerpt', ''))
    body_content = article.get('content') or article.get('body', '')

    # 1. In-article Ads
    body_with_ads = inject_in_article_ads(body_content)

    # 2. ToC
    toc_html, final_body = generate_table_of_contents(body_with_ads)

    # 3. Key Takeaways
    takeaways_html = generate_key_takeaways(article)

    # 4. FAQ
    faq_html, _ = generate_faq_data(article)

    # 5. Hubs cross promote
    hubs_html = generate_hubs_cross_promote(article)
    author_bio_html = generate_author_bio(article)

    initial_likes = int(article.get('likes', 12)) if str(article.get('likes', '')).isdigit() else 12

    hero_img_block = f'''
      <div class="mb-10 rounded-2xl overflow-hidden shadow-lg bg-gray-100 dark:bg-slate-800 border border-gray-200 dark:border-slate-800 max-h-[500px]">
        <img 
          src="{escape(img_url)}" 
          alt="{safe_title}" 
          class="w-full h-full object-cover object-center"
          loading="eager"
          onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80'"
        >
      </div>
    ''' if img_url else ''

    return f'''
    <!-- Top Meta Breadcrumb -->
    <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-6 border-b border-gray-100 dark:border-slate-800 text-xs">
      <div class="flex items-center gap-2">
        <a href="/" class="text-gray-500 hover:text-blue-600 transition-colors">Home</a>
        <span class="text-gray-400">/</span>
        <span class="px-2.5 py-1 rounded-full font-bold bg-blue-50 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400">
          {safe_cat}
        </span>
      </div>
      <div class="flex items-center gap-3 text-gray-500 dark:text-gray-400" data-nosnippet="" aria-hidden="true">
        <span>📅 {safe_date}</span>
        <span>•</span>
        <span>⏱️ {read_time}</span>
      </div>
    </div>

    <!-- Article Headline -->
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-extrabold font-serif-heading text-gray-950 dark:text-white leading-[1.2] mb-6 tracking-tight">
      {safe_title}
    </h1>

    <!-- Author & Publisher Bar -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-gray-50 dark:bg-slate-800/60 border border-gray-200/70 dark:border-slate-800 mb-8">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white font-bold text-lg shadow ring-2 ring-white dark:ring-slate-700">
          BB
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h4 class="font-bold text-gray-900 dark:text-gray-100 text-sm sm:text-base">Binod Bhatt</h4>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300">Lead Technical Editor</span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400">Tech Boss • <a href="https://binodbhatt.com.np" target="_blank" rel="author me noopener" class="hover:underline text-blue-600 dark:text-blue-400">binodbhatt.com.np</a></p>
        </div>
      </div>

      <!-- Action Buttons (Protected with data-nosnippet & aria-hidden) -->
      <div class="flex items-center gap-2" data-nosnippet="" aria-hidden="true">
        <button 
          id="likeBtn" 
          class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full border text-xs font-bold transition-all bg-white dark:bg-slate-900 border-gray-200 dark:border-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800"
          title="Appreciate this story"
        >
          <span class="text-sm">🤍</span>
          <span id="likeCountDisplay">{initial_likes}</span>
        </button>

        <button 
          id="bookmarkBtn" 
          class="p-2 rounded-full border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" 
          title="Bookmark story"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
          </svg>
        </button>

        <button 
          id="copyLinkBtn" 
          class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors" 
          title="Copy link"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
          </svg>
          <span>Share</span>
        </button>
      </div>
    </div>

    <!-- Featured Hero Image -->
    {hero_img_block}

    <!-- Audio Narration Bar -->
    <div id="articleAudioBar" data-nosnippet="" aria-hidden="true" aria-label="Audio narration controls" class="mb-8 p-4 rounded-2xl bg-gradient-to-r from-blue-50/90 to-indigo-50/90 dark:from-slate-800/90 dark:to-slate-900 border border-blue-100 dark:border-slate-700/80 flex flex-wrap items-center justify-between gap-3 shadow-xs">
      <div class="flex items-center gap-3" data-nosnippet="" aria-hidden="true">
        <button id="audioPlayBtn" data-nosnippet="" aria-hidden="true" class="w-10 h-10 rounded-full bg-blue-600 hover:bg-blue-700 text-white flex items-center justify-center shadow-md active:scale-95 transition-all flex-shrink-0" title="Listen to this story" aria-label="Listen to this story">
          <svg id="playIcon" class="w-4 h-4 ml-0.5 fill-current" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          <svg id="pauseIcon" class="w-4 h-4 hidden fill-current" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
        </button>
        <div data-nosnippet="" aria-hidden="true">
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-gray-900 dark:text-white">Listen to Article</span>
            <span class="text-[9px] px-1.5 py-0.5 rounded font-mono font-bold bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300 uppercase">AI Audio</span>
          </div>
          <p id="audioStatusText" class="text-[11px] text-gray-500 dark:text-gray-400 mt-0.5">Click to play narration • ~{read_time}</p>
        </div>
      </div>
      <div class="flex items-center gap-2" data-nosnippet="" aria-hidden="true">
        <select id="audioRateSelect" data-nosnippet="" aria-hidden="true" class="text-xs font-semibold px-2.5 py-1.5 rounded-xl bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-gray-700 dark:text-gray-300 focus:outline-none">
          <option value="1">1.0x Speed</option>
          <option value="1.25">1.25x Speed</option>
          <option value="1.5">1.5x Speed</option>
        </select>
        <button id="audioStopBtn" data-nosnippet="" aria-hidden="true" class="hidden px-2.5 py-1.5 rounded-xl text-xs font-bold text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/40 transition-colors" title="Stop Audio">
          ⏹ Stop
        </button>
      </div>
    </div>

    <!-- Executive Key Takeaways Card -->
    {takeaways_html}

    <!-- In-Depth Table of Contents -->
    {toc_html}

    <!-- Rich Article Body -->
    <div class="article-body text-gray-800 dark:text-gray-200 leading-relaxed max-w-none">
      {final_body}
    </div>

    <!-- Google FAQ Accordion & People Also Ask Section -->
    {faq_html}

    <!-- Tech Boss Interactive Hubs & Live Deals Callout -->
    {hubs_html}

    <!-- Author Bio Footnote -->
    {author_bio_html}

    <!-- Comments & Discussion Area -->
    <div id="commentsSection" class="mt-12 pt-8 border-t border-gray-200 dark:border-slate-800">
      <h3 class="text-lg sm:text-xl font-bold font-sans tracking-tight mb-6 flex items-center gap-2">
        <span>💬 Reader Discussion &amp; Feedback</span>
        <span id="commentCountBadge" class="text-xs font-semibold px-2 py-0.5 rounded-full bg-gray-100 dark:bg-slate-800 text-gray-600 dark:text-gray-400">0</span>
      </h3>

      <!-- Post Comment Form -->
      <form id="postCommentForm" class="mb-8 p-4 sm:p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/50 border border-gray-200 dark:border-slate-800">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
          <input 
            type="text" 
            id="commentAuthor" 
            required 
            placeholder="Your Name / Handle" 
            class="px-3.5 py-2 text-xs rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
          <input 
            type="email" 
            id="commentEmail" 
            placeholder="Email (Optional, kept private)" 
            class="px-3.5 py-2 text-xs rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
        </div>
        <textarea 
          id="commentText" 
          rows="3" 
          required 
          placeholder="Share your thoughts, ask a question, or report a benchmark finding..." 
          class="w-full px-3.5 py-2 text-xs rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3"
        ></textarea>
        <div class="flex justify-between items-center">
          <span class="text-[11px] text-gray-500 dark:text-gray-400">Markdown supported</span>
          <button 
            type="submit" 
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors"
          >
            Post Comment
          </button>
        </div>
      </form>

      <!-- Comments List -->
      <div id="commentsList" class="space-y-3">
        <!-- Rendered via JS -->
      </div>
    </div>
    '''

def render_related_grid(article, all_articles):
    art_cat = (article.get('category') or '').lower()
    art_id = article.get('id')

    # Find articles with same category
    same_cat = [a for a in all_articles if a.get('id') != art_id and (a.get('category') or '').lower() == art_cat]
    other = [a for a in all_articles if a.get('id') != art_id and a not in same_cat]

    related = (same_cat + other)[:3]
    if not related:
        return ''

    cards = []
    for rel in related:
        safe_rel_title = escape(rel.get('title', ''))
        safe_rel_cat = escape(rel.get('category', 'General'))
        safe_rel_date = escape(rel.get('date', 'Recent'))
        img_url = rel.get('image') or "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=400&q=80"
        if not img_url.startswith('http'):
            img_url = 'https://imtechboss.com/' + img_url.lstrip('/')

        rel_href = f"/{rel.get('id')}/"
        cards.append(f'''
          <a 
            href="{rel_href}" 
            class="group flex flex-col bg-white dark:bg-slate-900 rounded-2xl overflow-hidden border border-gray-200 dark:border-slate-800 shadow-sm hover:shadow-md hover:border-blue-500/40 transition-all p-3"
          >
            <div class="aspect-[16/10] rounded-xl overflow-hidden bg-gray-100 dark:bg-slate-800 mb-3">
              <img 
                src="{escape(img_url)}" 
                alt="{safe_rel_title}" 
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                loading="lazy"
                onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=400&q=80'"
              >
            </div>
            <span class="text-[10px] font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider mb-1">
              {safe_rel_cat}
            </span>
            <h4 class="font-bold text-xs sm:text-sm text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-2 leading-snug">
              {safe_rel_title}
            </h4>
            <div class="mt-auto pt-2 text-[10px] text-gray-400 flex items-center justify-between">
              <span>{safe_rel_date}</span>
              <span class="font-semibold text-blue-600 dark:text-blue-400 group-hover:translate-x-0.5 transition-transform">Read Story &rarr;</span>
            </div>
          </a>
        ''')

    return '\n'.join(cards)

def generate_schema_json(article, canonical_url, schema_faqs):
    img = article.get('image') or 'https://imtechboss.com/og-image.png'
    if not img.startswith('http'):
        img = 'https://imtechboss.com/' + img.lstrip('/')

    date_str = article.get('date', '2026-09-24')
    # ISO date parsing
    pub_iso = "2026-09-24T00:00:00Z"
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            pub_iso = dt.strftime("%Y-%m-%dT00:00:00Z")
            break
        except ValueError:
            pass

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "@id": canonical_url + "#article",
                "isPartOf": {
                    "@type": "WebPage",
                    "@id": canonical_url
                },
                "headline": article.get('title', ''),
                "description": article.get('excerpt', ''),
                "image": [img],
                "datePublished": pub_iso,
                "dateModified": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "inLanguage": "en-US",
                "mainEntityOfPage": canonical_url,
                "author": {
                    "@type": "Person",
                    "name": "Binod Bhatt",
                    "jobTitle": "Lead Systems & Hardware Engineer",
                    "url": "https://binodbhatt.com.np",
                    "sameAs": [
                        "https://binodbhatt.com.np",
                        "https://github.com/binodbhatt"
                    ],
                    "worksFor": {
                        "@type": "Organization",
                        "name": "Tech Boss",
                        "url": "https://imtechboss.com"
                    }
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Tech Boss",
                    "url": "https://imtechboss.com",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://imtechboss.com/og-image.png"
                    }
                },
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": ["#aioAnswerCapsule", "h1"]
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": canonical_url + "#breadcrumb",
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
                        "name": article.get('category', 'Technology'),
                        "item": "https://imtechboss.com/?category=" + article.get('category', 'Technology')
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": article.get('title', ''),
                        "item": canonical_url
                    }
                ]
            },
        ]
    }
    if schema_faqs and len(schema_faqs) > 0:
        schema["@graph"].append({
            "@type": "FAQPage",
            "@id": canonical_url + "#faq",
            "mainEntity": schema_faqs
        })
    return json.dumps(schema, ensure_ascii=False)

def build_all_static():
    print("=" * 70)
    print("   BUILDING PRE-RENDERED STATIC ARTICLE DIRECTORIES (/<slug>/)")
    print("=" * 70)

    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: {DATA_PATH} not found!")
        sys.exit(1)
    if not os.path.exists(POST_TEMPLATE_PATH):
        print(f"❌ Error: {POST_TEMPLATE_PATH} not found!")
        sys.exit(1)

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if not match:
        print("❌ Error: initialArticles not found in js/data.js!")
        sys.exit(1)

    articles = json.loads(match.group(1))
    print(f"Found {len(articles)} articles to pre-render.")

    with open(POST_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    # Pre-clean base template asset paths so they are absolute root paths:
    # favicon.svg -> /favicon.svg
    # og-image.png -> /og-image.png
    # manifest.json -> /manifest.json
    # css/style.css -> /css/style.css
    # js/data.js -> /js/data.js
    # js/pages.js -> /js/pages.js
    # js/post.js -> /js/post.js
    # js/vip-drawer.js -> /js/vip-drawer.js
    clean_tpl = template
    clean_tpl = re.sub(r'href="favicon\.svg"', 'href="/favicon.svg"', clean_tpl)
    clean_tpl = re.sub(r'href="og-image\.png"', 'href="/og-image.png"', clean_tpl)
    clean_tpl = re.sub(r'href="manifest\.json"', 'href="/manifest.json"', clean_tpl)
    clean_tpl = re.sub(r'href="css/style\.css([^"]*)"', r'href="/css/style.css\1"', clean_tpl)
    clean_tpl = re.sub(r'src="js/data\.js([^"]*)"', r'src="/js/data.js\1"', clean_tpl)
    clean_tpl = re.sub(r'src="js/pages\.js([^"]*)"', r'src="/js/pages.js\1"', clean_tpl)
    clean_tpl = re.sub(r'src="js/post\.js([^"]*)"', r'src="/js/post.js\1"', clean_tpl)
    clean_tpl = re.sub(r'src="js/vip-drawer\.js([^"]*)"', r'src="/js/vip-drawer.js\1"', clean_tpl)

    # Normalize static nav links to root
    clean_tpl = re.sub(r'href="tools"', 'href="/tools"', clean_tpl)
    clean_tpl = re.sub(r'href="compare"', 'href="/compare"', clean_tpl)
    clean_tpl = re.sub(r'href="deals"', 'href="/deals"', clean_tpl)
    clean_tpl = re.sub(r'href="about"', 'href="/about"', clean_tpl)
    clean_tpl = re.sub(r'href="contact"', 'href="/contact"', clean_tpl)
    clean_tpl = re.sub(r'href="privacy"', 'href="/privacy"', clean_tpl)
    clean_tpl = re.sub(r'href="terms"', 'href="/terms"', clean_tpl)
    clean_tpl = re.sub(r'href="disclaimer"', 'href="/disclaimer"', clean_tpl)

    count = 0
    for art in articles:
        aid = art.get('id', '').strip()
        if not aid:
            continue

        canonical_url = f"https://imtechboss.com/{aid}/"
        safe_title = escape(art.get('title', ''))
        safe_desc = escape(art.get('excerpt', ''))
        art_img = art.get('image', '')
        if not art_img.startswith('http'):
            art_img = 'https://imtechboss.com/' + art_img.lstrip('/')
        safe_img = escape(art_img)

        # Generate HTML components
        article_inner = render_article_inner_html(art)
        related_grid = render_related_grid(art, articles)
        _, schema_faqs = generate_faq_data(art)
        schema_json_ld = generate_schema_json(art, canonical_url, schema_faqs)

        # Replace in template
        page_html = clean_tpl

        # Replace Title
        page_html = re.sub(r'<title id="pageTitle">.*?</title>', f'<title id="pageTitle">{safe_title} — Tech Boss</title>', page_html)
        
        # Replace Meta Description
        page_html = re.sub(r'<meta name="description" id="metaDescription" content=".*?">', f'<meta name="description" id="metaDescription" content="{safe_desc}">', page_html)

                # Replace Canonical
        page_html = re.sub(r'<link id="canonicalUrl" rel="canonical" href=".*?">', f'<link id="canonicalUrl" rel="canonical" href="{canonical_url}">', page_html)

        # Search indexing directives
        if aid.startswith('blogger-'):
            page_html = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, follow">', page_html)
        else:
            page_html = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">', page_html)

        # Replace OG Meta
        page_html = re.sub(r'<meta id="ogUrl" property="og:url" content=".*?">', f'<meta id="ogUrl" property="og:url" content="{canonical_url}">', page_html)
        page_html = re.sub(r'<meta id="ogTitle" property="og:title" content=".*?">', f'<meta id="ogTitle" property="og:title" content="{safe_title} — Tech Boss">', page_html)
        page_html = re.sub(r'<meta id="ogDescription" property="og:description" content=".*?">', f'<meta id="ogDescription" property="og:description" content="{safe_desc}">', page_html)
        page_html = re.sub(r'<meta id="ogImage" property="og:image" content=".*?">', f'<meta id="ogImage" property="og:image" content="{safe_img}">', page_html)
        page_html = re.sub(r'<meta id="ogImageSecure" property="og:image:secure_url" content=".*?">', f'<meta id="ogImageSecure" property="og:image:secure_url" content="{safe_img}">', page_html)
        page_html = re.sub(r'<link id="imgSrc" rel="image_src" href=".*?">', f'<link id="imgSrc" rel="image_src" href="{safe_img}">', page_html)

        # Replace Twitter Meta
        page_html = re.sub(r'<meta id="twUrl" name="twitter:url" content=".*?">', f'<meta id="twUrl" name="twitter:url" content="{canonical_url}">', page_html)
        page_html = re.sub(r'<meta id="twTitle" name="twitter:title" content=".*?">', f'<meta id="twTitle" name="twitter:title" content="{safe_title} — Tech Boss">', page_html)
        page_html = re.sub(r'<meta id="twDescription" name="twitter:description" content=".*?">', f'<meta id="twDescription" name="twitter:description" content="{safe_desc}">', page_html)
        page_html = re.sub(r'<meta id="twImage" name="twitter:image" content=".*?">', f'<meta id="twImage" name="twitter:image" content="{safe_img}">', page_html)

        # Inject JSON-LD Schema before </head>
        json_ld_tag = f'\n  <script id="articleJsonLd" type="application/ld+json">{schema_json_ld}</script>\n</head>'
        page_html = page_html.replace('</head>', json_ld_tag, 1)

        # Replace Article Container with Pre-rendered HTML
        art_container_pattern = r'<article id="articleContainer" class="([^"]*)">[\s\S]*?</article>'
        page_html = re.sub(art_container_pattern, lambda m: f'<article id="articleContainer" data-prerendered="true" class="{m.group(1)}">\n{article_inner}\n      </article>', page_html, count=1)

        # Replace Related Stories section
        if related_grid:
            related_sec_pattern = r'<section id="relatedSection" class="([^"]*?)hidden">'
            page_html = re.sub(related_sec_pattern, r'<section id="relatedSection" class="\1">', page_html)
            page_html = page_html.replace('<div id="relatedGrid" class="grid grid-cols-1 sm:grid-cols-3 gap-5">\n          <!-- Injected via post.js -->\n        </div>',
                                          f'<div id="relatedGrid" class="grid grid-cols-1 sm:grid-cols-3 gap-5">\n{related_grid}\n        </div>')

        # Create target directory
        post_dir = os.path.join(ROOT_DIR, aid)
        os.makedirs(post_dir, exist_ok=True)
        out_file = os.path.join(post_dir, 'index.html')

        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(page_html)

        count += 1

    print(f"✅ Successfully pre-rendered all {count} static article pages (/<slug>/index.html)!")

    # Also ensure static pages have directory index.html files so /tools/, /compare/, /deals/ load cleanly
    static_pages = ['tools', 'compare', 'deals', 'about', 'contact', 'privacy', 'terms', 'disclaimer', 'archive']
    for p in static_pages:
        src_html = os.path.join(ROOT_DIR, f"{p}.html")
        if os.path.exists(src_html):
            p_dir = os.path.join(ROOT_DIR, p)
            os.makedirs(p_dir, exist_ok=True)
            dst_html = os.path.join(p_dir, 'index.html')
            with open(src_html, 'r', encoding='utf-8') as f:
                p_content = f.read()
            # Fix relative links to root-relative
            p_content = re.sub(r'href="favicon\.svg"', 'href="/favicon.svg"', p_content)
            p_content = re.sub(r'href="css/style\.css([^"]*)"', r'href="/css/style.css\1"', p_content)
            p_content = re.sub(r'src="js/([^"]*)"', r'src="/js/\1"', p_content)
            with open(dst_html, 'w', encoding='utf-8') as f:
                f.write(p_content)
            print(f"  Created static folder: /{p}/index.html")

    # Generate standalone interactive tool sub-routes (/tools/*)
    from generate_standalone_tools import generate_standalone_tools
    generate_standalone_tools()

    # Generate static Archive directory (/archive/)
    from generate_archive import generate_archive
    generate_archive()

    # Update Homepage index.html with Pre-rendered Latest Articles
    update_homepage_prerender(articles)

    # Regenerate _worker.js with updated Edge SSR metadata
    worker_script = os.path.join(ROOT_DIR, 'scripts', 'generate_worker.py')
    if os.path.exists(worker_script):
        import subprocess
        subprocess.run([sys.executable, worker_script], cwd=ROOT_DIR, check=False)

def update_homepage_prerender(articles):
    index_path = os.path.join(ROOT_DIR, "index.html")
    if not os.path.exists(index_path) or not articles:
        return

    featured = articles[0]
    trending = articles[1:4]
    grid_posts = articles[:24]

    feat_id = escape(featured['id'])
    feat_title = escape(featured['title'])
    feat_desc = escape(featured.get('excerpt') or featured.get('summary') or '')
    feat_cat = escape(featured.get('category') or 'AI & Technology')
    feat_date = escape(featured.get('date') or 'Recent')
    feat_read = escape(featured.get('readTime') or '4 min read')
    feat_img = featured.get('image') or 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80'

    featured_html = f'''<a 
            href="/{feat_id}/" 
            class="block relative rounded-3xl overflow-hidden shadow-xl aspect-[16/9] md:aspect-[21/11] bg-slate-900 group cursor-pointer"
            data-id="{feat_id}"
          >
            <img 
              src="{feat_img}" 
              alt="{feat_title}" 
              class="zoom-img w-full h-full object-cover opacity-80 group-hover:opacity-90 group-hover:scale-105 transition-all duration-500"
              onerror="this.onerror=null; this.src=\'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80\'"
            >
            <div class="absolute inset-0 bg-gradient-to-t from-black/95 via-black/50 to-transparent flex flex-col justify-end p-6 sm:p-8 md:p-10 text-white">
              <div class="flex items-center gap-3 mb-3">
                <span class="px-3 py-1 text-xs font-bold uppercase tracking-wider rounded-full bg-blue-600 text-white shadow">
                  Featured Story
                </span>
                <span class="text-xs text-gray-300 font-medium">{feat_cat}</span>
                <span class="text-xs text-gray-400">•</span>
                <span class="text-xs text-gray-300 font-medium">{feat_read}</span>
              </div>
              <h1 class="text-xl sm:text-2xl md:text-3xl lg:text-4xl font-extrabold font-serif-heading leading-tight mb-3 group-hover:text-blue-300 transition-colors">
                {feat_title}
              </h1>
              <p class="text-xs sm:text-sm text-gray-300 max-w-2xl line-clamp-2 mb-4 leading-relaxed">
                {feat_desc}
              </p>
              <div class="flex items-center justify-between pt-2">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center ring-2 ring-white/50">
                    T
                  </div>
                  <div>
                    <p class="text-xs font-bold">Tech Boss</p>
                    <p class="text-[10px] text-gray-400">Publisher • {feat_date}</p>
                  </div>
                </div>
                <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/20 backdrop-blur-md text-xs font-semibold hover:bg-white/30 transition-colors">
                  <span>Read Story</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                  </svg>
                </span>
              </div>
            </div>
          </a>'''

    trending_items = []
    for idx, art in enumerate(trending):
        tid = escape(art['id'])
        ttitle = escape(art['title'])
        tcat = escape(art.get('category') or 'General')
        tdate = escape(art.get('date') or 'Recent')
        trending_items.append(f'''<a 
              href="/{tid}/" 
              class="group flex gap-3 p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200/70 dark:border-slate-800 hover:border-blue-500/50 transition-all cursor-pointer" 
              data-id="{tid}"
            >
              <span class="text-2xl font-black font-serif-heading text-gray-300 dark:text-slate-700 group-hover:text-blue-600 transition-colors flex-shrink-0 w-6">
                0{idx + 1}
              </span>
              <div class="flex-1">
                <span class="text-[10px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                  {tcat}
                </span>
                <h3 class="font-bold text-xs sm:text-sm text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-2 mt-0.5">
                  {ttitle}
                </h3>
                <span class="text-[10px] text-gray-400 block mt-1">Tech Boss • {tdate}</span>
              </div>
            </a>''')
    trending_html = "\n            ".join(trending_items)

    grid_items = []
    for art in grid_posts:
        gid = escape(art['id'])
        gtitle = escape(art['title'])
        gdesc = escape(art.get('excerpt') or art.get('summary') or '')
        gcat = escape(art.get('category') or 'General')
        gdate = escape(art.get('date') or 'Recent')
        gread = escape(art.get('readTime') or '4 min read')
        gimg = art.get('image') or 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80'

        grid_items.append(f'''<article class="article-card bg-white dark:bg-slate-900 rounded-2xl overflow-hidden border border-gray-200/90 dark:border-slate-800 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col group" data-id="{gid}">
              <div class="relative overflow-hidden aspect-[16/10] bg-gray-100 dark:bg-slate-800">
                <a href="/{gid}/" class="block w-full h-full cursor-pointer" aria-hidden="true" tabindex="-1">
                  <img 
                    src="{gimg}" 
                    alt="{gtitle}" 
                    loading="lazy" 
                    class="zoom-img w-full h-full object-cover"
                    onerror="this.onerror=null; this.src=\'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80\'"
                  >
                </a>
                <div class="absolute top-3 left-3 flex gap-2 pointer-events-none">
                  <span class="px-2.5 py-1 text-[11px] font-bold rounded-full bg-white/90 dark:bg-slate-900/90 text-blue-600 dark:text-blue-400 backdrop-blur-md shadow-sm">
                    {gcat}
                  </span>
                </div>
              </div>
              <div class="p-5 flex-1 flex flex-col justify-between">
                <div>
                  <div class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mb-2.5">
                    <span>{gdate}</span>
                    <span>•</span>
                    <span>{gread}</span>
                  </div>
                  <h2 class="font-bold text-base sm:text-lg text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-2 leading-snug">
                    <a href="/{gid}/">{gtitle}</a>
                  </h2>
                  <p class="text-xs text-gray-600 dark:text-gray-400 mt-2 line-clamp-2 leading-relaxed">
                    {gdesc}
                  </p>
                </div>
                <div class="mt-4 pt-4 border-t border-gray-100 dark:border-slate-800 flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <div class="w-6 h-6 rounded-full bg-blue-600 text-white text-[10px] font-bold flex items-center justify-center">
                      T
                    </div>
                    <span class="text-xs text-gray-600 dark:text-gray-300 font-medium">Tech Boss</span>
                  </div>
                  <a href="/{gid}/" class="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1">
                    <span>Read</span>
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                  </a>
                </div>
              </div>
            </article>''')
    grid_html = "\n          ".join(grid_items)

    with open(index_path, 'r', encoding='utf-8') as f:
        idx_content = f.read()

    feat_pattern = r'(<div class="lg:col-span-8 group cursor-pointer" id="featuredArticleContainer">)[\s\S]*?(</div>\s*<!-- Trending Highlights Side Column -->)'
    idx_content = re.sub(feat_pattern, r'\1\n          ' + featured_html + r'\n        \2', idx_content)

    trend_pattern = r'(<div id="trendingListContainer" class="space-y-4">)[\s\S]*?(</div>\s*</div>\s*</div>\s*</section>)'
    idx_content = re.sub(trend_pattern, r'\1\n            ' + trending_html + r'\n          \2', idx_content)

    grid_pattern = r'(<div id="articlesGrid" class="grid grid-cols-1 sm:grid-cols-2 gap-6">)[\s\S]*?(</div>\s*<!-- Empty State -->)'
    idx_content = re.sub(grid_pattern, r'\1\n          ' + grid_html + r'\n        \2', idx_content)

    badge_pattern = r'<span id="spotlightCountBadge">.*?</span>'
    idx_content = re.sub(badge_pattern, f'<span id="spotlightCountBadge">{len(articles)} stories indexed</span>', idx_content)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(idx_content)
    print("  Successfully updated Homepage index.html with static pre-rendered articles!")


if __name__ == '__main__':
    build_all_static()
