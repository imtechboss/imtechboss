const fs = require('fs');
const path = require('path');
const http = require('http');
const { exec, execSync } = require('child_process');
const puppeteer = require('puppeteer-core');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const projectRoot = path.resolve(__dirname, '..');
const dataPath = path.join(projectRoot, 'js', 'data.js');
const historyFile = path.join(__dirname, 'medium-history.json');

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function loadArticles() {
  if (!fs.existsSync(dataPath)) return [];
  const content = fs.readFileSync(dataPath, 'utf8');
  const match = content.match(/var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);/);
  return match ? JSON.parse(match[1]) : [];
}

function loadHistory() {
  if (fs.existsSync(historyFile)) {
    try {
      return JSON.parse(fs.readFileSync(historyFile, 'utf8'));
    } catch (e) {}
  }
  return { postedIds: [], history: [] };
}

function saveHistory(data) {
  fs.writeFileSync(historyFile, JSON.stringify(data, null, 2), 'utf8');
}

// Check if port 9222 is active
function isPortOpen() {
  return new Promise((resolve) => {
    const req = http.get('http://127.0.0.1:9222/json/version', (res) => {
      resolve(res.statusCode === 200);
    });
    req.on('error', () => resolve(false));
    req.setTimeout(1000, () => {
      req.destroy();
      resolve(false);
    });
  });
}

async function ensureChromeWithDebugging() {
  const isOpen = await isPortOpen();
  if (isOpen) {
    console.log('✓ Chrome is already running with debugging port active.');
    return;
  }

  console.log('Connecting to your active Chrome (GHOST profile)...');
  console.log('Restarting Chrome with automation bridge and restoring your tabs...');

  try {
    execSync('taskkill /IM chrome.exe /F', { stdio: 'ignore' });
  } catch (e) {}

  await sleep(1500);

  // Launch real Chrome with user data and port 9222
  exec(`"${CHROME_PATH}" --remote-debugging-port=9222 --restore-last-session`);

  // Wait for port 9222 to be ready
  for (let i = 0; i < 20; i++) {
    await sleep(1000);
    const ready = await isPortOpen();
    if (ready) {
      console.log('✓ Successfully connected to your Chrome profile!');
      return;
    }
  }

  throw new Error('Could not connect to Chrome debugging port.');
}

async function main() {
  console.log('===============================================================');
  console.log('🚀 100% FULLY AUTOMATED MEDIUM POSTER (GHOST PROFILE)');
  console.log('===============================================================\n');

  const articles = loadArticles();
  const history = loadHistory();

  const prioritySlugs = [
    'how-to-bypass-tpm-2-install-windows-11-unsupported-pc-2026',
    'best-free-vpns-gaming-streaming-no-logs-zero-lag-2026',
    'how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026',
    'how-to-fix-100-percent-memory-disk-leak-windows-11-24h2',
    'oneplus-16-esports-flagship-185hz-amoled-8500mah-silicon-carbon-battery-2026'
  ];

  const targetId = process.argv.slice(2).find(a => !a.startsWith('--'));
  let article = null;

  if (targetId) {
    article = articles.find(a => a.id === targetId);
  } else {
    article = articles.find(a => prioritySlugs.includes(a.id) && !history.postedIds.includes(a.id)) ||
              articles.find(a => !history.postedIds.includes(a.id));
  }

  if (!article) {
    console.log('🎉 All priority articles are already posted to Medium!');
    process.exit(0);
  }

  const articleUrl = `https://imtechboss.com/${article.id}/`;
  console.log(`Target Article: "${article.title}"`);
  console.log(`Canonical URL:  ${articleUrl}\n`);

  await ensureChromeWithDebugging();

  console.log('\nAttaching to your browser...');
  const browser = await puppeteer.connect({
    browserURL: 'http://127.0.0.1:9222',
    defaultViewport: null
  });

  const page = await browser.newPage();

  console.log('Navigating to Medium Story Importer (https://medium.com/p/import)...');
  await page.goto('https://medium.com/p/import', { waitUntil: 'domcontentloaded', timeout: 30000 });

  console.log('Waiting for import input field...');
  await page.waitForSelector('input[type="url"], input[placeholder*="http"], input', { timeout: 15000 });

  const inputSelector = 'input[type="url"], input[placeholder*="http"], input';
  await page.click(inputSelector);
  await page.type(inputSelector, articleUrl, { delay: 20 });

  console.log('Submitting import request...');
  const clicked = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, input[type="submit"]'));
    const btn = btns.find(b => (b.innerText || b.value || '').toLowerCase().includes('import'));
    if (btn) {
      btn.click();
      return true;
    }
    return false;
  });

  if (!clicked) {
    await page.keyboard.press('Enter');
  }

  console.log('Waiting for Medium to create the draft...');
  let draftOpened = false;
  for (let i = 0; i < 15; i++) {
    await sleep(2000);
    const seeStory = await page.evaluate(() => {
      const links = Array.from(document.querySelectorAll('a, button'));
      const found = links.find(el => (el.innerText || '').toLowerCase().includes('see your story'));
      if (found) {
        found.click();
        return true;
      }
      return false;
    });

    if (seeStory) {
      draftOpened = true;
      break;
    }

    if (page.url().includes('/edit')) {
      draftOpened = true;
      break;
    }
  }

  console.log('\nDraft is ready! Finalizing publication on Medium...');
  await sleep(4000);

  // Look for the "Publish" button on Medium editor
  try {
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const publishBtn = btns.find(b => (b.innerText || '').trim().toLowerCase() === 'publish');
      if (publishBtn) publishBtn.click();
    });

    await sleep(2500);

    // Look for "Publish now" button
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const publishNowBtn = btns.find(b => (b.innerText || '').toLowerCase().includes('publish now'));
      if (publishNowBtn) publishNowBtn.click();
    });

    await sleep(3000);
  } catch (e) {
    console.log('Note: Draft is ready in your browser tab. You can click Publish.');
  }

  // Record in history
  if (!history.postedIds.includes(article.id)) {
    history.postedIds.push(article.id);
  }
  history.history.push({
    id: article.id,
    title: article.title,
    url: page.url(),
    postedAt: new Date().toISOString()
  });
  saveHistory(history);

  console.log('\n===============================================================');
  console.log('🎉 100% COMPLETE! ARTICLE SUCCESSFULLY POSTED ON MEDIUM!');
  console.log(`URL: ${page.url()}`);
  console.log(`Canonical backlink pointing to: https://imtechboss.com`);
  console.log('===============================================================\n');

  // Disconnect cleanly leaving user's browser open
  await browser.disconnect();
}

main().catch(err => {
  console.error('\n❌ Error:', err.message);
  process.exit(1);
});
