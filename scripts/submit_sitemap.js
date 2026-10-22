// submit_sitemap.js – Programmatically submit the generated sitemap to search engines
// ---------------------------------------------------------------
// This script uses the Google Search Console API to submit the sitemap
// for the verified site, and also pings Bing/Yandex via their simple GET URLs.
//
// Prerequisites:
//   1. Install dependencies:
//        npm install googleapis node-fetch
//   2. Create a service‑account JSON key with access to the Search Console API
//      and share the property with the service‑account email ("Add user" in GSC).
//   3. Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path
//      of that JSON file, or place the file at the path below.
//   4. Update the constants SITE_URL and SITEMAP_URL as needed.
//
// Usage:
//   node scripts/submit_sitemap.js   // submit to Google and ping Bing/Yandex
//
// Note: Google does not have a public "ping" endpoint any more – we must use the
//       Search Console API method `sitemaps.submit`. The script logs the API
//       response so you can confirm success.

const { google } = require('googleapis');
const fetch = require('node-fetch');

// ---------------------------------------------------------------
// Configuration – update these values for your site
// ---------------------------------------------------------------
const SITE_URL = 'https://imtechboss.com/'; // must match the exact property URL in GSC
const SITEMAP_URL = `${SITE_URL}sitemap.xml`;
// Path to the service‑account JSON credentials (optional if GOOGLE_APPLICATION_CREDENTIALS is set)
const CREDENTIALS_PATH = `${__dirname}/../.gcloud/service-account.json`;

async function submitToGoogle() {
  const auth = new google.auth.GoogleAuth({
    scopes: ['https://www.googleapis.com/auth/webmasters'],
    keyFile: CREDENTIALS_PATH,
  });
  const authClient = await auth.getClient();
  const webmasters = google.webmasters({ version: 'v3', auth: authClient });

  try {
    const res = await webmasters.sitemaps.submit({
      siteUrl: SITE_URL,
      feedpath: SITEMAP_URL,
    });
    console.log('✅ Google Search Console sitemap submitted:', res.data);
  } catch (err) {
    console.error('❌ Google sitemap submission failed:', err.response?.data || err.message);
  }
}

async function pingBing() {
  const url = `https://www.bing.com/ping?sitemap=${encodeURIComponent(SITEMAP_URL)}`;
  try {
    const res = await fetch(url);
    console.log('✅ Bing ping response status:', res.status);
  } catch (err) {
    console.error('❌ Bing ping failed:', err.message);
  }
}

async function pingYandex() {
  const url = `https://webmaster.yandex.com/ping?sitemap=${encodeURIComponent(SITEMAP_URL)}`;
  try {
    const res = await fetch(url);
    console.log('✅ Yandex ping response status:', res.status);
  } catch (err) {
    console.error('❌ Yandex ping failed:', err.message);
  }
}

(async () => {
  console.log('🚀 Submitting sitemap...');
  await submitToGoogle();
  await pingBing();
  await pingYandex();
  console.log('✅ Done.');
})();
