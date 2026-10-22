// Cloudflare Pages Functions - Global Request Interceptor
// Enforces Hard Edge 404 for removed/speculative/blogger posts and 301 canonical redirects

const duplicateRedirects = {
  "nvidia-rubin-r100-gpu-architecture-hbm4-288gb-tsmc-3nm-nvlink-6": "nvidia-rubin-r100-ultra-gpu-architecture-hbm4-cowos-3nm-2026",
  "google-project-suncatcher-space-based-tpu-satellite-ai-data-center-launch": "google-project-suncatcher-orbital-ai-supercomputer-spacex-trillium-tpu-2026",
  "how-to-run-deepseek-r1-locally-windows-11-ollama-gpu-guide": "how-to-run-deepseek-r1-locally-offline-ollama-lm-studio-guide-2026",
  "deepseek-r1-vs-claude-3-7-vs-chatgpt-o3-ai-comparison-2026": "deepseek-r1-vs-openai-o3-vs-claude-3-7-reasoning-models-benchmark-comparison-2026",
  "claude-vs-chatgpt-vs-deepseek-comparison-2026": "deepseek-r1-vs-openai-o3-vs-claude-3-7-reasoning-models-benchmark-comparison-2026",
  "how-to-fix-100-percent-disk-usage-windows-11-ssd-sysmain-guide-2026": "how-to-fix-100-percent-memory-disk-leak-windows-11-24h2",
  "how-to-fix-slow-wifi-at-home-router-tweaks": "how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026",
  "gta-6-official-release-date-system-requirements-map-leaks-2026": "gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026",
  "gta-6-release-date-map-pc-specs-nepal-price": "gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026",
  "top-5-free-ai-tools-2026": "top-free-ai-tools-video-voice-generators-2026",
  "top-10-free-ai-tools-everyone-should-use-2026": "top-free-ai-tools-video-voice-generators-2026"
};

const removedSlugs = new Set([
  "openai-gpt6-astra-computer-operator-ai-agent-2026",
  "apple-mac-mini-m6-first-2nm-chip-desktop-2026",
  "apple-iphone-18-pro-max-official-review-specs-2026",
  "iphone-18-pro-max-review-2026",
  "iphone-18-pro-max-vs-galaxy-s26-ultra",
  "samsung-galaxy-s26-ultra-review-price-nepal-2026",
  "samsung-galaxy-tab-s12-ultra-plus-launch-dynamic-amoled-galaxy-ai-2026",
  "anthropic-claude-sonnet-5-5-terminal-bench-agentic-coding-enterprise-2026",
  "anthropic-claude-4-5-opus-multi-agent-orchestration-tool-synthesis-2026",
  "openai-launches-dots-autonomous-always-on-personal-ai-assistant-2026",
  "xai-grok-4-7-coding-ai-model-elon-musk-2026",
  "alibaba-zhenwu-v900-china-most-powerful-ai-chip-2026",
  "white-house-super-intelligence-executive-order-national-tech-compact-2026",
  "trump-renames-ai-super-intelligence-un-speech-global-regulations-2026",
  "trump-tv-launch-media-boycott-white-house-2026",
  "openai-agent-breaches-australian-government-health-portal-2026",
  "openai-halts-frontier-model-training-sandbox-isolation-flaw-compute-cluster-2026",
  "cisa-cisco-catalyst-sdwan-zero-day-cve-2026-76504-72-hour-patch-mandate-2026",
  "critical-citrix-netscaler-zero-day-cve-2026-88772-whipshot-malware-2026",
  "apple-j490-smart-home-ai-display-october-13-event-john-ternus-2026",
  "nasa-spacex-crew-13-dragon-grace-iss-launch-october-2026",
  "spacex-starship-flight-14-first-orbital-launch-starlink-v3-2026",
  "amd-surpasses-1-trillion-market-cap-datacenter-ai-surge-2026",
  "apple-homeview-299-smart-display-a18-chip-facial-recognition-homeos-2026",
  "google-gemini-4-argon-frontier-reasoning-model-1m-token-output-2026",
  "google-fitbit-air-launch-gemini-health-biometric-wearable-2026",
  "oneplus-16-esports-flagship-185hz-amoled-8500mah-silicon-carbon-battery-2026"
]);

export async function onRequest(context) {
  try {
    const url = new URL(context.request.url);
    const pathname = url.pathname.toLowerCase();
    const cleanSlug = pathname.replace(/^\/+|\/+$/g, '');

    // 0. Worker Ping Check
    if (pathname === '/test-worker-ping') {
      return new Response('PAGES_FUNCTION_ALIVE_2026', { status: 200 });
    }

    // 1. Edge 404 Shield for removed/speculative/blogger posts
    if (removedSlugs.has(cleanSlug) || cleanSlug.startsWith('blogger-')) {
      const assetUrl = new URL(context.request.url);
      assetUrl.pathname = '/404.html';
      const notFoundRes = await context.env.ASSETS.fetch(new Request(assetUrl.toString(), context.request));
      const notFoundHeaders = new Headers(notFoundRes.headers);
      notFoundHeaders.set('X-Robots-Tag', 'noindex, nofollow');
      notFoundHeaders.set('Cache-Control', 'public, max-age=86400');
      return new Response(notFoundRes.body, {
        status: 404,
        statusText: 'Not Found',
        headers: notFoundHeaders
      });
    }

    // 2. Canonical 301 Redirect for Duplicate Posts
    if (duplicateRedirects[cleanSlug]) {
      return Response.redirect('https://imtechboss.com/' + duplicateRedirects[cleanSlug] + '/', 301);
    }

    // 3. Fall through to static asset or standard Pages serving
    return await context.next();
  } catch (err) {
    return await context.next();
  }
}
