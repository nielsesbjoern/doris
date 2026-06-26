(function () {
  const root = document.getElementById('contact-wizard');
  if (!root) return;

  const isEn = document.documentElement.lang === 'en';
  const RECIPIENT = 'dg@doris-gunsch.eu';
  const NL = '\r\n';
  const MAX_MAILTO_LENGTH = 1800;
  const AUTO_ADVANCE_MS = 220;

  const steps = root.querySelectorAll('[data-wizard-step]');
  const progressFill = root.querySelector('.contact-wizard__progress-fill');
  const progressLabel = root.querySelector('.contact-wizard__progress-label');
  const stepTitleEl = root.querySelector('#wizard-step-title');
  const btnBack = root.querySelector('[data-wizard-back]');
  const btnNext = root.querySelector('[data-wizard-next]');
  const btnMail = root.querySelector('[data-wizard-mail]');
  const btnMailFallback = root.querySelector('[data-wizard-mail-fallback]');
  const btnCopy = root.querySelector('[data-wizard-copy]');
  const btnSubmit = root.querySelector('[data-wizard-submit]');
  const previewEl = root.querySelector('[data-wizard-preview]');
  const statusEl = root.querySelector('[data-wizard-status]');
  const mailHintEl = root.querySelector('[data-wizard-mail-hint]');
  const cityField = root.querySelector('[data-wizard-city-field]');
  const cityInput = root.querySelector('[data-wizard-city]');

  let currentStep = 1;
  let advanceTimer = null;
  let copyResetTimer = null;
  const totalSteps = steps.length;

  const i18n = isEn
    ? {
        step: (n) => `Step ${n} of ${totalSteps}`,
        required: 'Please complete the required fields before continuing.',
        selectOption: 'Please select an option.',
        subjectPrefix: 'Enquiry',
        mailHint:
          'Your email app opens with the text above. Please review the message and send it.',
        mailManualHint:
          'Copy text, open email icon, paste and send.',
        copy: 'Copy text',
        copied: 'Copied',
        copyFailed: 'Copy failed — please select the text above manually.',
      }
    : {
        step: (n) => `Schritt ${n} von ${totalSteps}`,
        required: 'Bitte füllen Sie die Pflichtfelder aus, bevor Sie fortfahren.',
        selectOption: 'Bitte wählen Sie eine Option.',
        subjectPrefix: 'Anfrage',
        mailHint:
          'Es öffnet sich Ihr E-Mail-Programm mit dem Text oben. Bitte prüfen Sie die Nachricht und senden Sie sie ab.',
        mailManualHint:
          'Text kopieren, E-Mail-Symbol öffnen, einfügen und absenden.',
        copy: 'Text kopieren',
        copied: 'Kopiert',
        copyFailed: 'Kopieren fehlgeschlagen — bitte markieren Sie den Text oben manuell.',
      };

  function selectedChip(field) {
    const chip = root.querySelector(`.contact-wizard__chip[data-field="${field}"].is-active`);
    return chip ? chip.textContent.trim() : '';
  }

  function chipValue(field) {
    const chip = root.querySelector(`.contact-wizard__chip[data-field="${field}"].is-active`);
    return chip?.dataset.value ?? '';
  }

  function inputValue(name) {
    const el = root.querySelector(`[data-wizard-input="${name}"]`);
    return el?.value.trim() ?? '';
  }

  function needsCity() {
    const v = chipValue('durchfuehrung');
    return v === 'vor-ort' || v === 'hybrid';
  }

  function formatDurchfuehrung() {
    const base = selectedChip('durchfuehrung');
    if (!base) return '';
    if (needsCity()) {
      const city = inputValue('stadt');
      return city ? `${base} — ${city}` : base;
    }
    return base;
  }

  function collectData() {
    return {
      leistung: selectedChip('leistung'),
      anlass: selectedChip('anlass'),
      zielgruppe: selectedChip('zielgruppe'),
      teilnehmer: selectedChip('teilnehmer'),
      durchfuehrung: formatDurchfuehrung(),
      zeithorizont: selectedChip('zeithorizont'),
      name: inputValue('name'),
      firma: inputValue('firma'),
      position: inputValue('position'),
      telefon: inputValue('telefon'),
      freitext: inputValue('freitext'),
    };
  }

  function fieldLine(label, value) {
    return `· ${label}: ${value}${NL}`;
  }

  function sectionBlock(title, lines) {
    return `${NL}${title}${NL}${NL}${lines}`;
  }

  function freitextBlock(text) {
    return text
      .split(/\r?\n/)
      .map((line) => (line ? `  ${line}` : ''))
      .join(NL);
  }

  function buildEmailBody(data) {
    if (isEn) {
      let body =
        `Dear Ms Gunsch,${NL}${NL}` +
        `Via your website doris-gunsch.eu I would like to submit a confidential enquiry ` +
        `and look forward to hearing from you.` +
        sectionBlock(
          'ENQUIRY — OVERVIEW',
          fieldLine('Service area', data.leistung) +
            fieldLine('Context', data.anlass) +
            fieldLine('Target group', data.zielgruppe) +
            fieldLine('Participants', data.teilnehmer) +
            fieldLine('Format', data.durchfuehrung) +
            fieldLine('Time frame', data.zeithorizont),
        ) +
        sectionBlock(
          'CONTACT PERSON',
          fieldLine('Name', data.name) +
            fieldLine('Organisation', data.firma) +
            fieldLine('Role', data.position) +
            (data.telefon ? fieldLine('Phone', data.telefon) : ''),
        );

      if (data.freitext) {
        body += sectionBlock('ADDITIONAL NOTES', `${freitextBlock(data.freitext)}${NL}`);
      }

      body +=
        `${NL}—${NL}${NL}` +
        `I look forward to your reply regarding availability, approach and next steps.${NL}${NL}` +
        `Kind regards${NL}${NL}` +
        `${data.name}${NL}` +
        `${data.position}${NL}` +
        `${data.firma}`;

      return body;
    }

    let body =
      `Sehr geehrte Frau Gunsch,${NL}${NL}` +
      `über Ihre Website doris-gunsch.eu stelle ich eine vertrauliche Anfrage ` +
      `und freue mich auf Ihre Rückmeldung.` +
      sectionBlock(
        'ANFRAGE — ÜBERBLICK',
        fieldLine('Leistungsbereich', data.leistung) +
          fieldLine('Anlass', data.anlass) +
          fieldLine('Zielgruppe', data.zielgruppe) +
          fieldLine('Teilnehmerzahl', data.teilnehmer) +
          fieldLine('Durchführung', data.durchfuehrung) +
          fieldLine('Zeithorizont', data.zeithorizont),
      ) +
      sectionBlock(
        'ANSPRECHPARTNER/IN',
        fieldLine('Name', data.name) +
          fieldLine('Organisation', data.firma) +
          fieldLine('Position', data.position) +
          (data.telefon ? fieldLine('Telefon', data.telefon) : ''),
      );

    if (data.freitext) {
      body += sectionBlock('ERGÄNZUNG', `${freitextBlock(data.freitext)}${NL}`);
    }

    body +=
      `${NL}—${NL}${NL}` +
      `Ich freue mich auf Ihre Rückmeldung zu Verfügbarkeit, Vorgehen und den nächsten Schritten.${NL}${NL}` +
      `Mit freundlichen Grüßen${NL}${NL}` +
      `${data.name}${NL}` +
      `${data.position}${NL}` +
      `${data.firma}`;

    return body;
  }

  function buildSubject(data) {
    const who = data.firma || data.name;
    return `${i18n.subjectPrefix}: ${data.leistung} — ${who}`;
  }

  function buildMailtoLink(data, includeBody = true) {
    const subject = buildSubject(data);
    if (!includeBody) {
      return `mailto:${RECIPIENT}?subject=${encodeURIComponent(subject)}`;
    }
    const body = buildEmailBody(data);
    return `mailto:${RECIPIENT}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  }

  function isMailTooLong(data) {
    return buildMailtoLink(data, true).length > MAX_MAILTO_LENGTH;
  }

  function openMailtoLink(link) {
    const anchor = document.createElement('a');
    anchor.href = link;
    anchor.rel = 'noopener';
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
  }

  function setManualMailMode(manual) {
    if (btnMail) btnMail.hidden = manual;
    if (btnMailFallback) btnMailFallback.hidden = !manual;
    if (mailHintEl) {
      mailHintEl.textContent = manual ? i18n.mailManualHint : i18n.mailHint;
    }
  }

  function updateMailMode() {
    if (currentStep !== totalSteps) return;
    setManualMailMode(isMailTooLong(collectData()));
  }

  async function copyPreviewText() {
    const text = previewEl?.textContent ?? '';
    if (!text) return false;

    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(text);
        return true;
      }
    } catch {
      /* fall through */
    }

    if (!previewEl) return false;
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(previewEl);
    selection?.removeAllRanges();
    selection?.addRange(range);
    try {
      return document.execCommand('copy');
    } catch {
      return false;
    } finally {
      selection?.removeAllRanges();
    }
  }

  function flashCopyButton(copied) {
    if (!btnCopy) return;
    clearTimeout(copyResetTimer);
    btnCopy.textContent = copied ? i18n.copied : i18n.copyFailed;
    copyResetTimer = setTimeout(() => {
      btnCopy.textContent = i18n.copy;
    }, 2000);
  }

  async function handleCopyClick() {
    const ok = await copyPreviewText();
    flashCopyButton(ok);
    if (!ok) {
      setStatus(i18n.copyFailed, true);
    } else {
      setStatus('');
    }
  }

  function setStatus(message, isError) {
    if (!statusEl) return;
    statusEl.textContent = message;
    statusEl.hidden = !message;
    statusEl.classList.toggle('is-error', Boolean(isError));
  }

  function updateCityVisibility() {
    if (!cityField) return;
    const show = needsCity();
    cityField.hidden = !show;
    if (!show && cityInput) {
      cityInput.value = '';
    }
  }

  function filterAnlassOptions() {
    const leistung = chipValue('leistung');
    root.querySelectorAll('.contact-wizard__chip[data-field="anlass"]').forEach((chip) => {
      const groups = (chip.dataset.leistung || '').split(/\s+/).filter(Boolean);
      const match =
        groups.includes('all') ||
        (leistung && groups.includes(leistung)) ||
        !leistung;
      chip.hidden = !match;
      if (!match) {
        chip.classList.remove('is-active');
        chip.setAttribute('aria-pressed', 'false');
      }
    });
  }

  function validateStep(step) {
    if (step === 1) {
      return chipValue('leistung') ? null : i18n.selectOption;
    }
    if (step === 2) {
      return chipValue('anlass') ? null : i18n.selectOption;
    }
    if (step === 3) {
      if (!chipValue('zielgruppe') || !chipValue('teilnehmer') || !chipValue('durchfuehrung') || !chipValue('zeithorizont')) {
        return i18n.selectOption;
      }
      if (needsCity() && !inputValue('stadt')) {
        return i18n.required;
      }
      return null;
    }
    if (step === 4) {
      if (!inputValue('name') || !inputValue('firma') || !inputValue('position')) {
        return i18n.required;
      }
      return null;
    }
    return null;
  }

  function updatePreview() {
    if (!previewEl) return;
    previewEl.textContent = buildEmailBody(collectData());
    updateMailMode();
  }

  function showStep(step) {
    currentStep = step;
    steps.forEach((panel) => {
      const n = Number(panel.dataset.wizardStep);
      const active = n === step;
      panel.hidden = !active;
      panel.classList.toggle('is-active', active);
    });

    if (progressFill) {
      progressFill.style.width = `${((step - 1) / (totalSteps - 1)) * 100}%`;
    }
    if (progressLabel) {
      progressLabel.textContent = i18n.step(step);
    }

    const activePanel = root.querySelector(`[data-wizard-step="${step}"]`);
    if (stepTitleEl && activePanel?.dataset.stepTitle) {
      stepTitleEl.textContent = activePanel.dataset.stepTitle;
    }

    if (btnBack) btnBack.hidden = step === 1;
    if (btnNext) btnNext.hidden = step !== 4 && step !== 5;
    if (btnSubmit) btnSubmit.hidden = step !== totalSteps;
    if (btnCopy) btnCopy.hidden = step !== totalSteps;

    if (step !== totalSteps) {
      setManualMailMode(false);
      if (btnCopy) btnCopy.textContent = i18n.copy;
    }

    if (step === totalSteps) {
      updatePreview();
      setStatus('');
    } else if (step === 5) {
      root.querySelector('[data-wizard-input="freitext"]')?.focus();
    }
  }

  function goNext() {
    if (currentStep >= totalSteps) return;
    const error = validateStep(currentStep);
    if (error) {
      setStatus(error, true);
      return;
    }
    setStatus('');
    showStep(currentStep + 1);
    root.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function scheduleAutoAdvance() {
    clearTimeout(advanceTimer);
    advanceTimer = setTimeout(() => {
      if (validateStep(currentStep) === null) {
        goNext();
      }
    }, AUTO_ADVANCE_MS);
  }

  function tryAutoAdvanceFromChip(field) {
    if (currentStep === 1 && field === 'leistung') {
      scheduleAutoAdvance();
      return;
    }
    if (currentStep === 2 && field === 'anlass') {
      scheduleAutoAdvance();
      return;
    }
    if (currentStep === 3) {
      if (field === 'durchfuehrung' && needsCity()) {
        cityInput?.focus();
        return;
      }
      if (validateStep(3) === null) {
        scheduleAutoAdvance();
      }
    }
  }

  function activateChip(chip) {
    const field = chip.dataset.field;
    root.querySelectorAll(`.contact-wizard__chip[data-field="${field}"]`).forEach((el) => {
      const active = el === chip;
      el.classList.toggle('is-active', active);
      el.setAttribute('aria-pressed', active ? 'true' : 'false');
    });

    if (field === 'leistung') {
      filterAnlassOptions();
    }
    if (field === 'durchfuehrung') {
      updateCityVisibility();
    }

    tryAutoAdvanceFromChip(field);
  }

  function goBack() {
    clearTimeout(advanceTimer);
    setStatus('');
    if (currentStep > 1) {
      showStep(currentStep - 1);
    }
  }

  function openMailto() {
    const error = validateStep(4);
    if (error) {
      setStatus(error, true);
      showStep(4);
      return;
    }

    const data = collectData();
    const link = buildMailtoLink(data, true);

    if (link.length > MAX_MAILTO_LENGTH) {
      updatePreview();
      setManualMailMode(true);
      setStatus('');
      return;
    }

    setStatus('');
    openMailtoLink(link);
  }

  function openMailFallback() {
    const data = collectData();
    setStatus('');
    openMailtoLink(buildMailtoLink(data, false));
  }

  root.querySelectorAll('.contact-wizard__chip').forEach((chip) => {
    chip.addEventListener('click', () => activateChip(chip));
  });

  btnBack?.addEventListener('click', goBack);
  btnNext?.addEventListener('click', goNext);
  btnMail?.addEventListener('click', openMailto);
  btnMailFallback?.addEventListener('click', openMailFallback);
  btnCopy?.addEventListener('click', handleCopyClick);

  root.querySelectorAll('[data-wizard-input]').forEach((input) => {
    input.addEventListener('input', () => {
      if (currentStep === totalSteps) {
        updatePreview();
        return;
      }
      if (currentStep === 3 && input.dataset.wizardInput === 'stadt' && validateStep(3) === null) {
        scheduleAutoAdvance();
      }
    });
  });

  filterAnlassOptions();
  updateCityVisibility();
  showStep(1);
})();
