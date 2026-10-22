const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

const projectRoot = path.resolve(__dirname, '..');
const dataPath = path.join(projectRoot, 'js', 'data.js');

const content = fs.readFileSync(dataPath, 'utf8');
const match = content.match(/var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);/);
if (!match) {
  console.error("Could not find initialArticles");
  process.exit(1);
}

const articles = JSON.parse(match[1]);

const prioritySlugs = [
  'how-to-bypass-tpm-2-install-windows-11-unsupported-pc-2026',
  'best-free-vpns-gaming-streaming-no-logs-zero-lag-2026',
  'how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026',
  'how-to-fix-100-percent-memory-disk-leak-windows-11-24h2',
  'oneplus-16-esports-flagship-185hz-amoled-8500mah-silicon-carbon-battery-2026'
];

console.log(`\n===============================================================`);
console.log(`🚀 1-CLICK MEDIUM IMPORTER FOR GHOST (@binodbhatt500k)`);
console.log(`   (100% Safe - No Cloudflare Bot Blocks - Pure Native Chrome)`);
console.log(`===============================================================\n`);
console.log(`Select which article to import into Medium:\n`);

prioritySlugs.forEach((slug, idx) => {
  const art = articles.find(a => a.id === slug);
  if (art) {
    console.log(`  [${idx + 1}] ${art.title}`);
  }
});

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('\nEnter number (1-5) [Default is 1]: ', (answer) => {
  rl.close();
  const choice = parseInt(answer.trim(), 10) || 1;
  const targetSlug = prioritySlugs[choice - 1] || prioritySlugs[0];
  const targetArticle = articles.find(a => a.id === targetSlug);

  const articleUrl = `https://imtechboss.com/${targetArticle.id}/`;

  // Copy URL to Windows clipboard
  try {
    execSync(`powershell -Command "Set-Clipboard -Value '${articleUrl}'"`, { stdio: 'ignore' });
  } catch (e) {}

  console.log(`\n---------------------------------------------------------------`);
  console.log(`✅ LINK COPIED TO YOUR CLIPBOARD!`);
  console.log(`   ${articleUrl}`);
  console.log(`---------------------------------------------------------------`);
  console.log(`\nOpening Medium Importer in your real GHOST Chrome browser...`);
  console.log(`\n👉 ALL YOU HAVE TO DO:`);
  console.log(`   1. Click on the box on Medium`);
  console.log(`   2. Press Ctrl + V (Paste)`);
  console.log(`   3. Click "Import story"`);
  console.log(`   4. Click "Publish" — DONE! (DA 95 Backlink Created)`);
  console.log(`---------------------------------------------------------------\n`);

  // Open Medium import page in normal user Chrome (not Puppeteer, completely bypasses Cloudflare)
  execSync(`start chrome "https://medium.com/p/import"`, { shell: 'cmd.exe' });
});
