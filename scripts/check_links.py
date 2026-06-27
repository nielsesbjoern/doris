#!/usr/bin/env python3
"""Check internal HTML links resolve to files in the built site."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent

HREF_RE = re.compile(r'href="([^"]+)"')
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "javascript:", "#")
HTML_GLOBS = ("*.html", "en/**/*.html", "standorte/*.html", "en/standorte/*.html")


def html_files() -> list[Path]:
    files: list[Path] = []
    for pattern in HTML_GLOBS:
        files.extend(ROOT.glob(pattern))
    return sorted(set(files))


def resolve_href(href: str, source: Path) -> Optional[Path]:
    href = unquote(href.strip())
    if not href or href.startswith(SKIP_PREFIXES):
        return None

    parsed = urlparse(href)
    path = parsed.path
    if not path:
        return None

    if path.startswith("/"):
        candidate = ROOT / path.lstrip("/")
    else:
        candidate = (source.parent / path).resolve()

    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None

    if candidate.is_file():
        return candidate

    if candidate.with_suffix(".html").is_file():
        return candidate.with_suffix(".html")

    if candidate.is_dir() and (candidate / "index.html").is_file():
        return candidate / "index.html"

    return candidate


def check_links() -> list[str]:
    errors: list[str] = []
    for path in html_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for href in HREF_RE.findall(text):
            if href.startswith(SKIP_PREFIXES):
                continue
            target = resolve_href(href, path)
            if target is None:
                continue
            if not target.is_file():
                errors.append(f"{rel}: broken link {href!r} -> {target.relative_to(ROOT).as_posix()}")
    return errors


def main() -> None:
    errors = check_links()
    if errors:
        print("Broken internal links:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print(f"OK: internal link check ({len(html_files())} HTML files)")


if __name__ == "__main__":
    main()
