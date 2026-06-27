#!/usr/bin/env python3
"""HTML smoke tests and build injector checks."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_CANONICAL = frozenset({"404.html", "en/404.html"})


def html_pages() -> list[Path]:
    pages: list[Path] = []
    for path in sorted(ROOT.glob("*.html")):
        pages.append(path)
    en_dir = ROOT / "en"
    if en_dir.is_dir():
        pages.extend(sorted(en_dir.rglob("*.html")))
    standorte = ROOT / "standorte"
    if standorte.is_dir():
        pages.extend(sorted(standorte.glob("*.html")))
    en_standorte = en_dir / "standorte"
    if en_standorte.is_dir():
        pages.extend(sorted(en_standorte.glob("*.html")))
    return pages


def count_h1(html: str) -> int:
    return len(re.findall(r"<h1\b", html, re.IGNORECASE))


def test_pages_have_single_h1() -> None:
    for path in html_pages():
        rel = path.relative_to(ROOT).as_posix()
        html = path.read_text(encoding="utf-8")
        count = count_h1(html)
        if count != 1:
            raise AssertionError(f"{rel}: expected 1 <h1>, found {count}")


def test_pages_have_canonical() -> None:
    for path in html_pages():
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_CANONICAL:
            continue
        html = path.read_text(encoding="utf-8")
        if 'rel="canonical"' not in html:
            raise AssertionError(f"{rel}: missing canonical link")


def test_coaching_format_injector() -> None:
    for rel in ("coaching-formate.html", "en/coaching-formate.html"):
        path = ROOT / rel
        html = path.read_text(encoding="utf-8")
        for marker in (
            'id="formate-vergleich"',
            "format-guide",
            'id="format-panel"',
            "coaching-formats.js",
        ):
            if marker not in html:
                raise AssertionError(f"{rel}: missing format-finder marker {marker!r}")


def test_psi_bridge_injector() -> None:
    checks = {
        "diagnostik.html": ('id="psi-theorie"', "science-use-cases"),
        "en/diagnostik.html": ('id="psi-theorie"', "science-use-cases"),
        "index.html": ("home-science-note", "<!-- PSI_HOME_BRIDGE -->"),
        "en/index.html": ("home-science-note", "<!-- PSI_HOME_BRIDGE -->"),
        "leistungen.html": ("science-bridge--compact",),
        "en/leistungen.html": ("science-bridge--compact",),
        "coaching.html": ("coaching-foundation",),
        "en/coaching.html": ("coaching-foundation",),
        "trainings.html": ("PSI_TRAININGS_BRIDGE", "science-bridge--compact"),
        "en/trainings.html": ("PSI_TRAININGS_BRIDGE", "science-bridge--compact"),
        "team.html": ("PSI_TEAM_BRIDGE", "science-bridge--compact"),
        "en/team.html": ("PSI_TEAM_BRIDGE", "science-bridge--compact"),
    }
    for rel, markers in checks.items():
        path = ROOT / rel
        html = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in html:
                raise AssertionError(f"{rel}: missing PSI bridge marker {marker!r}")


def test_no_legacy_format_compare_css() -> None:
    source = ROOT / "css" / "styles.source.css"
    if not source.exists():
        return
    text = source.read_text(encoding="utf-8")
    if ".format-compare__" in text or re.search(r"\.format-compare\b", text):
        raise AssertionError("styles.source.css still contains legacy .format-compare__ rules")


def test_site_js_deferred() -> None:
    pattern = re.compile(r'<script[^>]*src="[^"]*site\.js[^"]*"[^>]*>', re.IGNORECASE)
    for path in html_pages():
        rel = path.relative_to(ROOT).as_posix()
        for match in pattern.finditer(path.read_text(encoding="utf-8")):
            if "defer" not in match.group(0):
                raise AssertionError(f"{rel}: site.js should load with defer")


def test_homepage_uses_contact_cta_not_wizard() -> None:
    for rel in ("index.html", "en/index.html"):
        html = (ROOT / rel).read_text(encoding="utf-8")
        if 'id="contact-wizard"' in html:
            raise AssertionError(f"{rel}: full contact wizard should not be on homepage")
        if "home-contact-cta" not in html:
            raise AssertionError(f"{rel}: missing home contact CTA")
        if 'href="kontakt#kontakt-anfrage"' not in html:
            raise AssertionError(f"{rel}: missing link to contact wizard")


def test_homepage_format_finder_links() -> None:
    for rel in ("index.html", "en/index.html"):
        html = (ROOT / rel).read_text(encoding="utf-8")
        if 'href="coaching-formate"' not in html:
            raise AssertionError(f"{rel}: missing format finder link")
        if rel.startswith("en/") and re.search(r'href="\.\./coaching-formate"', html):
            raise AssertionError(f"{rel}: format finder link escapes /en/")


def test_standort_pages_have_mini_case_disclaimer() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from standorte_data import CITY_SLUGS, STANDORT_UI  # noqa: E402

    de_disclaimer = STANDORT_UI["de"]["mini_case_disclaimer"][:40]
    en_disclaimer = STANDORT_UI["en"]["mini_case_disclaimer"][:40]
    for slug in CITY_SLUGS:
        for lang, subdir in (("de", "standorte"), ("en", "en/standorte")):
            path = ROOT / subdir / f"{slug}.html"
            html = path.read_text(encoding="utf-8")
            rel = path.relative_to(ROOT).as_posix()
            if "standort-case__disclaimer" not in html:
                raise AssertionError(f"{rel}: missing mini-case disclaimer")
            snippet = de_disclaimer if lang == "de" else en_disclaimer
            if snippet not in html:
                raise AssertionError(f"{rel}: disclaimer text not found")
            if "standort-case" not in html:
                raise AssertionError(f"{rel}: missing illustrative mini-case block")


def test_standort_pages_have_references() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from standorte_data import CITY_SLUGS  # noqa: E402

    for slug in CITY_SLUGS:
        for subdir in ("standorte", "en/standorte"):
            path = ROOT / subdir / f"{slug}.html"
            html = path.read_text(encoding="utf-8")
            rel = path.relative_to(ROOT).as_posix()
            if "standort-refs" not in html:
                raise AssertionError(f"{rel}: missing references section")
            if html.count("<li") < 3:
                raise AssertionError(f"{rel}: expected at least 3 list items (references/mandates)")


def main() -> None:
    test_pages_have_single_h1()
    test_pages_have_canonical()
    test_coaching_format_injector()
    test_psi_bridge_injector()
    test_no_legacy_format_compare_css()
    test_site_js_deferred()
    test_homepage_uses_contact_cta_not_wizard()
    test_homepage_format_finder_links()
    test_standort_pages_have_mini_case_disclaimer()
    test_standort_pages_have_references()
    print("OK: HTML smoke tests and injector checks")


if __name__ == "__main__":
    main()
