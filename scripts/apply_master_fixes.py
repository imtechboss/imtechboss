import re, os, sys

def update_build_static():
    script_path = os.path.join(os.path.dirname(__file__), 'build_static.py')
    with open(script_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. New generate_key_takeaways
    new_takeaways = '''def generate_key_takeaways(article):
    excerpt = (article.get('excerpt') or '').strip()
    content = article.get('content') or article.get('body', '')
    sections = re.split(r'<h2[^>]*>(.*?)</h2>', content, flags=re.IGNORECASE)
    takeaways = []

    if len(sections) > 1:
        for i in range(1, len(sections), 2):
            h2 = re.sub(r'<[^>]+>', '', sections[i]).strip()
            sec_content = sections[i+1] if i+1 < len(sections) else ''
            p_match = re.search(r'<p[^>]*>(.*?)</p>', sec_content, re.IGNORECASE)
            sent = ''
            if p_match:
                p_text = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
                s_split = re.split(r'(?<=[.!?])\\s+', p_text)
                if s_split and len(s_split[0]) > 20:
                    sent = s_split[0].strip()

            clean_h2 = re.sub(r'^(\\d+[\\.\\)]|Fix \\d+:?|Section \\d+:?)\\s*', '', h2).strip()
            if sent and sent != excerpt:
                item = f'<strong>{clean_h2}:</strong> {sent}'
                if item not in takeaways:
                    takeaways.append(item)
            elif clean_h2 and clean_h2 != excerpt:
                item = f'<strong>{clean_h2}</strong>'
                if item not in takeaways:
                    takeaways.append(item)
            if len(takeaways) >= 3:
                break

    if len(takeaways) < 3:
        ps = re.findall(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE)
        for p in ps:
            p_text = re.sub(r'<[^>]+>', '', p).strip()
            s_split = re.split(r'(?<=[.!?])\\s+', p_text)
            for s in s_split:
                s = s.strip()
                clean_s = re.sub(r'<[^>]+>', '', s).strip()
                if len(clean_s) > 30 and clean_s != excerpt and clean_s not in [re.sub(r'<[^>]+>', '', t) for t in takeaways]:
                    takeaways.append(clean_s)
                    if len(takeaways) >= 3:
                        break
            if len(takeaways) >= 3:
                break

    if not takeaways:
        return ''

    li_items = '\\n'.join([
        f\'\'\'<li class="flex items-start gap-2.5">
            <span class="w-1.5 h-1.5 rounded-full bg-blue-600 dark:bg-blue-400 mt-2 flex-shrink-0"></span>
            <span class="leading-relaxed">{pt}</span>
          </li>\'\'\'
        for pt in takeaways
    ])

    direct_summary = f\'\'\'
        <div class="text-xs sm:text-sm font-semibold text-gray-900 dark:text-white leading-relaxed mb-4 pb-3 border-b border-gray-100 dark:border-slate-800">
          <strong>Direct Summary: </strong>{escape(excerpt)}
        </div>
    \'\'\' if excerpt else ''

    return f\'\'\'
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
      <div class="text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-2">
        Core Takeaways &amp; Findings:
      </div>
      <ul class="space-y-2 text-xs sm:text-sm text-gray-800 dark:text-gray-200 list-none pl-0 mb-0">
        {li_items}
      </ul>
    </div>
    \'\'\''''

    # 2. New generate_faq_data with 7 topic branches
    new_faq_data = '''def _format_faq(faqs):
    faq_html = f\'\'\'
    <div class="my-10 p-6 sm:p-7 rounded-3xl bg-gray-50/90 dark:bg-slate-800/60 border border-gray-200/80 dark:border-slate-800/80 shadow-xs not-prose">
      <div class="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200/60 dark:border-slate-700/60">
        <span class="text-base">💬</span>
        <h3 class="text-sm sm:text-base font-extrabold uppercase tracking-wider text-gray-900 dark:text-white">
          Frequently Asked Questions &amp; Technical Clarifications
        </h3>
      </div>
      <div class="space-y-3">
        {\'\\n\'.join([
            f"""<details class="group p-4 rounded-2xl bg-white dark:bg-slate-800/80 border border-gray-200/80 dark:border-slate-700/80 transition-colors">
              <summary class="flex justify-between items-center font-bold text-xs sm:text-sm text-gray-900 dark:text-gray-100 cursor-pointer select-none">
                <span>{escape(f["q"])}</span>
                <span class="text-gray-400 group-open:rotate-180 transition-transform ml-2 text-xs flex-shrink-0">▼</span>
              </summary>
              <p class="mt-3 text-xs sm:text-sm text-gray-600 dark:text-gray-300 leading-relaxed border-t border-gray-100 dark:border-slate-700/60 pt-2.5">
                {escape(f["a"])}
              </p>
            </details>"""
            for f in faqs
        ])}
      </div>
    </div>
    \'\'\'

    schema_faqs = [
        {
            "@type": "Question",
            "name": f["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f["a"]
            }
        }
        for f in faqs
    ]

    return faq_html, schema_faqs

def generate_faq_data(article):
    cat = (article.get('category') or '').lower()
    title = (article.get('title') or '').lower()

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
                "a": "Yes. The steps detailed in this Tech Boss analysis operate within standard operating system guidelines and do not modify protected kernel modules or partition structures."
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

    # Branch 6: Networking, Security & Telecom
    if any(k in cat for k in ['cybersecurity', 'cloud', 'hosting']) or any(k in title for k in ['vpn', 'wifi', 'wi-fi', 'router', 'dns', 'wireguard', 'isp', '5g', 'telecom', 'ntc', 'ncell']):
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

    # Branch 7: General Tech & Engineering Fallback (NEVER Windows 11 DISM!)
    faqs = [
        {
            "q": "How are the technical specifications and benchmarks in this analysis verified?",
            "a": "Tech Boss cross-references manufacturer architectural whitepapers, standardized benchmark suites, developer documentation, and verified hardware telemetry to ensure objective technical accuracy."
        },
        {
            "q": "Can I use Tech Boss interactive tools to evaluate my setup?",
            "a": "Yes. Tech Boss provides free interactive diagnostics, hardware comparison calculators, and latency testing utilities directly in the Interactive Hubs section."
        },
        {
            "q": "How frequently is this technical analysis updated with new data?",
            "a": "Our editorial and engineering radar continuously monitors firmware revisions, driver patches, and industry silicon updates, refreshing analyses as verified test data becomes available."
        }
    ]
    return _format_faq(faqs)'''

    # Replace generate_key_takeaways using lambda
    old_takeaways_pattern = r'def generate_key_takeaways\(article\):[\s\S]*?return f\'\'\'\s*<div id="aioAnswerCapsule"[\s\S]*?</div>\s*\'\'\''
    if not re.search(old_takeaways_pattern, code):
        print("❌ Could not match old generate_key_takeaways")
        return False
    code = re.sub(old_takeaways_pattern, lambda m: new_takeaways, code, count=1)

    # Replace generate_faq_data using lambda
    old_faq_pattern = r'def generate_faq_data\(article\):[\s\S]*?return faq_html, schema_faqs'
    if not re.search(old_faq_pattern, code):
        print("❌ Could not match old generate_faq_data")
        return False
    code = re.sub(old_faq_pattern, lambda m: new_faq_data, code, count=1)

    # 3. Add noindex, follow for blogger- posts in build_all_static
    blogger_check = '''        # Replace Canonical
        page_html = re.sub(r'<link id="canonicalUrl" rel="canonical" href=".*?">', f'<link id="canonicalUrl" rel="canonical" href="{canonical_url}">', page_html)

        # Legacy blogger posts should be noindex, follow to preserve crawl budget
        if aid.startswith('blogger-'):
            page_html = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, follow">', page_html)'''
    
    canonical_pattern = r'# Replace Canonical\s+page_html = re\.sub\(r\'<link id="canonicalUrl" rel="canonical" href=".*?">\', f\'<link id="canonicalUrl" rel="canonical" href="\{canonical_url\}">\', page_html\)'
    if not re.search(canonical_pattern, code):
        print("❌ Could not match canonical block in build_all_static")
        return False
    code = re.sub(canonical_pattern, lambda m: blogger_check, code, count=1)

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(code)

    print("✅ scripts/build_static.py updated successfully!")
    return True

def update_generate_sitemap():
    script_path = os.path.join(os.path.dirname(__file__), 'generate_sitemap.py')
    with open(script_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Skip blogger- articles in sitemap
    old_loop = "for article in data:\n        aid = article.get('id', '')"
    new_loop = "for article in data:\n        aid = article.get('id', '')\n        if aid.startswith('blogger-'):\n            continue"

    if old_loop not in code:
        print("❌ Could not match article loop in generate_sitemap.py")
        return False

    code = code.replace(old_loop, new_loop, 1)

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(code)

    print("✅ scripts/generate_sitemap.py updated successfully!")
    return True

if __name__ == '__main__':
    ok1 = update_build_static()
    ok2 = update_generate_sitemap()
    if ok1 and ok2:
        print("🎉 Both scripts updated perfectly!")
    else:
        sys.exit(1)
