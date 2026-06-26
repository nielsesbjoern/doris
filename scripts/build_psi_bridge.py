#!/usr/bin/env python3
"""Inject PSI / scientific-depth bridge modules into key pages (DE + EN)."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from psi_bridge_data import TEXT  # noqa: E402
from seo import page_href  # noqa: E402
from wrap_pages import build_page, extract_main  # noqa: E402

MARKERS = {
    "home": ("<!-- PSI_HOME_BRIDGE -->", "<!-- /PSI_HOME_BRIDGE -->"),
    "home_hero": ("<!-- HOME_HERO_LEAD -->", "<!-- /HOME_HERO_LEAD -->"),
    "home_services": ("<!-- HOME_SERVICES_HEAD -->", "<!-- /HOME_SERVICES_HEAD -->"),
    "home_person": ("<!-- HOME_PERSON_TEXT -->", "<!-- /HOME_PERSON_TEXT -->"),
    "leistungen": ("<!-- PSI_LEISTUNGEN_BRIDGE -->", "<!-- /PSI_LEISTUNGEN_BRIDGE -->"),
    "coaching": ("<!-- PSI_COACHING_FOUNDATION -->", "<!-- /PSI_COACHING_FOUNDATION -->"),
    "diag_top": ("<!-- PSI_DIAGNOSTIK_TOP -->", "<!-- /PSI_DIAGNOSTIK_TOP -->"),
    "diag_depth": ("<!-- PSI_DIAGNOSTIK_DEPTH -->", "<!-- /PSI_DIAGNOSTIK_DEPTH -->"),
}


def inject_block(main: str, key: str, block: str, *, required: bool = True) -> str:
    start, end = MARKERS[key]
    if start not in main:
        if required:
            raise SystemExit(f"Missing {start} … {end} in page main content")
        return main
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{block}\n          {end}"
    return pattern.sub(replacement, main, count=1)


def render_home_bridge(lang: str, asset: str = "") -> str:
    t = TEXT[lang]
    return f"""        <p class="home-science-note">
          <strong>{html.escape(t["home_title"])}.</strong> {t["home_lead"]}
          <a href="{page_href("diagnostik.html", asset)}" class="card-link">{t["home_link_diagnostik"]}</a>
        </p>"""


def render_home_hero(lang: str) -> str:
    return f"""          <p class="hero-lead">
            {TEXT[lang]["hero_lead"]}
          </p>"""


UNI_OSNABRUECK_URL = "https://www.uni-osnabrueck.de/"


def _uni_link(lang: str) -> str:
    label = "Universität Osnabrück" if lang == "de" else "University of Osnabrück"
    return (
        f'<a href="{UNI_OSNABRUECK_URL}" class="text-link" rel="noopener noreferrer">'
        f"{html.escape(label)}</a>"
    )


def render_home_services_head(lang: str) -> str:
    t = TEXT[lang]
    intro = t["home_services_intro"].format(uni_link=_uni_link(lang))
    return f"""        <header class="home-services-header">
          <h2 class="home-services-title">{t["home_services_title"]}</h2>
          <p class="home-services-intro">{intro}</p>
        </header>"""


def render_home_person(lang: str) -> str:
    return f"""            <p class="home-person-text">
              {TEXT[lang]["person_text"]}
            </p>"""


def render_leistungen_bridge(lang: str, asset: str = "") -> str:
    t = TEXT[lang]
    return f"""        <aside class="science-bridge science-bridge--compact" aria-label="{html.escape(t["leistungen_title"])}">
          <h2 class="science-bridge__title">{t["leistungen_title"]}</h2>
          <p class="science-bridge__lead">{t["leistungen_lead"]}</p>
          <p class="science-bridge__trust">{t["leistungen_trust"]}</p>
          <p class="science-bridge__links">
            <a href="{page_href("diagnostik.html", asset)}" class="card-link">{t["leistungen_link"]}</a>
          </p>
        </aside>"""


def render_coaching_foundation(lang: str, asset: str = "") -> str:
    t = TEXT[lang]
    items = "\n".join(
        f"""              <li class="coaching-foundation__item">
                <strong>{html.escape(title)}</strong>
                <span>{html.escape(body)}</span>
              </li>"""
        for title, body in t["coaching_points"]
    )
    return f"""          <section class="coaching-foundation" aria-label="{html.escape(t["coaching_title"])}">
            <h2 class="coaching-foundation__title">{t["coaching_title"]}</h2>
            <ul class="coaching-foundation__list">
{items}
            </ul>
            <p class="coaching-foundation__links">
              <a href="{page_href("diagnostik.html", asset)}" class="card-link">{t["coaching_link_diagnostik"]}</a>
              <a href="{page_href("person.html", asset)}" class="card-link">{t["coaching_link_person"]}</a>
            </p>
          </section>"""


def render_diagnostik_top(lang: str, asset: str = "") -> str:
    t = TEXT[lang]
    cases = "\n".join(
        f"              <li>{html.escape(item)}</li>" for item in t["diag_use_cases"]
    )
    benefits = "\n".join(
        f"              <li>{html.escape(item)}</li>" for item in t["psi_benefits"]
    )
    return f"""          <p class="leistung-lead">
            {t["diag_lead"]}
          </p>
          <div class="science-use-cases">
            <p class="science-use-cases__label">{"Typische Anlässe" if lang == "de" else "Typical situations"}</p>
            <ul class="science-use-cases__list">
{cases}
            </ul>
          </div>
          <details class="science-detail profile-fact" id="psi-theorie">
            <summary class="profile-fact-title">
              <span class="profile-fact-name">{t["psi_summary"]}</span>
            </summary>
            <div class="science-detail__body prose">
              <p>{t["psi_intro"]}</p>
              <ul class="detail-list">
{benefits}
              </ul>
              <p>{t["psi_note"]}</p>
            </div>
          </details>"""


def wrap_diagnostik_depth(main: str, lang: str) -> str:
    t = TEXT[lang]
    start, end = MARKERS["diag_depth"]
    pattern = re.compile(re.escape(start) + r"(.*?)" + re.escape(end), re.DOTALL)

    def replacer(match: re.Match[str]) -> str:
        inner = match.group(1).strip("\n")
        return (
            f"{start}\n"
            f'          <details class="science-detail profile-fact">\n'
            f'            <summary class="profile-fact-title">\n'
            f'              <span class="profile-fact-name">{t["depth_summary"]}</span>\n'
            f"            </summary>\n"
            f'            <div class="science-detail__body prose">\n'
            f"{inner}\n"
            f"            </div>\n"
            f"          </details>\n"
            f"          {end}"
        )

    if not pattern.search(main):
        raise SystemExit(f"Missing {start} … {end} in diagnostik main content")
    return pattern.sub(replacer, main, count=1)


def patch_profile_alt(main: str, lang: str) -> str:
    alt = html.escape(TEXT[lang]["profile_image_alt"], quote=True)
    return re.sub(
        r'(<img src="(?:\.\./)?public/doris-web-600\.jpg" alt=")[^"]*(")',
        rf"\1{alt}\2",
        main,
        count=1,
    )


def patch_main(
    main: str,
    lang: str,
    asset: str = "",
    *,
    home: bool = False,
    leistungen: bool = False,
    coaching: bool = False,
    diagnostik: bool = False,
) -> str:
    if home:
        main = inject_block(main, "home_hero", render_home_hero(lang))
        main = inject_block(main, "home_services", render_home_services_head(lang))
        main = inject_block(main, "home", render_home_bridge(lang, asset))
        main = inject_block(main, "home_person", render_home_person(lang))
        main = patch_profile_alt(main, lang)
    if leistungen:
        main = inject_block(main, "leistungen", render_leistungen_bridge(lang, asset))
    if coaching:
        main = inject_block(main, "coaching", render_coaching_foundation(lang, asset))
    if diagnostik:
        main = inject_block(main, "diag_top", render_diagnostik_top(lang, asset))
        main = wrap_diagnostik_depth(main, lang)
    return main


def process_page(path: Path, lang: str, filename: str, asset: str = "", **flags: bool) -> None:
    raw = path.read_text(encoding="utf-8")
    main = extract_main(raw)
    if not main:
        raise SystemExit(f"Could not extract <main> from {path}")
    main = patch_main(main, lang, asset, **flags)
    build_page(lang, filename, main, path)


def main() -> None:
    process_page(ROOT / "index.html", "de", "index.html", home=True)
    process_page(ROOT / "en" / "index.html", "en", "index.html", asset="../", home=True)
    process_page(ROOT / "leistungen.html", "de", "leistungen.html", leistungen=True)
    process_page(
        ROOT / "en" / "leistungen.html",
        "en",
        "leistungen.html",
        asset="../",
        leistungen=True,
    )
    process_page(
        ROOT / "coaching.html",
        "de",
        "coaching.html",
        coaching=True,
    )
    process_page(
        ROOT / "en" / "coaching.html",
        "en",
        "coaching.html",
        asset="../",
        coaching=True,
    )
    process_page(
        ROOT / "diagnostik.html",
        "de",
        "diagnostik.html",
        diagnostik=True,
    )
    process_page(
        ROOT / "en" / "diagnostik.html",
        "en",
        "diagnostik.html",
        asset="../",
        diagnostik=True,
    )
    print("Built PSI bridge modules (DE + EN) on index, leistungen, coaching, diagnostik")


if __name__ == "__main__":
    main()
