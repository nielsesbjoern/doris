#!/usr/bin/env python3
"""Build city landing pages (DE + EN) and patch homepage accordion."""
from pathlib import Path
import html
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from standorte_data import (
    CITIES,
    CITY_SLUGS,
    EINSATZGEBIETE_COPY,
    HOME_GROUPS,
    HOME_STANDORTE,
    MAP_CITIES,
    MAP_SLUGS,
    MAP_SUBMAP_CITIES,
    ORPHAN_SLUGS,
    REACH_COPY,
    REACH_DESCRIPTIONS,
    REACH_FEATURED_SLUGS,
    RELATED_SLUGS,
    SERVICE_LINKS,
    STANDORT_UI,
    STANDORTE_META,
)
from wrap_pages import META, build_page, nav_prefix
from seo import page_href, wizard_href

HOME_STANDORTE_MARKER = "<!-- HOME_STANDORTE -->"
EINSATZGEBIETE_MAP_MARKER = "<!-- EINSATZGEBIETE_MAP -->"
EINSATZGEBIETE_PLACES_MARKER = "<!-- EINSATZGEBIETE_PLACES -->"


def _list_items(items: list[str]) -> str:
    return "\n".join(f"              <li>{item}</li>" for item in items)


def _ref_items(items: list) -> str:
    blocks = []
    for item in items:
        if isinstance(item, tuple):
            name, context = item
            blocks.append(
                f"""              <li class="standort-ref-item">
                <span class="standort-ref-name">{name}</span>
                <span class="standort-ref-context">{context}</span>
              </li>"""
            )
        else:
            blocks.append(f"              <li>{item}</li>")
    return "\n".join(blocks)


def _formats(items: list[tuple[str, str]]) -> str:
    blocks = []
    for title, text in items:
        blocks.append(
            f"""            <div class="standort-format">
              <p class="standort-format__title">{title}</p>
              <p>{text}</p>
            </div>"""
        )
    return "\n".join(blocks)


def _faq(items: list[tuple[str, str]]) -> str:
    blocks = []
    for question, answer in items:
        blocks.append(
            f"""          <details class="standort-faq-item">
            <summary>{question}</summary>
            <p>{answer}</p>
          </details>"""
        )
    return "\n".join(blocks)


def _services(lang: str, asset: str) -> str:
    links = SERVICE_LINKS[lang]
    items = "\n".join(
        f'              <li><a href="{page_href(href, asset)}" class="card-link">{label}</a></li>'
        for href, label in links
    )
    overview_label = (
        "Ausführliche Leistungsbeschreibungen"
        if lang == "de"
        else "Detailed service descriptions"
    )
    return f"""          <ul class="standort-services-list">
{items}
              <li><a href="{page_href("referenzen.html", asset)}" class="card-link">{"Referenzen" if lang == "de" else "References"}</a></li>
          </ul>
          <p class="standort-note"><a href="{page_href("leistungen.html", asset)}" class="card-link">{overview_label}</a></p>"""


MODULE_RENDERERS = {}


def _module(name):
    def decorator(fn):
        MODULE_RENDERERS[name] = fn
        return fn
    return decorator


@_module("hero")
def mod_hero(_city, lang, t, _asset, _slug):
    return f"""    <section class="page-section page-section--hero standort-hero">
      <div class="container">
        <p class="eyebrow">{t["hero_kicker"]}</p>
        <h1>{t["h1"]}</h1>
        <p class="standort-hero-lead">{t["hero_lead"]}</p>
      </div>
    </section>"""


@_module("intro")
def mod_intro(_city, lang, t, _asset, _slug):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <div class="standort-prose">
          <h2>{t["intro_title"]}</h2>
          <p>{t["intro"]}</p>
        </div>
      </div>
    </section>"""


@_module("collaboration")
def mod_collaboration(_city, lang, t, _asset, _slug):
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <div class="standort-prose">
          <h2>{t["collaboration_title"]}</h2>
          <p>{t["collaboration"]}</p>
        </div>
      </div>
    </section>"""


@_module("mandates")
def mod_mandates(_city, lang, t, _asset, _slug):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <h2>{t["mandates_title"]}</h2>
        <ul class="standort-list">
{_list_items(t["mandates"])}
        </ul>
      </div>
    </section>"""


@_module("sectors")
def mod_sectors(_city, lang, t, _asset, _slug):
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <h2>{t["sectors_title"]}</h2>
        <ul class="standort-list">
{_list_items(t["sectors"])}
        </ul>
      </div>
    </section>"""


