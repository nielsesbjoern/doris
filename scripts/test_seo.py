#!/usr/bin/env python3
"""Smoke tests for SEO URL helpers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from seo import (  # noqa: E402
    absolute_url,
    clean_internal_hrefs,
    clean_path,
    page_href,
)


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


def test_clean_internal_hrefs() -> None:
    assert 'href="kontakt"' in clean_internal_hrefs('<a href="kontakt.html">')
    assert 'href="../leistungen"' in clean_internal_hrefs('<a href="../leistungen.html">')
    assert clean_internal_hrefs('<a href="mailto:x@y.z">') == '<a href="mailto:x@y.z">'


def main() -> None:
    test_clean_path()
    test_absolute_url()
    test_page_href()
    test_clean_internal_hrefs()
    print("OK: seo helpers")


if __name__ == "__main__":
    main()
