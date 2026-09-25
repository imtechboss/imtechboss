// PulseNews & The Boss Journal Core Application Script

// State Management
let articles = [];
let activeCategory = "All";
let searchQuery = "";
let onlyBookmarks = false;
let bookmarkedIds = new Set();
let displayedCount = 12; // Initial batch of articles to display for instant silky performance

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
  try {
    initTheme();
    initStorage();
    initTickerAndClock();
    initNavigation();
    initSearch();
    initModals();
    initNewsletter();
    renderTrendingTopics();
    renderArticles();
    initSecretAdminTrigger();
    setupSpotlightSearch();
    initNotificationBell();

    // Direct deep-link to article or static page if URL has #hash
    const rawHash = window.location.hash.replace('#', '').trim();
    if (rawHash) {
      const lowerHash = rawHash.toLowerCase();
      setTimeout(() => {
        if (['about', 'contact', 'privacy', 'disclaimer'].includes(lowerHash)) {
          if (typeof openPageModal === 'function') openPageModal(lowerHash);
        } else {
          const matchedArticle = articles.find(a => a && (String(a.id).toLowerCase() === lowerHash || String(a.id) === rawHash));
          if (matchedArticle) {
            window.location.href = `post.html?id=${encodeURIComponent(matchedArticle.id)}`;
          }
        }
      }, 150);
    }
  } catch (err) {
    console.error("Initialization error:", err);
  }
});

function initSecretAdminTrigger() {
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
    if (e.ctrlKey && e.shiftKey && (e.key === "A" || e.key === "a")) {
      window.location.href = "admin.html";
    }
  });
}

// 1. Theme Management (Dark / Light mode)
function initTheme() {
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const sunIcon = document.getElementById("sunIcon");
  const moonIcon = document.getElementById("moonIcon");

  let savedTheme = null;
  try {
    savedTheme = localStorage.getItem("pulse_theme");
  } catch (e) {}

  const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (savedTheme === "dark" || (!savedTheme && systemDark)) {
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
      const isDark = document.documentElement.classList.toggle("dark");
      try {
        localStorage.setItem("pulse_theme", isDark ? "dark" : "light");
      } catch (e) {}

      if (isDark) {
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

// 2. Data & Safe Storage Management
function initStorage() {
  // Purge any large old cache key to free browser localStorage immediately
  try {
    localStorage.removeItem("pulse_articles");
    localStorage.removeItem("pulse_data_version");
  } catch (e) {}

  let customArticles = [];
  try {
    const storedCustom = localStorage.getItem("pulse_custom_posts");
    if (storedCustom) {
      customArticles = JSON.parse(storedCustom);
    }
    if (!Array.isArray(customArticles)) customArticles = [];
  } catch (e) {
    customArticles = [];
  }

  const baseArticles = (typeof initialArticles !== "undefined" && Array.isArray(initialArticles)) 
    ? initialArticles 
    : [];

  // Combine custom created articles (first) with base Blogger articles
  articles = [...customArticles, ...baseArticles];

  try {
    const storedBookmarks = localStorage.getItem("pulse_bookmarks");
    if (storedBookmarks) {
      const parsed = JSON.parse(storedBookmarks);
      bookmarkedIds = new Set(Array.isArray(parsed) ? parsed : []);
      updateBookmarkBadge();
    }
  } catch (e) {
    bookmarkedIds = new Set();
  }


}

function saveBookmarks() {
  try {
    localStorage.setItem("pulse_bookmarks", JSON.stringify(Array.from(bookmarkedIds)));
  } catch (e) {}
  updateBookmarkBadge();
}



function updateBookmarkBadge() {
  const badge = document.getElementById("bookmarksCountBadge");
  if (!badge) return;
  if (bookmarkedIds.size > 0) {
    badge.textContent = bookmarkedIds.size;
    badge.classList.remove("hidden");
  } else {
    badge.classList.add("hidden");
  }
}

// 3. Ticker & Clock
function initTickerAndClock() {
  const tickerContent = document.getElementById("tickerContent");
  const tickerItems = (typeof breakingNews !== 'undefined' && Array.isArray(breakingNews)) ? breakingNews : articles.slice(0, 5);
  if (tickerContent && tickerItems.length > 0) {
    const items = [...tickerItems, ...tickerItems];
    tickerContent.innerHTML = items.map(item => {
      const title = typeof item === 'object' && item.title ? item.title : String(item);
      const id = typeof item === 'object' && item.id ? item.id : null;
      return `
        <button 
          class="ticker-click-item inline-flex items-center gap-2 mx-6 text-xs hover:text-white cursor-pointer transition-colors text-left focus:outline-none group/ticker" 
          ${id ? `data-id="${escapeHtml(id)}"` : ''}
          title="Click to read: ${escapeHtml(title)}"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-blue-500 flex-shrink-0 group-hover/ticker:scale-125 transition-transform"></span>
          <span class="group-hover/ticker:underline">${escapeHtml(title)}</span>
        </button>
      `;
    }).join("");

    tickerContent.querySelectorAll(".ticker-click-item").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        if (id) {
          window.open('post.html?id=' + encodeURIComponent(id), '_blank');
        } else if (articles.length > 0) {
          window.open('post.html?id=' + encodeURIComponent(articles[0].id), '_blank');
        }
      });
    });
  }

  // Also make the "Breaking" badge clickable to read the latest article in a new tab
  const breakingBadge = document.querySelector(".bg-red-600");
  if (breakingBadge) {
    breakingBadge.style.cursor = "pointer";
    breakingBadge.title = "Click to open latest breaking story in new tab";
    breakingBadge.addEventListener("click", () => {
      if (articles.length > 0) {
        window.open('post.html?id=' + encodeURIComponent(articles[0].id), '_blank');
      }
    });
  }

  const dateTimeEl = document.getElementById("currentDateTime");
  if (dateTimeEl) {
    function updateClock() {
      const now = new Date();
      const options = { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };
      dateTimeEl.textContent = now.toLocaleDateString('en-US', options);
    }
    updateClock();
    setInterval(updateClock, 1000);
  }
}

