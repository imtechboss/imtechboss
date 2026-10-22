const fs = require('fs');
const path = require('path');

// Configuration — adjust file paths if your JSON is inside a /data/ folder
const POSTS_FILE = fs.existsSync('./posts.json') ? './posts.json' : (fs.existsSync('./data/posts.json') ? './data/posts.json' : './js/data.js');
const SITEMAP_FILE = './sitemap.xml';
const SITE_URL = 'https://imtechboss.com';

// 1. Exact list of Fake/Speculative Launch Slugs & Duplicate Slugs to Remove
const SLUGS_TO_REMOVE = new Set([
  // Speculative / Fake Official Launch News (AdSense Low-Value Triggers)
  'openai-gpt6-astra-computer-operator-ai-agent-2026',
  'apple-mac-mini-m6-first-2nm-chip-desktop-2026',
  'apple-iphone-18-pro-max-official-review-specs-2026',
  'iphone-18-pro-max-review-2026',
  'iphone-18-pro-max-vs-galaxy-s26-ultra',
  'samsung-galaxy-s26-ultra-review-price-nepal-2026',
  'samsung-galaxy-tab-s12-ultra-plus-launch-dynamic-amoled-galaxy-ai-2026',
  'anthropic-claude-sonnet-5-5-terminal-bench-agentic-coding-enterprise-2026',
  'anthropic-claude-4-5-opus-multi-agent-orchestration-tool-synthesis-2026',
  'openai-launches-dots-autonomous-always-on-personal-ai-assistant-2026',
  'xai-grok-4-7-coding-ai-model-elon-musk-2026',
  'alibaba-zhenwu-v900-china-most-powerful-ai-chip-2026',
  'white-house-super-intelligence-executive-order-national-tech-compact-2026',
  'trump-renames-ai-super-intelligence-un-speech-global-regulations-2026',
  'trump-tv-launch-media-boycott-white-house-2026',
  'openai-agent-breaches-australian-government-health-portal-2026',
  'openai-halts-frontier-model-training-sandbox-isolation-flaw-compute-cluster-2026',
  'cisa-cisco-catalyst-sdwan-zero-day-cve-2026-76504-72-hour-patch-mandate-2026',
  'critical-citrix-netscaler-zero-day-cve-2026-88772-whipshot-malware-2026',
  'apple-j490-smart-home-ai-display-october-13-event-john-ternus-2026',
  'nasa-spacex-crew-13-dragon-grace-iss-launch-october-2026',
  'spacex-starship-flight-14-first-orbital-launch-starlink-v3-2026',
  'amd-surpasses-1-trillion-market-cap-datacenter-ai-surge-2026',

  // Duplicate Cannibalizing Posts (Redirected to Primary Below)
  'nvidia-rubin-r100-gpu-architecture-hbm4-288gb-tsmc-3nm-nvlink-6',
  'google-project-suncatcher-space-based-tpu-satellite-ai-data-center-launch',
  'how-to-run-deepseek-r1-locally-windows-11-ollama-gpu-guide',
  'deepseek-r1-vs-claude-3-7-vs-chatgpt-o3-ai-comparison-2026',
  'claude-vs-chatgpt-vs-deepseek-comparison-2026',
  'how-to-fix-100-percent-disk-usage-windows-11-ssd-sysmain-guide-2026',
  'how-to-fix-slow-wifi-at-home-router-tweaks',
  'gta-6-official-release-date-system-requirements-map-leaks-2026',
  'gta-6-release-date-map-pc-specs-nepal-price',
  'top-5-free-ai-tools-2026',
  'top-10-free-ai-tools-everyone-should-use-2026'
]);

// 2. 301 Redirect Map for Consolidated Duplicate Posts
const REDIRECT_MAP = {
  '/nvidia-rubin-r100-gpu-architecture-hbm4-288gb-tsmc-3nm-nvlink-6/': '/nvidia-rubin-r100-ultra-gpu-architecture-hbm4-cowos-3nm-2026/',
  '/google-project-suncatcher-space-based-tpu-satellite-ai-data-center-launch/': '/google-project-suncatcher-orbital-ai-supercomputer-spacex-trillium-tpu-2026/',
  '/how-to-run-deepseek-r1-locally-windows-11-ollama-gpu-guide/': '/how-to-run-deepseek-r1-locally-offline-ollama-lm-studio-guide-2026/',
  '/deepseek-r1-vs-claude-3-7-vs-chatgpt-o3-ai-comparison-2026/': '/deepseek-r1-vs-openai-o3-vs-claude-3-7-reasoning-models-benchmark-comparison-2026/',
  '/claude-vs-chatgpt-vs-deepseek-comparison-2026/': '/deepseek-r1-vs-openai-o3-vs-claude-3-7-reasoning-models-benchmark-comparison-2026/',
  '/how-to-fix-100-percent-disk-usage-windows-11-ssd-sysmain-guide-2026/': '/how-to-fix-100-percent-memory-disk-leak-windows-11-24h2/',
  '/how-to-fix-slow-wifi-at-home-router-tweaks/': '/how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026/',
  '/gta-6-official-release-date-system-requirements-map-leaks-2026/': '/gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026/',
  '/gta-6-release-date-map-pc-specs-nepal-price/': '/gta-6-pc-system-requirements-ray-tracing-vram-fps-targets-2026/',
  '/top-5-free-ai-tools-2026/': '/top-free-ai-tools-video-voice-generators-2026/',
  '/top-10-free-ai-tools-everyone-should-use-2026/': '/top-free-ai-tools-video-voice-generators-2026/'
};

