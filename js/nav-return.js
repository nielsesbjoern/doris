(function () {
  const STORAGE_KEY = 'doris-return-nav';
  const ENTRY_PREFIX = 'doris-entry-nav-';
  const isEn = document.documentElement.lang === 'en';

  const ENTRY_FLOW_PAGES = new Set(['coaching-formate', 'en/coaching-formate']);
  const KONTAKT_PAGES = new Set(['kontakt', 'en/kontakt']);

  const PAGE_LABELS = {
    '': { de: '← Zurück zur Startseite', en: '← Back to home' },
    en: { de: '← Zurück zur Startseite', en: '← Back to home' },
    kontakt: { de: '← Zurück zu Kontakt', en: '← Back to contact' },
    leistungen: { de: '← Zurück zu Leistungen', en: '← Back to services' },
    coaching: { de: '← Zurück zu Coaching', en: '← Back to coaching' },
    'coaching-formate': { de: '← Zurück zum Format-Finder', en: '← Back to format finder' },
    trainings: { de: '← Zurück zu Trainings', en: '← Back to training' },
    team: { de: '← Zurück zu Team & Prozessbegleitung', en: '← Back to team facilitation' },
    diagnostik: { de: '← Zurück zu Diagnostik', en: '← Back to diagnostics' },
    einsatzgebiete: { de: '← Zurück zu Einsatzgebieten', en: '← Back to service areas' },
    referenzen: { de: '← Zurück zu Referenzen', en: '← Back to references' },
    person: { de: '← Zurück zur Person', en: '← Back to about' },
    links: { de: '← Zurück zu Links', en: '← Back to links' },
    impressum: { de: '← Zurück zum Impressum', en: '← Back to legal notice' },
    datenschutz: { de: '← Zurück zum Datenschutz', en: '← Back to privacy policy' },
  };

  function pathKey(pathname) {
    let path = pathname.replace(/\/$/, '') || '/';
    if (path === '/') return '';
    if (path === '/en') return 'en';
    if (path.startsWith('/en/')) return path.slice(1);
    return path.slice(1);
  }

  function labelsForKey(key) {
    if (PAGE_LABELS[key]) return PAGE_LABELS[key];

    if (key.startsWith('standorte/')) {
      const heading = document.querySelector('main h1')?.textContent?.trim();
      if (heading) {
        return {
          de: `← Zurück zu ${heading}`,
          en: `← Back to ${heading}`,
        };
      }
      return {
        de: '← Zurück zu Einsatzgebieten',
        en: '← Back to service areas',
      };
    }

    const fallback = key.split('/').pop()?.replace(/-/g, ' ') || 'page';
    return {
      de: `← Zurück zu ${fallback}`,
      en: `← Back to ${fallback}`,
    };
  }

  function readReturnNav() {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  function clearReturnNav() {
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch {
      /* ignore */
    }
  }

  function readEntry(pageKey) {
    try {
      const raw = sessionStorage.getItem(`${ENTRY_PREFIX}${pageKey}`);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  function persistEntry(pageKey, context) {
    if (!context?.href) return;
    try {
      sessionStorage.setItem(
        `${ENTRY_PREFIX}${pageKey}`,
        JSON.stringify({
          href: context.href,
          labelDe: context.labelDe,
          labelEn: context.labelEn,
        })
      );
    } catch {
      /* ignore */
    }
  }

  function clearEntry(pageKey) {
    try {
      sessionStorage.removeItem(`${ENTRY_PREFIX}${pageKey}`);
    } catch {
      /* ignore */
    }
  }

  function applyBackContext(back, context) {
    if (!back || !context) return;
    if (context.href) back.href = context.href;
    back.textContent = isEn ? context.labelEn : context.labelDe;
  }

  function currentReturnContext() {
    const href = `${window.location.pathname}${window.location.hash}`;
    const labels = labelsForKey(pathKey(window.location.pathname));
    return { href, labelDe: labels.de, labelEn: labels.en };
  }

  function saveForTarget(targetHref) {
    const targetUrl = new URL(targetHref, window.location.href);
    const currentKey = pathKey(window.location.pathname);
    const targetKey = pathKey(targetUrl.pathname);
    const from = currentReturnContext();

    if (ENTRY_FLOW_PAGES.has(currentKey) && !KONTAKT_PAGES.has(targetKey)) {
      clearEntry(currentKey);
    }

    try {
      sessionStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          target: targetKey,
          href: from.href,
          labelDe: from.labelDe,
          labelEn: from.labelEn,
        })
      );
    } catch {
      /* sessionStorage unavailable */
    }
  }

  function applyReturnNav() {
    const back = document.querySelector('.page-back .btn-back');
    if (!back) return;

    const currentKey = pathKey(window.location.pathname);
    const stored = readReturnNav();

    if (stored?.target === currentKey) {
      applyBackContext(back, stored);
      clearReturnNav();

      if (ENTRY_FLOW_PAGES.has(currentKey)) {
        persistEntry(currentKey, stored);
      }
      return;
    }

    if (ENTRY_FLOW_PAGES.has(currentKey)) {
      const entry = readEntry(currentKey);
      if (entry) {
        applyBackContext(back, entry);
      }
    }
  }

  function shouldSkipLink(anchor) {
    const href = anchor.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) {
      return true;
    }
    if (anchor.target === '_blank' || anchor.hasAttribute('download')) return true;
    if (anchor.closest('.lang-switcher') || anchor.closest('.sidebar-lang')) return true;
    if (anchor.closest('.page-back')) return true;
    if (anchor.hasAttribute('data-no-return-nav')) return true;
    return false;
  }

  document.addEventListener('click', (event) => {
    if (event.defaultPrevented) return;

    const anchor = event.target.closest('a[href]');
    if (!anchor || shouldSkipLink(anchor)) return;

    let dest;
    try {
      dest = new URL(anchor.getAttribute('href'), window.location.href);
    } catch {
      return;
    }

    if (dest.origin !== window.location.origin) return;
    if (dest.pathname === window.location.pathname) return;

    saveForTarget(`${dest.pathname}${dest.hash}`);
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyReturnNav);
  } else {
    applyReturnNav();
  }

  window.DorisNavReturn = { saveForTarget };
})();
