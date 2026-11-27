// Cloudflare Pages Advanced Mode Worker
// Lightweight Canonical Routing, 404 Shield & Admin Protection (Zero Payload Bloat)

const duplicateRedirects = {"nvidia-rubin-r100-gpu-architecture-hbm4-288gb-tsmc-3nm-nvlink-6": "nvidia-rubin-r100-ultra-gpu-architecture-hbm4-cowos-3nm-2026", "google-project-suncatcher-space-based-tpu-satellite-ai-data-center-launch": "google-project-suncatcher-orbital-ai-supercomputer-spacex-trillium-tpu-2026", "deepseek-r1-vs-claude-3-7-vs-chatgpt-o3-ai-comparison-2026": "deepseek-r1-vs-openai-o3-vs-claude-3-7-reasoning-models-benchmark-comparison-2026", "claude-vs-chatgpt-vs-deepseek-comparison-2026": "deepseek-r1-vs-openai-o3-vs-claude-3-7-reasoning-models-benchmark-comparison-2026", "how-to-fix-100-percent-disk-usage-windows-11-ssd-sysmain-guide-2026": "how-to-fix-100-percent-memory-disk-leak-windows-11-24h2", "how-to-fix-slow-wifi-at-home-router-tweaks": "how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026", "gta-6-official-release-date-system-requirements-map-leaks-2026": "gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026", "gta-6-release-date-map-pc-specs-nepal-price": "gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026", "how-to-fix-kernel-power-event-id-41-windows-11-random-restarts-2026": "how-to-fix-kernel-power-event-id-41-random-restarts-windows-11"};
const removedSlugs = new Set(["how-to-run-deepseek-r1-locally-windows-11-ollama-gpu-guide", "top-5-free-ai-tools-2026", "top-10-free-ai-tools-everyone-should-use-2026", "openai-gpt6-astra-computer-operator-ai-agent-2026", "apple-mac-mini-m6-first-2nm-chip-desktop-2026", "apple-iphone-18-pro-max-official-review-specs-2026", "iphone-18-pro-max-review-2026", "iphone-18-pro-max-vs-galaxy-s26-ultra", "samsung-galaxy-s26-ultra-review-price-nepal-2026", "samsung-galaxy-tab-s12-ultra-plus-launch-dynamic-amoled-galaxy-ai-2026", "anthropic-claude-sonnet-5-5-terminal-bench-agentic-coding-enterprise-2026", "anthropic-claude-4-5-opus-multi-agent-orchestration-tool-synthesis-2026", "openai-launches-dots-autonomous-always-on-personal-ai-assistant-2026", "xai-grok-4-7-coding-ai-model-elon-musk-2026", "alibaba-zhenwu-v900-china-most-powerful-ai-chip-2026", "white-house-super-intelligence-executive-order-national-tech-compact-2026", "trump-renames-ai-super-intelligence-un-speech-global-regulations-2026", "trump-tv-launch-media-boycott-white-house-2026", "openai-agent-breaches-australian-government-health-portal-2026", "openai-halts-frontier-model-training-sandbox-isolation-flaw-compute-cluster-2026", "cisa-cisco-catalyst-sdwan-zero-day-cve-2026-76504-72-hour-patch-mandate-2026", "critical-citrix-netscaler-zero-day-cve-2026-88772-whipshot-malware-2026", "apple-j490-smart-home-ai-display-october-13-event-john-ternus-2026", "nasa-spacex-crew-13-dragon-grace-iss-launch-october-2026", "spacex-starship-flight-14-first-orbital-launch-starlink-v3-2026", "amd-surpasses-1-trillion-market-cap-datacenter-ai-surge-2026", "apple-homeview-299-smart-display-a18-chip-facial-recognition-homeos-2026", "google-gemini-4-argon-frontier-reasoning-model-1m-token-output-2026", "google-fitbit-air-launch-gemini-health-biometric-wearable-2026", "oneplus-16-esports-flagship-185hz-amoled-8500mah-silicon-carbon-battery-2026", "how-to-bypass-android-frp-google-account-lock-2026-guide", "ea-shuts-down-bioware-cancels-mass-effect-5-rpg-legacy-2026", "apple-iphone-duo-foldable-specs-a20-pro-price-release-guide-2026", "apple-iphone-duo-foldable-display-crack-hinge-damage-warranty-guide-2026", "apple-event-pro-and-tell-m6-macbook-pro-oled-touchscreen-ipad-mini-2026", "anthropic-unveils-claude-duet-autonomous-agent-opus-5-5-marketplace-2026", "ftc-federal-investigation-openai-anthropic-consumer-risk-ai-regulation-2026", "how-to-stream-live-sports-4k-without-cable-wnba-college-football-guide-2026", "how-to-watch-notre-dame-vs-byu-live-stream-tv-channel-peacock-cord-cutting-guide-2026", "gta-6-settings-optimization-120fps", "adobe-premiere-android-launch-free-4k-export-no-watermark-2026", "ai-agents-hidden-communication-cpu-cache-side-channel-sandbox-exploit-2026", "ai-smart-glasses-privacy-ban-uk-venues-worldwide-2026", "amazon-rebrands-kindle-unlimited-to-kindle-plus-ai-audiobooks-pricing-2026", "amd-lisa-su-samsung-hbm4-supply-summit-mi455x-helios-2026", "apple-screenless-fitness-band-whoop-competitor-leaks-2026", "best-budget-1440p-gaming-gpus-2026-vram-price-benchmarks", "best-cheap-cloud-vps-hosting-developers-ai-2026", "best-free-ai-coding-assistant-vscode-2026", "best-free-cloud-vps-gpu-hosting-ai-developers-2026", "best-laptop-video-editing-2026-budget-pro", "best-nvme-ssds-2026-pcie-gen-4-gen-5-gaming-ai-benchmarks", "big-tech-signs-historic-voluntary-ai-safety-accord-standards-2026", "broadcom-custom-ai-asic-chips-surge-threatens-nvidia-gpu-monopoly-2026", "chinese-hackers-impersonate-us-officials-steal-ai-researcher-emails-2026", "coreweave-launches-forge-enterprise-ai-training-agent-evaluation-layer-2026", "ddr5-ram-speed-latency-guide-6000mhz-cl30-vs-7200mhz-gaming-2026", "eu-ai-act-2026-guide-developers-businesses", "europe-jupiter-exascale-supercomputer-2026-specs", "fifa-world-cup-2026-tech-revolution-ai-stadiums-smart-balls", "free-up-iphone-storage-without-deleting-photos", "gta-6-vice-city-album-marketing-countdown-november-2026", "hbm-memory-supercycle-micron-sk-hynix-sold-out-ai-vram-bottleneck-2026", "how-to-build-launch-micro-saas-with-ai-48-hours", "how-to-enable-tpm-2-secure-boot-valorant-windows-11-without-bios-error", "how-to-fix-ea-app-xbox-app-slow-download-speed-windows-11", "how-to-fix-epic-games-launcher-slow-download-speed-windows-11", "how-to-fix-exception-access-violation-0xc0000005-game-crash-windows-11", "how-to-fix-high-cpu-memory-system-compressed-memory-windows-11", "how-to-fix-nvidia-nvlddmkm-sys-blue-screen-bsod-windows-11-2026", "how-to-fix-windows-11-24h2-micro-stuttering-dpc-latency-gaming-guide-2026", "how-to-fix-windows-11-automatic-repair-loop-srttrail-bcd-guide-2026", "how-to-install-ps5-firmware-update-usb-safe-mode-fix-errors-2026", "how-to-protect-from-ai-voice-cloning-phone-scams-2026", "how-to-run-deepseek-r1-locally-offline-ollama-lm-studio-guide-2026", "how-to-run-llm-locally-complete-beginners-guide-2026", "how-to-start-cybersecurity-career-2026-no-degree", "inside-openai-o1-test-time-compute-chain-of-thought-hardware-scaling-2026", "kling-ai-vs-runway-gen-3-vs-luma-dream-machine-ai-video-comparison-2026", "meta-muse-ai-agent-amazon-controversy-autonomous-shopping-2026", "nextdns-vs-control-d-vs-adguard-dns-router-ios-setup-guide-2026", "nist-finalizes-post-quantum-cryptography-fips-203-ml-kem-harvest-now-decrypt-later", "nvidia-geforce-rtx-5070-ti-specs-benchmarks-1440p-gaming-2026", "nvidia-palantir-ai-semiconductor-supply-chain-gpu-shortage-2026", "nvidia-rtx-30-gpu-unlock-mod-vbios-shunt-power-limit-boost-guide-2026", "nvidia-rtx-spark-client-ai-desktops-laptops-specs-architecture-2026", "october-2026-biggest-game-releases-gears-cod-phantom-blade", "oled-monitor-burn-in-prevention-care-guide-2026", "openai-sora-official-launch-cinematic-benchmarks-pricing-alternatives-2026", "qualcomm-snapdragon-x2-elite-3nm-oryon-v2-60-tops-npu-vs-apple-m4-lunar-lake", "rockstar-gta-6-pc-directstorage-16gb-vram-requirements-2026", "samsung-smart-tv-tizen-telemetry-audio-capture-security-report-2026", "softbank-11-billion-ai-bond-sale-openai-infrastructure-2026", "tailscale-vs-wireguard-vs-openvpn-speed-security-2026", "the-2026-gaming-rush-blockbusters-before-gta-6-handheld-wars", "top-cybersecurity-certifications-2026-highest-paying", "top-free-ai-tools-video-voice-generators-2026", "windows-11-september-2026-update-breaks-vpn-connections-how-to-fix"]);

