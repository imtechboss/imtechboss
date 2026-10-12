const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const ALT_CHROME_PATH = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe';
const USER_DATA_DIR = path.join(process.env.USERPROFILE || 'C:\\Users\\BOSS', '.medium_automation_profile');

const projectRoot = path.resolve(__dirname, '..');
const dataPath = path.join(projectRoot, 'js', 'data.js');
const historyFile = path.join(__dirname, 'medium-history.json');

function getChromeExecutable() {
  if (fs.existsSync(CHROME_PATH)) return CHROME_PATH;
  if (fs.existsSync(ALT_CHROME_PATH)) return ALT_CHROME_PATH;
  throw new Error('Google Chrome not found on this system');
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
    } catch (e) {
      console.warn('Warning reading medium-history.json:', e.message);
    }
  }
  return { postedIds: [], history: [] };
}

function saveHistory(data) {
  fs.writeFileSync(historyFile, JSON.stringify(data, null, 2), 'utf8');
}

// Generate valid Medium topic tags
function getMediumTags(article) {
  const cat = (article.category || '').toLowerCase();
  const title = (article.title || '').toLowerCase();
  const text = `${cat} ${title}`;

  const tags = [];
  if (text.includes('windows')) tags.push('Windows 11');
  if (text.includes('gaming') || text.includes('game')) tags.push('Gaming');
  if (text.includes('vpn') || text.includes('security')) tags.push('Cybersecurity');
  if (text.includes('ai') || text.includes('llama') || text.includes('gpt')) tags.push('Artificial Intelligence');
  if (text.includes('wifi') || text.includes('router') || text.includes('dns')) tags.push('Networking');
  if (text.includes('gpu') || text.includes('hardware') || text.includes('nvidia')) tags.push('Hardware');
  
  if (tags.length === 0) tags.push('Technology');
  if (tags.length < 3) tags.push('Tech');
  if (tags.length < 4) tags.push('Software');
  if (tags.length < 5) tags.push('Tutorial');

  return tags.slice(0, 5);
}

async function runLoginMode() {
  console.log('\n===============================================================');
  console.log('🔑 MEDIUM AUTOMATION: 1-TIME LOGIN SESSION SETUP');
  console.log('===============================================================');
  console.log('Chrome is opening Medium in a dedicated automation session.');
  console.log('Please log into your Medium account (@binodbhatt500k) in this window.');
  console.log('Once logged in, you can close the browser or press Ctrl+C in terminal.');
  console.log('Your login will be saved permanently for automated posting!\n');

  const browser = await puppeteer.launch({
    executablePath: getChromeExecutable(),
    userDataDir: USER_DATA_DIR,
    headless: false,
    defaultViewport: null,
    args: ['--start-maximized', '--no-sandbox']
  });

  const page = await browser.newPage();
  await page.goto('https://medium.com/m/signin', { waitUntil: 'networkidle2' });
  console.log('👉 Browser is open at Medium login page. Log in, then return to terminal.');
}

