const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { postArticleToBluesky } = require('./bluesky');
const { postArticleToMastodon } = require('./mastodon');

const projectRoot = path.resolve(__dirname, '..');
const dataPath = path.join(projectRoot, 'js', 'data.js');
const historyFile = path.join(__dirname, 'social-history.json');
const lastBskyFile = path.join(projectRoot, '.last_bluesky_id.txt');
const lastMstdFile = path.join(projectRoot, '.last_mastodon_id.txt');

// Load articles dynamically from data.js
function loadArticles() {
  if (!fs.existsSync(dataPath)) {
    console.error('❌ js/data.js not found');
    return [];
  }
  try {
    const dataRaw = fs.readFileSync(dataPath, 'utf8');
    const ctx = {};
    vm.runInNewContext(dataRaw, ctx);
    return ctx.initialArticles || [];
  } catch (err) {
    console.error('❌ Error parsing js/data.js:', err.message);
    return [];
  }
}

// Initialize history tracking file
function loadHistory() {
  if (fs.existsSync(historyFile)) {
    try {
      return JSON.parse(fs.readFileSync(historyFile, 'utf8'));
    } catch (e) {
      console.error('Warning reading history file, resetting:', e.message);
    }
  }

  // Pre-seed with any existing one-off posted tracker files
  const initialPosted = [];
  if (fs.existsSync(lastBskyFile)) {
    const bskyId = fs.readFileSync(lastBskyFile, 'utf8').trim();
    if (bskyId && !initialPosted.includes(bskyId)) initialPosted.push(bskyId);
  }
  if (fs.existsSync(lastMstdFile)) {
    const mstdId = fs.readFileSync(lastMstdFile, 'utf8').trim();
    if (mstdId && !initialPosted.includes(mstdId)) initialPosted.push(mstdId);
  }

  return {
    postedIds: initialPosted,
    history: initialPosted.map(id => ({
      id,
      postedAt: new Date().toISOString(),
      note: 'Pre-seeded from previous single-post runs'
    }))
  };
}

function saveHistory(historyData) {
  try {
    fs.writeFileSync(historyFile, JSON.stringify(historyData, null, 2), 'utf8');
  } catch (err) {
    console.error('Error saving history file:', err.message);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runScheduler() {
  console.log('======================================================================');
  console.log('  🚀 Tech Boss (imtechboss.com) - Auto Social Cross-Poster');
  console.log('  Platforms: Bluesky (@imtechboss.bsky.social) & Mastodon (@imtechboss)');
  console.log('======================================================================');
  console.log('Rules:');
  console.log(' • Backlog articles: Shared every 20-25 minutes (natural anti-spam cadence)');
  console.log(' • Brand new articles: Prioritized and shared with a 5-minute difference');
  console.log(' • State saved to: scripts/social-history.json (survives restarts & power off)');
  console.log(' • Dynamic updates: Auto-detects newly added articles in data.js\n');

  while (true) {
    const articles = loadArticles();
    if (articles.length === 0) {
      console.log('No articles found in data.js. Retrying in 1 minute...');
      await sleep(60 * 1000);
      continue;
    }

    const history = loadHistory();

    // Identify unposted articles
    const unpostedArticles = articles.filter(a => !history.postedIds.includes(a.id));

    if (unpostedArticles.length === 0) {
      console.log(`🎉 All ${articles.length} articles have been shared! Checking for newly published articles in 10 minutes...`);
      await sleep(10 * 60 * 1000);
      continue;
    }

    console.log(`📊 Unposted articles remaining: ${unpostedArticles.length} / ${articles.length}`);

    // Check if the newest article (at index 0) is unposted
    const latestArticle = articles[0];
    let nextArticleToPost;
    let delayMinutes;

    if (!history.postedIds.includes(latestArticle.id)) {
      // It's a fresh newly added article! Give it 5 minutes delay
      nextArticleToPost = latestArticle;
      delayMinutes = 5;
      console.log(`⚡ Fresh new article detected at top: "${nextArticleToPost.title}"`);
      console.log(`⏱️ Waiting 5 minutes before posting this new story...`);
    } else {
      // Standard drip queue: pick oldest unposted (from bottom) to drip in chronological order
      nextArticleToPost = unpostedArticles[unpostedArticles.length - 1];
      // Random 20 to 25 minutes
      delayMinutes = Math.floor(Math.random() * 6) + 20; // 20 to 25 min
      const scheduledTime = new Date(Date.now() + delayMinutes * 60 * 1000).toLocaleTimeString();
      console.log(`⏳ Next in queue: "${nextArticleToPost.title}" [${nextArticleToPost.category || 'Tech'}]`);
      console.log(`⏱️ Interval timer: Posting in ${delayMinutes} minutes (at ${scheduledTime})...`);
    }

    // Wait the scheduled duration
    await sleep(delayMinutes * 60 * 1000);

    // Cross-post to Bluesky & Mastodon
    try {
      console.log(`\n🚀 Cross-posting to Bluesky & Mastodon: "${nextArticleToPost.title}"...`);

      // 1. Post to Bluesky
      let bskyResult = null;
      try {
        bskyResult = await postArticleToBluesky(nextArticleToPost);
      } catch (be) {
        console.error('Bluesky posting warning:', be.message);
      }

      // 2. Post to Mastodon
      let mstdResult = null;
      try {
        mstdResult = await postArticleToMastodon(nextArticleToPost);
      } catch (me) {
        console.error('Mastodon posting warning:', me.message);
      }

      // Record if at least one succeeded or both
      if (bskyResult || mstdResult) {
        history.postedIds.push(nextArticleToPost.id);
        history.history.push({
          id: nextArticleToPost.id,
          title: nextArticleToPost.title,
          category: nextArticleToPost.category,
          postedAt: new Date().toISOString(),
          bskyUri: bskyResult ? bskyResult.uri : null,
          mastodonUrl: mstdResult ? mstdResult.url : null
        });
        saveHistory(history);

        // Also update individual tracker files for backward compatibility
        try {
          if (bskyResult) fs.writeFileSync(lastBskyFile, nextArticleToPost.id, 'utf8');
          if (mstdResult) fs.writeFileSync(lastMstdFile, nextArticleToPost.id, 'utf8');
        } catch (e) {}

        console.log(`✅ Logged in scripts/social-history.json! Total posted so far: ${history.postedIds.length}\n`);
      } else {
        console.error(`⚠️ Both platforms failed for "${nextArticleToPost.title}". Will retry in next cycle...`);
      }
    } catch (err) {
      console.error('Error during auto-post execution:', err.message);
    }
  }
}

if (require.main === module) {
  runScheduler().catch(err => {
    console.error('Fatal scheduler error:', err);
  });
}

module.exports = { runScheduler };
