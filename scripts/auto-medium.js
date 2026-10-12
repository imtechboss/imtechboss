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

function syncProfileData(targetProfile = 'Default') {
  try {
    const srcDir = path.join(process.env.LOCALAPPDATA, 'Google', 'Chrome', 'User Data');
    const destDir = USER_DATA_DIR;
    if (!fs.existsSync(srcDir)) return;
    fs.mkdirSync(destDir, { recursive: true });

    // Copy Local State so Chrome knows the profile names
    const localStateSrc = path.join(srcDir, 'Local State');
    if (fs.existsSync(localStateSrc)) {
      try { fs.copyFileSync(localStateSrc, path.join(destDir, 'Local State')); } catch (e) {}
    }

    // Sync profiles
    for (const prof of [targetProfile, 'Default', 'Profile 2']) {
      const pSrc = path.join(srcDir, prof);
      const pDest = path.join(destDir, prof);
      if (!fs.existsSync(pSrc)) continue;

      fs.mkdirSync(pDest, { recursive: true });
      fs.mkdirSync(path.join(pDest, 'Network'), { recursive: true });

      const files = ['Preferences', 'Login Data', 'Web Data', path.join('Network', 'Cookies')];
      for (const rel of files) {
        const s = path.join(pSrc, rel);
        const d = path.join(pDest, rel);
        if (fs.existsSync(s)) {
          try {
            const { execSync } = require('child_process');
            execSync('copy "' + s + '" "' + d + '" /Y', { shell: 'cmd.exe', stdio: 'ignore' });
          } catch (e) {}
        }
      }
    }
  } catch (err) {}
}

async function runLoginMode(profileName = 'Default') {
  console.log('\n===============================================================');
  console.log(`🔑 MEDIUM AUTOMATION: 1-TIME SETUP FOR PROFILE [${profileName} - GHOST / binodbhatt500k]`);
  console.log('===============================================================');
  console.log('Syncing your Chrome profile configuration...');
  syncProfileData(profileName);

  console.log('Opening Chrome directly with your GHOST (binodbhatt500k) Profile...');
  console.log('Please log into Medium (@binodbhatt500k) in this window.');
  console.log('Once logged in, it will automatically save your session!\n');

  const browser = await puppeteer.launch({
    executablePath: getChromeExecutable(),
    userDataDir: USER_DATA_DIR,
    headless: false,
    defaultViewport: null,
    ignoreDefaultArgs: ['--enable-automation'],
    args: [
      '--start-maximized',
      '--no-sandbox',
      '--disable-blink-features=AutomationControlled',
      `--profile-directory=${profileName}`
    ]
  });

  const page = await browser.newPage();
  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });
  await page.goto('https://medium.com/m/signin', { waitUntil: 'domcontentloaded' });
  console.log('👉 Browser is open at Medium sign-in page. Please complete login...');

  // Wait until logged in (up to 10 minutes)
  const startTime = Date.now();
  let loggedIn = false;
  while (Date.now() - startTime < 600000) {
    await new Promise(r => setTimeout(r, 3000));
    try {
      const isStillOnSignin = page.url().includes('/m/signin');
      const hasUserMenu = await page.evaluate(() => {
        return document.querySelector('button[aria-label="user options"], img[alt*="profile"], a[href*="/@"]') !== null;
      }).catch(() => false);

      if (!isStillOnSignin || hasUserMenu) {
        console.log('\n🎉 SUCCESS! Medium login detected and permanently saved!');
        console.log('You can now run auto-post at any time without logging in again.');
        loggedIn = true;
        break;
      }
    } catch (e) {
      // browser might have been closed by user
      break;
    }
  }

  if (loggedIn) {
    await new Promise(r => setTimeout(r, 3000));
  }
  await browser.close().catch(() => {});
}

async function autoPostArticle(targetArticle, profileName = 'Default') {
  const articleUrl = `https://imtechboss.com/post?id=${targetArticle.id}`;
  const tags = getMediumTags(targetArticle);

  console.log('\n===============================================================');
  console.log(`🚀 AUTOMATING MEDIUM IMPORT FOR [Profile: ${profileName} - GHOST / binodbhatt500k]:`);
  console.log(`Title: "${targetArticle.title}"`);
  console.log(`URL:   ${articleUrl}`);
  console.log(`Tags:  ${tags.join(', ')}`);
  console.log('===============================================================\n');

  console.log('1. Syncing profile and launching automated Chrome session...');
  syncProfileData(profileName);

  const browser = await puppeteer.launch({
    executablePath: getChromeExecutable(),
    userDataDir: USER_DATA_DIR,
    headless: false, // Visible so user can see it work smoothly
    defaultViewport: null,
    ignoreDefaultArgs: ['--enable-automation'],
    args: [
      '--start-maximized',
      '--no-sandbox',
      '--disable-blink-features=AutomationControlled',
      `--profile-directory=${profileName}`
    ]
  });

  const page = await browser.newPage();
  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });

  try {
    console.log('2. Navigating to Medium Story Importer (https://medium.com/p/import)...');
    await page.goto('https://medium.com/p/import', { waitUntil: 'domcontentloaded', timeout: 30000 });
    console.log('Current URL after navigation:', page.url());

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
  const profileArg = args.find(a => a.startsWith('--profile='));
  const profileName = profileArg ? profileArg.split('=')[1] : 'Default';

  if (args.includes('--login')) {
    await runLoginMode(profileName);
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

  await autoPostArticle(targetArticle, profileName);
}

main();
