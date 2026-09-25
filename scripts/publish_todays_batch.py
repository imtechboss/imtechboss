import json, re, os, datetime

new_articles = [
    {
        "id": "meta-unveils-orion-holographic-ar-glasses-silicon-carbide-neural-wristband-2026",
        "title": "Meta Unveils Orion Holographic AR Glasses: Silicon Carbide Lenses and Neural Wristband Interface Detailed",
        "excerpt": "Meta has pulled back the curtain on Orion, a standalone 98-gram holographic augmented reality prototype engineered with custom silicon carbide optical waveguides and an electromyography neural wristband that reads motor neuron impulses.",
        "category": "AI & Technology",
        "date": "2026-09-25",
        "author": "Tech Boss",
        "image": "https://images.unsplash.com/photo-1592478411213-6153e4ebc07d?auto=format&fit=crop&w=1200&q=80",
        "readTime": "6 min read",
        "featured": True,
        "tags": [
            "Meta",
            "Orion",
            "Augmented Reality",
            "AR Glasses",
            "Wearables",
            "Silicon Carbide",
            "AI Hardware"
        ],
        "content": """<p>After a decade of secretive research inside Reality Labs and billions of dollars in specialized optical prototyping, Meta CEO Mark Zuckerberg has publicly demonstrated <strong>Orion</strong>. Unlike bulky mixed-reality headsets such as the Apple Vision Pro or Meta Quest 3, Orion is packaged into thick-rimmed glasses weighing just 98 grams. The prototype represents a major technical achievement in micro-optics, custom silicon miniaturization, and neural input architecture.</p>

<h2>Why Silicon Carbide Replaced Optical Glass</h2>
<p>The primary barrier holding back consumer augmented reality has always been optical physics: balancing field of view (FOV) with light efficiency and frame weight. Most existing smart glasses use resin or standard optical glass waveguides, restricting their diagonal display window to a narrow 30-to-40-degree field of view that feels like looking at floating graphics through a mailbox slot.</p>

<p>For Orion, Meta abandoned traditional glass entirely and spent years manufacturing waveguides from synthetic <strong>silicon carbide</strong>. Silicon carbide offers critical physical properties:</p>
<ul>
  <li><strong>Extreme Refractive Index (2.7):</strong> Compared to optical glass (1.5) or polycarbonate (1.58), silicon carbide bends light at much sharper internal angles. This enables an expansive <strong>70-degree diagonal field of view</strong> without thick edge lenses.</li>
  <li><strong>Thermal Stability:</strong> Silicon carbide does not warp or introduce optical aberrations as micro-LED projectors heat up during prolonged operation.</li>
  <li><strong>Structural Rigidity:</strong> The material provides extreme hardness, allowing lens elements to remain thin while resisting drops and impacts.</li>
</ul>

<p>Pairing these waveguides with pairs of sub-micron Micro-LED projectors capable of pumping out millions of nits ensures holographic text, browser windows, and full-scale 3D models remain legible even under direct outdoor sunlight.</p>

<h2>The EMG Neural Wristband: Control Without Arm Fatigue</h2>
<p>The most radical departure from traditional user interfaces is how wearers navigate Orion's software. Rather than forcing users to hold their hands up in front of optical cameras to pinch virtual buttons—a motion that causes severe shoulder fatigue within minutes—Orion relies on a lightweight <strong>electromyography (EMG) wristband</strong>.</p>

<p>The wristband uses medical-grade sensors to detect electrical motor neuron impulses traveling down the arm into the wrist. When your brain decides to pinch your index finger and thumb, the wristband detects the electrical twitch fractions of a millisecond before your fingers physically touch. This enables micro-gestures: resting your hand casually in your pocket or on your lap while scrolling through messages or confirming prompts with zero visible hand motion.</p>

<h2>Distributed Computing Architecture: The Wireless Puck</h2>
<p>To keep the glasses under 100 grams without cooking the wearer's temples, Meta offloaded heavy computation to an external wireless compute puck. The glasses house dual custom processors responsible for sensor fusion, low-latency spatial audio, and head tracking. Graphic rendering, spatial anchoring, and multi-modal AI reasoning run on the puck via a proprietary, ultra-low-latency wireless protocol.</p>

<p>On-device cameras track eye gaze to determine what the user is inspecting. If a wearer looks at ingredients inside their refrigerator, integrated multi-modal AI recognizes items in real time, overlays floating recipe cards, and speaks guidance through directional speakers built into the magnesium temple arms.</p>

<h2>Roadmap to Consumer Production</h2>
<p>Orion is not hitting store shelves immediately. Because manufacturing high-purity silicon carbide wafers in optical grades remains prohibitively expensive, each prototype costs thousands of dollars to assemble. Meta is currently distributing hundreds of Orion developer kits to internal teams and external partners while refining mass-manufacturing processes to bring consumer-ready units to market within the next few hardware cycles.</p>"""
    },
    {
        "id": "amd-ryzen-7-9800x3d-inverts-3d-v-cache-architecture-full-overclocking-unlocked-2026",
        "title": "AMD Ryzen 7 9800X3D Inverts 3D V-Cache Architecture: Thermal Redesign Unlocks Full Overclocking for PC Gamers",
        "excerpt": "AMD's upcoming Zen 5 Ryzen 7 9800X3D flips its cache stacking orientation, placing the 64MB SRAM cache die underneath the Core Complex Die to expose compute cores directly to the integrated heat spreader and enable unrestricted multiplier overclocking.",
        "category": "Hardware",
        "date": "2026-09-25",
        "author": "Tech Boss",
        "image": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=1200&q=80",
        "readTime": "5 min read",
        "featured": True,
        "tags": [
            "AMD",
            "Ryzen 7 9800X3D",
            "Zen 5",
            "3D V-Cache",
            "Overclocking",
            "PC Hardware",
            "Gaming CPU"
        ],
        "content": """<p>When AMD unveiled the Ryzen 7 5800X3D and subsequent Ryzen 7 7800X3D, the chips quickly established themselves as undisputed monarchs of gaming performance. By vertically bonding an extra 64MB of high-density SRAM cache directly to the silicon die, AMD dramatically reduced high-latency roundtrips to system RAM. Yet, both processors suffered from a critical limitation: rigid thermal constraints that forced AMD to lock core voltage and disable manual multiplier overclocking.</p>

<p>With the impending arrival of the <strong>Ryzen 7 9800X3D</strong> built on the Zen 5 "Granite Ridge" architecture, leaked packaging and engineering documentation reveal that AMD has completely inverted its 3D die-stacking configuration to conquer thermal bottlenecks and unlock full overclocking headroom.</p>

<h2>The Thermal Flaw of 1st and 2nd Gen 3D V-Cache</h2>
<p>In previous X3D designs, the 64MB 3D V-Cache die was bonded directly on top of the Core Complex Die (CCD). To ensure even mechanical height across the package, structural silicon shims were placed over the remaining area of the CPU cores.</p>

<p>This layout created a severe thermodynamic penalty. Silicon is an effective heat insulator. Because the sensitive SRAM cache was sandwiched between the blazing-hot compute cores and the copper Integrated Heat Spreader (IHS), heat produced by the Zen 4 execution engines had to migrate upward through the cache layer before reaching the CPU cooler. To prevent thermal degradation of the cache retention cells, AMD enforced strict voltage caps (roughly 1.15V&ndash;1.20V) and dialed down maximum single-core boost clocks by several hundred megahertz compared to non-X3D variants.</p>

<h2>Inverted Stacking: Cache Below, Cores on Top</h2>
<p>For the Zen 5 generation, AMD semiconductor packaging engineers re-engineered the through-silicon via (TSV) interconnects to flip the physical stacking order:</p>
<ol>
  <li><strong>SRAM Cache on the Substrate:</strong> The 64MB 3D V-Cache die is now positioned directly on the organic package substrate at the bottom of the stack.</li>
  <li><strong>Compute Die on Top:</strong> The active Zen 5 Core Complex Die (housing 8 high-performance cores and 16 threads) sits directly on top of the cache.</li>
  <li><strong>Direct Thermal Contact:</strong> The compute cores now make direct surface contact with the CPU's gold-plated copper heat spreader.</li>
</ol>

<p>This inverted geometry fundamentally alters thermal dissipation dynamics. High-wattage heat generated during intense gaming bursts transfers straight into liquid cooling blocks or air coolers without cooking the cache below. As a direct result, AMD has eliminated the artificial frequency deficit. The Ryzen 7 9800X3D is reported to feature an out-of-the-box base clock of 4.7 GHz and boost ceilings pushing past <strong>5.2 GHz</strong>.</p>

<h2>Full Multiplier Overclocking Confirmed</h2>
<p>Because thermal transfer efficiency is no longer compromised, motherboard manufacturers confirm that the 9800X3D will be the first fully unlocked 3D V-Cache processor in history. Enthusiasts will enjoy unrestricted access to:</p>
<ul>
  <li><strong>Manual Core Multipliers:</strong> Push all-core frequencies beyond 5.4 GHz on premium X870 and X670E motherboards with sufficient cooling.</li>
  <li><strong>Precision Boost Overdrive (PBO) & Curve Optimizer:</strong> Fine-tune per-core voltage-frequency curves to extract maximum efficiency.</li>
  <li><strong>Extreme Memory Profiles (EXPO):</strong> Tighter sub-timing tuning and high-speed DDR5-6000+ support without memory controller stability degradation.</li>
</ul>

<h2>Expected Gaming Impact</h2>
<p>While standard productivity benchmarks will benefit from Zen 5's wider 6-wide dispatch engine and native 512-bit AVX-512 data paths, gaming remains the primary target. Titles notorious for heavy CPU simulation bottlenecks—such as <em>Microsoft Flight Simulator 2024</em>, <em>Baldur's Gate 3</em>, and <em>Escape from Tarkov</em>—will see massive improvements in 1% and 0.1% low frametimes, eliminating micro-stutters during heavy multiplayer encounters. The Ryzen 7 9800X3D is set to reinforce AMD's dominant position at the apex of gaming hardware.</p>"""
    },
    {
        "id": "microsoft-windows-11-24h2-recall-security-overhaul-opt-in-bitlocker-enclave-2026",
        "title": "Microsoft Re-Engineers Windows 11 Recall: Mandatory Opt-In, BitLocker Enclave, and Windows Hello Protection Explained",
        "excerpt": "Following intense backlash from cybersecurity researchers, Microsoft has completely restructured Windows 11's AI-powered Recall feature into a zero-trust architecture requiring hardware-bound encryption keys and biometric verification for every data query.",
        "category": "Software & Utilities",
        "date": "2026-09-25",
        "author": "Tech Boss",
        "image": "https://images.unsplash.com/photo-1618401471353-b98aedd04e11?auto=format&fit=crop&w=1200&q=80",
        "readTime": "5 min read",
        "featured": True,
        "tags": [
            "Windows 11",
            "Microsoft",
            "Recall",
            "Copilot+",
            "Cybersecurity",
            "Encryption",
            "Artificial Intelligence"
        ],
        "content": """<p>When Microsoft first showcased <strong>Windows Recall</strong> as the centerpiece of its Copilot+ PC initiative in mid-2024, the tech giant envisioned an intelligent photographic memory for desktop computing. By taking periodic high-resolution snapshots of a user's screen every few seconds and indexing them with on-device multi-modal small language models, Recall promised to let users search their entire digital timeline using conversational natural language.</p>

<p>Instead, the feature triggered one of the most severe cybersecurity backlashes in modern computing history. White-hat security researchers quickly revealed that original preview builds stored optical character recognition (OCR) plain text and screen metadata inside an unencrypted SQLite database directly within user directories. Info-stealing trojans and unauthorized local users could extract months of banking details, passwords, and confidential emails in seconds. Recognizing the crisis, Microsoft postponed the rollout to execute a complete architectural redesign.</p>

<h2>1. 100% Opt-In: Zero Silent Activation</h2>
<p>The revised Recall experience in <strong>Windows 11 version 24H2</strong> strips away silent automatic activation. During initial device setup (Out of Box Experience), users are presented with a clear, full-screen prompt asking whether they wish to enable Recall. If a user declines, the snapshot pipeline remains completely dormant.</p>

<p>Furthermore, Microsoft has added granular control options that allow corporate IT administrators and private users to completely uninstall Recall binaries from the operating system via "Turn Windows features on or off," satisfying enterprise compliance mandates across Europe and North America.</p>

<h2>2. Virtualization-Based Security (VBS) Enclave Protection</h2>
<p>To eliminate the risk of local database scraping, Microsoft moved the entire processing and storage pipeline behind hardware-isolated <strong>Virtualization-Based Security (VBS) Enclaves</strong>. This architecture fundamentally isolates Recall from the rest of the Windows kernel:</p>
<ul>
  <li><strong>Cryptographic Binding to TPM 2.0:</strong> Encryption keys securing snapshots and search indices are bound to the motherboard's Trusted Platform Module (TPM 2.0). Even if a malicious attacker removes the NVMe storage drive and connects it to a second computer, the data cannot be decrypted.</li>
  <li><strong>Just-In-Time Decryption:</strong> Snapshots remain encrypted at rest. When a user executes a search, only the specific requested snapshot is decrypted momentarily in protected RAM before returning to an encrypted state.</li>
  <li><strong>Malware Isolation:</strong> Even if a trojan achieves administrative kernel rights on the host operating system, it cannot inspect memory allocated inside the secure VBS enclave.</li>
</ul>

<h2>3. Mandatory Windows Hello Biometric Authorization</h2>
<p>Under the revised protocol, access to Recall's timeline interface is directly tied to <strong>Windows Hello Enhanced Sign-in Security (ESS)</strong>. Opening the Recall search bar or viewing past snapshots requires active biometric verification—either through facial recognition, a fingerprint sensor, or a secure hardware-backed PIN.</p>

<p>If an employee steps away from their laptop in a coffee shop or shared office, an unauthorized bystander cannot scroll back through previous browser tabs or documents, because the system requests biometric confirmation before rendering any saved visual history.</p>

<h2>4. Native Filtering for Sensitive Financial and Password Data</h2>
<p>To address concerns surrounding sensitive credential leakage, Microsoft integrated real-time heuristics and on-device computer vision filters. Recall automatically detects credit card numbers, national identification credentials, and password input fields, dropping frames before they are committed to storage.</p>

<p>Additionally, private browsing sessions in Google Chrome, Microsoft Edge, Mozilla Firefox, and other Chromium browsers are automatically blacklisted from the snapshot schedule. Users can also designate specific applications or confidential websites that Recall is permanently prohibited from observing.</p>

<h2>The Verdict: A Model for Responsible On-Device AI</h2>
<p>While the initial announcement of Recall highlighted the perils of rushing AI features without thorough threat modeling, Microsoft's comprehensive security overhaul sets a new standard for on-device generative intelligence. By anchoring data processing to dedicated Neural Processing Units (NPUs) and securing storage behind hardware enclaves, Windows 11 demonstrates that personal computing utilities can deliver cutting-edge assistance without sacrificing user sovereignty and data privacy.</p>"""
    }
]

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, 'js', 'data.js')

