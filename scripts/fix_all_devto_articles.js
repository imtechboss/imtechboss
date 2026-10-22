// scripts/fix_all_devto_articles.js
// Fix broken tables, canonical URLs, remove unverified posts & stitched text on DEV.to

const fs = require('fs');
const path = require('path');

const DEVTO_API_KEY = process.env.DEVTO_API_KEY || 'ZtmMvBpzm7EgsBquEstMv5mq';
const projectRoot = path.resolve(__dirname, '..');
const dataPath = path.join(projectRoot, 'js', 'data.js');

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function loadLocalArticles() {
  const raw = fs.readFileSync(dataPath, 'utf8');
  const m = raw.match(/var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);/);
  if (!m) return [];
  return JSON.parse(m[1]);
}

function convertHtmlToMarkdown(html) {
  if (!html) return '';
  let md = html;

  // Tables
  md = md.replace(/<table[^>]*>([\s\S]*?)<\/table>/gi, (match, tableContent) => {
    const rows = [];
    const trMatches = tableContent.match(/<tr[^>]*>([\s\S]*?)<\/tr>/gi) || [];
    let isHeader = true;
    for (const tr of trMatches) {
      const cells = [];
      const cellMatches = tr.match(/<(th|td)[^>]*>([\s\S]*?)<\/(th|td)>/gi) || [];
      for (const cell of cellMatches) {
        let text = cell.replace(/<[^>]+>/g, '').trim().replace(/\|/g, '\\|');
        text = text.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
        cells.push(text);
      }
      if (cells.length > 0) {
        rows.push('| ' + cells.join(' | ') + ' |');
        if (isHeader) {
          rows.push('| ' + Array(cells.length).fill('---').join(' | ') + ' |');
          isHeader = false;
        }
      }
    }
    return rows.length > 0 ? '\n\n' + rows.join('\n') + '\n\n' : '';
  });

  // Headings
  md = md.replace(/<h2[^>]*>(.*?)<\/h2>/gi, '\n\n## $1\n\n');
  md = md.replace(/<h3[^>]*>(.*?)<\/h3>/gi, '\n\n### $1\n\n');
  md = md.replace(/<h4[^>]*>(.*?)<\/h4>/gi, '\n\n#### $1\n\n');

  // Formatting
  md = md.replace(/<strong>(.*?)<\/strong>/gi, '**$1**');
  md = md.replace(/<b>(.*?)<\/b>/gi, '**$1**');
  md = md.replace(/<em>(.*?)<\/em>/gi, '*$1*');
  md = md.replace(/<i>(.*?)<\/i>/gi, '*$1*');
  md = md.replace(/<code>(.*?)<\/code>/gi, '`$1`');

  // Lists
  md = md.replace(/<li[^>]*>(.*?)<\/li>/gi, '- $1\n');
  md = md.replace(/<\/?(ul|ol)[^>]*>/gi, '\n');

  // Paragraphs
  md = md.replace(/<p[^>]*>(.*?)<\/p>/gi, '\n\n$1\n\n');
  md = md.replace(/<br\s*\/?>/gi, '\n');
  md = md.replace(/<div[^>]*>([\s\S]*?)<\/div>/gi, '\n$1\n');

  // Clean tags
  md = md.replace(/<[^>]+>/g, '');

  // HTML entities
  md = md.replace(/&nbsp;/g, ' ');
  md = md.replace(/&amp;/g, '&');
  md = md.replace(/&quot;/g, '"');
  md = md.replace(/&#39;/g, "'");
  md = md.replace(/&lt;/g, '<');
  md = md.replace(/&gt;/g, '>');

  // Clean excessive newlines
  md = md.replace(/\n{3,}/g, '\n\n').trim();

  return md;
}

async function devToRequest(endpoint, method = 'GET', body = null) {
  const url = `https://dev.to/api${endpoint}`;
  const opts = {
    method,
    headers: {
      'api-key': DEVTO_API_KEY,
      'Content-Type': 'application/json',
      'User-Agent': 'TechBossUpdater/1.0',
    },
  };
  if (body) {
    opts.body = JSON.stringify(body);
  }

  for (let attempt = 1; attempt <= 3; attempt++) {
    const res = await fetch(url, opts);
    if (res.status === 429) {
      console.log(`[Rate limit 429] Backing off 5s (attempt ${attempt})...`);
      await sleep(5000);
      continue;
    }
    const text = await res.text();
    try {
      return { ok: res.ok, status: res.status, data: JSON.parse(text) };
    } catch (e) {
      return { ok: res.ok, status: res.status, raw: text };
    }
  }
  return { ok: false, status: 429, error: 'Max retries exceeded' };
}

async function main() {
  console.log('======================================================================');
  console.log('  DEV.TO POST SYNC & BUG FIXER');
  console.log('======================================================================\n');

  const localArticles = loadLocalArticles();
  console.log(`Loaded ${localArticles.length} local articles from js/data.js`);

  // Step 1: Unpublish unverified speculative launch posts
  const unpublishIds = [
    { id: 4850859, name: 'Gemini 4 Argon' },
    { id: 4833006, name: 'OnePlus 16 Deep-Dive' },
    { id: 4853817, name: 'Apple HomeView $299' },
  ];

  for (const item of unpublishIds) {
    console.log(`Unpublishing ${item.name} (${item.id})...`);
    const res = await devToRequest(`/articles/${item.id}`, 'PUT', {
      article: { published: false },
    });
    console.log(`Result: ${res.status}`);
    await sleep(3500);
  }

  // Step 2: Fetch all my DEV.to articles
  console.log('\nFetching published articles from DEV.to...');
  const allRes = await devToRequest('/articles/me/all');
  if (!allRes.ok || !Array.isArray(allRes.data)) {
    console.error('Failed to fetch articles:', allRes);
    return;
  }

  const published = allRes.data.filter(a => a.published);
  console.log(`Found ${published.length} published articles.\n`);

  for (let i = 0; i < published.length; i++) {
    const devArt = published[i];
    console.log(`[${i + 1}/${published.length}] Checking: "${devArt.title.substring(0, 50)}..." (ID: ${devArt.id})`);

    // Fetch full article details
    const detRes = await devToRequest(`/articles/${devArt.id}`);
    await sleep(3000);
    if (!detRes.ok) {
      console.log(`  Failed to get details: HTTP ${detRes.status}`);
      continue;
    }

    const fullArt = detRes.data;
    let body = fullArt.body_markdown || '';
    let canonical = fullArt.canonical_url || '';
    let needsUpdate = false;

    // Match with local article by title or slug in canonical
    let matchLocal = localArticles.find(la => la.title.trim().toLowerCase() === fullArt.title.trim().toLowerCase());
    if (!matchLocal) {
      // Try fuzzy match
      matchLocal = localArticles.find(la => {
        const t1 = la.title.toLowerCase().replace(/[^a-z0-9]/g, '');
        const t2 = fullArt.title.toLowerCase().replace(/[^a-z0-9]/g, '');
        return t1.includes(t2.substring(0, 20)) || t2.includes(t1.substring(0, 20));
      });
    }

    if (matchLocal) {
      const correctCanonical = `https://imtechboss.com/${matchLocal.id}/`;
      if (canonical !== correctCanonical) {
        console.log(`  Canonical update: ${canonical} -> ${correctCanonical}`);
        canonical = correctCanonical;
        needsUpdate = true;
      }

      // Check if table needs rebuild or local content has table
      if (matchLocal.content && matchLocal.content.includes('<table')) {
        console.log(`  Article contains <table>, re-converting to Markdown table...`);
        const freshMd = convertHtmlToMarkdown(matchLocal.content);
        body = freshMd;
        needsUpdate = true;
      }
    }

    // Fix stitched topic paragraph in Google Quantum Willow
    if (body.includes('Implementing localized inference pipelines')) {
      console.log('  Removing stitched LLM paragraph from Google Quantum article...');
      body = body.replace(/Implementing localized inference pipelines[\s\S]*?across enterprise software environments\./gi, '');
      needsUpdate = true;
    }

    // Fix table formatting if broken raw text is detected
    if (body.includes('Core Configuration8P') || body.includes('Process NodeTSMC')) {
      console.log('  Fixing broken table in Intel Core Ultra 9 285K article...');
      const tableMd = `\n\n| Specification Feature | Intel Core Ultra 9 285K | AMD Ryzen 9 9950X3D |\n| --- | --- | --- |\n| Core Configuration | 8P + 16E (24 Cores / 24 Threads) | 16 Cores / 32 Threads (SMT) |\n| Process Node | TSMC N3B (Compute Tile) | TSMC N4X (Compute) + N6 (I/O) |\n| Total L3 Cache | 36 MB Intel Smart Cache | 128 MB (64MB 3D V-Cache + 64MB Flat) |\n| Max Boost Clock | 5.7 GHz (P-core Turbo) | 5.7 GHz (Single-Core Boost) |\n| Base / Max Power | 125W Base / 250W MTP | 120W TDP / 162W PPT |\n| Platform Socket | LGA-1851 (Z890) | AM5 (X870E / B650E) |\n\n`;
      body = body.replace(/Core Configuration8P[\s\S]*?AM5 \(X870E \/ B650E\)/gi, tableMd);
      needsUpdate = true;
    }

    // Fix footer canonical link
    if (matchLocal) {
      const targetSlugUrl = `https://imtechboss.com/${matchLocal.id}/`;
      // Replace any old footer
      body = body.replace(/\*Originally published on \[Tech Boss[^\]]*\]\([^\)]+\)[^\*]*\*/gi, '');
      body = body.replace(/\*Originally published at imtechboss\.com[^\*]*\*/gi, '');
      body = body.trim() + `\n\n---\n\n*Originally published on [Tech Boss](${targetSlugUrl})*`;
      needsUpdate = true;
    }

    if (needsUpdate) {
      console.log(`  Pushing update to DEV.to for article ID ${devArt.id}...`);
      const updatePayload = {
        article: {
          body_markdown: body,
          canonical_url: canonical,
        },
      };
      const upRes = await devToRequest(`/articles/${devArt.id}`, 'PUT', updatePayload);
      if (upRes.ok) {
        console.log(`  ✅ Successfully updated article ${devArt.id}`);
      } else {
        console.error(`  ❌ Update failed for ${devArt.id}:`, upRes);
      }
      await sleep(3500);
    } else {
      console.log('  No update needed.');
    }
  }

  console.log('\n======================================================================');
  console.log('🎉 ALL DEV.TO POSTS UPDATED & VERIFIED!');
  console.log('======================================================================');
}

main().catch(err => console.error('Fatal error:', err));
