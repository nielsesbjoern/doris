(function () {
  if (document.body.dataset.page !== 'referenzen') return;

  const isEn = document.documentElement.lang === 'en';
  const sectorParam = 'sector';
  const searchParam = 'q';

  const featured = document.getElementById('referenzen-featured');
  const featuredItems = featured?.querySelectorAll('.referenzen-featured-item') ?? [];
  const sectors = document.querySelectorAll('.referenzen-sector');
  const chips = document.querySelectorAll('.referenzen-filter__chip');
  const searchInput = document.getElementById('referenzen-search');
  const statusEl = document.getElementById('referenzen-filter-status');
  const emptyEl = document.getElementById('referenzen-empty');
  const resetBtn = document.getElementById('referenzen-reset');

  let activeSector = 'all';
  let searchQuery = '';

  function sectorTitle(slug) {
    const el = document.querySelector(`.referenzen-filter__chip[data-sector="${slug}"]`);
    return el?.textContent.trim() ?? slug;
  }

  function setChipState(sector) {
    chips.forEach((chip) => {
      const active = chip.dataset.sector === sector;
      chip.classList.toggle('is-active', active);
      chip.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  }

  function matchesSearch(name) {
    if (!searchQuery) return true;
    return name.includes(searchQuery);
  }

  function applyFilters() {
    let visibleCount = 0;
    let visibleSectors = 0;
    const sectorNames = [];

    featuredItems.forEach((item) => {
      const itemSector = item.dataset.sector;
      const sectorMatch = activeSector === 'all' || itemSector === activeSector;
      const searchMatch = matchesSearch(item.dataset.name || '');
      const visible = sectorMatch && searchMatch;
      item.classList.toggle('is-filtered-out', !visible);
    });

    if (featured) {
      const anyFeatured = Array.from(featuredItems).some(
        (item) => !item.classList.contains('is-filtered-out')
      );
      featured.classList.toggle('is-filtered-out', !anyFeatured);
    }

    sectors.forEach((sectorEl) => {
      const slug = sectorEl.dataset.sector;
      const sectorMatch = activeSector === 'all' || slug === activeSector;
      let sectorVisibleCount = 0;

      sectorEl.querySelectorAll('.referenzen-list li').forEach((item) => {
        const searchMatch = matchesSearch(item.dataset.name || '');
        const visible = sectorMatch && searchMatch;
        item.classList.toggle('is-filtered-out', !visible);
        if (visible) sectorVisibleCount += 1;
      });

      const sectorVisible = sectorVisibleCount > 0;
      sectorEl.classList.toggle('is-filtered-out', !sectorVisible);

      if (sectorVisible) {
        visibleSectors += 1;
        visibleCount += sectorVisibleCount;
        if (activeSector === 'all' && searchQuery) {
          sectorNames.push(sectorTitle(slug));
        } else if (activeSector !== 'all') {
          sectorNames.push(sectorTitle(slug));
        }
        if (activeSector !== 'all' || searchQuery) {
          sectorEl.open = true;
        }
      }
    });

    const filtering = activeSector !== 'all' || searchQuery;
    if (emptyEl) {
      emptyEl.hidden = visibleCount > 0 || !filtering;
    }

    if (!statusEl || !filtering) {
      if (statusEl) statusEl.textContent = '';
      return;
    }

    if (visibleCount === 0) {
      statusEl.textContent = '';
      return;
    }

    if (activeSector !== 'all') {
      const template = isEn ? '{n} companies in {sector}' : '{n} Unternehmen in {sector}';
      statusEl.textContent = template
        .replace('{n}', String(visibleCount))
        .replace('{sector}', sectorTitle(activeSector));
      return;
    }

    const template = isEn
      ? '{n} companies in {count} sectors'
      : '{n} Unternehmen in {count} Branchen';
    statusEl.textContent = template
      .replace('{n}', String(visibleCount))
      .replace('{count}', String(visibleSectors));
  }

  function syncUrl() {
    const params = new URLSearchParams();
    if (activeSector !== 'all') params.set(sectorParam, activeSector);
    if (searchQuery) params.set(searchParam, searchQuery);
    const query = params.toString();
    const url = query
      ? `${window.location.pathname}?${query}`
      : window.location.pathname;
    window.history.replaceState(null, '', url);
  }

  function readUrl() {
    const params = new URLSearchParams(window.location.search);
    const sector = params.get(sectorParam);
    const query = params.get(searchParam);
    if (sector && document.querySelector(`.referenzen-filter__chip[data-sector="${sector}"]`)) {
      activeSector = sector;
    }
    if (query) {
      searchQuery = query.toLowerCase().trim();
      if (searchInput) searchInput.value = query;
    }
    setChipState(activeSector);
  }

  function resetFilters() {
    activeSector = 'all';
    searchQuery = '';
    if (searchInput) searchInput.value = '';
    setChipState('all');
    sectors.forEach((sectorEl) => {
      sectorEl.open = false;
    });
    applyFilters();
    syncUrl();
    searchInput?.focus();
  }

  chips.forEach((chip) => {
    chip.addEventListener('click', () => {
      activeSector = chip.dataset.sector || 'all';
      setChipState(activeSector);
      applyFilters();
      syncUrl();
    });
  });

  searchInput?.addEventListener('input', () => {
    searchQuery = searchInput.value.toLowerCase().trim();
    applyFilters();
    syncUrl();
  });

  searchInput?.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      e.preventDefault();
      resetFilters();
    }
  });

  resetBtn?.addEventListener('click', resetFilters);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && document.activeElement !== searchInput) {
      if (activeSector !== 'all' || searchQuery) {
        resetFilters();
      }
    }
  });

  readUrl();
  applyFilters();
})();
