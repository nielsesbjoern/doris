(function () {
  const root = document.getElementById('formate-vergleich');
  if (!root) return;

  const isEn = document.documentElement.lang === 'en';
  const groupTabs = root.querySelectorAll('.format-compare__group');
  const chipGroups = root.querySelectorAll('.format-compare__filter[data-chip-group]');
  const cards = root.querySelectorAll('.format-compare__card');
  const statusEl = document.getElementById('format-compare-status');

  let activeGroup = 'anlass';
  let activeFormat = 'all';

  function chipsForGroup(group) {
    return root.querySelectorAll(`.format-compare__chip[data-group="${group}"]`);
  }

  function setGroupState(group) {
    activeGroup = group;
    activeFormat = 'all';

    groupTabs.forEach((tab) => {
      const active = tab.dataset.group === group;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', active ? 'true' : 'false');
    });

    chipGroups.forEach((chipGroup) => {
      const visible = chipGroup.dataset.chipGroup === group;
      chipGroup.hidden = !visible;
    });

    chipsForGroup(group).forEach((chip) => {
      const isAll = chip.dataset.format === 'all';
      chip.classList.toggle('is-active', isAll);
      chip.setAttribute('aria-pressed', isAll ? 'true' : 'false');
    });

    applyFilters();
  }

  function setChipState(format) {
    activeFormat = format;
    chipsForGroup(activeGroup).forEach((chip) => {
      const active = chip.dataset.format === format;
      chip.classList.toggle('is-active', active);
      chip.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    applyFilters();
  }

  function formatTitle(id) {
    const chip = root.querySelector(
      `.format-compare__chip[data-format="${id}"][data-group="${activeGroup}"]`
    );
    return chip?.textContent.trim() ?? id;
  }

  function applyFilters() {
    let visibleCount = 0;

    cards.forEach((card) => {
      const inGroup = card.dataset.group === activeGroup;
      const formatMatch = activeFormat === 'all' || card.dataset.format === activeFormat;
      const visible = inGroup && formatMatch;
      card.classList.toggle('is-filtered-out', !visible);
      card.classList.toggle('is-highlighted', activeFormat !== 'all' && card.dataset.format === activeFormat);
      if (visible) visibleCount += 1;
    });

    if (!statusEl) return;

    if (activeFormat === 'all') {
      statusEl.textContent = '';
      return;
    }

    const template = isEn
      ? 'Showing: {format}'
      : 'Angezeigt: {format}';
    statusEl.textContent = template.replace('{format}', formatTitle(activeFormat));
  }

  function readHash() {
    const hash = window.location.hash.replace('#', '');
    if (!hash.startsWith('format-')) return;

    const id = hash.slice('format-'.length);
    const card = document.getElementById(`format-${id}`);
    if (!card) return;

    const group = card.dataset.group;
    if (group) setGroupState(group);
    setChipState(id);
    card.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  groupTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const group = tab.dataset.group;
      if (group && group !== activeGroup) {
        setGroupState(group);
      }
    });
  });

  root.querySelectorAll('.format-compare__chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      const format = chip.dataset.format || 'all';
      const group = chip.dataset.group;
      if (group && group !== activeGroup) {
        setGroupState(group);
      }
      setChipState(format);
    });
  });

  window.addEventListener('hashchange', readHash);

  setGroupState('anlass');
  readHash();
})();
