# Project Instructions & Publishing Rules — Tech Boss (imtechboss.com)

This document contains mandatory guidelines and operational rules for developing, writing, and publishing content on `imtechboss.com`.

---

## 1. New Article Publishing Protocol (MANDATORY ORDER)

Whenever a new article is created or published, follow these steps strictly in this exact sequence:

### Step 1: Image Standards
- Always use high-resolution Unsplash images with **1200px crop format**:
  `https://images.unsplash.com/photo-[ID]?auto=format&fit=crop&w=1200&q=80`
- **NEVER** use `?w=800` or low-resolution images. Flipboard, Twitter, Facebook, and Pinterest require high-res images ($\ge 1200\text{px}$) to extract featured cards properly.

### Step 2: Update Codebase Files & Escape XML
1. **`js/data.js`**: Add article to `initialArticles` array at the top.
   - **CRITICAL**: The HTML body MUST be stored under the key **`"content"`** (e.g. `"content": "<h2>...</h2><p>...</p>"`).
   - **STRICTLY PROHIBITED**: NEVER use the key `"body"`. The reader (`post.js`) and Edge SSR (`_worker.js`) require `"content"`.
   - Ensure valid JSON structure, rich formatted HTML, and 1200px image URL.
2. **`feed.xml`**: Add `<item>` with `<media:content>`, `<media:thumbnail>`, and `<enclosure>` using the 1200px image. **MUST escape all `&` as `&amp;` in image and media URLs.**
3. **`sitemap.xml`**: Add `<url>` with current date (`YYYY-MM-DD`). **MUST escape all `&` as `&amp;` in `<image:loc>` and `<loc>` URLs.**
4. **MANDATORY PRE-FLIGHT VALIDATION**: Always run the master automated validator before moving to Step 3:
   ```bash
   python scripts/validate_all.py
   ```
   This validates both article schema/content integrity (`validate_articles.py`) and XML syntax (`validate_xml.py`).
   **DO NOT proceed if validation outputs any error.**

### Step 3: Regenerate Cloudflare Edge Worker
- Always run:
  ```bash
  python scripts/generate_worker.py
  ```
- This updates `_worker.js` with OpenGraph (`og:image`, `og:title`), Twitter card tags, and Edge SSR pre-rendering with full article content.

### Step 4: Multi-Engine Real-Time Indexing (MANDATORY)
- Trigger instant crawler discovery across Google, Microsoft Bing, Yandex, Seznam, and partner engines:
  ```bash
  # Google Instant Indexing API
  node scripts/google_indexing.js
  # Bing & IndexNow Engine Partners
  node scripts/ping_indexnow.js
  ```

### Step 5: Automated Master Pipeline (ONE-COMMAND PUBLISHING)
- Alternatively, run the all-in-one automated pipeline which regenerates sitemap, feed, worker, runs validations, pushes to Google Indexing API + IndexNow, syndicates to DEV.to, broadcasts to Bluesky/Mastodon, and pushes to Git in one command:
  ```bash
  python scripts/publish_pipeline.py
  ```
- Commit and push to Git triggers Cloudflare Pages auto-deploy:
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
- **Author:** Always `"Tech Boss"`.

---

## 4. Zero-Duplicate & Genuine Global News Rule (MANDATORY)
- **Zero Duplicate Policy:** Before writing, cross-reference `js/data.js` and ensure the topic has never been covered on `imtechboss.com`. Duplicate or rehashed articles are strictly prohibited.
- **Genuine Top Worldwide News:** Topics must be grounded in breaking, verified, and high-impact developments in global tech (AI models, semiconductor nodes, GPU/CPU architectures, operating system shifts, cybersecurity).
- **Multi-Engine Indexing:** Every single new article must be submitted to Bing, Yandex, Google, and IndexNow without exception.

---

## 5. Mandatory XML & Sitemap Validation Rule (ZERO ERRORS)
- **XML Ampersand Escaping Rule:** Raw `&` characters are forbidden in any XML attribute or body tag. Every URL containing query parameters (like `?auto=format&fit=crop&w=1200&q=80`) must strictly be written as `?auto=format&amp;fit=crop&amp;w=1200&amp;q=80`.
- **Google Search Console Zero-Error Guarantee:** The sitemap submitted to Google Search Console (`/sitemap.xml`) must at all times remain 100% parseable, well-formed XML with zero unrecognized tokens.

---

## 6. Mandatory Article Schema & Content Integrity Rule (ZERO DEFECTS)
- **Field Name Standard:** Every article object in `js/data.js` MUST use `"content"` for its HTML body text. The key `"body"` is strictly prohibited.
- **Minimum Word Count:** Every article must strictly contain at least 600+ words (no upper limit) of rich technical analysis, detailed specifications, and proper HTML structure (`<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>`, `<blockquote>`). Articles under 600 words are strictly prohibited.
- **No Duplicate Headings/Paragraphs:** Automated validation scans for repeated blocks or duplicate `<h2>` tags. Duplicate content within an article is strictly forbidden.
- **Pre-Flight Master Check:** Execute `python scripts/validate_all.py` before every worker generation and deploy. If it fails, fix the issue immediately before proceeding.
