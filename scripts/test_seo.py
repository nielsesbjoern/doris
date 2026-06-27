#!/usr/bin/env python3
"""Smoke tests for SEO URL helpers and EN internal links."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from seo import (  # noqa: E402
    OG_IMAGE,
    OG_IMAGE_BRAND,
    OG_IMAGE_BRAND_WIDTH,
    OG_IMAGE_WIDTH,
    absolute_url,
    clean_internal_hrefs,
    clean_path,
    content_asset_prefix,
    og_image_meta,
    page_href,
    page_link_prefix,
    wizard_href,
    wizard_href_for_page,
)

ROOT = Path(__file__).resolve().parent.parent

ASSET_PATH_MARKERS = ("/public/", "/css/", "/js/")


def extract_main(html: str) -> str:
    match = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else ""


def parent_depth(href: str) -> int:
    depth = 0
    rest = href
    while rest.startswith("../"):
        depth += 1
        rest = rest[3:]
    return depth


def is_asset_href(href: str) -> bool:
    return any(marker in href for marker in ASSET_PATH_MARKERS)


def test_clean_path() -> None:
    assert clean_path("index.html") == ""
    assert clean_path("kontakt.html") == "kontakt"
    assert clean_path("standorte/berlin.html") == "standorte/berlin"


def test_absolute_url() -> None:
    assert absolute_url("index.html", "de") == "https://www.doris-gunsch.eu/"
    assert absolute_url("index.html", "en") == "https://www.doris-gunsch.eu/en/"
    assert absolute_url("kontakt.html", "de") == "https://www.doris-gunsch.eu/kontakt"
    assert absolute_url("standorte/berlin.html", "en") == (
        "https://www.doris-gunsch.eu/en/standorte/berlin"
    )


def test_page_href() -> None:
    assert page_href("index.html") == "./"
    assert page_href("kontakt.html", "../") == "../kontakt"
    assert page_href("standorte/berlin.html", "../../") == "../../standorte/berlin"
    assert page_href("standorte/berlin.html", "") == "standorte/berlin"


def test_page_link_prefix() -> None:
    assert page_link_prefix("index.html") == ""
    assert page_link_prefix("coaching.html") == ""
    assert page_link_prefix("standorte/berlin.html") == "../"


def test_content_asset_prefix() -> None:
    assert content_asset_prefix("de", "index.html") == ""
    assert content_asset_prefix("en", "index.html") == "../"
    assert content_asset_prefix("de", "standorte/berlin.html") == "../"
    assert content_asset_prefix("en", "standorte/berlin.html") == "../../"


def test_clean_internal_hrefs() -> None:
    assert 'href="kontakt"' in clean_internal_hrefs('<a href="kontakt.html">')
    assert 'href="../leistungen"' in clean_internal_hrefs('<a href="../leistungen.html">')
    assert clean_internal_hrefs('<a href="mailto:x@y.z">') == '<a href="mailto:x@y.z">'


def test_og_image_meta() -> None:
    url, w, h, alt = og_image_meta("coaching.html", "de")
    assert url == OG_IMAGE_BRAND
    assert w == OG_IMAGE_BRAND_WIDTH
    url, w, h, alt = og_image_meta("index.html", "de")
    assert url == OG_IMAGE
    assert w == OG_IMAGE_WIDTH
    url, _, _, alt = og_image_meta("standorte/berlin.html", "de", city="Berlin")
    assert url == OG_IMAGE
    assert "Berlin" in alt


def test_knows_about_localized() -> None:
    from seo import KNOWS_ABOUT, business_schema

    assert "Führungskräfteentwicklung" in business_schema("de")
    assert "Leadership development" in business_schema("en")
    assert len(KNOWS_ABOUT["de"]) == len(KNOWS_ABOUT["en"])


def test_en_main_links_stay_in_language_tree() -> None:
    """EN pages must not link above /en/ via too many ../ segments."""
    en_dir = ROOT / "en"
    for path in sorted(en_dir.rglob("*.html")):
        meta_filename = path.relative_to(en_dir).as_posix()
        max_parent = page_link_prefix(meta_filename).count("../")
        main = extract_main(path.read_text(encoding="utf-8"))
        if not main:
            continue

        for match in re.finditer(r'href="([^"]+)"', main):
            href = match.group(1)
            if href.startswith(("#", "mailto:", "tel:", "http:", "https:")):
                continue
            if is_asset_href(href):
                continue
            depth = parent_depth(href)
            if depth > max_parent:
                raise AssertionError(
                    f"{path.relative_to(ROOT)}: {href!r} escapes /en/ "
                    f"(../ depth {depth}, max {max_parent})"
                )


def test_en_top_level_main_has_no_parent_links() -> None:
    for path in sorted((ROOT / "en").glob("*.html")):
        main = extract_main(path.read_text(encoding="utf-8"))
        for match in re.finditer(r'href="(\.\./[^"]+)"', main):
            href = match.group(1)
            if is_asset_href(href):
                continue
            raise AssertionError(f"{path.name}: parent-relative link in <main>: {href}")


def test_wizard_href() -> None:
    assert wizard_href("", leistung="coaching", same_page=True) == "?leistung=coaching#kontakt-anfrage"
    assert wizard_href("../", leistung="team", stadt="Berlin") == "../kontakt?leistung=team&stadt=Berlin#kontakt-anfrage"
    assert wizard_href_for_page("coaching.html", "") == "kontakt?leistung=coaching#kontakt-anfrage"
    assert wizard_href_for_page("person.html", "") == "kontakt#kontakt-anfrage"


def main() -> None:
    test_clean_path()
    test_absolute_url()
    test_page_href()
    test_page_link_prefix()
    test_content_asset_prefix()
    test_clean_internal_hrefs()
    test_og_image_meta()
    test_knows_about_localized()
    test_wizard_href()
    test_en_top_level_main_has_no_parent_links()
    test_en_main_links_stay_in_language_tree()
    print("OK: seo helpers and EN link checks")


if __name__ == "__main__":
    main()
