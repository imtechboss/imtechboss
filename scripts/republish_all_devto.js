// scripts/republish_all_devto.js
// Run this script whenever you want to re-publish all DEV.to drafts after AdSense approval
const API_KEY = 'ZtmMvBpzm7EgsBquEstMv5mq';

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function republishAll() {
  console.log('Fetching all draft DEV.to articles...');
  const res = await fetch('https://dev.to/api/articles/me/all', {
    headers: { 'api-key': API_KEY, 'User-Agent': 'TechBoss/1.0' }
  });
  const data = await res.json();
  const drafts = data.filter(a => !a.published);
  console.log(`Found ${drafts.length} draft articles on DEV.to.\n`);

  for (let i = 0; i < drafts.length; i++) {
    const art = drafts[i];
    process.stdout.write(`[${i + 1}/${drafts.length}] Republishing: "${art.title.substring(0, 45)}..." (ID: ${art.id})... `);
    try {
      const pubRes = await fetch(`https://dev.to/api/articles/${art.id}`, {
        method: 'PUT',
        headers: {
          'api-key': API_KEY,
          'Content-Type': 'application/json',
          'User-Agent': 'TechBoss/1.0'
        },
        body: JSON.stringify({ article: { published: true } })
      });
      if (pubRes.ok) {
        console.log('✅ 200 OK (Published)');
      } else {
        console.log(`❌ HTTP ${pubRes.status}`);
      }
    } catch (e) {
      console.log(`❌ Error: ${e.message}`);
    }
    await sleep(2000);
  }
}

republishAll().catch(err => console.error('Fatal error:', err));
