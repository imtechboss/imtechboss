const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const dataPath = path.join(__dirname, '..', 'js', 'data.js');
const content = fs.readFileSync(dataPath, 'utf8');

const match = content.match(/var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);/);
if (!match) {
  console.error("Could not find initialArticles");
  process.exit(1);
}

const articles = JSON.parse(match[1]);

// Top 5 highest-priority articles for Medium syndication
const prioritySlugs = [
  'how-to-bypass-tpm-2-install-windows-11-unsupported-pc-2026',
  'best-free-vpns-gaming-streaming-no-logs-zero-lag-2026',
  'how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026',
  'how-to-fix-100-percent-memory-disk-leak-windows-11-24h2',
  'oneplus-16-esports-flagship-185hz-amoled-8500mah-silicon-carbon-battery-2026'
];

console.log(`\n===============================================================`);
console.log(`🚀 MEDIUM SYNDICATION HELPER FOR @binodbhatt500k (DA 95 BACKLINKS)`);
console.log(`===============================================================\n`);
console.log(`Medium Importer URL: https://medium.com/p/import\n`);
console.log(`Instructions:`);
console.log(`1. Open https://medium.com/p/import in your browser.`);
console.log(`2. Paste any of the article URLs below into the import box.`);
console.log(`3. Click "Import story". Medium will fetch content and auto-assign canonical backlink to imtechboss.com.`);
console.log(`4. Review formatting and click "Publish".\n`);
console.log(`---------------------------------------------------------------`);
console.log(`TOP PRIORITY ARTICLES READY FOR MEDIUM:`);
console.log(`---------------------------------------------------------------`);

prioritySlugs.forEach((slug, idx) => {
  const art = articles.find(a => a.id === slug);
  if (art) {
    const url = `https://imtechboss.com/post?id=${art.id}`;
    console.log(`\n[${idx + 1}] ${art.title}`);
    console.log(`    🔗 URL: ${url}`);
    console.log(`    🏷️ Recommended Tags: Tech, Windows, Cybersecurity, Gaming, Software`);
  }
});

console.log(`\n===============================================================`);

if (process.argv.includes('--open')) {
  console.log("Opening https://medium.com/p/import in default browser...");
  const cmd = process.platform === 'win32' ? `start https://medium.com/p/import` : `open https://medium.com/p/import`;
  exec(cmd);
}
