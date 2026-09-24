import { articlesMeta } from './articles_meta.js';

export async function onRequest(context) {
  try {
    const { request, env } = context;
    const url = new URL(request.url);
    const id = url.searchParams.get('id');
    const response = await env.ASSETS.fetch(request);

    if (!id || !articlesMeta[id]) {
      return response;
    }

    const article = articlesMeta[id];
    const safeTitle = (article.title || '').replace(/"/g, '&quot;');
    const safeDesc = (article.excerpt || '').replace(/"/g, '&quot;');
    const safeImg = article.image || 'https://imtechboss.com/og-image.png';
    const canonical = `https://imtechboss.com/post.html?id=${encodeURIComponent(id)}`;

    return new HTMLRewriter()
      .on('title#pageTitle', {
        element(e) {
          e.setInnerContent(`${safeTitle} | Tech Boss`);
        }
      })
      .on('meta#metaDescription', {
        element(e) {
          e.setAttribute('content', safeDesc);
        }
      })
      .on('link#canonicalUrl', {
        element(e) {
          e.setAttribute('href', canonical);
        }
      })
      .on('meta#ogTitle', {
        element(e) {
          e.setAttribute('content', safeTitle);
        }
      })
      .on('meta#ogDescription', {
        element(e) {
          e.setAttribute('content', safeDesc);
        }
      })
      .on('meta#ogImage', {
        element(e) {
          e.setAttribute('content', safeImg);
        }
      })
      .on('meta#ogUrl', {
        element(e) {
          e.setAttribute('content', canonical);
        }
      })
      .on('meta#twTitle', {
        element(e) {
          e.setAttribute('content', safeTitle);
        }
      })
      .on('meta#twDescription', {
        element(e) {
          e.setAttribute('content', safeDesc);
        }
      })
      .on('meta#twImage', {
        element(e) {
          e.setAttribute('content', safeImg);
        }
      })
      .on('meta#twUrl', {
        element(e) {
          e.setAttribute('content', canonical);
        }
      })
      .transform(response);
  } catch (err) {
    return await context.env.ASSETS.fetch(context.request);
  }
}
