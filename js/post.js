// post.js - Dedicated Full-Page Article Reader for Tech Boss (Binod Bhatt)

document.addEventListener("DOMContentLoaded", () => {
  initPostTheme();
  initReadingProgressBar();
  initPostPageModal();
  renderPostDetail();
  initPostSecretAdminTrigger();

  setupSpotlightSearchPost();
  setupNewsletterPost();

  // Hash deep link support on post.html (e.g. post.html#about)
  const hash = window.location.hash.replace('#', '').toLowerCase();
  if (['about', 'contact', 'privacy', 'disclaimer'].includes(hash)) {
    setTimeout(() => openPostPageModal(hash), 150);
  }
});

function initPostSecretAdminTrigger() {
  let clicks = 0;
  let clickTimer = null;

  function handleAdminClick(e) {
    clearTimeout(clickTimer);
    clicks++;

    if (clicks === 2) {
      if (typeof showToast === 'function') {
        showToast("🔑 Click 1 more time for Admin Studio");
      }
    } else if (clicks >= 3) {
      if (typeof showToast === 'function') {
        showToast("🚀 Opening Admin Studio...");
      }
      setTimeout(() => {
        window.location.href = "admin.html";
      }, 250);
      return;
    }

    clickTimer = setTimeout(() => {
      clicks = 0;
    }, 2500);
  }

  document.querySelectorAll(".secret-admin-trigger, #secretAdminTrigger").forEach(el => {
    el.addEventListener("click", handleAdminClick);
  });

  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && !e.altKey && (e.key === "A" || e.key === "a")) {
      const el = document.activeElement;
      if (el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT' || el.isContentEditable)) return;
      e.preventDefault();
      window.location.href = "admin.html";
    }
  });
}

// 1. Theme Management (Sync with index.html)
function initPostTheme() {
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const sunIcon = document.getElementById("sunIcon");
  const moonIcon = document.getElementById("moonIcon");

  let savedTheme = null;
  try {
    savedTheme = localStorage.getItem("pulse_theme");
  } catch (e) {}

  const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const isDark = savedTheme === "dark" || (!savedTheme && systemDark);

  if (isDark) {
    document.documentElement.classList.add("dark");
    if (sunIcon) sunIcon.classList.remove("hidden");
    if (moonIcon) moonIcon.classList.add("hidden");
  } else {
    document.documentElement.classList.remove("dark");
    if (sunIcon) sunIcon.classList.add("hidden");
    if (moonIcon) moonIcon.classList.remove("hidden");
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
      const nowDark = document.documentElement.classList.toggle("dark");
      try {
        try { localStorage.setItem("pulse_theme", nowDark ? "dark" : "light"); } catch (e) {}
      } catch (e) {}

      if (nowDark) {
        if (sunIcon) sunIcon.classList.remove("hidden");
        if (moonIcon) moonIcon.classList.add("hidden");
        showToast("Dark mode activated");
      } else {
        if (sunIcon) sunIcon.classList.add("hidden");
        if (moonIcon) moonIcon.classList.remove("hidden");
        showToast("Light mode activated");
      }
    });
  }
}

