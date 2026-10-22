import re, json, os

def generate_worker():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'js', 'data.js')
    worker_path = os.path.join(base_dir, '_worker.js')
    redir_json_path = os.path.join(base_dir, 'scripts', 'duplicate_redirects.json')

    with open(redir_json_path, 'r', encoding='utf-8') as f:
        duplicate_redirects = json.load(f)

    with open(data_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);?\s*$', content, re.DOTALL)
    if not match:
        print('Error: initialArticles not found')
        return

    data = json.loads(match.group(1))
    meta = {}
    for a in data:
        raw_author = a.get('author', 'Tech Boss')
        if isinstance(raw_author, dict):
            author_str = raw_author.get('name', 'Tech Boss')
        elif isinstance(raw_author, str) and raw_author.strip():
            author_str = raw_author.strip()
        else:
            author_str = 'Tech Boss'

        meta[a['id']] = {
            'title': a.get('title', ''),
            'excerpt': a.get('excerpt', ''),
            'content': a.get('content') or a.get('body', ''),
            'readTime': a.get('readTime', '5 min read'),
            'image': a.get('image', ''),
            'date': a.get('date', ''),
            'author': author_str,
            'category': a.get('category', 'AI & Technology')
        }

    # Alias old slug to new slug
    if 'nvidia-blackwell-nvl72-liquid-cooling-overheating-hurdles-2026' in meta:
        meta['nvidia-blackwell-nvl72-racks-liquid-cooling-overheating-hyperscalers-2026'] = meta['nvidia-blackwell-nvl72-liquid-cooling-overheating-hurdles-2026']

    top_articles = [
        {
            'id': a['id'],
            'title': a.get('title', ''),
            'excerpt': a.get('excerpt', ''),
            'image': a.get('image', ''),
            'date': a.get('date', ''),
            'category': a.get('category', 'Technology'),
            'readTime': a.get('readTime', '5 min read')
        }
        for a in data[:10]
    ]

    meta_json = json.dumps(meta, ensure_ascii=False)
    top_articles_json = json.dumps(top_articles, ensure_ascii=False)
    dup_json = json.dumps(duplicate_redirects, ensure_ascii=False)

    removed_slugs_list = [
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
    ]
    removed_json = json.dumps(removed_slugs_list, ensure_ascii=False)

    template = f"""// Cloudflare Pages Advanced Mode Worker
// Automatically injects dynamic OpenGraph & Twitter metadata, plus Edge SSR Pre-Rendering for Google AdSense & SEO

const articlesMeta = {meta_json};
const topArticles = {top_articles_json};
const duplicateRedirects = {dup_json};
const removedSlugs = new Set({removed_json});

export default {{
  async fetch(request, env) {{
    try {{
      const url = new URL(request.url);
      const pathname = url.pathname.toLowerCase();
      if (pathname === '/test-worker-ping') {{
        return new Response('WORKER_IS_ALIVE_2026', {{ status: 200 }});
      }}
      const cleanSlug = pathname.replace(/^\\/+|\\/+$/g, '');

      // 0. Hard Edge 404 Shield for removed/speculative/blogger posts
      if (removedSlugs.has(cleanSlug) || cleanSlug.startsWith('blogger-')) {{
        const assetUrl = new URL(request.url);
        assetUrl.pathname = '/404.html';
        const notFoundRes = await env.ASSETS.fetch(new Request(assetUrl.toString(), request));
        const notFoundHeaders = new Headers(notFoundRes.headers);
        notFoundHeaders.set('X-Robots-Tag', 'noindex, nofollow');
        return new Response(notFoundRes.body, {{
          status: 404,
          statusText: 'Not Found',
          headers: notFoundHeaders
        }});
      }}

      // Check duplicate redirects from merged/deduplicated articles
      if (duplicateRedirects[cleanSlug]) {{
        return Response.redirect('https://imtechboss.com/' + duplicateRedirects[cleanSlug] + '/', 301);
      }}

      // 0. Canonical 301 Redirect: Consolidate www.imtechboss.com -> imtechboss.com for AdSense & SEO
      if (url.hostname === 'www.imtechboss.com') {{
        url.hostname = 'imtechboss.com';
        return Response.redirect(url.toString(), 301);
      }}

      const ADMIN_SECRET = 'binod_boss_2026';

      // 1. Secure Admin Access Controller (Key / Cookie Authenticated)
      if (pathname === '/admin' || pathname === '/admin.html') {{
        const adminKey = url.searchParams.get('key');
        const cookieHeader = request.headers.get('Cookie') || '';
        const hasAuthCookie = cookieHeader.includes('tb_admin_auth=granted_secure_2026');

        if (adminKey === ADMIN_SECRET || hasAuthCookie) {{
          const response = await env.ASSETS.fetch(request);
          const newHeaders = new Headers(response.headers);
          if (adminKey === ADMIN_SECRET) {{
            newHeaders.set('Set-Cookie', 'tb_admin_auth=granted_secure_2026; Path=/; Max-Age=86400; Secure; HttpOnly; SameSite=Strict');
          }}
          newHeaders.set('X-Robots-Tag', 'noindex, nofollow');
          return new Response(response.body, {{
            status: response.status,
            statusText: response.statusText,
            headers: newHeaders
          }});
        }} else {{
          return Response.redirect(new URL('/?admin_denied=1', request.url).toString(), 302);
        }}
      }}

      // 2. Trailing Slash Fix for Pages Static Assets
      if (pathname.endsWith('.html') && pathname !== '/index.html' && pathname !== '/post.html') {{
        let response = await env.ASSETS.fetch(request);
        if (response.status === 308 || response.status === 301) {{
          const loc = response.headers.get('Location');
          if (loc) {{
            const redirectUrl = new URL(loc, request.url);
            response = await env.ASSETS.fetch(new Request(redirectUrl.toString(), request));
          }}
        }}
        return response;
      }}

      // 3. Homepage Edge SSR: Pre-render top articles into raw HTML for Google AdSense Review Crawlers
      if (pathname === '/' || pathname === '/index.html') {{
        const response = await env.ASSETS.fetch(request);
        const hero = topArticles[0];
        const heroTitle = (hero.title || '').replace(/"/g, '&quot;');
        const heroDesc = (hero.excerpt || '').replace(/"/g, '&quot;');
        const heroImg = hero.image || 'https://imtechboss.com/og-image.png';

        let gridHtml = '';
        for (let i = 0; i < topArticles.length; i++) {{
          const a = topArticles[i];
          const st = (a.title || '').replace(/"/g, '&quot;');
          const se = (a.excerpt || '').replace(/"/g, '&quot;');
          gridHtml += `
            <article class="article-card bg-white dark:bg-slate-900 rounded-2xl overflow-hidden border border-gray-200 dark:border-slate-800 shadow-sm flex flex-col">
              <div class="aspect-[16/10] overflow-hidden bg-gray-100">
                <a href="/${{encodeURIComponent(a.id)}}/" aria-hidden="true" tabindex="-1">
                  <img src="${{a.image}}" alt="${{st}}" class="w-full h-full object-cover" loading="lazy" />
                </a>
              </div>
              <div class="p-5 flex-1 flex flex-col justify-between">
                <div>
                  <div class="text-[11px] text-gray-500 mb-2"><span>${{a.category || 'Tech'}}</span> &bull; <span>${{a.date || 'Recent'}}</span></div>
                  <h2 class="font-bold text-base sm:text-lg text-gray-900 dark:text-gray-100 line-clamp-2">
                    <a href="/${{encodeURIComponent(a.id)}}/">${{st}}</a>
                  </h2>
                  <p class="text-xs text-gray-600 dark:text-gray-400 mt-2 line-clamp-2">${{se}}</p>
                </div>
                <div class="mt-4 pt-4 border-t border-gray-100 dark:border-slate-800 flex justify-between items-center text-xs">
                  <span class="font-semibold text-gray-700 dark:text-gray-300">Tech Boss</span>
                  <a href="/${{encodeURIComponent(a.id)}}/" class="font-bold text-blue-600 hover:underline">Read Article &rarr;</a>
                </div>
              </div>
            </article>
          `;
        }}

        return new HTMLRewriter()
          .on('div#featuredArticleContainer', {{
            element(e) {{
              e.setInnerContent(`
                <a href="/${{encodeURIComponent(hero.id)}}/" class="block relative rounded-3xl overflow-hidden shadow-xl aspect-[16/9] md:aspect-[21/11] bg-slate-900 group cursor-pointer">
                  <img src="${{heroImg}}" alt="${{heroTitle}}" class="w-full h-full object-cover opacity-80" />
                  <div class="absolute inset-0 bg-gradient-to-t from-black/95 via-black/50 to-transparent flex flex-col justify-end p-6 sm:p-8 md:p-10 text-white">
                    <span class="px-3 py-1 text-xs font-bold uppercase tracking-wider rounded-full bg-blue-600 text-white w-max mb-3">${{hero.category || 'Featured'}}</span>
                    <h1 class="text-xl sm:text-2xl md:text-3xl font-bold font-serif-heading leading-tight mb-2">${{heroTitle}}</h1>
                    <p class="text-xs sm:text-sm text-gray-300 line-clamp-2 mb-4 leading-relaxed">${{heroDesc}}</p>
                    <div class="text-xs text-gray-400">By Tech Boss &bull; ${{hero.date || 'Recent'}}</div>
                  </div>
                </a>
              `, {{ html: true }});
            }}
          }})
          .on('div#articlesGrid', {{
            element(e) {{
              e.setInnerContent(gridHtml, {{ html: true }});
            }}
          }})
          .transform(response);
      }}

      const id = url.searchParams.get('id');

      // 4. Legacy Post Query Parameter Redirects -> Clean Static /slug/
      if (pathname === '/post.html' || pathname === '/post') {{
        if (!id || id === 'blogger-512') {{
          return Response.redirect(new URL('/', request.url).toString(), 301);
        }}
        if (duplicateRedirects[id]) {{
          return Response.redirect('https://imtechboss.com/' + duplicateRedirects[id] + '/', 301);
        }}
        return Response.redirect('https://imtechboss.com/' + encodeURIComponent(id) + '/', 301);
      }}

      if (pathname === '/404' || pathname === '/404.html') {{
        const assetUrl = new URL(request.url);
        assetUrl.pathname = '/404.html';
        const notFoundRes = await env.ASSETS.fetch(new Request(assetUrl.toString(), request));
        const notFoundHeaders = new Headers(notFoundRes.headers);
        notFoundHeaders.set('X-Robots-Tag', 'noindex, nofollow');
        return new Response(notFoundRes.body, {{
          status: 404,
          headers: notFoundHeaders
        }});
      }}

      return await env.ASSETS.fetch(request);
    }} catch (err) {{
      return await env.ASSETS.fetch(request);
    }}
  }}
}};
"""

    with open(worker_path, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f'Successfully generated _worker.js with {len(meta)} articles and 301 duplicate redirects.')

if __name__ == '__main__':
    generate_worker()
