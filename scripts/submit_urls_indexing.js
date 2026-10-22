// submit_urls_indexing.js – Push up to 200 URLs to Google Indexing API
// ---------------------------------------------------------------
const fs = require('fs');
const path = require('path');
const { JWT } = require('google-auth-library');

const URLS_FILE = path.resolve(__dirname, '..', 'urls.txt');
const CREDENTIALS_PATH = path.resolve(__dirname, 'credentials.json');
const MAX_BATCH = 200;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function loadUrls() {
  if (!fs.existsSync(URLS_FILE)) {
    console.error(`❌ URLs file not found: ${URLS_FILE}`);
    process.exit(1);
  }
  const raw = fs.readFileSync(URLS_FILE, 'utf8');
  const all = raw
    .split('\n')
    .map(l => l.trim())
    .filter(l => l.length > 0);

  const unique = [];
  const seen = new Set();
  for (const u of all) {
    if (!seen.has(u)) {
      seen.add(u);
      unique.push(u);
    }
  }

  return unique.slice(0, MAX_BATCH);
}

async function main() {
  const urls = loadUrls();
  if (urls.length === 0) {
    console.log('No URLs to submit.');
    return;
  }

  if (!fs.existsSync(CREDENTIALS_PATH)) {
    console.error(`❌ Credentials file not found at: ${CREDENTIALS_PATH}`);
    process.exit(1);
  }

  const key = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
  const client = new JWT({
    email: key.client_email,
    key: key.private_key,
    scopes: ['https://www.googleapis.com/auth/indexing'],
  });

  console.log(`🔑 Authenticating service account: ${key.client_email}`);
  const tokens = await client.authorize();
  console.log(`✅ Authenticated! Starting submission of ${urls.length} URLs to Google Indexing API...\n`);

  let successCount = 0;
  let failCount = 0;
  const results = [];

  for (let i = 0; i < urls.length; i++) {
    const url = urls[i];
    try {
      const res = await fetch('https://indexing.googleapis.com/v3/urlNotifications:publish', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${tokens.access_token}`,
        },
        body: JSON.stringify({
          url: url,
          type: 'URL_UPDATED',
        }),
      });

      const data = await res.json();
      if (res.ok) {
        successCount++;
        console.log(`[${i + 1}/${urls.length}] ✅ Success: ${url}`);
        results.push({ url, status: 'OK' });
      } else {
        failCount++;
        const errMessage = data?.error?.message || res.statusText;
        console.error(`[${i + 1}/${urls.length}] ❌ Failed: ${url} -> ${errMessage}`);
        results.push({ url, status: 'ERROR', message: errMessage });
      }
    } catch (err) {
      failCount++;
      console.error(`[${i + 1}/${urls.length}] ❌ Exception: ${url} -> ${err.message}`);
      results.push({ url, status: 'EXCEPTION', message: err.message });
    }

    // Gentle pacing to prevent rate-limit spikes
    await sleep(60);
  }

  console.log(`\n========================================`);
  console.log(`🎯 SUBMISSION COMPLETED`);
  console.log(`Total: ${urls.length}`);
  console.log(`✅ Successful: ${successCount}`);
  console.log(`❌ Failed: ${failCount}`);
  console.log(`========================================`);

  fs.writeFileSync(
    path.resolve(__dirname, 'submission_report.json'),
    JSON.stringify({ timestamp: new Date().toISOString(), total: urls.length, successCount, failCount, results }, null, 2)
  );
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
