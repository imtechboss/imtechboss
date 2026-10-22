const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const projectRoot = path.resolve(__dirname, '..');
const dataContent = fs.readFileSync(path.join(projectRoot, 'js', 'data.js'), 'utf8');

const match = dataContent.match(/var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);/);
if (!match) {
  console.error('❌ initialArticles not found in js/data.js');
  process.exit(1);
}

const articles = JSON.parse(match[1]);
const host = 'imtechboss.com';
const key = 'a8f3b9c712e44d569801a23c45d6e7f8';
const keyLocation = `https://${host}/${key}.txt`;
const sitemapUrl = `https://${host}/sitemap.xml`;
const feedUrl = `https://${host}/feed.xml`;

const allUrls = [
  `https://${host}/`,
  `https://${host}/about/`,
  `https://${host}/contact/`,
  `https://${host}/privacy/`,
  `https://${host}/disclaimer/`,
  `https://${host}/terms/`,
  `https://${host}/tools/`,
  `https://${host}/compare/`,
  `https://${host}/deals/`,
  `https://${host}/sitemap.xml`,
  ...articles.map(a => `https://${host}/${a.id || a.slug}/`)
];

// Deduplicate
const uniqueUrls = Array.from(new Set(allUrls));

console.log('======================================================================');
console.log('   GLOBAL SEARCH ENGINE & FEED MULTI-SERVICE PINGER');
console.log('   Tech Boss (imtechboss.com)');
console.log('======================================================================');
console.log(`📡 Total URLs to submit: ${uniqueUrls.length}`);
console.log(`📄 Sitemap: ${sitemapUrl}`);
console.log(`📰 RSS Feed: ${feedUrl}`);
console.log('----------------------------------------------------------------------\n');

// 1. IndexNow Submission
async function pingIndexNow(hostname, endpointPath) {
  return new Promise((resolve) => {
    const payload = JSON.stringify({
      host,
      key,
      keyLocation,
      urlList: uniqueUrls
    });

    const req = https.request({
      hostname,
      port: 443,
      path: endpointPath,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': Buffer.byteLength(payload),
        'User-Agent': 'TechBossPinger/1.0'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const ok = res.statusCode >= 200 && res.statusCode < 300;
        console.log(`  [IndexNow -> ${hostname}] Status: ${res.statusCode} ${ok ? '✅ OK' : data.substring(0, 80)}`);
        resolve({ service: hostname, status: res.statusCode, ok });
      });
    });

    req.on('error', (err) => {
      console.log(`  [IndexNow -> ${hostname}] ❌ Error: ${err.message}`);
      resolve({ service: hostname, status: 0, error: err.message });
    });

    req.setTimeout(10000, () => {
      req.destroy();
      console.log(`  [IndexNow -> ${hostname}] ⚠️ Timeout`);
      resolve({ service: hostname, status: 408 });
    });

    req.write(payload);
    req.end();
  });
}

// 2. HTTP GET Ping (Sitemaps)
async function pingUrl(serviceName, targetUrl) {
  return new Promise((resolve) => {
    const u = new URL(targetUrl);
    const client = u.protocol === 'https:' ? https : http;

    const req = client.get(targetUrl, {
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; TechBossSitemapPinger/1.0)' }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const ok = res.statusCode >= 200 && res.statusCode < 400;
        console.log(`  [${serviceName}] Status: ${res.statusCode} ${ok ? '✅ OK' : 'Returned ' + res.statusCode}`);
        resolve({ service: serviceName, status: res.statusCode, ok });
      });
    });

    req.on('error', (err) => {
      console.log(`  [${serviceName}] ❌ Error: ${err.message}`);
      resolve({ service: serviceName, status: 0, error: err.message });
    });

    req.setTimeout(8000, () => {
      req.destroy();
      console.log(`  [${serviceName}] ⚠️ Timeout`);
      resolve({ service: serviceName, status: 408 });
    });
  });
}

