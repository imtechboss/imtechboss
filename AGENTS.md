# Project Instructions & Publishing Rules — Tech Boss (imtechboss.com)

This document contains mandatory guidelines and operational rules for developing, writing, and publishing content on `imtechboss.com`.

---

## 1. New Article Publishing Protocol (MANDATORY ORDER)

Whenever a new article is created or published, follow these steps strictly in this exact sequence:

### Step 1: Image Standards
- Always use high-resolution Unsplash images with **1200px crop format**:
  `https://images.unsplash.com/photo-[ID]?auto=format&fit=crop&w=1200&q=80`
- **NEVER** use `?w=800` or low-resolution images. Flipboard, Twitter, Facebook, and Pinterest require high-res images ($\ge 1200\text{px}$) to extract featured cards properly.

### Step 2: Update Codebase Files
1. **`js/data.js`**: Add article to `initialArticles` array at the top. Ensure valid JSON structure, rich formatted HTML body, and 1200px image URL.
2. **`feed.xml`**: Add `<item>` with `<media:content>`, `<media:thumbnail>`, and `<enclosure>` using the 1200px image.
3. **`sitemap.xml`**: Add `<url>` with current date (`YYYY-MM-DD`).

### Step 3: Regenerate Cloudflare Edge Worker
- Always run:
  ```bash
  python scripts/generate_worker.py
  ```
- This updates `_worker.js` with OpenGraph (`og:image`, `og:title`), Twitter card tags, and the high-res `<img class="flipboard-image" width="1200" height="900" ... />` tag.

### Step 4: Multi-Engine Real-Time Indexing (MANDATORY)
- Always ping IndexNow immediately after publishing to trigger instant crawler discovery across Microsoft Bing, Yandex, Seznam, and partner engines:
  ```bash
  node scripts/ping_indexnow.js
  ```

### Step 5: Deploy BEFORE Sharing (Critical)
- **NEVER share to Flipboard or social media before deploying.** (If Flipboard crawls before the worker is deployed, it permanently caches the fallback logo).
- Deploy immediately to Cloudflare Pages:
  ```bash
  npx wrangler@3 pages deploy . --project-name imtechboss
  ```
- Commit and push to Git:
  ```bash
  git add .
  git commit -m "Publish: [Article Title]"
  git push origin main
  ```

---

## 2. Social Sharing & Flipboard Protocol
- **Flipboard Bookmarklet / Share Button URL Pattern:**
  `https://share.flipboard.com/bookmarklet/popout?v=2&title=${encodeURIComponent(article.title)}&url=${encodeURIComponent('https://imtechboss.com/post.html?id=' + article.id + '&flip=1')}`
- Only share or flip **after** `npx wrangler@3 pages deploy` reports `✨ Deployment complete`.

---

## 3. Writing Quality & Editorial Guidelines
- **Anti-AI Detection Rules:** Strictly NEVER use AI clichés:
  - Banned words: *delve, landscape, pivotal, testament, game-changer, in conclusion, tapestries, realm, beacon, seamlessly*.
- **Tone:** Authoritative, direct, fast-paced technical journalism.
- **Language:** English for article content; Romanized Nepali for communication with the publisher (Binod Bhatt).

---

## 4. Zero-Duplicate & Genuine Global News Rule (MANDATORY)
- **Zero Duplicate Policy:** Before writing, cross-reference `js/data.js` and ensure the topic has never been covered on `imtechboss.com`. Duplicate or rehashed articles are strictly prohibited.
- **Genuine Top Worldwide News:** Topics must be grounded in breaking, verified, and high-impact developments in global tech (AI models, semiconductor nodes, GPU/CPU architectures, operating system shifts, cybersecurity).
- **Multi-Engine Indexing:** Every single new article must be submitted to Bing, Yandex, Google, and IndexNow without exception.
