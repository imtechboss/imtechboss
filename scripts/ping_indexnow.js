const https = require('https');
const fs = require('fs');
const path = require('path');

const baseDir = path.resolve(__dirname, '..');
const dataContent = fs.readFileSync(path.join(baseDir, 'js', 'data.js'), 'utf8');

const match = dataContent.match(/var\s+initialArticles\s*=\s*(\[.*?\]);/s);
if (!match) {
  console.error('initialArticles not found');
  process.exit(1);
}

const articles = JSON.parse(match[1]);

const key = 'a8f3b9c712e44d569801a23c45d6e7f8';
const host = 'imtechboss.com';

const urls = [
  `https://${host}/`,
  `https://${host}/sitemap.xml`,
  ...articles.map(a => `https://${host}/post?id=${a.id}`)
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
  console.log(`Submitting all ${articles.length} articles (${urls.length} URLs total) to Bing & IndexNow...`);
  await submitToEndpoint('api.indexnow.org', '/IndexNow');
  await submitToEndpoint('www.bing.com', '/IndexNow');
  await submitToEndpoint('yandex.com', '/indexnow');
  console.log('Done! All URLs submitted to Bing, Yandex, and IndexNow partners.');
}

main();
