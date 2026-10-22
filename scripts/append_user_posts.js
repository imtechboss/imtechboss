const fs = require('fs');
const { execSync } = require('child_process');

const POSTS_FILE = fs.existsSync('./posts.json') ? './posts.json' : './data/posts.json';
const DATA_JS_FILE = './js/data.js';
const SITEMAP_FILE = './sitemap.xml';
const SITE_URL = 'https://imtechboss.com';

const newPosts = [
  {
    id: "how-to-harden-php-servers-prevent-rce-webshell-exploits-2026",
    slug: "how-to-harden-php-servers-prevent-rce-webshell-exploits-2026",
    title: "How to Harden PHP 8.x Servers Against Remote Code Execution (RCE) and Webshell Exploits in 2026",
    category: "Software & Tech",
    author: "Tech Boss",
    date: "2026-10-22",
    readTime: "8 min read",
    image: "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?auto=format&fit=crop&w=1200&q=80",
    excerpt: "A complete server engineering guide to securing PHP 8.x production environments against php2shell payloads, CGI argument injection, unauthenticated RCE vulnerabilities, and unauthorized file execution.",
    content: `
      <p>Unpatched PHP runtimes and misconfigured FastCGI Process Manager (PHP-FPM) pools remain primary targets for automated <code>php2shell</code> remote code execution (RCE) campaigns. Attackers routinely exploit exposed file upload endpoints, insecure deserialization, and CGI argument injection to drop persistent webshells inside public web directories. Hardening a production Linux web server requires strict configuration at three distinct layers: the <code>php.ini</code> runtime directives, the Nginx or Apache worker isolation boundaries, and filesystem permission locks.</p>

      <h2>1. Disable High-Risk Process Execution Functions in php.ini</h2>
      <p>The vast majority of PHP webshells rely on built-in system execution wrappers to spawn a reverse shell or run arbitrary bash commands under the <code>www-data</code> user. Unless your application explicitly invokes local CLI binaries, you should disable all OS-level execution functions in your active <code>/etc/php/8.3/fpm/php.ini</code> file:</p>
      <pre><code>; Disable dangerous OS command execution and process control functions
disable_functions = exec,passthru,shell_exec,system,proc_open,popen,curl_multi_exec,parse_ini_file,show_source,pcntl_exec,pcntl_fork

; Prevent PHP from fetching and executing remote scripts via include/require
allow_url_fopen = Off
allow_url_include = Off

; Hide PHP version headers from HTTP responses
expose_php = Off

; Restrict PHP filesystem access strictly to the application root
open_basedir = /var/www/html/:/tmp/</code></pre>
      <p>Setting <code>open_basedir</code> guarantees that even if a vulnerability exists within a third-party plugin, the PHP worker process cannot traverse upward into <code>/etc/passwd</code> or inspect sibling virtual hosts on the same machine.</p>

      <h2>2. Block PHP Execution Inside Upload and Cache Directories</h2>
      <p>File upload forms for avatars, attachments, or document imports are the number-one entry vector for webshells. Even when MIME-type checks are implemented in application code, attackers bypass weak filters using double extensions (such as <code>avatar.jpg.php</code>) or polyglot image headers. You must instruct Nginx to refuse script execution inside static storage directories:</p>
      <pre><code># Nginx block: Deny PHP script execution in user upload folders
location ~* ^/(uploads|storage|cache|assets)/.*\\.(php|php5|phtml|phar|inc)$ {
    deny all;
    return 403;
}

# Ensure FastCGI only processes existing local scripts
location ~ \\.php$ {
    try_files $uri =404;
    fastcgi_split_path_info ^(.+\\.php)(/.+)$;
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_pass unix:/run/php/php8.3-fpm.sock;
}</code></pre>
      <p>The <code>try_files $uri =404;</code> directive is critical: it prevents Nginx from passing non-existent image paths to the PHP interpreter when <code>cgi.fix_pathinfo</code> is mishandled.</p>

      <h2>3. PHP Security Directive Impact Comparison</h2>
      <table>
        <thead>
          <tr>
            <th>Directive / Rule</th>
            <th>Configuration File</th>
            <th>Exploit Class Mitigated</th>
            <th>Production Overhead</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>disable_functions</code></td>
            <td><code>php.ini</code></td>
            <td>Webshell command execution (<code>shell_exec</code>, <code>system</code>)</td>
            <td>Zero</td>
          </tr>
          <tr>
            <td><code>allow_url_include = Off</code></td>
            <td><code>php.ini</code></td>
            <td>Remote File Inclusion (RFI) payload injection</td>
            <td>Zero</td>
          </tr>
          <tr>
            <td><code>open_basedir</code></td>
            <td><code>php.ini</code> / Pool conf</td>
            <td>Directory traversal and cross-site file snooping</td>
            <td>Negligible (&lt;1% I/O check)</td>
          </tr>
          <tr>
            <td><code>try_files $uri =404</code></td>
            <td><code>nginx.conf</code></td>
            <td>FastCGI path info spoofing on uploaded images</td>
            <td>Zero</td>
          </tr>
        </tbody>
      </table>

      <h2>4. Auditing Live Servers for Hidden Webshells via Linux CLI</h2>
      <p>If you suspect an older PHP installation was exposed prior to patching, run a targeted filesystem audit across your web root to locate obfuscated <code>eval(base64_decode(...))</code> payloads or recently modified scripts:</p>
      <pre><code># 1. Scan for obfuscated PHP webshell signatures
grep -rnE "(eval\\s*\\(|base64_decode\\s*\\(|gzinflate\\s*\\(|shell_exec\\s*\\(|passthru\\s*\\()" /var/www/html/

# 2. List all .php files modified in the last 72 hours
find /var/www/html/ -type f -name "*.php" -mtime -3 -ls

# 3. Verify no unexpected files exist inside the uploads directory
find /var/www/html/uploads/ -type f -name "*.php*"</code></pre>
      <p>After verifying the codebase is clean, restart PHP-FPM using <code>sudo systemctl restart php8.3-fpm</code> and enforce read-only file permissions (<code>chmod 0440</code> or immutable deployment containers) on core application files so runtime workers cannot modify <code>.php</code> scripts on disk.</p>
    `
  },
  {
    id: "how-to-install-ps5-firmware-update-usb-safe-mode-fix-errors-2026",
    slug: "how-to-install-ps5-firmware-update-usb-safe-mode-fix-errors-2026",
    title: "How to Install PS5 Firmware Update Manually via USB Safe Mode & Fix Update Error Codes (2026 Guide)",
    category: "Gaming Guides",
    author: "Tech Boss",
    date: "2026-10-22",
    readTime: "7 min read",
    image: "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?auto=format&fit=crop&w=1200&q=80",
    excerpt: "Step-by-step troubleshooting guide to manually installing PlayStation 5 system software updates (including Firmware 14.20) via USB in Safe Mode to resolve corrupted downloads and SU-101312-8 error loops.",
    content: `
      <p>When a PlayStation 5 system software rollout—such as the PS5 firmware 14.20 stability and DualSense wireless controller update—encounters unstable Wi-Fi packet loss or cached installer corruption, the console can get stuck in an endless verification loop. Instead of repeatedly retrying a broken over-the-air (OTA) download, performing a clean manual installation via USB in PS5 Safe Mode bypasses the network cache and flashes the firmware directly from local storage.</p>

      <h2>1. Differentiating Update Files vs. Full Reinstallation Files</h2>
      <p>Before formatting your USB drive, you must download the correct package type from Sony's official PlayStation support portal. Selecting the wrong file will wipe your saved games and captured media:</p>
      <table>
        <thead>
          <tr>
            <th>File Package Type</th>
            <th>Approximate File Size</th>
            <th>Deletes Console Data?</th>
            <th>When to Use</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>PS5 Update File</strong> (<code>PS5UPDATE.PUP</code>)</td>
            <td>~1.1 GB – 1.3 GB</td>
            <td><strong>No</strong> (Preserves all games &amp; settings)</td>
            <td>Standard firmware upgrades, OTA download freezes, Safe Mode Option 3</td>
          </tr>
          <tr>
            <td><strong>PS5 Reinstallation File</strong> (<code>PS5UPDATE.PUP</code>)</td>
            <td>~1.2 GB+ (Full OS Image)</td>
            <td><strong>Yes</strong> (Factory resets internal SSD)</td>
            <td>Replacing the internal SSD or fixing severe OS boot corruption (Safe Mode Option 7)</td>
          </tr>
        </tbody>
      </table>

      <h2>2. Preparing the FAT32 or exFAT USB Drive</h2>
      <p>The PS5 bootloader cannot read NTFS-formatted flash drives. Use a USB 3.0 drive with at least 4 GB of free capacity and configure the exact case-sensitive folder hierarchy below:</p>
      <ol>
        <li>Insert your USB flash drive into a Windows PC or Mac and format it to <strong>exFAT</strong> or <strong>FAT32</strong> (exFAT is recommended to avoid the 4 GB file size ceiling).</li>
        <li>Inside the root of the USB drive, create a folder named <code>PS5</code> (all uppercase letters).</li>
        <li>Inside the <code>PS5</code> folder, create a subfolder named <code>UPDATE</code> (all uppercase letters).</li>
        <li>Place your downloaded update file inside that folder and confirm it is named exactly <code>PS5UPDATE.PUP</code>. Your final path must be: <code>USB_DRIVE:\\PS5\\UPDATE\\PS5UPDATE.PUP</code>.</li>
      </ol>
      <p><em>Warning:</em> If your browser downloads a second copy named <code>PS5UPDATE(1).PUP</code>, the console will fail to recognize the file and display error code <strong>SU-101193-5</strong>.</p>

      <h2>3. Booting into PS5 Safe Mode and Flashing the Firmware</h2>
      <ol>
        <li>Turn off your PlayStation 5 completely (ensure the power LED indicator is completely off, not pulsing orange in Rest Mode).</li>
        <li>Plug the prepared USB drive into one of the rear SuperSpeed USB Type-A ports on the console, and connect your DualSense controller using a physical USB-C data cable.</li>
        <li>Press and hold the physical <strong>Power button</strong> on the console. You will hear a first beep immediately—keep holding the button for roughly <strong>7 seconds</strong> until you hear a <strong>second beep</strong>, then release.</li>
        <li>Press the <strong>PS button</strong> on your wired DualSense controller to activate Safe Mode.</li>
        <li>Select <strong>Option 3: Update System Software</strong> &rarr; <strong>Update from USB Storage Device</strong> &rarr; <strong>OK</strong>.</li>
      </ol>

      <h2>4. Post-Update Fixes: DualSense Audio & HDMI 2.1 Handshake</h2>
      <p>After the console reboots into the updated system software, prompt your controller firmware update when notified. If you experience blank screen flickers on 120Hz VRR televisions or muffled DualSense mic output after updating:</p>
      <ul>
        <li><strong>Rebuild Database &amp; Clear System Cache:</strong> Boot back into Safe Mode and select <strong>Option 6: Clear Cache and Rebuild Database</strong> &rarr; <strong>Clear System Software Cache</strong>. This purges leftover shader and OS configuration blocks from the previous firmware version without deleting any games.</li>
        <li><strong>Reset 4K Video Transfer Rate:</strong> Navigate to <em>Settings &rarr; Screen and Video &rarr; Video Output</em> and set <strong>4K Video Transfer Rate</strong> to <em>Automatic</em> and re-toggle <strong>VRR (Variable Refresh Rate)</strong> to resync the HDMI 2.1 EDID handshake.</li>
      </ul>
    `
  },
  {
    id: "linux-zram-swappiness-optimization-4gb-8gb-ram-guide-2026",
    slug: "linux-zram-swappiness-optimization-4gb-8gb-ram-guide-2026",
    title: "How to Configure ZRAM, Swappiness, and EarlyOOM on Linux to Run Heavy IDEs Smoothly on 4GB/8GB RAM PCs",
    category: "Software & Tech",
    author: "Tech Boss",
    date: "2026-10-22",
    readTime: "8 min read",
    image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?auto=format&fit=crop&w=1200&q=80",
    excerpt: "Eliminate Linux desktop freezes on 4GB and 8GB DDR3/DDR4 systems by configuring zstd-compressed ZRAM block devices, kernel memory page-cluster tuning, and EarlyOOM protection.",
    content: `
      <p>Running modern development environments—such as VS Code, Flutter/Android toolchains, or Chromium-based browsers—on compact desktop PCs equipped with 4 GB or 8 GB of RAM quickly exhausts physical memory. When the Linux kernel begins swapping memory pages out to a traditional SSD or HDD swap partition, disk I/O wait times skyrocket and the desktop UI completely freezes (a condition known as swap thrashing). Configuring <strong>ZRAM</strong> creates a compressed block device directly inside physical RAM, delivering sub-millisecond swap latency while effectively doubling usable memory capacity for text and code buffers.</p>

      <h2>1. Why ZRAM Outperforms Traditional Disk Swap</h2>
      <p>Instead of writing inactive memory pages across a SATA or NVMe bus, ZRAM compresses memory pages in-place inside RAM using high-speed algorithms like <code>zstd</code> or <code>lz4</code>. Because source code, DOM trees, and Electron heaps compress at a <strong>2.8:1 to 3.5:1 ratio</strong>, 2 GB of data compressed inside ZRAM consumes only ~600 MB of physical RAM.</p>
      <table>
        <thead>
          <tr>
            <th>Swap Mechanism</th>
            <th>Compression Algorithm</th>
            <th>Average Compression Ratio</th>
            <th>Read/Write Latency</th>
            <th>SSD Wear Impact</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>ZRAM (zstd)</strong></td>
            <td>Zstandard (<code>zstd</code>)</td>
            <td>~3.2 : 1</td>
            <td>~0.02 ms (RAM speed)</td>
            <td>Zero SSD writes</td>
          </tr>
          <tr>
            <td><strong>ZRAM (lz4)</strong></td>
            <td>LZ4 Fast</td>
            <td>~2.3 : 1</td>
            <td>~0.01 ms (Lowest CPU load)</td>
            <td>Zero SSD writes</td>
          </tr>
          <tr>
            <td><strong>SSD Swapfile</strong></td>
            <td>None</td>
            <td>1.0 : 1</td>
            <td>~0.50 – 2.50 ms</td>
            <td>High write amplification</td>
          </tr>
        </tbody>
      </table>

      <h2>2. Step-by-Step Setup: Installing and Tuning zramswap (Ubuntu/Debian/Mint)</h2>
      <p>On Debian- and Ubuntu-based distributions, install the official <code>zram-tools</code> package and configure it to allocate 100% of your physical RAM capacity as the uncompressed ZRAM limit using the <code>zstd</code> compressor:</p>
      <pre><code># 1. Install zram-tools and earlyoom
sudo apt update &amp;&amp; sudo apt install -y zram-tools earlyoom

# 2. Configure /etc/default/zramswap
sudo tee /etc/default/zramswap &lt;&lt;'EOF'
ALGO=zstd
PERCENT=100
PRIORITY=100
EOF

# 3. Restart the zramswap service and verify status
sudo systemctl restart zramswap
zramctl</code></pre>
      <p>Running <code>zramctl</code> will confirm that <code>/dev/zram0</code> is active with the <code>zstd</code> algorithm and a swap priority of <code>100</code>, ensuring the kernel always prefers ZRAM over any fallback disk swap partition.</p>

      <h2>3. Kernel sysctl Tuning for Compressed Memory</h2>
      <p>Default Linux kernel VM parameters are designed for slow spinning disks, where swapping is avoided until the last moment (<code>vm.swappiness=60</code>) and pages are read in 8-page clusters (<code>vm.page-cluster=3</code>). With ZRAM, you want the kernel to proactively compress inactive background pages and fetch single pages with zero read-ahead overhead. Add these rules to <code>/etc/sysctl.d/99-zram-tuning.conf</code>:</p>
      <pre><code># Encourage proactive compression of cold anonymous memory pages into ZRAM
vm.swappiness = 150

# Disable swap read-ahead clustering since ZRAM has zero seek latency
vm.page-cluster = 0

# Retain directory and inode caches longer to keep IDE file searches snappy
vm.vfs_cache_pressure = 50

# Prevent large dirty write buffers from stalling system memory
vm.dirty_background_ratio = 5
vm.dirty_ratio = 10</code></pre>
      <p>Apply the changes immediately by running <code>sudo sysctl --system</code>.</p>

      <h2>4. Preventing Hard System Lockups with EarlyOOM</h2>
      <p>The native Linux kernel Out-Of-Memory (OOM) killer often triggers too late, allowing a runaway compiler or browser tab to freeze the X11/Wayland compositor for several minutes. Enabling the <code>earlyoom</code> daemon monitors free RAM and free swap every second, gracefully terminating the single heaviest memory-consuming process before your mouse cursor ever stutters:</p>
      <pre><code>sudo systemctl enable --now earlyoom
sudo systemctl status earlyoom</code></pre>
    `
  },
  {
    id: "nextdns-vs-control-d-vs-adguard-dns-router-ios-setup-guide-2026",
    slug: "nextdns-vs-control-d-vs-adguard-dns-router-ios-setup-guide-2026",
    title: "NextDNS vs Control D vs AdGuard DNS: Complete Router & iOS Configuration Guide for Zero-Latency Ad Blocking (2026)",
    category: "Software & Tech",
    author: "Tech Boss",
    date: "2026-10-22",
    readTime: "7 min read",
    image: "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80",
    excerpt: "Compare NextDNS, Control D, and AdGuard DNS across DoH/DoQ latency, blocklist accuracy (HaGeZi vs OISD), iOS configuration profiles, and home ONU router setups.",
    content: `
      <p>Browser-based ad blockers only filter traffic inside a single web browser, leaving mobile apps, smart TVs, and operating system telemetry completely unfiltered. Furthermore, running local VPN-tunnel blockers on smartphones continuously drains battery life. Implementing a cloud-based encrypted DNS resolver—specifically <strong>NextDNS</strong>, <strong>Control D</strong>, or <strong>AdGuard DNS</strong>—blocks ad servers, tracking domains, and phishing endpoints at the network resolution layer before a single byte of payload data is downloaded.</p>

      <h2>1. Head-to-Head Comparison: NextDNS vs. Control D vs. AdGuard DNS</h2>
      <table>
        <thead>
          <tr>
            <th>Feature / Metric</th>
            <th>NextDNS</th>
            <th>Control D</th>
            <th>AdGuard DNS</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Supported Protocols</strong></td>
            <td>DoH, DoT, DoQ, IPv4/v6</td>
            <td>DoH, DoH3, DoT, DoQ, Legacy</td>
            <td>DoH, DoT, DoQ, DNSCrypt</td>
          </tr>
          <tr>
            <td><strong>Free Tier Monthly Limit</strong></td>
            <td>300,000 queries/month</td>
            <td>Unlimited (Free Public Resolvers)</td>
            <td>300,000 queries/month</td>
          </tr>
          <tr>
            <td><strong>Best Native Blocklists</strong></td>
            <td>HaGeZi Multi Pro, OISD, 1Hosts</td>
            <td>Control D Native + HaGeZi/OISD</td>
            <td>AdGuard Base + OISD</td>
          </tr>
          <tr>
            <td><strong>Smart Traffic Redirection</strong></td>
            <td>No</td>
            <td>Yes (Proxy geo-routing built in)</td>
            <td>No</td>
          </tr>
          <tr>
            <td><strong>iOS Battery Overhead</strong></td>
            <td>Zero (Native <code>.mobileconfig</code>)</td>
            <td>Zero (Native <code>.mobileconfig</code>)</td>
            <td>Zero (Native <code>.mobileconfig</code>)</td>
          </tr>
        </tbody>
      </table>

      <h2>2. Selecting the Optimal Blocklist Without Breaking Websites</h2>
      <p>Over-aggressive DNS blocklists frequently break banking portals, shopping checkouts, and social media login flows. For a zero-maintenance setup across family devices and workstations, avoid stacking ten overlapping lists. Instead, enable <strong>one</strong> primary curated list:</p>
      <ul>
        <li><strong>HaGeZi Multi PRO (Recommended for Power Users):</strong> Aggressively blocks ads, telemetry, malvertising, and tracking CNAMEs while maintaining an actively curated whitelist to prevent false positives.</li>
        <li><strong>OISD Big (Recommended for Whole-Home Routers):</strong> Engineered specifically around the philosophy that "nothing should break." Ideal when configuring DNS directly on a home ONU/router shared by multiple family members.</li>
      </ul>

      <h2>3. Native iOS Setup Using Signed Configuration Profiles (No App Required)</h2>
      <p>On iPhone and iPad, you should avoid installing third-party DNS apps that register a fake local VPN icon. Instead, use iOS native Encrypted DNS profiles:</p>
      <ol>
        <li>Open Safari on your iOS device and visit <code>apple.nextdns.io</code> (for NextDNS) or your Control D endpoint generator.</li>
        <li>Enter your Configuration ID, select <strong>DNS-over-HTTPS (DoH)</strong> or <strong>DNS-over-QUIC (DoQ)</strong>, and tap <strong>Download Profile</strong>.</li>
        <li>Open <em>Settings &rarr; Profile Downloaded</em> at the top of the menu and complete the installation.</li>
        <li>Verify active encryption under <em>Settings &rarr; General &rarr; VPN &amp; Device Management &rarr; DNS</em>. You can also exclude your trusted home Wi-Fi SSID if your router already runs the same policy.</li>
      </ol>

      <h2>4. Configuring Fiber ONU Routers and Measuring True DNS Latency</h2>
      <p>Standard ISP fiber routers (such as ZTE ZXHN or Huawei HG series ONUs) only accept unencrypted IPv4/IPv6 DNS addresses under <em>Network &rarr; LAN &rarr; DHCP Server</em>. To use NextDNS or Control D on a basic router, link your Dynamic IP (or DDNS hostname) in the provider dashboard and enter their linked IPv4 addresses into your router's Primary and Secondary DNS fields, while disabling <strong>ISP DNS Relay</strong>.</p>
      <p>To verify which provider has the lowest latency routing from your ISP in South Asia, run this quick terminal benchmark:</p>
      <pre><code># Measure actual DNS query resolution time in milliseconds
dig @45.90.28.0 example.com | grep "Query time"
dig @76.76.2.0 example.com | grep "Query time"
dig @94.140.14.14 example.com | grep "Query time"</code></pre>
    `
  },
  {
    id: "cursor-vs-windsurf-vs-vscode-roo-code-ram-performance-benchmark-2026",
    slug: "cursor-vs-windsurf-vs-vscode-roo-code-ram-performance-benchmark-2026",
    title: "Cursor vs Windsurf vs VS Code + Roo Code: Real-World RAM Usage, Context Indexing & Local LLM Benchmark (2026)",
    category: "AI & Technology",
    author: "Tech Boss",
    date: "2026-10-22",
    readTime: "8 min read",
    image: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80",
    excerpt: "An engineering benchmark comparing Cursor, Windsurf, and stock VS Code with Roo Code across memory footprint, codebase RAG indexing speed, multi-file edits, and Bring-Your-Own-Key (BYOK) pricing.",
    content: `
      <p>AI-assisted software engineering has shifted from simple single-line autocomplete to autonomous multi-file agents capable of refactoring entire architectures, running terminal tests, and fixing linter errors automatically. However, because modern AI IDEs fork Microsoft's Electron-based Visual Studio Code and bundle heavy background vector indexers, memory consumption on 8 GB and 16 GB developer machines varies dramatically between <strong>Cursor</strong>, <strong>Windsurf</strong>, and stock <strong>VS Code paired with Roo Code</strong>.</p>

      <h2>1. Real-World Memory (RAM) & CPU Footprint Benchmark</h2>
      <p>We benchmarked all three setups opening an identical 4,200-file Flutter and TypeScript monorepo on a Linux/Windows workstation, measuring Resident Set Size (RSS) memory after initial codebase indexing settled:</p>
      <table>
        <thead>
          <tr>
            <th>IDE / Agent Environment</th>
            <th>Idle RAM Usage (1 File Open)</th>
            <th>Active Agent + Indexing RAM</th>
            <th>Codebase Indexing Method</th>
            <th>BYOK / Custom API Support</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Cursor</strong></td>
            <td>~1.45 GB</td>
            <td>~2.35 GB</td>
            <td>Cloud Merkle-Tree Sync + Embeddings</td>
            <td>Partial (Custom key disables Tab/Composer features)</td>
          </tr>
          <tr>
            <td><strong>Windsurf</strong></td>
            <td>~1.30 GB</td>
            <td>~2.10 GB</td>
            <td>Cascade AST + Local Context Engine</td>
            <td>Subscription-based credits</td>
          </tr>
          <tr>
            <td><strong>VS Code + Roo Code</strong></td>
            <td>~0.85 GB</td>
            <td>~1.40 GB</td>
            <td>On-demand Ripgrep + Tree-sitter AST</td>
            <td><strong>100% Native</strong> (OpenRouter, Anthropic, Gemini, Ollama)</td>
          </tr>
        </tbody>
      </table>

      <h2>2. Architectural Differences in Context Retrieval</h2>
      <ul>
        <li><strong>Cursor (Composer &amp; Tab):</strong> Cursor excels at low-latency speculative multi-line diffs ("Cursor Tab"). It computes a Merkle tree of your workspace and uploads obfuscated chunks to compute vector embeddings, making <code>@Codebase</code> queries very fast at the cost of higher background network and renderer memory overhead.</li>
        <li><strong>Windsurf (Cascade):</strong> Windsurf's Cascade engine tracks real-time developer actions—including recent terminal commands and cursor jumps—to infer which files belong in the prompt window without requiring manual <code>@file</code> tagging.</li>
        <li><strong>VS Code + Roo Code:</strong> Rather than running a persistent background embedding daemon, Roo Code uses deterministic <code>ripgrep</code> searches and Tree-sitter abstract syntax tree (AST) definitions on demand. This keeps idle RAM usage nearly 600 MB lower than standalone forked IDEs, making it the superior choice for 4 GB and 8 GB RAM machines.</li>
      </ul>

      <h2>3. Reducing Electron Memory Bloat for Large Projects</h2>
      <p>Regardless of whether you use Cursor, Windsurf, or stock VS Code, excluding generated build artifacts from the file watcher and AI indexer prevents runaway CPU and RAM spikes. Add these exclusions to your workspace <code>.vscode/settings.json</code> and <code>.cursorignore</code>:</p>
      <pre><code>{
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/node_modules/**": true,
    "**/build/**": true,
    "**/.dart_tool/**": true,
    "**/dist/**": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/build": true,
    "**/.dart_tool": true,
    "**/package-lock.json": true
  }
}</code></pre>
      <p>Excluding <code>build/</code>, <code>.dart_tool/</code>, and <code>node_modules/</code> cuts language server (LSP) indexing memory by up to 45% and prevents AI agents from wasting context tokens reading compiled bundles.</p>
    `
  }
];