@_module("references")
def mod_references(_city, lang, t, _asset, _slug):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <h2>{t["references_title"]}</h2>
        <p class="standort-muted">{t["references_intro"]}</p>
        <ul class="standort-refs">
{_ref_items(t["references"])}
        </ul>
        <p class="standort-note"><a href="{page_href("referenzen.html", _asset)}" class="card-link">{"Alle Referenzen" if lang == "de" else "All references"}</a></p>
      </div>
    </section>"""


@_module("formats")
def mod_formats(_city, lang, t, _asset, _slug):
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <h2>{t["formats_title"]}</h2>
        <div class="standort-formats">
{_formats(t["formats"])}
        </div>
      </div>
    </section>"""


@_module("mini_case")
def mod_mini_case(_city, lang, t, _asset, _slug):
    ui = STANDORT_UI[lang]
    title = ui["mini_case_title"]
    disclaimer = ui["mini_case_disclaimer"]
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <h2>{title}</h2>
        <p class="standort-case__disclaimer">{disclaimer}</p>
        <blockquote class="standort-case">{t["mini_case"]}</blockquote>
      </div>
    </section>"""


@_module("logistics")
def mod_logistics(_city, lang, t, _asset, _slug):
    ui = STANDORT_UI[lang]
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <div class="standort-prose">
          <h2>{ui["logistics_title"]}</h2>
          <p>{t["logistics"]}</p>
        </div>
      </div>
    </section>"""


@_module("format_teaser")
def mod_format_teaser(_city, lang, t, asset, _slug):
    ui = STANDORT_UI[lang]
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <article class="card card--lead standort-format-teaser">
          <p class="eyebrow">{ui["format_teaser_kicker"]}</p>
          <h2>{ui["format_teaser_title"]}</h2>
          <p>{ui["format_teaser_text"]}</p>
          <p class="hero-actions">
            <a href="{page_href("coaching-formate.html", asset)}" class="btn btn-secondary">{ui["format_teaser_btn"]}</a>
          </p>
        </article>
      </div>
    </section>"""


@_module("related")
def mod_related(_city, lang, t, asset, slug):
    ui = STANDORT_UI[lang]
    slugs = RELATED_SLUGS.get(slug, [])
    if not slugs:
        return ""
    links = "\n".join(
        f'              <li><a href="{page_href(f"standorte/{s}.html", asset)}" class="card-link">'
        f'{html.escape(CITIES[s][lang]["home_label"])}</a></li>'
        for s in slugs
        if s in CITIES
    )
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <h2>{ui["related_title"]}</h2>
        <ul class="standort-related-list">
{links}
        </ul>
      </div>
    </section>"""


@_module("quote")
def mod_quote(_city, lang, t, _asset, _slug):
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <blockquote class="standort-quote">{t["quote"]}</blockquote>
      </div>
    </section>"""


@_module("nearby")
def mod_nearby(_city, lang, t, _asset, _slug):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <div class="standort-prose">
          <h2>{t["nearby_title"]}</h2>
          <p>{t["nearby"]}</p>
        </div>
      </div>
    </section>"""


@_module("faq")
def mod_faq(_city, lang, t, _asset, _slug):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <h2>{t["faq_title"]}</h2>
        <div class="standort-faq">
{_faq(t["faq"])}
        </div>
      </div>
    </section>"""


@_module("services")
def mod_services(_city, lang, t, _asset, _slug):
    audience = ""
    if t.get("audience_title") and t.get("audience"):
        audience = f"""        <p class="standort-subhead">{t["audience_title"]}</p>
        <p class="standort-muted">{t["audience"]}</p>
"""
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <h2>{t["services_title"]}</h2>
{audience}
{_services(lang, _asset)}
      </div>
    </section>"""


@_module("cta")
def mod_cta(_city, lang, t, _asset, slug):
    city_name = _city["name_de"] if lang == "de" else _city["name_en"]
    wizard_link = wizard_href(_asset, leistung="coaching", stadt=city_name)
    return f"""    <section class="page-section page-section--cta standort-cta">
      <div class="container">
        <article class="card card--lead">
          <h2>{t["cta_title"]}</h2>
          <p>{t["cta_text"]}</p>
          <div class="hero-actions">
            <a href="{wizard_link}" class="btn btn-primary">{t["cta_btn"]}</a>
            <a href="tel:+4954114496" class="btn btn-secondary">{"Anrufen" if lang == "de" else "Call"}</a>
          </div>
        </article>
      </div>
    </section>"""


def build_main(slug: str, lang: str) -> str:
    city = CITIES[slug]
    t = city[lang]
    nav = nav_prefix(f"standorte/{slug}.html")
    parts = []
    for module_name in city["module_order"]:
        renderer = MODULE_RENDERERS[module_name]
        block = renderer(city, lang, t, nav, slug)
        if block:
            parts.append(block)
    return f"""<!-- Standort {city["name_de"]} -->
{chr(10).join(parts)}
"""


