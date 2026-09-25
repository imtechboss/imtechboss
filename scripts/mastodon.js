const MASTODON_HOST = 'https://mastodon.social';
const MASTODON_ACCESS_TOKEN = process.env.MASTODON_ACCESS_TOKEN || 'DETVE4toZzAeiy4sUEAbCvGg0iE6q3-NnKBHstH1FVE';

async function uploadMedia(imageUrl, description) {
  if (!imageUrl) return null;
  try {
    console.log('Downloading image for Mastodon attachment...');
    const imgRes = await fetch(imageUrl);
    if (!imgRes.ok) return null;
    const arrayBuffer = await imgRes.arrayBuffer();
    const blob = new Blob([arrayBuffer], { type: 'image/jpeg' });

    const formData = new FormData();
    formData.append('file', blob, 'featured.jpg');
    if (description) {
      formData.append('description', description.substring(0, 400));
    }

    const res = await fetch(`${MASTODON_HOST}/api/v2/media`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${MASTODON_ACCESS_TOKEN}`
      },
      body: formData
    });

    if (!res.ok) {
      console.warn('Mastodon media upload status:', res.status);
      return null;
    }

    const data = await res.json();
    return data.id;
  } catch (err) {
    console.warn('Mastodon media upload error:', err.message);
    return null;
  }
}

async function postArticleToMastodon(article) {
  console.log(`\n🐘 Preparing to post article to Mastodon: "${article.title}"...`);

  const articleUrl = `https://imtechboss.com/post.html?id=${encodeURIComponent(article.id)}`;
  let categoryTag = (article.category || 'Tech').replace(/[^a-zA-Z0-9]/g, '');
  let tags = (article.tags || ['Tech', 'News'])
    .map(t => '#' + t.replace(/[^a-zA-Z0-9]/g, ''))
    .filter(t => t.length > 1)
    .slice(0, 4)
    .join(' ');

  let mediaId = null;
  if (article.image) {
    mediaId = await uploadMedia(article.image, article.title);
    if (mediaId) {
      console.log('✓ Image attachment uploaded with Media ID:', mediaId);
      // Wait a moment for Mastodon media processing
      await new Promise(r => setTimeout(r, 1200));
    }
  }

  // Mastodon allows up to 500 characters
  let statusText = `⚡ ${article.title}\n\n${article.excerpt}\n\n👉 Read the complete guide:\n${articleUrl}\n\n${tags}`;
  if (statusText.length > 490) {
    statusText = `⚡ ${article.title}\n\n${article.excerpt.substring(0, 200)}...\n\n👉 Read complete guide:\n${articleUrl}\n\n#Tech #${categoryTag} #TechBoss`;
  }

  const payload = {
    status: statusText,
    visibility: 'public',
    language: 'en'
  };

  if (mediaId) {
    payload.media_ids = [mediaId];
  }

  const res = await fetch(`${MASTODON_HOST}/api/v1/statuses`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${MASTODON_ACCESS_TOKEN}`
    },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    const data = await res.json();
    console.log('🎉 Successfully published post on Mastodon!');
    console.log('Mastodon Status URL:', data.url);
    return data;
  } else {
    const errorData = await res.text();
    console.error('Failed to post on Mastodon:', res.status, errorData);
    return false;
  }
}

module.exports = {
  postArticleToMastodon
};