// 2. Fetch and Render Article Details
function renderPostDetail() {
  try {
    const container = document.getElementById("articleContainer");
    const relatedSection = document.getElementById("relatedSection");
    const relatedGrid = document.getElementById("relatedGrid");

    if (!container) return;

    const urlParams = new URLSearchParams(window.location.search);
    const postId = urlParams.get("id");

    // Gather articles
    let customArticles = [];
    try {
      const storedCustom = localStorage.getItem("pulse_custom_posts");
      if (storedCustom) customArticles = JSON.parse(storedCustom);
      if (!Array.isArray(customArticles)) customArticles = [];
    } catch (e) {
      customArticles = [];
    }

  const baseArticles = (typeof initialArticles !== "undefined" && Array.isArray(initialArticles))
    ? initialArticles
    : [];

  const allArticles = [...customArticles, ...baseArticles];

  let targetId = postId;
  if (!targetId && allArticles.length > 0) {
    targetId = allArticles[0].id;
  }

  if (!targetId || allArticles.length === 0) {
    renderNotFound(container, "No story identifier was specified.");
    return;
  }

  const article = allArticles.find(a => String(a.id) === String(targetId));

  if (!article) {
    renderNotFound(container, `We couldn't find the story you requested.`);
    return;
  }

  // Update Page Title and Meta Tags
  document.title = `${article.title} — Tech Boss`;
  const metaDesc = document.getElementById("metaDescription");
  if (metaDesc && article.excerpt) {
    metaDesc.setAttribute("content", article.excerpt);
  }

  // Dynamic Open Graph & Twitter Card update for Social Sharing
  const ogUrl = document.getElementById("ogUrl");
  const ogTitle = document.getElementById("ogTitle");
  const ogDesc = document.getElementById("ogDescription");
  const ogImg = document.getElementById("ogImage");
  const twTitle = document.getElementById("twTitle");
  const twDesc = document.getElementById("twDescription");
  const twImg = document.getElementById("twImage");

  const canonicalHref = `https://imtechboss.com/post.html?id=${encodeURIComponent(article.id)}`;
  const canonicalUrl = document.getElementById("canonicalUrl");
  if (canonicalUrl) canonicalUrl.setAttribute("href", canonicalHref);
  if (ogUrl) ogUrl.setAttribute("content", canonicalHref);
  if (ogTitle) ogTitle.setAttribute("content", `${article.title} — Tech Boss`);
  if (twTitle) twTitle.setAttribute("content", `${article.title} — Tech Boss`);
  if (article.excerpt) {
    if (ogDesc) ogDesc.setAttribute("content", article.excerpt);
    if (twDesc) twDesc.setAttribute("content", article.excerpt);
  }

  const fullImgUrl = article.image 
    ? (article.image.startsWith("http") ? article.image : window.location.origin + '/' + article.image)
    : "https://imtechboss.com/og-image.png";

  if (ogImg) ogImg.setAttribute("content", fullImgUrl);
  if (twImg) twImg.setAttribute("content", fullImgUrl);

  // Dynamic Google Schema.org (JSON-LD) Structured Data for Rich Search Results
  try {
    let schemaScript = document.getElementById("articleJsonLd");
    if (!schemaScript) {
      schemaScript = document.createElement("script");
      schemaScript.id = "articleJsonLd";
      schemaScript.type = "application/ld+json";
      document.head.appendChild(schemaScript);
    }

    const schemaData = {
      "@context": "https://schema.org",
      "@type": "TechArticle",
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": currentHref
      },
      "headline": article.title,
      "description": article.excerpt || article.title,
      "image": [fullImgUrl],
      "datePublished": (() => { try { const d = new Date(article.timestamp || article.date); return !isNaN(d.getTime()) ? d.toISOString() : "2026-09-19T00:00:00Z"; } catch(e) { return "2026-09-19T00:00:00Z"; } })(),
      "dateModified": (() => { try { const d = new Date(article.timestamp || article.date); return !isNaN(d.getTime()) ? d.toISOString() : "2026-09-19T00:00:00Z"; } catch(e) { return "2026-09-19T00:00:00Z"; } })(),
      "author": {
        "@type": "Organization",
        "name": article.author?.name || "Tech Boss",
        "url": "https://imtechboss.com"
      },
      "publisher": {
        "@type": "Organization",
        "name": "Tech Boss",
        "logo": {
          "@type": "ImageObject",
          "url": "https://imtechboss.com/og-image.png"
        }
      }
    };
    schemaScript.textContent = JSON.stringify(schemaData);

    // BreadcrumbList Schema
    let breadcrumbScript = document.getElementById("breadcrumbJsonLd");
    if (!breadcrumbScript) {
      breadcrumbScript = document.createElement("script");
      breadcrumbScript.id = "breadcrumbJsonLd";
      breadcrumbScript.type = "application/ld+json";
      document.head.appendChild(breadcrumbScript);
    }
    const breadcrumbData = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://imtechboss.com" },
        { "@type": "ListItem", "position": 2, "name": article.category || "Article", "item": `https://imtechboss.com/?category=${encodeURIComponent(article.category || '')}` },
        { "@type": "ListItem", "position": 3, "name": article.title }
      ]
    };
    breadcrumbScript.textContent = JSON.stringify(breadcrumbData);
  } catch (e) {}

  // Handle Likes
  let likeCount = Number.isFinite(parseInt(article.likes, 10)) ? parseInt(article.likes, 10) : 0;
  let userHasLiked = false;
  try {
    userHasLiked = localStorage.getItem(`pulse_liked_${article.id}`) === "true";
    const storedLikes = localStorage.getItem(`pulse_like_count_${article.id}`);
    if (storedLikes) {
      const parsed = parseInt(storedLikes, 10);
      if (!isNaN(parsed)) likeCount = parsed;
    }
  } catch (e) {}

  // Handle Bookmarks
  let isBookmarked = false;
  let bookmarkedIds = new Set();
  try {
    const storedBookmarks = localStorage.getItem("pulse_bookmarks");
    if (storedBookmarks) {
      bookmarkedIds = new Set(JSON.parse(storedBookmarks));
      isBookmarked = bookmarkedIds.has(article.id);
    }
  } catch (e) {}

  // Calculate Accurate Dynamic Reading Time
  const rawText = (article.content || article.excerpt || "").replace(/<[^>]*>/g, " ");
  const wordCount = rawText.trim().split(/\s+/).filter(Boolean).length;
  const calculatedMins = Math.max(1, Math.round(wordCount / 180));
  const readTime = `${calculatedMins} min read`;

  // Process Clean HTML Content & In-Article AdSense Injection
  let articleBodyHtml = "";
  if (article.content && article.content.trim().length > 0) {
    articleBodyHtml = injectInArticleAdSense(article.content);
  } else if (article.excerpt) {
    articleBodyHtml = `<p>${escapeHtml(article.excerpt)}</p>`;
  } else {
    articleBodyHtml = `<p>Full content for this story is coming soon.</p>`;
  }

  const safeTitle = escapeHtml(article.title);
  const safeCat = escapeHtml(article.category || "General");
  const safeAuthor = escapeHtml(article.author?.name || "Tech Boss");
  const safeDate = escapeHtml(article.date || "Recent");
  const views = escapeHtml(article.views || "1.2K");
  const imgUrl = article.image || "";

  // Render Article Content
  container.innerHTML = `
    <!-- Top Meta Breadcrumb -->
    <div class="flex flex-wrap items-center justify-between gap-3 mb-6 pb-6 border-b border-gray-100 dark:border-slate-800 text-xs">
      <div class="flex items-center gap-2">
        <a href="index.html" class="text-gray-500 hover:text-blue-600 transition-colors">Home</a>
        <span class="text-gray-400">/</span>
        <span class="px-2.5 py-1 rounded-full font-bold bg-blue-50 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400">
          ${safeCat}
        </span>
      </div>
      <div class="flex items-center gap-3 text-gray-500 dark:text-gray-400">
        <span>📅 ${safeDate}</span>
        <span>•</span>
        <span>⏱️ ${readTime}</span>
        <span>•</span>
        <span>👁️ ${views} reads</span>
      </div>
    </div>

    <!-- Article Headline -->
    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-extrabold font-serif-heading text-gray-950 dark:text-white leading-[1.2] mb-6 tracking-tight">
      ${safeTitle}
    </h1>

    <!-- Author & Publisher Bar -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-gray-50 dark:bg-slate-800/60 border border-gray-200/70 dark:border-slate-800 mb-8">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white font-bold text-lg shadow ring-2 ring-white dark:ring-slate-700">
          ${safeAuthor.charAt(0)}
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h4 class="font-bold text-gray-900 dark:text-gray-100 text-sm sm:text-base">${safeAuthor}</h4>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300">Editor</span>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400">Tech Boss • imtechboss.com</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2">
        <button 
          id="likeBtn" 
          class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full border text-xs font-bold transition-all ${userHasLiked ? 'bg-red-50 border-red-200 text-red-600 dark:bg-red-950/40 dark:border-red-800' : 'bg-white dark:bg-slate-900 border-gray-200 dark:border-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800'}"
          title="Appreciate this story"
        >
          <span class="text-sm">${userHasLiked ? '❤️' : '🤍'}</span>
          <span id="likeCountDisplay">${likeCount}</span>
        </button>

        <button 
          id="bookmarkBtn" 
          class="p-2 rounded-full border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" 
          title="${isBookmarked ? 'Remove bookmark' : 'Bookmark story'}"
        >
          <svg class="w-4 h-4 ${isBookmarked ? 'fill-blue-600 text-blue-600' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
          </svg>
        </button>

        <button 
          id="copyLinkBtn" 
          class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors" 
          title="Copy link"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
          </svg>
          <span>Share</span>
        </button>
      </div>
    </div>

    <!-- Featured Hero Image (if available) -->
    ${imgUrl ? `
      <div class="mb-10 rounded-2xl overflow-hidden shadow-lg bg-gray-100 dark:bg-slate-800 border border-gray-200 dark:border-slate-800 max-h-[500px]">
        <img 
          src="${imgUrl}" 
          alt="${safeTitle}" 
          class="w-full h-full object-cover object-center"
          onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80'"
        >
      </div>
    ` : ''}

    <!-- Top Article Ad Banner -->
    <div class="ad-slot-box mb-8 text-center bg-gray-50 dark:bg-slate-800/60 rounded-2xl p-3 sm:p-4 border border-gray-200/80 dark:border-slate-800 not-prose overflow-hidden shadow-xs">
      <span class="text-[9px] uppercase font-bold tracking-widest text-gray-400 block mb-1.5">Sponsored / Advertisement</span>
      <!-- horizontal -->
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-pub-1043419685176632"
           data-ad-slot="9198547569"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
    </div>

    <!-- Rich Article Body -->
    <div class="article-body text-gray-800 dark:text-gray-200 leading-relaxed max-w-none">
      ${articleBodyHtml}
    </div>

    <!-- Social Share Bar & Tags -->
    <div class="mt-12 pt-8 border-t border-gray-200 dark:border-slate-800">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-gray-400">Share this story</span>
          <div class="flex items-center gap-2 mt-2">
            <!-- WhatsApp -->
            <a 
              href="https://api.whatsapp.com/send?text=${encodeURIComponent(article.title + ' ' + window.location.href)}" 
              target="_blank" 
              rel="noopener"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold transition-colors shadow-sm"
              title="Share on WhatsApp"
            >
              <span>WhatsApp</span>
            </a>

            <!-- Flipboard -->
            <a 
              href="https://share.flipboard.com/bookmarklet/popout?v=2&title=${encodeURIComponent(article.title)}&url=${encodeURIComponent('https://imtechboss.com/post.html?id=' + article.id + '&flip=1')}" 
              target="_blank" 
              rel="noopener"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#f52828] hover:bg-[#d41c1c] text-white text-xs font-bold transition-colors shadow-sm"
              title="Flip to Flipboard Magazine"
            >
              <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M0 0h8v24H0V0zm8 8h8v8H8V8zm0-8h16v8H8V0z"/></svg>
              <span>Flipboard</span>
            </a>

            <!-- Pinterest -->
            <a 
              href="https://pinterest.com/pin/create/button/?url=${encodeURIComponent('https://imtechboss.com/post.html?id=' + article.id)}&media=${encodeURIComponent(article.image ? (article.image.startsWith('http') ? article.image : 'https://imtechboss.com/' + article.image) : 'https://imtechboss.com/assets/banner.png')}&description=${encodeURIComponent(article.title)}" 
              target="_blank" 
              rel="noopener"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#e60023] hover:bg-[#ad081b] text-white text-xs font-bold transition-colors shadow-sm"
              title="Pin to Pinterest"
            >
              <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.373 0 0 5.372 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738.098.119.112.224.083.345-.09.375-.291 1.199-.334 1.357-.053.225-.172.271-.401.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.354-.629-2.758-1.379l-.749 2.848c-.269 1.045-1.004 2.352-1.498 3.146 1.123.345 2.306.535 3.55.535 6.627 0 12-5.373 12-12 0-6.628-5.373-12-12-12z"/></svg>
              <span>Pinterest</span>
            </a>

            <!-- Reddit -->
            <a 
              href="https://reddit.com/submit?url=${encodeURIComponent(window.location.href)}&title=${encodeURIComponent(article.title)}" 
              target="_blank" 
              rel="noopener"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#ff4500] hover:bg-[#e03d00] text-white text-xs font-bold transition-colors shadow-sm"
              title="Share on Reddit"
            >
              <span>Reddit</span>
            </a>

            <!-- X / Twitter -->
            <a 
              href="https://twitter.com/intent/tweet?text=${encodeURIComponent(article.title)}&url=${encodeURIComponent(window.location.href)}" 
              target="_blank" 
              rel="noopener"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-black dark:bg-slate-800 hover:bg-gray-800 text-white text-xs font-bold transition-colors shadow-sm"
              title="Share on X"
            >
              <span>X</span>
            </a>


            <!-- LinkedIn -->
            <a 
              href="https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}" 
              target="_blank" 
              rel="noopener"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#0077b5] hover:bg-[#006396] text-white text-xs font-bold transition-colors shadow-sm"
              title="Share on LinkedIn"
            >
              <span>LinkedIn</span>
            </a>

            <!-- Facebook -->
            <a 
              href="https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}" 
              target="_blank" 
              rel="noopener"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#1877f2] hover:bg-[#166fe5] text-white text-xs font-bold transition-colors shadow-sm"
              title="Share on Facebook"
            >
              <span>Facebook</span>
            </a>

            <!-- Copy Link -->
            <button 
              id="bottomCopyLinkBtn" 
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-gray-100 dark:bg-slate-800 hover:bg-gray-200 dark:hover:bg-slate-700 text-gray-700 dark:text-gray-300 text-xs font-bold transition-colors"
              title="Copy article link"
            >
              <span>Copy Link</span>
            </button>
          </div>
        </div>

        <button 
          id="scrollToTopBtn"
          class="text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1"
        >
          <span>Back to Top</span>
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/></svg>
        </button>
      </div>
    </div>

    <!-- Author Profile Card -->
    <div class="mt-10 p-6 sm:p-8 rounded-2xl bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-slate-800/80 dark:to-slate-900 border border-blue-100 dark:border-slate-700/60 flex flex-col sm:flex-row items-center sm:items-start gap-5">
      <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white font-extrabold text-2xl flex items-center justify-center flex-shrink-0 shadow-md">
        TB
      </div>
      <div class="text-center sm:text-left flex-1">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 class="text-lg font-bold font-sans text-gray-950 dark:text-white">Tech Boss</h3>
            <p class="text-xs text-blue-600 dark:text-blue-400 font-semibold">Editorial &amp; Engineering Team • imtechboss.com</p>
          </div>
          <a 
            href="mailto:binodbhatt500k@gmail.com" 
            class="inline-flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow transition-all self-center sm:self-auto"
          >
            <span>Get in Touch</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </a>
        </div>
        <p class="text-xs sm:text-sm text-gray-600 dark:text-gray-300 mt-3 leading-relaxed">
          Editorial team behind <strong>imtechboss.com</strong>. Curating educational tutorials, tech analyses, gaming walkthroughs, and creative digital resources for thousands of monthly readers.
        </p>
      </div>
    </div>

    <!-- Comments Section -->
    <div class="mt-12 pt-8 border-t border-gray-200 dark:border-slate-800">
      <h3 class="text-xl font-bold font-serif-heading mb-6 flex items-center justify-between">
        <span>Comments & Discussion</span>
        <span id="commentCountBadge" class="text-xs font-sans px-2.5 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300 font-bold">0</span>
      </h3>

      <!-- Post Comment Form -->
      <form id="postCommentForm" class="mb-8 p-4 sm:p-5 rounded-2xl bg-gray-50 dark:bg-slate-800/50 border border-gray-200 dark:border-slate-800">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
          <div>
            <label class="block text-[11px] font-bold text-gray-600 dark:text-gray-400 uppercase tracking-wider mb-1">Your Name</label>
            <input 
              type="text" 
              id="commentAuthor" 
              required 
              placeholder="e.g. Aabir" 
              class="w-full px-3 py-2 text-xs rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 dark:text-white"
            >
          </div>
          <div>
            <label class="block text-[11px] font-bold text-gray-600 dark:text-gray-400 uppercase tracking-wider mb-1">Email (Optional)</label>
            <input 
              type="email" 
              id="commentEmail" 
              placeholder="name@example.com" 
              class="w-full px-3 py-2 text-xs rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 dark:text-white"
            >
          </div>
        </div>
        <div class="mb-3">
          <label class="block text-[11px] font-bold text-gray-600 dark:text-gray-400 uppercase tracking-wider mb-1">Your Thoughts</label>
          <textarea 
            id="commentText" 
            required 
            rows="3" 
            placeholder="Write your feedback or question..." 
            class="w-full px-3 py-2 text-xs rounded-xl bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 dark:text-white"
          ></textarea>
        </div>
        <div class="flex justify-end">
          <button 
            type="submit" 
            class="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow hover:shadow-md transition-all active:scale-95"
          >
            Post Comment
          </button>
        </div>
      </form>

      <!-- Comments List -->
      <div id="commentsList" class="space-y-3">
        <!-- Rendered via JS -->
      </div>
    </div>
  `;

  // Attach interactive button listeners
  setupInteractivePostActions(article, likeCount, userHasLiked, isBookmarked, bookmarkedIds);

  // Render Comments
  renderComments(article.id);

  // Handle broken images gracefully
  container.querySelectorAll(".article-body img").forEach(img => {
    const hideBrokenImage = () => {
      img.style.display = "none";
      const parentA = img.closest("a");
      if (parentA && parentA.children.length === 1 && !parentA.textContent.trim()) {
        parentA.style.display = "none";
      }
    };
    img.addEventListener("error", hideBrokenImage);
    if (img.complete && (img.naturalWidth === 0 || img.naturalHeight === 0)) { hideBrokenImage(); }
  });

  // Ensure all links inside content open in a new tab safely
  container.querySelectorAll(".article-body a").forEach(link => {
    const href = link.getAttribute("href");
    if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
    try {
      const url = new URL(href, window.location.href);
      if (url.origin !== window.location.origin) {
        link.setAttribute("target", "_blank");
        link.setAttribute("rel", "noopener noreferrer");
      }
    } catch (e) {}
  });

  // Generate Table of Contents
  generateTableOfContents(container);

  // Setup 1-Click Code Copy Buttons
  setupCodeCopyButtons(container);

  // Setup High-Converting Resource Download Counter
  setupDownloadCounters(container);

  // Render Related Articles & Unhide Section (Increases Pageviews & Impressions)
  renderRelatedArticles(article);

  // Setup Floating "Read Next" Story Widget (Boosts Read-through & Multi-page visits)
  setupFloatingReadNext(article);

  // Trigger AdSense for dynamically injected in-article ad slots
  setTimeout(() => {
    try {
      const dynamicAds = container.querySelectorAll("ins.adsbygoogle:not([data-adsbygoogle-status])");
      dynamicAds.forEach((ad) => {
        try {
          // Only skip truly hidden containers (e.g. side-ad-gutter on mobile)
          const parentGutter = ad.closest('.side-ad-gutter');
          if (parentGutter && getComputedStyle(parentGutter).display === 'none') return;
          // Prevent availableWidth=0 errors on hidden/collapsed containers
          if (ad.offsetWidth === 0) return;
          (window.adsbygoogle = window.adsbygoogle || []).push({});
        } catch (err) {
          console.warn("In-article AdSense push:", err);
        }
      });
    } catch (e) {}
  }, 300);

  // Clean up unfilled AdSense slots (hide empty boxes when no ads available)
  try {
    const handleUnfilled = (adEl) => {
      if (adEl.getAttribute("data-ad-status") === "unfilled") {
        const gutter = adEl.closest(".side-ad-gutter");
        if (gutter) gutter.style.display = "none";
        const box = adEl.closest(".ad-slot-box");
        if (box && !gutter) box.style.display = "none";
      }
    };
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((m) => {
        if (m.type === "attributes" && m.attributeName === "data-ad-status") {
          handleUnfilled(m.target);
        }
      });
    });
    document.querySelectorAll("ins.adsbygoogle").forEach((ad) => {
      handleUnfilled(ad);
      observer.observe(ad, { attributes: true, attributeFilter: ["data-ad-status"] });
    });
  } catch (err) {}


  // Render Related Articles
  // renderRelatedStories(allArticles, article, relatedSection, relatedGrid);

  // Scroll to top button
  const topBtn = document.getElementById("scrollToTopBtn");
  if (topBtn) {
    topBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
  } catch (e) {
    renderNotFound(container, "An unexpected error occurred while loading this story.");
    console.error(e);
  }
}

