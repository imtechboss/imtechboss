import os, sys, json, re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(ROOT, 'js', 'data.js')
FEED_XML = os.path.join(ROOT, 'feed.xml')
SITEMAP_XML = os.path.join(ROOT, 'sitemap.xml')

guide_article = {
    "id": "how-to-fix-windows-11-24h2-micro-stuttering-dpc-latency-gaming-guide-2026",
    "title": "How to Fix Micro-Stuttering and DPC Latency in Windows 11 24H2: Complete DX12 & UE5 Optimization Guide (2026)",
    "excerpt": "Eliminate micro-stutters, frame pacing drops, and audio pops in Windows 11 24H2 with verified MSI GPU interrupt modes, DPC latency driver audits, timer resolution tweaks, and Core Isolation adjustments.",
    "category": "Tech Guides",
    "date": "October 18, 2026",
    "readTime": "8 min read",
    "author": "Tech Boss",
    "image": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1200&q=80",
    "content": """<p class="lead text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 leading-relaxed">Even on high-end gaming rigs equipped with RTX 4090 or RX 7900 XTX graphics cards and modern multi-core processors, many PC gamers running Windows 11 24H2 experience frustrating micro-stutters, erratic 1% low frame pacing, and random audio crackling. While average frame rates may show 144 FPS or higher, sporadic millisecond hitches ruin competitive gameplay in titles running on DirectX 12 and Unreal Engine 5. This engineering troubleshooting guide diagnoses the underlying root causes—chiefly Deferred Procedure Call (DPC) latency spikes, legacy line-based interrupt conflicts, and background kernel scheduler overhead—and provides verified, step-by-step solutions to restore fluid frame delivery.</p>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Understanding the Root Cause: DPC Latency vs Raw Frame Rate</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">In the Windows operating system architecture, hardware drivers communicate with the CPU using Interrupt Service Routines (ISRs) and Deferred Procedure Calls (DPCs). When a poorly optimized device driver (such as a Wi-Fi controller, audio codec, or secondary storage driver) holds CPU execution threads for longer than 1,000 microseconds, real-time gaming threads stall. These micro-interruptions do not drastically affect average FPS counters, but they introduce sharp 1% low frame drops and momentary frame freezes.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Before applying software tweaks, run an diagnostic sweep using the free utility <strong>LatencyMon</strong>. Launch the software, click the green Play button, run your game for five minutes, and check the <em>Drivers</em> tab. If drivers such as <code>nvlddmkm.sys</code> (Nvidia GPU), <code>ndis.sys</code> (Network), or <code>wdf01000.sys</code> (Windows Driver Framework) display execution times exceeding 1,500 µs, apply the hardware-level solutions detailed below.</p>

<div class="my-8 p-6 bg-gray-50 dark:bg-slate-900/60 rounded-2xl border border-gray-200 dark:border-slate-800">
  <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">DPC Latency Targets for Competitive Gaming</h3>
  <div class="overflow-x-auto">
    <table class="w-full text-left text-sm text-gray-700 dark:text-gray-300">
      <thead>
        <tr class="border-b border-gray-200 dark:border-slate-700 font-bold text-gray-900 dark:text-white">
          <th class="py-2.5">Latency Range</th>
          <th class="py-2.5">Gaming Impact</th>
          <th class="py-2.5">System Status</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100 dark:divide-slate-800">
        <tr><td class="py-2 font-medium">&lt; 250 µs</td><td>Flawless frame pacing, zero hitches in 240Hz+ monitors</td><td>Optimal Gaming Tuning</td></tr>
        <tr><td class="py-2 font-medium">250 – 800 µs</td><td>Occasional minor 1% low dips during heavy explosions or loading</td><td>Acceptable Desktop Standard</td></tr>
        <tr><td class="py-2 font-medium">800 – 1,500 µs</td><td>Noticeable micro-stutters during camera pans in Unreal Engine 5</td><td>Driver Conflict Present</td></tr>
        <tr><td class="py-2 font-medium">&gt; 1,500 µs</td><td>Severe hitches, audio crackling, input delay spikes</td><td>Critical Latency Bottleneck</td></tr>
      </tbody>
    </table>
  </div>
</div>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Fix 1: Enable Message Signaled-Based Interrupts (MSI Mode) on Your GPU</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">By default, many graphics card installations on Windows 11 remain configured in legacy Line-Based Interrupt (IRQ) mode. In legacy mode, your GPU shares hardware interrupt lines with other motherboard peripherals like SATA controllers and USB host controllers, forcing the CPU to serialize requests. Switching your graphics card to <strong>Message Signaled-Based Interrupts (MSI Mode)</strong> enables dedicated, packet-based direct memory access that cuts GPU interrupt latency in half.</p>

<ol class="space-y-4 my-6 list-decimal list-inside text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
  <li>Download the open-source <strong>MSI Utility v3</strong> (run as Administrator).</li>
  <li>Locate your discrete graphics card in the device list (e.g., <em>NVIDIA GeForce RTX 4080</em> or <em>AMD Radeon RX 7900 XT</em>).</li>
  <li>Check the box under the <strong>MSI</strong> column for your GPU.</li>
  <li>In the <strong>Interrupt Priority</strong> dropdown column, select <strong>High</strong> (or leave on Undefined for AMD graphics).</li>
  <li>Click <strong>Apply</strong> in the top right corner and restart your computer.</li>
</ol>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Fix 2: Configure Core Isolation (HVCI) and Virtualization-Based Security (VBS)</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Windows 11 24H2 aggressively enforces Memory Integrity (Hypervisor-Protected Code Integrity, or HVCI) under Virtualization-Based Security. While HVCI provides enterprise-grade malware protection, it introduces a 5% to 15% frame pacing penalty in CPU-intensive DirectX 12 games by virtualizing kernel page tables. Dedicated gaming enthusiasts can reclaim this headroom by reviewing our comprehensive guide on <a href="post?id=how-to-disable-vbs-windows-11-gaming-performance" class="text-blue-600 dark:text-blue-400 font-semibold underline">how to safely disable VBS for gaming performance</a>.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">To adjust this directly: open <em>Windows Security &gt; Device Security &gt; Core isolation details</em>. Toggle <strong>Memory Integrity</strong> to <strong>Off</strong> and restart your system. If you also run into background diagnostic slowdowns or high memory leaks during extended sessions, implement our verified steps to <a href="post?id=how-to-fix-100-percent-memory-disk-leak-windows-11-24h2" class="text-blue-600 dark:text-blue-400 font-semibold underline">fix 100% memory and disk leaks in Windows 11 24H2</a>.</p>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Fix 3: Resolve Network Card Interrupts &amp; Real-Time Latency</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Onboard Realtek and Intel Ethernet/Wi-Fi adapters are frequent culprits behind sudden micro-freezes. Energy-saving features periodically throttle network controller clock rates, generating massive DPC execution spikes inside <code>ndis.sys</code>. You can permanently stop this behavior with three driver adjustments:</p>

<ul class="space-y-3 my-4 list-disc list-inside text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
  <li>Press <strong>Win + X</strong> and open <strong>Device Manager</strong>. Expand <em>Network adapters</em>, right-click your active controller, and select <em>Properties</em>.</li>
  <li>Under the <strong>Advanced</strong> tab, locate <strong>Energy Efficient Ethernet</strong> and set it to <strong>Disabled</strong>.</li>
  <li>Locate <strong>Green Ethernet</strong> (or <em>Gigabit Lite</em>) and set it to <strong>Disabled</strong>.</li>
  <li>Locate <strong>Interrupt Moderation</strong>. For competitive online games, leave it <em>Enabled</em> but set <strong>Interrupt Moderation Rate</strong> to <strong>Low</strong> to minimize packet queuing delays.</li>
  <li>Pair these hardware tweaks with low-ping network configurations using our verified tutorial on <a href="post?id=how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026" class="text-blue-600 dark:text-blue-400 font-semibold underline">how to optimize Wi-Fi and choose the best gaming DNS</a>.</li>
</ul>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Fix 4: Enforce Platform Clock and High-Precision Event Timer (HPET) Consistency</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">A widespread cause of stutter in modern game engines is clock desynchronization between the motherboard's High Precision Event Timer (HPET) and the CPU Time Stamp Counter (TSC). When both timers run concurrently with conflicting query frequencies, game loops stutter when sampling frame delta times.</p>

<div class="my-6 p-4 bg-gray-900 text-gray-100 rounded-xl font-mono text-xs overflow-x-auto leading-relaxed border border-gray-800">
  <p class="text-gray-400 mb-2"># Open PowerShell as Administrator and disable artificial platform clock overrides</p>
  <p class="text-green-400">bcdedit /deletevalue useplatformclock</p>
  <p class="text-green-400">bcdedit /set disabledynamictick yes</p>
  <p class="text-green-400">bcdedit /set useplatformtick yes</p>
</div>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Disabling dynamic ticks ensures that the operating system maintains a consistent timer tick rate during full-screen rendering, preventing clock drift between CPU render threads and GPU present calls. Additionally, ensure Windows Defender background scans do not trigger mid-match by checking our guide on <a href="post?id=antimalware-service-executable-high-cpu-memory-fix-windows-11" class="text-blue-600 dark:text-blue-400 font-semibold underline">fixing Antimalware Service Executable high CPU usage</a>.</p>

<div class="my-6 p-4 border-l-4 border-blue-600 bg-blue-50/50 dark:bg-blue-950/30 rounded-r-xl">
  <h4 class="font-bold text-blue-900 dark:text-blue-300 mb-1">Tech Boss Performance Verdict</h4>
  <p class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">Micro-stuttering in Windows 11 24H2 is almost never caused by insufficient GPU raw horsepower, but by microsecond driver latency bottlenecks. By enabling MSI Mode on your graphics card, disabling Energy Efficient Ethernet, streamlining Core Isolation, and standardizing system platform clocks, you eliminate interrupt stalls and achieve razor-sharp 1% low frame pacing across all demanding DirectX 12 titles.</p>
</div>"""
}

