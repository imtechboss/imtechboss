import os, json, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'js', 'data.js')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);', content)
if not match:
    print("Error: initialArticles not found")
    exit(1)

articles = json.loads(match.group(1))
updated_count = 0

# Check RTX 5090 vs RTX 4090 article
for art in articles:
    if art['id'] == 'rtx-5090-vs-rtx-4090-blackwell-benchmarks-specs-upgrade-guide-2026':
        if 'tools.html' not in art['content']:
            callout = """<div class="p-4 my-6 rounded-2xl bg-blue-50 dark:bg-slate-800 border border-blue-200 dark:border-slate-700 text-xs sm:text-sm text-gray-800 dark:text-gray-200">
  <strong>🛠️ Free Interactive Tool:</strong> Planning your upgrade? Check if your current CPU or PSU will bottleneck the RTX 5090 using our <a href="tools.html" class="underline font-bold text-blue-600 dark:text-blue-400">PC Bottleneck &amp; Hardware Matcher Calculator</a>.
</div>"""
            art['content'] = art['content'].replace('<h2>4K Gaming', callout + '\n\n<h2>4K Gaming')
            updated_count += 1

    if art['id'] == 'best-gaming-gpus-under-500-dollars-2026-vram-1440p-rankings':
        if 'tools.html' not in art['content']:
            callout = """<div class="p-4 my-6 rounded-2xl bg-emerald-50 dark:bg-slate-800 border border-emerald-200 dark:border-slate-700 text-xs sm:text-sm text-gray-800 dark:text-gray-200">
  <strong>🎮 System Compatibility:</strong> Will these GPUs run your favorite titles at 1440p? Test your full setup with our <a href="tools.html" class="underline font-bold text-emerald-600 dark:text-emerald-400">Can My PC Run It? Tool</a>.
</div>"""
            art['content'] = art['content'].replace('<h2>Analysis', callout + '\n\n<h2>Analysis')
            updated_count += 1

if updated_count > 0:
    new_json = json.dumps(articles, indent=2, ensure_ascii=False)
    new_content = content[:match.start(1)] + new_json + content[match.end(1):]
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {updated_count} articles with smart internal cross-links!")
else:
    print("All target articles already have internal cross-links.")