def city_list_desc(slug: str, lang: str) -> str:
    if slug in REACH_DESCRIPTIONS:
        return REACH_DESCRIPTIONS[slug][lang]
    label = CITIES[slug][lang]["home_label"]
    if " — " in label:
        return label.split(" — ", 1)[1]
    return label


def render_reach_places(lang: str, asset: str = "") -> str:
    copy = REACH_COPY[lang]
    featured_items = []
    for slug in REACH_FEATURED_SLUGS:
        city = CITIES[slug]
        name = city["name_de"] if lang == "de" else city["name_en"]
        desc = city_list_desc(slug, lang)
        featured_items.append(
            f"""              <li class="reach-places-item" data-slug="{slug}">
                <a href="{page_href(f"standorte/{slug}.html", asset)}" class="reach-places-link">
                  <span class="reach-places-city">{name}</span>
                  <span class="reach-places-desc">{desc}</span>
                </a>
              </li>"""
        )
    map_more = [slug for slug in MAP_SLUGS if slug not in REACH_FEATURED_SLUGS]
    more_slugs = map_more + [slug for slug in ORPHAN_SLUGS if slug in CITIES]
    more_items = "\n".join(
        f'              <li data-slug="{slug}"><a href="{page_href(f"standorte/{slug}.html", asset)}">'
        f'{html.escape(CITIES[slug][lang]["home_label"])}</a></li>'
        for slug in more_slugs
    )
    return f"""            <p class="reach-places-kicker">{copy["places_kicker"]}</p>
            <ul class="reach-places-list">
{chr(10).join(featured_items)}
            </ul>
            <details class="reach-more">
              <summary class="reach-more-summary">{copy["more_summary"]}</summary>
              <ul class="reach-more-list">
{more_items}
              </ul>
            </details>"""


def _standorte_links(slugs: list[str], lang: str, asset: str) -> str:
    return "\n".join(
        f'            <li><a href="{page_href(f"standorte/{slug}.html", asset)}">'
        f'{html.escape(CITIES[slug][lang]["home_label"])}</a></li>'
        for slug in slugs
    )


def render_home_standorte(lang: str, asset: str = "") -> str:
    h = HOME_STANDORTE[lang]
    groups = HOME_GROUPS[lang]
    group_blocks = []
    for label, slugs in groups:
        links = _standorte_links(slugs, lang, asset)
        group_blocks.append(
            f"""          <p class="home-standorte-group-label">{label}</p>
          <ul class="home-standorte-list">
{links}
          </ul>"""
        )
    einsatz_label = "Alle Einsatzgebiete auf der Karte" if lang == "de" else "All service areas on the map"
    return f"""        <details class="home-standorte">
          <summary>{h["summary"]}</summary>
          <p class="home-standorte-intro">{h["intro"]}</p>
{chr(10).join(group_blocks)}
          <p class="home-standorte-more"><a href="{page_href("einsatzgebiete.html", asset)}" class="card-link">{einsatz_label}</a></p>
        </details>"""


def patch_home_standorte(path: Path, lang: str, asset: str = ""):
    page_html = path.read_text(encoding="utf-8")
    block = render_home_standorte(lang, asset=asset)
    if HOME_STANDORTE_MARKER in page_html:
        page_html = page_html.replace(HOME_STANDORTE_MARKER, block)
    else:
        page_html = re.sub(
            r'<details class="home-standorte">.*?</details>\s*',
            block + "\n",
            page_html,
            count=1,
            flags=re.DOTALL,
        )
    path.write_text(page_html, encoding="utf-8")


def localize_map_svg(svg: str, lang: str) -> str:
    if lang == "de":
        return svg
    svg = svg.replace(
        'aria-label="Karte DACH-Raum mit Einsatzorten"',
        'aria-label="Map of the DACH region with selected service locations"',
    ).replace(
        "<title>Einsatzgebiet Doris Gunsch</title>",
        "<title>Service area Doris Gunsch</title>",
    )
    for city in MAP_CITIES + MAP_SUBMAP_CITIES:
        name_de = city["name_de"]
        name_en = city["name_en"]
        if name_de != name_en:
            svg = svg.replace(f">{name_de}</text>", f">{name_en}</text>")
        slug = city.get("slug")
        if slug and city["link"] and slug in REACH_DESCRIPTIONS:
            de_aria = html.escape(f"{name_de} — {REACH_DESCRIPTIONS[slug]['de']}", quote=True)
            en_aria = html.escape(f"{name_en} — {REACH_DESCRIPTIONS[slug]['en']}", quote=True)
            svg = svg.replace(f'aria-label="{de_aria}"', f'aria-label="{en_aria}"')
    return svg