// 3. Interactive Post Actions (Like, Bookmark, Copy Link)
function setupInteractivePostActions(article, initialLikes, userHasLiked, initialBookmarked, bookmarkedIds) {
  let likes = Number.isFinite(initialLikes) ? Math.max(0, initialLikes) : 0;
  let hasLiked = userHasLiked;
  let isBookmarked = initialBookmarked;

  const likeBtn = document.getElementById("likeBtn");
  const likeCountDisplay = document.getElementById("likeCountDisplay");
  const bookmarkBtn = document.getElementById("bookmarkBtn");
  const copyLinkBtn = document.getElementById("copyLinkBtn");

  if (likeBtn && likeCountDisplay) {
    likeBtn.addEventListener("click", () => {
      if (!hasLiked) {
        likes += 1;
        hasLiked = true;
        likeBtn.className = "inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full border text-xs font-bold transition-all bg-red-50 border-red-200 text-red-600 dark:bg-red-950/40 dark:border-red-800";
        likeBtn.querySelector("span").textContent = "❤️";
        likeCountDisplay.textContent = likes;
        likeBtn.setAttribute('title', 'Unlike this story');
        likeBtn.setAttribute('aria-label', 'Unlike this story');
        showToast("❤️ Thank you for liking this story!");
      } else {
        likes = Math.max(0, likes - 1);
        hasLiked = false;
        likeBtn.className = "inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full border text-xs font-bold transition-all bg-white dark:bg-slate-900 border-gray-200 dark:border-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800";
        likeBtn.querySelector("span").textContent = "🤍";
        likeCountDisplay.textContent = likes;
        likeBtn.setAttribute('title', 'Appreciate this story');
        likeBtn.setAttribute('aria-label', 'Appreciate this story');
      }
      try {
        try { localStorage.setItem(`pulse_liked_${article.id}`, hasLiked ? "true" : "false"); } catch (e) {}
        try { localStorage.setItem(`pulse_like_count_${article.id}`, String(likes)); } catch (e) {}
      } catch (e) {}
    });
  }

  if (bookmarkBtn) {
    bookmarkBtn.addEventListener("click", () => {
      if (isBookmarked) {
        bookmarkedIds.delete(article.id);
        isBookmarked = false;
        bookmarkBtn.innerHTML = `
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
          </svg>
        `;
        bookmarkBtn.setAttribute('title', 'Bookmark story');
        bookmarkBtn.setAttribute('aria-label', 'Bookmark story');
        showToast("Story removed from bookmarks");
      } else {
        bookmarkedIds.add(article.id);
        isBookmarked = true;
        bookmarkBtn.innerHTML = `
          <svg class="w-4 h-4 fill-blue-600 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
          </svg>
        `;
        bookmarkBtn.setAttribute('title', 'Remove bookmark');
        bookmarkBtn.setAttribute('aria-label', 'Remove bookmark');
        showToast("Story saved to bookmarks!");
      }
      try {
        try { localStorage.setItem("pulse_bookmarks", JSON.stringify(Array.from(bookmarkedIds))); } catch (e) {}
      } catch (e) {}
    });
  }

  const fallbackCopy = (text) => {
    try {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      showToast("🔗 Link copied to clipboard!");
    } catch (e) {
      promptCopy(text);
    }
  };

  const handleCopyLink = () => {
    const url = window.location.href;
    const title = document.title;
    // Use native share on mobile if available
    if (navigator.share) {
      navigator.share({ title, url })
        .catch(() => {}); // User cancelled share dialog
      return;
    }
    if (window.isSecureContext && navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      navigator.clipboard.writeText(url)
        .then(() => showToast("🔗 Link copied to clipboard!"))
        .catch(() => fallbackCopy(url));
    } else {
      fallbackCopy(url);
    }
  };

  if (copyLinkBtn) {
    copyLinkBtn.addEventListener("click", handleCopyLink);
  }

  const bottomCopyLinkBtn = document.getElementById("bottomCopyLinkBtn");
  if (bottomCopyLinkBtn) {
    bottomCopyLinkBtn.addEventListener("click", handleCopyLink);
  }

  // Handle Comment Submission
  const commentForm = document.getElementById("postCommentForm");
  if (commentForm) {
    commentForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const authorInput = document.getElementById("commentAuthor");
      const textInput = document.getElementById("commentText");

      const author = authorInput.value.trim();
      const text = textInput.value.trim();

      if (!author || !text) return;

      let commentsStore = {};
      try {
        const stored = localStorage.getItem("pulse_comments");
        if (stored) commentsStore = JSON.parse(stored);
      } catch (e) {}

      if (!commentsStore[article.id]) {
        commentsStore[article.id] = [];
      }

      const newComment = {
        id: "c-" + Date.now(),
        author,
        text,
        date: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
      };

      commentsStore[article.id].unshift(newComment);

      try {
        try { localStorage.setItem("pulse_comments", JSON.stringify(commentsStore)); } catch (e) {}
      } catch (e) {}

      authorInput.value = "";
      textInput.value = "";

      showToast("💬 Comment posted successfully!");
      renderComments(article.id);
    });
  }
}

