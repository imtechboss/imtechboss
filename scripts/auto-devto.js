const fs = require('fs');
const path = require('path');
const vm = require('vm');

async function autoPostDevTo() {
  const apiKey = process.env.DEVTO_API_KEY || 'XdP5PGJyaQgncb6juY9DLbu2';
  const dataPath = path.join(__dirname, '..', 'js', 'data.js');
  const trackerFile = path.join(__dirname, '..', '.last_devto_id.txt');

  if (!fs.existsSync(dataPath)) return;

  const dataRaw = fs.readFileSync(dataPath, 'utf8');
  const ctx = {};
  vm.runInNewContext(dataRaw, ctx);
  const articles = ctx.initialArticles || [];

  if (articles.length === 0) return;

  // Find latest AI, tech or coding article suitable for dev.to
  const suitable = articles.find(a => 
    a.category.toLowerCase().includes('ai') || 
    a.category.toLowerCase().includes('cybersecurity') ||
    a.category.toLowerCase().includes('tech')
  ) || articles[0];

  let lastId = '';
  if (fs.existsSync(trackerFile)) {
    lastId = fs.readFileSync(trackerFile, 'utf8').trim();
  }

  if (suitable.id === lastId && process.env.FORCE_POST !== 'true') {
    console.log('Latest suitable article already posted to Dev.to. Skipping.');
    return;
  }

  const canonicalUrl = `https://imtechboss.com/post?id=${suitable.id}`;
  
  // Format body markdown from excerpt and sections
  let cleanBody = `${suitable.excerpt}\n\n`;
  cleanBody += `### About This Analysis\nIn late 2026, technology is evolving faster than ever. This guide explores the core technical architecture, benchmark metrics, and practical implementations.\n\n`;
  cleanBody += `---\n\n> 🚀 **Read the Complete In-Depth Guide on Tech Boss:**\n> [${suitable.title}](${canonicalUrl})\n`;

  const tags = (suitable.tags || []).slice(0, 4).map(t => t.toLowerCase().replace(/[^a-z0-9]/g, '')).filter(t => t.length > 1);

  const payload = {
    article: {
      title: suitable.title,
      published: true,
      body_markdown: cleanBody,
      tags: tags.length ? tags : ['tech', 'ai', 'programming'],
      canonical_url: canonicalUrl,
      main_image: (suitable.image && suitable.image.startsWith('http')) ? suitable.image : undefined
    }
  };

  const res = await fetch('https://dev.to/api/articles', {
    method: 'POST',
    headers: {
      'api-key': apiKey,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  if (res.ok) {
    console.log('Published to Dev.to:', data.url);
    fs.writeFileSync(trackerFile, suitable.id, 'utf8');
  } else {
    console.error('Failed to post to Dev.to:', data);
  }
}

autoPostDevTo();
