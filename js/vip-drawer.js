// Tech Boss VIP Exit-Intent & High-Converting Newsletter Drawer
(function() {
  const STORAGE_KEY = 'tb_vip_drawer_dismissed';
  const SUBSCRIBERS_KEY = 'pulse_newsletter_subscribers';

  function isDismissed() {
    try {
      const expiry = localStorage.getItem(STORAGE_KEY);
      if (expiry && Date.now() < parseInt(expiry, 10)) {
        return true;
      }
      const subscribers = localStorage.getItem(SUBSCRIBERS_KEY);
      if (subscribers && subscribers.length > 5) {
        // User already subscribed
        return true;
      }
    } catch (e) {}
    return false;
  }

  function setDismissed(days = 14) {
    try {
      const expiry = Date.now() + (days * 24 * 60 * 60 * 1000);
      localStorage.setItem(STORAGE_KEY, expiry.toString());
    } catch (e) {}
  }

  function createDrawer() {
    if (document.getElementById('tbVipDrawer') || isDismissed()) return;

    const drawer = document.createElement('div');
    drawer.id = 'tbVipDrawer';
    drawer.className = 'fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-50 max-w-sm w-[calc(100%-2rem)] bg-slate-900/95 dark:bg-slate-900/95 backdrop-blur-md border border-blue-500/40 shadow-2xl rounded-3xl p-5 sm:p-6 text-white transition-all duration-500 transform translate-y-8 opacity-0 pointer-events-none';

    drawer.innerHTML = `
      <div class="relative">
        <button id="closeTbVipDrawer" aria-label="Close newsletter invite" class="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center text-sm font-bold transition-colors">
          ✕
        </button>

        <div class="flex items-center gap-2 mb-2">
          <span class="w-2 h-2 rounded-full bg-blue-500 animate-ping"></span>
          <span class="text-[10px] uppercase font-bold tracking-widest text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded-full border border-blue-500/20">
            Tech Boss VIP Dispatch
          </span>
        </div>

        <h4 class="text-base sm:text-lg font-black text-white leading-snug mb-1">
          Stay Ahead of Hardware &amp; AI
        </h4>
        <p class="text-xs text-slate-300 leading-relaxed mb-4">
          Weekly curated GPU benchmarks, Windows diagnostic fixes, and local LLM guides delivered straight to your inbox.
        </p>

        <form id="tbVipForm" class="space-y-2">
          <div class="relative">
            <input 
              type="email" 
              id="tbVipEmail" 
              placeholder="Enter your email address" 
              required
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-xs text-white placeholder-slate-500 outline-none transition"
            >
          </div>
          <button 
            type="submit" 
            class="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg hover:shadow-blue-500/25 transition-all active:scale-95 flex items-center justify-center gap-2"
          >
            <span>Subscribe for Free</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </button>
        </form>

        <div class="mt-3 flex items-center justify-between text-[10px] text-slate-400">
          <span>🔒 Zero spam. Unsubscribe anytime.</span>
          <button id="tbVipLaterBtn" class="hover:text-slate-200 underline">Maybe later</button>
        </div>
      </div>
    `;

    document.body.appendChild(drawer);

    // Bind Close
    const closeBtn = document.getElementById('closeTbVipDrawer');
    const laterBtn = document.getElementById('tbVipLaterBtn');
    function hideDrawer(days = 14) {
      drawer.classList.add('translate-y-8', 'opacity-0');
      drawer.classList.remove('pointer-events-auto');
      drawer.classList.add('pointer-events-none');
      setDismissed(days);
      setTimeout(() => drawer.remove(), 500);
      document.removeEventListener('keydown', handleEsc);
    }

    function handleEsc(e) {
      if (e.key === 'Escape') hideDrawer(14);
    }
    document.addEventListener('keydown', handleEsc);

    if (closeBtn) closeBtn.addEventListener('click', () => hideDrawer(14));
    if (laterBtn) laterBtn.addEventListener('click', () => hideDrawer(14));

    // Bind Submit
    const form = document.getElementById('tbVipForm');
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const emailInput = document.getElementById('tbVipEmail');
        const em = emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!em || !emailRegex.test(em)) {
          if (typeof showToast === 'function') {
            showToast('⚠️ Please enter a valid email address.');
          }
          return;
        }

        let subscribers = [];
        try {
          const stored = localStorage.getItem(SUBSCRIBERS_KEY);
          if (stored) subscribers = JSON.parse(stored);
        } catch (err) {}

        if (!subscribers.includes(em)) {
          subscribers.push(em);
          try {
            localStorage.setItem(SUBSCRIBERS_KEY, JSON.stringify(subscribers));
          } catch (e) {}
        }

        drawer.innerHTML = `
          <div class="text-center py-4">
            <span class="text-3xl block mb-2">🎉</span>
            <h4 class="text-base font-bold text-white mb-1">Welcome to Tech Boss VIP!</h4>
            <p class="text-xs text-slate-300">You're on the list. Keep an eye on your inbox for our weekly benchmarks.</p>
          </div>
        `;
        setTimeout(() => hideDrawer(365), 3500);
      });
    }
  }

  function showDrawer() {
    const drawer = document.getElementById('tbVipDrawer');
    if (!drawer) return;
    drawer.classList.remove('translate-y-8', 'opacity-0', 'pointer-events-none');
    drawer.classList.add('translate-y-0', 'opacity-100', 'pointer-events-auto');
  }

  let triggered = false;
  function triggerOnce() {
    if (triggered || isDismissed()) return;
    triggered = true;
    createDrawer();
    setTimeout(showDrawer, 100);
  }

  // 1. Scroll trigger (50% scroll)
  window.addEventListener('scroll', () => {
    if (triggered) return;
    const scrollPos = window.scrollY + window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;
    if (scrollPos > docHeight * 0.5) {
      triggerOnce();
    }
  }, { passive: true });

  // 2. Desktop exit-intent trigger (mouse leaving viewport at top)
  document.addEventListener('mouseleave', (e) => {
    if (triggered) return;
    if (e.clientY <= 10) {
      triggerOnce();
    }
  });

  // 3. Time-based fallback (45 seconds)
  setTimeout(() => {
    if (!triggered) triggerOnce();
  }, 45000);

})();
