(function () {
  const root = document.getElementById('formate-vergleich');
  if (!root) return;

  const isEn = document.documentElement.lang === 'en';
  const STORAGE_KEY = 'doris-format-inquiry';
  const contactPath = isEn ? '/en/kontakt' : '/kontakt';
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  const modeTabs = root.querySelectorAll('.format-guide__mode');
  const formatPanel = document.getElementById('format-panel');
  const items = root.querySelectorAll('.format-guide__item');
  const statusEl = document.getElementById('format-guide-status');
  const inquiryPanel = document.getElementById('format-guide-inquiry');
  const inquiryTextEl = document.getElementById('format-guide-inquiry-text');
  const inquiryBtn = document.getElementById('format-guide-inquiry-btn');
  const comparePanel = document.getElementById('format-guide-compare');
  const compareTable = comparePanel?.querySelector('.format-guide__table--compare');
  const clearBtn = document.getElementById('format-guide-clear');

  const i18n = isEn
    ? {
        maxTwo: 'At most two formats at once — please deselect one.',
        showing: 'Comparing: {a} and {b}',
        oneSelected: 'Selected: {a} — choose one more format.',
        detailsShow: 'Details',
        detailsHide: 'Close',
        inquiryOne: 'Enquire about this format',
        inquiryTwo: 'Enquire about these formats',
        inquiryHintOne: 'You selected {a}.',
        inquiryHintTwo: 'You are comparing {a} and {b}.',
        groupAnlass: 'By occasion',
        groupDurchfuehrung: 'By delivery',
      }
    : {
        maxTwo: 'Maximal zwei Formate gleichzeitig — bitte eines abwählen.',
        showing: 'Vergleich: {a} und {b}',
        oneSelected: 'Ausgewählt: {a} — wählen Sie ein weiteres Format.',
        detailsShow: 'Details',
        detailsHide: 'Schließen',
        inquiryOne: 'Anfrage zu diesem Format',
        inquiryTwo: 'Anfrage zu diesen Formaten',
        inquiryHintOne: 'Sie haben {a} ausgewählt.',
        inquiryHintTwo: 'Sie vergleichen {a} und {b}.',
        groupAnlass: 'Nach Anlass',
        groupDurchfuehrung: 'Nach Durchführung',
      };

  let activeGroup = 'anlass';
  const selected = new Set();

  function itemTitle(item) {
    return item.querySelector('.format-guide__name')?.textContent.trim() ?? '';
  }

  function itemTeaser(item) {
    return item.querySelector('.format-guide__teaser')?.textContent.trim() ?? '';
  }

  function itemRows(item) {
    const rows = new Map();
    item.querySelectorAll('.format-guide__row').forEach((row) => {
      const label = row.dataset.rowKey || row.querySelector('dt')?.textContent.trim();
      const value = row.querySelector('dd')?.textContent.trim();
      if (label) rows.set(label, value ?? '');
    });
    return rows;
  }

  function groupLabel(group) {
    return group === 'durchfuehrung' ? i18n.groupDurchfuehrung : i18n.groupAnlass;
  }

  function setGroupState(group) {
    activeGroup = group;
    selected.clear();

    modeTabs.forEach((tab) => {
      const active = tab.dataset.group === group;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', active ? 'true' : 'false');
      tab.tabIndex = active ? 0 : -1;
    });

    const activeTab = root.querySelector('.format-guide__mode.is-active');
    if (formatPanel && activeTab?.id) {
      formatPanel.setAttribute('aria-labelledby', activeTab.id);
    }

    items.forEach((item) => {
      const inGroup = item.dataset.group === group;
      item.hidden = !inGroup;
      item.open = false;
      item.classList.remove('is-picked', 'is-highlighted');
      const input = item.querySelector('.format-guide__pick-input');
      if (input) input.checked = false;
    });

    updateComparePanel();
    updateStatus();
    updateInquiryPanel();
  }

  function pickedItems() {
    return Array.from(selected)
      .map((id) => root.querySelector(`#format-${id}`))
      .filter(Boolean);
  }

  function updateComparePanel() {
    const picked = pickedItems();

    items.forEach((item) => {
      item.classList.toggle('is-picked', selected.has(item.dataset.format));
    });

    if (!comparePanel || !compareTable) return;

    if (picked.length < 2) {
      comparePanel.hidden = true;
      return;
    }

    const wasHidden = comparePanel.hidden;
    comparePanel.hidden = false;
    if (wasHidden && !prefersReducedMotion.matches) {
      comparePanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    const [a, b] = picked;
    const rowsA = itemRows(a);
    const rowsB = itemRows(b);

    const headCells = compareTable.querySelectorAll('thead .format-guide__compare-slot');
    if (headCells[0]) headCells[0].textContent = itemTitle(a);
    if (headCells[1]) headCells[1].textContent = itemTitle(b);

    compareTable.querySelectorAll('tbody tr').forEach((tr) => {
      const label = tr.dataset.rowLabel;
      const cells = tr.querySelectorAll('.format-guide__compare-slot');
      if (cells[0]) cells[0].textContent = rowsA.get(label) ?? '—';
      if (cells[1]) cells[1].textContent = rowsB.get(label) ?? '—';
    });
  }

  function updateInquiryPanel() {
    if (!inquiryPanel || !inquiryBtn) return;

    const picked = pickedItems();
    if (picked.length === 0) {
      inquiryPanel.hidden = true;
      return;
    }

    inquiryPanel.hidden = false;
    const titles = picked.map(itemTitle);

    if (inquiryTextEl) {
      if (picked.length === 1) {
        inquiryTextEl.textContent = i18n.inquiryHintOne.replace('{a}', titles[0]);
      } else {
        inquiryTextEl.textContent = i18n.inquiryHintTwo
          .replace('{a}', titles[0])
          .replace('{b}', titles[1]);
      }
    }

    inquiryBtn.textContent = picked.length === 1 ? i18n.inquiryOne : i18n.inquiryTwo;

    if (!prefersReducedMotion.matches) {
      inquiryPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  function updateStatus() {
    if (!statusEl) return;
    const picked = pickedItems();

    if (picked.length === 0) {
      statusEl.textContent = '';
      return;
    }

    if (picked.length === 1) {
      statusEl.textContent = i18n.oneSelected.replace('{a}', itemTitle(picked[0]));
      return;
    }

    statusEl.textContent = '';
  }

  function buildInquiryPayload() {
    const picked = pickedItems();
    return {
      source: 'format-finder',
      group: activeGroup,
      groupLabel: groupLabel(activeGroup),
      compare: picked.length > 1,
      formats: picked.map((item) => {
        const rows = itemRows(item);
        const durationKey = isEn ? 'Duration / setting' : 'Dauer / Setting';
        const occasionKey = isEn ? 'Typical occasion' : 'Typischer Anlass';
        return {
          id: item.dataset.format,
          title: itemTitle(item),
          duration: rows.get(durationKey) || itemTeaser(item),
          occasion: rows.get(occasionKey) || '',
        };
      }),
    };
  }

  function goToContactInquiry() {
    const picked = pickedItems();
    if (picked.length === 0) return;

    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(buildInquiryPayload()));
    } catch {
      /* sessionStorage unavailable — still navigate */
    }

    window.DorisNavReturn?.saveForTarget(`${contactPath}?leistung=coaching#kontakt-anfrage`);
    window.location.href = `${contactPath}?leistung=coaching#kontakt-anfrage`;
  }

  function togglePick(formatId, checked) {
    if (checked) {
      if (selected.size >= 2) {
        statusEl.textContent = i18n.maxTwo;
        const input = root.querySelector(
          `.format-guide__pick-input[value="${formatId}"]`
        );
        if (input) input.checked = false;
        return;
      }
      selected.add(formatId);
    } else {
      selected.delete(formatId);
    }

    updateComparePanel();
    updateStatus();
    updateInquiryPanel();
  }

  function clearSelection() {
    selected.clear();
    root.querySelectorAll('.format-guide__pick-input').forEach((input) => {
      input.checked = false;
    });
    updateComparePanel();
    updateStatus();
    updateInquiryPanel();
  }

  function updateToggleLabel(item) {
    const toggle = item.querySelector('.format-guide__toggle');
    if (toggle) {
      toggle.textContent = item.open ? i18n.detailsHide : i18n.detailsShow;
    }
  }

  function readHash() {
    const hash = window.location.hash.replace('#', '');
    if (!hash.startsWith('format-')) return;

    const id = hash.slice('format-'.length);
    const item = document.getElementById(`format-${id}`);
    if (!item) return;

    const group = item.dataset.group;
    if (group) setGroupState(group);
    item.open = true;
    updateToggleLabel(item);
    item.classList.add('is-highlighted');
    item.scrollIntoView({ behavior: 'smooth', block: 'start' });
    window.setTimeout(() => item.classList.remove('is-highlighted'), 2000);
  }

  function activateTab(tab) {
    const group = tab.dataset.group;
    if (group && group !== activeGroup) {
      setGroupState(group);
    }
    tab.focus();
  }

  modeTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      activateTab(tab);
    });

    tab.addEventListener('keydown', (e) => {
      const tabs = Array.from(modeTabs);
      const index = tabs.indexOf(tab);
      if (index < 0) return;

      let next = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        next = tabs[(index + 1) % tabs.length];
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        next = tabs[(index - 1 + tabs.length) % tabs.length];
      } else if (e.key === 'Home') {
        next = tabs[0];
      } else if (e.key === 'End') {
        next = tabs[tabs.length - 1];
      }

      if (next) {
        e.preventDefault();
        activateTab(next);
      }
    });
  });

  root.querySelectorAll('[data-format-pick]').forEach((pick) => {
    pick.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  });

  root.querySelectorAll('.format-guide__pick-input').forEach((input) => {
    input.addEventListener('change', () => {
      togglePick(input.value, input.checked);
    });
  });

  items.forEach((item) => {
    item.addEventListener('toggle', () => {
      updateToggleLabel(item);
    });
  });

  clearBtn?.addEventListener('click', clearSelection);
  inquiryBtn?.addEventListener('click', goToContactInquiry);

  window.addEventListener('hashchange', readHash);

  setGroupState('anlass');
  readHash();
})();
