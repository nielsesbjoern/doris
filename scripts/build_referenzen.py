#!/usr/bin/env python3
"""Build referenzen main content (DE + EN) and refresh full pages."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from referenzen_data import FEATURED, SECTORS_DE, SECTORS_EN, TEXT
from wrap_pages import build_page, extract_main, META


def render_list(items, tag):
    lines = []
    for item in items:
        lines.append(f"            <li>{item.format(tag=tag)}</li>")
    return "\n".join(lines)


def render_sectors(sectors, tag, sector_count_label):
    blocks = []
    for title, items in sectors:
        count = sector_count_label.format(n=len(items))
        blocks.append(
            f"""        <details class="referenzen-sector">
          <summary class="referenzen-sector-title">
            <span class="referenzen-sector-name">{title}</span>
            <span class="referenzen-sector-meta">{count}</span>
          </summary>
          <ul class="referenzen-list">
{render_list(items, tag)}
          </ul>
        </details>"""
        )
    return "\n\n".join(blocks)


def build_main(lang):
    t = TEXT[lang]
    sectors = SECTORS_EN if lang == "en" else SECTORS_DE
    featured_items = "\n".join(
        f'          <li class="referenzen-featured-item">{item.format(tag=t["tag"])}</li>'
        for item in FEATURED
    )
    return f"""<!-- {t["comment"]} -->
    <section class="section page-section" id="referenzen">
      <div class="container">
        <header class="section-header section-header--wide">
          <p class="eyebrow">{t["eyebrow"]}</p>
          <h1>{t["h1"]}</h1>
          <p class="section-intro">
            {t["intro"]}
          </p>
        </header>

        <div class="referenzen-featured">
          <h2 class="referenzen-featured-title">{t["featured_title"]}</h2>
          <ul class="referenzen-featured-list">
{featured_items}
          </ul>
        </div>

        <div class="referenzen-sectors">
{render_sectors(sectors, t["tag"], t["sector_count"])}
        </div>

        <p class="referenzen-note">
          {t["note"]}
        </p>
        <p class="referenzen-disclaimer">
          {t["disclaimer"]}
        </p>
      </div>
    </section>"""


def main():
    filename = "referenzen.html"
    de_main = build_main("de")
    en_main = build_main("en")

    build_page("de", filename, de_main, ROOT / filename)
    build_page("en", filename, en_main, ROOT / "en" / filename)
    print("Built referenzen.html (DE + EN)")


if __name__ == "__main__":
    main()
