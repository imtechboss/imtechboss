const fs = require('fs');
const path = require('path');

console.log('==============================================');
console.log('   TECH BOSS FULL PROJECT HEALTH & BUG AUDIT  ');
console.log('==============================================\n');

let totalErrors = 0;
let totalWarnings = 0;

// 1. JS SYNTAX AUDIT
console.log('[1/5] Checking JavaScript Syntax Across Project...');
const jsFiles = [
  'js/app.js', 'js/post.js', 'js/data.js', 'js/pages.js', 'js/vip-drawer.js',
  'scripts/ping_indexnow.js', 'scripts/social-auto-scheduler.js', '_worker.js'
];
jsFiles.forEach(f => {
  if (!fs.existsSync(f)) {
    console.warn(`  ⚠ ${f} does not exist on disk`);
    totalWarnings++;
    return;
  }
  try {
    const code = fs.readFileSync(f, 'utf8');
    if (f === '_worker.js') {
      // ES module syntax check
      new Function(code.replace(/export\s+default\s+/g, 'const __worker_export = '));
      console.log(`  ✓ ${f}: Valid Cloudflare Edge Worker ES Module`);
    } else {
      new Function(code);
      console.log(`  ✓ ${f}: Valid JavaScript`);
    }
  } catch (e) {
    console.error(`  ✗ ${f}: SYNTAX ERROR -> ${e.message}`);
    totalErrors++;
  }
});

// 2. DATA.JS INTEGRITY AUDIT
console.log('\n[2/5] Checking js/data.js Article Database Integrity...');
try {
  const dataContent = fs.readFileSync('js/data.js', 'utf8');
  eval(dataContent);
  if (!Array.isArray(initialArticles)) {
    console.error('  ✗ initialArticles is not an array!');
    totalErrors++;
  } else {
    console.log(`  ✓ initialArticles array found with ${initialArticles.length} articles.`);
    const seenIds = new Set();
    initialArticles.forEach((art, idx) => {
      if (!art.id) {
        console.error(`  ✗ Article at index ${idx} has NO ID!`);
        totalErrors++;
      } else if (seenIds.has(art.id)) {
        console.error(`  ✗ Duplicate article ID: "${art.id}"`);
        totalErrors++;
      } else {
        seenIds.add(art.id);
      }

      if (!art.title || art.title.trim().length === 0) {
        console.error(`  ✗ Article [${art.id}] has empty title!`);
        totalErrors++;
      }
      if (!art.category) {
        console.warn(`  ⚠ Article [${art.id}] missing category`);
        totalWarnings++;
      }
      if (!art.image || !art.image.startsWith('http')) {
        console.warn(`  ⚠ Article [${art.id}] has unusual image URL: ${art.image}`);
        totalWarnings++;
      }
      if (!art.content && !art.excerpt) {
        console.error(`  ✗ Article [${art.id}] has neither content nor excerpt!`);
        totalErrors++;
      }
    });
  }
} catch (e) {
  console.error(`  ✗ Failed to parse data.js: ${e.message}`);
  totalErrors++;
}

// 3. HTML FILES & BROKEN LINK AUDIT
console.log('\n[3/5] Checking HTML Files for Broken Links & Duplicate IDs...');
const htmlFiles = fs.readdirSync('.').filter(f => f.endsWith('.html'));
console.log(`  Found ${htmlFiles.length} HTML files: ${htmlFiles.join(', ')}`);

htmlFiles.forEach(htmlFile => {
  const content = fs.readFileSync(htmlFile, 'utf8');

  // Check duplicate IDs
  const idRegex = /\bid=["']([^"']+)["']/gi;
  const seenIds = new Map();
  let match;
  while ((match = idRegex.exec(content)) !== null) {
    const id = match[1];
    seenIds.set(id, (seenIds.get(id) || 0) + 1);
  }
  for (const [id, count] of seenIds.entries()) {
    if (count > 1) {
      // Ignore adsbygoogle / common third-party if any
      console.warn(`  ⚠ ${htmlFile}: Duplicate id="${id}" (appears ${count} times)`);
      totalWarnings++;
    }
  }

  // Check internal hrefs
  const hrefRegex = /\bhref=["']([^"']+)["']/gi;
  while ((match = hrefRegex.exec(content)) !== null) {
    const fullHref = match[1];
    if (fullHref.startsWith('http://') || fullHref.startsWith('https://') || 
        fullHref.startsWith('mailto:') || fullHref.startsWith('tel:') || 
        fullHref.startsWith('javascript:') || fullHref.startsWith('#') ||
        fullHref.includes('${')) {
      continue;
    }
    let cleanPath = fullHref.split('?')[0].split('#')[0];
    if (!cleanPath || cleanPath === '/') continue;
    if (cleanPath.startsWith('/')) cleanPath = cleanPath.slice(1);
    if (cleanPath.endsWith('/')) {
      if (fs.existsSync(cleanPath) || fs.existsSync(cleanPath + 'index.html')) continue;
    }
    if (!fs.existsSync(cleanPath)) {
      console.warn(`  ⚠ ${htmlFile}: Broken local link href="${fullHref}" -> "${cleanPath}" not found on disk`);
      totalWarnings++;
    }
  }

  // Check internal src attributes
  const srcRegex = /\bsrc=["']([^"']+)["']/gi;
  while ((match = srcRegex.exec(content)) !== null) {
    const src = match[1];
    if (src.startsWith('http://') || src.startsWith('https://') || src.startsWith('data:')) {
      continue;
    }
    const cleanSrc = src.split('?')[0];
    if (!cleanSrc) continue;
    if (!fs.existsSync(cleanSrc)) {
      console.warn(`  ⚠ ${htmlFile}: Broken asset src="${src}" -> "${cleanSrc}" not found on disk`);
      totalWarnings++;
    }
  }
});

// 4. RSS FEED & SITEMAP AUDIT
console.log('\n[4/5] Checking feed.xml & sitemap.xml Consistency...');
try {
  const sitemap = fs.readFileSync('sitemap.xml', 'utf8');
  const feed = fs.readFileSync('feed.xml', 'utf8');
  const sitemapUrls = (sitemap.match(/<loc>/g) || []).length;
  const feedItems = (feed.match(/<item>/g) || []).length;
  console.log(`  ✓ sitemap.xml contains ${sitemapUrls} indexed URLs`);
  console.log(`  ✓ feed.xml contains ${feedItems} RSS feed items`);
} catch (e) {
  console.error(`  ✗ Error inspecting sitemap/feed: ${e.message}`);
  totalErrors++;
}

// 5. PYTHON GENERATOR SCRIPT AUDIT
console.log('\n[5/5] Checking scripts/generate_worker.py...');
if (fs.existsSync('scripts/generate_worker.py')) {
  console.log('  ✓ scripts/generate_worker.py exists');
} else {
  console.error('  ✗ scripts/generate_worker.py missing!');
  totalErrors++;
}

console.log('\n==============================================');
console.log(`AUDIT FINISHED: ${totalErrors} Critical Errors, ${totalWarnings} Warnings`);
console.log('==============================================');
process.exit(totalErrors > 0 ? 1 : 0);
