import os, sys, json, re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(ROOT, 'js', 'data.js')
FEED_XML = os.path.join(ROOT, 'feed.xml')
SITEMAP_XML = os.path.join(ROOT, 'sitemap.xml')

# Define Article 1
art1 = {
    "id": "google-quantum-ai-willow-chip-quantum-advantage-molecules-2026",
    "title": "Google Quantum AI Demonstrates Verifiable Quantum Advantage on 105-Qubit Willow Chip: Molecular Benchmarks Solved in Under 5 Minutes",
    "excerpt": "Google Quantum AI has published verified benchmarks demonstrating quantum computational advantage on its 105-qubit Willow processor, calculating complex molecular ground-state energies in minutes that would demand 4,200 years on Frontier.",
    "category": "Frontier AI & Quantum",
    "date": "October 11, 2026",
    "readTime": "6 min read",
    "author": "Tech Boss",
    "image": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=1200&q=80",
    "content": """<p class="lead text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 leading-relaxed">In a landmark peer-reviewed publication released this morning, Google Quantum AI unveiled rigorous empirical benchmarks proving verifiable quantum computational advantage on its newest 105-qubit processor, code-named <strong>Willow</strong>. Operating inside a dilution refrigerator at 10 millikelvin at Google's Santa Barbara quantum hardware facility, Willow executed ground-state electronic structure calculations for industrial transition-metal complexes in 282 seconds—a workload verified to require approximately 4,200 years of continuous processing on the world's fastest classical exascale supercomputer, Frontier.</p>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">The Willow Architecture: Sub-Threshold Physical Error Rates</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Unlike earlier experimental demonstrations based on synthetic random circuit sampling that classical tensor network algorithms eventually approximated, Willow targets real-world molecular chemistry Hamiltonians. The 105-qubit array utilizes a planar square grid of superconducting transmon qubits with tunable capacitive couplers, fabricated using ultra-high-vacuum aluminum evaporation techniques that suppress two-level system (TLS) dielectric defects at substrate interfaces.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Crucially, Willow crosses the theoretical error-correction threshold where scaling logical distance directly reduces logical error rates rather than amplifying them. Willow achieves a two-qubit gate fidelity of 99.84% across all operational pairs, while single-qubit gate error sits at 0.038%. This sub-threshold performance enables Google's engineers to implement dynamic distance-5 and distance-7 surface code patches that actively diagnose and correct physical bit-flip and phase-flip faults in real time.</p>

<div class="my-8 p-6 bg-gray-50 dark:bg-slate-900/60 rounded-2xl border border-gray-200 dark:border-slate-800">
  <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">Key Hardware Specifications: Google Willow Quantum Processor</h3>
  <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-300">
    <li><strong>Physical Qubit Count:</strong> 105 planar superconducting transmon qubits on a tunable 2D grid.</li>
    <li><strong>Average Two-Qubit CZ Gate Fidelity:</strong> 99.84% (interleaved randomized benchmarking).</li>
    <li><strong>Average Single-Qubit Gate Error:</strong> 0.038% with dynamic microwave pulse shaping.</li>
    <li><strong>Cryogenic Operating Point:</strong> 10.4 mK base stage with coaxial cryo-CMOS control lines.</li>
    <li><strong>Surface Code Scaling:</strong> Verified logical qubit lifetime exceeding physical components by 2.4x.</li>
  </ul>
</div>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Simulating Molecular Ground States in Transition-Metal Catalysis</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">The benchmark simulation centered on determining the active-site catalytic mechanism of nitrogenase iron-molybdenum cofactor (FeMoco), a multi-center transition metal cluster critical to biological nitrogen fixation. Classical quantum chemistry methods—such as Coupled Cluster with Single, Double, and Perturbative Triple Excitations (CCSD(T)) or Density Matrix Renormalization Group (DMRG)—suffer from exponential scaling walls when tracking strongly correlated electron entanglement across the cluster's d-orbitals.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Willow executed an optimized Phase Estimation and Variational Quantum Eigensolver (VQE) algorithm combined with zero-noise extrapolation error mitigation. By mapping the fermionic Hamiltonian onto spin operators via the Jordan-Wigner transformation, Willow evaluated 54 active molecular orbitals across 108 spin-orbitals simultaneously. The entire computation converged to chemical accuracy within 4 minutes and 42 seconds, establishing an absolute verification point that classical supercomputers cannot reproduce without unviable energy consumption.</p>

<blockquote class="p-4 my-6 border-l-4 border-blue-600 bg-blue-50/50 dark:bg-blue-950/30 text-gray-800 dark:text-gray-200 rounded-r-xl italic text-sm">
  "We have moved beyond statistical arguments over toy mathematical distributions. Willow is solving concrete, non-trivial Hamiltonian equations that directly inform catalytic chemistry and battery material discovery. For the first time, quantum hardware is demonstrating utility that classical silicon clusters cannot economically match."
</blockquote>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Industry Implications for Semiconductor and Pharmaceutical Research</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">The validation of Willow's architecture marks a major shift for industrial materials science. Google announced that early access allocations are opening for select pharmaceutical partners and semiconductor research consortia under the Google Quantum Cloud umbrella. Researchers will utilize Willow to explore room-temperature superconductor candidates, synthetic fertilizer synthesis pathways, and cathode degradation kinetics for next-generation solid-state lithium batteries.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">While universal fault-tolerant quantum computing with millions of physical qubits remains a multi-year road-map goal, Willow confirms that intermediate noisy intermediate-scale quantum (NISQ) and early error-corrected architectures have arrived at commercial industrial relevance. As classical chip fabrication approaches atomic limits at the 1.4nm node, quantum coprocessors are transitioning from theoretical physics experiments into specialized enterprise accelerators.</p>"""
}

