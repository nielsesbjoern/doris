(function () {
  const sidebar = document.getElementById('site-sidebar');
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  const sidebarOverlay = document.querySelector('.sidebar-overlay');
  const langSwitcher = document.getElementById('lang-switcher');
  const langTrigger = document.getElementById('lang-switcher-trigger');
  const langCurrent = langSwitcher?.querySelector('.lang-switcher__current');
  const langOptions = langSwitcher?.querySelectorAll('.lang-switcher__option');
  const themeToggle = document.getElementById('theme-toggle');
  const yearEl = document.getElementById('year');
  const isEn = document.documentElement.lang === 'en' || window.location.pathname.includes('/en/');
  const currentLang = isEn ? 'en' : 'de';
  const touchLangMq = window.matchMedia('(hover: none), (pointer: coarse)');
  const THEME_KEY = 'dg-theme';

  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  function closeSidebar() {
    sidebar?.classList.remove('is-open');
    sidebarToggle?.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('sidebar-open');
  }

  function openSidebar() {
    sidebar?.classList.add('is-open');
    sidebarToggle?.setAttribute('aria-expanded', 'true');
    document.body.classList.add('sidebar-open');
  }

  sidebarToggle?.addEventListener('click', () => {
    if (sidebar?.classList.contains('is-open')) {
      closeSidebar();
    } else {
      openSidebar();
    }
  });

  window.matchMedia('(min-width: 1024px)').addEventListener('change', (e) => {
    if (e.matches) closeSidebar();
  });

  sidebarOverlay?.addEventListener('click', closeSidebar);

  sidebar?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      if (window.matchMedia('(max-width: 1023px)').matches) {
        closeSidebar();
      }
    });
  });

  function closeLangMenu() {
    if (!langSwitcher) return;
    langSwitcher.classList.remove('is-open');
    langTrigger?.setAttribute('aria-expanded', 'false');
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeSidebar();
      closeLangMenu();
    }
  });

  function relativePagePath() {
    const path = window.location.pathname;
    if (path.includes('/en/')) {
      return path.split('/en/').pop() || 'index.html';
    }
    const trimmed = path.replace(/^\//, '');
    return trimmed || 'index.html';
  }

  function langUrl(targetLang) {
    const rel = relativePagePath();
    if (targetLang === 'en') {
      return isEn ? null : `en/${rel}`;
    }
    const enDepth = (relativePagePath().match(/\//g) || []).length + 1;
    return isEn ? `${'../'.repeat(enDepth)}${rel}` : null;
  }

  function setLangUI(lang) {
    if (langCurrent) {
      langCurrent.textContent = lang.toUpperCase();
    }
    langOptions?.forEach((option) => {
      const active = option.dataset.lang === lang;
      option.classList.toggle('is-active', active);
      option.setAttribute('aria-selected', active ? 'true' : 'false');
    });
  }

  function navigateLang(target) {
    const url = langUrl(target);
    if (url) {
      localStorage.setItem('dg-lang', target);
      window.location.href = url;
    }
  }

  if (langSwitcher) {
    setLangUI(currentLang);

    langOptions?.forEach((option) => {
      option.addEventListener('click', () => {
        const target = option.dataset.lang;
        if (target && target !== currentLang) {
          navigateLang(target);
        } else {
          closeLangMenu();
        }
      });
    });

    langSwitcher.addEventListener('mouseenter', () => {
      if (!touchLangMq.matches) {
        langTrigger?.setAttribute('aria-expanded', 'true');
      }
    });

    langSwitcher.addEventListener('mouseleave', () => {
      if (!touchLangMq.matches) {
        langTrigger?.setAttribute('aria-expanded', 'false');
      }
    });

    langTrigger?.addEventListener('click', (e) => {
      if (!touchLangMq.matches) return;
      e.preventDefault();
      const open = langSwitcher.classList.toggle('is-open');
      langTrigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    document.addEventListener('click', (e) => {
      if (!langSwitcher.contains(e.target)) {
        closeLangMenu();
      }
    });
  }

  const savedLang = localStorage.getItem('dg-lang');
  if (savedLang && ((savedLang === 'en' && !isEn) || (savedLang === 'de' && isEn))) {
    const url = langUrl(savedLang);
    if (url && !window.location.search.includes('noredirect')) {
      window.location.replace(url);
    }
  }

  function getPreferredTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function themeLabel(theme) {
    if (isEn) {
      return theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    }
    return theme === 'dark' ? 'Hellmodus aktivieren' : 'Dunkelmodus aktivieren';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    if (themeToggle) {
      themeToggle.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
      themeToggle.setAttribute('aria-label', themeLabel(theme));
    }
  }

  applyTheme(getPreferredTheme());

  themeToggle?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
  });

  function initScrollProgress() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    let ticking = false;

    function updateScrollProgress() {
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      const progress = scrollable > 0 ? Math.min(1, Math.max(0, window.scrollY / scrollable)) : 0;
      document.documentElement.style.setProperty('--scroll-progress', String(progress));
      ticking = false;
    }

    function onScroll() {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(updateScrollProgress);
      }
    }

    updateScrollProgress();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
  }

  initScrollProgress();
})();
