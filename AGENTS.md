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
1. **`js/data.js` & `posts.json`**: Add article to both data files simultaneously.
   - **CRITICAL**: The HTML body MUST be stored under the key **`"content"`** (e.g. `"content": "<h2>...</h2><p>...</p>"`).
   - **STRICTLY PROHIBITED**: NEVER use the key `"body"`. The reader (`post.js`) and Edge SSR (`_worker.js`) require `"content"`.
   - Ensure valid JSON structure, rich formatted HTML, and 1200px image URL.
2. **`feed.xml`**: Add `<item>` with `<media:content>`, `<media:thumbnail>`, and `<enclosure>` using the 1200px image. **MUST escape all `&` as `&amp;` in image and media URLs.**
3. **`sitemap.xml`**: Add `<url>` with current date (`YYYY-MM-DD`). **MUST escape all `&` as `&amp;` in `<image:loc>` and `<loc>` URLs.**
4. **MANDATORY PRE-FLIGHT VALIDATION**: Always run the master automated validator before moving to Step 3:
   ```bash
   python scripts/validate_all.py
   ```
   This validates article schema, anti-AI tone, XML syntax, and complete site health.
   **DO NOT proceed if validation outputs any error.**

### Step 3: Regenerate Static Directories & Cloudflare Edge Worker
- Always run:
  ```bash
  python scripts/build_static.py
  ```
- This updates all static folders `/<slug>/index.html`, homepage `index.html`, and `_worker.js` with OpenGraph metadata, Twitter cards, and Edge SSR pre-rendering.

### Step 4: Multi-Engine Real-Time Indexing (MANDATORY)
- Trigger instant crawler discovery across Google, Microsoft Bing, Yandex, Seznam, and partner engines:
  ```bash
  # Google Instant Indexing API
  node scripts/google_indexing.js
  # Bing & IndexNow Engine Partners
  node scripts/ping_indexnow.js
  ```

### Step 5: Automated Master Pipeline (ONE-COMMAND PUBLISHING)
- Alternatively, run the all-in-one automated pipeline which regenerates static pages, sitemap, feed, worker, runs validations, pushes to Google Indexing API + IndexNow, syndicates to DEV.to, broadcasts to Bluesky/Mastodon, and pushes to Git in one command:
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
- **Clean Permalinks Only:** All social sharing and Flipboard links must use clean permalinks:
  `https://share.flipboard.com/bookmarklet/popout?v=2&title=${encodeURIComponent(article.title)}&url=${encodeURIComponent('https://imtechboss.com/' + article.id + '/')}`
- Strictly **NEVER** use legacy query parameters like `post.html?id=` in share URLs.
- Only share or flip **after** Cloudflare Pages deployment is complete and verified live.

---

## 3. Writing Quality & Editorial Guidelines
- **Anti-AI Detection Rules:** Strictly NEVER use AI clichés:
  - Banned words: *delve, landscape, pivotal, testament, game-changer, in conclusion, tapestries, realm, beacon, seamlessly*.
- **Tone:** Authoritative, direct, fast-paced technical journalism.
- **Language:** English for article content; Romanized Nepali for communication with the publisher (Binod Bhatt).
- **Author:** Always `"Tech Boss"`.

---

## 4. Zero-Duplicate & Genuine Global News Rule (MANDATORY)
- **Zero Duplicate Policy:** Before writing, cross-reference `js/data.js` and `posts.json` and ensure the topic has never been covered on `imtechboss.com`. Duplicate or rehashed articles are strictly prohibited.
- **Genuine Top Worldwide News:** Topics must be grounded in breaking, verified, and high-impact developments in global tech (AI models, semiconductor nodes, GPU/CPU architectures, operating system shifts, cybersecurity).
- **Multi-Engine Indexing:** Every single new article must be submitted to Bing, Yandex, Google, and IndexNow without exception.

---

