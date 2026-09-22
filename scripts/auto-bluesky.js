const fs = require('fs');
const path = require('path');
const vm = require('vm');

async function autoPostLatest() {
  const identifier = process.env.BLUESKY_HANDLE || 'imtechboss.bsky.social';
  const password = process.env.BLUESKY_APP_PASSWORD || 'sz7o-o56n-monc-m4px';
  const dataPath = path.join(__dirname, '..', 'js', 'data.js');
  const trackerFile = path.join(__dirname, '..', '.last_bluesky_id.txt');

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
    console.log('Latest article already posted to Bluesky. Skipping.');
    return;
  }

  // 1. Login
  const loginRes = await fetch('https://bsky.social/xrpc/com.atproto.server.createSession', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ identifier, password })
  });

  const session = await loginRes.json();
  if (!loginRes.ok) {
    console.error('Bluesky login failed:', session);
    return;
  }

  // 2. Fetch/Upload Article Image
  let thumbBlob = null;
  try {
    let imgBuffer = null;
    let mimeType = 'image/jpeg';

    if (latest.image.startsWith('http://') || latest.image.startsWith('https://')) {
      const imgRes = await fetch(latest.image);
      if (imgRes.ok) {
        const arrBuf = await imgRes.arrayBuffer();
        imgBuffer = Buffer.from(arrBuf);
        mimeType = imgRes.headers.get('content-type') || 'image/jpeg';
      }
    } else {
      const localPath = path.join(__dirname, '..', latest.image.replace(/^\//, ''));
      if (fs.existsSync(localPath)) {
        imgBuffer = fs.readFileSync(localPath);
        if (localPath.endsWith('.png')) mimeType = 'image/png';
      }
    }

    if (imgBuffer) {
      const blobRes = await fetch('https://bsky.social/xrpc/com.atproto.repo.uploadBlob', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session.accessJwt}`,
          'Content-Type': mimeType
        },
        body: imgBuffer
      });
      const blobData = await blobRes.json();
      if (blobRes.ok) {
        thumbBlob = blobData.blob;
        console.log('Article image uploaded as blob successfully!');
      }
    }
  } catch (err) {
    console.warn('Image upload failed, proceeding with text:', err.message);
  }

  // 3. Craft Post
  const articleUrl = `https://imtechboss.com/post?id=${latest.id}`;
  const tagsText = (latest.tags || []).slice(0, 3).map(t => `#${t.replace(/\s+/g, '')}`).join(' ');

  let postText = `🔥 NEW ON TECH BOSS:\n${latest.title}\n\nRead the full guide 👇\n${articleUrl}\n\n${tagsText}`;
  if (postText.length > 290) {
    postText = `🔥 NEW: ${latest.title.slice(0, 130)}...\n\nRead more 👇\n${articleUrl}\n\n${tagsText}`;
  }

  const record = {
    $type: 'app.bsky.feed.post',
    text: postText,
    createdAt: new Date().toISOString(),
    facets: [
      {
        index: {
          byteStart: Buffer.from(postText.slice(0, postText.indexOf(articleUrl))).length,
          byteEnd: Buffer.from(postText.slice(0, postText.indexOf(articleUrl) + articleUrl.length)).length
        },
        features: [
          {
            $type: 'app.bsky.richtext.facet#link',
            uri: articleUrl
          }
        ]
      }
    ]
  };

  if (thumbBlob) {
    record.embed = {
      $type: 'app.bsky.embed.external',
      external: {
        uri: articleUrl,
        title: latest.title,
        description: latest.excerpt || 'Read the full in-depth article on Tech Boss.',
        thumb: thumbBlob
      }
    };
  }

  const postRes = await fetch('https://bsky.social/xrpc/com.atproto.repo.createRecord', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${session.accessJwt}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      repo: session.did,
      collection: 'app.bsky.feed.post',
      record: record
    })
  });

  const postResult = await postRes.json();
  if (postRes.ok) {
    console.log('🎉 Article successfully published to Bluesky! Post URI:', postResult.uri);
    fs.writeFileSync(trackerFile, latest.id, 'utf8');
  } else {
    console.error('Failed to post article:', postResult);
  }
}

autoPostLatest();
