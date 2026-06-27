#!/usr/bin/env python3
"""Build coaching format finder page and teaser on coaching overview (DE + EN)."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from coaching_formats_data import FORMATS, TEXT  # noqa: E402
from seo import page_href, page_link_prefix  # noqa: E402
from wrap_pages import build_page, extract_main, strip_wrapped_artifacts  # noqa: E402

COMPARE_START = "<!-- FORMAT_COMPARE -->"
COMPARE_END = "<!-- /FORMAT_COMPARE -->"
TEASER_START = "<!-- FORMAT_TEASER -->"
TEASER_END = "<!-- /FORMAT_TEASER -->"
HOME_HIGHLIGHT_START = "<!-- HOME_FORMAT_HIGHLIGHT -->"
HOME_HIGHLIGHT_END = "<!-- /HOME_FORMAT_HIGHLIGHT -->"
HOME_HERO_ACTIONS_START = "<!-- HOME_HERO_ACTIONS -->"
HOME_HERO_ACTIONS_END = "<!-- /HOME_HERO_ACTIONS -->"
HOME_HERO_HINT_START = "<!-- HOME_HERO_HINT -->"
HOME_HERO_HINT_END = "<!-- /HOME_HERO_HINT -->"
HOME_COACHING_CARD_START = "<!-- HOME_COACHING_CARD_FOOTER -->"
HOME_COACHING_CARD_END = "<!-- /HOME_COACHING_CARD_FOOTER -->"


def field(fmt: dict, key: str, lang: str) -> str:
    return fmt[f"{key}_{lang}"]


def render_item(fmt: dict, lang: str, t: dict) -> str:
    title = html.escape(field(fmt, "title", lang))
    duration = html.escape(field(fmt, "duration", lang))
    occasion = html.escape(field(fmt, "occasion", lang))
    outcome = html.escape(field(fmt, "outcome", lang))
    suitable = html.escape(field(fmt, "suitable", lang))
    less_suitable = html.escape(field(fmt, "less_suitable", lang))
    hidden = ' hidden' if fmt["group"] != "anlass" else ""

    return f"""            <details class="format-guide__item" id="format-{fmt["id"]}" data-format="{fmt["id"]}" data-group="{fmt["group"]}"{hidden}>
              <summary class="format-guide__summary">
                <label class="format-guide__pick" data-format-pick>
                  <input type="checkbox" class="format-guide__pick-input" value="{fmt["id"]}" aria-label="{t["compare_pick"]}: {title}">
                </label>
                <span class="format-guide__name">{title}</span>
                <span class="format-guide__teaser">{duration}</span>
                <span class="format-guide__teaser format-guide__teaser--wide">{occasion}</span>
                <span class="format-guide__toggle" aria-hidden="true">{t["details_show"]}</span>
              </summary>
              <div class="format-guide__body">
                <dl class="format-guide__meta">
                  <div class="format-guide__row" data-row-key="{html.escape(t["label_duration"])}">
                    <dt>{t["label_duration"]}</dt>
                    <dd>{duration}</dd>
                  </div>
                  <div class="format-guide__row" data-row-key="{html.escape(t["label_occasion"])}">
                    <dt>{t["label_occasion"]}</dt>
                    <dd>{occasion}</dd>
                  </div>
                  <div class="format-guide__row" data-row-key="{html.escape(t["label_outcome"])}">
                    <dt>{t["label_outcome"]}</dt>
                    <dd>{outcome}</dd>
                  </div>
                  <div class="format-guide__row" data-row-key="{html.escape(t["label_suitable"])}">
                    <dt>{t["label_suitable"]}</dt>
                    <dd>{suitable}</dd>
                  </div>
                  <div class="format-guide__row" data-row-key="{html.escape(t["label_less_suitable"])}">
                    <dt>{t["label_less_suitable"]}</dt>
                    <dd>{less_suitable}</dd>
                  </div>
                </dl>
              </div>
            </details>"""


def render_compare(lang: str) -> str:
    t = TEXT[lang]
    items = "\n".join(render_item(fmt, lang, t) for fmt in FORMATS)
    row_labels = [
        t["label_duration"],
        t["label_occasion"],
        t["label_outcome"],
        t["label_suitable"],
        t["label_less_suitable"],
    ]
    thead_cells = "".join(
        '\n                <th scope="col" class="format-guide__compare-slot"></th>' for _ in range(2)
    )
    tbody_rows = "".join(
        f'                    <tr data-row-label="{html.escape(label)}"><th scope="row">{label}</th>'
        f'<td class="format-guide__compare-slot"></td><td class="format-guide__compare-slot"></td></tr>\n'
        for label in row_labels
    )

    return f"""          <div class="detail-block format-guide" id="formate-vergleich">
            <h2 class="visually-hidden">{t["title"]}</h2>
            <p class="detail-intro">
              {t["intro"]}
            </p>

            <div class="format-guide__modes" role="tablist" aria-label="{t["title"]}">
              <button type="button" class="format-guide__mode is-active" role="tab" data-group="anlass" aria-selected="true" id="format-tab-anlass" aria-controls="format-panel">
                <span class="format-guide__mode-title">{t["group_anlass"]}</span>
                <span class="format-guide__mode-desc">{t["group_anlass_desc"]}</span>
              </button>
              <button type="button" class="format-guide__mode" role="tab" data-group="durchfuehrung" aria-selected="false" id="format-tab-durchfuehrung" aria-controls="format-panel">
                <span class="format-guide__mode-title">{t["group_durchfuehrung"]}</span>
                <span class="format-guide__mode-desc">{t["group_durchfuehrung_desc"]}</span>
              </button>
            </div>

            <p class="format-guide__hint">{t["compare_hint"]}</p>
            <p class="format-guide__status" id="format-guide-status" aria-live="polite" aria-atomic="true"></p>

            <div class="format-guide__inquiry" id="format-guide-inquiry" hidden>
              <p class="format-guide__inquiry-text" id="format-guide-inquiry-text"></p>
              <button type="button" class="btn btn-primary format-guide__inquiry-btn" id="format-guide-inquiry-btn">{t["inquiry_one"]}</button>
            </div>

            <div class="format-guide__compare" id="format-guide-compare" hidden>
              <div class="format-guide__compare-head">
                <h3 class="format-guide__compare-title">{t["compare_panel_title"]}</h3>
                <button type="button" class="format-guide__compare-clear" id="format-guide-clear">{t["compare_clear"]}</button>
              </div>
              <div class="format-guide__compare-scroll">
                <table class="format-guide__table format-guide__table--compare">
                  <thead>
                    <tr>{thead_cells}
                    </tr>
                  </thead>
                  <tbody>
{tbody_rows}                  </tbody>
                </table>
              </div>
            </div>

            <div class="format-guide__overview" id="format-panel" role="tabpanel" aria-labelledby="format-tab-anlass">
              <div class="format-guide__head" aria-hidden="true">
                <span class="format-guide__head-pick"></span>
                <span class="format-guide__head-name">{t["col_format"]}</span>
                <span class="format-guide__head-duration">{t["col_duration"]}</span>
                <span class="format-guide__head-occasion">{t["col_occasion"]}</span>
                <span class="format-guide__head-action">{t["col_details"]}</span>
              </div>
              <div class="format-guide__list">
{items}
              </div>
            </div>

            <p class="format-guide__note">{t["note"]}</p>
          </div>"""


def render_teaser(lang: str, link_prefix: str) -> str:
    t = TEXT[lang]
    href = page_href("coaching-formate.html", link_prefix)
    return f"""          <aside class="format-teaser card card--lead" aria-label="{html.escape(t["teaser_title"], quote=True)}">
            <p class="format-teaser__kicker">{t["teaser_kicker"]}</p>
            <h3 class="format-teaser__title">{t["teaser_title"]}</h3>
            <p class="format-teaser__text">{t["teaser_text"]}</p>
            <a href="{href}" class="btn btn-primary">{t["teaser_btn"]}</a>
          </aside>"""


def render_home_highlight(lang: str, link_prefix: str) -> str:
    t = TEXT[lang]
    href = page_href("coaching-formate.html", link_prefix)
    return f"""    <section class="section page-section home-format-highlight" aria-labelledby="home-format-highlight-title">
      <div class="container">
        <div class="home-format-highlight__inner">
          <div class="home-format-highlight__copy">
            <p class="home-format-highlight__kicker">{t["home_kicker"]}</p>
            <h2 id="home-format-highlight-title" class="home-format-highlight__title">{t["home_title"]}</h2>
          </div>
          <div class="home-format-highlight__actions">
            <a href="{href}" class="btn btn-format-finder btn-lg">{t["home_btn"]}</a>
            <a href="{page_href("coaching.html", link_prefix)}" class="btn-text">{t["home_coaching_link"]}</a>
          </div>
        </div>
      </div>
    </section>"""


def render_home_hero_actions(lang: str, link_prefix: str) -> str:
    t = TEXT[lang]
    fmt_href = page_href("coaching-formate.html", link_prefix)
    leist_href = page_href("leistungen.html", link_prefix)
    contact_href = page_href("kontakt.html", link_prefix) + "#kontakt-anfrage"
    contact_label = "Kontakt aufnehmen" if lang == "de" else "Get in touch"
    services_label = "Leistungen ansehen" if lang == "de" else "View services"
    return f"""          <div class="hero-actions">
            <a href="{contact_href}" class="btn btn-primary">{contact_label}</a>
            <a href="{fmt_href}" class="btn btn-format-finder">{t["hero_btn"]}</a>
            <a href="{leist_href}" class="btn-text">{services_label}</a>
          </div>"""


def render_home_hero_hint(lang: str, link_prefix: str) -> str:
    t = TEXT[lang]
    href = page_href("coaching-formate.html", link_prefix)
    return f"""          <p class="hero-format-hint">{t["hero_hint"]} <a href="{href}" class="hero-format-hint__link">{t["hero_hint_link"]}</a></p>"""


def render_home_coaching_card_footer(lang: str, link_prefix: str) -> str:
    t = TEXT[lang]
    coaching_href = page_href("coaching.html", link_prefix)
    fmt_href = page_href("coaching-formate.html", link_prefix)
    more = "Mehr zum Coaching" if lang == "de" else "More on coaching"
    return f"""            <a href="{coaching_href}" class="card-link">{more}</a>
            <a href="{fmt_href}" class="card-link card-link--format">{t["home_coaching_card_link"]}</a>"""


def inject_block(main: str, start: str, end: str, block: str, *, required: bool = True) -> str:
    if start not in main:
        if required:
            raise SystemExit(f"Missing {start} … {end}")
        return main
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{block}\n          {end}"
    return pattern.sub(replacement, main, count=1)


def patch_main(path: Path, lang: str, filename: str) -> str:
    raw = path.read_text(encoding="utf-8")
    main = strip_wrapped_artifacts(extract_main(raw))
    if not main:
        raise SystemExit(f"Could not extract <main> from {path}")

    link_prefix = page_link_prefix(filename)
    name = path.name
    if name == "coaching-formate.html":
        main = inject_block(main, COMPARE_START, COMPARE_END, render_compare(lang))
    elif name == "coaching.html":
        if COMPARE_START in main:
            main = inject_block(main, COMPARE_START, COMPARE_END, render_teaser(lang, link_prefix))
        else:
            main = inject_block(
                main, TEASER_START, TEASER_END, render_teaser(lang, link_prefix), required=False
            )
            if TEASER_START not in main:
                raise SystemExit(f"Missing format teaser markers in {path}")
    elif name == "index.html":
        main = inject_block(
            main,
            HOME_HERO_ACTIONS_START,
            HOME_HERO_ACTIONS_END,
            render_home_hero_actions(lang, link_prefix),
        )
        main = inject_block(
            main,
            HOME_COACHING_CARD_START,
            HOME_COACHING_CARD_END,
            render_home_coaching_card_footer(lang, link_prefix),
        )
        main = re.sub(
            re.escape(HOME_HERO_HINT_START) + r".*?" + re.escape(HOME_HERO_HINT_END) + r"\s*",
            "",
            main,
            count=1,
            flags=re.DOTALL,
        )
        main = re.sub(
            re.escape(HOME_HIGHLIGHT_START) + r".*?" + re.escape(HOME_HIGHLIGHT_END) + r"\s*",
            "",
            main,
            count=1,
            flags=re.DOTALL,
        )
    else:
        raise SystemExit(f"Unexpected file for build_coaching: {path}")
    return main


def main() -> None:
    jobs = (
        ("de", "coaching-formate.html", ROOT / "coaching-formate.html"),
        ("en", "coaching-formate.html", ROOT / "en" / "coaching-formate.html"),
        ("de", "coaching.html", ROOT / "coaching.html"),
        ("en", "coaching.html", ROOT / "en" / "coaching.html"),
        ("de", "index.html", ROOT / "index.html"),
        ("en", "index.html", ROOT / "en" / "index.html"),
    )
    for lang, filename, path in jobs:
        if not path.exists():
            raise SystemExit(f"Missing {path}")
        main = patch_main(path, lang, filename)
        build_page(lang, filename, main, path)
    print("Built coaching format finder page, teasers and home highlight (DE + EN)")


if __name__ == "__main__":
    main()
