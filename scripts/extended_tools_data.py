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
        "guide_title": "Electricity Bill Calculator Nepal Online: How to Calculate Units, Minimum Charge & Local GPU Cost",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">Running a 350W RTX desktop actively for 6 hours per day consumes 63 kWh (units) per month—roughly Rs. 660/month in Nepal or ~$10/month in the US. Compared to $20–$200/month cloud API bills, local LLMs quickly pay off when you already own a capable GPU.</p>
        <h3 class="text-base font-bold text-gray-900 dark:text-white mt-5 mb-2">How to Calculate Electricity Unit in Nepal (NEA Domestic Tariff &amp; Minimum Charge)</h3>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-4">In Nepal, <strong>1 Unit = 1 kWh (1,000 Watts running for 1 hour)</strong>. The formula is <code>(Watts × Hours per Day × 30) ÷ 1000</code>. Under Nepal Electricity Authority (NEA) domestic single-phase meters (5A, 15A, 30A, 60A), the minimum monthly charge starts from Rs. 30–Rs. 125 for basic slabs (up to 20 units free on 5A meters), while middle consumption slabs (31–250 units) average Rs. 8.00 to Rs. 11.00 per unit and high slabs above 250–400 units scale to Rs. 11.00–Rs. 12.00 per unit.</p>
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
              screen: "15.6-inch or 14-inch Full HD IPS (Reject washed-out TN panels)",
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
    {
        "slug": "nepal-land-area-converter",
        "icon": "📐",
        "badge": "Nepal Land & Cadastral Math",
        "h1": "Nepal Land Area Converter (Ropani-Aana & Bigha-Kattha)",
        "title": "Nepal Land Area Converter: Ropani-Aana-Paisa & Bigha-Kattha (2026) — Tech Boss",
        "description": "Convert Nepal land units accurately between Ropani-Aana-Paisa-Daam, Bigha-Kattha-Dhur, Square Feet, Square Meter, and estimate NPR land valuation.",
        "capsule_title": "Standard Nepal Survey Conversion",
        "capsule_text": "1 Ropani equals 16 Aana (5,476 sq. ft / 508.74 sq. m) and 1 Aana equals 4 Paisa (342.25 sq. ft). In the Terai system, 1 Bigha equals 20 Kattha (72,900 sq. ft) and 1 Kattha equals 20 Dhur (3,645 sq. ft). Enter any measurement below for instant conversion and NPR valuation.",
        "tool_html": """
        <section id="nepalLandTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Input Unit System</label>
              <select id="landInputMode" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="ropani" selected>Hill System (Ropani - Aana - Paisa - Daam)</option>
                <option value="bigha">Terai System (Bigha - Kattha - Dhur)</option>
                <option value="sqft">Square Feet (Sq. Ft)</option>
                <option value="sqm">Square Meter (Sq. m — Mero Kitta)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Optional Price per Aana or Kattha (NPR)</label>
              <input id="landRateNpr" type="number" min="0" step="10000" placeholder="e.g. 3500000 (Rs. 35 Lakh)" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm text-gray-900 dark:text-white" />
            </div>
          </div>

          <div id="landRopaniInputs" class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
            <div><label class="block text-[11px] font-bold text-gray-500 mb-1">Ropani</label><input id="inRopani" type="number" min="0" step="any" value="0" class="w-full px-3 py-2 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" /></div>
            <div><label class="block text-[11px] font-bold text-gray-500 mb-1">Aana</label><input id="inAana" type="number" min="0" step="any" value="4" class="w-full px-3 py-2 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" /></div>
            <div><label class="block text-[11px] font-bold text-gray-500 mb-1">Paisa</label><input id="inPaisa" type="number" min="0" step="any" value="0" class="w-full px-3 py-2 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" /></div>
            <div><label class="block text-[11px] font-bold text-gray-500 mb-1">Daam</label><input id="inDaam" type="number" min="0" step="any" value="0" class="w-full px-3 py-2 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" /></div>
          </div>

          <div id="landBighaInputs" class="hidden grid grid-cols-3 gap-3 mb-5">
            <div><label class="block text-[11px] font-bold text-gray-500 mb-1">Bigha</label><input id="inBigha" type="number" min="0" step="any" value="0" class="w-full px-3 py-2 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" /></div>
            <div><label class="block text-[11px] font-bold text-gray-500 mb-1">Kattha</label><input id="inKattha" type="number" min="0" step="any" value="1" class="w-full px-3 py-2 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" /></div>
            <div><label class="block text-[11px] font-bold text-gray-500 mb-1">Dhur</label><input id="inDhur" type="number" min="0" step="any" value="0" class="w-full px-3 py-2 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" /></div>
          </div>

          <div id="landFlatInput" class="hidden mb-5">
            <label id="landFlatLabel" class="block text-[11px] font-bold text-gray-500 mb-1">Area Value</label>
            <input id="inFlatArea" type="number" min="0" step="any" value="1369" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" />
          </div>

          <button id="calcNepalLandBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm shadow transition-colors">
            📐 Convert Land Area &amp; Calculate Valuation
          </button>
          <div id="nepalLandResultBox" class="hidden mt-6 p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const modeSel = document.getElementById('landInputMode');
          const ropDiv = document.getElementById('landRopaniInputs');
          const bigDiv = document.getElementById('landBighaInputs');
          const flatDiv = document.getElementById('landFlatInput');
          const flatLbl = document.getElementById('landFlatLabel');
          const btn = document.getElementById('calcNepalLandBtn');
          const box = document.getElementById('nepalLandResultBox');
          if (!modeSel || !btn || !box) return;

          const SQFT_PER_ROPANI = 5476;
          const SQFT_PER_AANA = 342.25;
          const SQFT_PER_PAISA = 85.5625;
          const SQFT_PER_DAAM = 21.390625;
          const SQFT_PER_BIGHA = 72900;
          const SQFT_PER_KATTHA = 3645;
          const SQFT_PER_DHUR = 182.25;
          const SQM_TO_SQFT = 10.7639104167;

          modeSel.addEventListener('change', () => {
            const m = modeSel.value;
            ropDiv.classList.toggle('hidden', m !== 'ropani');
            bigDiv.classList.toggle('hidden', m !== 'bigha');
            flatDiv.classList.toggle('hidden', m !== 'sqft' && m !== 'sqm');
            if (m === 'sqft') flatLbl.textContent = 'Area in Square Feet (Sq. Ft)';
            if (m === 'sqm') flatLbl.textContent = 'Area in Square Meters (Sq. m — Mero Kitta / Lalpurja)';
          });

          btn.addEventListener('click', () => {
            const m = modeSel.value;
            let sqft = 0;
            if (m === 'ropani') {
              const r = parseFloat(document.getElementById('inRopani').value) || 0;
              const a = parseFloat(document.getElementById('inAana').value) || 0;
              const p = parseFloat(document.getElementById('inPaisa').value) || 0;
              const d = parseFloat(document.getElementById('inDaam').value) || 0;
              sqft = r * SQFT_PER_ROPANI + a * SQFT_PER_AANA + p * SQFT_PER_PAISA + d * SQFT_PER_DAAM;
            } else if (m === 'bigha') {
              const b = parseFloat(document.getElementById('inBigha').value) || 0;
              const k = parseFloat(document.getElementById('inKattha').value) || 0;
              const dh = parseFloat(document.getElementById('inDhur').value) || 0;
              sqft = b * SQFT_PER_BIGHA + k * SQFT_PER_KATTHA + dh * SQFT_PER_DHUR;
            } else if (m === 'sqft') {
              sqft = parseFloat(document.getElementById('inFlatArea').value) || 0;
            } else {
              sqft = (parseFloat(document.getElementById('inFlatArea').value) || 0) * SQM_TO_SQFT;
            }

            const sqm = sqft / SQM_TO_SQFT;
            const totalAana = sqft / SQFT_PER_AANA;
            const totalKattha = sqft / SQFT_PER_KATTHA;

            // R-A-P-D breakdown
            let rem = sqft;
            const rop = Math.floor(rem / SQFT_PER_ROPANI); rem -= rop * SQFT_PER_ROPANI;
            const aan = Math.floor(rem / SQFT_PER_AANA); rem -= aan * SQFT_PER_AANA;
            const pai = Math.floor(rem / SQFT_PER_PAISA); rem -= pai * SQFT_PER_PAISA;
            const daa = (rem / SQFT_PER_DAAM).toFixed(2);

            // B-K-D breakdown
            let remB = sqft;
            const big = Math.floor(remB / SQFT_PER_BIGHA); remB -= big * SQFT_PER_BIGHA;
            const kat = Math.floor(remB / SQFT_PER_KATTHA); remB -= kat * SQFT_PER_KATTHA;
            const dhu = (remB / SQFT_PER_DHUR).toFixed(2);

            const rate = parseFloat(document.getElementById('landRateNpr').value) || 0;
            let valHtml = '';
            if (rate > 0) {
              const units = m === 'bigha' ? totalKattha : totalAana;
              const unitName = m === 'bigha' ? 'Kattha' : 'Aana';
              const totalNpr = Math.round(units * rate);
              const crores = (totalNpr / 10000000).toFixed(2);
              const lakhs = (totalNpr / 100000).toFixed(2);
              valHtml = `<div class="mt-3 p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-xs text-emerald-800 dark:text-emerald-300"><strong>Estimated Valuation (@ Rs. ${rate.toLocaleString()} / ${unitName}):</strong> Rs. ${totalNpr.toLocaleString()} (~Rs. ${lakhs} Lakh / Rs. ${crores} Crore)</div>`;
            }

            box.innerHTML = `
              <h3 class="text-base font-extrabold text-emerald-700 dark:text-emerald-400 mb-3">Exact Nepal Cadastral Conversion</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs mb-3">
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700">
                  <span class="text-gray-500 block">Hill System (R-A-P-D)</span>
                  <strong class="text-sm text-gray-900 dark:text-white">${rop} Ropani, ${aan} Aana, ${pai} Paisa, ${daa} Daam</strong>
                  <div class="text-[11px] text-gray-500 mt-1">Total: ${totalAana.toFixed(3)} Aana</div>
                </div>
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700">
                  <span class="text-gray-500 block">Terai System (B-K-D)</span>
                  <strong class="text-sm text-gray-900 dark:text-white">${big} Bigha, ${kat} Kattha, ${dhu} Dhur</strong>
                  <div class="text-[11px] text-gray-500 mt-1">Total: ${totalKattha.toFixed(3)} Kattha</div>
                </div>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
                <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Square Feet</span><strong>${sqft.toFixed(2)} sq.ft</strong></div>
                <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Square Meter</span><strong>${sqm.toFixed(2)} sq.m</strong></div>
                <div class="p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Hectare / Acre</span><strong>${(sqm/10000).toFixed(4)} ha</strong></div>
              </div>
              ${valHtml}
              <div class="mt-3 flex flex-wrap gap-4 text-xs">
                <a href="/mero-kitta-nagarik-app-driving-license-online-form-nepal-guide-2026/" class="font-bold text-blue-600 dark:text-blue-400 hover:underline">Check Mero Kitta Online Map Guide &rarr;</a>
                <a href="/land-solution-nepal-cadastral-calculator/" class="font-bold text-emerald-600 dark:text-emerald-400 hover:underline">Land Solution Cadastral Kitta-Kaat Software &rarr;</a>
              </div>
            `;
            box.classList.remove('hidden');
          });
        })();
        """,
        "guide_title": "Understanding Ropani-Aana vs Bigha-Kattha & Mero Kitta Sq. Meter Values",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-3">On official Nepali Lalpurja and <a href="/mero-kitta-nagarik-app-driving-license-online-form-nepal-guide-2026/" class="text-blue-600 underline font-semibold">Mero Kitta</a> records, land area is often stored in square meters (sq. m) or R-A-P-D / B-K-D notation. One Ropani equals 508.74 sq. m (5,476 sq. ft), while one Kattha equals 338.63 sq. m (3,645 sq. ft).</p>
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">For multi-parcel subdivision (Kitta Kaat) and irregular plot area geometry, explore <a href="/land-solution-nepal-cadastral-calculator/" class="text-blue-600 underline font-semibold">Land Solution Nepal Cadastral Software</a>.</p>
        """
    },
    {
        "slug": "nepal-salary-tax-ssf-calculator",
        "icon": "💰",
        "badge": "Nepal Income Tax & Payroll",
        "h1": "Nepal Salary Tax, SSF & 5% IT Export Calculator (FY 2082/83)",
        "title": "Nepal Salary Tax & SSF Calculator 2026 (Single/Married + 5% IT Tax) — Tech Boss",
        "description": "Calculate annual & monthly Nepal income tax (Single vs Married slabs), 1% SST, SSF/PF/CIT deductions, net take-home NPR salary, and 5% foreign IT export tax.",
        "capsule_title": "Nepal Tax Slabs & 5% IT Export Rule",
        "capsule_text": "Salaried individuals in Nepal pay 1% Social Security Tax (SST) on the first Rs. 5,00,000 (Single) or Rs. 6,00,000 (Married), followed by progressive 10%, 20%, 30%, 36%, and 39% slabs. Registered SSF contributors are exempt from the 1% SST on the base slab. Foreign software/IT export remittances remain eligible for 5% final withholding tax.",
        "tool_html": """
        <section id="nepalTaxTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Monthly Gross Salary (NPR)</label>
              <input id="taxMonthlySalary" type="number" min="0" step="1000" value="100000" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Annual Bonus / Festival Months</label>
              <select id="taxSalaryMonths" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="12">12 Months (No Dashain Bonus)</option>
                <option value="13" selected>13 Months (Incl. 1-Month Dashain Bonus)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Assessment Status</label>
              <select id="taxMaritalStatus" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="single" selected>Single (Unmarried — Rs. 5L Base)</option>
                <option value="married">Couple / Married (Rs. 6L Base)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">SSF / PF Deduction</label>
              <select id="taxSsfMode" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="none">No SSF / PF (Standard 1% SST)</option>
                <option value="ssf" selected>Enrolled in SSF (11% Employee on 60% Basic, 0% SST)</option>
                <option value="pf10">EPF / CIT (10% Employee Deduction)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Annual Insurance Deduction (NPR)</label>
              <input id="taxInsurance" type="number" min="0" max="40000" step="1000" value="0" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Income Mode</label>
              <select id="taxIncomeType" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="local" selected>Domestic Nepal Payroll Salary</option>
                <option value="it_export">Remote Foreign IT Export (5% Final TDS)</option>
              </select>
            </div>
          </div>
          <button id="calcNepalTaxBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm shadow transition-colors">
            💰 Calculate Annual &amp; Monthly Nepal Tax
          </button>
          <div id="nepalTaxResultBox" class="hidden mt-6 p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const btn = document.getElementById('calcNepalTaxBtn');
          const box = document.getElementById('nepalTaxResultBox');
          if (!btn || !box) return;

          btn.addEventListener('click', () => {
            const monthly = parseFloat(document.getElementById('taxMonthlySalary').value) || 0;
            const months = parseInt(document.getElementById('taxSalaryMonths').value, 10);
            const marital = document.getElementById('taxMaritalStatus').value;
            const ssfMode = document.getElementById('taxSsfMode').value;
            const ins = Math.min(40000, parseFloat(document.getElementById('taxInsurance').value) || 0);
            const incType = document.getElementById('taxIncomeType').value;

            const annualGross = monthly * months;
            if (incType === 'it_export') {
              const tax5 = Math.round(annualGross * 0.05);
              const netYear = annualGross - tax5;
              const netMonth = Math.round(netYear / 12);
              box.innerHTML = `
                <h3 class="text-base font-extrabold text-emerald-700 dark:text-emerald-400 mb-3">Foreign IT Service Export (5% Final Withholding Tax)</h3>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs mb-3">
                  <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Annual Gross</span><strong class="text-sm">Rs. ${Math.round(annualGross).toLocaleString()}</strong></div>
                  <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">5% Final IT Tax</span><strong class="text-sm text-rose-600">Rs. ${tax5.toLocaleString()}</strong></div>
                  <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Monthly Net Take-Home</span><strong class="text-sm text-emerald-600">Rs. ${netMonth.toLocaleString()}</strong></div>
                </div>
                <p class="text-xs text-gray-600 dark:text-gray-300 mb-2">Under Nepal's IT export tax rules, commercial banks deduct 5% final TDS upon receiving convertible foreign currency via SWIFT/Wise with clear software invoice remarks.</p>
                <a href="/nepali-developers-international-payments-wise-payoneer-swift-2026/" class="text-xs font-bold text-blue-600 hover:underline">Read Nepali Developer International Payments &amp; 5% Tax Guide &rarr;</a>
              `;
              box.classList.remove('hidden');
              return;
            }

            let annualFund = 0;
            if (ssfMode === 'ssf') annualFund = Math.round((monthly * 0.60) * 0.11 * 12);
            else if (ssfMode === 'pf10') annualFund = Math.round((monthly * 0.60) * 0.10 * 12);
            const fundDeductible = Math.min(annualFund, annualGross / 3, 500000);
            const taxable = Math.max(0, annualGross - fundDeductible - ins);

            const baseSlab = marital === 'married' ? 600000 : 500000;
            let rem = taxable;
            let tax = 0;
            const breakdown = [];

            const s1 = Math.min(rem, baseSlab);
            const r1 = ssfMode === 'ssf' ? 0 : 0.01;
            const t1 = s1 * r1;
            tax += t1; rem -= s1;
            breakdown.push(`Slab 1 (${(r1*100).toFixed(0)}% on Rs. ${Math.round(s1).toLocaleString()}): Rs. ${Math.round(t1).toLocaleString()}`);

            const brackets = [
              [200000, 0.10, '10%'],
              [300000, 0.20, '20%'],
              [1000000, 0.30, '30%'],
              [3000000, 0.36, '36%'],
              [Infinity, 0.39, '39%']
            ];
            for (const [cap, rate, lbl] of brackets) {
              if (rem <= 0) break;
              const chunk = Math.min(rem, cap);
              const t = chunk * rate;
              tax += t; rem -= chunk;
              breakdown.push(`${lbl} on Rs. ${Math.round(chunk).toLocaleString()}: Rs. ${Math.round(t).toLocaleString()}`);
            }

            const annualTax = Math.round(tax);
            const monthlyTax = Math.round(annualTax / 12);
            const monthlyFund = Math.round(annualFund / 12);
            const monthlyInHand = Math.round((annualGross - annualTax - annualFund) / months);

            box.innerHTML = `
              <h3 class="text-base font-extrabold text-blue-700 dark:text-blue-400 mb-3">Nepal Annual &amp; Monthly Payroll Tax Summary</h3>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs mb-3">
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Taxable Income</span><strong>Rs. ${Math.round(taxable).toLocaleString()}</strong></div>
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Annual Tax</span><strong class="text-rose-600">Rs. ${annualTax.toLocaleString()}</strong></div>
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Monthly TDS / Fund</span><strong>Rs. ${monthlyTax.toLocaleString()} / ${monthlyFund.toLocaleString()}</strong></div>
                <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Est. Monthly Net</span><strong class="text-emerald-600">Rs. ${monthlyInHand.toLocaleString()}</strong></div>
              </div>
              <ul class="text-xs text-gray-700 dark:text-gray-300 space-y-1 mb-3">${breakdown.map(b => `<li>• ${b}</li>`).join('')}</ul>
              <a href="/mero-kitta-nagarik-app-driving-license-online-form-nepal-guide-2026/" class="text-xs font-bold text-blue-600 hover:underline">Need a Personal PAN Card? Check Nagarik App PAN Guide &rarr;</a>
            `;
            box.classList.remove('hidden');
          });
        })();
        """,
        "guide_title": "How Nepal Salary Tax, SSF & 5% IT Export TDS Are Calculated",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-3">In Nepal, you must hold a Personal PAN number (easily generated via <a href="/mero-kitta-nagarik-app-driving-license-online-form-nepal-guide-2026/" class="text-blue-600 underline font-semibold">Nagarik App</a>) for employer TDS reconciliation or <a href="/nepali-developers-international-payments-wise-payoneer-swift-2026/" class="text-blue-600 underline font-semibold">5% IT Export tax</a> bank certificates.</p>
        """
    },
    {
        "slug": "nepal-govt-photo-document-compressor",
        "icon": "🪪",
        "badge": "Nepal Govt Form Image Resizer",
        "h1": "Nepal Govt Form Photo & Document Compressor (<100KB / <200KB)",
        "title": "Nepal Govt Form Photo & Document Size Compressor (<100KB / <200KB) — Tech Boss",
        "description": "Resize and compress passport photos, signatures, and citizenship scans below 100KB or 200KB locally in your browser for Loksewa, DoTM License, NID, e-Passport, and Mero Kitta.",
        "capsule_title": "100% Private Browser-Local Compression",
        "capsule_text": "Nepalese government portals (Loksewa, DoTM Driving License, NID, Mero Kitta, IRD PAN) reject image uploads above 100KB–200KB. This tool shrinks JPG dimensions and file size entirely inside your browser—your citizenship or passport photos never leave your device.",
        "tool_html": """
        <section id="nepalCompressTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Portal Preset Target</label>
              <select id="compPreset" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="100|1000" selected>IRD PAN / Mero Kitta / DoTM License (&lt; 100 KB)</option>
                <option value="200|1200">Loksewa Document Scan (&lt; 200 KB)</option>
                <option value="50|450">Loksewa / Exam Passport Photo (&lt; 50 KB, 450px)</option>
                <option value="30|350">Signature Scan (&lt; 30 KB, 350px)</option>
                <option value="300|1400">NID / e-Passport High-Clarity Scan (&lt; 300 KB)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Select Image (JPG / PNG / WebP)</label>
              <input id="compFileInput" type="file" accept="image/*" class="w-full px-3 py-2 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-xs text-gray-900 dark:text-white" />
            </div>
          </div>
          <button id="compRunBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow transition-colors">
            🪪 Compress Image Locally (Zero Upload)
          </button>
          <div id="nepalCompResultBox" class="hidden mt-6 p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const btn = document.getElementById('compRunBtn');
          const fileIn = document.getElementById('compFileInput');
          const preset = document.getElementById('compPreset');
          const box = document.getElementById('nepalCompResultBox');
          if (!btn || !fileIn || !box) return;

          btn.addEventListener('click', () => {
            const file = fileIn.files && fileIn.files[0];
            if (!file) {
              box.innerHTML = '<p class="text-xs font-bold text-rose-600">Please select an image file first.</p>';
              box.classList.remove('hidden');
              return;
            }
            const [maxKbStr, maxDimStr] = preset.value.split('|');
            const targetBytes = parseInt(maxKbStr, 10) * 1024;
            const maxDim = parseInt(maxDimStr, 10);

            const reader = new FileReader();
            reader.onload = (ev) => {
              const img = new Image();
              img.onload = () => {
                let w = img.width, h = img.height;
                if (w > maxDim || h > maxDim) {
                  const ratio = Math.min(maxDim / w, maxDim / h);
                  w = Math.round(w * ratio);
                  h = Math.round(h * ratio);
                }
                const canvas = document.createElement('canvas');
                canvas.width = w; canvas.height = h;
                const ctx = canvas.getContext('2d');
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, w, h);
                ctx.drawImage(img, 0, 0, w, h);

                let q = 0.90;
                let dataUrl = canvas.toDataURL('image/jpeg', q);
                const estBytes = (url) => Math.round((url.length - 'data:image/jpeg;base64,'.length) * 0.75);
                while (estBytes(dataUrl) > targetBytes && q > 0.15) {
                  q -= 0.07;
                  dataUrl = canvas.toDataURL('image/jpeg', q);
                }
                while (estBytes(dataUrl) > targetBytes && w > 240) {
                  w = Math.round(w * 0.8); h = Math.round(h * 0.8);
                  canvas.width = w; canvas.height = h;
                  ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, w, h);
                  ctx.drawImage(img, 0, 0, w, h);
                  dataUrl = canvas.toDataURL('image/jpeg', 0.65);
                }
                const finalKb = (estBytes(dataUrl) / 1024).toFixed(1);
                const origKb = (file.size / 1024).toFixed(1);
                const dlName = file.name.replace(/\\.[^.]+$/, '') + '-compressed.jpg';

                box.innerHTML = `
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
                    <div>
                      <h3 class="text-sm font-extrabold text-emerald-700 dark:text-emerald-400">Compressed Ready: ${finalKb} KB (from ${origKb} KB)</h3>
                      <p class="text-xs text-gray-500">Output: ${w} x ${h} px JPEG (100% processed in your browser)</p>
                    </div>
                    <a href="${dataUrl}" download="${dlName}" class="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold text-center">⬇ Download JPG (${finalKb} KB)</a>
                  </div>
                  <img src="${dataUrl}" alt="Compressed preview" class="max-h-48 rounded-xl border border-gray-200 dark:border-slate-700" />
                `;
                box.classList.remove('hidden');
              };
              img.src = ev.target.result;
            };
            reader.readAsDataURL(file);
          });
        })();
        """,
        "guide_title": "Recommended Image Limits for Nepalese Govt Online Portals",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">Most Nepal e-governance portals (Loksewa, DoTM Driving License, IRD PAN, NID, and e-Passport) enforce strict JPEG limits between 50KB and 200KB. Use the presets above and follow our <a href="/loksewa-online-application-form-payment-photo-size-fix-nepal-2026/" class="text-blue-600 underline font-semibold">Loksewa Online Form &amp; Upload Guide</a> or <a href="/mero-kitta-nagarik-app-driving-license-online-form-nepal-guide-2026/" class="text-blue-600 underline font-semibold">Mero Kitta &amp; Driving License Guide</a>.</p>
        """
    },
    {
        "slug": "preeti-to-unicode-nepali-converter",
        "icon": "अ",
        "badge": "Nepali Typography Utility",
        "h1": "Preeti to Unicode Nepali Converter (Instant & Offline)",
        "title": "Preeti to Unicode Nepali Converter Online (Free & Fast) — Tech Boss",
        "description": "Convert legacy Preeti font text into clean Nepali Unicode instantly in your browser for government portals, emails, websites, and social media.",
        "capsule_title": "Instant Preeti-to-Unicode Mapping",
        "capsule_text": "Paste legacy Preeti text on the left to convert it into standard UTF-8 Nepali Unicode (Devanagari) with proper इकार (ि) placement, half-consonants, and Nepali numerals (०-९). Works 100% offline with 1-click copy.",
        "tool_html": """
        <section id="preetiTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Preeti Text Input</label>
              <textarea id="preetiInput" rows="6" placeholder="e.g. g]kfn /fHo" class="w-full p-3.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm text-gray-900 dark:text-white"></textarea>
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Unicode Nepali Output</label>
              <textarea id="unicodeOutput" rows="6" readonly placeholder="नेपाल राज्य" class="w-full p-3.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm text-gray-900 dark:text-white"></textarea>
            </div>
          </div>
          <div class="flex flex-wrap gap-3">
            <button id="convertPreetiBtn" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs sm:text-sm">Convert to Unicode</button>
            <button id="copyUnicodeBtn" class="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs sm:text-sm">Copy Unicode</button>
            <button id="clearPreetiBtn" class="px-4 py-2.5 rounded-xl bg-gray-200 dark:bg-slate-800 text-gray-700 dark:text-gray-300 font-bold text-xs sm:text-sm">Clear</button>
          </div>
          <p id="preetiStatus" class="hidden mt-3 text-xs font-bold text-emerald-600"></p>
        </section>
        """,
        "tool_js": """
        (function() {
          const inp = document.getElementById('preetiInput');
          const out = document.getElementById('unicodeOutput');
          const btn = document.getElementById('convertPreetiBtn');
          const copyBtn = document.getElementById('copyUnicodeBtn');
          const clrBtn = document.getElementById('clearPreetiBtn');
          const status = document.getElementById('preetiStatus');
          if (!inp || !out || !btn) return;

          const map = {
            'c':'अ','cf':'आ','O':'इ','O{':'ई','p':'उ','pm':'ऊ','C':'ऋ','P':'ए','P]':'ऐ','cf]':'ओ','cf}':'औ',
            's':'क','v':'ख','u':'ग','3':'घ','ª':'ङ','r':'च','5':'छ','h':'ज','´':'झ','`':'ञ',
            '6':'ट','7':'ठ','8':'ड','9':'ढ','0f':'ण','t':'त','y':'थ','b':'द','w':'ध','g':'न',
            'k':'प','km':'फ','a':'ब','e':'भ','d':'म','o':'य','/':'र','n':'ल','j':'व',
            'z':'श','if':'ष',';':'स','x':'ह','q':'त्र','1':'ज्ञ','If':'क्ष','M':'ः','+':'ं',
            'f':'ा','l':'ि','L':'ी','\'':'ु','"':'ू','[':'ृ',']':'े','}':'ै','f]':'ो','f}':'ौ',
            '\\':'्','F':'ँ','S':'क्','V':'ख्','U':'ग','R':'च्','H':'ज्',
            'T':'त्','Y':'थ्','W':'ध्','G':'न्','K':'प्','A':'ब्','E':'भ्','D':'म्','N':'ल्','J':'व्','Z':'श्',
            '!':'१','@':'२','#':'३','$':'४','%':'५','^':'६','&':'७','*':'८','(':'९',')':'०',
            '.':'।',',':',','?':'?'
          };
          const multiKeys = ['cf]','cf}','O{','P]','0f','km','If','if','f]','f}'];

          function convert(text) {
            let res = '';
            let i = 0;
            while (i < text.length) {
              let matched = false;
              for (const k of multiKeys) {
                if (text.startsWith(k, i)) { res += map[k]; i += k.length; matched = true; break; }
              }
              if (!matched) {
                const ch = text[i];
                if (ch === 'l' && i + 1 < text.length) {
                  // Pre-base i-matra: move after next consonant
                  let next = text[i + 1];
                  let mappedNext = map[next] || next;
                  res += mappedNext + 'ि';
                  i += 2;
                } else {
                  res += (map[ch] !== undefined ? map[ch] : ch);
                  i++;
                }
              }
            }
            return res.replace(/([क-ह])्([ािीुूृेैोौ])/g, '$1$2');
          }

          btn.addEventListener('click', () => { out.value = convert(inp.value); });
          inp.addEventListener('input', () => { out.value = convert(inp.value); });
          copyBtn.addEventListener('click', () => {
            if (!out.value) return;
            navigator.clipboard.writeText(out.value).then(() => {
              status.textContent = 'Copied Nepali Unicode to clipboard!';
              status.classList.remove('hidden');
              setTimeout(() => status.classList.add('hidden'), 2000);
            });
          });
          clrBtn.addEventListener('click', () => { inp.value = ''; out.value = ''; });
        })();
        """,
        "guide_title": "Why Unicode Is Required on Modern Nepal Websites & Govt Forms",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">Legacy Preeti typing only displays correctly on computers with the Preeti TTF font installed. Modern portals like Nagarik App, Mero Kitta, Loksewa, and Google Search require standard UTF-8 Devanagari Unicode.</p>
        """
    },
    {
        "slug": "nepal-emi-loan-sip-calculator",
        "icon": "🏦",
        "badge": "Nepal Banking & SIP Planner",
        "h1": "Nepal Bank Loan EMI & SIP Calculator (NPR)",
        "title": "Nepal Home/Auto Loan EMI & SIP Compound Calculator (NPR) — Tech Boss",
        "description": "Calculate monthly bank loan EMI, total interest in NPR for Nepal home/auto/education loans, or project long-term SIP mutual fund returns.",
        "capsule_title": "Nepal Bank EMI & SIP Compounding Math",
        "capsule_text": "Compare reducing-balance bank loan EMIs (NPR) at current Nepalese commercial bank interest rates (8%–14%) or calculate monthly SIP compounding returns before committing to a loan or mutual fund plan.",
        "tool_html": """
        <section id="nepalEmiTool" class="tool-section max-w-4xl mx-auto bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-gray-200 dark:border-slate-800 shadow-sm">
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-5">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Mode</label>
              <select id="emiMode" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-semibold text-gray-900 dark:text-white">
                <option value="emi" selected>Bank Loan EMI (NPR)</option>
                <option value="sip">Monthly SIP Wealth (NPR)</option>
              </select>
            </div>
            <div>
              <label id="emiAmountLabel" class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Loan Principal (NPR)</label>
              <input id="emiPrincipal" type="number" min="1000" step="10000" value="2500000" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Annual Interest / Return (%)</label>
              <input id="emiRate" type="number" min="1" max="40" step="0.1" value="10.5" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-600 dark:text-gray-400 mb-2">Tenure (Years)</label>
              <input id="emiYears" type="number" min="1" max="40" step="1" value="10" class="w-full px-3.5 py-2.5 rounded-xl bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 text-sm font-bold text-gray-900 dark:text-white" />
            </div>
          </div>
          <button id="calcEmiBtn" class="w-full sm:w-auto px-6 py-3 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-sm shadow transition-colors">
            🏦 Calculate EMI / SIP Breakdown
          </button>
          <div id="nepalEmiResultBox" class="hidden mt-6 p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/80 border border-gray-200 dark:border-slate-700"></div>
        </section>
        """,
        "tool_js": """
        (function() {
          const modeSel = document.getElementById('emiMode');
          const lbl = document.getElementById('emiAmountLabel');
          const prinIn = document.getElementById('emiPrincipal');
          const btn = document.getElementById('calcEmiBtn');
          const box = document.getElementById('nepalEmiResultBox');
          if (!modeSel || !btn || !box) return;

          modeSel.addEventListener('change', () => {
            if (modeSel.value === 'sip') {
              lbl.textContent = 'Monthly SIP Deposit (NPR)';
              prinIn.value = '10000';
            } else {
              lbl.textContent = 'Loan Principal (NPR)';
              prinIn.value = '2500000';
            }
          });

          btn.addEventListener('click', () => {
            const m = modeSel.value;
            const P = parseFloat(prinIn.value) || 0;
            const rAnn = parseFloat(document.getElementById('emiRate').value) || 0;
            const yrs = parseFloat(document.getElementById('emiYears').value) || 1;
            const n = Math.round(yrs * 12);
            const r = (rAnn / 100) / 12;

            if (m === 'emi') {
              const emi = r > 0 ? (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1) : P / n;
              const totalPay = emi * n;
              const totalInt = totalPay - P;
              box.innerHTML = `
                <h3 class="text-base font-extrabold text-amber-700 dark:text-amber-400 mb-3">Nepal Bank Loan EMI Breakdown (${yrs} Years @ ${rAnn}%)</h3>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                  <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Monthly EMI</span><strong class="text-lg text-blue-600">Rs. ${Math.round(emi).toLocaleString()}</strong></div>
                  <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Total Interest</span><strong class="text-lg text-rose-600">Rs. ${Math.round(totalInt).toLocaleString()}</strong></div>
                  <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Total Repayment</span><strong class="text-lg text-gray-900 dark:text-white">Rs. ${Math.round(totalPay).toLocaleString()}</strong></div>
                </div>
              `;
            } else {
              const fv = r > 0 ? P * ((Math.pow(1 + r, n) - 1) / r) * (1 + r) : P * n;
              const invested = P * n;
              const gain = fv - invested;
              box.innerHTML = `
                <h3 class="text-base font-extrabold text-emerald-700 dark:text-emerald-400 mb-3">Nepal SIP Wealth Projection (${yrs} Years @ ${rAnn}%)</h3>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                  <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Total Invested</span><strong class="text-lg">Rs. ${Math.round(invested).toLocaleString()}</strong></div>
                  <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Estimated Gain</span><strong class="text-lg text-emerald-600">Rs. ${Math.round(gain).toLocaleString()}</strong></div>
                  <div class="p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700"><span class="text-gray-500 block">Projected Value</span><strong class="text-lg text-blue-600">Rs. ${Math.round(fv).toLocaleString()}</strong></div>
                </div>
              `;
            }
            box.classList.remove('hidden');
          });
        })();
        """,
        "guide_title": "Evaluating Nepal Base Rates, Reducing Balance EMIs & SIP Compounding",
        "guide_html": """
        <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">Nepalese commercial banks price home, auto, and education loans using Bank Base Rate + Premium under a reducing-balance schedule. Compare loan interest costs against long-term <a href="/meroshare-c-asba-demat-ipo-apply-nepal-error-fix-guide-2026/" class="text-blue-600 underline font-semibold">Meroshare / NEPSE SIP returns</a> before locking long tenures.</p>
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
        <a href="/tools/" class="text-blue-600 dark:text-blue-400 font-bold">All 22 Tools</a>
        <a href="/nepal/" class="text-emerald-600 dark:text-emerald-400 font-bold">Nepal Hub</a>
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
        <a href="/tools/" class="text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline">View All 22 Tools &rarr;</a>
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
