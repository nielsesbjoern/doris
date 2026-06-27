#!/usr/bin/env python3
"""Minify CSS from source files for production deploys."""
from __future__ import annotations

from pathlib import Path

from css_utils import minify_css

ROOT = Path(__file__).resolve().parent.parent

CSS_SOURCES = (
    (ROOT / "css" / "fonts.css", ROOT / "css" / "fonts.css"),
    (ROOT / "css" / "styles.source.css", ROOT / "css" / "styles.css"),
)


def minify_file(source: Path, target: Path) -> None:
    original = source.read_text(encoding="utf-8")
    minified = minify_css(original)
    if target.exists():
        current = target.read_text(encoding="utf-8").strip()
        if current == minified:
            return
    target.write_text(minified + "\n", encoding="utf-8")
    print(
        f"Minified {source.relative_to(ROOT)} → {target.relative_to(ROOT)} "
        f"({len(original)} → {len(minified)} bytes)"
    )


def main() -> None:
    for source, target in CSS_SOURCES:
        if not source.exists():
            raise SystemExit(f"Missing CSS source: {source.relative_to(ROOT)}")
        minify_file(source, target)
    print("CSS minification complete")


if __name__ == "__main__":
    main()
