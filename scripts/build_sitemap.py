#!/usr/bin/env python3
"""Generate sitemap.xml with hreflang alternates for all DE/EN pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from wrap_pages import META  # noqa: E402
from seo import absolute_url, file_lastmod  # noqa: E402

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NS = "http://www.w3.org/1999/xhtml"


def build_sitemap() -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<urlset xmlns="{SITEMAP_NS}" xmlns:xhtml="{XHTML_NS}">',
    ]

    for filename in META:
        if filename == "404.html":
            continue

        de_path = ROOT / filename
        en_path = ROOT / "en" / filename
        lastmod = file_lastmod(de_path if de_path.exists() else en_path)
        de_url = absolute_url(filename, "de")
        en_url = absolute_url(filename, "en")

        for loc in (de_url, en_url):
            lines.append("  <url>")
            lines.append(f"    <loc>{loc}</loc>")
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
            for alt_lang, alt_href in (
                ("de", de_url),
                ("en", en_url),
                ("x-default", de_url),
            ):
                lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="{alt_lang}" href="{alt_href}" />'
                )
            lines.append("  </url>")

    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    out = ROOT / "sitemap.xml"
    out.write_text(build_sitemap(), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