def render_einsatzgebiete_hero(lang: str) -> str:
    c = EINSATZGEBIETE_COPY[lang]
    return f"""        <header class="section-header section-header--wide">
          <p class="eyebrow">{c["eyebrow"]}</p>
          <h1>{c["h1"]}</h1>
          <p class="reach-lead">{c["lead"]}</p>
          <p class="reach-body">{c["body"]}</p>
          <p class="reach-note">{c["note"]}</p>
        </header>"""


def patch_einsatzgebiete_hero(path: Path, lang: str):
    page_html = path.read_text(encoding="utf-8")
    block = render_einsatzgebiete_hero(lang)
    page_html = re.sub(
        r'<header class="section-header section-header--wide">.*?</header>',
        block,
        page_html,
        count=1,
        flags=re.DOTALL,
    )
    path.write_text(page_html, encoding="utf-8")


def render_einsatzgebiete_map(lang: str) -> str:
    svg = (ROOT / "assets" / "map-dach.svg").read_text(encoding="utf-8")
    svg = localize_map_svg(svg, lang)
    indented = "\n".join(
        f"                {line}" if line.strip() else line for line in svg.splitlines()
    )
    return f"""            <div class="map-standalone map-standalone--interactive">
{indented}
            </div>"""


def patch_einsatzgebiete_map(path: Path, lang: str):
    html = path.read_text(encoding="utf-8")
    block = render_einsatzgebiete_map(lang)
    if EINSATZGEBIETE_MAP_MARKER in html:
        html = html.replace(EINSATZGEBIETE_MAP_MARKER, block)
    else:
        html = re.sub(
            r'<div class="reach-layout__map">.*?</div>\s*(?=<aside class="reach-layout__places")',
            f'<div class="reach-layout__map">\n{block}\n          </div>\n          ',
            html,
            count=1,
            flags=re.DOTALL,
        )
    path.write_text(html, encoding="utf-8")


def patch_einsatzgebiete_places(path: Path, lang: str, asset: str = ""):
    page_html = path.read_text(encoding="utf-8")
    block = render_reach_places(lang, asset=asset)
    places_aria = html.escape(EINSATZGEBIETE_COPY[lang]["places_aria"])
    aside_block = (
        f'          <aside class="reach-layout__places" aria-label="{places_aria}">\n'
        f"{block}\n"
        f"          </aside>\n"
    )
    if EINSATZGEBIETE_PLACES_MARKER in page_html:
        page_html = page_html.replace(EINSATZGEBIETE_PLACES_MARKER, aside_block)
    else:
        page_html = re.sub(
            r'<aside class="reach-layout__places"[^>]*>.*?(?:</aside>\s*)+',
            aside_block,
            page_html,
            count=1,
            flags=re.DOTALL,
        )
    path.write_text(page_html, encoding="utf-8")


def main():
    from build_map_dach import main as build_map_dach

    build_map_dach()

    standorte_dir = ROOT / "standorte"
    en_standorte_dir = ROOT / "en" / "standorte"
    standorte_dir.mkdir(exist_ok=True)
    en_standorte_dir.mkdir(exist_ok=True)

    for slug in CITY_SLUGS:
        filename = f"standorte/{slug}.html"
        for lang, out_dir in (("de", standorte_dir), ("en", en_standorte_dir)):
            main_html = build_main(slug, lang)
            build_page(lang, filename, main_html, out_dir / f"{slug}.html")

    patch_einsatzgebiete_hero(ROOT / "einsatzgebiete.html", "de")
    patch_einsatzgebiete_hero(ROOT / "en" / "einsatzgebiete.html", "en")
    patch_einsatzgebiete_map(ROOT / "einsatzgebiete.html", "de")
    patch_einsatzgebiete_map(ROOT / "en" / "einsatzgebiete.html", "en")
    patch_einsatzgebiete_places(ROOT / "einsatzgebiete.html", "de")
    # EN standorte live under en/standorte/ — same depth as en/einsatzgebiete.html
    patch_einsatzgebiete_places(ROOT / "en" / "einsatzgebiete.html", "en")
    patch_home_standorte(ROOT / "index.html", "de")
    patch_home_standorte(ROOT / "en" / "index.html", "en")
    print("Built", len(CITY_SLUGS), "standorte pages (DE + EN), einsatzgebiete and home standorte")


if __name__ == "__main__":
    main()