function promptCopy(text) {
  window.prompt("Copy this link to share:", text);
}

// 4. Render Comments List
function renderComments(articleId) {
  const commentsList = document.getElementById("commentsList");
  const countBadge = document.getElementById("commentCountBadge");
  if (!commentsList) return;

  let commentsStore = {};
  try {
    const stored = localStorage.getItem("pulse_comments");
    if (stored) commentsStore = JSON.parse(stored);
  } catch (e) {}

  const raw = commentsStore[articleId];
  const comments = Array.isArray(raw) ? raw : [];

  if (countBadge) {
    countBadge.textContent = comments.length;
  }

  if (comments.length === 0) {
    commentsList.innerHTML = `
      <div class="text-center py-8 px-4 rounded-xl bg-gray-50 dark:bg-slate-800/40 border border-dashed border-gray-200 dark:border-slate-800">
        <p class="text-xs text-gray-500 dark:text-gray-400">No comments yet. Be the first to share your thoughts on this story!</p>
      </div>
    `;
    return;
  }

  commentsList.innerHTML = comments.filter(c => c && typeof c === 'object' && c.author && c.text).map(c => `
    <div class="p-4 rounded-xl bg-gray-50 dark:bg-slate-800/60 border border-gray-200/80 dark:border-slate-800 text-xs">
      <div class="flex items-center justify-between mb-1.5">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 rounded-full bg-blue-600 text-white font-bold text-[10px] flex items-center justify-center">
            ${escapeHtml(c.author).charAt(0).toUpperCase()}
          </div>
          <span class="font-bold text-gray-900 dark:text-gray-100">${escapeHtml(c.author)}</span>
        </div>
        <span class="text-[10px] text-gray-400">${escapeHtml(c.date || 'Recent')}</span>
      </div>
      <p class="text-gray-700 dark:text-gray-300 leading-relaxed pl-8">
        ${escapeHtml(c.text)}
      </p>
    </div>
  `).join("");
}

