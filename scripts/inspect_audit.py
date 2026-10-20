import os
import re
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, 'js', 'data.js')

with open(data_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check in-article post?id links
matches = re.findall(r'href=[\'"](?:(?:\.?\/)?post(?:\.html)?\?id=)([^&\'"]+)(?:&[^\'"]*)?[\'"]', content, re.IGNORECASE)
print(f"Total post?id links in data.js: {len(matches)}")
print("Sample matches:", matches[:10])

# Check blogger- count
blogger_matches = re.findall(r'"id":\s*"blogger-\d+"', content)
print(f"Total blogger- posts: {len(blogger_matches)}")

# Check duplicates mentioned in Bug 10
duplicates_to_check = [
    'apple-iphone-18-pro-max-official-review-specs-2026',
    'iphone-18-pro-max-review-2026',
    'iphone-18-pro-max-vs-galaxy-s26-ultra',
    'nvidia-rubin-r100-ultra-gpu-architecture-hbm4-cowos-3nm-2026',
    'nvidia-rubin-r100-gpu-architecture-hbm4-288gb-tsmc-3nm-nvlink-6',
    'google-project-suncatcher-orbital-ai-supercomputer-spacex-trillium-tpu-2026',
    'google-project-suncatcher-space-based-tpu-satellite-ai-data-center-launch',
    'how-to-run-deepseek-r1-locally-offline-ollama-lm-studio-guide-2026',
    'how-to-run-deepseek-r1-locally-windows-11-ollama-gpu-guide',
    'deepseek-r1-vs-openai-o3-vs-claude-3-7-reasoning-models-benchmark-comparison-2026',
    'deepseek-r1-vs-claude-3-7-vs-chatgpt-o3-ai-comparison-2026',
    'how-to-fix-100-percent-memory-disk-leak-windows-11-24h2',
    'how-to-fix-100-percent-disk-usage-windows-11-ssd-sysmain-guide-2026',
    'how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026',
    'how-to-fix-slow-wifi-at-home-router-tweaks',
    'gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026',
    'gta-6-official-release-date-system-requirements-map-leaks-2026',
    'gta-6-release-date-map-pc-specs-nepal-price'
]

match_array = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', content, re.DOTALL)
articles = json.loads(match_array.group(1))
id_set = {a['id'] for a in articles}

print("\nDuplicate IDs presence in data.js:")
for did in duplicates_to_check:
    print(f"  {did}: {'PRESENT' if did in id_set else 'ABSENT'}")