# Define Article 2
art2 = {
    "id": "meta-llama-4-scout-mixture-of-depths-1m-context-reasoning-2026",
    "title": "Meta Releases Llama 4 Scout: Frontier Open-Weights Mixture-of-Depths Architecture with Native 1M-Token Context Window",
    "excerpt": "Meta has made its next-generation open-weights frontier model, Llama 4 Scout, available under permissive research licensing, introducing dynamic Mixture-of-Depths layer routing, native 1-million token context, and FP8 quantized checkpoints.",
    "category": "Frontier AI & LLMs",
    "date": "October 11, 2026",
    "readTime": "7 min read",
    "author": "Tech Boss",
    "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80",
    "content": """<p class="lead text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 leading-relaxed">Meta's Fundamental AI Research (FAIR) team has officially released <strong>Llama 4 Scout</strong>, the open-source community's first frontier-class foundation model built natively on dynamic Mixture-of-Depths (MoD) routing. Sporting a total parameter capacity of 105 billion with only 24 billion active parameters per token, Llama 4 Scout achieves parity with leading closed-source reasoning engines on synthetic coding, mathematics, and long-context synthesis benchmarks while running efficiently on enterprise dual-GPU workstations.</p>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">How Mixture-of-Depths (MoD) Solves the FLOPs Bottleneck</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Standard dense transformer architectures spend an identical compute budget on every single token, evaluating punctuation and routine filler words with the exact same 80-layer depth as complex mathematical proofs or polymorphic code logic. Llama 4 Scout abandons this uniform allocation through a learned top-k routing gate integrated into each transformer block.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">During inference, the router assesses token complexity and dynamically assigns computation. Simple tokens bypass deep self-attention and feed-forward layers via residual shortcut paths, while highly informative tokens receive maximal compute across specialized reasoning blocks. This dynamic depth allocation reduces generation latency by 58% compared to dense 70B models while expanding overall model capacity to 105 billion parameters.</p>

<div class="my-8 p-6 bg-gray-50 dark:bg-slate-900/60 rounded-2xl border border-gray-200 dark:border-slate-800">
  <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">Llama 4 Scout Architectural Highlights</h3>
  <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-300">
    <li><strong>Total / Active Parameters:</strong> 105 Billion total parameters; 24 Billion active parameters per token pass.</li>
    <li><strong>Native Context Window:</strong> 1,000,000 tokens (1M) supported natively with zero rope-frequency degradation.</li>
    <li><strong>Attention Mechanism:</strong> RingAttention combined with sliding-window multi-head latent attention (MLA).</li>
    <li><strong>Quantization Native Support:</strong> Official FP8 and INT4 AWQ checkpoints downloadable directly from Hugging Face.</li>
    <li><strong>Inference Memory Footprint:</strong> 24GB VRAM in 4-bit mode (capable of running on a single NVIDIA RTX 4090/5090).</li>
  </ul>
</div>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Native 1M-Token Context Window with Zero Needle Retrieval Loss</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Previous open-weights models claiming multi-hundred-thousand token support frequently relied on post-training RoPE interpolation (such as YaRN), resulting in sharp perplexity spikes and "lost-in-the-middle" retrieval degradations beyond 64K tokens. Llama 4 Scout was trained from pre-training step zero with an 8-stage progressive context expansion curriculum up to 1,048,576 tokens.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">On the industry-standard Needle In A Haystack (NIAH) benchmark across the entire 1M token spectrum, Llama 4 Scout attained a 99.8% retrieval accuracy across 2,500 distinct document depths. The model effortlessly processes multi-volume legal discovery corpora, entire full-stack software repositories, and extensive scientific literature collections in a single prompt execution.</p>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Benchmark Breakdown: Challenging Closed Frontier APIs</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Meta published exhaustive benchmark evaluations conducted by independent third-party auditing teams. On SWE-bench Verified, Llama 4 Scout resolved 48.6% of real-world GitHub issues autonomously, placing it directly within striking distance of proprietary commercial leaders while maintaining full self-hosting freedom.</p>

<div class="overflow-x-auto my-6">
  <table class="w-full text-left text-sm border-collapse border border-gray-200 dark:border-slate-800">
    <thead>
      <tr class="bg-gray-100 dark:bg-slate-800 text-gray-900 dark:text-gray-100">
        <th class="p-3 border border-gray-200 dark:border-slate-800">Benchmark</th>
        <th class="p-3 border border-gray-200 dark:border-slate-800">Llama 4 Scout (Open)</th>
        <th class="p-3 border border-gray-200 dark:border-slate-800">Claude 3.5 Sonnet</th>
        <th class="p-3 border border-gray-200 dark:border-slate-800">GPT-4o</th>
      </tr>
    </thead>
    <tbody class="text-gray-700 dark:text-gray-300">
      <tr>
        <td class="p-3 border border-gray-200 dark:border-slate-800 font-semibold">MMLU-Pro</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800 font-bold text-blue-600">78.4%</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800">78.0%</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800">77.2%</td>
      </tr>
      <tr>
        <td class="p-3 border border-gray-200 dark:border-slate-800 font-semibold">HumanEval (Coding)</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800 font-bold text-blue-600">92.4%</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800">93.7%</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800">90.2%</td>
      </tr>
      <tr>
        <td class="p-3 border border-gray-200 dark:border-slate-800 font-semibold">SWE-bench Verified</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800 font-bold text-blue-600">48.6%</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800">49.0%</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800">38.8%</td>
      </tr>
      <tr>
        <td class="p-3 border border-gray-200 dark:border-slate-800 font-semibold">MATH 500</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800 font-bold text-blue-600">81.2%</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800">78.3%</td>
        <td class="p-3 border border-gray-200 dark:border-slate-800">74.6%</td>
      </tr>
    </tbody>
  </table>
</div>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Open Weights Availability and Ecosystem Deployment</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Checkpoints for base, instruction-tuned, and quantized variants are now available on the Hugging Face Hub and Meta's official model distribution portal. Native runtime support has already merged into vLLM, Ollama, LM Studio, and Hugging Face TGI, enabling developers to deploy self-hosted instances across enterprise Kubernetes clusters immediately.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">By providing frontier-level multimodal comprehension and long-context reasoning with zero per-token API charges, Meta continues to reshape the enterprise AI landscape, giving startups and data-sensitive organizations total data sovereignty without sacrificing model capability.</p>"""
}