// 5. Render Related Stories
function renderRelatedStories(allArticles, currentArticle, relatedSection, relatedGrid) {
  if (!relatedSection || !relatedGrid) return;

  // Find 3 other articles from same category, or newest
  let related = allArticles.filter(a => String(a.id) !== String(currentArticle.id) && a.category === currentArticle.category);
  if (related.length < 3) {
    const additional = allArticles.filter(a => String(a.id) !== String(currentArticle.id) && !related.some(r => String(r.id) === String(a.id)));
    related = [...related, ...additional];
  }
  related = related.slice(0, 3);

  if (related.length === 0) {
    relatedSection.classList.add("hidden");
    return;
  }

  relatedSection.classList.remove("hidden");
  relatedGrid.innerHTML = related.map(rel => {
    const safeTitle = escapeHtml(rel.title);
    const safeCat = escapeHtml(rel.category || "General");
    const safeDate = escapeHtml(rel.date || "Recent");
    const imgUrl = rel.image || "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=400&q=80";

    return `
      <a 
        href="post.html?id=${encodeURIComponent(rel.id)}" 
        class="group flex flex-col bg-white dark:bg-slate-900 rounded-2xl overflow-hidden border border-gray-200 dark:border-slate-800 shadow-sm hover:shadow-md hover:border-blue-500/40 transition-all p-3"
      >
        <div class="aspect-[16/10] rounded-xl overflow-hidden bg-gray-100 dark:bg-slate-800 mb-3">
          <img 
            src="${imgUrl}" 
            alt="${safeTitle}" 
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=400&q=80'"
          >
        </div>
        <span class="text-[10px] font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider mb-1">
          ${safeCat}
        </span>
        <h4 class="font-bold text-xs sm:text-sm text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-2 leading-snug">
          ${safeTitle}
        </h4>
        <div class="mt-auto pt-2 text-[10px] text-gray-400 flex items-center justify-between">
          <span>${safeDate}</span>
          <span class="font-semibold text-blue-600 dark:text-blue-400 group-hover:translate-x-0.5 transition-transform">Read Story →</span>
        </div>
      </a>
    `;
  }).join("");
}

// 6. Not Found Fallback
function renderNotFound(container, message) {
  container.innerHTML = `
    <div class="text-center py-20 sm:py-28 px-4">
      <div class="w-16 h-16 rounded-2xl bg-red-100 dark:bg-red-950/50 text-red-600 dark:text-red-400 flex items-center justify-center text-3xl mx-auto mb-4 font-bold">
        !
      </div>
      <h2 class="text-2xl sm:text-3xl font-bold font-serif-heading text-gray-900 dark:text-white mb-2">
        Story Not Found
      </h2>
      <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto mb-6">
        ${message} It may have been archived or moved.
      </p>
      <a 
        href="index.html" 
        class="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md hover:shadow-lg transition-all"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
        <span>Return to Homepage</span>
      </a>
    </div>
  `;
}

// 7. Toast Notification Utility
let toastTimer = null;
const toastQueue = [];
let isToastShowing = false;

function showToast(message) {
  toastQueue.push(message);
  if (!isToastShowing) processToastQueue();
}

function processToastQueue() {
  if (toastQueue.length === 0) { isToastShowing = false; return; }
  isToastShowing = true;
  const message = toastQueue.shift();
  const toast = document.getElementById("toastNotification");
  const msgEl = document.getElementById("toastMessage");
  if (!toast || !msgEl) { isToastShowing = false; return; }

  msgEl.textContent = message;
  toast.classList.remove("translate-y-20", "opacity-0", "pointer-events-none");
  toast.classList.add("translate-y-0", "opacity-100");

  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.classList.remove("translate-y-0", "opacity-100");
    toast.classList.add("translate-y-20", "opacity-0", "pointer-events-none");
    setTimeout(processToastQueue, 300);
  }, 2800);
}

// 8. Reading Progress Bar
function initReadingProgressBar() {
  const bar = document.getElementById("readingProgressBar");
  if (!bar) return;
  let ticking = false;
  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        const winScroll = window.scrollY || document.documentElement.scrollTop || 0;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
        bar.style.width = Math.min(100, Math.max(0, scrolled)) + "%";
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
}

// 9. Static Page Modal Support on post.html
function initPostPageModal() {
  const pageModal = document.getElementById("pageModal");
  const closePageModalBtn = document.getElementById("closePageModalBtn");
  if (closePageModalBtn && pageModal) {
    closePageModalBtn.addEventListener("click", () => pageModal.classList.add("hidden"));
    pageModal.addEventListener("click", (e) => {
      if (e.target === pageModal) pageModal.classList.add("hidden");
    });
  }

  document.addEventListener("click", (e) => {
    const trigger = e.target.closest(".page-trigger");
    if (trigger) {
      e.preventDefault();
      const pageKey = trigger.getAttribute("data-page");
      if (pageKey) openPostPageModal(pageKey);
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && pageModal) {
      pageModal.classList.add("hidden");
    }
  });
}

