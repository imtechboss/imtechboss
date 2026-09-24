const BSKY_HANDLE = process.env.BLUESKY_HANDLE || 'imtechboss.bsky.social';
const BSKY_PASSWORD = process.env.BLUESKY_APP_PASSWORD || 'sz7o-o56n-monc-m4px';
const MASTODON_INSTANCE = process.env.MASTODON_INSTANCE || 'https://mastodon.social';
const MASTODON_TOKEN = process.env.MASTODON_ACCESS_TOKEN || 'DETVE4toZzAeiy4sUEAbCvGg0iE6q3-NnKBHstH1FVE';

const MAG_URL = 'https://flipboard.com/@imtechboss/tech-boss-ai-news-mvthmcr0y';

async function postBluesky() {
  console.log('--- Posting to Bluesky ---');
  const loginRes = await fetch('https://bsky.social/xrpc/com.atproto.server.createSession', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ identifier: BSKY_HANDLE, password: BSKY_PASSWORD })
  });

  const session = await loginRes.json();
  if (!loginRes.ok) {
    console.error('Bluesky login failed:', session);
    return;
  }

  const text = `📱 We are officially on Flipboard!\n\nFollow our curated magazine 'TECH BOSS AI & NEWS' for daily deep-dives on AI breakthroughs, cybersecurity guides, and tech news:\n\n${MAG_URL}\n\n#TechBoss #AI #Technology #Flipboard`;

  // Byte index for facet
  const enc = new TextEncoder();
  const textBytes = enc.encode(text);
  const urlBytes = enc.encode(MAG_URL);
  const startIdx = text.indexOf(MAG_URL);
  const byteStart = enc.encode(text.slice(0, startIdx)).length;
  const byteEnd = byteStart + urlBytes.length;

  const record = {
    $type: 'app.bsky.feed.post',
    text: text,
    facets: [
      {
        index: { byteStart, byteEnd },
        features: [{ $type: 'app.bsky.richtext.facet#link', uri: MAG_URL }]
      }
    ],
    embed: {
      $type: 'app.bsky.embed.external',
      external: {
        uri: MAG_URL,
        title: 'TECH BOSS AI & NEWS on Flipboard',
        description: 'Curated daily magazine featuring breaking AI news, cybersecurity guides, gaming benchmarks, and tech reviews.'
      }
    },
    createdAt: new Date().toISOString()
  };

  const postRes = await fetch('https://bsky.social/xrpc/com.atproto.repo.createRecord', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${session.accessJwt}`
    },
    body: JSON.stringify({
      repo: session.did,
      collection: 'app.bsky.feed.post',
      record: record
    })
  });

  const postData = await postRes.json();
  if (!postRes.ok) {
    console.error('Bluesky post failed:', postData);
  } else {
    console.log('✅ Bluesky announcement posted successfully! URI:', postData.uri);
  }
}

async function postMastodon() {
  console.log('--- Posting to Mastodon ---');
  const text = `📱 We are officially on Flipboard!\n\nFollow our curated digital magazine 'TECH BOSS AI & NEWS' for daily deep-dives on AI breakthroughs, cybersecurity guides, and tech news:\n\n${MAG_URL}\n\n#TechBoss #AI #Technology #Flipboard #DigitalMagazine`;

  const res = await fetch(`${MASTODON_INSTANCE}/api/v1/statuses`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${MASTODON_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      status: text,
      visibility: 'public'
    })
  });

  const data = await res.json();
  if (!res.ok) {
    console.error('Mastodon post failed:', data);
  } else {
    console.log('✅ Mastodon announcement posted successfully! URL:', data.url);
  }
}

async function main() {
  await postBluesky();
  await new Promise(r => setTimeout(r, 3000));
  await postMastodon();
}

main().catch(console.error);
