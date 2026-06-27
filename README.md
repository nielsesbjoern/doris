# Doris Gunsch – Website

Statische Website für [Doris Gunsch – Psychologische Managementberatung](https://www.doris-gunsch.eu).

## Build

```bash
python3 scripts/build.py
```

Einzelne Schritte (lokal, inkl. Asset-Generierung):

```bash
python3 scripts/build_fonts.py
python3 scripts/build_images.py
python3 scripts/build_favicons.py
python3 scripts/wrap_pages.py
python3 scripts/build_referenzen.py
python3 scripts/build_standorte.py
python3 scripts/build_sitemap.py
python3 scripts/build_llms.py
python3 scripts/build_minify.py   # styles.source.css → styles.css
```

Auf Vercel werden Font-, Bild- und Favicon-Schritte übersprungen (Assets sind committed; kein Pillow im Deploy). CSS wird aus `css/styles.source.css` minifiziert.

Abhängigkeiten für lokale Asset-Generierung: `pip install -r requirements.txt`

### Tests & Build-Check

```bash
python3 scripts/test_seo.py
python3 scripts/test_site.py
./scripts/check_build.sh          # Tests + Build + git diff (wie CI)
./scripts/install_git_hooks.sh    # Pre-commit-Hook optional installieren
```

## Inhalte bearbeiten

| Was | Wo |
|-----|-----|
| Seiteninhalt (Text in `<main>`) | `*.html` (DE) bzw. `en/*.html` (EN) |
| Navigation, SEO-Head, Shell | `scripts/wrap_pages.py` + `scripts/seo.py` |
| Standort-Seiten (Städte) | `scripts/standorte_data.py` → `build_standorte.py` |
| Referenzen | `scripts/referenzen_data.py` → `build_referenzen.py` |
| **Styles** | **`css/styles.source.css`** (nicht `styles.css` — wird beim Build minifiziert) |

Nach Änderungen am Inhalt oder an den Generatoren:

```bash
python3 scripts/build.py
```

`wrap_pages.py` extrahiert den `<main>`-Block und schreibt die vollständige Seite zurück — Shell-Änderungen direkt in den HTML-Dateien gehen beim Build verloren.

## Struktur

- `index.html`, `en/` — Seiten (DE + EN)
- `scripts/` — Generatoren für Shell, Standorte, Referenzen, Sitemap, LLM-Texte, Tests
- `css/styles.source.css` — bearbeitbare Styles; `css/styles.css` — minifiziertes Build-Artefakt
- `js/` — Skripte (`site.js` lädt mit `defer` am Seitenende)
- `public/` — Bilder, Fonts, Favicon

## Kontaktformular

Der Kontakt-Wizard erstellt einen Anfragetext im Browser. Standard: `mailto:` (kein Server-Empfang). Fallback: Text kopieren und an dg@doris-gunsch.eu senden. Optional: direkte Übermittlung über Formspree — Endpoint in `scripts/contact_config.py` (`FORMSPREE_ENDPOINT`) setzen, dann `python3 scripts/build.py` ausführen.

## Deployment

Vercel (`vercel.json`): `cleanUrls`, Security-Header, langfristiges Caching für `/public`, `/css`, `/js`.