function openPostPageModal(pageKey) {
  const pageModal = document.getElementById("pageModal");
  const pageContent = document.getElementById("pageModalContent");
  if (!pageModal || !pageContent) return;

  const data = (typeof staticPages !== 'undefined' && staticPages[pageKey]) 
    ? staticPages[pageKey] 
    : (window.staticPages && window.staticPages[pageKey]);

  if (!data) return;

  pageContent.innerHTML = `
    <div class="border-b border-gray-100 dark:border-slate-800 pb-5 mb-6">
      <div class="flex items-center gap-2 mb-2">
        <span class="px-2.5 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 text-[11px] font-bold uppercase tracking-wider">
          Official Information
        </span>
        <span class="text-xs text-gray-400">•</span>
        <span class="text-xs text-gray-500 dark:text-gray-400">Updated: ${data.lastUpdated || '2026'}</span>
      </div>
      <h2 class="text-2xl sm:text-3xl font-extrabold font-serif-heading text-gray-950 dark:text-white">
        ${escapeHtml(data.title)}
      </h2>
      <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 mt-1">
        ${escapeHtml(data.subtitle || '')}
      </p>
    </div>
    <div class="page-body">
      ${data.content}
    </div>
  `;

  const contactForm = document.getElementById("contactPageForm");
  if (contactForm) {
    contactForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = document.getElementById("contactName").value.trim();
      const email = document.getElementById("contactEmail").value.trim();
      const subject = document.getElementById("contactSubject").value.trim();
      const message = document.getElementById("contactMessage").value.trim();

      const mailtoUrl = `mailto:binodbhatt500k@gmail.com?subject=${encodeURIComponent('[imtechboss.com] ' + subject)}&body=${encodeURIComponent('From: ' + name + ' (' + email + ')\n\n' + message)}`;
      window.location.href = mailtoUrl;
      showToast("✉️ Opening email client to send message!");
      contactForm.reset();
    });
  }

  pageModal.classList.remove("hidden");
  pageContent.scrollTop = 0;
}

// Utility: Escape HTML
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// 7. Monetization: In-Article AdSense Injection (Smart Placement for 100% of Articles)
function injectInArticleAdSense(html) {
  if (!html || !html.trim()) return html;

  const adBanner = `
    <div class="ad-slot-box my-8 text-center bg-gray-50 dark:bg-slate-800 rounded-2xl p-4 sm:p-5 border border-gray-200/80 dark:border-slate-800 not-prose overflow-hidden shadow-xs">
      <span class="text-[10px] uppercase font-bold tracking-widest text-gray-400 block mb-2">Sponsored / Advertisement</span>
      <!-- square -->
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-pub-1043419685176632"
           data-ad-slot="5211138610"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
    </div>
  `;

  const adBanner2 = `
    <div class="ad-slot-box my-8 text-center bg-gray-50 dark:bg-slate-800 rounded-2xl p-4 sm:p-5 border border-gray-200/80 dark:border-slate-800 not-prose overflow-hidden shadow-xs">
      <span class="text-[10px] uppercase font-bold tracking-widest text-gray-400 block mb-2">Sponsored / Advertisement</span>
      <!-- horizontal banner -->
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-pub-1043419685176632"
           data-ad-slot="6665664396"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
    </div>
  `;

  let inserted = false;

  // Strategy 1: Articles with 6 or more <p> tags (insert after 3rd AND 6th paragraphs)
  const pMatches = html.match(/<\/p>/gi);
  const pCount = pMatches ? pMatches.length : 0;
  if (pCount >= 6) {
    let count = 0;
    html = html.replace(/<\/p>/gi, (match) => {
      count++;
      if (count === 3) {
        inserted = true;
        return match + '\n' + adBanner;
      }
      if (count === 6) {
        return match + '\n' + adBanner2;
      }
      return match;
    });
    if (inserted) return html;
  }

  // Strategy 1b: Articles with 3 to 5 <p> tags (insert after 2nd or 3rd paragraph)
  if (pCount >= 3) {
    let count = 0;
    const targetP = pCount >= 5 ? 3 : 2;
    html = html.replace(/<\/p>/gi, (match) => {
      count++;
      if (count === targetP && !inserted) {
        inserted = true;
        return match + '\n' + adBanner;
      }
      return match;
    });
    if (inserted) return html;
  }

  // Strategy 2: Articles with 1 or 2 <p> tags (insert after 1st paragraph)
  if (pCount > 0 && !inserted) {
    let count = 0;
    html = html.replace(/<\/p>/gi, (match) => {
      count++;
      if (count === 1 && !inserted) {
        inserted = true;
        return match + '\n' + adBanner;
      }
      return match;
    });
    if (inserted) return html;
  }

  // Strategy 3: Articles with subheadings (<h2> or <h3>)
  if (!inserted && /<\/h[23]>/i.test(html)) {
    let hCount = 0;
    html = html.replace(/<\/h[23]>/gi, (match) => {
      hCount++;
      if (hCount === 1 && !inserted) {
        inserted = true;
        return match + '\n' + adBanner;
      }
      return match;
    });
    if (inserted) return html;
  }

  // Strategy 4: Articles with line breaks (<br><br>) after 200 characters
  if (!inserted && /<br\s*\/?>\s*<br\s*\/?>/i.test(html)) {
    html = html.replace(/(<br\s*\/?>\s*<br\s*\/?>)/gi, (match, p1, offset) => {
      if (!inserted && offset > 200) {
        inserted = true;
        return match + '\n' + adBanner;
      }
      return match;
    });
    if (inserted) return html;
  }

  // Strategy 5: Legacy Blogger posts formatted with </div> tags after 250 characters
  if (!inserted && /<\/div>/i.test(html)) {
    html = html.replace(/<\/div>/gi, (match, offset) => {
      if (!inserted && offset > 250) {
        inserted = true;
        return match + '\n' + adBanner;
      }
      return match;
    });
    if (inserted) return html;
  }

  // Strategy 6: Absolute guaranteed fallback (append inside article)
  if (!inserted) {
    html = html + '\n' + adBanner;
    inserted = true;
  }

  return html;
}

// 8. Reader Feature: Table of Contents (ToC)
function generateTableOfContents(container) {
  const headings = container.querySelectorAll(".article-body h2, .article-body h3");
  if (headings.length < 2) return;

  const tocContainer = document.createElement("div");
  tocContainer.className = "my-6 p-5 rounded-2xl bg-blue-50/50 dark:bg-slate-800/80 border border-blue-100 dark:border-slate-800 text-xs";
  
  let listItems = "";
  headings.forEach((heading, idx) => {
    let headingId = heading.id && heading.id.trim();
    if (!headingId) {
      const slug = heading.textContent.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
      headingId = slug || `section-${idx}`;
      heading.id = headingId;
    }
    const isH3 = heading.tagName.toLowerCase() === "h3";
    listItems += `
      <li class="${isH3 ? 'ml-4 list-disc text-gray-500 dark:text-gray-400' : 'font-semibold text-gray-800 dark:text-gray-200'} my-1">
        <a href="#${headingId}" class="hover:text-blue-600 dark:hover:text-blue-400 hover:underline transition-colors">${escapeHtml(heading.textContent)}</a>
      </li>
    `;
  });

  tocContainer.innerHTML = `
    <div class="flex items-center justify-between font-bold text-gray-900 dark:text-white uppercase tracking-wider mb-2">
      <span class="flex items-center gap-1.5">📑 Table of Contents</span>
      <button id="toggleTocBtn" class="text-xs text-blue-600 dark:text-blue-400 hover:underline font-semibold">Hide</button>
    </div>
    <ul id="tocList" class="space-y-1 list-none pl-0">
      ${listItems}
    </ul>
  `;

  const articleBody = container.querySelector(".article-body");
  if (articleBody) {
    articleBody.insertBefore(tocContainer, articleBody.firstChild);

    const toggleBtn = tocContainer.querySelector("#toggleTocBtn");
    const tocList = tocContainer.querySelector("#tocList");
    if (toggleBtn && tocList) {
      toggleBtn.addEventListener("click", () => {
        const isHidden = tocList.classList.toggle("hidden");
        toggleBtn.textContent = isHidden ? "Show" : "Hide";
      });
    }
  }
}

