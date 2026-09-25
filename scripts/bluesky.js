const https = require('https');
const http = require('http');

const BSKY_HANDLE = process.env.BLUESKY_HANDLE || 'imtechboss.bsky.social';
const BSKY_APP_PASSWORD = process.env.BLUESKY_APP_PASSWORD || 'sz7o-o56n-monc-m4px';

function httpRequest(options, postData, isBinary = false) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => {
        const buffer = Buffer.concat(chunks);
        if (isBinary) {
          return resolve({ status: res.statusCode, buffer });
        }
        const str = buffer.toString('utf8');
        try {
          resolve({ status: res.statusCode, body: JSON.parse(str) });
        } catch (e) {
          resolve({ status: res.statusCode, raw: str });
        }
      });
    });
    req.on('error', reject);
    if (postData) {
      if (Buffer.isBuffer(postData)) {
        req.write(postData);
      } else {
        req.write(typeof postData === 'string' ? postData : JSON.stringify(postData));
      }
    }
    req.end();
  });
}

function fetchUrlBuffer(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    protocol.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return resolve(fetchUrlBuffer(res.headers.location));
      }
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => resolve({ buffer: Buffer.concat(chunks), contentType: res.headers['content-type'] || 'image/jpeg' }));
    }).on('error', reject);
  });
}

async function createSession() {
  const res = await httpRequest({
    hostname: 'bsky.social',
    port: 443,
    path: '/xrpc/com.atproto.server.createSession',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  }, {
    identifier: BSKY_HANDLE,
    password: BSKY_APP_PASSWORD
  });
  return res;
}

// Upload image to Bluesky blob storage
async function uploadBlob(accessJwt, imageBuffer, mimeType = 'image/jpeg') {
  const res = await httpRequest({
    hostname: 'bsky.social',
    port: 443,
    path: '/xrpc/com.atproto.repo.uploadBlob',
    method: 'POST',
    headers: {
      'Content-Type': mimeType,
      'Authorization': `Bearer ${accessJwt}`
    }
  }, imageBuffer);

  if (res.status === 200 && res.body && res.body.blob) {
    return res.body.blob;
  }
  return null;
}

// Calculate UTF-8 byte offsets for facets (Bluesky requires byte indices, not character counts)
function extractFacets(text) {
  const facets = [];
  const utf8Encoder = new TextEncoder();

  // Match URLs
  const urlRegex = /https?:\/\/[^\s]+/g;
  let match;
  while ((match = urlRegex.exec(text)) !== null) {
    const matchedUrl = match[0];
    const prefix = text.substring(0, match.index);
    const byteStart = utf8Encoder.encode(prefix).length;
    const byteEnd = byteStart + utf8Encoder.encode(matchedUrl).length;

    facets.push({
      index: { byteStart, byteEnd },
      features: [{
        $type: 'app.bsky.richtext.facet#link',
        uri: matchedUrl
      }]
    });
  }

  // Match Tags (#AI, #Tech, etc.)
  const tagRegex = /(?:^|\s)(#[a-zA-Z0-9_]+)/g;
  while ((match = tagRegex.exec(text)) !== null) {
    const rawTag = match[1];
    const tag = rawTag.substring(1);
    const indexInMatch = match[0].indexOf(rawTag);
    const prefix = text.substring(0, match.index + indexInMatch);
    const byteStart = utf8Encoder.encode(prefix).length;
    const byteEnd = byteStart + utf8Encoder.encode(rawTag).length;

    facets.push({
      index: { byteStart, byteEnd },
      features: [{
        $type: 'app.bsky.richtext.facet#tag',
        tag: tag
      }]
    });
  }

  return facets;
}

async function postArticleToBluesky(article) {
  console.log(`\n🦋 Preparing to post article to Bluesky: "${article.title}"...`);
  const sessionRes = await createSession();
  if (sessionRes.status !== 200) {
    console.error('Bluesky login failed:', sessionRes.body);
    return false;
  }

  const { accessJwt, did, handle } = sessionRes.body;
  console.log(`Connected to Bluesky as @${handle}`);

  const articleUrl = `https://imtechboss.com/post.html?id=${encodeURIComponent(article.id)}`;

  // Fetch and upload image thumbnail if available
  let thumbBlob = null;
  if (article.image) {
    try {
      console.log('Downloading image thumbnail for embed card...');
      const { buffer, contentType } = await fetchUrlBuffer(article.image);
      // Ensure image is under 950KB for Bluesky blob limit
      if (buffer.length < 950000) {
        console.log('Uploading thumbnail to Bluesky...');
        thumbBlob = await uploadBlob(accessJwt, buffer, contentType.split(';')[0]);
      }
    } catch (e) {
      console.log('Could not upload thumbnail, continuing without it:', e.message);
    }
  }

  // Tags
  let categoryTag = (article.category || 'Tech').replace(/[^a-zA-Z0-9]/g, '');
  let extraTag = (article.tags && article.tags[0]) ? article.tags[0].replace(/[^a-zA-Z0-9]/g, '') : 'TechBoss';
  const readMore = `\n\n👉 Full Story: ${articleUrl}\n#Tech #${categoryTag} #${extraTag}`;
  const maxAvailableForText = 280 - readMore.length;

  let headerText = `⚡ ${article.title}`;
  if (headerText.length > maxAvailableForText) {
    headerText = headerText.substring(0, maxAvailableForText - 3) + '...';
  } else if ((headerText + '\n\n' + article.excerpt).length <= maxAvailableForText) {
    headerText = headerText + '\n\n' + article.excerpt;
  } else {
    const remaining = maxAvailableForText - headerText.length - 4;
    if (remaining > 30) {
      headerText = headerText + '\n\n' + article.excerpt.substring(0, remaining - 3) + '...';
    }
  }

  const postText = `${headerText}${readMore}`;
  const facets = extractFacets(postText);

  const embed = {
    $type: 'app.bsky.embed.external',
    external: {
      uri: articleUrl,
      title: article.title,
      description: article.excerpt || article.title
    }
  };

  if (thumbBlob) {
    embed.external.thumb = thumbBlob;
  }

  const record = {
    $type: 'app.bsky.feed.post',
    text: postText,
    facets: facets,
    embed: embed,
    createdAt: new Date().toISOString()
  };

  console.log('Publishing post on Bluesky...');
  const postRes = await httpRequest({
    hostname: 'bsky.social',
    port: 443,
    path: '/xrpc/com.atproto.repo.createRecord',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessJwt}`
    }
  }, {
    repo: did,
    collection: 'app.bsky.feed.post',
    record: record
  });

  if (postRes.status === 200) {
    console.log('🎉 Post successfully published on Bluesky!');
    console.log('Bluesky Post URI:', postRes.body.uri);
    return postRes.body;
  } else {
    console.error('Failed to post on Bluesky:', postRes.body || postRes.raw);
    return false;
  }
}

module.exports = {
  createSession,
  uploadBlob,
  extractFacets,
  postArticleToBluesky
};
