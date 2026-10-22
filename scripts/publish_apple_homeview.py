import os, sys, json, re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(ROOT, 'js', 'data.js')
FEED_XML = os.path.join(ROOT, 'feed.xml')
SITEMAP_XML = os.path.join(ROOT, 'sitemap.xml')

homeview_article = {
    "id": "apple-homeview-299-smart-display-a18-chip-facial-recognition-homeos-2026",
    "title": "Apple Unveils HomeView for $299: A18 Silicon, 7-Inch Square Liquid Retina Display, and Multi-User Facial Recognition",
    "excerpt": "Apple has officially entered the dedicated smart display market with Apple HomeView, featuring an A18 chip, a 1088x1088 Liquid Retina touchscreen, iMac G4-inspired countertop acoustics, and camera-based facial recognition for six household members.",
    "category": "Smart Home & IoT",
    "date": "October 15, 2026",
    "readTime": "8 min read",
    "author": "Tech Boss",
    "image": "https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=1200&q=80",
    "content": """<p class="lead text-lg font-medium text-gray-700 dark:text-gray-300 mb-6 leading-relaxed">Apple has officially unveiled the Apple HomeView, a $299 dedicated smart home command center that bridges ambient home automation with on-device Apple Intelligence. Representing Apple's most consequential hardware category launch of late 2026, HomeView combines custom A18 silicon, an edge-to-edge 7-inch square Liquid Retina display, and an iMac G4-inspired domed acoustic base. Pre-orders are live ahead of a November 13 global shipping date, signaling Apple's direct challenge to Amazon Echo Show and Google Nest Hub ecosystems through local privacy and hardware integration.</p>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Hardware Architecture: Countertop Aesthetics and Wall-Mount Options</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Apple designed HomeView in two distinct form factors at the identical $299 price point. The tabletop countertop edition anchors the 7-inch display to a rounded, weighted speaker base via a polished stainless steel tilting hinge, echoing the iconic articulating arm of the early-2000s iMac G4. Available in Silver, Starlight, Rose Pink, and Space Gray, the countertop model blends into kitchens, bedside tables, and home offices.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">For architectural installations, Apple engineered a flush wall-mounted variant in Silver and Space Gray that secures directly over standard single-gang electrical junction boxes or low-voltage wall brackets. The display measures exactly 7 inches diagonally with a unique 1:1 aspect ratio (1088 x 1088 pixels at 220 ppi). The panel covers 500 nits of peak brightness for sunlit kitchens while dropping to an ultra-dim 0.3 nits in nightstand mode, matching the eye-comfort dynamics introduced on the iPhone 16 series.</p>

<div class="my-8 p-6 bg-gray-50 dark:bg-slate-900/60 rounded-2xl border border-gray-200 dark:border-slate-800">
  <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">Apple HomeView Core Specifications</h3>
  <div class="overflow-x-auto">
    <table class="w-full text-left text-sm text-gray-700 dark:text-gray-300">
      <thead>
        <tr class="border-b border-gray-200 dark:border-slate-700 font-bold text-gray-900 dark:text-white">
          <th class="py-2.5">Component</th>
          <th class="py-2.5">Countertop Tabletop Model</th>
          <th class="py-2.5">Flush Wall-Mount Model</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100 dark:divide-slate-800">
        <tr><td class="py-2 font-medium">Retail Price</td><td>$299 / £299</td><td>$299 / £299 (Brackets from $59)</td></tr>
        <tr><td class="py-2 font-medium">Processor</td><td>Apple A18 (6-Core CPU + 16-Core NPU)</td><td>Apple A18 (6-Core CPU + 16-Core NPU)</td></tr>
        <tr><td class="py-2 font-medium">Display</td><td>7-inch Square Liquid Retina (1088x1088, 220 ppi)</td><td>7-inch Square Liquid Retina (1088x1088, 220 ppi)</td></tr>
        <tr><td class="py-2 font-medium">Brightness Range</td><td>0.3 nits minimum to 500 nits peak</td><td>0.3 nits minimum to 500 nits peak</td></tr>
        <tr><td class="py-2 font-medium">Camera System</td><td>12MP Center Stage (f/2.4) with Privacy Shutter</td><td>12MP Center Stage (f/2.4) with Privacy Shutter</td></tr>
        <tr><td class="py-2 font-medium">Speaker Drivers</td><td>Dual full-range drivers + down-firing woofer</td><td>Dual compact high-excursion drivers</td></tr>
        <tr><td class="py-2 font-medium">Wireless Protocols</td><td>Wi-Fi 6E, Bluetooth 6.0, Thread Border Router</td><td>Wi-Fi 6E, Bluetooth 6.0, Thread Border Router</td></tr>
        <tr><td class="py-2 font-medium">Smart Home Standards</td><td>Matter 1.3 Controller, Apple HomeKit</td><td>Matter 1.3 Controller, Apple HomeKit</td></tr>
      </tbody>
    </table>
  </div>
</div>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">A18 Silicon &amp; Facial Recognition: 6-Profile Dynamic Switching</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Unlike competitor smart displays that rely on low-power ARM Cortex-A53 microcontrollers, Apple equipped HomeView with the full A18 application processor fabricated on TSMC's second-generation 3nm (N3E) process. The 16-core Neural Engine processes real-time vision algorithms directly on device, eliminating latency when executing complex smart home triggers.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Using the 12MP ultra-wide Center Stage camera, HomeView implements multi-user facial recognition capable of storing up to six distinct household profiles. When a user walks into the kitchen, the display identifies the individual and dynamically rearranges the HomeOS widget interface: displaying personal calendar appointments, unread Messages summaries, flight alerts, and tailored Apple Music recommendations. Once the user steps away, the screen transitions back to a clean ambient standby clock or family photo carousel, protecting personal privacy.</p>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">Next-Generation Conversational Siri &amp; HomeOS Integration</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">HomeView serves as the premier stationary showcase for Apple Intelligence. Siri on HomeView gains deep screen awareness and natural conversational memory. Users can issue compound, multi-clause instructions without repeating wake words: <em>"Turn down the living room lights to thirty percent, check if the garage door is locked, and show me the backyard security feed."</em></p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">The device operates on HomeOS, an operating system optimized for glanceable touch controls and voice navigation. A persistent smart dock anchors favorite accessories, while automated contextual cards surface relevant camera streams whenever motion is detected at the front door. Through Matter 1.3 and integrated Thread Border Router capabilities, HomeView directly pairs with third-party accessories from Philips Hue, Nanoleaf, Eve, and Aqara without requiring external proprietary bridges.</p>

<div class="my-8 p-6 bg-gray-50 dark:bg-slate-900/60 rounded-2xl border border-gray-200 dark:border-slate-800">
  <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">Audio Engineering &amp; Room Acoustics</h3>
  <ul class="space-y-3 text-sm text-gray-700 dark:text-gray-300">
    <li><strong>Acoustic Architecture:</strong> The countertop base houses two custom full-range transducers coupled with a high-excursion down-firing woofer and dual force-cancelling passive radiators for distortion-free bass response.</li>
    <li><strong>Spatial Audio &amp; Dolby Atmos:</strong> Supports room-filling Spatial Audio playback via Apple Music, creating an immersive acoustic soundstage in medium to large rooms.</li>
    <li><strong>Beamforming Microphone Array:</strong> A studio-grade 4-microphone array utilizes acoustic echo cancellation to isolate voice commands even during high-volume music playback.</li>
    <li><strong>Safety Sound Recognition:</strong> Onboard microphones monitor for smoke and carbon monoxide detector alarms, immediately broadcasting critical notifications to family iPhones and Apple Watches.</li>
  </ul>
</div>

<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mt-8 mb-4">The Apple Home Collection: Strategic Alliances with LG and Schneider</h2>
<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">Coinciding with the HomeView release, Apple introduced the Apple Home Collection, a curated line of smart accessories developed in strategic collaboration with industrial leaders LG Electronics and Schneider Electric. The lineup includes weather-resistant outdoor 4K cameras with encrypted HomeKit Secure Video storage, motorized smart deadbolts with Apple Wallet Home Key support, and smart circuit panel relays that monitor real-time home energy consumption.</p>

<p class="text-base text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">By controlling both the physical hub and the underlying certified accessory pipeline, Apple addresses the fragmentation and unreliability that have hindered smart home adoption over the past decade. Every interaction executes locally across the Thread mesh network, with biometric templates and security video footage protected under Apple's Secure Enclave encryption architecture.</p>

<div class="my-6 p-4 border-l-4 border-blue-600 bg-blue-50/50 dark:bg-blue-950/30 rounded-r-xl">
  <h4 class="font-bold text-blue-900 dark:text-blue-300 mb-1">Tech Boss Lab Verdict</h4>
  <p class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">At $299, the <strong>Apple HomeView</strong> establishes a new benchmark for ambient smart home displays. By pairing flagship A18 processing power with an ultra-responsive 1:1 Liquid Retina display, robust countertop acoustics, and true multi-user facial profile switching, Apple delivers a refined, privacy-first command center that outclasses generic smart displays and solidifies the HomeOS ecosystem for years to come.</p>
</div>"""
}

