const fs = require('fs');
const path = require('path');
const vm = require('vm');

const MASTODON_INSTANCE = process.env.MASTODON_INSTANCE || 'https://mastodon.social';
const MASTODON_TOKEN = process.env.MASTODON_ACCESS_TOKEN || 'DETVE4toZzAeiy4sUEAbCvGg0iE6q3-NnKBHstH1FVE';
const BASE_URL = 'https://imtechboss.com';

const dataPath = path.join(__dirname, '..', 'js', 'data.js');
const trackerFile = path.join(__dirname, '..', '.last_mastodon_id.txt');

async function uploadMedia(imageUrl, description) {
  try {
    const imgRes = await fetch(imageUrl);
    if (!imgRes.ok) return null;
    const arrayBuffer = await imgRes.arrayBuffer();
    const blob = new Blob([arrayBuffer], { type: 'image/jpeg' });

    const formData = new FormData();
    formData.append('file', blob, 'image.jpg');
    if (description) {
      formData.append('description', description.substring(0, 400));
    }

    const res = await fetch(`${MASTODON_INSTANCE}/api/v2/media`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${MASTODON_TOKEN}`
      },
      body: formData
    });

    if (!res.ok) {
      console.log('Media upload failed:', res.status, await res.text());
      return null;
    }

    const data = await res.json();
    return data.id;
  } catch (err) {
    console.log('Error uploading media to Mastodon:', err.message);
    return null;
  }
}

async function postStatus(article, mediaId) {
  const url = `${BASE_URL}/post.html?id=${article.id}`;
  
  // Format tags as hashtags
  const hashtags = (article.tags || ['Tech', 'News'])
    .map(t => '#' + t.replace(/[^a-zA-Z0-9]/g, ''))
    .filter(t => t.length > 1)
    .slice(0, 4)
    .join(' ');

  const text = `${article.title}\n\n${article.excerpt.substring(0, 220)}...\n\nRead more: ${url}\n\n${hashtags}`;

  const payload = {
    status: text,
    visibility: 'public'
  };

  if (mediaId) {
    payload.media_ids = [mediaId];
  }

  const res = await fetch(`${MASTODON_INSTANCE}/api/v1/statuses`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${MASTODON_TOKEN}`
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    throw new Error(`Status post failed: ${res.status} ${await res.text()}`);
  }

  return await res.json();
}

async function main() {
  if (!fs.existsSync(dataPath)) {
    console.error('data.js not found');
    return;
  }

  const dataRaw = fs.readFileSync(dataPath, 'utf8');
  const ctx = {};
  vm.runInNewContext(dataRaw, ctx);
  const articles = ctx.initialArticles || [];

  if (articles.length === 0) {
    console.log('No articles found');
    return;
  }

  const latest = articles[0];
  console.log('Latest Article:', latest.id, '-', latest.title);

  let lastId = '';
  if (fs.existsSync(trackerFile)) {
    lastId = fs.readFileSync(trackerFile, 'utf8').trim();
  }

  if (latest.id === lastId && process.env.FORCE_POST !== 'true') {
    console.log('Latest article already posted to Mastodon. Skipping.');
    return;
  }

  let mediaId = null;
  if (latest.image) {
    console.log('Uploading image attachment...');
    mediaId = await uploadMedia(latest.image, latest.title);
    if (mediaId) {
      console.log('✓ Media uploaded with ID:', mediaId);
      await new Promise(r => setTimeout(r, 1500));
    }
  }

  const post = await postStatus(latest, mediaId);
  console.log('🎉 Successfully published to Mastodon!');
  console.log('Post URL:', post.url);

  fs.writeFileSync(trackerFile, latest.id);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
