#!/usr/bin/env python3
"""Inject coaching format comparison into coaching pages (DE + EN)."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from coaching_formats_data import FORMATS, TEXT  # noqa: E402
from wrap_pages import build_page, extract_main, strip_wrapped_artifacts  # noqa: E402

MARKER_START = "<!-- FORMAT_COMPARE -->"
MARKER_END = "<!-- /FORMAT_COMPARE -->"


def field(fmt: dict, key: str, lang: str) -> str:
    return fmt[f"{key}_{lang}"]


def render_card(fmt: dict, lang: str, t: dict) -> str:
    title = html.escape(field(fmt, "title", lang))
    badge = t["badge_anlass"] if fmt["group"] == "anlass" else t["badge_durchfuehrung"]
    rows = [
        ("duration", t["label_duration"]),
        ("occasion", t["label_occasion"]),
        ("outcome", t["label_outcome"]),
        ("suitable", t["label_suitable"]),
        ("less_suitable", t["label_less_suitable"]),
    ]
    dl_rows = []
    for key, label in rows:
        value = html.escape(field(fmt, key, lang))
        dl_rows.append(
            f"""              <div class="format-compare__row">
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>"""
        )
    return f"""            <article class="format-compare__card" id="format-{fmt["id"]}" data-format="{fmt["id"]}" data-group="{fmt["group"]}">
              <header class="format-compare__card-head">
                <span class="format-compare__badge">{badge}</span>
                <h4>{title}</h4>
              </header>
              <dl class="format-compare__meta">
{chr(10).join(dl_rows)}
              </dl>
            </article>"""


def render_compare(lang: str) -> str:
    t = TEXT[lang]
    group_anlass = t["group_anlass"]
    group_durchfuehrung = t["group_durchfuehrung"]

    chips_anlass = []
    chips_anlass.append(
        f"""          <button type="button" class="format-compare__chip is-active" data-format="all" data-group="anlass" aria-pressed="true">
            {t["filter_all"]}
          </button>"""
    )
    chips_durchfuehrung = [
        f"""          <button type="button" class="format-compare__chip is-active" data-format="all" data-group="durchfuehrung" aria-pressed="true">
            {t["filter_all"]}
          </button>"""
    ]
    for fmt in FORMATS:
        title = html.escape(field(fmt, "title", lang))
        chip = f"""          <button type="button" class="format-compare__chip" data-format="{fmt["id"]}" data-group="{fmt["group"]}" aria-pressed="false">
            {title}
          </button>"""
        if fmt["group"] == "anlass":
            chips_anlass.append(chip)
        else:
            chips_durchfuehrung.append(chip)

    cards = "\n".join(render_card(fmt, lang, t) for fmt in FORMATS)

    return f"""          <div class="detail-block format-compare" id="formate-vergleich">
            <h3 class="detail-subtitle">{t["title"]}</h3>
            <p class="detail-intro">
              {t["intro"]}
            </p>

            <div class="format-compare__groups" role="tablist" aria-label="{t["title"]}">
              <button type="button" class="format-compare__group is-active" role="tab" data-group="anlass" aria-selected="true" id="format-tab-anlass" aria-controls="format-panel">
                {group_anlass}
              </button>
              <button type="button" class="format-compare__group" role="tab" data-group="durchfuehrung" aria-selected="false" id="format-tab-durchfuehrung" aria-controls="format-panel">
                {group_durchfuehrung}
              </button>
            </div>

            <div class="format-compare__toolbar">
              <div class="format-compare__filter" data-chip-group="anlass" role="group" aria-label="{t["filter_label"]}">
{chr(10).join(chips_anlass)}
              </div>
              <div class="format-compare__filter" data-chip-group="durchfuehrung" role="group" aria-label="{t["filter_label"]}" hidden>
{chr(10).join(chips_durchfuehrung)}
              </div>
              <p class="format-compare__status" id="format-compare-status" aria-live="polite" aria-atomic="true"></p>
            </div>

            <div class="format-compare__list" id="format-panel" role="tabpanel" aria-labelledby="format-tab-anlass">
{cards}
            </div>

            <p class="format-compare__note">{t["note"]}</p>
          </div>"""


def inject_compare(main: str, lang: str) -> str:
    block = render_compare(lang)
    pattern = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        re.DOTALL,
    )
    replacement = f"{MARKER_START}\n{block}\n          {MARKER_END}"
    if not pattern.search(main):
        raise SystemExit(f"Missing {MARKER_START} … {MARKER_END} in coaching main content")
    return pattern.sub(replacement, main, count=1)


def patch_file(path: Path, lang: str) -> str:
    raw = path.read_text(encoding="utf-8")
    main = strip_wrapped_artifacts(extract_main(raw))
    if not main:
        raise SystemExit(f"Could not extract <main> from {path}")
    return inject_compare(main, lang)


def main() -> None:
    de_main = patch_file(ROOT / "coaching.html", "de")
    en_main = patch_file(ROOT / "en" / "coaching.html", "en")
    build_page("de", "coaching.html", de_main, ROOT / "coaching.html")
    build_page("en", "coaching.html", en_main, ROOT / "en" / "coaching.html")
    print("Built coaching format compare (DE + EN)")


if __name__ == "__main__":
    main()