// 9. Reader Feature: 1-Click Code Copy Button
function setupCodeCopyButtons(container) {
  const preElements = container.querySelectorAll(".article-body pre");
  preElements.forEach(pre => {
    if (pre.querySelector(".copy-code-btn")) return;
    pre.style.position = "relative";
    pre.classList.add("group");

    const copyBtn = document.createElement("button");
    copyBtn.className = "copy-code-btn absolute top-2 right-2 px-2.5 py-1 text-[11px] font-bold rounded-lg bg-slate-800/90 text-gray-200 hover:bg-slate-700 hover:text-white transition-all opacity-80 hover:opacity-100 shadow-sm border border-slate-700";
    copyBtn.innerHTML = `<span>📋 Copy</span>`;

    copyBtn.addEventListener("click", () => {
      const codeElem = pre.querySelector("code");
      const textToCopy = (codeElem ? codeElem.innerText : pre.innerText).replace(/📋 Copy|✓ Copied!/g, '').trim();
      if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
        navigator.clipboard.writeText(textToCopy).then(() => {
          copyBtn.innerHTML = `<span>✓ Copied!</span>`;
          copyBtn.classList.add("bg-emerald-600", "text-white");
          setTimeout(() => {
            copyBtn.innerHTML = `<span>📋 Copy</span>`;
            copyBtn.classList.remove("bg-emerald-600", "text-white");
          }, 2000);
        }).catch(() => {});
      } else {
        try {
          const textArea = document.createElement('textarea');
          textArea.value = textToCopy;
          textArea.style.position = 'fixed';
          textArea.style.left = '-9999px';
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand('copy');
          document.body.removeChild(textArea);
          copyBtn.innerHTML = `<span>✓ Copied!</span>`;
          copyBtn.classList.add("bg-emerald-600", "text-white");
          setTimeout(() => {
            copyBtn.innerHTML = `<span>📋 Copy</span>`;
            copyBtn.classList.remove("bg-emerald-600", "text-white");
          }, 2000);
        } catch(err) {}
      }
    });

    pre.appendChild(copyBtn);
  });
}

// 10. High-Converting Resource Download Counter
function setupDownloadCounters(container) {
  const downloadLinks = container.querySelectorAll('.article-body a[href*="mediafire"], .article-body a[href*="drive.google.com"], .article-body a[href*=".apk"], .article-body a[href*=".zip"], .article-body a[href*=".pdf"], .article-body a[href*="mega.nz"]');
  downloadLinks.forEach(link => {
    const originalHref = link.getAttribute("href");
    link.addEventListener("click", (e) => {
      if (link.dataset.downloadReady === "true") return;
      e.preventDefault();

      let countdown = 5;
      link.classList.add("pointer-events-none", "opacity-80");
      link.innerHTML = `<span class="inline-flex items-center gap-1.5 font-bold">⏳ Generating secure link (${countdown}s)...</span>`;

      const timer = setInterval(() => {
        countdown--;
        if (countdown > 0) {
          link.innerHTML = `<span class="inline-flex items-center gap-1.5 font-bold">⏳ Generating secure link (${countdown}s)...</span>`;
        } else {
          clearInterval(timer);
          link.dataset.downloadReady = "true";
          link.classList.remove("pointer-events-none", "opacity-80");
          link.innerHTML = `<span class="inline-flex items-center gap-1.5 font-bold text-emerald-600 dark:text-emerald-400">🚀 Link Ready! Click to Open →</span>`;
        }
      }, 1000);
    });
  });
}

// 11. Spotlight Search (Ctrl + K) & Newsletter on Post Page
function setupSpotlightSearchPost() {
  const searchModal = document.getElementById("searchModal");
  const searchInput = document.getElementById("spotlightSearchInput");
  const searchResults = document.getElementById("spotlightSearchResults");
  const closeBtn = document.getElementById("closeSearchModalBtn");
  const triggerBtn = document.getElementById("searchModalTrigger");
  const countBadge = document.getElementById("spotlightCountBadge");

  if (!searchModal || !searchInput) return;

  let allArticlesList = [];
  try {
    let custom = JSON.parse(localStorage.getItem("pulse_custom_posts") || "[]");
    if (!Array.isArray(custom)) custom = [];
    const base = (typeof initialArticles !== "undefined" && Array.isArray(initialArticles)) ? initialArticles : [];
    allArticlesList = [...custom, ...base];
  } catch (e) {
    allArticlesList = (typeof initialArticles !== "undefined" && Array.isArray(initialArticles)) ? initialArticles : [];
  }

  if (countBadge) {
    countBadge.textContent = `${allArticlesList.length} stories indexed`;
  }

  function openSearch() {
    searchModal.classList.remove("hidden");
    setTimeout(() => searchInput.focus(), 50);
  }

  function closeSearch() {
    searchModal.classList.add("hidden");
    searchInput.value = "";
    searchResults.innerHTML = `<p class="text-gray-400 text-center py-8">Type keywords above to search all ${allArticlesList.length} articles...</p>`;
  }

  if (triggerBtn) triggerBtn.addEventListener("click", openSearch);

  window.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (searchModal.classList.contains("hidden")) {
        openSearch();
      } else {
        closeSearch();
      }
    } else if (e.key === "Escape" && !searchModal.classList.contains("hidden")) {
      closeSearch();
    }
  });

  if (closeBtn) closeBtn.addEventListener("click", closeSearch);
  searchModal.addEventListener("click", (e) => {
    if (e.target === searchModal) closeSearch();
  });

  searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim().toLowerCase();
    if (!query) {
      searchResults.innerHTML = `<p class="text-gray-400 text-center py-8">Type keywords above to search all ${allArticlesList.length} articles...</p>`;
      return;
    }

    const matches = allArticlesList.filter(a => {
      if (!a) return false;
      const t = (a.title || "").toLowerCase();
      const c = (a.category || "").toLowerCase();
      const tags = Array.isArray(a.tags) ? a.tags.join(' ').toLowerCase() : (typeof a.tags === 'string' ? a.tags.toLowerCase() : '');
      return t.includes(query) || c.includes(query) || tags.includes(query);
    }).slice(0, 10);

    if (matches.length === 0) {
      searchResults.innerHTML = `
        <div class="text-center py-8 text-gray-400">
          <p>No stories found matching "<span class="text-gray-900 dark:text-white font-semibold">${escapeHtml(query)}</span>"</p>
        </div>
      `;
      return;
    }

    searchResults.innerHTML = matches.map(m => `
      <a 
        href="post.html?id=${encodeURIComponent(m.id)}" 
        class="flex items-center justify-between p-3 rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors group"
      >
        <div class="min-w-0 flex-1 pr-3">
          <div class="flex items-center gap-2 mb-1">
            <span class="px-2 py-0.5 rounded text-[9px] font-bold bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 uppercase">${escapeHtml(m.category || 'Story')}</span>
            <span class="text-[10px] text-gray-400">${escapeHtml(m.date || '')}</span>
          </div>
          <h4 class="font-bold text-xs text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 truncate">
            ${escapeHtml(m.title)}
          </h4>
        </div>
        <span class="text-xs text-gray-400 group-hover:text-blue-500 flex-shrink-0">→</span>
      </a>
    `).join("");
  });
}

