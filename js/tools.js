
    // Theme Management
    const themeBtn = document.getElementById("themeToggleBtn");
    const sunIcon = document.getElementById("sunIcon");
    const moonIcon = document.getElementById("moonIcon");

    function syncThemeIcons() {
      const isDark = document.documentElement.classList.contains("dark");
      if (isDark) {
        sunIcon.classList.remove("hidden");
        moonIcon.classList.add("hidden");
      } else {
        sunIcon.classList.add("hidden");
        moonIcon.classList.remove("hidden");
      }
    }
    syncThemeIcons();

    if (themeBtn) {
      themeBtn.addEventListener("click", () => {
        const isDark = document.documentElement.classList.toggle("dark");
        try { localStorage.setItem("pulse_theme", isDark ? "dark" : "light"); } catch (e) {}
        syncThemeIcons();
        showToast(isDark ? "Dark mode activated" : "Light mode activated");
      });
    }

    function showToast(msg) {
      const c = document.getElementById("toastContainer");
      if (!c) return;
      const t = document.createElement("div");
      t.className = "px-4 py-2.5 rounded-xl bg-slate-900 text-white text-xs font-semibold shadow-lg transition-all transform translate-y-2 opacity-0 pointer-events-auto border border-slate-800";
      t.textContent = msg;
      c.appendChild(t);
      setTimeout(() => { t.classList.remove("translate-y-2", "opacity-0"); }, 10);
      setTimeout(() => {
        t.classList.add("opacity-0", "translate-y-2");
        setTimeout(() => t.remove(), 300);
      }, 3000);
    }

    // Tabs switching
    function activateTab(targetId) {
      const btn = document.querySelector(`.tool-tab-btn[data-target="${targetId}"]`);
      if (btn) {
        document.querySelectorAll(".tool-tab-btn").forEach(b => {
          b.classList.remove("bg-blue-600", "text-white", "shadow", "active");
          b.classList.add("bg-white", "dark:bg-slate-900", "border", "border-gray-200", "dark:border-slate-800", "text-gray-700", "dark:text-gray-300");
        });
        btn.classList.add("bg-blue-600", "text-white", "shadow", "active");
        btn.classList.remove("bg-white", "dark:bg-slate-900", "border", "border-gray-200", "dark:border-slate-800", "text-gray-700", "dark:text-gray-300");

        document.querySelectorAll(".tool-section").forEach(sec => sec.classList.add("hidden"));
        const targetSec = document.getElementById(targetId);
        if (targetSec) targetSec.classList.remove("hidden");
      }
    }

    document.querySelectorAll(".tool-tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-target");
        activateTab(targetId);
      });
    });

    // Deep-linking via query string (?tool=vram) or hash (#aiVramTool)
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const toolParam = (urlParams.get("tool") || "").toLowerCase();
      const hash = window.location.hash.replace("#", "").toLowerCase();
      if (toolParam.includes("vram") || hash.includes("vram") || hash.includes("aivram")) {
        activateTab("aiVramTool");
      } else if (toolParam.includes("gpu") || hash.includes("gpu")) {
        activateTab("gpuMatcherTool");
      } else if (toolParam.includes("game") || hash.includes("game")) {
        activateTab("gameCheckerTool");
      } else if (toolParam.includes("prompt") || hash.includes("prompt")) {
        activateTab("promptTool");
      } else if (toolParam.includes("cheat") || hash.includes("cheat")) {
        activateTab("cheatsheetTool");
      } else if (toolParam.includes("bottleneck") || hash.includes("bottleneck")) {
        activateTab("bottleneckTool");
      }
    } catch (e) {}

    // 1. Bottleneck Calculator Logic
    const calcBtn = document.getElementById("calcBottleneckBtn");
    if (calcBtn) {
      if (calcBtn) calcBtn.addEventListener("click", () => {
        const bRes = document.getElementById("bottleneckResult"); if (bRes) bRes.classList.remove("hidden");
        const cpuScore = parseInt(document.getElementById("cpuSelect").value, 10);
        const gpuScore = parseInt(document.getElementById("gpuSelect").value, 10);
        const res = parseInt(document.getElementById("resSelect").value, 10);

        // Resolution weights: 1080p is CPU bound (weight 1.3), 1440p balanced (1.0), 4K GPU bound (0.7)
        let weight = 1.0;
        if (res === 1080) weight = 1.25;
        if (res === 2160) weight = 0.72;

        const effectiveCpu = cpuScore * (1 / weight);
        const diff = Math.abs(effectiveCpu - gpuScore);
        const maxScore = Math.max(effectiveCpu, gpuScore);
        const rawPct = Math.min(65, Math.max(2, (diff / maxScore) * 60));
        const pctFormatted = rawPct.toFixed(1) + "%";

        const pctEl = document.getElementById("bottleneckPct");
        const statusEl = document.getElementById("bottleneckStatus");
        const analysisEl = document.getElementById("bottleneckAnalysis");
        const tierEl = document.getElementById("gamingTier");
        const tipEl = document.getElementById("bottleneckTip");

        pctEl.textContent = pctFormatted;

        if (rawPct < 8) {
          pctEl.className = "text-3xl sm:text-4xl font-black text-emerald-600 dark:text-emerald-400";
          statusEl.className = "text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300";
          statusEl.textContent = "Optimal Match (No bottleneck)";
          analysisEl.textContent = `Your processor and graphics card operate in near-perfect equilibrium at this resolution. Both units achieve 97-100% theoretical utilization in modern gaming titles without frame pacing hitches.`;
          tierEl.textContent = res === 2160 ? "Enthusiast 4K Ultra 120Hz+" : "Elite 1440p Competitive High-FPS";
          tipEl.textContent = "Pro Tip: Pair this hardware with a high-bandwidth PCIe Gen 4/5 NVMe SSD to reduce DirectStorage asset decompression delays.";
        } else if (effectiveCpu < gpuScore) {
          // CPU bottleneck
          pctEl.className = "text-3xl sm:text-4xl font-black text-amber-500 dark:text-amber-400";
          statusEl.className = "text-xs font-bold px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300";
          statusEl.textContent = "Processor Bottleneck Detected";
          analysisEl.textContent = `Your GPU is significantly faster than your CPU at this resolution. In CPU-heavy titles (e.g., Cyberpunk 2077, Microsoft Flight Simulator), your graphics card will sit at partial load waiting for instructions.`;
          tierEl.textContent = "Mid-High Tier (GPU Underutilized)";
          tipEl.textContent = "Pro Tip: Increasing resolution scale to 1440p or 4K with DSR/VSR will shift processing weight back to your GPU, yielding crisper visuals at nearly identical frame rates.";
        } else {
          // GPU bottleneck
          pctEl.className = "text-3xl sm:text-4xl font-black text-blue-500 dark:text-blue-400";
          statusEl.className = "text-xs font-bold px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900/60 dark:text-blue-300";
          statusEl.textContent = "GPU Limited (Standard for Gaming)";
          analysisEl.textContent = `Your CPU easily feeds your graphics card with frames to spare. This is the optimal configuration for gaming since running GPUs at 99-100% capacity produces consistent frame delivery.`;
          tierEl.textContent = "GPU-Bound Solid Performance";
          tipEl.textContent = "Pro Tip: Use DLSS, FSR 3.1, or XeSS Quality scaling to recover 30-40% extra FPS without sacrificing visual fidelity.";
        }

        showToast("Calculated hardware bottleneck analysis!");
      });
    }

    // 2. AI Prompt Generator Logic
    const genPromptBtn = document.getElementById("generatePromptBtn");
    const copyPromptBtn = document.getElementById("copyPromptBtn");
    const rawInput = document.getElementById("rawPromptInput");
    const promptOutput = document.getElementById("promptOutput");

    if (genPromptBtn) {
      if (genPromptBtn) genPromptBtn.addEventListener("click", () => {
        const topic = (rawInput.value || "Build a responsive web application dashboard").trim();
        const model = document.getElementById("promptModel").value;
        const goal = document.getElementById("promptGoal").value;
        const tone = document.getElementById("promptTone").value;

        const structured = 
`[SYSTEM CONTEXT & ROLE]
You are a world-class ${tone}. Your analysis and implementation must adhere strictly to modern engineering standards, maintain zero filler, and avoid superficial clichés.

[OBJECTIVE]
${goal}: "${topic}"

[CONSTRAINTS & EXECUTION DIRECTIVES]
1. Target Architecture: Optimized specifically for ${model} capabilities.
2. Code & Design: Provide end-to-end executable implementations, robust error boundaries, and production-tested patterns.
3. Clarity: Structure responses with explicit markdown sections, step-by-step logic, and measurable benchmark criteria.
4. Tone Guardrails: Be direct, authoritative, and concise. Never use generic buzzwords.

[DELIVERABLE SPECIFICATION]
Provide:
1. Executive architectural summary.
2. Complete, copy-pasteable implementation with clear parameter annotations.
3. Edge-case handling and security considerations.`;

        promptOutput.textContent = structured;
        showToast("✨ Structured prompt generated successfully!");
      });
    }

    if (copyPromptBtn) {
      if (copyPromptBtn) copyPromptBtn.addEventListener("click", () => {
        const text = promptOutput.textContent;
        navigator.clipboard.writeText(text).then(() => {
          showToast("📋 Prompt copied to clipboard!");
        }).catch(() => {
          showToast("Failed to copy automatically.");
        });
      });
    }

    // 3. Command Cheat Sheets Logic
    const cheatData = [
      { cat: 'linux', cmd: 'journalctl -xeu service-name', desc: 'Inspect real-time logs for a specific systemd daemon service' },
      { cat: 'linux', cmd: 'sudo lsof -i :8080', desc: 'Identify which process is actively binding or listening on port 8080' },
      { cat: 'linux', cmd: 'htop', desc: 'Interactive real-time process manager, thread monitor, and resource analyzer' },
      { cat: 'linux', cmd: 'sudo chown -R $USER:$USER /var/www', desc: 'Recursively transfer directory ownership to current user' },
      { cat: 'linux', cmd: 'tar -czvf backup.tar.gz /target/folder', desc: 'Compress target directory into an encrypted gzip archive' },
      { cat: 'git', cmd: 'git commit --amend --no-edit', desc: 'Add staged changes into the most recent commit without modifying message' },
      { cat: 'git', cmd: 'git stash push -m "WIP feature"', desc: 'Safely stash working directory changes with a descriptive label' },
      { cat: 'git', cmd: 'git stash pop', desc: 'Re-apply the most recently stashed changes and remove them from stash list' },
      { cat: 'git', cmd: 'git reset --soft HEAD~1', desc: 'Undo the last commit while keeping all modified files safely staged' },
      { cat: 'git', cmd: 'git clean -fd', desc: 'Force remove all untracked files and directories from the repository' },
      { cat: 'docker', cmd: 'docker system prune -af --volumes', desc: 'Reclaim storage by removing all unused containers, images, and volumes' },
      { cat: 'docker', cmd: 'docker compose up -d --build', desc: 'Rebuild container images and launch multi-service stack in background' },
      { cat: 'docker', cmd: 'docker exec -it container_name /bin/bash', desc: 'Open an interactive terminal shell inside a live running container' },
      { cat: 'docker', cmd: 'docker logs -f --tail 100 container_name', desc: 'Stream live container stdout/stderr output tracking the last 100 lines' }
    ];

    const cheatList = document.getElementById("cheatList");
    const cheatSearch = document.getElementById("cheatSearchInput");
    let activeCheatCat = 'all';

    function renderCheats() {
      if (!cheatList) return;
      const q = (cheatSearch ? cheatSearch.value : '').toLowerCase().trim();

      const filtered = cheatData.filter(item => {
        const matchesCat = activeCheatCat === 'all' || item.cat === activeCheatCat;
        const matchesSearch = !q || item.cmd.toLowerCase().includes(q) || item.desc.toLowerCase().includes(q);
        return matchesCat && matchesSearch;
      });

      if (filtered.length === 0) {
        cheatList.innerHTML = `<div class="p-8 text-center text-xs text-gray-500">No commands match your filter.</div>`;
        return;
      }

      cheatList.innerHTML = filtered.map(item => `
        <div class="p-3.5 sm:p-4 rounded-2xl bg-gray-50 dark:bg-slate-800/60 border border-gray-200/80 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 group hover:border-blue-500/50 transition-colors">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${item.cat === 'linux' ? 'bg-orange-100 text-orange-700 dark:bg-orange-950/60 dark:text-orange-300' : (item.cat === 'git' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/60 dark:text-blue-300' : 'bg-cyan-100 text-cyan-700 dark:bg-cyan-950/60 dark:text-cyan-300')}">
                ${item.cat}
              </span>
              <p class="text-xs text-gray-600 dark:text-gray-300 truncate">${item.desc}</p>
            </div>
            <code class="text-xs sm:text-sm font-mono font-bold text-gray-950 dark:text-gray-100 select-all block bg-white dark:bg-slate-900 px-3 py-1.5 rounded-lg border border-gray-200/60 dark:border-slate-700">
              ${item.cmd}
            </code>
          </div>
          <button 
            data-cmd="${item.cmd.replace(/"/g, '&quot;')}"
            class="cheat-copy-btn px-3.5 py-1.5 rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 hover:bg-gray-100 dark:hover:bg-slate-800 text-xs font-bold text-blue-600 dark:text-blue-400 transition-colors flex-shrink-0 self-start sm:self-center shadow-xs"
          >
            Copy
          </button>
        </div>
      `).join("");
    }

    if (cheatList) {
      if (cheatList) cheatList.addEventListener('click', (e) => {
        const btn = e.target.closest('.cheat-copy-btn');
        if (btn) {
          const cmd = btn.getAttribute('data-cmd');
          if (cmd && navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
            navigator.clipboard.writeText(cmd).then(() => showToast('📋 Command copied to clipboard!'));
          }
        }
      });
    }

    renderCheats();

    if (cheatSearch) {
      if (cheatSearch) cheatSearch.addEventListener("input", renderCheats);
    }

    document.querySelectorAll(".cheat-cat-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".cheat-cat-btn").forEach(b => {
          b.classList.remove("bg-blue-600", "text-white", "active");
          b.classList.add("bg-gray-100", "dark:bg-slate-800", "text-gray-700", "dark:text-gray-300");
        });
        btn.classList.add("bg-blue-600", "text-white", "active");
        btn.classList.remove("bg-gray-100", "dark:bg-slate-800", "text-gray-700", "dark:text-gray-300");
        activeCheatCat = btn.getAttribute("data-cat");
        renderCheats();
      });
    });

    // 4. GPU Matcher Logic
    const findGpuBtn = document.getElementById("findGpuBtn");
    if (findGpuBtn) {
      if (findGpuBtn) findGpuBtn.addEventListener("click", () => {
        const qRes = document.getElementById("quizResultBox"); if (qRes) qRes.classList.remove("hidden");
        const budget = document.getElementById("quizBudget").value;
        const workload = document.getElementById("quizWorkload").value;
        const res = document.getElementById("quizResolution").value;

        let gpu = "NVIDIA GeForce RTX 4070 Super (12GB)";
        let cpu = "AMD Ryzen 7 7800X3D or Intel Core i5 14600K";
        let psu = "650W – 750W Gold";
        let fps = "110–140 FPS on 1440p Ultra Settings";
        let rationale = "Outstanding balanced choice for 1440p high-refresh gaming with full DLSS 3.5 support.";

        if (budget === "enthusiast" || (budget === "high" && workload === "ai") || res === "4k") {
          if (budget === "enthusiast" || workload === "ai") {
            gpu = "NVIDIA GeForce RTX 5090 (32GB) or RTX 4090 (24GB)";
            cpu = "AMD Ryzen 7 9800X3D or Ryzen 9 9950X";
            psu = "1000W – 1200W ATX 3.1 PCIe 5.1";
            fps = "144+ FPS in 4K Native Ultra / Path Tracing";
            rationale = "The ultimate workstation and gaming GPU. 24GB–32GB VRAM allows native execution of 70B quantized DeepSeek LLMs and unrestricted 4K path-traced rendering.";
          } else {
            gpu = "NVIDIA GeForce RTX 5080 (16GB) or RTX 4080 Super";
            cpu = "AMD Ryzen 7 9800X3D or Intel Core i7 14700K";
            psu = "850W Gold";
            fps = "100–120 FPS in 4K Ultra Settings";
            rationale = "High-efficiency 4K gaming powerhouse with next-gen GDDR7 memory bandwidth.";
          }
        } else if (budget === "high") {
          gpu = "NVIDIA GeForce RTX 4070 Ti Super (16GB) / AMD Radeon RX 7900 XT";
          cpu = "AMD Ryzen 7 7800X3D";
          psu = "750W – 850W Gold";
          fps = "120–160 FPS on 1440p / 75+ FPS on 4K";
          rationale = "The 16GB VRAM buffer ensures maximum longevity against memory-heavy console ports.";
        } else if (budget === "budget") {
          gpu = "NVIDIA GeForce RTX 4060 (8GB) or AMD Radeon RX 7600 XT (16GB)";
          cpu = "AMD Ryzen 5 7600 or Intel Core i5 12400F";
          psu = "550W – 650W Bronze";
          fps = "140–200+ FPS on 1080p Esports / 60–80 FPS 1080p AAA";
          rationale = "Exceptional power efficiency running under 130W, perfect for high-refresh 1080p esports and budget-friendly builds.";
        }

        document.getElementById("matchedGpuTitle").textContent = gpu;
        document.getElementById("matchedCpu").textContent = cpu;
        document.getElementById("matchedPsu").textContent = psu;
        document.getElementById("matchedFps").textContent = fps;
        document.getElementById("matchedRationale").textContent = rationale;

        showToast("🎯 Perfect hardware match found!");
      });
    }

    // 5. Can My PC Run It Checker Logic
    const canRunBtn = document.getElementById("checkCanRunBtn");
    if (canRunBtn) {
      if (canRunBtn) canRunBtn.addEventListener("click", () => {
        const gRes = document.getElementById("gameCheckResult"); if (gRes) gRes.classList.remove("hidden");
        const game = document.getElementById("gameSelect").value;
        const gpuVal = parseInt(document.getElementById("gameGpuSelect").value, 10);
        const cpuVal = parseInt(document.getElementById("gameCpuSelect").value, 10);
        const ramVal = parseInt(document.getElementById("gameRamSelect").value, 10);

        let composite = Math.round((gpuVal * 0.6) + (cpuVal * 0.3) + ((ramVal / 32) * 10));

        let tierTitle = "✨ Recommended Ultra Spec";
        let tierColor = "text-emerald-600 dark:text-emerald-400";
        let fps1080 = "120+ FPS Ultra";
        let fps1440 = "85–105 FPS High";
        let fps4k = "55–65 FPS (DLSS)";
        let tip = "Enable DLSS Quality or FSR 3.1 to maintain smooth frame times.";

        if (composite >= 85) {
          tierTitle = "👑 Enthusiast 4K Max Settings Ready";
          tierColor = "text-purple-600 dark:text-purple-400";
          fps1080 = "165+ FPS Ultra Max";
          fps1440 = "120–144+ FPS High";
          fps4k = "75–90+ FPS Full RT";
          tip = "Your rig exceeds standard targets. You can safely max out Full Path Tracing and Ray Reconstruction.";
        } else if (composite >= 65) {
          tierTitle = "✨ Recommended High-FPS Spec";
          tierColor = "text-emerald-600 dark:text-emerald-400";
          fps1080 = "110–130 FPS High";
          fps1440 = "75–90 FPS High";
          fps4k = "45–55 FPS Balanced";
          tip = "Ideal balance for 1440p gaming. Keep textures on High and utilize DLSS/FSR for high refresh rates.";
        } else if (composite >= 40) {
          tierTitle = "⚡ Minimum 1080p Playable Spec";
          tierColor = "text-amber-500 dark:text-amber-400";
          fps1080 = "50–65 FPS Medium";
          fps1440 = "35–45 FPS Low";
          fps4k = "20–30 FPS (Not Recommended)";
          tip = "Lower Volumetric Fog, Shadow Quality, and Crowd Density to maintain a stable 60 FPS floor.";
        } else {
          tierTitle = "⚠️ Below Recommended Specifications";
          tierColor = "text-red-500";
          fps1080 = "25–35 FPS Low (Stuttering)";
          fps1440 = "Unplayable (< 25 FPS)";
          fps4k = "Unplayable (< 15 FPS)";
          tip = "Hardware will experience VRAM bottlenecks and memory swapping. Consider upgrading to a 12GB+ GPU and 16GB dual-channel RAM.";
        }

        const titleEl = document.getElementById("gameTierTitle");
        titleEl.textContent = tierTitle;
        titleEl.className = "text-2xl sm:text-3xl font-black " + tierColor;
        document.getElementById("gamePlayabilityScore").textContent = composite + " / 100";
        document.getElementById("fps1080").textContent = fps1080;
        document.getElementById("fps1440").textContent = fps1440;
        document.getElementById("fps4k").textContent = fps4k;
        document.getElementById("gameOptimizationTip").textContent = tip;

        showToast("🔍 Game compatibility analysis complete!");
      });
    }

    // 6. AI & LLM VRAM Calculator Logic
    const calcLlmBtn = document.getElementById("calcLlmVramBtn");
    if (calcLlmBtn) {
      const modelSpecs = {
        deepseek_r1_671b: { params: 671, name: "DeepSeek R1 (671B)", ollama: "ollama run deepseek-r1:671b", kvRatio: 0.00035 }, // MLA compressed
        deepseek_r1_70b:  { params: 70,  name: "DeepSeek R1 Distill Qwen (70B)", ollama: "ollama run deepseek-r1:70b", kvRatio: 0.0002 },
        llama33_70b:      { params: 70,  name: "Meta LLaMA 3.3 (70B)", ollama: "ollama run llama3.3:70b", kvRatio: 0.0002 },
        deepseek_r1_32b:  { params: 32.5,name: "DeepSeek R1 Distill Qwen (32B)", ollama: "ollama run deepseek-r1:32b", kvRatio: 0.00012 },
        qwen25_32b:       { params: 32.5,name: "Qwen 2.5 Coder (32B)", ollama: "ollama run qwen2.5-coder:32b", kvRatio: 0.00012 },
        deepseek_r1_14b:  { params: 14.7,name: "DeepSeek R1 Distill Qwen (14B)", ollama: "ollama run deepseek-r1:14b", kvRatio: 0.00006 },
        mistral_123b:     { params: 123, name: "Mistral Large 2 (123B)", ollama: "ollama run mistral-large", kvRatio: 0.0003 },
        llama31_8b:       { params: 8.0, name: "Meta LLaMA 3.1 (8B)", ollama: "ollama run llama3.1:8b", kvRatio: 0.000035 },
        gemma2_27b:       { params: 27.2,name: "Google Gemma 2 (27B)", ollama: "ollama run gemma2:27b", kvRatio: 0.0001 },
        phi4_14b:         { params: 14.0,name: "Microsoft Phi-4 (14B)", ollama: "ollama run phi4:14b", kvRatio: 0.00006 }
      };

      const quantMultipliers = {
        fp16: 2.00,
        q8_0: 1.08,
        q5_k_m: 0.72,
        q4_k_m: 0.58,
        q3_k_m: 0.46,
        q2_k: 0.35
      };

      if (calcLlmBtn) calcLlmBtn.addEventListener("click", () => {
        const lRes = document.getElementById("llmResultCard"); if (lRes) lRes.classList.remove("hidden");
        const modelKey = document.getElementById("llmModelSelect").value;
        const quantKey = document.getElementById("llmQuantSelect").value;
        const contextLen = parseInt(document.getElementById("llmContextSelect").value, 10);
        const gpuVram = parseInt(document.getElementById("llmHardwareSelect").value, 10);

        const spec = modelSpecs[modelKey] || modelSpecs.deepseek_r1_70b;
        const bPerParam = quantMultipliers[quantKey] || 0.58;

        // Weights footprint
        const weightsGb = spec.params * bPerParam;

        // KV cache footprint (scales with context length)
        const kvGb = (contextLen * spec.kvRatio) * (quantKey === 'fp16' ? 1.5 : 1.0);

        // CUDA / context activation overhead
        const overheadGb = spec.params > 100 ? 2.5 : (spec.params > 30 ? 1.5 : 1.0);

        const totalVram = weightsGb + kvGb + overheadGb;

        // Determine Status Tier
        let tierTitle = "🟢 100% Fits in GPU VRAM (Maximum Acceleration)";
        let tierColor = "text-emerald-600 dark:text-emerald-400";
        let tip = `Entire model loads directly into GPU VRAM. Lightning-fast throughput (40–90 tokens/second) with zero system memory bottlenecks.`;

        if (totalVram <= gpuVram) {
          tierTitle = "🟢 100% Fits in GPU VRAM (Full Acceleration)";
          tierColor = "text-emerald-600 dark:text-emerald-400";
          tip = `The model (${totalVram.toFixed(1)}GB) fits completely inside your ${gpuVram}GB VRAM buffer. You will achieve maximum native speed (~45–90 tok/sec) via Ollama, vLLM, or LM Studio.`;
        } else if (totalVram <= gpuVram * 2.8) {
          const offloadPct = Math.min(95, Math.round(((totalVram - gpuVram) / totalVram) * 100));
          tierTitle = "🟡 Partial CPU Offloading Required";
          tierColor = "text-amber-500 dark:text-amber-400";
          tip = `Model requires ${totalVram.toFixed(1)}GB memory. With ${gpuVram}GB VRAM, roughly ${offloadPct}% of transformer layers must offload to system RAM via llama.cpp or Ollama. Expected inference speed: 8–18 tokens/sec.`;
        } else {
          tierTitle = "🔴 Insufficient Memory / Severe OOM";
          tierColor = "text-red-500";
          tip = `Model footprint (${totalVram.toFixed(1)}GB) heavily exceeds your current ${gpuVram}GB capacity. Offloading over 80% to system RAM will bottleneck memory bus bandwidth down to < 2 tok/sec. Recommended hardware: ${totalVram > 90 ? 'Dual Mac Studio 192GB or Enterprise Node' : 'GPU upgrade to at least ' + Math.ceil(totalVram) + 'GB combined VRAM'}.`;
        }

        const titleEl = document.getElementById("llmStatusTitle");
        titleEl.textContent = tierTitle;
        titleEl.className = "text-2xl sm:text-3xl font-black " + tierColor;

        document.getElementById("llmTotalVram").textContent = totalVram.toFixed(1) + " GB";
        document.getElementById("llmWeightsMem").textContent = weightsGb.toFixed(1) + " GB";
        document.getElementById("llmKvMem").textContent = kvGb.toFixed(2) + " GB";
        document.getElementById("llmOverheadMem").textContent = overheadGb.toFixed(1) + " GB";
        document.getElementById("llmSpeedTip").textContent = tip;
        document.getElementById("llmOllamaCmd").textContent = spec.ollama;

        showToast("🧠 AI VRAM analysis calculated!");
      });

      const copyCmdBtn = document.getElementById("copyLlmCmdBtn");
      if (copyCmdBtn) {
        if (copyCmdBtn) copyCmdBtn.addEventListener("click", () => {
          const cmdText = document.getElementById("llmOllamaCmd").textContent;
          navigator.clipboard.writeText(cmdText).then(() => {
            showToast("📋 Ollama command copied to clipboard!");
          }).catch(() => {
            showToast("Failed to copy command");
          });
        });
      }
    }

    // Newsletter subscription on tools page
    const toolsForm = document.getElementById("toolsNewsletterForm");
    const toolsEmail = document.getElementById("toolsNewsletterEmail");
    if (toolsForm && toolsEmail) {
      if (toolsForm) toolsForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const em = toolsEmail.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!em || !emailRegex.test(em)) {
          showToast("⚠️ Please enter a valid email address.");
          return;
        }
        let subscribers = [];
        try {
          const stored = localStorage.getItem("pulse_newsletter_subscribers");
          if (stored) subscribers = JSON.parse(stored);
        } catch (err) {}
        if (!subscribers.includes(em)) {
          subscribers.push(em);
          try { localStorage.setItem("pulse_newsletter_subscribers", JSON.stringify(subscribers)); } catch (e) {}
        }
        toolsEmail.value = "";
        showToast("🎉 Successfully subscribed to Tech Boss Dispatch!");
      });
    }

    // Embed Code Copy Handler
    const copyToolEmbedBtn = document.getElementById("copyToolEmbedBtn");
    if (copyToolEmbedBtn) {
      if (copyToolEmbedBtn) copyToolEmbedBtn.addEventListener("click", () => {
        const embedCode = `<iframe src="https://imtechboss.com/tools" width="100%" height="750" frameborder="0" style="border-radius:16px;border:1px solid #334155;"></iframe>\\n<p style="font-size:11px;font-family:sans-serif;color:#64748b;">Powered by <a href="https://imtechboss.com" target="_blank" rel="noopener">Tech Boss Interactive Tools Suite</a></p>`;
        navigator.clipboard.writeText(embedCode).then(() => {
          showToast("📋 Interactive Tools embed code copied to clipboard!");
        }).catch(() => {
          showToast("Failed to copy embed code");
        });
      });
    }
  