def main():
    print("============================================================")
    print("PUBLISHING APPLE HOMEVIEW TO TECH BOSS")
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
    articles.insert(0, homeview_article)

    updated_json = json.dumps(articles, indent=2, ensure_ascii=False)
    new_content = f"var initialArticles = {updated_json};\n"

    with open(DATA_JS, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Added Apple HomeView to Index 0 in js/data.js. Total articles: {len(articles)}")

    # 2. Update feed.xml
    print("Updating feed.xml...")
    with open(FEED_XML, 'r', encoding='utf-8') as f:
        feed = f.read()

    now_rfc822 = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    esc_img = homeview_article["image"].replace("&", "&amp;")
    esc_title = homeview_article["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    esc_desc = homeview_article["excerpt"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    esc_cat = homeview_article["category"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    new_feed_item = f"""    <item>
      <title>{esc_title}</title>
      <link>https://imtechboss.com/{homeview_article['id']}/</link>
      <guid isPermaLink="true">https://imtechboss.com/{homeview_article['id']}/</guid>
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
    print("[OK] Updated feed.xml with Apple HomeView")

    # 3. Update sitemap.xml
    print("Updating sitemap.xml...")
    with open(SITEMAP_XML, 'r', encoding='utf-8') as f:
        sitemap = f.read()

    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    sitemap_entry = f"""  <url>
    <loc>https://imtechboss.com/{homeview_article['id']}/</loc>
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
    print(f"[OK] Added sitemap.xml entry for Apple HomeView")

if __name__ == '__main__':
    main()
