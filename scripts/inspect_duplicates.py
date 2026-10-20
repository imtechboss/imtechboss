import json, re

with open('js/data.js', 'r', encoding='utf-8') as f:
    c = f.read()

articles = json.loads(re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', c, re.DOTALL).group(1))
art_map = {a['id']: a for a in articles}

pairs = [
    ("iPhone 18", ['apple-iphone-18-pro-max-official-review-specs-2026', 'iphone-18-pro-max-review-2026', 'iphone-18-pro-max-vs-galaxy-s26-ultra']),
    ("Rubin R100", ['nvidia-rubin-r100-ultra-gpu-architecture-hbm4-cowos-3nm-2026', 'nvidia-rubin-r100-gpu-architecture-hbm4-288gb-tsmc-3nm-nvlink-6']),
    ("Suncatcher", ['google-project-suncatcher-orbital-ai-supercomputer-spacex-trillium-tpu-2026', 'google-project-suncatcher-space-based-tpu-satellite-ai-data-center-launch']),
    ("DeepSeek Local", ['how-to-run-deepseek-r1-locally-offline-ollama-lm-studio-guide-2026', 'how-to-run-deepseek-r1-locally-windows-11-ollama-gpu-guide']),
    ("DeepSeek vs o3", ['deepseek-r1-vs-openai-o3-vs-claude-3-7-reasoning-models-benchmark-comparison-2026', 'deepseek-r1-vs-claude-3-7-vs-chatgpt-o3-ai-comparison-2026']),
    ("Windows 11 Disk", ['how-to-fix-100-percent-memory-disk-leak-windows-11-24h2', 'how-to-fix-100-percent-disk-usage-windows-11-ssd-sysmain-guide-2026']),
    ("Slow WiFi", ['how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026', 'how-to-fix-slow-wifi-at-home-router-tweaks']),
    ("GTA 6 Specs", ['gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026', 'gta-6-official-release-date-system-requirements-map-leaks-2026', 'gta-6-release-date-map-pc-specs-nepal-price'])
]

for name, ids in pairs:
    print(f"\n--- {name} ---")
    for aid in ids:
        if aid in art_map:
            a = art_map[aid]
            content = a.get('content') or a.get('body') or ''
            words = len(re.sub(r'<[^>]+>', ' ', content).split())
            print(f"  ID: {aid}")
            print(f"     Title: {a.get('title')[:70]}")
            print(f"     Date: {a.get('date')}, Words: {words}")
        else:
            print(f"  ID: {aid} (NOT FOUND)")
