// scripts/submit_sitemap.js — Programmatic Google Search Console & Indexing API Sitemap Submitter
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const baseDir = path.resolve(__dirname, '..');
const possibleKeys = [
  path.join(baseDir, '..', 'google index.json'),
  path.join(baseDir, 'google index.json'),
  path.join(__dirname, 'google index.json')
];

let keyPath = null;
for (const p of possibleKeys) {
  if (fs.existsSync(p)) {
    keyPath = p;
    break;
  }
}

if (!keyPath) {
  console.error('❌ Error: "google index.json" service account key file not found!');
  process.exit(1);
}

const key = JSON.parse(fs.readFileSync(keyPath, 'utf8'));

function base64Url(str) {
  return Buffer.from(str).toString('base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
}

async function getAccessToken(scope) {
  const header = { alg: 'RS256', typ: 'JWT' };
  const now = Math.floor(Date.now() / 1000);
  const claim = {
    iss: key.client_email,
    scope: scope,
    aud: 'https://oauth2.googleapis.com/token',
    exp: now + 3600,
    iat: now
  };

  const encodedHeader = base64Url(JSON.stringify(header));
  const encodedClaim = base64Url(JSON.stringify(claim));
  const signInput = `${encodedHeader}.${encodedClaim}`;

  const signer = crypto.createSign('RSA-SHA256');
  signer.update(signInput);
  const signature = signer.sign(key.private_key, 'base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
  const jwt = `${signInput}.${signature}`;

  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'grant_type=' + encodeURIComponent('urn:ietf:params:oauth:grant-type:jwt-bearer') + '&assertion=' + encodeURIComponent(jwt)
  });

  const data = await res.json();
  if (!data.access_token) {
    throw new Error('Failed to obtain token: ' + JSON.stringify(data));
  }
  return data.access_token;
}

async function main() {
  console.log('🚀 Service Account:', key.client_email);

  // 1. Google Search Console API Submission
  console.log('\n--- 1. Submitting to Google Search Console API ---');
  try {
    const gscToken = await getAccessToken('https://www.googleapis.com/auth/webmasters');
    const siteUrl = 'https://imtechboss.com/';
    const sitemaps = [
      'https://imtechboss.com/sitemap.xml',
      'https://imtechboss.com/feed.xml'
    ];

    for (const sm of sitemaps) {
      const submitUrl = `https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(siteUrl)}/sitemaps/${encodeURIComponent(sm)}`;
      const subRes = await fetch(submitUrl, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${gscToken}` }
      });
      if (subRes.status === 204 || (subRes.status >= 200 && subRes.status < 300)) {
        console.log(`✅ Google Search Console: ${sm} successfully submitted!`);
      } else {
        const errText = await subRes.text();
        console.log(`⚠️ GSC Status ${subRes.status}: ${errText}`);
      }
    }
  } catch (err) {
    console.error('❌ GSC API Error:', err.message);
  }

  // 2. Google Instant Indexing API Submission
  console.log('\n--- 2. Submitting to Google Instant Indexing API ---');
  try {
    const idxToken = await getAccessToken('https://www.googleapis.com/auth/indexing');
    const targets = [
      'https://imtechboss.com/sitemap.xml',
      'https://imtechboss.com/feed.xml'
    ];
    for (const target of targets) {
      const res = await fetch('https://indexing.googleapis.com/v3/urlNotifications:publish', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idxToken}`
        },
        body: JSON.stringify({
          url: target,
          type: 'URL_UPDATED'
        })
      });
      if (res.status === 200) {
        console.log(`✅ Instant Indexing API: ${target} notified!`);
      } else {
        const err = await res.json();
        console.log(`⚠️ Indexing Status ${res.status}:`, err);
      }
    }
  } catch (err) {
    console.error('❌ Indexing API Error:', err.message);
  }

  // 3. Query GSC Sitemaps Status
  console.log('\n--- 3. Verifying Live Sitemaps in Google Search Console ---');
  try {
    const gscToken = await getAccessToken('https://www.googleapis.com/auth/webmasters');
    const smRes = await fetch('https://www.googleapis.com/webmasters/v3/sites/' + encodeURIComponent('https://imtechboss.com/') + '/sitemaps', {
      headers: { Authorization: `Bearer ${gscToken}` }
    });
    const smData = await smRes.json();
    if (smData.sitemap) {
      for (const sm of smData.sitemap) {
        console.log(`📌 ${sm.path}`);
        console.log(`   Type: ${sm.type} | Last Downloaded: ${sm.lastDownloaded}`);
        console.log(`   Errors: ${sm.errors} | Warnings: ${sm.warnings} | Pending: ${sm.isPending}`);
      }
    }
  } catch (err) {
    console.error('❌ Query GSC Status Error:', err.message);
  }
}

main();
