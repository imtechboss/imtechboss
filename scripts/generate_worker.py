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
        meta[a['id']] = {
            'title': a.get('title', ''),
            'excerpt': a.get('excerpt', ''),
            'image': a.get('image', '')
        }

    meta_json = json.dumps(meta, ensure_ascii=False)

    template = f"""// Cloudflare Pages Advanced Mode Worker
// Automatically injects dynamic OpenGraph & Twitter metadata for /post & /post.html

const articlesMeta = {meta_json};

export default {{
  async fetch(request, env) {{
    try {{
      const url = new URL(request.url);
      const id = url.searchParams.get('id');

      if ((url.pathname === '/post' || url.pathname === '/post.html') && id && articlesMeta[id]) {{
        const assetUrl = new URL(request.url);
        assetUrl.pathname = '/post';
        const response = await env.ASSETS.fetch(new Request(assetUrl.toString(), request));
        const article = articlesMeta[id];
        const safeTitle = (article.title || '').replace(/"/g, '&quot;');
        const safeDesc = (article.excerpt || '').replace(/"/g, '&quot;');
        const safeImg = article.image || 'https://imtechboss.com/og-image.png';
        const canonical = 'https://imtechboss.com/post?id=' + encodeURIComponent(id);

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
              e.prepend(`<img class="flipboard-image" src="${{safeImg}}" alt="${{safeTitle}}" style="display:none;" />`, {{ html: true }});
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

      return await env.ASSETS.fetch(request);
    }} catch (err) {{
      return await env.ASSETS.fetch(request);
    }}
  }}
}};
"""

    with open(worker_path, 'w', encoding='utf-8') as out:
        out.write(template)

    print(f'Successfully generated _worker.js with {len(meta)} articles.')

if __name__ == '__main__':
    generate_worker()
