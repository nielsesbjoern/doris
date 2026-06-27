#!/usr/bin/env python3
"""Build referenzen main content (DE + EN) and refresh full pages."""
from pathlib import Path
import html
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from referenzen_data import (  # noqa: E402
    FEATURED,
    SECTOR_SLUGS,
    SECTORS_DE,
    SECTORS_EN,
    TEXT,
)
from wrap_pages import build_page  # noqa: E402


def search_key(raw: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw)
    text = html.unescape(text)
    return text.lower().strip()


def render_list(items, tag):
    lines = []
    for item in items:
        rendered = item.format(tag=tag)
        key = html.escape(search_key(rendered), quote=True)
        lines.append(f'            <li data-name="{key}">{rendered}</li>')
    return "\n".join(lines)


def render_sectors(sectors, slugs, tag, sector_count_label):
    blocks = []
    for (title, items), slug in zip(sectors, slugs):
        count = sector_count_label.format(n=len(items))
        blocks.append(
            f"""        <details class="referenzen-sector" id="sector-{slug}" data-sector="{slug}">
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


def render_filter_chips(sectors, slugs, t):
    chips = [
        f"""          <button type="button" class="referenzen-filter__chip is-active" data-sector="all" aria-pressed="true">
            {t["filter_all"]}
          </button>"""
    ]
    for (title, _items), slug in zip(sectors, slugs):
        chips.append(
            f"""          <button type="button" class="referenzen-filter__chip" data-sector="{slug}" aria-pressed="false">
            {title}
          </button>"""
        )
    return "\n".join(chips)


def render_featured_item(item: dict, lang: str, tag_label: str) -> str:
    context = item["context_de"] if lang == "de" else item["context_en"]
    name_html = html.escape(item["name"])
    if item.get("tag"):
        name_html = (
            f'<span class="referenzen-featured-name">{name_html}</span> '
            f'<span class="ref-tag ref-tag--stacked">{html.escape(tag_label)}</span>'
        )
    search_name = item["name"]
    key = html.escape(search_key(search_name), quote=True)
    return (
        f'          <li class="referenzen-featured-item" data-sector="{item["sector"]}" '
        f'data-name="{key}">\n'
        f'            <p class="referenzen-featured-name">{name_html}</p>\n'
        f'            <p class="referenzen-featured-context">{html.escape(context)}</p>\n'
        f"          </li>"
    )


def build_main(lang):
    t = TEXT[lang]
    sectors = SECTORS_EN if lang == "en" else SECTORS_DE
    featured_items = "\n".join(
        render_featured_item(item, lang, t["tag"]) for item in FEATURED
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

        <div class="referenzen-featured" id="referenzen-featured">
          <h2 class="referenzen-featured-title">{t["featured_title"]}</h2>
          <ul class="referenzen-featured-list">
{featured_items}
          </ul>
        </div>

        <div class="referenzen-toolbar" role="search">
          <div class="referenzen-filter" role="group" aria-label="{t["filter_label"]}">
{render_filter_chips(sectors, SECTOR_SLUGS, t)}
          </div>
          <label class="referenzen-search">
            <span class="visually-hidden">{t["search_label"]}</span>
            <input
              type="search"
              id="referenzen-search"
              class="referenzen-search__input"
              placeholder="{t["search_placeholder"]}"
              autocomplete="off"
              enterkeyhint="search">
          </label>
          <p class="referenzen-filter-status" id="referenzen-filter-status" aria-live="polite" aria-atomic="true"></p>
        </div>

        <p class="referenzen-empty" id="referenzen-empty" hidden>
          {t["filter_empty"]}
          <button type="button" class="referenzen-empty__reset" id="referenzen-reset">{t["filter_reset"]}</button>
        </p>

        <div class="referenzen-sectors" id="referenzen-sectors">
{render_sectors(sectors, SECTOR_SLUGS, t["tag"], t["sector_count"])}
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