def main():
    print("============================================================")
    print("PUBLISHING WINDOWS 11 MICRO-STUTTERING GUIDE TO TECH BOSS")
    print("============================================================")

    # 1. Update js/data.js
    with open(DATA_JS, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);', content)
    if not match:
        print("Error: Could not find initialArticles in data.js")
        sys.exit(1)

    articles = json.loads(match.group(1))

    # Prepend as index 0 (Top Featured Article)
    articles.insert(0, guide_article)

    updated_json = json.dumps(articles, indent=2, ensure_ascii=False)
    new_content = f"var initialArticles = {updated_json};\n"

    with open(DATA_JS, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Added guide to Index 0 in js/data.js. Total articles: {len(articles)}")

    # 2. Update feed.xml
    print("Updating feed.xml...")
    with open(FEED_XML, 'r', encoding='utf-8') as f:
        feed = f.read()

    now_rfc822 = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    esc_img = guide_article["image"].replace("&", "&amp;")
    esc_title = guide_article["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    esc_desc = guide_article["excerpt"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    esc_cat = guide_article["category"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    new_feed_item = f"""    <item>
      <title>{esc_title}</title>
      <link>https://imtechboss.com/{guide_article['id']}/</link>
      <guid isPermaLink="true">https://imtechboss.com/{guide_article['id']}/</guid>
      <pubDate>{now_rfc822}</pubDate>
      <description>{esc_desc}</description>
      <category>{esc_cat}</category>
      <author>binodbhatt500k@gmail.com (Tech Boss)</author>
      <enclosure url="{esc_img}" length="150000" type="image/jpeg" />
      <media:content url="{esc_img}" medium="image" type="image/jpeg" width="1200" height="800">
        <media:title type="plain">{esc_title}</media:title>
      </media:content>
      <media:thumbnail url="{esc_img}" width="1200" height="800" />
    </item>\n"""

    channel_pos = feed.find('<channel>') + len('<channel>')
    feed = feed[:channel_pos] + "\n" + new_feed_item + feed[channel_pos:]
    with open(FEED_XML, 'w', encoding='utf-8') as f:
        f.write(feed)
    print("[OK] Updated feed.xml with new guide")

    # 3. Update sitemap.xml
    print("Updating sitemap.xml...")
    with open(SITEMAP_XML, 'r', encoding='utf-8') as f:
        sitemap = f.read()

    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    sitemap_entry = f"""  <url>
    <loc>https://imtechboss.com/{guide_article['id']}/</loc>
    <lastmod>{today_str}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
    <image:image>
      <image:loc>{esc_img}</image:loc>
      <image:title>{esc_title}</image:title>
    </image:image>
  </url>\n"""

    urlset_pos = sitemap.find('<urlset') 
    end_tag_pos = sitemap.find('>', urlset_pos) + 1
    sitemap = sitemap[:end_tag_pos] + "\n" + sitemap_entry + sitemap[end_tag_pos:]
    with open(SITEMAP_XML, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f"[OK] Added sitemap.xml entry for new guide")

if __name__ == '__main__':
    main()
