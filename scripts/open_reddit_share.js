const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const dataPath = path.join(__dirname, '..', 'js', 'data.js');
const content = fs.readFileSync(dataPath, 'utf8');

const match = content.match(/var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);/);
if (!match) {
  console.error("Could not find initialArticles");
  process.exit(1);
}

const articles = JSON.parse(match[1]);

// Get article (latest by default or by ID)
const targetId = process.argv[2];
const article = targetId ? articles.find(a => a.id === targetId) : articles[0];

if (!article) {
  console.error("Article not found");
  process.exit(1);
}

const articleUrl = `https://imtechboss.com/post.html?id=${article.id}`;
const redditTitle = article.title;

// Direct submit URL for Reddit:
const redditUrl = `https://www.reddit.com/submit?url=${encodeURIComponent(articleUrl)}&title=${encodeURIComponent(redditTitle)}`;

console.log(`\n======================================================`);
console.log(`🚀 1-CLICK REDDIT SUBMISSION FOR:`);
console.log(`"${article.title}"`);
console.log(`======================================================\n`);
console.log(`👉 Direct Clickable Reddit Link:\n${redditUrl}\n`);
console.log(`(Yo link browser ma kholna saath Title ra Link aafai fill hunchha, khali Post ma click gare pugchha!)\n`);

// Optionally open in default browser if argument is --open
if (process.argv.includes('--open')) {
  console.log("Opening in browser...");
  const cmd = process.platform === 'win32' ? `start "" "${redditUrl}"` : `open "${redditUrl}"`;
  exec(cmd);
}