function setupNewsletterPost() {
  const form = document.getElementById("newsletterForm");
  const emailInput = document.getElementById("newsletterEmail");
  if (!form || !emailInput) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = emailInput.value.trim();
    if (!email) return;

    let subscribers = [];
    try {
      const stored = localStorage.getItem("pulse_newsletter_subscribers");
      if (stored) subscribers = JSON.parse(stored);
    } catch (err) {}

    if (!subscribers.includes(email)) {
      subscribers.push(email);
      try { localStorage.setItem("pulse_newsletter_subscribers", JSON.stringify(subscribers)); } catch (e) {}
    }

    emailInput.value = "";
    showToast("🎉 Subscribed to Tech Boss Dispatch!");
  });
}

/*
function setupReadingProgressBar() {
  const progressBar = document.getElementById("readingProgressBar");
  if (!progressBar) return;
  window.addEventListener("scroll", () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
    progressBar.style.width = scrolled + "%";
  }, { passive: true });
}
*/

function _getArticlesList() {
  // post.html does not load app.js, so `articles` global is undefined here.
  // Resolve from initialArticles (data.js) + custom posts in localStorage.
  if (typeof articles !== 'undefined' && Array.isArray(articles)) return articles;
  let customArticles = [];
  try {
    const stored = localStorage.getItem('pulse_custom_posts');
    if (stored) customArticles = JSON.parse(stored);
    if (!Array.isArray(customArticles)) customArticles = [];
  } catch (e) { customArticles = []; }
  const base = (typeof initialArticles !== 'undefined' && Array.isArray(initialArticles)) ? initialArticles : [];
  return [...customArticles, ...base];
}

function renderRelatedArticles(currentArticle) {
  const section = document.getElementById("relatedSection");
  const grid = document.getElementById("relatedGrid");
  if (!section || !grid) return;

  const allArts = _getArticlesList();
  if (!allArts || allArts.length === 0) return;

  // Find up to 3 related articles (same category preferred, excluding current)
  const currentCat = (currentArticle.category || "").toLowerCase();
  let related = allArts.filter(a => a && a.id !== currentArticle.id && (a.category || "").toLowerCase() === currentCat);

  // If less than 3, backfill with other articles
  if (related.length < 3) {
    const others = allArts.filter(a => a && a.id !== currentArticle.id && !related.some(r => r.id === a.id));
    related = [...related, ...others];
  }

  related = related.slice(0, 3);
  if (related.length === 0) return;

  grid.innerHTML = related.map(art => {
    const safeTitle = escapeHtml(art.title);
    const safeCat = escapeHtml(art.category || 'General');
    const safeDate = escapeHtml(art.date || 'Recent');
    const imgUrl = art.image || "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80";

    return `
      <a href="post.html?id=${encodeURIComponent(art.id)}" class="group flex flex-col bg-white dark:bg-slate-900 rounded-2xl overflow-hidden border border-gray-200/80 dark:border-slate-800 shadow-xs hover:shadow-md transition-all">
        <div class="aspect-[16/10] overflow-hidden bg-gray-100 dark:bg-slate-800 relative">
          <img 
            src="${imgUrl}" 
            alt="${safeTitle}" 
            loading="lazy" 
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80'"
          >
          <span class="absolute top-2.5 left-2.5 px-2 py-0.5 text-[10px] font-bold rounded-full bg-white/90 dark:bg-slate-900/90 text-blue-600 dark:text-blue-400 backdrop-blur-md shadow-xs">
            ${safeCat}
          </span>
        </div>
        <div class="p-4 flex-1 flex flex-col justify-between">
          <h4 class="font-bold text-xs sm:text-sm text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 line-clamp-2 transition-colors leading-snug mb-3">
            ${safeTitle}
          </h4>
          <div class="text-[10px] text-gray-400 flex items-center justify-between pt-2 border-t border-gray-100 dark:border-slate-800/80">
            <span>📅 ${safeDate}</span>
            <span class="text-blue-600 dark:text-blue-400 font-semibold group-hover:translate-x-0.5 transition-transform">Read Story →</span>
          </div>
        </div>
      </a>
    `;
  }).join("");

  section.classList.remove("hidden");
}

function setupFloatingReadNext(currentArticle) {
  const allArts = _getArticlesList();
  if (!allArts || allArts.length < 2) return;

  // Don't show if user dismissed it in this session
  if (sessionStorage.getItem("tb_dismiss_next_pill") === "true") return;

  // Pick next story
  const currentIndex = allArts.findIndex(a => a && a.id === currentArticle.id);
  const nextArticle = (currentIndex >= 0 && currentIndex + 1 < allArts.length)
    ? allArts[currentIndex + 1]
    : allArts.find(a => a && a.id !== currentArticle.id);

  if (!nextArticle || nextArticle.id === currentArticle.id) return;

  const safeTitle = escapeHtml(nextArticle.title);
  const imgUrl = nextArticle.image || "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=200&q=80";

  let widget = document.getElementById("floatingReadNextWidget");
  if (!widget) {
    widget = document.createElement("div");
    widget.id = "floatingReadNextWidget";
    widget.className = "fixed bottom-5 right-5 z-40 max-w-sm w-[calc(100%-2.5rem)] sm:w-80 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border border-blue-500/30 rounded-2xl shadow-2xl p-3 transform translate-y-32 opacity-0 pointer-events-none transition-all duration-300 flex items-center gap-3";
    widget.innerHTML = `
      <div class="w-12 h-12 rounded-xl overflow-hidden flex-shrink-0 bg-gray-100 dark:bg-slate-800">
        <img src="${imgUrl}" alt="${safeTitle}" class="w-full h-full object-cover">
      </div>
      <div class="flex-1 min-w-0">
        <div class="flex items-center justify-between gap-1 mb-0.5">
          <span class="text-[9px] uppercase font-black text-blue-600 dark:text-blue-400 tracking-wider">Read Next</span>
          <button id="closeFloatingReadNext" aria-label="Dismiss recommendation" class="text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 text-sm font-bold leading-none p-0.5">×</button>
        </div>
        <a href="post.html?id=${encodeURIComponent(nextArticle.id)}" class="block text-xs font-bold text-gray-900 dark:text-white truncate hover:text-blue-600 transition-colors">
          ${safeTitle}
        </a>
      </div>
      <a href="post.html?id=${encodeURIComponent(nextArticle.id)}" class="flex-shrink-0 w-8 h-8 rounded-xl bg-blue-600 hover:bg-blue-700 text-white flex items-center justify-center text-xs shadow-md transition-all active:scale-95" title="Read Next Story">
        →
      </a>
    `;
    document.body.appendChild(widget);

    document.getElementById("closeFloatingReadNext")?.addEventListener("click", () => {
      widget.classList.add("translate-y-32", "opacity-0", "pointer-events-none");
      sessionStorage.setItem("tb_dismiss_next_pill", "true");
    });
  }

  // Show widget after 30% scroll
  let isShown = false;
  window.addEventListener("scroll", () => {
    if (sessionStorage.getItem("tb_dismiss_next_pill") === "true") return;
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrollPercent = height > 0 ? (winScroll / height) * 100 : 0;

    if (scrollPercent >= 30 && !isShown) {
      isShown = true;
      widget.classList.remove("translate-y-32", "opacity-0", "pointer-events-none");
    }
  }, { passive: true });
}





