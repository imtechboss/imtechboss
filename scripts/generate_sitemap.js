const fs = require('fs');
const path = require('path');
const vm = require('vm');

const base = 'https://imtechboss.com';
const dataPath = path.join(__dirname, '..', 'js', 'data.js');
const sitemapPath = path.join(__dirname, '..', 'sitemap.xml');
const feedPath = path.join(__dirname, '..', 'feed.xml');

const code = fs.readFileSync(dataPath, 'utf8');
const ctx = {};
vm.runInNewContext(code, ctx);
const articles = ctx.initialArticles || [];

function formatW3CDate(dateStr) {
  if (!dateStr) return new Date().toISOString().split('T')[0];
  
  // If already YYYY-MM-DD
  if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr.trim())) {
    return dateStr.trim();
  }

  const d = new Date(dateStr);
  if (!isNaN(d.getTime())) {
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  return new Date().toISOString().split('T')[0];
}

const today = formatW3CDate(new Date().toISOString());

// 1. Generate strictly compliant sitemap.xml
let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
xml += `  <url>\n    <loc>${base}/</loc>\n    <lastmod>${today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n`;

let validCount = 0;
let invalidCount = 0;

articles.forEach(a => {
  const lastmod = formatW3CDate(a.date);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(lastmod)) {
    invalidCount++;
  } else {
    validCount++;
  }

  // XML escape special characters in loc if needed (standard URL)
  const loc = `${base}/post.html?id=${encodeURIComponent(a.id)}`;
  xml += `  <url>\n    <loc>${base}/post.html?id=${a.id}</loc>\n    <lastmod>${lastmod}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n`;
});

xml += '</urlset>\n';
fs.writeFileSync(sitemapPath, xml, 'utf8');

console.log(`Generated sitemap.xml:`);
console.log(`  Total URLs: ${articles.length + 1}`);
console.log(`  Valid W3C YYYY-MM-DD dates: ${validCount + 1}`);
console.log(`  Invalid dates: ${invalidCount}`);

// 2. Generate feed.xml
const top20 = articles.slice(0, 20);
let rss = '<?xml version="1.0" encoding="UTF-8"?>\n';
rss += '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n';
rss += '  <title>Tech Boss</title>\n';
rss += `  <link>${base}</link>\n`;
rss += '  <description>Latest Technology News, Reviews, AI, Gadgets and Gaming</description>\n';
rss += '  <language>en-us</language>\n';
rss += `  <atom:link href="${base}/feed.xml" rel="self" type="application/rss+xml"/>\n`;

top20.forEach(a => {
  const title = (a.title || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const desc = (a.excerpt || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const cat = (a.category || 'Technology').replace(/&/g, '&amp;');
  const pubDate = new Date(a.date || Date.now()).toUTCString();
  rss += `  <item>\n    <title>${title}</title>\n    <link>${base}/post.html?id=${a.id}</link>\n    <guid>${base}/post.html?id=${a.id}</guid>\n    <pubDate>${pubDate}</pubDate>\n    <description>${desc}</description>\n    <category>${cat}</category>\n  </item>\n`;
});

rss += '</channel>\n</rss>\n';
fs.writeFileSync(feedPath, rss, 'utf8');
console.log(`Generated feed.xml with top ${top20.length} articles`);