with open(data_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', content, re.DOTALL)
if not match:
    print("Error: initialArticles array not found in data.js")
    exit(1)

existing_articles = json.loads(match.group(1))

# Check for banned words in new articles
banned_words = ['delve', 'landscape', 'pivotal', 'testament', 'game-changer', 'in conclusion', 'tapestries', 'realm', 'beacon', 'seamlessly']
for a in new_articles:
    full_text = a['title'] + " " + a['excerpt'] + " " + a['content']
    for bw in banned_words:
        if re.search(r'\b' + bw + r'\b', full_text, re.IGNORECASE):
            print(f"ERROR: Banned word '{bw}' found in article '{a['title']}'!")
            exit(1)

print("PASS: 0 banned AI cliché words in new articles.")

combined = new_articles + existing_articles

new_data_js = f"var initialArticles = {json.dumps(combined, indent=2, ensure_ascii=False)};\n"
with open(data_path, 'w', encoding='utf-8') as f:
    f.write(new_data_js)

print(f"Updated data.js: now {len(combined)} articles (added {len(new_articles)} new).")

# Update feed.xml
feed_path = os.path.join(base_dir, 'feed.xml')
with open(feed_path, 'r', encoding='utf-8') as f:
    feed_content = f.read()

channel_marker = '<channel>'
idx = feed_content.find(channel_marker)
if idx != -1:
    insert_pos = feed_content.find('>', idx) + 1
    new_items_xml = ""
    for a in new_articles:
        pub_date = datetime.datetime.strptime(a['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 12:00:00 +0000')
        safe_title = a['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        safe_desc = a['excerpt'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        url = f"https://imtechboss.com/post.html?id={a['id']}"
        img = a['image']
        cat = a['category']
        new_items_xml += f"""
    <item>
      <title>{safe_title}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <description>{safe_desc}</description>
      <category>{cat}</category>
      <pubDate>{pub_date}</pubDate>
      <media:content url="{img}" medium="image" width="1200" height="800" />
      <media:thumbnail url="{img}" width="1200" height="800" />
      <enclosure url="{img}" type="image/jpeg" length="150000" />
    </item>"""
    
    updated_feed = feed_content[:insert_pos] + new_items_xml + feed_content[insert_pos:]
    with open(feed_path, 'w', encoding='utf-8') as f:
        f.write(updated_feed)
    print("Updated feed.xml with 3 new items.")

