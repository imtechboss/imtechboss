const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, '..', 'js', 'data.js');
const content = fs.readFileSync(dataPath, 'utf8');

const match = content.match(/var\s+initialArticles\s*=\s*(\[[\s\S]*?\]);/);
if (!match) {
  console.error("Could not find initialArticles in data.js");
  process.exit(1);
}

const articles = JSON.parse(match[1]);

function cleanHtml(html) {
  return html
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .trim();
}

function extractKeyBullets(article) {
  const content = article.content || '';
  // Find lists or strong sentences
  const listMatches = content.match(/<li>([\s\S]*?)<\/li>/g);
  if (listMatches && listMatches.length >= 3) {
    return listMatches.slice(0, 4).map(li => cleanHtml(li));
  }
  // Otherwise split paragraphs
  const pMatches = content.match(/<p>([\s\S]*?)<\/p>/g);
  if (pMatches) {
    return pMatches.slice(0, 4).map(p => cleanHtml(p).slice(0, 180) + '...');
  }
  return [article.excerpt];
}

function generateRedditPost(article) {
  const bullets = extractKeyBullets(article);
  const bulletMd = bullets.map(b => `* ${b}`).join('\n');
  const url = `https://imtechboss.com/post.html?id=${article.id}`;

  return `### Reddit Post Format (r/hardware, r/technology, r/buildapc, r/pcmasterrace)
**Suggested Title:** ${article.title}

**Post Body (Copy & Paste as Markdown):**
**TL;DR:** ${article.excerpt}

---

### Key Technical Breakdown & Findings:
${bulletMd}

### Technical Verdict / Discussion:
Modern architectural bottlenecks show how crucial memory bandwidth, firmware security, and hardware margins have become in 2026 systems. 

**Community Discussion:**
* What are your thoughts on these findings?
* Has your rig encountered this issue or are you planning a hardware upgrade this cycle?

---
*Full technical benchmarks, comparative data tables, and diagnostic walk-through:* 
[Read the full report on Tech Boss](${url})
`;
}

function generateHackerNewsPost(article) {
  const url = `https://imtechboss.com/post.html?id=${article.id}`;
  return `### Hacker News Submission (news.ycombinator.com)
**Title:** ${article.title.replace(/\b(Is The.*Worth It\?|Complete 2026 Guide)\b/gi, '').trim()}
**URL:** ${url}

**Optional Top Comment:**
I put together an architectural and diagnostic breakdown analyzing the engineering details behind this:
- **Core Observation:** ${article.excerpt}
- Focuses on real-world trace data and hardware metrics rather than vendor marketing.
`;
}

function generateDiscordPost(article) {
  const url = `https://imtechboss.com/post.html?id=${article.id}`;
  const bullets = extractKeyBullets(article).slice(0, 3);
  return `### Discord / Telegram Community Format
🔥 **${article.title}**
> ${article.excerpt}

📌 **Key Highlights:**
${bullets.map(b => `• ${b}`).join('\n')}

👉 **Read Full Breakdown:** ${url}
`;
}

// Check CLI arguments
const requestedId = process.argv[2];
let targetArticles = [];

if (requestedId) {
  const found = articles.find(a => a.id === requestedId);
  if (!found) {
    console.error(`Article with ID '${requestedId}' not found.`);
    process.exit(1);
  }
  targetArticles = [found];
} else {
  // Take top 3 articles
  targetArticles = articles.slice(0, 3);
}

let fullMarkdownOutput = `# Tech Boss — Social Summary & Reddit/Hacker News Distribution Kit
Generated on: ${new Date().toISOString().split('T')[0]}

Use these pre-formatted, high-value technical summaries to share on Reddit, Hacker News, Discord, and forums to drive engaged organic referral traffic without link-spam penalties.

`;

for (const art of targetArticles) {
  fullMarkdownOutput += `\n================================================================================\n`;
  fullMarkdownOutput += `## Article: ${art.title}\n`;
  fullMarkdownOutput += `**ID:** \`${art.id}\` | **Category:** ${art.category}\n\n`;
  fullMarkdownOutput += generateRedditPost(art) + "\n\n";
  fullMarkdownOutput += generateHackerNewsPost(art) + "\n\n";
  fullMarkdownOutput += generateDiscordPost(art) + "\n";
}

const outputPath = path.join(__dirname, '..', 'social_summaries.md');
fs.writeFileSync(outputPath, fullMarkdownOutput, 'utf8');

console.log(`\nSuccessfully exported summaries for ${targetArticles.length} article(s)!`);
console.log(`Saved to: social_summaries.md`);
if (targetArticles.length === 1) {
  console.log(`\nPreview for '${targetArticles[0].title}':\n`);
  console.log(generateRedditPost(targetArticles[0]));
}
