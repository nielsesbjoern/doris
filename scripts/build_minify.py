#!/usr/bin/env python3
"""Minify committed CSS and JS assets for production deploys."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CSS_FILES = (
    ROOT / "css" / "fonts.css",
    ROOT / "css" / "styles.css",
)


def minify_css(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", text)
    text = text.replace(";}", "}")
    return text.strip()


def minify_js(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"(^|[^:])//.*?$", r"\1", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([{}();,:=+\-*/<>!&|?\[\]])\s*", r"\1", text)
    return text.strip()


def minify_file(path: Path, *, kind: str) -> None:
    original = path.read_text(encoding="utf-8")
    minified = minify_css(original) if kind == "css" else minify_js(original)
    if minified != original:
        path.write_text(minified + "\n", encoding="utf-8")
        print(f"Minified {path.relative_to(ROOT)} ({len(original)} → {len(minified)} bytes)")


def main() -> None:
    for css_path in CSS_FILES:
        minify_file(css_path, kind="css")
    print("CSS minification complete (JS skipped — regex-safe)")


if __name__ == "__main__":
    main()