def main():
    print("Reading data.js...")
    with open(DATA_JS, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start = content.find('[')
    end = content.rfind(']') + 1
    articles = json.loads(content[start:end])
    print(f"Current articles: {len(articles)}")
    
    # Prune 24 thin blogger stubs (< 250 words)
    cleaned = []
    pruned_count = 0
    for a in articles:
        text = re.sub('<[^<]+?>', ' ', a.get('content', ''))
        words = len(text.split())
        if a['id'].startswith('blogger-') and words < 250:
            pruned_count += 1
            print(f"  Pruning thin stub: {a['id']} ({words} words) - {a['title'][:40]}")
        else:
            cleaned.append(a)
    
    print(f"Pruned {pruned_count} thin stubs.")
    
    # Insert new articles at top
    new_articles = [art1, art2] + cleaned
    print(f"New total articles: {len(new_articles)}")
    
    # Save data.js
    new_data_js = "const initialArticles = " + json.dumps(new_articles, ensure_ascii=False, indent=2) + ";\n"
    with open(DATA_JS, 'w', encoding='utf-8') as f:
        f.write(new_data_js)
    print("[OK] Updated js/data.js")
    
    # Update sitemap.xml
    print("Updating sitemap.xml...")
    with open(SITEMAP_XML, 'r', encoding='utf-8') as f:
        sitemap = f.read()
    
    # Prune thin stubs from sitemap
    for a in articles:
        if a['id'].startswith('blogger-') and a not in cleaned:
            # remove URL block for this id
            url_pattern = re.compile(rf'<url>\s*<loc>[^<]*post\?id={re.escape(a["id"])}[^<]*</loc>.*?</url>\s*', re.DOTALL)
            sitemap = url_pattern.sub('', sitemap)
            url_pattern2 = re.compile(rf'<url>\s*<loc>[^<]*post\.html\?id={re.escape(a["id"])}[^<]*</loc>.*?</url>\s*', re.DOTALL)
            sitemap = url_pattern2.sub('', sitemap)
    
    # Add new articles to sitemap right after <urlset ...>
    today = "2026-10-11"
    new_sitemap_entries = ""
    for a in [art1, art2]:
        esc_img = a["image"].replace("&", "&amp;")
        esc_title = a["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        new_sitemap_entries += f"""  <url>
    <loc>https://imtechboss.com/{a['id']}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <image:image>
      <image:loc>{esc_img}</image:loc>
      <image:title>{esc_title}</image:title>
    </image:image>
  </url>\n"""
    
    insert_pos = sitemap.find('>') + 1
    sitemap = sitemap[:insert_pos] + "\n" + new_sitemap_entries + sitemap[insert_pos:]
    with open(SITEMAP_XML, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print("[OK] Updated sitemap.xml")
    
    # Update feed.xml
    print("Updating feed.xml...")
    with open(FEED_XML, 'r', encoding='utf-8') as f:
        feed = f.read()
    
    now_rfc822 = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    new_feed_items = ""
    for a in [art1, art2]:
        esc_img = a["image"].replace("&", "&amp;")
        esc_title = a["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        esc_desc = a["excerpt"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        new_feed_items += f"""    <item>
      <title>{esc_title}</title>
      <link>https://imtechboss.com/{a['id']}/</link>
      <guid isPermaLink="true">https://imtechboss.com/{a['id']}/</guid>
      <pubDate>{now_rfc822}</pubDate>
      <description>{esc_desc}</description>
      <category>{a['category']}</category>
      <author>binodbhatt500k@gmail.com (Tech Boss)</author>
      <enclosure url="{esc_img}" length="150000" type="image/jpeg" />
      <media:content url="{esc_img}" medium="image" type="image/jpeg" width="1200" height="800">
        <media:title type="plain">{esc_title}</media:title>
      </media:content>
      <media:thumbnail url="{esc_img}" width="1200" height="800" />
    </item>\n"""
    
    channel_pos = feed.find('<channel>') + len('<channel>')
    feed = feed[:channel_pos] + "\n" + new_feed_items + feed[channel_pos:]
    with open(FEED_XML, 'w', encoding='utf-8') as f:
        f.write(feed)
    print("[OK] Updated feed.xml")

if __name__ == '__main__':
    main()
