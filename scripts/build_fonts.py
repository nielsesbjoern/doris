#!/usr/bin/env python3
"""Download and self-host Google Fonts (latin subsets) for faster, non-blocking loads."""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS_DIR = ROOT / "public" / "fonts"
CSS_OUT = ROOT / "css" / "fonts.css"

GOOGLE_CSS = (
    "https://fonts.googleapis.com/css2?"
    "family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&"
    "family=Inter:wght@400;500;600&display=swap"
)
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
KEEP_RANGES = ("/* latin */", "/* latin-ext */")


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def _download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _parse_blocks(css: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for match in re.finditer(r"/\* ([^*]+) \*/\s*(@font-face\s*\{[^}]+\})", css):
        blocks.append((match.group(1).strip(), match.group(2)))
    return blocks


def build_fonts_css() -> str:
    raw = _fetch(GOOGLE_CSS)
    FONTS_DIR.mkdir(parents=True, exist_ok=True)

    out_blocks: list[str] = []
    seen_urls: dict[str, str] = {}

    for label, block in _parse_blocks(raw):
        if label not in ("latin", "latin-ext"):
            continue

        url_match = re.search(r"url\((https://[^)]+\.woff2)\)", block)
        if not url_match:
            continue

        remote_url = url_match.group(1)
        if remote_url not in seen_urls:
            family_match = re.search(r"font-family:\s*'([^']+)'", block)
            style_match = re.search(r"font-style:\s*(\w+)", block)
            weight_match = re.search(r"font-weight:\s*(\d+)", block)
            family = family_match.group(1) if family_match else "font"
            style = style_match.group(1) if style_match else "normal"
            weight = weight_match.group(1) if weight_match else "400"
            subset = "latin-ext" if label == "latin-ext" else "latin"
            filename = (
                f"{_slug(family)}-{subset}-{weight}"
                f"{'-italic' if style == 'italic' else ''}.woff2"
            )
            dest = FONTS_DIR / filename
            if not dest.exists() or dest.stat().st_size == 0:
                print(f"  Downloading {filename}")
                _download(remote_url, dest)
            seen_urls[remote_url] = f"../public/fonts/{filename}"

        local_url = seen_urls[remote_url]
        local_block = re.sub(
            r"url\([^)]+\)",
            f"url('{local_url}')",
            block,
        )
        out_blocks.append(f"/* {label} */\n{local_block}")

    return "\n\n".join(out_blocks) + "\n"


def main() -> None:
    css = build_fonts_css()
    CSS_OUT.write_text(css, encoding="utf-8")
    font_count = len(list(FONTS_DIR.glob("*.woff2")))
    print(f"Wrote {CSS_OUT} ({font_count} font files in {FONTS_DIR})")


if __name__ == "__main__":
    main()