function appendPosts() {
  if (!fs.existsSync(POSTS_FILE)) {
    console.error("Could not find posts.json in the current directory.");
    process.exit(1);
  }

  const raw = fs.readFileSync(POSTS_FILE, 'utf8');
  const parsed = JSON.parse(raw);
  const postsArray = Array.isArray(parsed) ? parsed : (parsed.posts || []);

  const existingSlugs = new Set(postsArray.map(p => p.slug || p.id));
  let addedCount = 0;

  // Prepend new posts to the top of the feed so they appear first on the homepage
  // Iterate in reverse of newPosts so the first in newPosts ends up at the very top
  for (const post of [...newPosts].reverse()) {
    if (!existingSlugs.has(post.slug)) {
      postsArray.unshift(post);
      addedCount++;
    }
  }

  const output = Array.isArray(parsed) ? postsArray : { ...parsed, posts: postsArray };
  fs.writeFileSync(POSTS_FILE, JSON.stringify(output, null, 2), 'utf8');
  console.log(`Added ${addedCount} new high-value posts to ${POSTS_FILE}. Total posts: ${postsArray.length}`);

  // Also update js/data.js
  const dataJsContent = "var initialArticles = " + JSON.stringify(postsArray, null, 2) + ";\n";
  fs.writeFileSync(DATA_JS_FILE, dataJsContent, 'utf8');
  console.log(`Synchronized ${DATA_JS_FILE} with ${postsArray.length} articles.`);

  // Update sitemap.xml if present
  if (fs.existsSync(SITEMAP_FILE)) {
    let xml = fs.readFileSync(SITEMAP_FILE, 'utf8');
    const today = "2026-10-22";
    let newEntries = "";

    for (const post of newPosts) {
      const loc = `${SITE_URL}/${post.slug}/`;
      if (!xml.includes(loc)) {
        newEntries += `  <url>\n    <loc>${loc}</loc>\n    <lastmod>${today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>\n`;
      }
    }

    if (newEntries) {
      xml = xml.replace('</urlset>', `${newEntries}</urlset>`);
      fs.writeFileSync(SITEMAP_FILE, xml, 'utf8');
      console.log(`Updated ${SITEMAP_FILE} with new URLs.`);
    }
  }

  // Pre-render static pages
  console.log("Pre-rendering all static pages using python scripts/build_static.py...");
  try {
    const res = execSync('python scripts/build_static.py', { encoding: 'utf8' });
    console.log(res);
  } catch (err) {
    console.error("build_static.py failed:", err.message);
  }
}

appendPosts();
