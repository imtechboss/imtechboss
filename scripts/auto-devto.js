const fs = require('fs');
const path = require('path');
const vm = require('vm');

const DEVTO_API_KEY = process.env.DEVTO_API_KEY || 'ZtmMvBpzm7EgsBquEstMv5mq';
const projectRoot = path.resolve(__dirname, '..');
const dataPath = path.join(projectRoot, 'js', 'data.js');
const historyFile = path.join(__dirname, 'devto-history.json');
const trackerFile = path.join(projectRoot, '.last_devto_id.txt');

// Load articles from js/data.js
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

// Load Dev.to publishing history
function loadHistory() {
  if (fs.existsSync(historyFile)) {
    try {
      return JSON.parse(fs.readFileSync(historyFile, 'utf8'));
    } catch (e) {
      console.warn('⚠️ Warning reading devto-history.json:', e.message);
    }
  }
  return { postedIds: [], history: [] };
}

function saveHistory(historyData) {
  fs.writeFileSync(historyFile, JSON.stringify(historyData, null, 2), 'utf8');
}

// Convert HTML content from article to clean Markdown suitable for Dev.to
function htmlToMarkdown(html) {
  if (!html) return '';
  let md = html;
  
  // Tables: convert <table> to GitHub Flavored Markdown table
  md = md.replace(/\u003ctable[^\u003e]*\u003e([\\s\\S]*?)\u003c\/table\u003e/gi, (match, tableContent) => {
    const rows = [];
    const trMatches = tableContent.match(/\u003ctr[^\u003e]*\u003e([\\s\\S]*?)\u003c\/tr\u003e/gi) || [];
    let isHeader = true;
    for (const tr of trMatches) {
      const cells = [];
      const cellMatches = tr.match(/\u003c(th|td)[^\u003e]*\u003e([\\s\\S]*?)\u003c\/(th|td)\u003e/gi) || [];
      for (const cell of cellMatches) {
        let text = cell.replace(/\u003c[^\u003e]+\u003e/g, '').trim().replace(/\\|/g, '\\\\|');
        text = text.replace(/\u0026amp;/g, '&').replace(/\u0026quot;/g, '"').replace(/\u0026#39;/g, "'").replace(/\u0026lt;/g, '<').replace(/\u0026gt;/g, '>');
        cells.push(text);
      }
      if (cells.length > 0) {
        rows.push('| ' + cells.join(' | ') + ' |');
        if (isHeader) {
          rows.push('| ' + Array(cells.length).fill('---').join(' | ') + ' |');
          isHeader = false;
        }
      }
    }
    // Ensure blank lines before and after the table markdown
    return rows.length > 0 ? '\n\n' + rows.join('\n') + '\n\n' : '';
  });

  // Headings
  md = md.replace(/\u003ch2[^\u003e]*\u003e(.*?)\u003c\/h2\u003e/gi, '\n\n## $1\n\n');
  md = md.replace(/\u003ch3[^\u003e]*\u003e(.*?)\u003c\/h3\u003e/gi, '\n\n### $1\n\n');
  md = md.replace(/\u003ch4[^\u003e]*\u003e(.*?)\u003c\/h4\u003e/gi, '\n\n#### $1\n\n');

  // Lists
  md = md.replace(/\u003cli[^\u003e]*\u003e(.*?)\u003c\/li\u003e/gi, '- $1\n');
  md = md.replace(/\u003c\/?(ul|ol)[^\u003e]*\u003e/gi, '\n');

  // Blockquotes
  md = md.replace(/\u003cblockquote[^\u003e]*\u003e(.*?)\u003c\/blockquote\u003e/gis, (m, c) => {
    const inner = c.replace(/\u003cp[^\u003e]*\u003e(.*?)\u003c\/p\u003e/gi, '$1\n> ').trim();
    return `\n> ${inner}\n\n`;
  });

  // Paragraphs
  md = md.replace(/\u003cp[^\u003e]*\u003e(.*?)\u003c\/p\u003e/gis, '$1\n\n');

  // Bold, italic, code
  md = md.replace(/\u003cstrong[^\u003e]*\u003e(.*?)\u003c\/strong\u003e/gi, '**$1**');
  md = md.replace(/\u003cb[^\u003e]*\u003e(.*?)\u003c\/b\u003e/gi, '**$1**');
  md = md.replace(/\u003cem[^\u003e]*\u003e(.*?)\u003c\/em\u003e/gi, '*$1*');
  md = md.replace(/\u003ci[^\u003e]*\u003e(.*?)\u003c\/i\u003e/gi, '*$1*');
  md = md.replace(/\u003ccode[^\u003e]*\u003e(.*?)\u003c\/code\u003e/gi, '`$1`');

  // Strip remaining tags
  md = md.replace(/\u003c[^\u003e]+\u003e/g, '');

  // Decode common HTML entities
  md = md.replace(/\u0026amp;/g, '&')
    .replace(/\u0026quot;/g, '"')
    .replace(/\u0026#39;/g, "'")
    .replace(/\u0026lt;/g, '<')
    .replace(/\u0026gt;/g, '>')
    .replace(/\u0026mdash;/g, '—')
    .replace(/\u0026ndash;/g, '–');

  // Ensure a blank line before any table start if missing
  md = md.replace(/\n\|/g, '\n\n|');

  // Normalize extra whitespace and newlines
  md = md.replace(/\n{3,}/g, '\n\n').trim();
  return md;
}

// Generate valid Dev.to tags (max 4, lowercase alphanumeric)
function getDevToTags(article) {
  const cat = (article.category || '').toLowerCase();
  const title = (article.title || '').toLowerCase();
  const text = `${cat} ${title}`;
  
  const tags = new Set();
  if (text.includes('how to') || text.includes('guide') || text.includes('fix')) tags.add('tutorial');
  if (text.includes('windows')) tags.add('windows');
  if (text.includes('game') || text.includes('gaming')) tags.add('gaming');
  if (text.includes('security') || text.includes('vpn') || text.includes('privacy')) tags.add('security');
  if (text.includes('wifi') || text.includes('dns') || text.includes('network')) tags.add('devops');
  if (text.includes('quantum')) tags.add('quantum');
  if (text.includes('llama') || text.includes('llm') || text.includes('gpt') || text.includes('claude') || text.includes('ai')) tags.add('ai');
  if (text.includes('gpu') || text.includes('hardware') || text.includes('nvidia') || text.includes('chip') || text.includes('cpu')) tags.add('hardware');
  if (text.includes('open-weights') || text.includes('open source') || text.includes('opensource')) tags.add('opensource');
  if (text.includes('coding') || text.includes('software') || text.includes('programming') || text.includes('developer')) tags.add('programming');
  if (text.includes('web') || text.includes('browser')) tags.add('webdev');
  
  if (tags.size === 0) tags.add('technology');
  if (tags.size < 4) tags.add('tech');
  
  return Array.from(tags).slice(0, 4);
}

// Publish an article object to DEV.to
async function publishArticleToDevTo(article, options = {}) {
  const canonicalUrl = `https://imtechboss.com/${article.id}/`;
  
  // Format body markdown from full article content or excerpt
  let bodyMarkdown = '';
  if (article.content && article.content.length > 200) {
    bodyMarkdown = htmlToMarkdown(article.content);
  } else {
    bodyMarkdown = `${article.excerpt || ''}\n\n`;
    bodyMarkdown += `### About This Technical Analysis\nIn late 2026, technology is evolving faster than ever. This guide explores the core technical architecture, benchmark metrics, and practical implementations.\n\n`;
  }
  
  // Append canonical citation and dynamic tailored CTA footer
  const cat = (article.category || '').toLowerCase();
  const title = (article.title || '').toLowerCase();
  let ctaText = 'Explore interactive engineering tools, real-time performance diagnostics, and tech insights at [imtechboss.com](https://imtechboss.com).';
  if (cat.includes('hard') || cat.includes('gam') || title.includes('gpu') || title.includes('cpu') || title.includes('ps6') || title.includes('zen 6')) {
    ctaText = 'Explore hardware telemetry benchmarks, GPU architecture breakdowns, and interactive spec comparisons at [imtechboss.com](https://imtechboss.com).';
  } else if (cat.includes('ai') || title.includes('llm') || title.includes('gpt') || title.includes('model') || title.includes('reasoning')) {
    ctaText = 'Explore deep neural architecture benchmarks, local LLM quantization guides, and AI tools at [imtechboss.com](https://imtechboss.com).';
  } else if (title.includes('windows') || title.includes('wifi') || title.includes('fix') || title.includes('how to')) {
    ctaText = 'Explore step-by-step operating system optimizations, kernel latency fixes, and systems tools at [imtechboss.com](https://imtechboss.com).';
  }

  bodyMarkdown += `\n\n---\n\n*Originally published on [Tech Boss (${article.title})](${canonicalUrl}) — ${ctaText}*`;
  
  const tags = getDevToTags(article);
  
  const image = (article.image && article.image.startsWith('http')) 
    ? article.image 
    : (article.image ? `https://imtechboss.com/${article.image.replace(/^\/+/, '')}` : undefined);

  const payload = {
    article: {
      title: article.title,
      published: true,
      body_markdown: bodyMarkdown,
      tags: tags,
      canonical_url: canonicalUrl,
      main_image: image
    }
  };

  if (options.dryRun) {
    console.log('🧪 DRY RUN MODE — Not sending to Dev.to');
    console.log('Title:', payload.article.title);
    console.log('Tags:', payload.article.tags);
    console.log('Canonical URL:', payload.article.canonical_url);
    console.log('Image:', payload.article.main_image);
    console.log('Body length:', payload.article.body_markdown.length, 'chars');
    console.log('\nPreview:\n' + payload.article.body_markdown.slice(0, 500) + '...\n');
    return { ok: true, dryRun: true };
  }

  console.log(`📤 Publishing to DEV.to: "${article.title}"...`);
  const res = await fetch('https://dev.to/api/articles', {
    method: 'POST',
    headers: {
      'api-key': DEVTO_API_KEY,
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    },
    body: JSON.stringify(payload)
  });

  const rawText = await res.text();
  let data = {};
  try {
    data = JSON.parse(rawText);
  } catch (e) {
    console.error(`❌ DEV.to API returned non-JSON response (Status ${res.status}):`);
    console.error(rawText.slice(0, 300));
    return { ok: false, error: `HTTP ${res.status}: Non-JSON response` };
  }

  if (res.ok) {
    console.log('✅ Successfully published to DEV.to!');
    console.log('🔗 URL:', data.url);
    console.log('🆔 DEV.to Article ID:', data.id);
    
    // Update tracking
    const history = loadHistory();
    if (!history.postedIds.includes(article.id)) {
      history.postedIds.push(article.id);
    }
    history.history.push({
      id: article.id,
      devto_id: data.id,
      url: data.url,
      postedAt: new Date().toISOString()
    });
    saveHistory(history);
    fs.writeFileSync(trackerFile, article.id, 'utf8');
    
    return { ok: true, data };
  } else {
    console.error('❌ Failed to publish to DEV.to:', data);
    return { ok: false, error: data };
  }
}

// CLI entry point
async function main() {
  const args = process.argv.slice(2);
  const isDryRun = args.includes('--dry-run');
  const targetId = args.find(a => !a.startsWith('--'));

  const articles = loadArticles();
  if (!articles.length) {
    console.error('No articles loaded.');
    process.exit(1);
  }

  let targetArticle = null;
  if (targetId) {
    targetArticle = articles.find(a => a.id === targetId);
    if (!targetArticle) {
      console.error(`Article with ID "${targetId}" not found in js/data.js`);
      process.exit(1);
    }
  } else {
    const history = loadHistory();
    // Find latest article that has not yet been posted
    targetArticle = articles.find(a => !history.postedIds.includes(a.id));
    if (!targetArticle) {
      console.log('🎉 All articles have already been published to DEV.to!');
      process.exit(0);
    }
  }

  const result = await publishArticleToDevTo(targetArticle, { dryRun: isDryRun });
  if (!result.ok && !result.dryRun) {
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  publishArticleToDevTo,
  htmlToMarkdown,
  getDevToTags
};
