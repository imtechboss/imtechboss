import os

EXTENDED_TOOLS = [
    {
        "slug": "windows-bsod-error-code-lookup",
        "icon": "🛡️",
        "badge": "Windows 11 Diagnostics",
        "h1": "Windows BSOD Stop Code & Event ID Lookup",
        "title": "Windows BSOD Error Code Lookup Tool (2026) — Tech Boss",
        "description": "Look up Windows 11 BSOD stop codes (0x0000000A, 0x00000133, Event ID 41, 0x00000116) for exact kernel root causes, WinDbg commands, and verified driver fixes.",
        "capsule_title": "Instant Kernel Crash Triage",
        "capsule_text": "Select or search any Windows 11 BugCheck hex code or Event Viewer ID below to isolate whether the crash stems from RAM/XMP instability, storage controller latency, GPU driver timeouts, or PSU transient power loss.",
        "tool_html": """
        <section id="bsodLookupTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Select Common BSOD / Event Code</label>
              <select id="bsodCodeSelect" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="0x0000000A">0x0000000A — IRQL_NOT_LESS_OR_EQUAL</option>
                <option value="0x00000133">0x00000133 — DPC_WATCHDOG_VIOLATION</option>
                <option value="EVENT_41">Event ID 41 — Kernel-Power Unexpected Restart</option>
                <option value="0x00000116">0x00000116 — VIDEO_TDR_FAILURE (nvlddmkm / amdkmdag)</option>
                <option value="0x0000001A">0x0000001A — MEMORY_MANAGEMENT</option>
                <option value="0x00000124">0x00000124 — WHEA_UNCORRECTABLE_ERROR</option>
                <option value="0x0000007E">0x0000007E — SYSTEM_THREAD_EXCEPTION_NOT_HANDLED</option>
                <option value="DXGI_HUNG">DXGI_ERROR_DEVICE_HUNG — DirectX GPU Hang</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Or Filter by Keyword / Hex</label>
              <input id="bsodSearchInput" type="text" placeholder="e.g. 0x133, watchdog, nvlddmkm, 41" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm text-gray-900 dark:text-white" />
            </div>
          </div>
          <button id="lookupBsodBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm shadow transition-colors">
            🔍 Diagnose Stop Code &amp; Get Fix Steps
          </button>
          <div id="bsodResultBox" class="hidden mt-6 p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const DB = {
            "0x0000000A": {
              name: "IRQL_NOT_LESS_OR_EQUAL (0x0000000A)",
              subsystem: "Kernel Driver / DDR5 XMP-EXPO RAM Stability",
              severity: "High — Driver or Memory Access Violation",
              cause: "A kernel-mode driver or system process attempted to read/write pageable memory at an elevated Interrupt Request Level (IRQL).",
              steps: [
                "Open C:\\Windows\\Minidump in WinDbg and run !analyze -v to read the MODULE_NAME causing the fault.",
                "Disable DDR5 XMP/EXPO in BIOS temporarily and test stability at stock JEDEC speeds.",
                "Run Admin Terminal: DISM /Online /Cleanup-Image /RestoreHealth followed by sfc /scannow.",
                "Clean-reinstall GPU and Realtek/Intel NIC drivers rather than relying on Windows Update stubs."
              ],
              guide: "/how-to-fix-irql-not-less-or-equal-0x0000000a-bsod-windows-11/"
            },
            "0x00000133": {
              name: "DPC_WATCHDOG_VIOLATION (0x00000133)",
              subsystem: "Storage Controller (SATA/NVMe) / PCIe ASPM Latency",
              severity: "High — Deferred Procedure Call Timeout",
              cause: "A single DPC routine ran longer than the Windows watchdog timeout on a CPU core, commonly triggered by outdated AHCI/NVMe drivers or PCIe power saving.",
              steps: [
                "Open Device Manager -> IDE ATA/ATAPI Controllers and switch vendor drivers to Standard SATA AHCI Controller.",
                "Set PCI Express -> Link State Power Management to Off inside Control Panel Power Options.",
                "Update NVMe SSD firmware using Samsung Magician, WD Dashboard, or Crucial Storage Executive.",
                "Run LatencyMon for 10 minutes to catch the exact .sys driver spiking ISR/DPC execution time."
              ],
              guide: "/how-to-fix-dpc-watchdog-violation-0x00000133-bsod-windows-11/"
            },
            "EVENT_41": {
              name: "Kernel-Power Event ID 41 (BugcheckCode 0)",
              subsystem: "Power Supply Transients / BIOS C-States / Fast Startup",
              severity: "Critical — Abrupt Hardware Power Loss",
              cause: "Windows rebooted without cleanly shutting down. When BugcheckCode is 0, power dropped before the OS could write a crash dump.",
              steps: [
                "Disable Windows Fast Startup in Control Panel -> Power Options -> Choose what the power buttons do.",
                "Replace daisy-chained PCIe GPU cables with dedicated 8-pin or native 12V-2x6 ATX 3.1 cables.",
                "Verify PSU wattage headroom with our PC Power Supply Calculator to rule out GPU transient trips.",
                "If restarts happen at desktop idle, disable Global C-State Control or set Power Supply Idle Control to Typical Current Idle in BIOS."
              ],
              guide: "/how-to-fix-kernel-power-event-id-41-random-restarts-windows-11/"
            },
            "0x00000116": {
              name: "VIDEO_TDR_FAILURE (0x00000116)",
              subsystem: "GPU Driver Timeout (nvlddmkm.sys / amdkmdag.sys)",
              severity: "High — Display Driver Reset Failed",
              cause: "Windows Timeout Detection and Recovery (TDR) tried to reset an unresponsive GPU driver after 2 seconds and failed.",
              steps: [
                "Boot into Safe Mode, wipe display drivers cleanly with Display Driver Uninstaller (DDU), and install the latest WHQL Studio/Game Ready driver.",
                "Remove GPU core/memory overclocks and inspect 12V-2x6 / 8-pin power connector seating.",
                "Check GPU hotspot temperatures under load to rule out dried thermal paste or fan curve failure."
              ],
              guide: "/how-to-fix-dxgi-error-device-hung-directx-crash-windows-11/"
            },
            "0x0000001A": {
              name: "MEMORY_MANAGEMENT (0x0000001A)",
              subsystem: "Physical RAM Modules / Pagefile / Corrupted Storage",
              severity: "High — Memory Page Table Corruption",
              cause: "Severe memory management error caused by defective DRAM cells, overly tight XMP timings, or corrupted virtual memory pagefiles.",
              steps: [
                "Run Windows Memory Diagnostic (mdsched.exe) or MemTest86 from USB for at least 2 full passes.",
                "Test one RAM stick at a time in slot A2 to isolate a faulty DIMM.",
                "Check NVMe SSD S.M.A.R.T. health because failing pagefile sectors also trigger 0x1A."
              ],
              guide: "/how-to-fix-100-percent-memory-disk-leak-windows-11-24h2/"
            },
            "0x00000124": {
              name: "WHEA_UNCORRECTABLE_ERROR (0x00000124)",
              subsystem: "CPU Hardware / VCore Undervolt / PCIe Bus",
              severity: "Critical — Hardware Machine Check Exception",
              cause: "The processor reported a fatal hardware error directly to Windows Hardware Error Architecture (WHEA).",
              steps: [
                "Reset BIOS Curve Optimizer (AMD PBO) or Intel undervolt offsets back to 0 immediately.",
                "Update motherboard BIOS to the latest stable AGESA / Intel microcode release.",
                "Check Event Viewer -> System for WHEA-Logger Event ID 18/19 to see whether the failing APIC ID is a CPU core or PCIe device."
              ],
              guide: "/how-to-fix-kernel-power-event-id-41-random-restarts-windows-11/"
            },
            "0x0000007E": {
              name: "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED (0x0000007E)",
              subsystem: "Third-Party Kernel Driver / Outdated BIOS",
              severity: "Medium-High — Unhandled Kernel Exception",
              cause: "A system thread threw an exception that the error handler could not catch, typically right after a driver or Windows cumulative update.",
              steps: [
                "Boot into Safe Mode and roll back the most recently installed driver or Windows Update.",
                "Check C:\\Windows\\Minidump in WinDbg to identify the offending third-party .sys module.",
                "Ensure at least 15–20% free disk space on C: for system pagefile and update staging."
              ],
              guide: "/windows-11-slow-after-update-fix-2026/"
            },
            "DXGI_HUNG": {
              name: "DXGI_ERROR_DEVICE_HUNG",
              subsystem: "DirectX 12 Pipeline / GPU Shader Timeout",
              severity: "Medium-High — Game Engine GPU Hang",
              cause: "The graphics card stopped responding to DirectX command buffers due to driver bugs, aggressive factory OC, or unstable shader compilation.",
              steps: [
                "Clear DirectX Shader Cache via Windows Disk Cleanup and game-specific shader folders.",
                "Enable Debug Mode in NVIDIA Control Panel (Help -> Debug Mode) to test reference clocks.",
                "Disable Hardware-Accelerated GPU Scheduling (HAGS) temporarily if crashes occur during dual-monitor video playback."
              ],
              guide: "/how-to-fix-dxgi-error-device-hung-directx-crash-windows-11/"
            }
          };

          const sel = document.getElementById('bsodCodeSelect');
          const inp = document.getElementById('bsodSearchInput');
          const btn = document.getElementById('lookupBsodBtn');
          const box = document.getElementById('bsodResultBox');

          function render() {
            let key = sel.value;
            const q = (inp.value || '').trim().toLowerCase();
            if (q) {
              const found = Object.keys(DB).find(k => k.toLowerCase().includes(q) || DB[k].name.toLowerCase().includes(q) || DB[k].cause.toLowerCase().includes(q));
              if (found) {
                key = found;
                sel.value = found;
              }
            }
            const item = DB[key];
            if (!item) return;
            box.innerHTML = `
              <div class="flex flex-wrap items-center justify-between gap-2 pb-3 mb-3 border-b border-gray-200 dark:border-slate-700">
                <h3 class="text-lg font-extrabold text-gray-900 dark:text-white">${item.name}</h3>
                <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 dark:bg-rose-900/40 text-rose-700 dark:text-rose-300">${item.severity}</span>
              </div>
              <p class="text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400 mb-1">Primary Subsystem: ${item.subsystem}</p>
              <p class="text-sm text-gray-700 dark:text-gray-300 mb-4">${item.cause}</p>
              <div class="text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-2">Ordered Fix Checklist:</div>
              <ol class="list-decimal pl-5 space-y-1.5 text-sm text-gray-800 dark:text-gray-200 mb-4">
                ${item.steps.map(s => `<li>${s}</li>`).join('')}
              </ol>
              <a href="${item.guide}" class="inline-flex items-center gap-1 text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline">Read Full Step-by-Step Repair Guide &rarr;</a>
            `;
            box.classList.remove('hidden');
          }
          if (btn) btn.addEventListener('click', render);
        })();
        """,
        "guide_title": "How to Read Windows 11 Crash Dumps Before Changing Hardware",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Most Windows 11 Blue Screen of Death (BSOD) crashes look identical on screen, which leads PC owners to reinstall Windows or replace healthy parts unnecessarily. Separating software driver faults from physical hardware instability starts with two built-in logs: <strong>Event Viewer (System Log)</strong> and <strong>Kernel Minidumps</strong> stored under <code>C:\\Windows\\Minidump</code>.</p>
        <h3 class="text-base font-bold text-gray-900 dark:text-white mt-5 mb-2">1. Distinguish BugCheck Codes from BugcheckCode 0</h3>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">When Windows catches a bad driver or memory address in time, it halts execution and writes a non-zero hex stop code such as <code>0x0000000A</code> or <code>0x00000133</code>. If your PC simply clicks off and reboots with Event ID 41 and <code>BugcheckCode: 0</code>, the OS never had a chance to log a dump—pointing directly toward power delivery transients, motherboard VRM protection, or BIOS idle C-state voltage drops.</p>
        <h3 class="text-base font-bold text-gray-900 dark:text-white mt-5 mb-2">2. Use WinDbg !analyze -v to Name the Exact Driver</h3>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Install the official WinDbg app from the Microsoft Store, open the latest <code>.dmp</code> file, and run <code>!analyze -v</code>. Scroll down to <code>MODULE_NAME</code> and <code>IMAGE_NAME</code>. Drivers like <code>nvlddmkm.sys</code> (NVIDIA), <code>amdkmdag.sys</code> (AMD), <code>storahci.sys</code> (storage), or <code>rt640x64.sys</code> (Realtek Ethernet) tell you the exact component to update or roll back cleanly.</p>
        <h3 class="text-base font-bold text-gray-900 dark:text-white mt-5 mb-2">3. Always Test Stock BIOS Defaults First</h3>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">DDR5 XMP/EXPO profiles and CPU undervolts (AMD Curve Optimizer / Intel adaptive offsets) are the number-one hidden trigger behind intermittent <code>0x0000000A</code>, <code>0x0000001A</code>, and <code>0x00000124</code> crashes. Returning memory to stock JEDEC speeds for 48 hours confirms immediately whether your silicon or your drivers are at fault.</p>
        """
    },
    {
        "slug": "ollama-command-generator",
        "icon": "⚙️",
        "badge": "Local AI Engineering",
        "h1": "Ollama CLI & Modelfile Command Generator",
        "title": "Ollama Command & Modelfile Builder (2026) — Tech Boss",
        "description": "Generate ready-to-paste Ollama CLI commands, Flash Attention environment variables, KV cache quantization flags, and custom Modelfiles for 8GB–24GB GPUs.",
        "capsule_title": "Zero-Mistake Local LLM Config Builder",
        "capsule_text": "Configure your model tag, context window (num_ctx), Flash Attention, and KV cache quantization (q8_0/q4_0) to generate exact PowerShell/Bash environment variables and a custom Modelfile.",
        "tool_html": """
        <section id="ollamaGenTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Base Ollama Model</label>
              <select id="olModel" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="qwen2.5-coder:32b">qwen2.5-coder:32b (24GB VRAM Coding)</option>
                <option value="qwen2.5-coder:14b">qwen2.5-coder:14b (12GB–16GB VRAM)</option>
                <option value="deepseek-r1:32b">deepseek-r1:32b (24GB Reasoning)</option>
                <option value="deepseek-r1:14b">deepseek-r1:14b (12GB Reasoning)</option>
                <option value="deepseek-r1:8b">deepseek-r1:8b (6GB–8GB Laptop GPU)</option>
                <option value="llama3.3:70b">llama3.3:70b (Dual 24GB / 48GB+ VRAM)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Context Window (num_ctx)</label>
              <select id="olCtx" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="4096">4,096 tokens (Low VRAM Safe)</option>
                <option value="8192" selected>8,192 tokens (Balanced Coding)</option>
                <option value="16384">16,384 tokens (Long Files)</option>
                <option value="32768">32,768 tokens (Repo Context)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">KV Cache Quantization</label>
              <select id="olKv" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="f16">f16 (Default Full Precision)</option>
                <option value="q8_0" selected>q8_0 (Saves ~45% KV VRAM, Minimal Loss)</option>
                <option value="q4_0">q4_0 (Max Context Savings for 8GB–12GB GPUs)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Operating System Shell</label>
              <select id="olOs" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="win">Windows PowerShell</option>
                <option value="linux">Linux / macOS Bash</option>
              </select>
            </div>
          </div>
          <button id="genOllamaBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-bold text-sm shadow transition-colors">
            ⚙️ Generate Ollama CLI &amp; Modelfile
          </button>
          <div id="ollamaResultBox" class="hidden mt-6 space-y-4"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const btn = document.getElementById('genOllamaBtn');
          const box = document.getElementById('ollamaResultBox');
          if (!btn || !box) return;
          btn.addEventListener('click', () => {
            const model = document.getElementById('olModel').value;
            const ctx = document.getElementById('olCtx').value;
            const kv = document.getElementById('olKv').value;
            const os = document.getElementById('olOs').value;
            const customName = model.replace(':', '-') + '-ctx' + (parseInt(ctx, 10) / 1024) + 'k';
            const envBlock = os === 'win'
              ? `$env:OLLAMA_FLASH_ATTENTION="1"\\n$env:OLLAMA_KV_CACHE_TYPE="${kv}"\\n$env:OLLAMA_KEEP_ALIVE="15m"\\nollama serve`
              : `export OLLAMA_FLASH_ATTENTION=1\\nexport OLLAMA_KV_CACHE_TYPE=${kv}\\nexport OLLAMA_KEEP_ALIVE=15m\\nollama serve`;
            const modelfile = `FROM ${model}\\nPARAMETER num_ctx ${ctx}\\nPARAMETER temperature 0.2\\nPARAMETER repeat_penalty 1.08`;
            const runCmd = `ollama create ${customName} -f Modelfile\\nollama run ${customName}`;
            box.innerHTML = `
              <div class="p-4 rounded-2xl bg-slate-900 text-slate-100 font-mono text-xs overflow-x-auto">
                <div class="text-purple-400 font-sans font-bold uppercase mb-2">1. Environment Variables (${os === 'win' ? 'Windows PowerShell' : 'Linux/macOS Bash'})</div>
                <pre style="white-space:pre-wrap;">${envBlock}</pre>
              </div>
              <div class="p-4 rounded-2xl bg-slate-900 text-slate-100 font-mono text-xs overflow-x-auto">
                <div class="text-emerald-400 font-sans font-bold uppercase mb-2">2. Custom Modelfile (Save as Modelfile)</div>
                <pre style="white-space:pre-wrap;">${modelfile}</pre>
              </div>
              <div class="p-4 rounded-2xl bg-slate-900 text-slate-100 font-mono text-xs overflow-x-auto">
                <div class="text-blue-400 font-sans font-bold uppercase mb-2">3. Build &amp; Launch Commands</div>
                <pre style="white-space:pre-wrap;">${runCmd}</pre>
              </div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Tip: Verify exact VRAM headroom first using our <a href="/tools/llm-vram-calculator/" class="text-blue-600 dark:text-blue-400 font-bold hover:underline">LLM VRAM Calculator</a>.</p>
            `;
            box.classList.remove('hidden');
          });
        })();
        """,
        "guide_title": "Why Default Ollama Settings Waste GPU Speed (and How Flash Attention Fixes It)",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Out of the box, Ollama defaults to a <code>2048</code> or <code>4096</code> token context window and uncompressed <code>f16</code> KV cache. For coding assistants inside VS Code (Continue.dev, Cline, or Roo Code), small context truncates your open files, while jumping straight to <code>32768</code> tokens without KV cache quantization can push a 14B or 32B model over your GPU VRAM limit and trigger slow system RAM spillover.</p>
        <h3 class="text-base font-bold text-gray-900 dark:text-white mt-5 mb-2">Enabling Flash Attention &amp; q8_0 KV Cache</h3>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Setting <code>OLLAMA_FLASH_ATTENTION=1</code> together with <code>OLLAMA_KV_CACHE_TYPE=q8_0</code> cuts context memory consumption by roughly 45% with virtually zero perplexity drop on coding and reasoning tasks. On a 24GB RTX 3090 or RTX 4090, this unlocks 16K–32K context on 32B Q4_K_M models while keeping 100% of layers in fast GDDR6X memory.</p>
        <h3 class="text-base font-bold text-gray-900 dark:text-white mt-5 mb-2">Choosing Temperature for Coding vs. Chat</h3>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">Keep <code>PARAMETER temperature 0.2</code> in your coding Modelfile to prevent hallucinated imports and syntax drift. Pair this generator with our <a href="/best-local-ai-models-for-coding-2026-qwen-coder-vs-deepseek-benchmarks/" class="text-blue-600 dark:text-blue-400 font-semibold hover:underline">Best Local LLM for Coding 2026 Guide</a> and <a href="/14b-vs-32b-vs-70b-local-llms-24gb-vram-quantization-speed-guide-2026/" class="text-blue-600 dark:text-blue-400 font-semibold hover:underline">14B vs 32B vs 70B 24GB VRAM Analysis</a>.</p>
        """
    },
    {
        "slug": "dual-gpu-vram-split-calculator",
        "icon": "🎛️",
        "badge": "Multi-GPU Local AI",
        "h1": "Dual-GPU VRAM Split Calculator (llama.cpp & Ollama)",
        "title": "Dual-GPU VRAM Split Calculator (2026) — Tech Boss",
        "description": "Calculate exact llama.cpp --tensor-split ratios and combined VRAM budgets for mismatched dual-GPU setups like RTX 3090 24GB + RTX 3060 12GB.",
        "capsule_title": "Mismatched Dual-GPU Layer Balancing",
        "capsule_text": "Enter both GPU VRAM sizes and your target GGUF model to compute combined usable VRAM, display-headroom safety margin, and exact llama.cpp --tensor-split weights.",
        "tool_html": """
        <section id="dualGpuTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Primary GPU (Display + Compute)</label>
              <select id="gpu1Vram" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="24" selected>24 GB (RTX 3090 / 4090 / 7900 XTX)</option>
                <option value="32">32 GB (RTX 5090)</option>
                <option value="16">16 GB (RTX 5070 Ti / 4080 / 4060 Ti)</option>
                <option value="12">12 GB (RTX 3060 / 4070 / 5070)</option>
                <option value="8">8 GB (RTX 4060 / 3070)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Secondary GPU (Headless Compute)</label>
              <select id="gpu2Vram" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="24">24 GB (RTX 3090 / 4090 / P40)</option>
                <option value="16">16 GB (RTX 4060 Ti / 5070 Ti)</option>
                <option value="12" selected>12 GB (RTX 3060 / 4070)</option>
                <option value="8">8 GB (RTX 3060 Ti / 4060)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Target Model Size (Q4_K_M)</label>
              <select id="dualModelGb" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="21.5">32B Q4_K_M (~21.5 GB total w/ 8K ctx)</option>
                <option value="30.5" selected>49B–56B / 32B Q6_K (~30.5 GB total)</option>
                <option value="44.0">70B Q4_K_M (~44.0 GB total w/ 8K ctx)</option>
                <option value="65.0">123B Mistral Large Q4 (~65.0 GB)</option>
              </select>
            </div>
          </div>
          <button id="calcDualGpuBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow transition-colors">
            🎛️ Compute Dual-GPU Tensor Split
          </button>
          <div id="dualGpuResultBox" class="hidden mt-6 p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const btn = document.getElementById('calcDualGpuBtn');
          const box = document.getElementById('dualGpuResultBox');
          if (!btn || !box) return;
          btn.addEventListener('click', () => {
            const g1 = parseFloat(document.getElementById('gpu1Vram').value);
            const g2 = parseFloat(document.getElementById('gpu2Vram').value);
            const need = parseFloat(document.getElementById('dualModelGb').value);
            const usable1 = Math.max(0, g1 - 1.8);
            const usable2 = Math.max(0, g2 - 0.6);
            const totalUsable = +(usable1 + usable2).toFixed(1);
            const r1 = Math.round((usable1 / (usable1 + usable2)) * 100);
            const r2 = 100 - r1;
            const fits = totalUsable >= need;
            const status = fits
              ? `<span class="text-emerald-600 dark:text-emerald-400 font-extrabold">✅ 100% Dual-GPU Offload Fits (${totalUsable} GB usable vs ${need} GB needed)</span>`
              : `<span class="text-rose-600 dark:text-rose-400 font-extrabold">⚠️ Short by ${(need - totalUsable).toFixed(1)} GB — Will Spill to System RAM</span>`;
            box.innerHTML = `
              <div class="mb-3 text-base">${status}</div>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4 text-xs">
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><div class="text-gray-500">GPU 0 Usable (OS Reserve)</div><div class="text-base font-bold text-gray-900 dark:text-white">${usable1.toFixed(1)} GB</div></div>
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><div class="text-gray-500">GPU 1 Usable (Headless)</div><div class="text-base font-bold text-gray-900 dark:text-white">${usable2.toFixed(1)} GB</div></div>
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><div class="text-gray-500">Recommended Split Ratio</div><div class="text-base font-bold text-indigo-600 dark:text-indigo-400">${r1},${r2}</div></div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-900 text-emerald-300 font-mono text-xs overflow-x-auto">
                llama-server -m model.gguf -ngl 99 --split-mode layer --tensor-split ${r1},${r2} -fa
              </div>
            `;
            box.classList.remove('hidden');
          });
        })();
        """,
        "guide_title": "Engineering Mismatched Dual-GPU Rigs for Local LLMs",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">You do not need two identical flagship cards to run 48GB+ local language models. Pairing a used 24GB RTX 3090 with an affordable 12GB RTX 3060 gives you 36GB of raw VRAM—enough to run 32B models at Q6_K/Q8_0 precision or 70B models at IQ3_XS/IQ4_XS quantization without touching slow system DDR5.</p>
        <h3 class="text-base font-bold text-gray-900 dark:text-white mt-5 mb-2">Why GPU 0 Needs Extra Headroom</h3>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Your primary display GPU holds the Windows Desktop Window Manager (DWM), browser GPU buffers, and CUDA context overhead (typically 1.5–2.0 GB). Using an even 50/50 split on mismatched GPUs—or ignoring display overhead—causes instant Out-Of-Memory (OOM) crashes on GPU 0 while GPU 1 still sits half-empty.</p>
        <h3 class="text-base font-bold text-gray-900 dark:text-white mt-5 mb-2">PCIe Bandwidth &amp; Power Supply Notes</h3>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">Under <code>--split-mode layer</code>, only compact activation tensors cross the PCIe bus between GPUs, meaning even a PCIe Gen 3 x4 chipset slot works reliably for inference. Always verify combined transient wattage with our <a href="/tools/pc-power-supply-calculator/" class="text-blue-600 dark:text-blue-400 font-semibold hover:underline">PC Power Supply Calculator</a>.</p>
        """
    },
    {
        "slug": "json-jwt-cron-dev-toolkit",
        "icon": "🧰",
        "badge": "100% Client-Side Dev Utilities",
        "h1": "Offline JSON Formatter, JWT Decoder & Cron Explainer",
        "title": "Offline JSON, JWT Decoder & Cron Toolkit — Tech Boss",
        "description": "Format and validate JSON, decode JWT headers/payloads locally in your browser (zero server upload), and translate 5-field Cron expressions into plain English.",
        "capsule_title": "Zero-Upload Browser-Local Developer Toolkit",
        "capsule_text": "All JSON formatting, JWT base64url decoding, and Cron parsing runs 100% locally inside your browser JavaScript runtime. No tokens or payloads ever leave your device.",
        "tool_html": """
        <section id="devToolkitTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm space-y-8">
          <div>
            <h2 class="text-lg font-extrabold text-gray-900 dark:text-white mb-2">1. JSON Formatter &amp; Validator</h2>
            <textarea id="jsonInput" rows="4" placeholder='{"site":"imtechboss","tools":17,"offline":true}' class="w-full p-3 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 font-mono text-xs text-gray-900 dark:text-white mb-3"></textarea>
            <button id="formatJsonBtn" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow">Format &amp; Validate JSON</button>
            <pre id="jsonOutputBox" class="hidden mt-3 p-4 rounded-xl bg-slate-900 text-emerald-300 font-mono text-xs overflow-x-auto"></pre>
          </div>
          <div class="pt-6 border-t border-gray-200 dark:border-slate-800">
            <h2 class="text-lg font-extrabold text-gray-900 dark:text-white mb-2">2. Local JWT Token Decoder (Zero Network Transmission)</h2>
            <textarea id="jwtInput" rows="3" placeholder="Paste eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlRlY2ggQm9zcyJ9.signature" class="w-full p-3 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 font-mono text-xs text-gray-900 dark:text-white mb-3"></textarea>
            <button id="decodeJwtBtn" class="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs shadow">Decode JWT Locally</button>
            <pre id="jwtOutputBox" class="hidden mt-3 p-4 rounded-xl bg-slate-900 text-sky-300 font-mono text-xs overflow-x-auto"></pre>
          </div>
          <div class="pt-6 border-t border-gray-200 dark:border-slate-800">
            <h2 class="text-lg font-extrabold text-gray-900 dark:text-white mb-2">3. 5-Field Cron Expression Explainer</h2>
            <div class="flex flex-col sm:flex-row gap-3">
              <input id="cronInput" type="text" value="*/15 * * * 1-5" class="flex-1 px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 font-mono text-sm text-gray-900 dark:text-white" />
              <button id="explainCronBtn" class="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow">Explain Cron</button>
            </div>
            <div id="cronOutputBox" class="hidden mt-3 p-4 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm text-gray-900 dark:text-white"></div>
          </div>
        </section>
        """,
        "tool_js": """
        (function() {
          const jBtn = document.getElementById('formatJsonBtn');
          const jOut = document.getElementById('jsonOutputBox');
          if (jBtn && jOut) {
            jBtn.addEventListener('click', () => {
              const raw = (document.getElementById('jsonInput').value || '').trim() || '{"site":"imtechboss","tools":17,"offline":true}';
              try {
                const parsed = JSON.parse(raw);
                jOut.textContent = JSON.stringify(parsed, null, 2);
              } catch (e) {
                jOut.textContent = 'Invalid JSON: ' + e.message;
              }
              jOut.classList.remove('hidden');
            });
          }

          const jwtBtn = document.getElementById('decodeJwtBtn');
          const jwtOut = document.getElementById('jwtOutputBox');
          if (jwtBtn && jwtOut) {
            jwtBtn.addEventListener('click', () => {
              const raw = (document.getElementById('jwtInput').value || '').trim() || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlRlY2ggQm9zcyIsInJvbGUiOiJlZGl0b3IifQ.sig';
              try {
                const parts = raw.split('.');
                if (parts.length < 2) throw new Error('JWT must contain at least header.payload');
                const dec = (s) => JSON.parse(atob(s.replace(/-/g, '+').replace(/_/g, '/').padEnd(Math.ceil(s.length / 4) * 4, '=')));
                jwtOut.textContent = 'HEADER:\\n' + JSON.stringify(dec(parts[0]), null, 2) + '\\n\\nPAYLOAD:\\n' + JSON.stringify(dec(parts[1]), null, 2);
              } catch (e) {
                jwtOut.textContent = 'JWT Decode Error: ' + e.message;
              }
              jwtOut.classList.remove('hidden');
            });
          }

          const cBtn = document.getElementById('explainCronBtn');
          const cOut = document.getElementById('cronOutputBox');
          if (cBtn && cOut) {
            cBtn.addEventListener('click', () => {
              const expr = (document.getElementById('cronInput').value || '').trim();
              const p = expr.split(/\\s+/);
              if (p.length !== 5) {
                cOut.textContent = 'Please enter a standard 5-field cron expression (minute hour day-of-month month day-of-week).';
              } else {
                const [min, hr, dom, mon, dow] = p;
                const desc = (val, unit) => val === '*' ? `every ${unit}` : val.startsWith('*/') ? `every ${val.slice(2)} ${unit}s` : `${unit} ${val}`;
                cOut.innerHTML = `<strong>Schedule Breakdown:</strong> Runs at <code>${desc(min, 'minute')}</code>, <code>${desc(hr, 'hour')}</code>, <code>${desc(dom, 'day of month')}</code>, <code>${desc(mon, 'month')}</code>, on <code>${desc(dow, 'day of week')}</code>.`;
              }
              cOut.classList.remove('hidden');
            });
          }
        })();
        """,
        "guide_title": "Why Developers Prefer Client-Side Offline Inspection Tools",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Pasting production API responses or live OAuth JWT tokens into third-party server-backed web tools risks leaking bearer secrets into server access logs. Every utility on this page executes strictly inside your browser's JavaScript sandbox with zero external API requests.</p>
        <h3 class="text-base font-bold text-gray-900 dark:text-white mt-5 mb-2">Common Cron Expressions Cheat Sheet</h3>
        <ul class="list-disc pl-5 space-y-1.5 text-sm text-gray-600 dark:text-gray-300">
          <li><code>*/5 * * * *</code> — Runs every 5 minutes (health checks, queue workers)</li>
          <li><code>0 2 * * *</code> — Runs daily at 02:00 AM (database backups &amp; sitemap builds)</li>
          <li><code>0 9 * * 1-5</code> — Runs weekdays Monday through Friday at 09:00 AM</li>
          <li><code>0 0 1 * *</code> — Runs on the 1st of every month at midnight</li>
        </ul>
        """
    },
    {
        "slug": "ssd-nvme-pcie-speed-calculator",
        "icon": "💾",
        "badge": "Storage & Motherboard Engineering",
        "h1": "NVMe SSD PCIe Gen 3 vs Gen 4 vs Gen 5 Speed Calculator",
        "title": "NVMe SSD PCIe Speed & Bottleneck Calculator — Tech Boss",
        "description": "Check real-world sequential read/write ceilings when pairing PCIe Gen 3, Gen 4, or Gen 5 NVMe SSDs with older x4 or x2 motherboard M.2 slots.",
        "capsule_title": "Real M.2 Slot Throughput Ceiling",
        "capsule_text": "NVMe drives negotiate down to the lower PCIe generation and lane width of either the drive or motherboard M.2 slot. Check your real effective ceiling before upgrading.",
        "tool_html": """
        <section id="nvmeSpeedTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">NVMe SSD Rating</label>
              <select id="nvmeDriveGen" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="3">PCIe Gen 3.0 x4 (~3,500 MB/s)</option>
                <option value="4" selected>PCIe Gen 4.0 x4 (~7,400 MB/s)</option>
                <option value="5">PCIe Gen 5.0 x4 (~14,500 MB/s)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Motherboard M.2 Slot Gen</label>
              <select id="nvmeSlotGen" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="3" selected>PCIe Gen 3.0 Slot</option>
                <option value="4">PCIe Gen 4.0 Slot</option>
                <option value="5">PCIe Gen 5.0 Slot</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Active M.2 Lanes</label>
              <select id="nvmeLanes" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="4" selected>x4 Lanes (Standard Primary M.2)</option>
                <option value="2">x2 Lanes (Shared Chipset / Budget Laptop)</option>
              </select>
            </div>
          </div>
          <button id="calcNvmeBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-cyan-600 hover:bg-cyan-700 text-white font-bold text-sm shadow transition-colors">
            💾 Calculate Effective NVMe Speed
          </button>
          <div id="nvmeResultBox" class="hidden mt-6 p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const btn = document.getElementById('calcNvmeBtn');
          const box = document.getElementById('nvmeResultBox');
          if (!btn || !box) return;
          const MAX_PER_LANE = { 3: 875, 4: 1850, 5: 3625 };
          btn.addEventListener('click', () => {
            const dGen = parseInt(document.getElementById('nvmeDriveGen').value, 10);
            const sGen = parseInt(document.getElementById('nvmeSlotGen').value, 10);
            const lanes = parseInt(document.getElementById('nvmeLanes').value, 10);
            const effGen = Math.min(dGen, sGen);
            const driveMax = MAX_PER_LANE[dGen] * 4;
            const effSpeed = MAX_PER_LANE[effGen] * lanes;
            const lossPct = Math.max(0, Math.round(((driveMax - effSpeed) / driveMax) * 100));
            box.innerHTML = `
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-3 text-xs">
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><div class="text-gray-500">Negotiated Link</div><div class="text-base font-extrabold text-cyan-600 dark:text-cyan-400">PCIe Gen ${effGen}.0 x${lanes}</div></div>
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><div class="text-gray-500">Effective Sequential Cap</div><div class="text-base font-extrabold text-gray-900 dark:text-white">~${effSpeed.toLocaleString()} MB/s</div></div>
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><div class="text-gray-500">Sequential Bottleneck</div><div class="text-base font-extrabold ${lossPct > 0 ? 'text-amber-600' : 'text-emerald-600'}">${lossPct}% Capped</div></div>
              </div>
              <p class="text-xs text-gray-600 dark:text-gray-300">${lossPct > 0 ? 'Your drive is backward-compatible and will run cooler, but peak sequential transfers are capped by the motherboard slot. Random 4K OS responsiveness remains fast.' : 'Full rated sequential throughput unlocked with zero PCIe slot bottleneck.'}</p>
            `;
            box.classList.remove('hidden');
          });
        })();
        """,
        "guide_title": "Understanding Real-World NVMe Speed vs. Marketing Box Numbers",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Sequential throughput (e.g., 7,400 MB/s on PCIe Gen 4 or 14,500 MB/s on PCIe Gen 5) only matters when copying huge video files or loading 20GB+ local LLM GGUF weights from disk into VRAM. For Windows boot times and application launches, 4K random read latency (QD1) matters far more than raw sequential bandwidth.</p>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">If your NVMe drive suddenly shows RAW partitions or severe slowdown after Windows 11 24H2 BitLocker encryption, check our <a href="/windows-11-24h2-bitlocker-ssd-slowdown-benchmarks-fix-guide-2026/" class="text-blue-600 dark:text-blue-400 font-semibold hover:underline">Windows 11 24H2 BitLocker SSD Fix</a> and <a href="/how-to-recover-corrupted-nvme-ssd-data-windows-11/" class="text-blue-600 dark:text-blue-400 font-semibold hover:underline">NVMe Data Recovery Guide</a>.</p>
        """
    },
    {
        "slug": "local-ai-electricity-cost-calculator",
        "icon": "⚡",
        "badge": "Global USD & Nepal NEA Tariff",
        "h1": "GPU Rig & Local AI Electricity Cost Calculator (USD & NPR)",
        "title": "GPU & Local AI Electricity Cost Calculator (USD/NPR) — Tech Boss",
        "description": "Calculate exact monthly and yearly electricity bills for gaming PCs and 24/7 Ollama local AI rigs in both USD ($/kWh) and Nepal NPR (NEA electricity rates).",
        "capsule_title": "Real Power Bill Estimator (USD & Nepal NPR)",
        "capsule_text": "Enter average system load watts, daily hours, and currency (Global USD or Nepal Electricity Authority NPR/unit) to compare local GPU electricity costs against cloud AI subscriptions.",
        "tool_html": """
        <section id="powerCostTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Total Wall Power Draw (Watts)</label>
              <input id="rigWatts" type="number" value="350" min="20" max="2000" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Active Hours Per Day</label>
              <input id="rigHours" type="number" value="6" min="1" max="24" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Electricity Tariff Preset</label>
              <select id="tariffPreset" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="NPR|10.5" selected>Nepal NEA Domestic (~Rs. 10.50 / kWh)</option>
                <option value="NPR|12.0">Nepal NEA High Slab (~Rs. 12.00 / kWh)</option>
                <option value="USD|0.16">USA Average ($0.16 / kWh)</option>
                <option value="USD|0.32">Europe / UK Average ($0.32 / kWh)</option>
              </select>
            </div>
          </div>
          <button id="calcPowerCostBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-sm shadow transition-colors">
            ⚡ Calculate Monthly Power Bill
          </button>
          <div id="powerCostResultBox" class="hidden mt-6 p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const btn = document.getElementById('calcPowerCostBtn');
          const box = document.getElementById('powerCostResultBox');
          if (!btn || !box) return;
          btn.addEventListener('click', () => {
            const w = Math.max(10, parseFloat(document.getElementById('rigWatts').value) || 350);
            const h = Math.min(24, Math.max(1, parseFloat(document.getElementById('rigHours').value) || 6));
            const [curr, rateStr] = document.getElementById('tariffPreset').value.split('|');
            const rate = parseFloat(rateStr);
            const kwhMonth = (w / 1000) * h * 30;
            const costMonth = kwhMonth * rate;
            const costYear = costMonth * 12;
            const sym = curr === 'NPR' ? 'Rs. ' : '$';
            box.innerHTML = `
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><div class="text-gray-500">Monthly Energy (Units)</div><div class="text-base font-extrabold text-gray-900 dark:text-white">${kwhMonth.toFixed(1)} kWh</div></div>
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><div class="text-gray-500">Estimated Monthly Cost</div><div class="text-base font-extrabold text-amber-600 dark:text-amber-400">${sym}${costMonth.toFixed(2)}</div></div>
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><div class="text-gray-500">Estimated Yearly Cost</div><div class="text-base font-extrabold text-gray-900 dark:text-white">${sym}${costYear.toFixed(2)}</div></div>
              </div>
              <p class="text-xs text-gray-600 dark:text-gray-300 mt-3">Note: Local AI inference spikes wattage only while generating tokens; idle GPUs typically drop to 15–35W. Undervolting an RTX GPU by 15% cuts power bills with under 3% speed loss.</p>
            `;
            box.classList.remove('hidden');
          });
        })();
        """,
        "guide_title": "Local GPU Electricity vs. Paid Cloud AI Subscriptions",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Running a 350W RTX desktop actively for 6 hours per day consumes 63 kWh (units) per month—roughly Rs. 660/month in Nepal or ~$10/month in the US. Compared to $20–$200/month cloud API bills, local LLMs quickly pay off when you already own a capable GPU.</p>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">For PSU sizing and safe transient headroom on modern RTX 40/50-series cards, pair this estimator with our <a href="/tools/pc-power-supply-calculator/" class="text-blue-600 dark:text-blue-400 font-semibold hover:underline">PC Power Supply Calculator</a>.</p>
        """
    },
    {
        "slug": "nepal-laptop-budget-finder",
        "icon": "🇳🇵",
        "badge": "Nepal Tech Buying Advisor",
        "h1": "Nepal Laptop Budget & Specs Finder (NPR 2026)",
        "title": "Nepal Laptop Budget Finder (Rs. 60k–2.5L NPR) — Tech Boss",
        "description": "Find the right laptop specs in Nepal for your exact NPR budget (Rs. 60,000 to Rs. 2,50,000+) across CSIT/coding, gaming, video editing, and local AI workloads.",
        "capsule_title": "Avoid Overpaying in Kathmandu / Putalisadak / New Road",
        "capsule_text": "Pick your NPR budget bracket and primary workload to see the exact minimum CPU, RAM, SSD, GPU, and display panel specs you should demand before buying in Nepal.",
        "tool_html": """
        <section id="nepalLaptopTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Your Budget in Nepal (NPR)</label>
              <select id="npBudget" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="70k">Rs. 60,000 – Rs. 80,000 (Student / Office)</option>
                <option value="100k" selected>Rs. 80,000 – Rs. 1,10,000 (CSIT / Coding Sweet Spot)</option>
                <option value="150k">Rs. 1,10,000 – Rs. 1,60,000 (Gaming / Editing / RTX 4050-4060)</option>
                <option value="220k">Rs. 1,60,000 – Rs. 2,50,000+ (Pro Dev / Local AI / MacBook Pro)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Primary Workload</label>
              <select id="npUse" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="coding" selected>CSIT / BIT / Web &amp; App Programming</option>
                <option value="gaming">1080p / 1440p Gaming + 3D</option>
                <option value="ai">Local AI (Ollama / Python ML)</option>
                <option value="office">Office, Accounting &amp; Portability</option>
              </select>
            </div>
          </div>
          <button id="findNepalLaptopBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm shadow transition-colors">
            🇳🇵 Get Minimum Specs &amp; Nepal Buying Advice
          </button>
          <div id="nepalLaptopResultBox" class="hidden mt-6 p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const btn = document.getElementById('findNepalLaptopBtn');
          const box = document.getElementById('nepalLaptopResultBox');
          if (!btn || !box) return;
          const DATA = {
            "70k": {
              tier: "Entry Student / Coding Baseline (Rs. 60k–80k)",
              cpu: "AMD Ryzen 5 7520U / 5500U or Intel Core i5-1235U / 1335U",
              ram: "16GB DDR4/LPDDR5 (Avoid 8GB soldered models!)",
              gpu: "Integrated Radeon / Iris Xe",
              screen: "15.6\" or 14\" Full HD IPS (Reject washed-out TN panels)",
              models: "Acer Aspire 5, Lenovo IdeaPad Slim 3 (Ryzen 5), Asus Vivobook Go 15",
              warn: "Verify genuine VAT bill & 1-year authorized distributor warranty; avoid older Celeron/i3 8GB stock cleared at Rs. 65k."
            },
            "100k": {
              tier: "Nepal CSIT & Developer Sweet Spot (Rs. 80k–1.1L)",
              cpu: "Ryzen 5 7535HS / Intel Core i5-13420H or Apple M1/M2 (16GB if found)",
              ram: "16GB DDR5 (Upgradeable dual-slot preferred)",
              gpu: "RTX 2050/3050 (6GB) for Gaming/AI OR Integrated for 8+ hr battery",
              screen: "100% sRGB IPS or 144Hz FHD IPS",
              models: "Lenovo LOQ Essential, Acer Nitro V 15 (RTX 3050 6GB), Asus Zenbook 14 / Vivobook S14",
              warn: "For programming/Docker/Android Studio, 16GB RAM + 512GB Gen 4 NVMe is mandatory—never buy 8GB RAM above Rs. 80,000."
            },
            "150k": {
              tier: "Performance Gaming, Video Editing & Entry Local AI (Rs. 1.1L–1.6L)",
              cpu: "Ryzen 7 7435HS / 8845HS or Intel Core i7-13620H / Core Ultra 5",
              ram: "16GB–32GB DDR5-5600",
              gpu: "NVIDIA RTX 4050 (6GB) or RTX 4060 (8GB VRAM — Best Value for Ollama 8B/14B!)",
              screen: "144Hz–165Hz 100% sRGB IPS",
              models: "Lenovo LOQ 15 (RTX 4060), Acer Predator Helios Neo 16, Asus TUF A15 (RTX 4060)",
              warn: "Check GPU TGP wattage (look for 100W+ RTX 4060, not 45W thin-and-light capped variants) and check keyboard layout/sealed box."
            },
            "220k": {
              tier: "Pro Engineering, Heavy Local AI & Creator Tier (Rs. 1.6L–2.5L+)",
              cpu: "Apple M3/M4 Pro (18GB–24GB Unified RAM) or Ryzen 9 / Core Ultra 7",
              ram: "24GB–32GB Unified or DDR5",
              gpu: "RTX 4070 / 5060-5070 Laptop (8GB–12GB) or Apple Unified Memory for 14B–32B LLMs",
              screen: "2.5K QHD 165Hz+ or Liquid Retina XDR",
              models: "MacBook Pro 14 (18GB/24GB), Lenovo Legion 5 Pro, Asus ROG Zephyrus G14/G16",
              warn: "If running 14B–32B local AI models on laptop, Apple Silicon 24GB+ Unified Memory outperforms 8GB NVIDIA laptop GPUs."
            }
          };
          btn.addEventListener('click', () => {
            const b = document.getElementById('npBudget').value;
            const use = document.getElementById('npUse').value;
            const d = DATA[b];
            const extra = use === 'ai'
              ? 'Local AI Priority: Aim for at least 8GB NVIDIA VRAM (RTX 4060) or 16GB–24GB Apple Unified Memory to run 8B–14B Ollama models cleanly.'
              : use === 'gaming'
              ? 'Gaming Priority: Demand 100W+ TGP NVIDIA RTX GPU and dual-channel 16GB DDR5 for smooth 1% lows.'
              : use === 'coding'
              ? 'Coding Priority: Prioritize 16GB+ RAM, 512GB+ NVMe SSD, Linux/WSL2 compatibility, and a sharp IPS display.'
              : 'Office Priority: Prioritize 1.4kg weight, USB-C PD charging, and 7+ hour battery life over dedicated GPU.';
            box.innerHTML = `
              <h3 class="text-base font-extrabold text-emerald-700 dark:text-emerald-400 mb-3">${d.tier}</h3>
              <ul class="space-y-1.5 text-sm text-gray-800 dark:text-gray-200 mb-3">
                <li><strong>Target CPU:</strong> ${d.cpu}</li>
                <li><strong>Minimum RAM:</strong> ${d.ram}</li>
                <li><strong>GPU Target:</strong> ${d.gpu}</li>
                <li><strong>Display:</strong> ${d.screen}</li>
                <li><strong>Shortlist Models in Nepal:</strong> ${d.models}</li>
              </ul>
              <p class="text-xs font-semibold text-blue-700 dark:text-blue-300 mb-2">🎯 ${extra}</p>
              <p class="text-xs text-amber-700 dark:text-amber-300">⚠️ <strong>Nepal Buyer Checklist:</strong> ${d.warn}</p>
              <div class="mt-3"><a href="/best-laptops-under-1-lakh-npr-nepal-2026-coding-csit-guide/" class="text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline">Read Full Nepal Laptop Buying Guide &rarr;</a></div>
            `;
            box.classList.remove('hidden');
          });
        })();
        """,
        "guide_title": "How to Verify Authentic Laptops in Nepal (Putalisadak, New Road & Online)",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Laptop prices in Nepal fluctuate based on official authorized imports versus grey-market channels. Before paying Rs. 80,000 to Rs. 2,50,000, always verify three things in-store: check the serial number directly on Lenovo/Asus/Acer/Apple's official warranty portal, inspect SSD power-on hours using CrystalDiskInfo (a brand-new laptop should show under 5–10 hours), and confirm whether RAM is upgradeable or soldered.</p>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">For detailed model breakdowns, read our <a href="/best-laptops-under-1-lakh-npr-nepal-2026-coding-csit-guide/" class="text-blue-600 dark:text-blue-400 font-semibold hover:underline">Best Laptops Under 1 Lakh NPR in Nepal</a> and <a href="/run-local-ai-ollama-budget-gaming-laptop-nepal-rtx-3050-4050-4060/" class="text-blue-600 dark:text-blue-400 font-semibold hover:underline">Running Ollama on Budget Gaming Laptops in Nepal</a>.</p>
        """
    },
    {
        "slug": "nepal-isp-router-mesh-advisor",
        "icon": "📡",
        "badge": "Nepal Fiber & Wi-Fi 6 Planner",
        "h1": "Nepal ISP Router, Wi-Fi 6 Mesh & Ping Optimizer",
        "title": "Nepal ISP Wi-Fi Mesh & Ping Advisor (WorldLink/Vianet/CGNet) — Tech Boss",
        "description": "Plan Wi-Fi 6 routers, concrete-wall mesh nodes, and low-ping Bridge Mode settings for WorldLink, Vianet, CGNet, and Subisu fiber connections in Nepal.",
        "capsule_title": "Built for Nepali Concrete Houses & Multi-Floor Flats",
        "capsule_text": "Nepali RCC concrete pillars and brick walls kill 5GHz Wi-Fi within two rooms. Enter your ISP, house floors, and devices to get the right secondary router, Ethernet backhaul, and ping fix.",
        "tool_html": """
        <section id="nepalIspTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Nepal Fiber ISP</label>
              <select id="npIsp" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="WorldLink" selected>WorldLink (Nokia / Huawei ONT)</option>
                <option value="Vianet">Vianet (XGS-PON / Dual-Band ONT)</option>
                <option value="CGNet">CGNet (Fiber ONT)</option>
                <option value="Subisu">Subisu / ClassicTech</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">House Layout (Concrete Walls)</label>
              <select id="npFloors" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="1">Single Flat (2–4 Rooms)</option>
                <option value="2" selected>2-Floor Concrete House</option>
                <option value="3">3+ Floor House / Office</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Top Priority</label>
              <select id="npPriority" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="gaming" selected>Low Gaming Ping &amp; Zoom Calls</option>
                <option value="coverage">Full-House Wi-Fi Coverage</option>
                <option value="budget">Budget Fix Under Rs. 5,000</option>
              </select>
            </div>
          </div>
          <button id="calcNepalIspBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-bold text-sm shadow transition-colors">
            📡 Generate Nepal Wi-Fi &amp; Ping Blueprint
          </button>
          <div id="nepalIspResultBox" class="hidden mt-6 p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const btn = document.getElementById('calcNepalIspBtn');
          const box = document.getElementById('nepalIspResultBox');
          if (!btn || !box) return;
          btn.addEventListener('click', () => {
            const isp = document.getElementById('npIsp').value;
            const floors = parseInt(document.getElementById('npFloors').value, 10);
            const prio = document.getElementById('npPriority').value;
            const nodes = floors === 1 ? '1 Wi-Fi 6 Router (AX1800/AX3000)' : floors === 2 ? '2-Node Wired Backhaul Mesh (1 per floor)' : '3-Node Wired Cat6 Ethernet Mesh (1 per floor)';
            const cost = floors === 1 ? 'Rs. 4,500 – Rs. 7,500' : floors === 2 ? 'Rs. 9,000 – Rs. 15,000' : 'Rs. 16,000 – Rs. 24,000';
            const pingTip = prio === 'gaming'
              ? `Keep gaming PC/PS5 wired via Cat6 cable, set DNS to 1.1.1.1 / 8.8.8.8, and ask ${isp} support to verify clean optical power (-16 to -23 dBm) or enable Bridge Mode if using your own SQM/QoS router.`
              : `Run a single Cat6 cable between floors instead of wireless repeaters; wireless repeaters cut throughput by 50% through Nepali concrete slabs.`;
            box.innerHTML = `
              <h3 class="text-base font-extrabold text-teal-700 dark:text-teal-400 mb-3">${isp} Recommended Topology (${floors}-Floor Setup)</h3>
              <ul class="space-y-1.5 text-sm text-gray-800 dark:text-gray-200 mb-3">
                <li><strong>Hardware Setup:</strong> ${nodes}</li>
                <li><strong>Estimated Nepal Budget:</strong> ${cost} (TP-Link Archer AX23 / Deco X20 / Xiaomi AX3000T)</li>
                <li><strong>Backhaul Rule:</strong> Always connect floor-to-floor secondary routers using Cat6 Ethernet in Access Point (AP) mode to avoid Double NAT.</li>
                <li><strong>5GHz Channel Tip:</strong> Set 5GHz width to 80MHz on non-overlapping channels (36 or 149) to stop neighbor interference in Kathmandu/Pokhara apartments.</li>
              </ul>
              <p class="text-xs text-blue-700 dark:text-blue-300 mb-2">⚡ ${pingTip}</p>
              <a href="/worldlink-vianet-cgnet-router-wifi-mesh-gaming-ping-fix-nepal/" class="text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline">Read Full Nepal ISP Router &amp; Ping Guide &rarr;</a>
            `;
            box.classList.remove('hidden');
          });
        })();
        """,
        "guide_title": "Why Fiber Speed Drops Upstairs in Nepali Concrete Homes",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Even on a 200–300 Mbps fiber plan from WorldLink, Vianet, or CGNet, an ISP-provided single ONT router struggles to penetrate reinforced concrete slabs (RCC) and brick walls. Cheap wireless Wi-Fi repeaters amplify weak signal while halving bandwidth and doubling ping jitter.</p>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">The cleanest fix in Nepal is running one affordable Cat6 cable from the main ONT LAN port to a secondary Wi-Fi 6 router placed upstairs in <strong>Access Point (AP) mode</strong>. See our full <a href="/worldlink-vianet-cgnet-router-wifi-mesh-gaming-ping-fix-nepal/" class="text-blue-600 dark:text-blue-400 font-semibold hover:underline">WorldLink, Vianet &amp; CGNet Router Optimization Guide</a>.</p>
        """
    },
]


