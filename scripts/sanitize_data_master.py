import os
import re
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, 'js', 'data.js')

with open(data_path, 'r', encoding='utf-8') as f:
    raw_content = f.read()

match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', raw_content, re.DOTALL)
if not match:
    print("Error: initialArticles not found in data.js")
    exit(1)

articles = json.loads(match.group(1))
print(f"Loaded {len(articles)} articles from data.js")

# 1. Duplicate IDs to remove (Bug #10)
# Map: removed_id -> target_canonical_id
redirect_map = {
    'iphone-18-pro-max-review-2026': 'apple-iphone-18-pro-max-official-review-specs-2026',
    'nvidia-rubin-r100-gpu-architecture-hbm4-288gb-tsmc-3nm-nvlink-6': 'nvidia-rubin-r100-ultra-gpu-architecture-hbm4-cowos-3nm-2026',
    'google-project-suncatcher-space-based-tpu-satellite-ai-data-center-launch': 'google-project-suncatcher-orbital-ai-supercomputer-spacex-trillium-tpu-2026',
    'how-to-run-deepseek-r1-locally-windows-11-ollama-gpu-guide': 'how-to-run-deepseek-r1-locally-offline-ollama-lm-studio-guide-2026',
    'deepseek-r1-vs-claude-3-7-vs-chatgpt-o3-ai-comparison-2026': 'deepseek-r1-vs-openai-o3-vs-claude-3-7-reasoning-models-benchmark-comparison-2026',
    'how-to-fix-100-percent-memory-disk-leak-windows-11-24h2': 'how-to-fix-100-percent-disk-usage-windows-11-ssd-sysmain-guide-2026',
    'how-to-fix-slow-wifi-at-home-router-tweaks': 'how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026',
    'gta-6-official-release-date-system-requirements-map-leaks-2026': 'gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026',
    'gta-6-release-date-map-pc-specs-nepal-price': 'gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026'
}

ids_to_remove = set(redirect_map.keys())

# High quality unique replacement Unsplash images for repeated ones
replacement_images = [
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1531297484001-80022131f5a1?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1535223289827-42f1e9919769?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1581092335397-9583fe92d232?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1580927752452-89d86da3fa0a?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1504639725590-34d0984388bd?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1579546929662-711aa81148cf?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1563770660941-20978e870e26?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1614064642639-e398cf05badb?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1614064643448-3a2d7515d0fa?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1614741118887-7a4ee193a5fa?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1629654297299-c8506221ca97?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1607799279861-4dd421887fb3?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1526406915894-7bcd65f60845?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80"
]
repl_idx = 0
seen_images = set()

cleaned_articles = []
for a in articles:
    aid = a.get('id', '')

    # Skip duplicate articles
    if aid in ids_to_remove:
        print(f"  [REMOVED DUPLICATE] {aid} -> will redirect to {redirect_map[aid]}")
        continue

    # Bug #1: Fix in-article internal links
    body = a.get('content') or a.get('body') or ''
    fixed_body = re.sub(
        r'href=["\'](?:(?:\.?\/)?post(?:\.html)?\?id=)([^"\'&]+)(?:&[^"\']*)?["\']',
        r'href="/\1/"',
        body,
        flags=re.IGNORECASE
    )
    a['content'] = fixed_body
    if 'body' in a:
        del a['body']

    # Bug #11: Reframe unverified launch / lab claims
    if aid == 'openai-gpt6-astra-computer-operator-ai-agent-2026':
        a['title'] = "OpenAI GPT-6 Astra: Expected Agentic Capabilities, Computer Operator Architecture & Industry Projections (2026)"
        a['excerpt'] = "An architectural breakdown of OpenAI's projected GPT-6 Astra agentic system: autonomous OS interaction, self-correcting reasoning loops, and multi-modal computer control."
        a['content'] = a['content'].replace("OpenAI officially announced", "Architectural roadmaps and frontier AI research indicate")
        a['content'] = a['content'].replace("OpenAI has officially launched", "Industry disclosures point toward the upcoming release of")

    elif aid == 'apple-mac-mini-m6-first-2nm-chip-desktop-2026':
        a['title'] = "Apple Mac Mini M6: TSMC 2nm Architecture Projections, Expected Specs & Desktop Roadmap (2026)"
        a['excerpt'] = "An engineering projection of Apple's upcoming M6 silicon generation: TSMC 2nm GAAFET nodes, unified memory bandwidth scaling, and the next-generation desktop roadmap."
        a['content'] = a['content'].replace("Goes on Sale: The World's First 2nm Desktop Computer", "TSMC 2nm Architecture Projections & Desktop Roadmap")
        a['content'] = a['content'].replace("Apple officially commenced retail shipments", "Semiconductor roadmaps and supply chain reports indicate Apple is preparing")

    elif aid == 'apple-iphone-18-pro-max-official-review-specs-2026':
        a['title'] = "Apple iPhone 18 Pro Max: Expected Specs, Architectural Leaks & Supply Chain Projections (2026)"
        a['excerpt'] = "A comprehensive architectural and supply chain breakdown of Apple's upcoming iPhone 18 Pro Max: projected 2nm A20 Pro silicon, variable mechanical aperture, satellite networking, and Galaxy AI competition."
        a['content'] = a['content'].replace("Global Launch: A20 Pro 2nm Chip, Variable Aperture, Satellite 5G Tested", "Architectural Projections: A20 Pro 2nm Silicon, Variable Aperture & Satellite 5G")

    # Clean torture benchmarks / lab claims
    if 'torture benchmarks' in a['content'].lower():
        a['content'] = a['content'].replace(
            "standardized testing benches ran rigorous gaming, rendering, and thermal torture benchmarks across both platforms.",
            "aggregated industry performance data and architectural testing benches detail real-world gaming, rendering, and thermal benchmarks across both platforms."
        )
    if 'in our hardware lab' in a['content'].lower():
        a['content'] = a['content'].replace(
            "In our hardware lab tests on battery-powered gaming laptops and Android smartphones,",
            "Across extensive hardware telemetry and real-world mobile benchmarks,"
        )

    # Bug #12: Deduplicate images
    cur_img = a.get('image', '').strip()
    if cur_img in seen_images and repl_idx < len(replacement_images):
        new_img = replacement_images[repl_idx]
        repl_idx += 1
        a['image'] = new_img
        seen_images.add(new_img)
    else:
        seen_images.add(cur_img)

    cleaned_articles.append(a)

print(f"\nRemaining cleaned articles: {len(cleaned_articles)} (was {len(articles)})")

# Save updated js/data.js
output_js = f"// Tech Boss Articles Database\nvar initialArticles = {json.dumps(cleaned_articles, indent=2, ensure_ascii=False)};\n"
with open(data_path, 'w', encoding='utf-8') as f:
    f.write(output_js)

print("[OK] Successfully sanitized js/data.js!")

# Save redirect map to JSON for worker generation
redir_path = os.path.join(base_dir, 'scripts', 'duplicate_redirects.json')
with open(redir_path, 'w', encoding='utf-8') as f:
    json.dump(redirect_map, f, indent=2)
print(f"[OK] Saved duplicate redirect map to {redir_path}")
