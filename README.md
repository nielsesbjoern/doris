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
```

Auf Vercel werden Font-, Bild- und Favicon-Schritte übersprungen (Assets sind committed; kein Pillow im Deploy).

Abhängigkeiten für lokale Asset-Generierung: `pip install -r requirements.txt`

## Inhalte bearbeiten

| Was | Wo |
|-----|-----|
| Seiteninhalt (Text in `<main>`) | `*.html` (DE) bzw. `en/*.html` (EN) |
| Navigation, SEO-Head, Shell | `scripts/wrap_pages.py` + `scripts/seo.py` |
| Standort-Seiten (Städte) | `scripts/standorte_data.py` → `build_standorte.py` |
| Referenzen | `scripts/referenzen_data.py` → `build_referenzen.py` |

Nach Änderungen am Inhalt oder an den Generatoren:

```bash
python3 scripts/build.py
```

`wrap_pages.py` extrahiert den `<main>`-Block und schreibt die vollständige Seite zurück — Shell-Änderungen direkt in den HTML-Dateien gehen beim Build verloren.

## Struktur

- `index.html`, `en/` — Seiten (DE + EN)
- `scripts/` — Generatoren für Shell, Standorte, Referenzen, Sitemap, LLM-Texte
- `css/`, `js/` — Styles und Skripte
- `public/` — Bilder, Fonts, Favicon

## Deployment

Vercel (`vercel.json`): `cleanUrls`, Security-Header, langfristiges Caching für `/public`, `/css`, `/js`.
