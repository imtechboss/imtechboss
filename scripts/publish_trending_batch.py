import json, re, os, datetime
import xml.etree.ElementTree as ET

new_articles = [
    {
        "id": "nvidia-rtx-5090-600w-tdp-12v-2x6-power-connector-melting-concerns-2026",
        "title": "NVIDIA RTX 5090 Hits 600W TDP: Why the Revised 12V-2x6 Power Connector is Reigniting Melting Fears for PC Builders",
        "excerpt": "Internal testing logs reveal NVIDIA's upcoming GeForce RTX 5090 pushes total board power to 600 watts, triggering intense scrutiny over the revised 12V-2x6 power connector and mandatory 1000W ATX 3.1 power supply requirements.",
        "category": "Hardware",
        "date": "2026-09-24",
        "author": "Tech Boss",
        "image": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=1200&q=80",
        "readTime": "6 min read",
        "featured": True,
        "tags": [
            "Nvidia",
            "RTX 5090",
            "Blackwell",
            "PC Hardware",
            "GPU",
            "Power Supply",
            "Gaming"
        ],
        "content": """<p>As board partners finalize reference coolers and PCB revisions for NVIDIA's next-generation Blackwell consumer graphics architecture, verified power profiling data indicates that the flagship <strong>GeForce RTX 5090</strong> demands a massive 600-watt Total Board Power (TBP) budget. This dramatic 150W escalation over the RTX 4090 has ignited heated arguments among system builders, custom PC system integrators, and electrical engineers regarding the safety and thermal reliability of the revised 12V-2x6 power connector.</p>

<h2>The Evolution from 12VHPWR to 12V-2x6</h2>
<p>When NVIDIA introduced the original 12VHPWR (PCIe 5.0) 16-pin connector on the RTX 4090 in late 2022, high-profile reports of burnt terminal blocks and melted plastic sockets dominated enthusiast forums. Investigations by independent lab engineers revealed that slight terminal misalignment, incomplete terminal seating, or severe horizontal cable bending generated high resistance contact patches capable of hitting 150&deg;C under full load.</p>

<p>In response, the PCI-SIG revised the standard, introducing the <strong>12V-2x6 (CEM 5.1)</strong> specification. The updated connector features critical safety adjustments:</p>
<ul>
  <li><strong>Recessed Sense Pins:</strong> Sense pins (S1&ndash;S4) were shortened by 1.7mm. If the connector is even slightly unseated by as little as 1mm, the power supply detects an open circuit and drops allowable wattage from 600W to 150W or refuses initialization entirely.</li>
  <li><strong>Lengthened Power Terminals:</strong> Current-carrying conductor pins were extended by 0.25mm to increase physical surface contact depth inside the mating plug.</li>
  <li><strong>Thicker Conductor Walls:</strong> Internal copper spring clips were reinforced to maintain clamping force under thermal expansion cycles.</li>
</ul>

<h2>Why 600W Pushes Physics to the Limit</h2>
<p>While the mechanical improvements of 12V-2x6 dramatically reduce accidental user installation errors, sustaining a continuous 600W electrical current across a compact 16-pin interface presents sheer thermodynamic reality. Delivering 600W across six active 12V pins requires approximately 8.33 amps per pin under continuous load.</p>

<p>During intense compute spikes and burst ray tracing passes in titles like <em>Cyberpunk 2077</em> with path tracing, transient microsecond excursions can spike total instantaneous draw well beyond 750 watts. High-current loads passing through micro-terminals naturally produce resistive heat. In poorly ventilated mid-tower chassis cases where ambient internal temperature exceeds 45&deg;C, thermal headroom on the power connector remains perilously thin.</p>

<h2>Power Supply Mandates: Why ATX 3.1 Is Non-Negotiable</h2>
<p>Building an enthusiast gaming workstation around the RTX 5090 will require widespread infrastructure upgrades. System builders must evaluate several core power requirements:</p>
<ol>
  <li><strong>Minimum 1000W to 1200W PSU:</strong> A standard 850W power supply will face instant Over Current Protection (OCP) shutdowns when paired with modern high-wattage desktop processors like the Intel Core i9-14900KS or AMD Ryzen 9 9950X.</li>
  <li><strong>Native 12V-2x6 Cables:</strong> Avoid daisy-chained multi-8-pin PCIe adapter splitters. Native cables designed specifically for ATX 3.1 modular supplies reduce junction resistance by eliminating extra terminal crimp hops.</li>
  <li><strong>Zero Cable Bend Radius within 35mm:</strong> Hardware manufacturers explicitly warn that cables must remain straight for at least 35mm from the GPU power receptacle before initiating any bend toward side panels.</li>
</ol>

<h2>The Verdict for Enthusiast Upgraders</h2>
<p>The GeForce RTX 5090 is shaping up to deliver historic rasterization and tensor compute throughput. However, raw performance scaling is clearly arriving at the expense of electrical efficiency. PC builders preparing for the Blackwell generation must treat power delivery and thermal chassis airflow with the same meticulous engineering discipline previously reserved for industrial workstations.</p>"""
    },
    {
        "id": "sony-ps5-pro-pssr-300-tops-neural-engine-4k-60fps-ray-tracing-2026",
        "title": "Sony PS5 Pro PSSR Tested: 300 TOPS Custom Neural Engine Delivers 4K 60FPS Ray Tracing Across 50+ Launch Titles",
        "excerpt": "Sony's PlayStation 5 Pro introduces custom machine learning hardware rated at 300 TOPS, enabling PlayStation Spectral Super Resolution (PSSR) to deliver sharp 4K presentation at a locked 60 frames per second without typical temporal artifacts.",
        "category": "Gaming",
        "date": "2026-09-24",
        "author": "Tech Boss",
        "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=1200&q=80",
        "readTime": "5 min read",
        "featured": True,
        "tags": [
            "PS5 Pro",
            "Sony",
            "PlayStation",
            "PSSR",
            "Gaming",
            "Ray Tracing",
            "Consoles"
        ],
        "content": """<p>For the past four years, console gamers have faced a frustrating compromise: choose "Fidelity Mode" for crisp 4K visuals at a sluggish 30 frames per second, or select "Performance Mode" to gain fluid 60FPS at the expense of muddy 1080p internal render resolutions and aggressive dynamic resolution scaling. With the deployment of the <strong>PlayStation 5 Pro</strong>, Sony aims to abolish that compromise entirely through a proprietary machine learning upscaling pipeline known as <strong>PSSR (PlayStation Spectral Super Resolution)</strong>.</p>

<h2>The 300 TOPS Neural Architecture Inside PS5 Pro</h2>
<p>Unlike traditional temporal anti-aliasing upscalers like AMD FSR 2 or FSR 3—which rely purely on hand-crafted spatial heuristics and motion vectors executed across standard GPU compute units—PSSR is powered by dedicated silicon. Sony worked alongside AMD to bake a custom neural processing block into the PS5 Pro system-on-chip (SoC), rated at approximately <strong>300 TOPS (Tera Operations Per Second)</strong> of 8-bit int computation.</p>

<p>This dedicated machine learning block functions similarly to NVIDIA's Tensor Core array. Instead of consuming general rasterization shaders to reconstruct image geometry, PSSR offloads frame upscaling to the neural block. The neural model was trained on millions of multi-frame reference ground-truth gaming captures, enabling it to recognize sub-pixel detail, foliage edges, and specular reflections that traditional algorithm-based upscalers inadvertently blur or smear.</p>

<h2>Real-World Testing: 50+ Launch Titles Under the Microscope</h2>
<p>Early performance analyses across a verified lineup of over 50 "PS5 Pro Enhanced" titles reveal substantial upgrades in frame pacing and image clarity:</p>
<ul>
  <li><strong>Marvel's Spider-Man 2:</strong> Maintains a locked 60FPS while rendering ray-traced reflections on city skyscrapers at a full reconstructed 4K presentation, eliminating the flickering edge artifacts visible on base hardware.</li>
  <li><strong>Final Fantasy VII Rebirth:</strong> Fixes the notoriously soft and blurred presentation of the base PS5's Performance Mode. Internal resolution scales from 1152p directly to clean 4K without loss of skin micro-textures or foliage sharpness.</li>
  <li><strong>Gran Turismo 7:</strong> Enables experimental 8K output modes on supported displays alongside real-time ray-traced car reflections on vehicle paint during competitive online races.</li>
</ul>

<h2>The 45% GPU Leap and Enhanced Ray Tracing Engine</h2>
<p>PSSR does not operate in isolation. The graphics core of the PS5 Pro incorporates AMD's latest RDNA architectural improvements, boasting 67% more Compute Units than the standard model. Combined with 28% faster GDDR6 memory bandwidth, raw GPU rendering throughput increases by approximately 45%.</p>

<p>Crucially, ray tracing hardware has been upgraded to a dedicated traversal coprocessor capable of casting two to three times more intersection rays per cycle. This architectural shift prevents heavy path-traced lighting pipelines from stalling the main shader pipeline when multiple reflective surfaces collide on screen.</p>

<h2>A Turning Point for Living Room Graphics</h2>
<p>At a $699 price point without an optical disc drive, the PS5 Pro represents a premium enthusiast hardware upgrade rather than a mainstream replacement. However, from a pure computer engineering standpoint, PSSR proves that machine learning image reconstruction has become mandatory for modern rendering. Handcrafted algorithms have hit their limit, and neural super-resolution is now the official standard for high-performance console gaming.</p>"""
    },
    {
        "id": "snapdragon-8-elite-vs-dimensity-9400-3nm-oryon-cortex-x925-benchmark-2026",
        "title": "Snapdragon 8 Elite vs Dimensity 9400: Qualcomm’s 4.32GHz Oryon Architecture Clashes with MediaTek’s All-Big-Core Beast",
        "excerpt": "TSMC's second-generation 3nm node hosts the fiercest silicon rivalry in mobile history, pitting Qualcomm's custom 4.32GHz Oryon CPU cores directly against MediaTek's audacious All-Big-Core Dimensity 9400 architecture.",
        "category": "Smartphones",
        "date": "2026-09-24",
        "author": "Tech Boss",
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1200&q=80",
        "readTime": "5 min read",
        "featured": True,
        "tags": [
            "Snapdragon 8 Elite",
            "Dimensity 9400",
            "Qualcomm",
            "MediaTek",
            "Smartphones",
            "Mobile Chips",
            "Processors"
        ],
        "content": """<p>The annual flagship mobile processor cycle has arrived, and the stakes have never been higher. Both Qualcomm and MediaTek have abandoned conventional incremental silicon designs in favor of radical architectural pivots fabricated on TSMC's cutting-edge second-generation 3nm (N3E) process. Qualcomm has retired its Kryo branding entirely to introduce the <strong>Snapdragon 8 Elite</strong>, powered by custom Oryon desktop CPU cores. Meanwhile, MediaTek doubles down on its brute-force philosophy with the <strong>Dimensity 9400</strong>, featuring an all-big-core cluster devoid of efficiency cores.</p>

<h2>CPU Battle: 4.32GHz Oryon vs Cortex-X925 All-Big-Core</h2>
<p>The central clash lies in fundamental CPU design philosophies:</p>
<ul>
  <li><strong>Snapdragon 8 Elite:</strong> Features two custom "Prime" Oryon cores clocked at an astonishing <strong>4.32 GHz</strong>, accompanied by six performance cores running at 3.53 GHz. Qualcomm has eliminated efficiency cores completely, relying on the massive instruction-level efficiency of Oryon to handle background idle tasks. Geekbench 6 single-core results push past 3,200 points—surpassing Apple's A18 Pro in sustained throughput.</li>
  <li><strong>Dimensity 9400:</strong> Deploys a single Arm Cortex-X925 ultra-core clocked at 3.62 GHz, backed by three Cortex-X4 cores at 3.3 GHz, and four Cortex-A720 big cores at 2.4 GHz. By packing four total X-series heavy cores into a mobile thermal envelope, MediaTek dominates heavy multi-threaded compiling and video rendering with Geekbench multi-core marks topping 10,000 points.</li>
</ul>

<h2>Graphics Showdown: Adreno Sliced vs Immortalis-G925</h2>
<p>Mobile gaming demands consistent thermal stability under sustained 3D loads. In graphics hardware, both chipmakers deliver major architectural enhancements:</p>
<p>Qualcomm's redesigned <strong>Adreno GPU</strong> introduces sliced architecture, giving each compute slice its own dedicated memory pipeline. This yields a 40% performance gain while slashing power consumption by 40% during extended <em>Honkai: Star Rail</em> and <em>Genshin Impact</em> gameplay. Qualcomm also integrates native support for Unreal Engine 5.3's Nanite geometry virtualization directly into silicon.</p>

<p>MediaTek counters with the 12-core <strong>Immortalis-G925 MC12</strong>. MediaTek boasts a 41% peak performance improvement and a massive 52% uplift in hardware ray-tracing throughput. In ray-traced reflections benchmarks, the Immortalis-G925 edges out Qualcomm, delivering smoother specular highlights in next-gen mobile titles.</p>

<h2>AI Engines: On-Device LoRA vs 50 Tokens/Second LLMs</h2>
<p>Both silicon giants have aggressively expanded their neural processing units (NPUs) to execute multi-modal AI agents locally without cloud latency:</p>
<ul>
  <li>The Snapdragon 8 Elite's upgraded Hexagon NPU delivers 45% faster execution, capable of sustaining 70+ tokens per second on localized 7-billion parameter language models.</li>
  <li>MediaTek's 8th-generation NPU 890 supports high-speed on-device LoRA (Low-Rank Adaptation) model training, allowing users to fine-tune personal AI image generators directly on their smartphone hardware without uploading personal photos to external servers.</li>
</ul>

<h2>Thermal Reality and Sustained Performance</h2>
<p>While theoretical peak benchmarks shatter previous records, the true test will unfold in retail devices from OnePlus, Xiaomi, Vivo, and Samsung. Dissipating upward of 14W to 18W of peak burst wattage in a sealed glass smartphone body demands advanced dual-layer vapor chambers. Regardless of which silicon takes the crown, 2026 heralds the arrival of true desktop-grade computing power directly in our pockets.</p>"""
    },
    {
        "id": "inside-openai-o1-test-time-compute-chain-of-thought-hardware-scaling-2026",
        "title": "Inside OpenAI o1: How Test-Time Compute and Chain-of-Thought Scaling Are Reshaping AI Data Center Hardware",
        "excerpt": "OpenAI's o1 model shifts the computational paradigm from massive pre-training runs to dynamic test-time inference, driving unprecedented demand for low-latency HBM3e memory across enterprise GPU clusters.",
        "category": "AI & Technology",
        "date": "2026-09-24",
        "author": "Tech Boss",
        "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=80",
        "readTime": "6 min read",
        "featured": True,
        "tags": [
            "OpenAI",
            "AI Hardware",
            "o1",
            "Machine Learning",
            "Nvidia",
            "Data Centers",
            "Semiconductors"
        ],
        "content": """<p>For the past five years, the scaling laws governing artificial intelligence progress followed a singular formula: feed larger parameter counts into bigger GPU superclusters during the pre-training phase. However, as frontier labs face diminishing returns from web-scraped training tokens, OpenAI has unveiled a monumental shift in computational strategy with <strong>OpenAI o1</strong> (internally codenamed <em>Strawberry</em>). Rather than spending all computational horsepower before deployment, o1 introduces massive <strong>test-time compute scaling</strong>.</p>

<h2>What Is Test-Time Compute Scaling?</h2>
<p>In standard transformer models like GPT-4o, the model generates output tokens sequentially based on probabilistic next-token predictions, expending roughly the same fixed compute per output character regardless of question complexity. Ask it to spell a word or solve a quantum physics differential equation, and the compute expenditure per token remains nearly identical.</p>

<p>OpenAI o1 fundamentally re-engineers this mechanism. Before surfacing a final response, the model generates an internal, hidden "chain of thought." It formulates intermediate hypotheses, evaluates edge cases, debugs its own mathematical deductions, and backtracks when a reasoning branch fails. Crucially, the more compute time the model is allocated during inference, the higher its reasoning accuracy scales.</p>

<h2>Benchmark Proof: Beating Human PhD Competitors</h2>
<p>The practical results of test-time search algorithms are dramatic across quantitative disciplines:</p>
<ul>
  <li><strong>International Mathematics Olympiad (IMO):</strong> GPT-4 correctly solved only 13% of qualifying problems. OpenAI o1 scored an astonishing 83%, placing it among the top human high school math competitors on Earth.</li>
  <li><strong>Competitive Coding (Codeforces):</strong> o1 reached the 89th percentile among human elite software engineers, demonstrating self-correction during code generation by simulating execution loops internally.</li>
  <li><strong>Doctoral Science Questions (GPQA Diamond):</strong> Surpassed human expert PhD accuracy on complex chemistry, physics, and molecular biology diagnostic exams.</li>
</ul>

<h2>The Hardware Shockwave: VRAM and Inference Clusters</h2>
<p>While o1 represents a scientific triumph, its operational characteristics represent an earthquake for cloud data center architectures:</p>

<h3>1. Explosive Key-Value (KV) Cache Memory Demands</h3>
<p>Because o1 can generate thousands of hidden "thinking" tokens before presenting a 50-word answer, the attention Key-Value cache balloons rapidly. Maintaining massive context buffers for thousands of concurrent users requires vast pools of ultra-high-bandwidth memory (HBM3e), accelerating demand for 192GB and 288GB GPU configurations like the Nvidia H200 and Blackwell B200.</p>

<h3>2. The Shift from Training to Serving Infrastructure</h3>
<p>Historically, hardware vendors structured procurement around monolithic training superclusters interconnected via InfiniBand networks. With test-time compute, inference servers are no longer lightweight endpoints running 8-bit quantized models; they are high-powered compute engines consuming sustained megawatts of electricity to evaluate dynamic reasoning trees.</p>

<h3>3. Latency vs Accuracy Economics</h3>
<p>Users accustomed to instant 100-token-per-second responses must adapt to waiting 10 to 30 seconds while the model "thinks." In enterprise settings—such as autonomous medical diagnosis, automated aerospace engineering, or cryptographic audits—exchanging 20 seconds of latency for a 99% accuracy rate is an overwhelmingly profitable trade.</p>

<h2>The Future of Reasoning Systems</h2>
<p>OpenAI o1 marks the dawn of a second scaling era. As algorithmic breakthroughs shift the computational bottleneck from static pre-training data availability to dynamic real-time reasoning search, the semiconductor race will prioritize memory bandwidth, high-speed chip-to-chip interconnects, and specialized inference accelerators over raw FP32 compute density.</p>"""
    },
    {
        "id": "valve-steamos-expands-asus-rog-ally-x-lenovo-legion-go-windows-11-2026",
        "title": "Valve Expands SteamOS to Rival Handhelds: ASUS ROG Ally X and Lenovo Legion Go Set to Ditch Windows 11",
        "excerpt": "Valve is preparing official SteamOS dual-boot and standalone installers for rival AMD Z1 Extreme handhelds, replacing Windows 11 bloatware with dedicated Proton micro-compositor optimizations that reclaim 20% gaming battery life.",
        "category": "Gaming",
        "date": "2026-09-24",
        "author": "Tech Boss",
        "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80",
        "readTime": "5 min read",
        "featured": True,
        "tags": [
            "SteamOS",
            "Valve",
            "ASUS ROG Ally",
            "Legion Go",
            "Gaming",
            "PC Gaming",
            "Steam Deck"
        ],
        "content": """<p>When PC hardware giants ASUS, Lenovo, and MSI rushed to launch handheld gaming consoles powered by AMD's Ryzen Z1 Extreme silicon, they encountered a shared, insurmountable bottleneck: <strong>Microsoft Windows 11</strong>. Designed for desktop mice and keyboards, Windows 11 in a 7-inch handheld environment forced gamers to navigate finicky touch menus, suffered aggressive background update interruptions, and lacked an instant suspend-and-resume feature. Now, Valve is moving in for the kill by officially expanding <strong>SteamOS 3</strong> to rival third-party handhelds.</p>

<h2>The Problem with Windows 11 on Handhelds</h2>
<p>While devices like the <strong>ASUS ROG Ally X</strong> and <strong>Lenovo Legion Go</strong> boast superior raw hardware specs compared to the original Steam Deck—including 120Hz/144Hz VRR displays, faster LPDDR5X RAM, and 8-core Zen 4 CPU architectures—the actual user experience frequently stumbled:</p>
<ul>
  <li><strong>Background Resource Overhead:</strong> Windows services, telemetry services, and anti-virus sweeps consume between 3GB to 4.5GB of system memory before launching a single game.</li>
  <li><strong>Absence of True Sleep Mode:</strong> Pressing the power button on a Windows handheld initiates standard ACPI Sleep or Hibernation, which routinely crashes DirectX 12 render threads or drains the battery entirely while resting inside a travel case.</li>
  <li><strong>Micro-Stuttering and Display Compositor:</strong> Windows Desktop Window Manager (DWM) forces double-buffering layers that introduce latency and frame pacing judder on variable-refresh screens.</li>
</ul>

<h2>How SteamOS Unlocks 20% Extra Battery and Smooth Frame Pacing</h2>
<p>Valve’s Linux-based SteamOS solves these fundamental operating system constraints through purpose-built handheld engineering:</p>

<h3>1. Gamescope Micro-Compositor</h3>
<p>Rather than rendering a heavyweight desktop UI behind the game, SteamOS boots directly into <strong>Gamescope</strong>. This custom micro-compositor isolates the game into an isolated sandbox, handling resolution upscaling, dynamic refresh rate switching, and FSR frame scaling at the driver level with zero input lag.</p>

<h3>2. Instant Suspend and Resume</h3>
<p>Valve's custom Linux kernel allows players to tap the power button mid-boss fight in <em>Elden Ring</em> or <em>Black Myth: Wukong</em>, putting the APU into an ultra-low-power sleep state consuming under 1% battery per hour. Tapping the power button wakes the device back into gameplay in less than two seconds.</p>

<h3>3. TDP Power Profiles and Proton Translation</h3>
<p>Through Valve's Proton compatibility layer, Windows games run seamlessly on Linux without native ports. Crucially, SteamOS provides granular Watt-by-Watt TDP adjustment sliders, GPU clock limiters, and frame rate capping that can extend the ROG Ally X's massive 80Wh battery beyond six hours of continuous indie gaming.</p>

<h2>ASUS ROG Ally X and Lenovo Legion Go Integration</h2>
<p>Valve engineers have spent recent months adding hardware-specific driver hooks into the SteamOS codebase. Recent SteamOS Beta changelogs reveal explicit support for:</p>
<ol>
  <li>The ROG Ally's custom directional buttons, macro back paddles, and dynamic RGB thumbstick rings.</li>
  <li>Lenovo Legion Go's detachable TrueStrike controllers and native vertical-native 2560x1600 display panel rotation.</li>
  <li>Seamless dual-boot bootloader menus allowing gamers to retain a small Windows partition strictly for anti-cheat-locked games like <em>Call of Duty</em> and <em>Valorant</em>.</li>
</ol>

<h2>Valve’s Ecosystem Play: Becoming the Android of PC Gaming</h2>
<p>By transforming SteamOS into an open operating system for all handheld hardware manufacturers, Valve is replicating the strategy Google used with Android in the mobile space. Valve does not need to monopolize handheld hardware sales; as long as millions of gamers buy their games through the Steam store inside a fluid living-room console UI, Valve wins the platform war.</p>"""
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

# Also fix any old w=800 in existing articles
for a in existing_articles:
    if a.get('image') and '?w=800' in a['image']:
        a['image'] = a['image'].replace('?w=800', '?auto=format&fit=crop&w=1200&q=80')

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
    print("Updated feed.xml with 5 new items.")

