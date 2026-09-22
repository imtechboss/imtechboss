const fs = require('fs');
const path = require('path');

const { initialArticles } = require('../js/data.js');
const articles = initialArticles || [];

const baseUrl = 'https://imtechboss.com';
const today = new Date().toISOString().split('T')[0];

let xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Core Site Pages -->
  <url>
    <loc>${baseUrl}/</loc>
    <lastmod>${today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>${baseUrl}/index.html</loc>
    <lastmod>${today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
`;

articles.forEach(art => {
  let dateStr = today;
  if (art.timestamp) {
    try {
      dateStr = new Date(art.timestamp).toISOString().split('T')[0];
    } catch (e) {
      dateStr = today;
    }
  }
  const cleanId = encodeURIComponent(art.id);
  xml += `  <url>
    <loc>${baseUrl}/post.html?id=${cleanId}</loc>
    <lastmod>${dateStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>\n`;
});

xml += `</urlset>\n`;

const sitemapPath = path.join(__dirname, '..', 'sitemap.xml');
fs.writeFileSync(sitemapPath, xml, 'utf8');
console.log(`Successfully generated sitemap.xml with ${articles.length + 2} URLs.`);
