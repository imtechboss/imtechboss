const fs = require('fs');
const path = require('path');

const dataFile = path.join(__dirname, '..', 'js', 'data.js');
const sitemapFile = path.join(__dirname, '..', 'sitemap.xml');
const feedFile = path.join(__dirname, '..', 'feed.xml');

const newArticle = {
  id: 'nvidia-blackwell-nvl72-racks-liquid-cooling-overheating-hyperscalers-2026',
  title: 'Nvidia Blackwell NVL72 Racks Face Severe Liquid Cooling and Overheating Hurdles in Hyperscaler Cloud Centers',
  excerpt: "Hyperscale cloud providers report unexpected thermal density issues with Nvidia's flagship 120kW NVL72 AI racks. Here is how direct-to-chip liquid cooling and manifold redesigns are altering deployment roadmaps.",
  content: `<p>As hyperscale cloud providers ramp up installations of Nvidia’s flagship Blackwell GB200 NVL72 systems, data center engineers are encountering formidable thermal engineering hurdles. Several enterprise operators have documented recurring overheating incidents during prolonged floating-point stress tests, forcing server designers to modify fluid distribution manifolds and direct-to-chip cooling loops.</p>

<p>The GB200 NVL72 rack represents a monumental leap in concentrated computational power, integrating 72 Blackwell GPUs and 36 Grace CPUs into a single contiguous system functioning as an exascale AI accelerator. However, packing that much computational silicon into an industry-standard 19-inch rack footprint pushes total electrical consumption up to 120 kilowatts per rack—a thermal density four to five times higher than typical enterprise installations.</p>

<h2>The 120kW Thermal Density Challenge</h2>
<p>Traditional air cooling reaches its thermodynamic ceiling around 30 to 40 kilowatts per rack. Beyond that threshold, moving enough air volume requires jet-engine-velocity fans that consume unacceptable amounts of auxiliary power and create extreme acoustic vibrations. The NVL72 was engineered from day one to mandate 100% direct-to-chip (D2C) liquid cooling.</p>

<p>During initial deployment testing across major colocation facilities, engineers observed localized hot spots exceeding thermal throttling thresholds on the inner compute trays. Investigation revealed that the high pressure differential required to circulate coolant across 108 distinct cold plates created micro-cavitation and uneven flow distribution between the top and bottom chassis drawers.</p>

<h2>Redesigning Coolant Distribution Units (CDUs)</h2>
<p>To eliminate these thermal bottlenecks without throttling GPU clock speeds, server vendors and hyperscalers are collaborating with thermal management specialists to implement several critical revisions:</p>
<ul>
  <li><strong>Upgraded Coolant Distribution Units:</strong> Upgrading facility CDUs with variable-speed magnetic-drive pumps capable of sustaining higher volumetric flow rates without exceeding safe pipe pressure boundaries.</li>
  <li><strong>Redesigned Stainless Steel Manifolds:</strong> Replacing standard internal polymer hoses with custom-bent stainless steel manifolds to prevent micro-flexing under high temperature cycles.</li>
  <li><strong>Optimized Micro-Channel Cold Plates:</strong> Refining the copper pin-fin density directly above the dual-die Blackwell reticle to accelerate heat transfer into the treated water-glycol coolant loop.</li>
  <li><strong>Dripless Quick-Disconnects:</strong> Deploying blind-mate quick-disconnect couplings with reinforced O-rings rated for continuous operation at elevated liquid temperatures.</li>
</ul>

<h2>Impact on 2026–2027 AI Infrastructure Rollouts</h2>
<p>While the thermal recalibration has required adjustments to delivery timetables for specific clusters, cloud operators like Microsoft Azure, Amazon Web Services, and specialized AI cloud CoreWeave emphasize that core production shipments remain active. Data center retrofits—including reinforced raised floors to bear the rack's 3,000-pound weight and dedicated facility-loop heat exchangers—are proceeding in parallel.</p>

<p>The situation highlights a fundamental transition in computing: as AI model training demands exponential increases in GPU density, the primary constraints on artificial intelligence progress are shifting from semiconductor lithography to power distribution and thermodynamic heat removal.</p>`,
  category: 'AI & Technology',
  image: 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800',
  author: 'Tech Boss',
  date: '2026-09-24',
  tags: [
    'Nvidia',
    'Blackwell',
    'AI Hardware',
    'Data Centers',
    'Liquid Cooling',
    'Cloud Computing',
    'Semiconductors'
  ],
  readTime: '5 min read',
  featured: true
};

// 1. Update data.js
let dataContent = fs.readFileSync(dataFile, 'utf8');
eval(dataContent);
if (initialArticles.length > 0) {
  initialArticles[0].featured = false;
}
initialArticles.unshift(newArticle);
const updatedData = 'var initialArticles = ' + JSON.stringify(initialArticles, null, 2) + ';\n';
fs.writeFileSync(dataFile, updatedData, 'utf8');
console.log('✅ Updated data.js! Total articles:', initialArticles.length);

// 2. Update sitemap.xml
let sitemapContent = fs.readFileSync(sitemapFile, 'utf8');
const newSitemapEntry = `  <url>
    <loc>https://imtechboss.com/post.html?id=${newArticle.id}</loc>
    <lastmod>2026-09-24</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>\n`;

const sitemapInsertIndex = sitemapContent.indexOf('  <url>\n    <loc>https://imtechboss.com/post.html');
if (sitemapInsertIndex !== -1) {
  sitemapContent = sitemapContent.slice(0, sitemapInsertIndex) + newSitemapEntry + sitemapContent.slice(sitemapInsertIndex);
  fs.writeFileSync(sitemapFile, sitemapContent, 'utf8');
  console.log('✅ Updated sitemap.xml with new entry!');
}

// 3. Update feed.xml
let feedContent = fs.readFileSync(feedFile, 'utf8');
const safeTitle = newArticle.title.replace(/&/g, '&amp;');
const safeExcerpt = newArticle.excerpt.replace(/&/g, '&amp;').replace(/"/g, '&quot;');
const newFeedItem = `    <item>
      <title>${safeTitle}</title>
      <link>https://imtechboss.com/post.html?id=${newArticle.id}</link>
      <guid>https://imtechboss.com/post.html?id=${newArticle.id}</guid>
      <pubDate>Thu, 24 Sep 2026 00:00:00 GMT</pubDate>
      <category>AI &amp; Technology</category>
      <description>&lt;p&gt;&lt;img src="${newArticle.image}" alt="${safeTitle}" /&gt;&lt;/p&gt;&lt;p&gt;${safeExcerpt}&lt;/p&gt;</description>
      <media:content url="${newArticle.image}" medium="image" type="image/jpeg" />
      <media:thumbnail url="${newArticle.image}" />
      <enclosure url="${newArticle.image}" type="image/jpeg" length="102400" />
    </item>\n`;

const feedInsertIndex = feedContent.indexOf('    <item>');
if (feedInsertIndex !== -1) {
  feedContent = feedContent.slice(0, feedInsertIndex) + newFeedItem + feedContent.slice(feedInsertIndex);
  fs.writeFileSync(feedFile, feedContent, 'utf8');
  console.log('✅ Updated feed.xml with new item for Pinterest RSS!');
}
