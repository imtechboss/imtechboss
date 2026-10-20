import os
import json
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target_file = os.path.join(base_dir, 'scripts', 'generate_worker.py')
redir_json_path = os.path.join(base_dir, 'scripts', 'duplicate_redirects.json')

with open(redir_json_path, 'r', encoding='utf-8') as f:
    duplicate_redirects = json.load(f)

dup_json_str = json.dumps(duplicate_redirects, indent=2)

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add duplicateRedirects variable
content = content.replace("const topArticles = {top_articles_json};\n", f"const topArticles = {{top_articles_json}};\nconst duplicateRedirects = {dup_json_str};\n")

# Add slug check in worker fetch
old_fetch_start = """      const pathname = url.pathname.toLowerCase();
      // 0. Canonical 301 Redirect: Consolidate www.imtechboss.com -> imtechboss.com for AdSense & SEO"""

new_fetch_start = """      const pathname = url.pathname.toLowerCase();

      // Check duplicate redirects from merged articles
      const cleanSlug = pathname.replace(/^\\/|\\/$/g, '');
      if (duplicateRedirects[cleanSlug]) {{
        return Response.redirect('https://imtechboss.com/' + duplicateRedirects[cleanSlug] + '/', 301);
      }}

      // 0. Canonical 301 Redirect: Consolidate www.imtechboss.com -> imtechboss.com for AdSense & SEO"""

content = content.replace(old_fetch_start, new_fetch_start)

# Add redirect map check in post handler
old_post_handler = """      if (pathname === '/post.html' || pathname === '/post') {{
        if (!id || id === 'blogger-512') {{
          return Response.redirect(new URL('/', request.url).toString(), 301);
        }}
        if (id === 'gta-6-official-release-date-system-requirements-map-leaks-2026') {{
          return Response.redirect('https://imtechboss.com/gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026/', 301);
        }}
        return Response.redirect('https://imtechboss.com/' + encodeURIComponent(id) + '/', 301);
      }}"""

new_post_handler = """      if (pathname === '/post.html' || pathname === '/post') {{
        if (!id || id === 'blogger-512') {{
          return Response.redirect(new URL('/', request.url).toString(), 301);
        }}
        if (duplicateRedirects[id]) {{
          return Response.redirect('https://imtechboss.com/' + duplicateRedirects[id] + '/', 301);
        }}
        return Response.redirect('https://imtechboss.com/' + encodeURIComponent(id) + '/', 301);
      }}"""

content = content.replace(old_post_handler, new_post_handler)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Updated scripts/generate_worker.py with duplicateRedirects!")