// 4. Navigation & Category Filters
function initNavigation() {
  const categoryNavBar = document.getElementById("categoryNavBar");
  const mobileCategoryList = document.getElementById("mobileCategoryList");
  const filterPillsContainer = document.getElementById("filterPillsContainer");
  const mobileMenuBtn = document.getElementById("mobileMenuBtn");
  const mobileDrawer = document.getElementById("mobileDrawer");
  const bookmarksFilterBtn = document.getElementById("bookmarksFilterBtn");

  const categories = (typeof defaultCategories !== 'undefined' && Array.isArray(defaultCategories))
    ? defaultCategories
    : ["All", "Education & Notes", "General", "Gaming & Apps", "Software & Tech"];

  if (categoryNavBar) {
    categoryNavBar.innerHTML = categories.map(cat => `
      <button 
        class="nav-cat-btn px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors whitespace-nowrap ${cat === activeCategory ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' : 'text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400'}"
        data-category="${escapeHtml(cat)}"
      >
        ${escapeHtml(cat)}
      </button>
    `).join("");
  }

  if (mobileCategoryList) {
    mobileCategoryList.innerHTML = categories.map(cat => `
      <button 
        class="mobile-cat-btn text-left px-3 py-2 text-sm font-medium rounded-lg transition-colors ${cat === activeCategory ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800'}"
        data-category="${escapeHtml(cat)}"
      >
        ${escapeHtml(cat)}
      </button>
    `).join("");
  }

  if (filterPillsContainer) {
    filterPillsContainer.innerHTML = categories.map(cat => `
      <button 
        class="filter-pill-btn px-3.5 py-1.5 text-xs font-semibold rounded-full border transition-all whitespace-nowrap ${cat === activeCategory ? 'bg-slate-900 text-white dark:bg-blue-600 border-transparent shadow-sm' : 'bg-white dark:bg-slate-900 border-gray-200 dark:border-slate-800 text-gray-600 dark:text-gray-300 hover:border-gray-400'}"
        data-category="${escapeHtml(cat)}"
      >
        ${escapeHtml(cat)}
      </button>
    `).join("");
  }

  // Category switch handlers
  document.querySelectorAll(".nav-cat-btn, .mobile-cat-btn, .filter-pill-btn, .footer-cat-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const cat = btn.getAttribute("data-category");
      setCategory(cat);
      if (mobileDrawer && !mobileDrawer.classList.contains("hidden")) {
        mobileDrawer.classList.add("hidden");
      }
      if (btn.classList.contains("footer-cat-btn")) {
        const titleEl = document.getElementById("sectionTitle");
        if (titleEl) titleEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Topic Hub Pills handlers
  document.querySelectorAll(".topic-hub-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const q = btn.getAttribute("data-search") || "";
      const desktopSearch = document.getElementById("desktopSearchInput");
      const mobileSearch = document.getElementById("mobileSearchInput");
      if (desktopSearch) desktopSearch.value = q;
      if (mobileSearch) mobileSearch.value = q;
      searchQuery = q.toLowerCase();
      displayedCount = 12;
      const clearSearchBtn = document.getElementById("clearSearchBtn");
      if (clearSearchBtn) clearSearchBtn.classList.remove("hidden");
      renderArticles();
      const titleEl = document.getElementById("sectionTitle");
      if (titleEl) titleEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  if (mobileMenuBtn && mobileDrawer) {
    mobileMenuBtn.addEventListener("click", () => {
      mobileDrawer.classList.toggle("hidden");
    });
  }

  if (bookmarksFilterBtn) {
    bookmarksFilterBtn.addEventListener("click", () => {
      onlyBookmarks = !onlyBookmarks;
      displayedCount = 12;
      bookmarksFilterBtn.classList.toggle("text-blue-600", onlyBookmarks);
      bookmarksFilterBtn.classList.toggle("dark:text-blue-400", onlyBookmarks);
      
      const sectionTitle = document.getElementById("sectionTitle");
      const sectionSubtitle = document.getElementById("sectionSubtitle");
      if (onlyBookmarks) {
        if (sectionTitle) sectionTitle.textContent = "Saved Articles";
        if (sectionSubtitle) sectionSubtitle.textContent = "Your personally bookmarked stories.";
      } else {
        if (sectionTitle) sectionTitle.textContent = activeCategory === "All" ? "Latest Stories" : `${activeCategory} Stories`;
        if (sectionSubtitle) sectionSubtitle.textContent = "Explore all curated analyses and stories from our newsroom.";
      }
      renderArticles();
    });
  }
}

function setCategory(cat) {
  activeCategory = cat;
  onlyBookmarks = false;
  displayedCount = 12;
  searchQuery = '';
  
  const desktopSearchInput = document.getElementById("desktopSearchInput");
  const mobileSearchInput = document.getElementById("mobileSearchInput");
  if (desktopSearchInput) desktopSearchInput.value = '';
  if (mobileSearchInput) mobileSearchInput.value = '';
  const clearSearchBtn = document.getElementById("clearSearchBtn");
  if (clearSearchBtn) clearSearchBtn.classList.add("hidden");

  const bBtn = document.getElementById("bookmarksFilterBtn");
  if (bBtn) bBtn.classList.remove("text-blue-600", "dark:text-blue-400");
  
  const sectionTitle = document.getElementById("sectionTitle");
  const sectionSubtitle = document.getElementById("sectionSubtitle");
  if (sectionTitle) sectionTitle.textContent = cat === "All" ? "Latest Stories" : `${cat} Stories`;
  if (sectionSubtitle) sectionSubtitle.textContent = `Curated articles in ${cat.toLowerCase()}.`;

  document.querySelectorAll(".nav-cat-btn").forEach(btn => {
    const isCurrent = btn.getAttribute("data-category") === cat;
    btn.className = `nav-cat-btn px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors whitespace-nowrap ${
      isCurrent ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' : 'text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400'
    }`;
  });

  document.querySelectorAll(".filter-pill-btn").forEach(btn => {
    const isCurrent = btn.getAttribute("data-category") === cat;
    btn.className = `filter-pill-btn px-3.5 py-1.5 text-xs font-semibold rounded-full border transition-all whitespace-nowrap ${
      isCurrent ? 'bg-slate-900 text-white dark:bg-blue-600 border-transparent shadow-sm' : 'bg-white dark:bg-slate-900 border-gray-200 dark:border-slate-800 text-gray-600 dark:text-gray-300 hover:border-gray-400'
    }`;
  });

  document.querySelectorAll(".mobile-cat-btn").forEach(btn => {
    const isCurrent = btn.getAttribute("data-category") === cat;
    btn.className = `mobile-cat-btn text-left px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
      isCurrent ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800'
    }`;
  });

  renderArticles();
}

// 5. Search
function initSearch() {
  const desktopSearch = document.getElementById("desktopSearchInput");
  const mobileSearch = document.getElementById("mobileSearchInput");
  const clearSearchBtn = document.getElementById("clearSearchBtn");
  const resetSearchBtn = document.getElementById("resetSearchBtn");

  const handleInput = (val) => {
    searchQuery = (val || "").trim().toLowerCase();
    displayedCount = 12;

    if (desktopSearch && desktopSearch.value !== val) desktopSearch.value = val;
    if (mobileSearch && mobileSearch.value !== val) mobileSearch.value = val;

    const sectionTitle = document.getElementById("sectionTitle");
    const sectionSubtitle = document.getElementById("sectionSubtitle");

    if (searchQuery.length > 0) {
      if (clearSearchBtn) clearSearchBtn.classList.remove("hidden");
      if (sectionTitle) sectionTitle.textContent = `Search Results for "${val}"`;
      if (sectionSubtitle) sectionSubtitle.textContent = "Matching stories across all archives.";
    } else {
      if (clearSearchBtn) clearSearchBtn.classList.add("hidden");
      if (onlyBookmarks) {
        if (sectionTitle) sectionTitle.textContent = "Saved Articles";
        if (sectionSubtitle) sectionSubtitle.textContent = "Your personally bookmarked stories.";
      } else {
        if (sectionTitle) sectionTitle.textContent = activeCategory === "All" ? "Latest Stories" : `${activeCategory} Stories`;
        if (sectionSubtitle) sectionSubtitle.textContent = "Explore all curated analyses and stories from our newsroom.";
      }
    }
    renderArticles();
  };

  let searchDebounceTimer = null;
  const handleInputDebounced = (value) => {
    clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(() => handleInput(value), 250);
  };

  if (desktopSearch) desktopSearch.addEventListener("input", (e) => handleInputDebounced(e.target.value));
  if (mobileSearch) mobileSearch.addEventListener("input", (e) => handleInputDebounced(e.target.value));

  if (clearSearchBtn) {
    clearSearchBtn.addEventListener("click", () => {
      handleInput("");
      if (desktopSearch) desktopSearch.focus();
    });
  }

  if (resetSearchBtn) {
    resetSearchBtn.addEventListener("click", () => {
      handleInput("");
      setCategory("All");
    });
  }
}

// 6. Article Rendering Engine
function renderArticles(isAppending = false) {
  const featuredContainer = document.getElementById("featuredArticleContainer");
  const trendingContainer = document.getElementById("trendingListContainer");
  const gridContainer = document.getElementById("articlesGrid");
  const emptyState = document.getElementById("emptyState");
  const heroSection = document.getElementById("heroSection");

  if (!gridContainer) return;

  // Filter articles
  let filtered = articles.filter(art => {
    if (!art) return false;
    const matchesCat = activeCategory === "All" || (art.category && art.category.toLowerCase() === activeCategory.toLowerCase());
    const matchesSearch = !searchQuery || 
      (art.title && art.title.toLowerCase().includes(searchQuery)) ||
      (art.excerpt && art.excerpt.toLowerCase().includes(searchQuery)) ||
      (art.category && art.category.toLowerCase().includes(searchQuery)) ||
      (art.tags && (Array.isArray(art.tags) ? art.tags.some(t => String(t).toLowerCase().includes(searchQuery)) : String(art.tags).toLowerCase().includes(searchQuery))) ||
      (art.author && art.author.name && art.author.name.toLowerCase().includes(searchQuery));
    const matchesBookmark = !onlyBookmarks || bookmarkedIds.has(art.id);

    return matchesCat && matchesSearch && matchesBookmark;
  });

  // Hero Section display
  if (activeCategory === "All" && !searchQuery && !onlyBookmarks && heroSection) {
    heroSection.classList.remove("hidden");
    renderHero(featuredContainer, trendingContainer);
  } else if (heroSection) {
    heroSection.classList.add("hidden");
  }

  // Handle empty state
  if (filtered.length === 0) {
    gridContainer.innerHTML = "";
    if (emptyState) emptyState.classList.remove("hidden");
    removeLoadMoreButton();
    return;
  }

  if (emptyState) emptyState.classList.add("hidden");

  // Slice for instant pagination
  const startIndex = isAppending ? displayedCount - 12 : 0;
  const visibleArticles = filtered.slice(startIndex, displayedCount);
  const fullVisibleLength = filtered.slice(0, displayedCount).length;

  const adInFeedTemplate = (slotId = "6665664396") => `
    <div class="col-span-1 sm:col-span-2 ad-slot-box bg-white dark:bg-slate-900 rounded-2xl p-4 sm:p-5 border border-gray-200/90 dark:border-slate-800 shadow-sm text-center overflow-hidden my-1 not-prose">
      <span class="text-[9px] uppercase font-bold tracking-widest text-gray-400 block mb-2">Sponsored / Advertisement</span>
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-pub-1043419685176632"
           data-ad-slot="${slotId}"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
    </div>
  `;

  let cardsHtml = "";
  visibleArticles.forEach((art, index) => {
    const isBookmarked = bookmarkedIds.has(art.id);
    const safeTitle = escapeHtml(art.title);
    const safeExcerpt = escapeHtml(art.excerpt);
    const safeCat = escapeHtml(art.category || 'General');
    const safeDate = escapeHtml(art.date || 'Recent');
    const safeAuthor = escapeHtml(art.author?.name || 'Tech Boss');
    const imgUrl = art.image || "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80";

    cardsHtml += `
      <article class="article-card bg-white dark:bg-slate-900 rounded-2xl overflow-hidden border border-gray-200/90 dark:border-slate-800 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col group" data-id="${art.id}">
        <!-- Card Image Header -->
        <div class="relative overflow-hidden aspect-[16/10] bg-gray-100 dark:bg-slate-800">
          <a href="post.html?id=${encodeURIComponent(art.id)}" class="block w-full h-full cursor-pointer">
            <img 
              src="${imgUrl}" 
              alt="${safeTitle}" 
              loading="lazy" 
              class="zoom-img w-full h-full object-cover"
              onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80'"
            >
          </a>
          <div class="absolute top-3 left-3 flex gap-2 pointer-events-none">
            <span class="px-2.5 py-1 text-[11px] font-bold rounded-full bg-white/90 dark:bg-slate-900/90 text-blue-600 dark:text-blue-400 backdrop-blur-md shadow-sm">
              ${safeCat}
            </span>
          </div>
          <!-- 1-Click Flipboard Share -->
          <a 
            href="https://share.flipboard.com/bookmarklet/popout?v=2&title=${encodeURIComponent(art.title)}&url=${encodeURIComponent('https://imtechboss.com/post.html?id=' + art.id + '&flip=1')}" 
            target="_blank" 
            rel="noopener noreferrer"
            class="absolute top-3 right-12 w-8 h-8 rounded-full bg-white/80 dark:bg-slate-900/80 backdrop-blur-md flex items-center justify-center text-gray-700 dark:text-gray-200 hover:text-red-600 dark:hover:text-red-500 transition-colors shadow-sm z-10"
            title="Flip to Flipboard Magazine"
            onclick="event.stopPropagation();"
          >
            <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M0 0h8v24H0V0zm8 8h8v8H8V8zm0-8h16v8H8V0z"/></svg>
          </a>

          <button 
            class="bookmark-btn absolute top-3 right-3 w-8 h-8 rounded-full bg-white/80 dark:bg-slate-900/80 backdrop-blur-md flex items-center justify-center text-gray-700 dark:text-gray-200 hover:text-blue-600 dark:hover:text-blue-400 transition-colors shadow-sm z-10"
            data-id="${art.id}" 
            title="${isBookmarked ? 'Remove bookmark' : 'Bookmark story'}"
          >
            <svg class="w-4 h-4 ${isBookmarked ? 'fill-blue-600 text-blue-600' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
            </svg>
          </button>
        </div>

        <!-- Card Body -->
        <div class="p-5 flex-1 flex flex-col justify-between">
          <div>
            <div class="flex items-center gap-2 text-[11px] text-gray-500 dark:text-gray-400 mb-2">
              <span>📅 ${safeDate}</span>
              <span>•</span>
              <span>⏱️ ${art.readTime || '3 min read'}</span>
            </div>
            <h3 class="font-bold text-base sm:text-lg text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors leading-snug line-clamp-2">
              <a href="post.html?id=${encodeURIComponent(art.id)}">
                ${safeTitle}
              </a>
            </h3>
            <p class="text-xs text-gray-600 dark:text-gray-400 mt-2 line-clamp-2 leading-relaxed">
              ${safeExcerpt}
            </p>
          </div>

          <!-- Card Footer -->
          <div class="mt-4 pt-4 border-t border-gray-100 dark:border-slate-800 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-7 h-7 rounded-full bg-blue-600 text-white font-bold text-xs flex items-center justify-center ring-1 ring-gray-200 dark:ring-slate-700">
                ${safeAuthor.charAt(0)}
              </div>
              <span class="text-xs font-semibold text-gray-800 dark:text-gray-200">
                ${safeAuthor}
              </span>
            </div>
            <a 
              href="post.html?id=${encodeURIComponent(art.id)}" 
              class="text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1"
            >
              <span>Read</span>
              <svg class="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </a>
          </div>
        </div>
      </article>
    `;

    // Inject in-feed ads after 4th article and 10th article
    if ((startIndex + index) === 3 && fullVisibleLength > 4) {
      cardsHtml += adInFeedTemplate("6665664396");
    } else if ((startIndex + index) === 9 && fullVisibleLength > 10) {
      cardsHtml += adInFeedTemplate("5211138610");
    }
  });

  if (isAppending) {
    gridContainer.insertAdjacentHTML("beforeend", cardsHtml);
  } else {
    gridContainer.innerHTML = cardsHtml;
  }
  attachCardEvents();

  // Push AdSense for in-feed ads (race-condition safe: cancel any pending timer first)
  clearTimeout(window.__inFeedAdPushTimer);
  window.__inFeedAdPushTimer = setTimeout(() => {
    try {
      gridContainer.querySelectorAll("ins.adsbygoogle:not([data-ad-initialized])").forEach(ad => {
        ad.setAttribute("data-ad-initialized", "true");
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      });
    } catch (e) {}
  }, 500);

  // Manage Load More button
  if (filtered.length > displayedCount) {
    showLoadMoreButton(filtered.length);
  } else {
    removeLoadMoreButton();
  }
}

function showLoadMoreButton(totalCount) {
  let container = document.getElementById("loadMoreContainer");
  if (!container) {
    const gridContainer = document.getElementById("articlesGrid");
    if (!gridContainer || !gridContainer.parentNode) return;
    container = document.createElement("div");
    container.id = "loadMoreContainer";
    container.className = "col-span-full flex flex-col items-center justify-center pt-4 pb-2";
    container.innerHTML = `
      <button 
        id="loadMoreArticlesBtn" 
        class="px-6 py-2.5 rounded-full bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 hover:border-blue-500 text-xs font-bold text-gray-800 dark:text-gray-200 shadow-sm hover:shadow transition-all active:scale-95"
      >
        Load More Stories (${displayedCount} of ${totalCount})
      </button>
    `;
    gridContainer.parentNode.appendChild(container);
  }

  const realBtn = document.getElementById("loadMoreArticlesBtn");
  if (realBtn) {
    realBtn.textContent = `Load More Stories (${displayedCount} of ${totalCount})`;
    realBtn.onclick = () => {
      displayedCount += 12;
      renderArticles(true);
    };
  }
}

function removeLoadMoreButton() {
  const container = document.getElementById("loadMoreContainer");
  if (container) container.remove();
}

function renderHero(featuredContainer, trendingContainer) {
  if (!featuredContainer || !trendingContainer) return;

  const featured = articles.find(a => a.featured) || articles[0];
  const trending = articles.filter(a => a.trending && a.id !== featured?.id).slice(0, 3);

  if (featured) {
    const safeTitle = escapeHtml(featured.title);
    const safeExcerpt = escapeHtml(featured.excerpt);
    const safeCat = escapeHtml(featured.category || 'Featured');
    const safeDate = escapeHtml(featured.date || 'Recent');
    const safeAuthor = escapeHtml(featured.author?.name || 'Tech Boss');
    const imgUrl = featured.image || "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80";

    featuredContainer.innerHTML = `
      <a 
        href="post.html?id=${encodeURIComponent(featured.id)}" 
        class="block relative rounded-3xl overflow-hidden shadow-xl aspect-[16/9] md:aspect-[21/11] bg-slate-900 group cursor-pointer"
        data-id="${featured.id}"
      >
        <img 
          src="${imgUrl}" 
          alt="${safeTitle}" 
          class="zoom-img w-full h-full object-cover opacity-80 group-hover:opacity-90 group-hover:scale-105 transition-all duration-500"
          onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80'"
        >
        <div class="absolute inset-0 bg-gradient-to-t from-black/95 via-black/50 to-transparent flex flex-col justify-end p-6 sm:p-8 md:p-10 text-white">
          <div class="flex items-center gap-3 mb-3">
            <span class="px-3 py-1 text-xs font-bold uppercase tracking-wider rounded-full bg-blue-600 text-white shadow">
              Featured Story
            </span>
            <span class="text-xs text-gray-300 font-medium">${safeCat}</span>
            <span class="text-xs text-gray-400">•</span>
            <span class="text-xs text-gray-300 font-medium">${featured.readTime || '4 min read'}</span>
          </div>
          <h1 class="text-xl sm:text-2xl md:text-3xl lg:text-4xl font-extrabold font-serif-heading leading-tight mb-3 group-hover:text-blue-300 transition-colors">
            ${safeTitle}
          </h1>
          <p class="text-xs sm:text-sm text-gray-300 max-w-2xl line-clamp-2 mb-4 leading-relaxed">
            ${safeExcerpt}
          </p>
          <div class="flex items-center justify-between pt-2">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center ring-2 ring-white/50">
                ${safeAuthor.charAt(0)}
              </div>
              <div>
                <p class="text-xs font-bold">${safeAuthor}</p>
                <p class="text-[10px] text-gray-400">Publisher • ${safeDate}</p>
              </div>
            </div>
            <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/20 backdrop-blur-md text-xs font-semibold hover:bg-white/30 transition-colors">
              <span>Read Story</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
              </svg>
            </span>
          </div>
        </div>
      </a>
    `;
  }

  // Trending List
  trendingContainer.innerHTML = trending.map((art, idx) => {
    const safeTitle = escapeHtml(art.title);
    const safeCat = escapeHtml(art.category || 'General');
    const safeDate = escapeHtml(art.date || 'Recent');
    const imgUrl = art.image || "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=200&q=80";

    return `
      <a 
        href="post.html?id=${encodeURIComponent(art.id)}" 
        class="group flex gap-3 p-3 rounded-xl bg-white dark:bg-slate-900 border border-gray-200/70 dark:border-slate-800 hover:border-blue-500/50 transition-all cursor-pointer" 
        data-id="${art.id}"
      >
        <span class="text-2xl font-black font-serif-heading text-gray-300 dark:text-slate-700 group-hover:text-blue-600 transition-colors flex-shrink-0 w-6">
          0${idx + 1}
        </span>
        <div class="flex-1">
          <span class="text-[10px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
            ${safeCat}
          </span>
          <h4 class="text-xs sm:text-sm font-bold text-gray-900 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors line-clamp-2 leading-snug mt-0.5">
            ${safeTitle}
          </h4>
          <div class="flex items-center gap-2 text-[10px] text-gray-400 mt-1">
            <span>${safeDate}</span>
            <span>•</span>
            <span>${art.views || '1.2K'} reads</span>
          </div>
        </div>
        <div class="w-16 h-16 rounded-lg overflow-hidden flex-shrink-0 bg-gray-100 dark:bg-slate-800">
          <img 
            src="${imgUrl}" 
            alt="${safeTitle}" 
            class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
            onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=200&q=80'"
          >
        </div>
      </a>
    `;
  }).join("");
}

function attachCardEvents() {


  document.querySelectorAll(".bookmark-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      e.preventDefault();
      const id = btn.getAttribute("data-id");
      toggleBookmark(id);
    });
  });
}