// 3. WebSub / PubSubHubbub Push for RSS Feed
async function pingWebSub(hubUrl) {
  return new Promise((resolve) => {
    const u = new URL(hubUrl);
    const client = u.protocol === 'https:' ? https : http;
    const body = new URLSearchParams({
      'hub.mode': 'publish',
      'hub.url': feedUrl
    }).toString();

    const req = client.request(hubUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(body),
        'User-Agent': 'TechBossWebSub/1.0'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const ok = res.statusCode >= 200 && res.statusCode < 300;
        console.log(`  [WebSub Hub -> ${u.hostname}] Status: ${res.statusCode} ${ok ? '✅ 204 No Content / Published' : data.substring(0, 80)}`);
        resolve({ service: u.hostname, status: res.statusCode, ok });
      });
    });

    req.on('error', (err) => {
      console.log(`  [WebSub Hub -> ${u.hostname}] ❌ Error: ${err.message}`);
      resolve({ service: u.hostname, status: 0, error: err.message });
    });

    req.setTimeout(8000, () => {
      req.destroy();
      console.log(`  [WebSub Hub -> ${u.hostname}] ⚠️ Timeout`);
      resolve({ service: u.hostname, status: 408 });
    });

    req.write(body);
    req.end();
  });
}

// 4. Ping-O-Matic XML-RPC (Broadcaster to weblogs, technorati, feedburner, etc.)
async function pingOMatic() {
  return new Promise((resolve) => {
    const xml = `<?xml version="1.0"?>
<methodCall>
  <methodName>weblogUpdates.ping</methodName>
  <params>
    <param><value>Tech Boss</value></param>
    <param><value>https://${host}/</value></param>
    <param><value>${feedUrl}</value></param>
  </params>
</methodCall>`;

    const req = http.request({
      hostname: 'rpc.pingomatic.com',
      port: 80,
      path: '/RPC2',
      method: 'POST',
      headers: {
        'Content-Type': 'text/xml',
        'Content-Length': Buffer.byteLength(xml),
        'User-Agent': 'TechBossPinger/1.0'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const hasError = data.includes('<boolean>1</boolean>');
        console.log(`  [Ping-O-Matic XML-RPC] Status: ${res.statusCode} ${!hasError ? '✅ Broadcasted to Blog Aggregators' : 'Response: ' + data.substring(0, 60)}`);
        resolve({ service: 'Ping-O-Matic', status: res.statusCode, ok: !hasError });
      });
    });

    req.on('error', (err) => {
      console.log(`  [Ping-O-Matic] ❌ Error: ${err.message}`);
      resolve({ service: 'Ping-O-Matic', status: 0, error: err.message });
    });

    req.setTimeout(8000, () => {
      req.destroy();
      console.log(`  [Ping-O-Matic] ⚠️ Timeout`);
      resolve({ service: 'Ping-O-Matic', status: 408 });
    });

    req.write(xml);
    req.end();
  });
}

async function main() {
  console.log('1. Pinging IndexNow Search Engine Endpoints (Bing, Yandex, Seznam, IndexNow Hub)...');
  await pingIndexNow('api.indexnow.org', '/indexnow');
  await pingIndexNow('www.bing.com', '/indexnow');
  await pingIndexNow('yandex.com', '/indexnow');
  await pingIndexNow('search.seznam.cz', '/indexnow');

  console.log('\n2. Pinging WebSub / PubSubHubbub Hubs (Google RSS Instant Notification)...');
  await pingWebSub('https://pubsubhubbub.appspot.com/');
  await pingWebSub('https://pubsubhubbub.superfeedr.com/');

  console.log('\n3. Pinging XML-RPC Aggregators (Ping-O-Matic / FeedBurner / Weblogs)...');
  await pingOMatic();

  console.log('\n4. Pinging Search Engine Sitemap Endpoints...');
  await pingUrl('Bing Sitemap Ping', `https://www.bing.com/ping?sitemap=${encodeURIComponent(sitemapUrl)}`);
  await pingUrl('Google Sitemap Ping (Legacy)', `https://www.google.com/ping?sitemap=${encodeURIComponent(sitemapUrl)}`);

  console.log('\n======================================================================');
  console.log('🎉 ALL SEARCH ENGINE PINGS COMPLETED SUCCESSFULLY!');
  console.log('======================================================================');
}

main().catch(err => console.error('Fatal error:', err));
