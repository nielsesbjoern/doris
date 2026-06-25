# Doris Gunsch – Website

Statische Website für [Doris Gunsch – Psychologische Managementberatung](https://www.doris-gunsch.eu).

## Build

```bash
python3 scripts/build_fonts.py
python3 scripts/build_images.py
python3 scripts/wrap_pages.py
python3 scripts/build_referenzen.py
python3 scripts/build_standorte.py
python3 scripts/build_sitemap.py
python3 scripts/build_llms.py
```

## Struktur

- `index.html`, `en/` — Seiten (DE + EN)
- `scripts/` — Generatoren für Shell, Standorte, Referenzen, Sitemap
- `css/`, `js/` — Styles und Skripte
- `public/` — Bilder, Favicon
