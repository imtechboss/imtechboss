const fs = require('fs');
const path = require('path');
const vm = require('vm');

async function run() {
  const dataPath = path.join(__dirname, '..', 'js', 'data.js');
  const trackerFile = path.join(__dirname, '..', '.last_tweeted_id.txt');

  if (!fs.existsSync(dataPath)) {
    console.error('data.js not found');
    process.exit(1);
  }

  const dataRaw = fs.readFileSync(dataPath, 'utf8');
  const ctx = {};
  vm.runInNewContext(dataRaw, ctx);
  const articles = ctx.initialArticles || [];

  if (articles.length === 0) {
    console.log('No articles found.');
    return;
  }

  const latest = articles[0];
  console.log(`Latest article ID: ${latest.id}`);

  let lastTweeted = '';
  if (fs.existsSync(trackerFile)) {
    lastTweeted = fs.readFileSync(trackerFile, 'utf8').trim();
  }

  if (latest.id === lastTweeted && process.env.FORCE_TWEET !== 'true') {
    console.log('Latest article has already been tweeted. Skipping.');
    return;
  }

  // Verify Twitter API credentials
  const appKey = process.env.TWITTER_API_KEY;
  const appSecret = process.env.TWITTER_API_SECRET;
  const accessToken = process.env.TWITTER_ACCESS_TOKEN;
  const accessSecret = process.env.TWITTER_ACCESS_SECRET;

  if (!appKey || !appSecret || !accessToken || !accessSecret) {
    console.error('Missing Twitter API credentials in environment variables.');
    process.exit(1);
  }

  const { TwitterApi } = require('twitter-api-v2');
  const client = new TwitterApi({
    appKey,
    appSecret,
    accessToken,
    accessSecret,
  });

  const postUrl = `https://imtechboss.com/post?id=${latest.id}`;
  const hashtags = (latest.tags || []).slice(0, 3).map(t => `#${t.replace(/\s+/g, '')}`).join(' ');

  // Craft tweet text within 280 chars
  // Title (max 150) + url + hashtags
  let tweetText = `🔥 NEW: ${latest.title}\n\nRead full guide on Tech Boss 👇\n${postUrl}\n\n${hashtags}`;
  if (tweetText.length > 280) {
    const trimmedTitle = latest.title.slice(0, 100) + '...';
    tweetText = `🔥 NEW: ${trimmedTitle}\n\nRead more 👇\n${postUrl}\n\n${hashtags}`;
  }

  console.log('Attempting to post tweet:\n', tweetText);

  try {
    const res = await client.v2.tweet(tweetText);
    console.log('Tweet successfully published!', res.data);
    fs.writeFileSync(trackerFile, latest.id, 'utf8');
  } catch (err) {
    console.error('Failed to post tweet:', err);
    process.exit(1);
  }
}

run();
