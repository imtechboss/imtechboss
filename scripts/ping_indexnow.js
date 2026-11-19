const https = require('https');
const fs = require('fs');
const path = require('path');

const baseDir = path.resolve(__dirname, '..');
const sitemapContent = fs.readFileSync(path.join(baseDir, 'sitemap.xml'), 'utf8');

const key = 'a8f3b9c712e44d569801a23c45d6e7f8';
const host = 'imtechboss.com';

const locMatches = [...sitemapContent.matchAll(/<loc>(https:\/\/imtechboss\.com\/[^<]*)<\/loc>/g)].map(m => m[1]);
const urls = [
  ...new Set([
    ...locMatches,
    `https://${host}/sitemap.xml`,
    `https://${host}/feed.xml`,
  ])
];

const payload = JSON.stringify({
  host,
  key,
  keyLocation: `https://${host}/${key}.txt`,
  urlList: urls
});

function submitToEndpoint(hostname, endpointPath) {
  return new Promise((resolve) => {
    const req = https.request({
      hostname,
      port: 443,
      path: endpointPath,
      method: 'POST',
      family: 4,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        console.log(`✓ [${hostname}] Status: ${res.statusCode} ${res.statusCode === 200 ? 'OK' : data}`);
        resolve({ host: hostname, status: res.statusCode });
      });
    });

    req.on('error', (e) => {
      console.log(`✗ [${hostname}] Error:`, e.message);
      resolve({ host: hostname, error: e.message });
    });

    req.write(payload);
    req.end();
  });
}

async function main() {
  console.log(`Submitting all ${urls.length} clean sitemap URLs (including 17 tools + sitemap.xml + feed.xml) to Bing & IndexNow...`);
  await submitToEndpoint('api.indexnow.org', '/IndexNow');
  await submitToEndpoint('www.bing.com', '/IndexNow');
  await submitToEndpoint('yandex.com', '/indexnow');
  console.log('Done! All URLs submitted to Bing, Yandex, and IndexNow partners.');
}

main();