def render_extended_tools(root_dir, existing_tools_summary):
    all_links = existing_tools_summary + [
        {"slug": t["slug"], "icon": t["icon"], "h1": t["h1"], "badge": t["badge"]}
        for t in EXTENDED_TOOLS
    ]
    for cfg in EXTENDED_TOOLS:
        slug = cfg["slug"]
        canonical_url = f"https://imtechboss.com/tools/{slug}/"
        other_tools_html = ""
        for other in all_links:
            if other["slug"] == slug:
                continue
            other_tools_html += f"""
            <a href="/tools/{other['slug']}/" class="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 hover:border-blue-500 hover:shadow-md transition-all flex items-center gap-3 group">
              <span class="text-2xl">{other['icon']}</span>
              <div>
                <h4 class="font-bold text-xs sm:text-sm text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{other['h1']}</h4>
                <p class="text-[11px] text-gray-500 dark:text-gray-400 mt-0.5 line-clamp-1">{other['badge']}</p>
              </div>
            </a>
            """

        page_html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-HQDRHTFW7Q"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-HQDRHTFW7Q');
  </script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <title>{cfg['title']}</title>
  <meta name="description" content="{cfg['description']}">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{cfg['title']}">
  <meta property="og:description" content="{cfg['description']}">
  <meta property="og:site_name" content="Tech Boss">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{cfg['title']}">
  <meta name="twitter:description" content="{cfg['description']}">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2220%22 fill=%22%232563eb%22/><text x=%2250%25%22 y=%2254%25%22 dominant-baseline=%22central%22 text-anchor=%22middle%22 fill=%22white%22 font-family=%22sans-serif%22 font-weight=%22bold%22 font-size=%2250%22>TB</text></svg>">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "SoftwareApplication",
        "name": "{cfg['h1']}",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Web Browser",
        "url": "{canonical_url}",
        "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
        "publisher": {{ "@type": "Organization", "name": "Tech Boss", "url": "https://imtechboss.com/" }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://imtechboss.com/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Tools", "item": "https://imtechboss.com/tools/" }},
          {{ "@type": "ListItem", "position": 3, "name": "{cfg['h1']}", "item": "{canonical_url}" }}
        ]
      }}
    ]
  }}
  </script>
  <link rel="stylesheet" href="/css/styles.min.css?v=1.0">
  <script>
    try {{
      const savedTheme = localStorage.getItem("pulse_theme");
      const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      if (savedTheme === "dark" || (!savedTheme && systemDark)) document.documentElement.classList.add("dark");
    }} catch (e) {{}}
  </script>