function toggleBookmark(id) {
  try {
    const stored = localStorage.getItem("pulse_bookmarks");
    if (stored) bookmarkedIds = new Set(JSON.parse(stored));
  } catch(e) {}
  if (bookmarkedIds.has(id)) {
    bookmarkedIds.delete(id);
    showToast("Removed from bookmarks");
  } else {
    bookmarkedIds.add(id);
    showToast("Saved to bookmarks");
  }
  saveBookmarks();
  renderArticles();
}

// 7. Modals
function initModals() {
  const pageModal = document.getElementById("pageModal");
  const closePageModalBtn = document.getElementById("closePageModalBtn");
  if (closePageModalBtn && pageModal) {
    closePageModalBtn.addEventListener("click", () => pageModal.classList.add("hidden"));
    pageModal.addEventListener("click", (e) => {
      if (e.target === pageModal) pageModal.classList.add("hidden");
    });
  }

  // Universal click delegate for .page-trigger buttons
  document.addEventListener("click", (e) => {
    const trigger = e.target.closest(".page-trigger");
    if (trigger) {
      e.preventDefault();
      const pageKey = trigger.getAttribute("data-page");
      if (pageKey) openPageModal(pageKey);
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (pageModal) pageModal.classList.add("hidden");
    }
  });
}