// 3. Regex Patterns for Boilerplate Topic-Stitching Paragraphs
const BOILERPLATE_PATTERNS = [
  /<p[^>]*>[\s\S]*?78 degrees Celsius[\s\S]*?<\/p>/gi,
  /<li[^>]*>[\s\S]*?78 degrees Celsius[\s\S]*?<\/li>/gi,
  /Maintaining target GPU junction temperatures below 78 degrees Celsius ensures sustained boost clock frequencies during continuous batch runs\.?/gi,
  /<p[^>]*>[\s\S]*?4-bit AWQ[\s\S]*?<\/p>/gi,
  /Quantized weights, such as 4-bit AWQ or 8-bit FP8 representations, significantly reduce memory footprints while preserving empirical task performance across standardized reasoning evaluations\.?/gi,
  /Implementing localized inference pipelines guarantees data sovereignty, removes external API rate limits, and provides predictable execution costs across enterprise software environments\.?/gi,
  /<p[^>]*>[\s\S]*?Implementing localized inference pipelines guarantees data sovereignty[\s\S]*?<\/p>/gi,
  /Implementing industry-standard software engineering practices ensures reliable execution[\s\S]*?workflows\.?/gi,
  /<p[^>]*>[\s\S]*?Implementing industry-standard software engineering practices ensures reliable execution[\s\S]*?<\/p>/gi
];

function cleanPostHtml(html) {
  if (!html) return html;
  let cleaned = html;

  // Strip topic-stitched boilerplate paragraphs
  for (const regex of BOILERPLATE_PATTERNS) {
    cleaned = cleaned.replace(regex, '');
  }

  // Convert any remaining relative or query-based internal links to clean /slug/
  cleaned = cleaned.replace(
    /href=["'](?:\.?\/?)?post(?:\.html)?\?id=([^"']+)["']/gi,
    (_, slug) => {
      const target = REDIRECT_MAP[`/${slug}/`] || `/${slug}/`;
      return `href="${target}"`;
    }
  );

  return cleaned;
}

