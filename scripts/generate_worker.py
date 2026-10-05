import re, json, os

def generate_worker():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'js', 'data.js')
    worker_path = os.path.join(base_dir, '_worker.js')

    with open(data_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'var\s+initialArticles\s*=\s*(\[.*?\]);', content, re.DOTALL)
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

    # Alias old slug to new slug so both work seamlessly
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

    template = f"""// Cloudflare Pages Advanced Mode Worker
// Automatically injects dynamic OpenGraph & Twitter metadata, plus Edge SSR Pre-Rendering for Google AdSense & SEO

const articlesMeta = {meta_json};
const topArticles = {top_articles_json};

export default {{
  async fetch(request, env) {{
    try {{
      const url = new URL(request.url);
      const pathname = url.pathname.toLowerCase();
      const ADMIN_SECRET = 'binod_boss_2026';

      // 1. Secure Admin Access Controller (Key / Cookie Authenticated)
      if (pathname === '/admin' || pathname === '/admin.html') {{
        const adminKey = url.searchParams.get('key');
        const cookieHeader = request.headers.get('Cookie') || '';
        const hasAdminCookie = cookieHeader.includes('tb_admin_token=' + ADMIN_SECRET);

        if (adminKey === ADMIN_SECRET || hasAdminCookie) {{
          const assetUrl = new URL(request.url);
          assetUrl.pathname = '/admin';
          assetUrl.search = '';
          let response = await env.ASSETS.fetch(new Request(assetUrl.toString(), request));
          if (response.status >= 300 && response.status < 400) {{
            const loc = response.headers.get('Location') || '/admin';
            const redirectUrl = new URL(loc, request.url);
            response = await env.ASSETS.fetch(new Request(redirectUrl.toString(), request));
          }}
          const newHeaders = new Headers(response.headers);
          newHeaders.delete('Location');
          newHeaders.set('Content-Type', 'text/html; charset=utf-8');
          if (adminKey === ADMIN_SECRET) {{
            newHeaders.set('Set-Cookie', `tb_admin_token=${{ADMIN_SECRET}}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=86400`);
          }}
          return new Response(response.body, {{
            status: 200,
            headers: newHeaders
          }});
        }}

        // Unauthorized visitors or bots get a dead 404
        return new Response('404 Not Found', {{ status: 404, headers: {{ 'Content-Type': 'text/plain' }} }});
      }}

      // 2. Edge Security Shield: Block sensitive internal paths from external access
      if (
        pathname.startsWith('/scripts') || 
        pathname.startsWith('/blogger') || 
        pathname.includes('..') ||
        pathname.endsWith('.py') ||
        pathname.endsWith('.jsonl') ||
        pathname.endsWith('.sh')
      ) {{
        return new Response('404 Not Found', {{ status: 404, headers: {{ 'Content-Type': 'text/plain' }} }});
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
                <a href="post.html?id=${{encodeURIComponent(a.id)}}">
                  <img src="${{a.image}}" alt="${{st}}" class="w-full h-full object-cover" loading="lazy" />
                </a>
              </div>
              <div class="p-5 flex-1 flex flex-col justify-between">
                <div>
                  <div class="text-[11px] text-gray-500 mb-2"><span>${{a.category || 'Tech'}}</span> &bull; <span>${{a.date || 'Recent'}}</span></div>
                  <h2 class="font-bold text-base sm:text-lg text-gray-900 dark:text-gray-100 line-clamp-2">
                    <a href="post.html?id=${{encodeURIComponent(a.id)}}">${{st}}</a>
                  </h2>
                  <p class="text-xs text-gray-600 dark:text-gray-400 mt-2 line-clamp-2">${{se}}</p>
                </div>
                <div class="mt-4 pt-4 border-t border-gray-100 dark:border-slate-800 flex justify-between items-center text-xs">
                  <span class="font-semibold text-gray-700 dark:text-gray-300">Tech Boss</span>
                  <a href="post?id=${{encodeURIComponent(a.id)}}" class="font-bold text-blue-600 hover:underline">Read Article &rarr;</a>
                </div>
              </div>
            </article>
          `;
        }}

        return new HTMLRewriter()
          .on('div#featuredArticleContainer', {{
            element(e) {{
              e.setInnerContent(`
                <a href="post?id=${{encodeURIComponent(hero.id)}}" class="block relative rounded-3xl overflow-hidden shadow-xl aspect-[16/9] md:aspect-[21/11] bg-slate-900 group cursor-pointer">
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

      // 4. Dedicated Post Article Edge SSR: Pre-renders full article text for Google AdSense & SEO crawlers
      if (pathname === '/post' || pathname === '/post.html') {{
        if (!id) {{
          return Response.redirect(new URL('/', request.url).toString(), 301);
        }}
        if (!Object.prototype.hasOwnProperty.call(articlesMeta, id)) {{
          return new Response('Article Not Found', {{
            status: 404,
            headers: {{
              'Content-Type': 'text/plain; charset=utf-8',
              'X-Robots-Tag': 'noindex, nofollow'
            }}
          }});
        }}
        const assetUrl = new URL(request.url);
        assetUrl.pathname = '/post';
        const response = await env.ASSETS.fetch(new Request(assetUrl.toString(), request));
        const article = articlesMeta[id];
        const safeTitle = (article.title || '').replace(/"/g, '&quot;');
        const safeDesc = (article.excerpt || '').replace(/"/g, '&quot;');
        let safeImg = article.image || 'https://imtechboss.com/og-image.png';
        if (!safeImg.startsWith('http')) {{
          safeImg = 'https://imtechboss.com' + (safeImg.startsWith('/') ? '' : '/') + safeImg;
        }}
        const canonical = 'https://imtechboss.com/post?id=' + encodeURIComponent(id);
        const safeDate = article.date || '';
        const safeAuthor = (typeof article.author === 'string' ? article.author : (article.author?.name || 'Tech Boss')).replace(/"/g, '&quot;');
        const safeCategory = article.category || 'AI & Technology';
        const safeReadTime = article.readTime || '5 min read';
        const articleBody = article.content || '';

        let faqs = [];
        const catLower = safeCategory.toLowerCase();
        const titleUpper = (article.title || '').toUpperCase();
        if (catLower.includes('hard') || titleUpper.includes('RTX') || titleUpper.includes('RYZEN') || titleUpper.includes('INTEL') || titleUpper.includes('GPU') || titleUpper.includes('CPU') || titleUpper.includes('TSMC') || titleUpper.includes('A16') || titleUpper.includes('SEMICONDUCTOR')) {{
          faqs = [
            {{
              "@type": "Question",
              "name": "How does this semiconductor or hardware architecture improve performance and efficiency?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "By advancing lithography nodes and implementing backside power delivery networks (BSPDN), silicon designs reduce voltage drop (IR drop), eliminate interconnect congestion, and deliver 15% to 25% lower power consumption alongside double-digit clock frequency gains."
              }}
            }},
            {{
              "@type": "Question",
              "name": "Will this hardware advancement require new motherboard platforms or power standards?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Next-generation architectures often require updated socket standards, PCIe 5.0/6.0 bandwidth pipelines, and ATX 3.1 certified power delivery to handle aggressive transient power spikes and extreme compute densities."
              }}
            }},
            {{
              "@type": "Question",
              "name": "When will this technology reach commercial hardware availability?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Advanced process nodes transition from initial foundry risk production to high-volume manufacturing within 6 to 9 months, prioritizing high-performance computing (HPC) and flagship AI accelerators before client consumer rollouts."
              }}
            }}
          ];
        }} else if (catLower.includes('ai') || titleUpper.includes('DEEPSEEK') || titleUpper.includes('CLAUDE') || titleUpper.includes('GPT') || titleUpper.includes('LLM') || titleUpper.includes('MODEL') || titleUpper.includes('COLOSSUS')) {{
          faqs = [
            {{
              "@type": "Question",
              "name": "Can this AI model or architecture run locally on consumer hardware?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Quantized versions (such as 4-bit and 8-bit GGUF models) can run locally on consumer GPUs with 12GB to 24GB of VRAM using inference engines like Ollama, llama.cpp, and LM Studio."
              }}
            }},
            {{
              "@type": "Question",
              "name": "How does test-time compute reasoning improve model answers?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Reasoning models generate internal chain-of-thought tokens, verifying mathematical intermediate steps and backtracking when encountering logical contradictions before providing the output."
              }}
            }},
            {{
              "@type": "Question",
              "name": "Is prompt data kept private when self-hosting local models?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Yes. Running models on local hardware ensures that your prompts, source code, and queries remain on your private machine without transmitting telemetry to third-party cloud APIs."
              }}
            }}
          ];
        }} else {{
          faqs = [
            {{
              "@type": "Question",
              "name": "Are these technical instructions safe to apply on Windows 11?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Yes. The steps detailed in this Tech Boss analysis operate within standard operating system guidelines and do not modify protected kernel modules or partition structures."
              }}
            }},
            {{
              "@type": "Question",
              "name": "Does this solution require specialized third-party diagnostic software?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "The troubleshooting steps utilize built-in administrative tools such as PowerShell, DISM, SFC, and native Windows Diagnostics."
              }}
            }},
            {{
              "@type": "Question",
              "name": "What should I do if this issue persists after applying the fix?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Verify hardware stability, run memory integrity diagnostics, and inspect event viewer logs for recurring kernel error codes."
              }}
            }}
          ];
        }}

        const jsonLd = JSON.stringify({{
          "@context": "https://schema.org",
          "@graph": [
            {{
              "@type": "TechArticle",
              "@id": canonical + "#article",
              "isPartOf": {{
                "@type": "WebPage",
                "@id": canonical
              }},
              "headline": article.title || '',
              "description": article.excerpt || '',
              "image": [safeImg],
              "datePublished": article.date ? new Date(article.date).toISOString() : new Date().toISOString(),
              "dateModified": new Date().toISOString(),
              "inLanguage": "en-US",
              "mainEntityOfPage": canonical,
              "author": {{
                "@type": "Organization",
                "name": safeAuthor,
                "url": "https://imtechboss.com"
              }},
              "publisher": {{
                "@type": "Organization",
                "name": "Tech Boss",
                "url": "https://imtechboss.com",
                "logo": {{
                  "@type": "ImageObject",
                  "url": "https://imtechboss.com/og-image.png"
                }}
              }},
              "speakable": {{
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", "#articleContainer p"]
              }}
            }},
            {{
              "@type": "BreadcrumbList",
              "@id": canonical + "#breadcrumb",
              "itemListElement": [
                {{
                  "@type": "ListItem",
                  "position": 1,
                  "name": "Home",
                  "item": "https://imtechboss.com/"
                }},
                {{
                  "@type": "ListItem",
                  "position": 2,
                  "name": safeCategory,
                  "item": "https://imtechboss.com/?category=" + encodeURIComponent(safeCategory)
                }},
                {{
                  "@type": "ListItem",
                  "position": 3,
                  "name": article.title || '',
                  "item": canonical
                }}
              ]
            }},
            {{
              "@type": "FAQPage",
              "@id": canonical + "#faq",
              "mainEntity": faqs
            }}
          ]
        }});

        return new HTMLRewriter()
          .on('title#pageTitle', {{
            element(e) {{
              e.setInnerContent(safeTitle + ' | Tech Boss');
            }}
          }})
          .on('meta#metaDescription', {{
            element(e) {{
              e.setAttribute('content', safeDesc);
            }}
          }})
          .on('link#canonicalUrl', {{
            element(e) {{
              e.setAttribute('href', canonical);
            }}
          }})
          .on('head', {{
            element(e) {{
              e.append(`<script id="articleJsonLd" type="application/ld+json">${{jsonLd}}</script>`, {{ html: true }});
            }}
          }})
          .on('meta#ogTitle', {{
            element(e) {{
              e.setAttribute('content', safeTitle);
            }}
          }})
          .on('meta#ogDescription', {{
            element(e) {{
              e.setAttribute('content', safeDesc);
            }}
          }})
          .on('meta#ogImage', {{
            element(e) {{
              e.setAttribute('content', safeImg);
            }}
          }})
          .on('meta#ogImageSecure', {{
            element(e) {{
              e.setAttribute('content', safeImg);
            }}
          }})
          .on('link#imgSrc', {{
            element(e) {{
              e.setAttribute('href', safeImg);
            }}
          }})
          .on('article#articleContainer', {{
            element(e) {{
              e.setInnerContent(`
                <div class="static-ssr-post prose max-w-none">
                  <div class="flex items-center gap-2 mb-4 text-xs text-gray-500">
                    <a href="/">Home</a> &bull; <span class="font-bold text-blue-600">${{safeCategory}}</span> &bull; <span>${{safeDate}}</span> &bull; <span>${{safeReadTime}}</span> &bull; <span>By ${{safeAuthor}}</span>
                  </div>
                  <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-extrabold text-gray-950 dark:text-white mb-6 leading-tight">${{safeTitle}}</h1>
                  <div class="flex items-center gap-3.5 p-4 rounded-2xl bg-gray-50 dark:bg-slate-800/60 border border-gray-200/70 dark:border-slate-800 mb-8">
                    <div class="w-12 h-12 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-lg">TB</div>
                    <div>
                      <div class="font-bold text-sm sm:text-base text-gray-900 dark:text-gray-100">${{safeAuthor}}</div>
                      <div class="text-xs text-gray-500 dark:text-gray-400">Tech Boss Editorial &bull; imtechboss.com</div>
                    </div>
                  </div>
                  <img class="flipboard-image w-full rounded-2xl mb-8 object-cover max-h-[520px]" src="${{safeImg}}" alt="${{safeTitle}}" width="1200" height="900" style="max-width:100%;height:auto;display:block;" />
                  <div class="article-content text-base sm:text-lg leading-relaxed text-gray-800 dark:text-gray-200">
                    ${{articleBody}}
                  </div>
                </div>
              `, {{ html: true }});
            }}
          }})
          .on('meta#ogUrl', {{
            element(e) {{
              e.setAttribute('content', canonical);
            }}
          }})
          .on('meta#twTitle', {{
            element(e) {{
              e.setAttribute('content', safeTitle);
            }}
          }})
          .on('meta#twDescription', {{
            element(e) {{
              e.setAttribute('content', safeDesc);
            }}
          }})
          .on('meta#twImage', {{
            element(e) {{
              e.setAttribute('content', safeImg);
            }}
          }})
          .on('meta#twUrl', {{
            element(e) {{
              e.setAttribute('content', canonical);
            }}
          }})
          .transform(response);
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

    with open(worker_path, 'w', encoding='utf-8') as out:
        out.write(template)

    print(f'Successfully generated _worker.js with {len(meta)} articles and Edge SSR pre-rendering.')

if __name__ == '__main__':
    generate_worker()