</head>
<body class="bg-gray-50 dark:bg-slate-950 text-gray-900 dark:text-gray-100 min-h-screen flex flex-col justify-between font-sans transition-colors duration-200">
  <header class="border-b border-gray-200 dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 backdrop-blur sticky top-0 z-40">
    <div class="max-w-6xl mx-auto px-4 py-3.5 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2.5 group">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white font-extrabold text-base shadow-sm">TB</div>
        <div class="flex flex-col">
          <span class="text-base font-extrabold tracking-tight text-gray-950 dark:text-white">Tech Boss</span>
          <span class="text-[10px] font-semibold uppercase tracking-wider text-blue-600 dark:text-blue-400">Interactive Tools Suite</span>
        </div>
      </a>
      <nav class="flex items-center gap-2 sm:gap-4 text-xs font-semibold overflow-x-auto whitespace-nowrap">
        <a href="/" class="text-gray-600 dark:text-gray-300 hover:text-blue-600">Home</a>
        <a href="/tools/" class="text-blue-600 dark:text-blue-400 font-bold">All 17 Tools</a>
        <a href="/compare/" class="text-rose-600 dark:text-rose-400">Compare</a>
        <a href="/about/" class="hidden sm:inline text-gray-600 dark:text-gray-300">About</a>
        <a href="/contact/" class="hidden sm:inline text-gray-600 dark:text-gray-300">Contact</a>
        <button id="themeToggleBtn" class="p-2 rounded-full text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800" aria-label="Toggle Dark Mode">🌓</button>
      </nav>
    </div>
  </header>

  <main class="flex-grow max-w-4xl mx-auto px-4 py-8 sm:py-10 w-full">
    <nav class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mb-6" aria-label="Breadcrumb">
      <a href="/" class="hover:text-blue-600">Home</a><span>/</span>
      <a href="/tools/" class="hover:text-blue-600">Tools</a><span>/</span>
      <span class="text-gray-900 dark:text-gray-200 font-semibold truncate">{cfg['h1']}</span>
    </nav>

    <div class="mb-8">
      <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-[11px] font-bold uppercase tracking-wider mb-3">
        {cfg['icon']} {cfg['badge']}
      </span>
      <h1 class="text-2xl sm:text-4xl font-black text-gray-950 dark:text-white tracking-tight mb-3">{cfg['h1']}</h1>
      <div class="p-4 rounded-2xl bg-blue-50/70 dark:bg-blue-950/30 border border-blue-200/70 dark:border-blue-800/60 text-xs sm:text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
        <strong class="text-blue-800 dark:text-blue-300 font-bold block mb-1">⚡ {cfg['capsule_title']}</strong>
        {cfg['capsule_text']}
      </div>
    </div>

    <div class="mb-12">{cfg['tool_html']}</div>

    <section class="border-t border-gray-200 dark:border-slate-800 pt-8 mb-12">
      <h2 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-4">{cfg['guide_title']}</h2>
      {cfg['guide_html']}
    </section>

    <section class="border-t border-gray-200 dark:border-slate-800 pt-8 mb-8">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-bold text-base sm:text-lg text-gray-900 dark:text-white">Explore More Free Interactive Tools</h3>
        <a href="/tools/" class="text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline">View All 17 Tools &rarr;</a>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">{other_tools_html}</div>
    </section>
  </main>

  <footer class="border-t border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900 mt-12 py-8 text-xs text-gray-500 dark:text-gray-400">
    <div class="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div><span class="font-bold text-gray-800 dark:text-gray-200">Tech Boss</span> &bull; Free Engineering &amp; Nepal Tech Utilities</div>
      <div class="flex items-center gap-4">
        <a href="/tools/" class="hover:text-blue-600">All Tools</a>
        <a href="/about/" class="hover:text-blue-600">About</a>
        <a href="/privacy/" class="hover:text-blue-600">Privacy</a>
        <a href="/terms/" class="hover:text-blue-600">Terms</a>
        <a href="/contact/" class="hover:text-blue-600">Contact</a>
      </div>
    </div>
  </footer>

  <script>
    const tbThemeBtn = document.getElementById('themeToggleBtn');
    if (tbThemeBtn) tbThemeBtn.addEventListener('click', () => {{
      const isDark = document.documentElement.classList.toggle('dark');
      try {{ localStorage.setItem('pulse_theme', isDark ? 'dark' : 'light'); }} catch (e) {{}}
    }});
    {cfg['tool_js']}
  </script>
</body>
</html>
"""
        target_dir = os.path.join(root_dir, 'tools', slug)
        os.makedirs(target_dir, exist_ok=True)
        target_file = os.path.join(target_dir, 'index.html')
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(page_html)
        print(f"  ✅ Generated extended tool: /tools/{slug}/index.html ({len(page_html)} bytes)")
