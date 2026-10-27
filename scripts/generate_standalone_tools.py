#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STANDALONE TOOLS GENERATOR — TECH BOSS (imtechboss.com)
======================================================
Splits the bundled /tools suite into 6 high-ranking, dedicated sub-routes:
  1. /tools/pc-bottleneck-calculator/
  2. /tools/llm-vram-calculator/
  3. /tools/can-my-pc-run-it/
  4. /tools/ai-prompt-studio/
  5. /tools/developer-cheat-sheets/
  6. /tools/gpu-matcher-quiz/

Each standalone tool features:
  - Dedicated title tag optimized for non-branded intent (55-65 chars)
  - Focused meta description
  - Clean canonical URL: https://imtechboss.com/tools/{slug}/
  - Dedicated H1 & Direct Answer Capsule
  - Schema.org SoftwareApplication JSON-LD
  - Breadcrumbs navigation (Home > Tools > {Tool})
  - Related Tools navigation cluster
"""

import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_HTML_PATH = os.path.join(ROOT_DIR, 'tools.html')
JS_DIR = os.path.join(ROOT_DIR, 'js')

tools_config = [
    {
        "id": "bottleneckTool",
        "slug": "pc-bottleneck-calculator",
        "title": "PC Bottleneck Calculator 2026 — CPU & GPU Gaming Resolution Check | Tech Boss",
        "meta_desc": "Calculate CPU and GPU hardware bottlenecks across 1080p, 1440p, and 4K gaming resolutions. Check real-time FPS impact and hardware pairing recommendations.",
        "h1": "PC Bottleneck & Gaming Resolution Calculator (2026)",
        "capsule_title": "Direct Hardware Verdict:",
        "capsule_text": "A hardware bottleneck occurs when one PC component limits the maximum throughput of another. At 1080p, gaming performance is heavily CPU-bound. At 1440p and 4K, the workload shifts almost entirely to GPU compute and VRAM bandwidth. Bottleneck percentages below 10% represent ideal component synergy.",
        "app_category": "UtilitiesApplication",
        "name": "Tech Boss PC Bottleneck Calculator",
        "icon": "⚡",
        "badge": "Hardware Diagnostic",
        "guide_title": "Understanding PC Bottlenecks & Hardware Synergy in 2026",
        "guide_html": """
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8 text-sm">
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">🎯 Bottleneck Percentage Thresholds</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li><strong class="text-emerald-500">0% – 5% (Optimal Balance):</strong> Excellent component pairing. Neither CPU nor GPU restricts framerates.</li>
              <li><strong class="text-blue-500">5% – 10% (Minor Bottleneck):</strong> Normal operational variation. Unlikely to cause noticeable frame stutter.</li>
              <li><strong class="text-amber-500">10% – 20% (Noticeable Bottleneck):</strong> One component is visibly constraining peak performance in specific titles.</li>
              <li><strong class="text-rose-500">&gt; 20% (Severe Bottleneck):</strong> Significant hardware imbalance. Upgrading the limiting component unlocks massive performance.</li>
            </ul>
          </div>
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">🖥️ Resolution Scaling Physics</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li><strong>1080p (FHD):</strong> The GPU processes 2.07 million pixels per frame. High frame rates place intense load on CPU instruction queues and single-core clocks.</li>
              <li><strong>1440p (QHD):</strong> At 3.68 million pixels, the system reaches the optimal balance point between CPU instruction dispatch and GPU shader execution.</li>
              <li><strong>4K (UHD):</strong> At 8.29 million pixels, the GPU memory bus and rasterization units dictate over 90% of frame time limits.</li>
            </ul>
          </div>
        </div>
        """
    },
    {
        "id": "aiVramTool",
        "slug": "llm-vram-calculator",
        "title": "Local AI & LLM VRAM Sizer 2026 — GGUF, Quantization & GPU Memory Calculator | Tech Boss",
        "meta_desc": "Calculate exact GPU VRAM requirements for 7B, 14B, 32B, and 70B local LLMs. Compare Q4_K_M vs Q8_0 GGUF quantization, context cache sizes, and Ollama hardware requirements.",
        "h1": "Local AI & LLM VRAM Sizer (2026 Edition)",
        "capsule_title": "Local LLM Memory Sizing Rule:",
        "capsule_text": "Total VRAM consumption equals Model Weights plus KV Context Cache plus CUDA Runtime Overhead (~1.2GB). Running a 7B model at Q4_K_M requires approximately 5.8GB VRAM, while a 70B model requires at least 42GB VRAM. Never allocate 100% of physical VRAM to model weights—leave 2GB to 4GB for context cache to avoid severe CPU offloading stalls.",
        "app_category": "DeveloperApplication",
        "name": "Tech Boss Local LLM VRAM Sizer",
        "icon": "🧠",
        "badge": "AI & Ollama Sizing",
        "guide_title": "How to Calculate VRAM for Local Inference (GGUF, Quantization & Context)",
        "guide_html": """
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8 text-sm">
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">📊 Quantization Tradeoffs</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li><strong>Q4_K_M (4-bit Medium):</strong> The industry sweet spot. Retains 98.5% of full 16-bit model intelligence while reducing memory footprint by over 65%.</li>
              <li><strong>Q8_0 (8-bit Quantized):</strong> Near-lossless precision for complex coding and mathematical reasoning, requiring roughly double the VRAM of 4-bit weights.</li>
              <li><strong>FP16 / BF16 (Uncompressed):</strong> Full precision weights. Demands 2 bytes per parameter (e.g., 14GB for a 7B model, 140GB for a 70B model).</li>
            </ul>
          </div>
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">💡 Context Window Memory Math</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li><strong>4,096 Tokens (Standard):</strong> Adds roughly 500MB to 1GB to active GPU memory.</li>
              <li><strong>16,384 Tokens (Extended):</strong> Adds 2GB to 4GB of KV cache depending on attention head architecture (GQA vs MHA).</li>
              <li><strong>32,768+ Tokens (Long Context):</strong> Requires 6GB to 12GB of dedicated memory just for context memory tokens.</li>
            </ul>
          </div>
        </div>
        """
    },
    {
        "id": "gameCheckerTool",
        "slug": "can-my-pc-run-it",
        "title": "Can My PC Run It? 2026 — Live PC Game System Requirements & FPS Checker | Tech Boss",
        "meta_desc": "Check if your PC meets minimum and recommended system requirements for GTA 6, Cyberpunk 2077, Black Myth: Wukong, and CS2. Live hardware specs and FPS estimator.",
        "h1": "Can My PC Run It? Live Game Requirements Checker (2026)",
        "capsule_title": "Direct Game Compatibility Verdict:",
        "capsule_text": "Modern 2026 AAA PC titles mandate DirectX 12 Ultimate, DirectStorage NVMe SSDs, and a minimum of 8GB to 12GB VRAM for 1080p High settings. Ray tracing and high-refresh 1440p require at least 16GB VRAM and DLSS 3.5 or FSR 3.1 neural reconstruction to sustain 60+ FPS.",
        "app_category": "GameApplication",
        "name": "Tech Boss Can My PC Run It Checker",
        "icon": "🎮",
        "badge": "Gaming Performance",
        "guide_title": "PC Gaming Hardware Requirements & Minimum Specs Explained",
        "guide_html": """
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8 text-sm">
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">🕹️ Modern System Bottlenecks</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li><strong>8GB VRAM Cliff:</strong> Games like Cyberpunk 2077, Hogwarts Legacy, and GTA 6 experience severe stuttering on 8GB cards at 1440p due to VRAM overflow into system RAM.</li>
              <li><strong>DirectStorage SSD Requirement:</strong> Running modern open-world games on mechanical hard drives (HDDs) causes massive texture pop-in and audio sync failures.</li>
            </ul>
          </div>
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">🚀 Upscaling & Frame Generation</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li><strong>DLSS 3.5 / FSR 3.1:</strong> Renders at 67% internal resolution while reconstructing sharp 1440p/4K visuals, boosting frame rates by up to 60%.</li>
              <li><strong>Reflex & Anti-Lag:</strong> Crucial low-latency features that reduce frame buffering lag when GPU utilization hits 99%.</li>
            </ul>
          </div>
        </div>
        """
    },
    {
        "id": "promptTool",
        "slug": "ai-prompt-studio",
        "title": "AI Prompt Engineering Studio — Free System Prompt Generator & Optimizer | Tech Boss",
        "meta_desc": "Free AI prompt engineering tool for Claude, ChatGPT, and DeepSeek. Generate structured system prompts, specify persona constraints, and export Markdown templates.",
        "h1": "AI Prompt Engineering Studio",
        "capsule_title": "Prompt Engineering Architecture:",
        "capsule_text": "High-performance prompts follow four structural pillars: Persona & Role definition, Explicit Task Context, Guardrails & Negative Constraints, and Structured Output Formatting. Clear constraints prevent hallucinations and lower token consumption by up to 40%.",
        "app_category": "DesignApplication",
        "name": "Tech Boss AI Prompt Engineering Studio",
        "icon": "✨",
        "badge": "Prompt Studio",
        "guide_title": "Best Practices for Prompt Engineering with Claude, ChatGPT & DeepSeek",
        "guide_html": """
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8 text-sm">
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">📝 The 4-Part Prompt Structure</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li><strong>1. Persona:</strong> Assign domain expertise (e.g., Senior Systems Architect, Staff Security Engineer).</li>
              <li><strong>2. Context:</strong> Provide background parameters, target audience, and architectural constraints.</li>
              <li><strong>3. Guardrails:</strong> Define what the model must NOT do (e.g., no conversational pleasantries, no speculative claims).</li>
              <li><strong>4. Output Format:</strong> Request Markdown tables, code blocks, or JSON schemas.</li>
            </ul>
          </div>
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">⚡ Reasoning Model Tuning</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li><strong>DeepSeek R1 & OpenAI o3:</strong> Do not force few-shot examples on reasoning models; allow them to generate self-verification chains of thought.</li>
              <li><strong>Temperature:</strong> Use 0.0 to 0.2 for coding and deterministic math; use 0.6 to 0.8 for creative writing and brainstorming.</li>
            </ul>
          </div>
        </div>
        """
    },
    {
        "id": "cheatsheetTool",
        "slug": "developer-cheat-sheets",
        "title": "Developer & Linux Command Cheat Sheets — Searchable Docker, Git & Bash Reference | Tech Boss",
        "meta_desc": "Searchable quick-reference cheat sheet for Linux bash commands, Docker containers, Git workflows, and Windows PowerShell diagnostics.",
        "h1": "Developer & Systems Command Cheat Sheets",
        "capsule_title": "Developer Quick-Reference:",
        "capsule_text": "Instant searchable command-line cheatsheets for systems engineers, DevOps developers, and Linux administrators. Filter by category or search by task to copy production-ready syntax in one click.",
        "app_category": "DeveloperApplication",
        "name": "Tech Boss Developer & Command Cheat Sheets",
        "icon": "💻",
        "badge": "DevOps & CLI",
        "guide_title": "Mastering Systems Administration & Essential CLI Commands",
        "guide_html": """
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8 text-sm">
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">🐧 Linux & Server Administration</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li>Use <code>htop</code> and <code>journalctl -xe</code> to diagnose system load and failed systemd services.</li>
              <li>Inspect network sockets with <code>ss -tulpn</code> to identify port conflicts and open daemons.</li>
            </ul>
          </div>
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">🐳 Docker & Git Best Practices</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li>Clean dangling images and volumes with <code>docker system prune -af --volumes</code>.</li>
              <li>Inspect branch topology cleanly with <code>git log --oneline --graph --decorate</code>.</li>
            </ul>
          </div>
        </div>
        """
    },
    {
        "id": "gpuMatcherTool",
        "slug": "gpu-matcher-quiz",
        "title": "2026 GPU Matcher Quiz — Find the Best Graphics Card for Your Budget & Workload | Tech Boss",
        "meta_desc": "Interactive graphics card selector quiz. Match your budget ($300 to $1,500+), resolution, and workload (Gaming, Local AI, Video Editing) with the ideal GPU.",
        "h1": "2026 GPU & Hardware Matcher Quiz",
        "capsule_title": "GPU Buying Strategy in 2026:",
        "capsule_text": "Selecting the right GPU depends primarily on memory bandwidth, VRAM buffer capacity, and target display resolution. For pure 1080p gaming, 8GB to 12GB is sufficient. For 1440p gaming and local AI inference (DeepSeek/Ollama), 16GB is the mandatory baseline. For 4K gaming and 70B parameter models, 24GB is essential.",
        "app_category": "UtilityApplication",
        "name": "Tech Boss GPU Matcher Quiz",
        "icon": "🎯",
        "badge": "Hardware Matcher",
        "guide_title": "GPU Buying Guide: VRAM, Resolution & Workload Synergy",
        "guide_html": """
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8 text-sm">
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">🎮 Gaming Tier Breakdown</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li><strong>Budget ($250 – $350):</strong> RTX 4060 / RX 7600 XT — High-refresh 1080p esports and AAA medium settings.</li>
              <li><strong>Midrange ($500 – $650):</strong> RTX 5070 / RX 7800 XT — Flawless 1440p ultra gaming with high framerates.</li>
              <li><strong>Enthusiast ($800 – $1,200+):</strong> RTX 5080 / RTX 4090 — Uncompromising 4K gaming with full ray tracing.</li>
            </ul>
          </div>
          <div class="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800">
            <h3 class="font-bold text-base text-gray-900 dark:text-white mb-2">🧠 Local AI Workload Demands</h3>
            <ul class="space-y-2 text-gray-600 dark:text-gray-300 text-xs">
              <li><strong>Local LLMs:</strong> Prioritize raw VRAM capacity over GPU core clocks. A used 24GB RTX 3090 frequently outperforms a faster 12GB RTX 5070 because it fits larger parameter models.</li>
            </ul>
          </div>
        </div>
        """
    }
]

def generate_standalone_tools():
    with open(TOOLS_HTML_PATH, 'r', encoding='utf-8') as f:
        tools_html = f.read()

    # Extract all section blocks
    section_matches = re.findall(r'(<section[^>]*id="([^"]+)"[^>]*>.*?</section>)', tools_html, re.DOTALL)
    sections_by_id = {s_id: s_full for s_full, s_id in section_matches}

    # Extract the main script from tools.html and guard listeners
    scripts = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', tools_html, re.DOTALL)
    raw_js = scripts[-1]

    # Guard all event listeners so missing elements on standalone pages never throw errors
    guarded_js = raw_js
    guarded_listeners = [
        ('calcBtn.addEventListener', 'if (calcBtn) calcBtn.addEventListener'),
        ('genPromptBtn.addEventListener', 'if (genPromptBtn) genPromptBtn.addEventListener'),
        ('copyPromptBtn.addEventListener', 'if (copyPromptBtn) copyPromptBtn.addEventListener'),
        ('cheatList.addEventListener', 'if (cheatList) cheatList.addEventListener'),
        ('cheatSearch.addEventListener', 'if (cheatSearch) cheatSearch.addEventListener'),
        ('findGpuBtn.addEventListener', 'if (findGpuBtn) findGpuBtn.addEventListener'),
        ('canRunBtn.addEventListener', 'if (canRunBtn) canRunBtn.addEventListener'),
        ('calcLlmBtn.addEventListener', 'if (calcLlmBtn) calcLlmBtn.addEventListener'),
        ('copyCmdBtn.addEventListener', 'if (copyCmdBtn) copyCmdBtn.addEventListener'),
        ('toolsForm.addEventListener', 'if (toolsForm) toolsForm.addEventListener'),
        ('copyToolEmbedBtn.addEventListener', 'if (copyToolEmbedBtn) copyToolEmbedBtn.addEventListener'),
    ]
    for target, repl in guarded_listeners:
        guarded_js = guarded_js.replace(target, repl)

    # Save guarded js/tools.js
    tools_js_path = os.path.join(JS_DIR, 'tools.js')
    with open(tools_js_path, 'w', encoding='utf-8') as f:
        f.write(guarded_js)
    print(f"✅ Generated modular js/tools.js ({len(guarded_js)} bytes)")

    # Build each standalone tool page
    for cfg in tools_config:
        s_id = cfg["id"]
        slug = cfg["slug"]
        s_content = sections_by_id.get(s_id, "")
        if not s_content:
            print(f"❌ Section {s_id} not found in tools.html!")
            continue

        # In standalone page, remove class="tool-section hidden" and make it visible
        s_content_clean = re.sub(r'class="tool-section hidden"', 'class="tool-section"', s_content)

        canonical_url = f"https://imtechboss.com/tools/{slug}/"

        # Build Related Tools Links
        other_tools_html = ""
        for other in tools_config:
            if other["slug"] == slug:
                continue
            other_tools_html += f"""
            <a href="/tools/{other['slug']}/" class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 hover:border-blue-500 hover:shadow-md transition-all flex items-center gap-3 group">
              <span class="text-2xl">{other['icon']}</span>
              <div>
                <h4 class="font-bold text-xs sm:text-sm text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{other['h1']}</h4>
                <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-0.5 line-clamp-1">{other['badge']}</p>
              </div>
            </a>
            """

        page_html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
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
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <title>{cfg['title']}</title>
  <meta name="description" content="{cfg['meta_desc']}">
  <link rel="canonical" href="{canonical_url}">
  <link rel="alternate" type="application/rss+xml" title="Tech Boss RSS Feed" href="https://imtechboss.com/feed.xml">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Tech Boss">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{cfg['title']}">
  <meta property="og:description" content="{cfg['meta_desc']}">
  <meta property="og:image" content="https://imtechboss.com/og-image.png">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@imtechboss">
  <meta name="twitter:title" content="{cfg['title']}">
  <meta name="twitter:description" content="{cfg['meta_desc']}">
  <meta name="twitter:image" content="https://imtechboss.com/og-image.png">

  <!-- Google Fonts: Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <!-- Google AdSense Account Verification -->
  <meta name="google-adsense-account" content="ca-pub-1043419685176632">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1043419685176632" crossorigin="anonymous"></script>

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
          }}
        }}
      }}
    }}
  </script>
  <script>
    try {{
      const savedTheme = localStorage.getItem("pulse_theme");
      const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      if (savedTheme === "dark" || (!savedTheme && systemDark)) {{
        document.documentElement.classList.add("dark");
      }}
    }} catch (e) {{}}
  </script>
  <link rel="stylesheet" href="/css/style.css?v=7.5">

  <!-- Schema.org SoftwareApplication JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "SoftwareApplication",
        "@id": "{canonical_url}#software",
        "name": "{cfg['name']}",
        "applicationCategory": "{cfg['app_category']}",
        "operatingSystem": "All (Web Browser)",
        "url": "{canonical_url}",
        "description": "{cfg['meta_desc']}",
        "offers": {{
          "@type": "Offer",
          "price": "0.00",
          "priceCurrency": "USD"
        }},
        "publisher": {{
          "@type": "Organization",
          "name": "Tech Boss",
          "url": "https://imtechboss.com"
        }},
        "author": {{
          "@type": "Person",
          "name": "Binod Bhatt",
          "url": "https://binodbhatt.com.np",
          "jobTitle": "Lead Systems & Hardware Engineer"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "@id": "{canonical_url}#breadcrumb",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://imtechboss.com/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Tech Tools",
            "item": "https://imtechboss.com/tools/"
          }},
          {{
            "@type": "ListItem",
            "position": 3,
            "name": "{cfg['h1']}",
            "item": "{canonical_url}"
          }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body class="bg-gray-50 dark:bg-slate-950 text-gray-900 dark:text-gray-100 min-h-screen flex flex-col justify-between font-sans transition-colors duration-200">

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
            Interactive Tools Suite
          </span>
        </div>
      </a>

      <nav class="flex items-center gap-2 sm:gap-4 text-xs font-semibold overflow-x-auto whitespace-nowrap">
        <a href="/" class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Home</a>
        <a href="/tools/" class="text-blue-600 dark:text-blue-400 font-bold">Tech Tools</a>
        <a href="/compare/" class="text-rose-600 dark:text-rose-400 hover:text-rose-500 font-semibold transition-colors">Compare</a>
        <a href="/deals/" class="text-amber-600 dark:text-amber-400 hover:text-amber-500 font-semibold transition-colors">Deals</a>
        <a href="/about/" class="hidden sm:inline text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">About</a>
        <a href="/contact/" class="hidden sm:inline text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Contact</a>

        <button 
          id="themeToggleBtn"
          class="p-2 rounded-full text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors ml-1"
          title="Toggle Dark / Light Mode"
          aria-label="Toggle theme"
          data-nosnippet=""
        >
          <span id="sunIcon" class="hidden">☀️</span>
          <span id="moonIcon">🌙</span>
        </button>
      </nav>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-4xl mx-auto px-4 py-8 flex-1 w-full">
    
    <!-- Breadcrumbs -->
    <nav class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mb-6" aria-label="Breadcrumb">
      <a href="/" class="hover:text-blue-600 transition-colors">Home</a>
      <span>/</span>
      <a href="/tools/" class="hover:text-blue-600 transition-colors">Tools</a>
      <span>/</span>
      <span class="text-blue-600 dark:text-blue-400 font-semibold truncate">{cfg['h1']}</span>
    </nav>

    <!-- Page Title & Direct Answer Capsule (Prime GEO / AI Search Target) -->
    <div class="mb-8 text-center sm:text-left">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 mb-3">
        <span>{cfg['icon']}</span>
        <span>{cfg['badge']}</span>
      </div>
      <h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold text-gray-950 dark:text-white tracking-tight mb-4">
        {cfg['h1']}
      </h1>
      
      <!-- Direct Answer Capsule for AI Overviews & Featured Snippets -->
      <div id="aioAnswerCapsule" class="p-4 sm:p-5 rounded-2xl bg-blue-50/80 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900/60 text-xs sm:text-sm text-gray-700 dark:text-gray-300 leading-relaxed shadow-xs">
        <strong class="text-blue-800 dark:text-blue-300 font-bold block mb-1">⚡ {cfg['capsule_title']}</strong>
        {cfg['capsule_text']}
      </div>
    </div>

    <!-- The Interactive Tool Component -->
    <div class="mb-12">
      {s_content_clean}
    </div>

    <!-- Comprehensive Engineering Guide & Technical Documentation -->
    <section class="border-t border-gray-200 dark:border-slate-800 pt-8 mb-12">
      <h2 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-4">
        {cfg['guide_title']}
      </h2>
      {cfg['guide_html']}
    </section>

    <!-- Related Interactive Tools Hub Cluster -->
    <section class="border-t border-gray-200 dark:border-slate-800 pt-8 mb-8">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-bold text-base sm:text-lg text-gray-900 dark:text-white">Explore More Free Interactive Tools</h3>
        <a href="/tools/" class="text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline">View All 6 Tools &rarr;</a>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {other_tools_html}
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer class="border-t border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 mt-12 py-8 text-xs text-gray-500 dark:text-gray-400">
    <div class="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-2">
        <span class="font-bold text-gray-800 dark:text-gray-200">Tech Boss</span>
        <span>&bull;</span>
        <span>Independent Hardware &amp; AI Benchmarks</span>
      </div>
      <div class="flex items-center gap-4">
        <a href="/tools/" class="hover:text-blue-600 transition-colors">Tools Directory</a>
        <a href="/about/" class="hover:text-blue-600 transition-colors">About</a>
        <a href="/privacy/" class="hover:text-blue-600 transition-colors">Privacy Policy</a>
        <a href="/terms/" class="hover:text-blue-600 transition-colors">Terms of Service</a>
        <a href="/contact/" class="hover:text-blue-600 transition-colors">Contact</a>
      </div>
    </div>
  </footer>

  <!-- Toast Notification Container -->
  <div id="toastContainer" data-nosnippet="" aria-hidden="true" class="fixed bottom-6 right-6 z-50 flex flex-col gap-2 pointer-events-none"></div>

  <!-- Shared Modular Tools Logic -->
  <script src="/js/tools.js?v=2026.1"></script>
</body>
</html>
"""
        target_dir = os.path.join(ROOT_DIR, 'tools', slug)
        os.makedirs(target_dir, exist_ok=True)
        target_file = os.path.join(target_dir, 'index.html')
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(page_html)
        print(f"  ✅ Generated: /tools/{slug}/index.html ({len(page_html)} bytes)")

    print(f"\n🎉 Successfully created all 6 standalone interactive tool pages!")

if __name__ == '__main__':
    generate_standalone_tools()