function openPageModal(pageKey) {
  const pageModal = document.getElementById("pageModal");
  const pageContent = document.getElementById("pageModalContent");
  if (!pageModal || !pageContent) return;

  const data = (typeof staticPages !== 'undefined' && staticPages[pageKey]) 
    ? staticPages[pageKey] 
    : (window.staticPages && window.staticPages[pageKey]);

  if (!data) return;

  pageContent.innerHTML = `
    <!-- Page Header -->
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

    <!-- Page Body Content -->
    <div class="page-body">
      ${data.content}
    </div>
  `;

  // Wire up contact form if present
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

// 8. Newsletter & Trending Topics
function initNewsletter() {
  const form = document.getElementById("newsletterForm");
  const emailInput = document.getElementById("newsletterEmail");
  if (!form || !emailInput) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = emailInput.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
      if (typeof showToast === 'function') showToast("âš ï¸  Please enter a valid email address.");
      return;
    }

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

function renderTrendingTopics() {
  const container = document.getElementById("trendingTagsContainer");
  if (!container) return;

  const topics = (typeof trendingTopics !== 'undefined' && Array.isArray(trendingTopics) && trendingTopics.length > 0)
    ? trendingTopics
    : ["#Engineering", "#Education", "#Software", "#Android", "#Gaming", "#MacBook", "#Notes", "#Database", "#Mathematics"];

  container.innerHTML = topics.map(topic => `
    <button class="topic-tag px-2.5 py-1 text-xs font-semibold rounded-lg bg-gray-100 dark:bg-slate-800 hover:bg-blue-600 hover:text-white dark:hover:bg-blue-600 dark:hover:text-white text-gray-700 dark:text-gray-300 transition-colors shadow-sm">
      ${escapeHtml(topic)}
    </button>
  `).join("");

  container.querySelectorAll(".topic-tag").forEach(btn => {
    btn.addEventListener("click", () => {
      let query = btn.textContent.replace("#", "").trim();
      if (query.toLowerCase() === "engineeringnotes") query = "Engineering";
      if (query.toLowerCase() === "pcgames") query = "Gaming";
      if (query.toLowerCase() === "technepal") query = "Tech";
      if (query.toLowerCase() === "softwaremod") query = "Software";
      if (query.toLowerCase() === "androidapps") query = "Android";

      activeCategory = 'All';
      onlyBookmarks = false;
      
      const desktopSearch = document.getElementById("desktopSearchInput");
      const mobileSearch = document.getElementById("mobileSearchInput");
      if (desktopSearch) desktopSearch.value = query;
      if (mobileSearch) mobileSearch.value = query;
      searchQuery = query.toLowerCase();
      displayedCount = 12;
      const clearSearchBtn = document.getElementById("clearSearchBtn");
      if (clearSearchBtn) clearSearchBtn.classList.remove("hidden");
      
      // Update category UI to show 'All' as active
      document.querySelectorAll('.nav-cat-btn, .filter-pill-btn, .mobile-cat-btn').forEach(btn => {
        btn.classList.remove('text-blue-600', 'dark:text-blue-400', 'border-blue-600', 'bg-blue-50', 'dark:bg-blue-900/30');
      });
      const allBtns = document.querySelectorAll('[data-category="All"]');
      allBtns.forEach(btn => btn.classList.add('text-blue-600', 'dark:text-blue-400'));
      
      renderArticles();
      const titleEl = document.getElementById("sectionTitle");
      if (titleEl) titleEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
}



// 9. Utilities & Toast Alert
let toastTimer = null;
function showToast(message, icon = "✓") {
  const toast = document.getElementById("toastNotification");
  const msgEl = document.getElementById("toastMessage");
  const iconEl = document.getElementById("toastIcon");

  if (!toast || !msgEl || !iconEl) return;

  msgEl.textContent = message;
  iconEl.textContent = icon;

  toast.classList.remove("translate-y-20", "opacity-0", "pointer-events-none");
  toast.classList.add("translate-y-0", "opacity-100");

  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.classList.remove("translate-y-0", "opacity-100");
    toast.classList.add("translate-y-20", "opacity-0", "pointer-events-none");
  }, 2800);
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// 10. Spotlight Search Modal (Ctrl + K) & Newsletter Subscriptions
function setupSpotlightSearch() {
  const searchModal = document.getElementById("searchModal");
  const searchInput = document.getElementById("spotlightSearchInput");
  const searchResults = document.getElementById("spotlightSearchResults");
  const closeBtn = document.getElementById("closeSearchModalBtn");
  const countBadge = document.getElementById("spotlightCountBadge");

  if (!searchModal || !searchInput) return;

  if (countBadge && Array.isArray(articles)) {
    countBadge.textContent = `${articles.length} stories indexed`;
  }

  function openSearch() {
    searchModal.classList.remove("hidden");
    setTimeout(() => searchInput.focus(), 50);
  }

  function closeSearch() {
    searchModal.classList.add("hidden");
    searchInput.value = "";
    searchResults.innerHTML = "";
  }

  // Keyboard shortcut (Ctrl + K or Cmd + K) & ESC
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

  // Real-time live filtering
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim().toLowerCase();
    if (!query) {
      searchResults.innerHTML = `<p class="text-gray-400 text-center py-8">Type keywords above to search all ${articles.length} articles...</p>`;
      return;
    }

    const matches = articles.filter(a => {
      if (!a) return false;
      const t = (a.title || "").toLowerCase();
      const c = (a.category || "").toLowerCase();
      const tags = (Array.isArray(a.tags) ? a.tags.join(" ") : (typeof a.tags === 'string' ? a.tags : "")).toLowerCase();
      return t.includes(query) || c.includes(query) || tags.includes(query);
    }).slice(0, 10);

    if (matches.length === 0) {
      searchResults.innerHTML = `
        <div class="text-center py-8 text-gray-400">
          <p>No stories found matching "<span class="text-gray-900 dark:text-white font-semibold">${escapeHtml(query)}</span>"</p>
          <p class="text-[11px] text-gray-500 mt-1">Try another keyword like iPhone, Engineering, IOE, or Tech.</p>
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

// 8. Smart Push Notification Opt-In Bell
function initNotificationBell() {
  if (document.getElementById("smartNotificationBell")) return;

  const bell = document.createElement("button");
  bell.id = "smartNotificationBell";
  bell.className = "fixed bottom-6 left-6 z-40 p-3.5 rounded-full bg-blue-600 hover:bg-blue-700 text-white shadow-xl hover:shadow-2xl transition-all duration-300 active:scale-90 flex items-center justify-center group focus:outline-none";
  bell.title = "Get Instant Breaking Tech Alerts";
  bell.setAttribute("aria-label", "Subscribe to push notifications");

  let isSubscribed = false;
  try {
    isSubscribed = localStorage.getItem("pulse_push_subscribed") === "true";
  } catch (e) {}

  bell.innerHTML = `
    <div class="relative flex items-center justify-center">
      <svg class="w-5 h-5 fill-none stroke-current" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
      </svg>
      <span class="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full ${isSubscribed ? 'bg-emerald-400' : 'bg-amber-400 animate-ping'}"></span>
    </div>
  `;

  bell.addEventListener("click", async () => {
    if (!("Notification" in window)) {
      if (typeof showToast === "function") showToast("Push notifications are not supported in this browser.");
      return;
    }

    if (Notification.permission === "granted") {
      try { localStorage.setItem("pulse_push_subscribed", "true"); } catch (e) {}
      if (typeof showToast === "function") showToast("🔔 Notifications are active! You will receive breaking tech alerts.");
      return;
    }

    try {
      const permission = await Notification.requestPermission();
      if (permission === "granted") {
        try { localStorage.setItem("pulse_push_subscribed", "true"); } catch (e) {}
        if (typeof showToast === "function") showToast("🎉 Subscribed! You will receive breaking tech alerts.");
        try {
          new Notification("Tech Boss Journal", {
            body: "You're now subscribed to breaking tech and AI updates!",
            icon: "https://imtechboss.com/favicon.svg"
          });
        } catch (e) {}
        const pingDot = bell.querySelector(".animate-ping");
        if (pingDot) pingDot.className = "absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-emerald-400";
      } else {
        if (typeof showToast === "function") showToast("Notifications permission was not granted.");
      }
    } catch (err) {
      console.warn("Notification request error:", err);
    }
  });

  document.body.appendChild(bell);
}
