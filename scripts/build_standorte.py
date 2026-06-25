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
    HOME_STANDORTE,
    METRO_SLUGS,
    REACH_COPY,
    REACH_DESCRIPTIONS,
    REACH_FEATURED_SLUGS,
    REGION_SLUGS,
    SERVICE_LINKS,
    STANDORTE_META,
)
from wrap_pages import META, build_page, nav_prefix

HOME_STANDORTE_MARKER = "<!-- HOME_STANDORTE -->"
HOME_REACH_PLACES_MARKER = "<!-- HOME_REACH_PLACES -->"
HOME_MAP_MARKER = "<!-- HOME_MAP -->"


def _list_items(items: list[str]) -> str:
    return "\n".join(f"              <li>{item}</li>" for item in items)


def _formats(items: list[tuple[str, str]]) -> str:
    blocks = []
    for title, text in items:
        blocks.append(
            f"""            <div class="standort-format">
              <h3 class="standort-format__title">{title}</h3>
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
        f'              <li><a href="{asset}{href}" class="card-link">{label}</a></li>'
        for href, label in links
    )
    overview_label = (
        "Ausführliche Leistungsbeschreibungen →"
        if lang == "de"
        else "Detailed service descriptions →"
    )
    return f"""          <ul class="standort-services-list">
{items}
              <li><a href="{asset}referenzen.html" class="card-link">{"Referenzen" if lang == "de" else "References"}</a></li>
          </ul>
          <p class="standort-note"><a href="{asset}leistungen.html" class="card-link">{overview_label}</a></p>"""


MODULE_RENDERERS = {}


def _module(name):
    def decorator(fn):
        MODULE_RENDERERS[name] = fn
        return fn
    return decorator


@_module("hero")
def mod_hero(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--hero standort-hero">
      <div class="container">
        <p class="eyebrow">{t["hero_kicker"]}</p>
        <h1>{t["h1"]}</h1>
        <p class="standort-hero-lead">{t["hero_lead"]}</p>
      </div>
    </section>"""


@_module("intro")
def mod_intro(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <div class="standort-prose">
          <h2>{t["intro_title"]}</h2>
          <p>{t["intro"]}</p>
        </div>
      </div>
    </section>"""


@_module("collaboration")
def mod_collaboration(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <div class="standort-prose">
          <h2>{t["collaboration_title"]}</h2>
          <p>{t["collaboration"]}</p>
        </div>
      </div>
    </section>"""


@_module("mandates")
def mod_mandates(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <h2>{t["mandates_title"]}</h2>
        <ul class="standort-list">
{_list_items(t["mandates"])}
        </ul>
      </div>
    </section>"""


@_module("sectors")
def mod_sectors(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <h2>{t["sectors_title"]}</h2>
        <ul class="standort-list">
{_list_items(t["sectors"])}
        </ul>
      </div>
    </section>"""


@_module("references")
def mod_references(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <h2>{t["references_title"]}</h2>
        <p class="standort-muted">{t["references_intro"]}</p>
        <ul class="standort-refs">
{_list_items(t["references"])}
        </ul>
        <p class="standort-note"><a href="{_asset}referenzen.html" class="card-link">{"Alle Referenzen →" if lang == "de" else "All references →"}</a></p>
      </div>
    </section>"""


@_module("formats")
def mod_formats(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <h2>{t["formats_title"]}</h2>
        <div class="standort-formats">
{_formats(t["formats"])}
        </div>
      </div>
    </section>"""


@_module("mini_case")
def mod_mini_case(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <h2>{t["mini_case_title"]}</h2>
        <blockquote class="standort-case">{t["mini_case"]}</blockquote>
      </div>
    </section>"""


@_module("quote")
def mod_quote(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--compact standort-block standort-block--alt">
      <div class="container">
        <blockquote class="standort-quote">{t["quote"]}</blockquote>
      </div>
    </section>"""


@_module("nearby")
def mod_nearby(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <div class="standort-prose">
          <h2>{t["nearby_title"]}</h2>
          <p>{t["nearby"]}</p>
        </div>
      </div>
    </section>"""


@_module("faq")
def mod_faq(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--compact standort-block">
      <div class="container">
        <h2>{t["faq_title"]}</h2>
        <div class="standort-faq">
{_faq(t["faq"])}
        </div>
      </div>
    </section>"""


@_module("services")
def mod_services(_city, lang, t, _asset):
    audience = ""
    if t.get("audience_title") and t.get("audience"):
        audience = f"""        <h3 class="standort-subhead">{t["audience_title"]}</h3>
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
def mod_cta(_city, lang, t, _asset):
    return f"""    <section class="page-section page-section--cta standort-cta">
      <div class="container">
        <article class="card card--lead">
          <h2>{t["cta_title"]}</h2>
          <p>{t["cta_text"]}</p>
          <div class="hero-actions">
            <a href="{_asset}kontakt.html" class="btn btn-primary">{t["cta_btn"]}</a>
            <a href="tel:+4954114496" class="btn btn-secondary">{"+49 (0)541 14496" if lang == "de" else "Call"}</a>
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
        parts.append(renderer(city, lang, t, nav))
    return f"""<!-- Standort {city["name_de"]} -->
{chr(10).join(parts)}
"""


def render_reach_places(lang: str, asset: str = "") -> str:
    copy = REACH_COPY[lang]
    featured_items = []
    for slug in REACH_FEATURED_SLUGS:
        city = CITIES[slug]
        name = city["name_de"] if lang == "de" else city["name_en"]
        desc = REACH_DESCRIPTIONS[slug][lang]
        featured_items.append(
            f"""              <li class="reach-places-item">
                <a href="{asset}standorte/{slug}.html" class="reach-places-link">
                  <span class="reach-places-city">{name}</span>
                  <span class="reach-places-desc">{desc}</span>
                </a>
              </li>"""
        )
    more_slugs = [slug for slug in CITY_SLUGS if slug not in REACH_FEATURED_SLUGS]
    more_items = "\n".join(
        f'              <li><a href="{asset}standorte/{slug}.html">'
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
        f'            <li><a href="{asset}standorte/{slug}.html">'
        f'{html.escape(CITIES[slug][lang]["home_label"])}</a></li>'
        for slug in slugs
    )


def render_home_standorte(lang: str, asset: str = "") -> str:
    h = HOME_STANDORTE[lang]
    region_links = _standorte_links(REGION_SLUGS, lang, asset)
    metro_links = _standorte_links(METRO_SLUGS, lang, asset)
    return f"""        <details class="home-standorte">
          <summary>{h["summary"]}</summary>
          <p class="home-standorte-intro">{h["intro"]}</p>
          <p class="home-standorte-group-label">{h["region_label"]}</p>
          <ul class="home-standorte-list">
{region_links}
          </ul>
          <p class="home-standorte-group-label">{h["metro_label"]}</p>
          <ul class="home-standorte-list">
{metro_links}
          </ul>
        </details>"""


def render_home_map(lang: str) -> str:
    svg = (ROOT / "assets" / "map-dach.svg").read_text(encoding="utf-8")
    if lang == "en":
        svg = svg.replace(
            'aria-label="Karte DACH-Raum mit Einsatzorten"',
            'aria-label="Map of Germany with selected service locations"',
        ).replace(
            "<title>Einsatzgebiet Doris Gunsch</title>",
            "<title>Service area Doris Gunsch</title>",
        )
    indented = "\n".join(
        f"                {line}" if line.strip() else line for line in svg.splitlines()
    )
    return f"""            <div class="map-card">
              <div class="map-card-visual">
{indented}
              </div>
            </div>"""


def patch_home_map(path: Path, lang: str):
    html = path.read_text(encoding="utf-8")
    block = render_home_map(lang)
    if HOME_MAP_MARKER in html:
        html = html.replace(HOME_MAP_MARKER, block)
    else:
        html = re.sub(
            r'<div class="reach-layout__map">.*?</div>\s*(?=<aside class="reach-places-panel")',
            f'<div class="reach-layout__map">\n{block}\n          </div>\n          ',
            html,
            count=1,
            flags=re.DOTALL,
        )
    path.write_text(html, encoding="utf-8")


def patch_home_reach(path: Path, lang: str):
    html = path.read_text(encoding="utf-8")
    block = render_reach_places(lang, asset="")
    if HOME_REACH_PLACES_MARKER in html:
        html = html.replace(HOME_REACH_PLACES_MARKER, block)
    else:
        html = re.sub(
            r'<p class="reach-places-kicker">.*?</details>\s*</aside>',
            block + "\n        </aside>",
            html,
            count=1,
            flags=re.DOTALL,
        )
    path.write_text(html, encoding="utf-8")


def patch_home(path: Path, lang: str):
    html = path.read_text(encoding="utf-8")
    block = render_home_standorte(lang, asset="")
    if HOME_STANDORTE_MARKER in html:
        html = html.replace(HOME_STANDORTE_MARKER, block)
    elif '<details class="home-standorte">' in html:
        html = re.sub(
            r'<details class="home-standorte">.*?</details>',
            block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        html = re.sub(
            r"(</article>\s*)(</div>\s*</section>\s*</main>)",
            rf"\1\n{block}\n      \2",
            html,
            count=1,
            flags=re.DOTALL,
        )
    path.write_text(html, encoding="utf-8")


def main():
    standorte_dir = ROOT / "standorte"
    en_standorte_dir = ROOT / "en" / "standorte"
    standorte_dir.mkdir(exist_ok=True)
    en_standorte_dir.mkdir(exist_ok=True)

    for slug in CITY_SLUGS:
        filename = f"standorte/{slug}.html"
        for lang, out_dir in (("de", standorte_dir), ("en", en_standorte_dir)):
            main_html = build_main(slug, lang)
            build_page(lang, filename, main_html, out_dir / f"{slug}.html")

    patch_home(ROOT / "index.html", "de")
    patch_home(ROOT / "en" / "index.html", "en")
    patch_home_map(ROOT / "index.html", "de")
    patch_home_map(ROOT / "en" / "index.html", "en")
    patch_home_reach(ROOT / "index.html", "de")
    patch_home_reach(ROOT / "en" / "index.html", "en")
    print("Built", len(CITY_SLUGS), "standorte pages (DE + EN) and patched index")


if __name__ == "__main__":
    main()
