# How to Work on Tech Boss (imtechboss.com) from Another Device

This guide explains how to quickly set up and publish articles on `imtechboss.com` from a new computer or laptop.

---

## 1. Prerequisites (Install on New Device)
1. **Python 3.10+**: Download from [python.org](https://www.python.org/). (Check the box "Add Python to PATH" during installation).
2. **Node.js LTS**: Download from [nodejs.org](https://nodejs.org/). (Enables `npx wrangler` and IndexNow scripts).
3. **Git**: Download from [git-scm.com](https://git-scm.com/).
4. **Cloudflare Login**: In terminal, run `npx wrangler login` once to authorize Cloudflare Pages deployments for `binodbhatt500k@gmail.com`.

---

## 2. Directory Structure Overview
- `js/data.js` — All 242+ article objects in `initialArticles` array. (HTML body is strictly under key `"content"`).
- `sitemap.xml` — Google & Bing XML sitemap with high-res Unsplash image entries.
- `feed.xml` — RSS 2.0 XML feed.
- `_worker.js` — Cloudflare Edge Worker for dynamic OpenGraph, Twitter cards, and Edge SSR pre-rendering.
- `scripts/` — Automated scripts for validation, publishing, and worker generation.
- `AGENTS.md` / `GEMINI.md` — Mandatory editorial and publishing rules.

---

## 3. Essential Commands Cheat Sheet

### A. Pre-Flight Master Validation (Always run before deploy)
```bash
python scripts/validate_all.py
```
*Validates article schema, "content" key, anti-AI word scan, and XML syntax.*

### B. Regenerate Cloudflare Edge Worker
```bash
python scripts/generate_worker.py
```
*Updates `_worker.js` with SSR data for search engines and social cards.*

### C. Multi-Engine Instant Ping (IndexNow)
```bash
node scripts/ping_indexnow.js
```
*Notifies Bing, Yandex, and Seznam instantly.*

### D. Deploy to Cloudflare Pages
```bash
npx wrangler pages deploy . --project-name imtechboss --commit-dirty=true
```

### E. Sync with GitHub
```bash
git add .
git commit -m "Publish: [Article Title]"
git pull origin main --rebase
git push origin main
```

---

## 4. Key Rules to Remember
- **Images:** Always high-res Unsplash `w=1200`: `https://images.unsplash.com/photo-[ID]?auto=format&fit=crop&w=1200&q=80`
- **Key Name in `data.js`:** Must be `"content"`. The key `"body"` is strictly prohibited.
- **XML Escaping:** All `&` in XML URLs and category tags must be written as `&amp;`.
- **Anti-AI Banned Words:** Strictly avoid *delve, landscape, pivotal, testament, game-changer, in conclusion, tapestries, realm, beacon, seamlessly*.
- **Author:** Always `"Tech Boss"`.