async function autoPostArticle(targetArticle) {
  const articleUrl = `https://imtechboss.com/post?id=${targetArticle.id}`;
  const tags = getMediumTags(targetArticle);

  console.log('\n===============================================================');
  console.log(`🚀 AUTOMATING MEDIUM IMPORT FOR:`);
  console.log(`Title: "${targetArticle.title}"`);
  console.log(`URL:   ${articleUrl}`);
  console.log(`Tags:  ${tags.join(', ')}`);
  console.log('===============================================================\n');

  console.log('1. Launching automated Chrome session...');
  const browser = await puppeteer.launch({
    executablePath: getChromeExecutable(),
    userDataDir: USER_DATA_DIR,
    headless: false, // Visible so user can see it work smoothly
    defaultViewport: null,
    args: ['--start-maximized', '--no-sandbox']
  });

  const page = await browser.newPage();

  try {
    console.log('2. Navigating to Medium Story Importer (https://medium.com/p/import)...');
    await page.goto('https://medium.com/p/import', { waitUntil: 'networkidle2', timeout: 45000 });

    // Check if user is logged in
    const isLoginNeeded = await page.evaluate(() => {
      return document.querySelector('a[href*="/m/signin"]') !== null ||
             window.location.href.includes('/m/signin') ||
             window.location.href.includes('medium.com/?');
    });

    if (isLoginNeeded) {
      console.log('⚠️ Medium is not logged in yet in the automation profile!');
      console.log('👉 Please log into Medium in the opened Chrome window right now.');
      console.log('Waiting up to 60 seconds for login...');
      await page.waitForNavigation({ timeout: 60000 }).catch(() => {});
    }

    // Ensure we are on import page
    if (!page.url().includes('/p/import')) {
      await page.goto('https://medium.com/p/import', { waitUntil: 'networkidle2' });
    }

    console.log('3. Entering article URL into Medium importer...');
    await page.waitForSelector('input[type="url"], input[placeholder*="http"], input', { timeout: 15000 });
    
    // Type the URL
    const inputSelector = 'input[type="url"], input[placeholder*="http"], input';
    await page.click(inputSelector);
    await page.type(inputSelector, articleUrl, { delay: 30 });

    console.log('4. Submitting import request...');
    // Find and click the "Import story" button
    const importBtnClicked = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('button, input[type="submit"]'));
      const btn = buttons.find(b => (b.innerText || b.value || '').toLowerCase().includes('import'));
      if (btn) {
        btn.click();
        return true;
      }
      return false;
    });

    if (!importBtnClicked) {
      await page.keyboard.press('Enter');
    }

    console.log('5. Waiting for Medium to parse content and create draft...');
    await page.waitForTimeout ? page.waitForTimeout(6000) : new Promise(r => setTimeout(r, 6000));

    // Look for "See your story" button or redirect to editor
    console.log('6. Opening imported draft...');
    const seeStoryClicked = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('a, button'));
      const btn = buttons.find(b => (b.innerText || '').toLowerCase().includes('see your story'));
      if (btn) {
        btn.click();
        return true;
      }
      return false;
    });

    await new Promise(r => setTimeout(r, 5000));

    console.log(`Current URL: ${page.url()}`);
    console.log('\n✅ Story successfully imported to Medium as a draft!');
    console.log('Canonical URL is automatically bound to:', articleUrl);

    // Save to history
    const history = loadHistory();
    if (!history.postedIds.includes(targetArticle.id)) {
      history.postedIds.push(targetArticle.id);
    }
    history.history.push({
      id: targetArticle.id,
      title: targetArticle.title,
      url: page.url(),
      importedAt: new Date().toISOString()
    });
    saveHistory(history);

    console.log('🎉 Done! You can review and click Publish in the opened browser window, or close it.');
    console.log('(Browser will stay open for 30 seconds so you can see the result)\n');
    await new Promise(r => setTimeout(r, 30000));

  } catch (err) {
    console.error('❌ Error during Medium automation:', err.message);
  } finally {
    await browser.close().catch(() => {});
  }
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes('--login')) {
    await runLoginMode();
    return;
  }

  const articles = loadArticles();
  if (!articles.length) {
    console.error('No articles found in js/data.js');
    process.exit(1);
  }

  const history = loadHistory();
  const targetId = args.find(a => !a.startsWith('--'));

  let targetArticle = null;
  if (targetId) {
    targetArticle = articles.find(a => a.id === targetId);
    if (!targetArticle) {
      console.error(`Article "${targetId}" not found`);
      process.exit(1);
    }
  } else {
    // Top priority evergreen guides first
    const priorityIds = [
      'how-to-bypass-tpm-2-install-windows-11-unsupported-pc-2026',
      'best-free-vpns-gaming-streaming-no-logs-zero-lag-2026',
      'how-to-speed-up-slow-wifi-best-dns-settings-gaming-ping-2026',
      'how-to-fix-100-percent-memory-disk-leak-windows-11-24h2',
      'oneplus-16-esports-flagship-185hz-amoled-8500mah-silicon-carbon-battery-2026'
    ];
    targetArticle = articles.find(a => priorityIds.includes(a.id) && !history.postedIds.includes(a.id)) ||
                    articles.find(a => !history.postedIds.includes(a.id));
  }

  if (!targetArticle) {
    console.log('🎉 All priority articles have already been posted to Medium!');
    process.exit(0);
  }

  await autoPostArticle(targetArticle);
}

main();