function runCleanup() {
  if (!fs.existsSync(POSTS_FILE)) {
    console.error(`❌ Could not find ${POSTS_FILE}. Run this script inside your project root folder.`);
    process.exit(1);
  }

  const rawData = fs.readFileSync(POSTS_FILE, 'utf8');
  fs.writeFileSync(POSTS_FILE + '.backup.json', rawData, 'utf8');
  console.log(`✅ Backup created at ${POSTS_FILE}.backup.json`);

  let parsed;
  if (POSTS_FILE.endsWith('.js')) {
    const m = rawData.match(/var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);/);
    parsed = JSON.parse(m[1]);
  } else {
    parsed = JSON.parse(rawData);
  }
  const postsArray = Array.isArray(parsed) ? parsed : (parsed.posts || []);

  const keptPosts = [];
  const removedSlugs = [];

  for (const post of postsArray) {
    const slug = String(post.slug || post.id || '').trim();
    const title = String(post.title || '').toLowerCase();

    // Remove blogger-* legacy posts, blacklisted slugs, or known fake titles
    const isBloggerLegacy = slug.startsWith('blogger-');
    const isBlacklisted = SLUGS_TO_REMOVE.has(slug);
    const isHallucinatedTitle =
      title.includes('gemini 4 argon') ||
      title.includes('fitbit air') ||
      title.includes('oneplus 16') ||
      title.includes('homeview') ||
      title.includes('gpt-6 astra');

    if (isBloggerLegacy || isBlacklisted || isHallucinatedTitle) {
      removedSlugs.push(slug);
      continue;
    }

    // Clean boilerplate text & internal links across all possible content fields
    if (post.content) post.content = cleanPostHtml(post.content);
    if (post.body) post.body = cleanPostHtml(post.body);
    if (post.html) post.html = cleanPostHtml(post.html);

    keptPosts.push(post);
  }

  // Save cleaned posts.json and js/data.js
  const outputJson = Array.isArray(parsed) ? keptPosts : { ...parsed, posts: keptPosts };
  fs.writeFileSync('./posts.json', JSON.stringify(outputJson, null, 2), 'utf8');
  console.log(`✅ Cleaned ./posts.json: Kept ${keptPosts.length} high-value posts, Removed ${removedSlugs.length} low-value/duplicate posts.`);

  if (fs.existsSync('./js/data.js')) {
    fs.writeFileSync('./js/data.js', `var initialArticles = ${JSON.stringify(keptPosts, null, 2)};\n`, 'utf8');
    console.log(`✅ Cleaned ./js/data.js in sync.`);
  }

  // Delete physical static directories for removed posts so they don't stay live or mismatched
  let deletedFolders = 0;
  for (const slug of removedSlugs) {
    if (!slug) continue;
    const folderPath = path.join(process.cwd(), slug);
    if (fs.existsSync(folderPath) && fs.lstatSync(folderPath).isDirectory()) {
      fs.rmSync(folderPath, { recursive: true, force: true });
      deletedFolders++;
    }
  }

  // Also check for any blogger-* directories
  for (const f of fs.readdirSync(process.cwd())) {
    if (f.startsWith('blogger-')) {
      const bPath = path.join(process.cwd(), f);
      if (fs.existsSync(bPath) && fs.lstatSync(bPath).isDirectory()) {
        fs.rmSync(bPath, { recursive: true, force: true });
        deletedFolders++;
      }
    }
  }

  console.log(`🗑️ Deleted ${deletedFolders} static folders of removed/blogger/fake posts.`);

  // Generate clean sitemap.xml
  const today = new Date().toISOString().split('T')[0];
  const staticPages = [
    { loc: `${SITE_URL}/`, priority: '1.0', changefreq: 'daily' },
    { loc: `${SITE_URL}/tools`, priority: '0.9', changefreq: 'weekly' },
    { loc: `${SITE_URL}/compare`, priority: '0.9', changefreq: 'weekly' },
    { loc: `${SITE_URL}/deals`, priority: '0.8', changefreq: 'weekly' },
    { loc: `${SITE_URL}/about`, priority: '0.7', changefreq: 'monthly' },
    { loc: `${SITE_URL}/contact`, priority: '0.7', changefreq: 'monthly' },
    { loc: `${SITE_URL}/privacy`, priority: '0.5', changefreq: 'monthly' },
    { loc: `${SITE_URL}/terms`, priority: '0.5', changefreq: 'monthly' },
    { loc: `${SITE_URL}/disclaimer`, priority: '0.5', changefreq: 'monthly' }
  ];

  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;

  for (const page of staticPages) {
    xml += `  <url>\n    <loc>${page.loc}</loc>\n    <lastmod>${today}</lastmod>\n    <changefreq>${page.changefreq}</changefreq>\n    <priority>${page.priority}</priority>\n  </url>\n`;
  }

  for (const post of keptPosts) {
    const slug = String(post.slug || post.id).trim();
    let lastmod = today;
    if (post.date) {
      const parsedDate = new Date(post.date);
      if (!isNaN(parsedDate.getTime())) {
        lastmod = parsedDate.toISOString().split('T')[0];
      }
    }
    xml += `  <url>\n    <loc>${SITE_URL}/${slug}/</loc>\n    <lastmod>${lastmod}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n`;
  }

  xml += `</urlset>\n`;
  fs.writeFileSync(SITEMAP_FILE, xml, 'utf8');
  console.log(`✅ Generated clean ${SITEMAP_FILE} with ${staticPages.length + keptPosts.length} verified URLs.`);

  // Generate Cloudflare Pages _redirects file for consolidated duplicates
  let redirectsContent = `https://www.imtechboss.com/*  https://imtechboss.com/:splat  301\n`;
  for (const [fromUrl, toUrl] of Object.entries(REDIRECT_MAP)) {
    const fromNoSlash = fromUrl.replace(/\/$/, '');
    redirectsContent += `${fromNoSlash}  ${toUrl}  301\n`;
    redirectsContent += `${fromUrl}*  ${toUrl}  301\n`;
  }
  fs.writeFileSync('./_redirects', redirectsContent, 'utf8');
  console.log(`✅ Created ./_redirects file for 301 duplicate consolidation.`);
}

runCleanup();
