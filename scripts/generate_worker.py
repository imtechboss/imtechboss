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
            'image': a.get('image', ''),
            'date': a.get('date', ''),
            'author': a.get('author', 'Tech Boss'),
            'category': a.get('category', 'AI & Technology')
        }

    # Alias old slug to new slug so both work seamlessly
    if 'nvidia-blackwell-nvl72-liquid-cooling-overheating-hurdles-2026' in meta:
        meta['nvidia-blackwell-nvl72-racks-liquid-cooling-overheating-hyperscalers-2026'] = meta['nvidia-blackwell-nvl72-liquid-cooling-overheating-hurdles-2026']

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
        const safeDate = article.date || '';
        const safeAuthor = (article.author || 'Tech Boss').replace(/"/g, '&quot;');
        const safeCategory = article.category || 'AI & Technology';

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
              "name": "Will these optimization steps reset after a Windows update?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Most software configurations persist across normal restarts, though major seasonal Windows feature updates may occasionally revert specific background telemetry or service preferences."
              }}
            }},
            {{
              "@type": "Question",
              "name": "Where can I find more technical benchmarks and developer tools?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Explore the Tech Boss Interactive Tools suite, PC Bottleneck Calculator, and dedicated hardware reviews directly on imtechboss.com."
              }}
            }}
          ];
        }}

        const jsonLd = JSON.stringify({{
          "@context": "https://schema.org",
          "@graph": [
            {{
              "@type": ["TechArticle", "NewsArticle"],
              "@id": canonical + "#article",
              "isPartOf": {{
                "@type": "WebPage",
                "@id": canonical
              }},
              "headline": article.title || '',
              "description": article.excerpt || '',
              "image": [safeImg],
              "datePublished": safeDate,
              "dateModified": safeDate,
              "articleSection": safeCategory,
              "inLanguage": "en-US",
              "author": {{
                "@type": "Person",
                "name": article.author || 'Tech Boss',
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
              "mainEntityOfPage": {{
                "@type": "WebPage",
                "@id": canonical
              }},
              "url": canonical,
              "speakable": {{
                "@type": "SpeakableSpecification",
                "cssSelector": ["#postTitle", "#postExcerpt", "#postContent p"]
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
              e.prepend(`<img class="flipboard-image" src="${{safeImg}}" alt="${{safeTitle}}" width="1200" height="900" style="max-width:100%;height:auto;display:block;" />`, {{ html: true }});
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