## 5. Mandatory XML & Sitemap Validation Rule (ZERO ERRORS)
- **XML Ampersand Escaping Rule:** Raw `&` characters are forbidden in any XML attribute or body tag. Every URL containing query parameters must strictly be written as `?auto=format&amp;fit=crop&amp;w=1200&amp;q=80`.
- **Google Search Console Zero-Error Guarantee:** The sitemap submitted to Google Search Console (`/sitemap.xml`) must at all times remain 100% parseable, well-formed XML with zero unrecognized tokens.

---

## 6. Mandatory Article Schema & Content Integrity Rule (ZERO DEFECTS)
- **Field Name Standard:** Every article object in `js/data.js` and `posts.json` MUST use `"content"` for its HTML body text. The key `"body"` is strictly prohibited.
- **Minimum Word Count:** Every new article must strictly contain at least 600+ words (target 800-1100 words) of rich technical analysis, detailed specifications, benchmark tables, and proper HTML structure (`<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>`, `<blockquote>`).
- **No Duplicate Headings/Paragraphs:** Duplicate headings or repeated paragraphs within an article are strictly forbidden.
- **Pre-Flight Master Check:** Execute `python scripts/validate_all.py` before every worker generation and deploy. If it fails, fix the issue immediately before proceeding.

---

## 7. Zero Orphan Comments & Clean HTML Standard (MANDATORY)
- **Zero Stray Comments:** Orphaned or broken HTML comment closing tags (`-->`) are strictly prohibited in `post.html`, `index.html`, `tools.html`, and `scripts/build_static.py`.
- **Automated Check:** `scripts/validate_site_health.py` automatically scans all templates and article pages to guarantee zero visible comment leaks.

---

## 8. Canonical Clean URLs & Duplicate Routing Shield
- **Canonical Structure:** Every article must have a self-referencing canonical tag pointing strictly to `https://imtechboss.com/{slug}/` (with trailing slash).
- **No Query Indexing:** Legacy query routes (`/post?id=...`, `/post.html?id=...`) must return a `301 Moved Permanently` to `/{slug}/` and serve `X-Robots-Tag: noindex, follow`.
- **Robots Directives:** `robots.txt` must disallow administrative endpoints (`/admin`, `/admin.html`).

---

## 9. Category-Aware FAQ Isolation & Anti-Boilerplate Standard
- **Dedicated FAQ Categorization:** FAQs must strictly correspond to the article topic:
  - Cybersecurity & Privacy: Client-side AES-256 encryption, zero-knowledge vault security, recovery keys.
  - Hardware & GPUs: Power supplies (ATX 3.1, 12V-2x6), PCIe bandwidth, memory thermals.
  - AI & Machine Learning: VRAM sizing, quantization (GGUF 4-bit/8-bit), local inference (Ollama), private telemetry.
  - Gaming & Consoles: Target FPS, backward compatibility, DirectStorage NVMe speed.
- **Forbidden Boilerplate:** Generic Windows 11 kernel text or VRAM headings must NEVER be injected into non-Windows or non-hardware articles.

---

## 10. Interactive Tools State Synchronization Standard
- **Hidden Default Results:** On `/tools`, interactive result containers (`#bottleneckResult`, `#quizResultBox`, `#gameCheckResult`, `#llmResultCard`) must start with class `hidden` on initial page load.
- **Dynamic Calculation:** Metrics and hardware recommendations are computed and revealed only when the user clicks the action button or modifies dropdowns. This ensures search engine crawlers never index mismatched static defaults.

---

## 11. Crawler-Shielded UI Standard
- **Snippet Shields:** All modal close buttons (`&times;`, `✕`) and toast notification containers (`#toastNotification`) must be wrapped with `data-nosnippet` and `aria-hidden="true"`.
- This ensures search engine crawlers (Googlebot, Bingbot) never extract decorative UI symbols or temporary action toasts as snippet text.

---

## 12. Single Source of Truth & Zero One-Off Scripts
- **Unified Data Stores:** `posts.json` and `js/data.js` must remain in 100% synchronization at all times.
- **No Standalone Publishing Scripts:** Never create or run isolated one-off publishing scripts that bypass `scripts/publish_pipeline.py` and `scripts/build_static.py`. All updates must flow through the standardized pipeline.