export default {
  async fetch(request, env) {
    try {
      const url = new URL(request.url);
      const pathname = url.pathname.toLowerCase();
      if (pathname === '/test-worker-ping') {
        return new Response('WORKER_IS_ALIVE_2026', { status: 200 });
      }
      const cleanSlug = pathname.replace(/^\/+|\/+$/g, '');

      // 0. Hard Edge 404 Shield for removed/speculative/blogger posts
      if ((removedSlugs.has(cleanSlug) || cleanSlug.startsWith('blogger-')) && !url.searchParams.get('id')) {
        const assetUrl = new URL(request.url);
        assetUrl.pathname = '/404';
        let notFoundRes = await env.ASSETS.fetch(new Request(assetUrl.toString(), request));
        if ((notFoundRes.status === 308 || notFoundRes.status === 301 || notFoundRes.status === 302) && notFoundRes.headers.get('Location')) {
          const locUrl = new URL(notFoundRes.headers.get('Location'), request.url);
          notFoundRes = await env.ASSETS.fetch(new Request(locUrl.toString(), request));
        }
        const notFoundHeaders = new Headers(notFoundRes.headers);
        notFoundHeaders.set('X-Robots-Tag', 'noindex, nofollow');
        notFoundHeaders.set('Content-Type', 'text/html; charset=utf-8');
        const bodyText = await notFoundRes.text();
        const html404 = bodyText && bodyText.length > 200 ? bodyText : '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><title>404 Not Found — Tech Boss</title></head><body style="font-family:sans-serif;text-align:center;padding:4rem"><h1>404 — Page Not Found</h1><p>This story has been removed or moved. <a href="/">Return to Tech Boss Home</a></p></body></html>';
        return new Response(html404, {
          status: 404,
          statusText: 'Not Found',
          headers: notFoundHeaders
        });
      }

      // Check duplicate redirects from merged/deduplicated articles
      if (duplicateRedirects[cleanSlug]) {
        return Response.redirect('https://imtechboss.com/' + duplicateRedirects[cleanSlug] + '/', 301);
      }

      // 0. Canonical 301 Redirect: Consolidate www.imtechboss.com -> imtechboss.com for AdSense & SEO
      if (url.hostname === 'www.imtechboss.com') {
        url.hostname = 'imtechboss.com';
        return Response.redirect(url.toString(), 301);
      }

      // 0.5 Explicit 404 Endpoint Handler (Hard 404 status prevents Soft 404 in Search Console)
      if (pathname === '/404' || pathname === '/404.html') {
        const assetUrl = new URL(request.url);
        assetUrl.pathname = '/404.html';
        const notFoundRes = await env.ASSETS.fetch(new Request(assetUrl.toString(), request));
        const notFoundHeaders = new Headers(notFoundRes.headers);
        notFoundHeaders.set('X-Robots-Tag', 'noindex, nofollow');
        return new Response(notFoundRes.body, {
          status: 404,
          statusText: 'Not Found',
          headers: notFoundHeaders
        });
      }

      const ADMIN_SECRET = (env && env.ADMIN_SECRET) ? String(env.ADMIN_SECRET) : '';

      // 1. Secure Admin Access Controller (Key / Cookie Authenticated via Cloudflare Secret)
      if (pathname === '/admin' || pathname === '/admin.html') {
        const adminKey = url.searchParams.get('key');
        const cookieHeader = request.headers.get('Cookie') || '';
        const hasAuthCookie = ADMIN_SECRET && cookieHeader.includes('tb_admin_auth=granted_secure_2026');

        if (ADMIN_SECRET && ((adminKey && adminKey === ADMIN_SECRET) || hasAuthCookie)) {
          const response = await env.ASSETS.fetch(request);
          const newHeaders = new Headers(response.headers);
          if (adminKey === ADMIN_SECRET) {
            newHeaders.set('Set-Cookie', 'tb_admin_auth=granted_secure_2026; Path=/; Max-Age=86400; Secure; HttpOnly; SameSite=Strict');
          }
          newHeaders.set('X-Robots-Tag', 'noindex, nofollow');
          return new Response(response.body, {
            status: response.status,
            statusText: response.statusText,
            headers: newHeaders
          });
        } else {
          return Response.redirect(new URL('/?admin_denied=1', request.url).toString(), 302);
        }
      }

      // 1.5 Clean URL Normalizer: 301 Redirect /*/index.html -> /*/ and /index.html -> /
      if (pathname.endsWith('/index.html') && pathname !== '/index.html') {
        const cleanPath = pathname.slice(0, -'index.html'.length);
        return new Response(null, {
          status: 301,
          statusText: 'Moved Permanently',
          headers: {
            'Location': 'https://imtechboss.com' + cleanPath,
            'Cache-Control': 'public, max-age=86400',
            'X-Robots-Tag': 'noindex, follow'
          }
        });
      }
      if (pathname === '/index.html') {
        return new Response(null, {
          status: 301,
          statusText: 'Moved Permanently',
          headers: {
            'Location': 'https://imtechboss.com/',
            'Cache-Control': 'public, max-age=86400',
            'X-Robots-Tag': 'noindex, follow'
          }
        });
      }

      // 1.6 Clean URL Normalizer: 301 Redirect standalone *.html utility/legal pages -> canonical trailing slash path
      const staticUtilityPages = ['/about.html', '/contact.html', '/privacy.html', '/terms.html', '/disclaimer.html', '/tools.html', '/compare.html', '/deals.html', '/archive.html'];
      if (staticUtilityPages.includes(pathname)) {
        const cleanPath = pathname.replace(/\.html$/, '') + '/';
        return new Response(null, {
          status: 301,
          statusText: 'Moved Permanently',
          headers: {
            'Location': 'https://imtechboss.com' + cleanPath + (url.search || ''),
            'Cache-Control': 'public, max-age=86400',
            'X-Robots-Tag': 'noindex, follow'
          }
        });
      }

      

      // 1.7 Clean URL Normalizer: 301 Redirect non-trailing-slash utility/legal routes -> canonical trailing slash path
      const nonSlashPages = ['/about', '/contact', '/privacy', '/terms', '/disclaimer', '/tools', '/compare', '/deals', '/archive'];
      if (nonSlashPages.includes(pathname)) {
        return new Response(null, {
          status: 301,
          statusText: 'Moved Permanently',
          headers: {
            'Location': 'https://imtechboss.com' + pathname + '/' + (url.search || ''),
            'Cache-Control': 'public, max-age=86400',
            'X-Robots-Tag': 'noindex, follow'
          }
        });
      }

      // 1.8 Alias Normalizer: Redirect legacy/standard aliases to official canonical endpoints
      const aliasMap = {
        '/privacy-policy': '/privacy/',
        '/privacy-policy/': '/privacy/',
        '/about-us': '/about/',
        '/about-us/': '/about/',
        '/contact-us': '/contact/',
        '/contact-us/': '/contact/',
        '/terms-of-service': '/terms/',
        '/terms-of-service/': '/terms/',
        '/terms-and-conditions': '/terms/',
        '/terms-and-conditions/': '/terms/'
      };
      if (aliasMap[pathname]) {
        return new Response(null, {
          status: 301,
          statusText: 'Moved Permanently',
          headers: {
            'Location': 'https://imtechboss.com' + aliasMap[pathname],
            'Cache-Control': 'public, max-age=86400',
            'X-Robots-Tag': 'noindex, follow'
          }
        });
      }

      const id = url.searchParams.get('id');

      // 1.9 Universal Legacy & Nested Query Redirect Shield (Catches /post, /post.html, /*/post.html?id=*, ?id=* — never static JS/CSS/image assets)
      const isStaticAsset = /\.(js|css|svg|png|jpe?g|webp|ico|json|xml|txt|woff2?)$/i.test(pathname);
      if (!isStaticAsset && (id || pathname === '/post' || pathname === '/post/' || pathname.endsWith('/post') || pathname.endsWith('/post/') || pathname.endsWith('/post.html'))) {
        let dest = 'https://imtechboss.com/';
        if (id && !id.startsWith('blogger-') && id !== 'blogger-512' && !removedSlugs.has(id)) {
          dest = duplicateRedirects[id] ? ('https://imtechboss.com/' + duplicateRedirects[id] + '/') : ('https://imtechboss.com/' + encodeURIComponent(id) + '/');
        } else if (pathname.includes('/post.html')) {
          const parentSlug = pathname.split('/post.html')[0].replace(/^\/+|\/+$/g, '');
          if (parentSlug && !parentSlug.startsWith('blogger-') && !removedSlugs.has(parentSlug)) {
            dest = 'https://imtechboss.com/' + parentSlug + '/';
          }
        }
        return new Response(null, {
          status: 301,
          statusText: 'Moved Permanently',
          headers: {
            'Location': dest,
            'X-Robots-Tag': 'noindex, follow',
            'Cache-Control': 'public, max-age=86400'
          }
        });
      }

      // 2. Trailing Slash Fix for Pages Static Assets
      if (pathname.endsWith('.html') && pathname !== '/index.html' && !pathname.includes('post.html') && pathname !== '/404.html') {
        let response = await env.ASSETS.fetch(request);
        if (response.status === 308 || response.status === 301) {
          const loc = response.headers.get('Location');
          if (loc) {
            const redirectUrl = new URL(loc, request.url);
            response = await env.ASSETS.fetch(new Request(redirectUrl.toString(), request));
          }
        }
        return response;
      }

      // 3. Serve pre-rendered static HTML assets directly (index.html & /<slug>/index.html are already 100% SSG pre-rendered)
      return await env.ASSETS.fetch(request);
    } catch (err) {
      return await env.ASSETS.fetch(request);
    }
  }
};
