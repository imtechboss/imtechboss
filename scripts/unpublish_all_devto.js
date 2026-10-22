const API_KEY = 'ZtmMvBpzm7EgsBquEstMv5mq';

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function unpublishAll() {
  console.log('Fetching all published DEV.to articles...');
  const res = await fetch('https://dev.to/api/articles/me/all', {
    headers: { 'api-key': API_KEY, 'User-Agent': 'TechBoss/1.0' }
  });
  const data = await res.json();
  const published = data.filter(a => a.published);
  console.log(`Found ${published.length} published articles on DEV.to.\n`);

  for (let i = 0; i < published.length; i++) {
    const art = published[i];
    process.stdout.write(`[${i + 1}/${published.length}] Unpublishing: "${art.title.substring(0, 45)}..." (ID: ${art.id})... `);
    try {
      const upRes = await fetch(`https://dev.to/api/articles/${art.id}`, {
        method: 'PUT',
        headers: {
          'api-key': API_KEY,
          'Content-Type': 'application/json',
          'User-Agent': 'TechBoss/1.0'
        },
        body: JSON.stringify({ article: { published: false } })
      });
      if (upRes.ok) {
        console.log('✅ 200 OK (Converted to Draft)');
      } else {
        console.log(`❌ HTTP ${upRes.status}`);
      }
    } catch (e) {
      console.log(`❌ Error: ${e.message}`);
    }
    await sleep(2000);
  }

  console.log('\nVerifying remaining published articles on DEV.to...');
  const verifyRes = await fetch('https://dev.to/api/articles/me/all', {
    headers: { 'api-key': API_KEY, 'User-Agent': 'TechBoss/1.0' }
  });
  const verifyData = await verifyRes.json();
  const remaining = verifyData.filter(a => a.published);
  console.log(`Remaining published articles on DEV.to: ${remaining.length}`);
}

unpublishAll().catch(err => console.error('Fatal error:', err));
