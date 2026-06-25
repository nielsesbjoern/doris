#!/usr/bin/env python3
"""Generate square favicons from the Doris Gunsch logo mark (speech bubbles)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
LOGO = PUBLIC / "doris-logo-web.png"

# Icon-only crop in source logo (speech bubbles, no wordmark).
ICON_CROP = (68, 155, 192, 318)
PADDING_RATIO = 0.14
BG = (255, 255, 255, 255)


def trim(icon: Image.Image, threshold: int = 35) -> Image.Image:
    pixels = icon.load()
    w, h = icon.size
    min_x, min_y, max_x, max_y = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a > 20 and max(r, g, b) > threshold:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
    return icon.crop((min_x, min_y, max_x + 1, max_y + 1))


def make_square_icon(src: Image.Image, size: int) -> Image.Image:
    sw, sh = src.size
    inner = int(size * (1 - 2 * PADDING_RATIO))
    scale = min(inner / sw, inner / sh)
    nw = max(1, int(sw * scale))
    nh = max(1, int(sh * scale))
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), BG)
    canvas.paste(resized, ((size - nw) // 2, (size - nh) // 2), resized)
    return canvas.convert("RGB")


def main() -> None:
    logo = Image.open(LOGO).convert("RGBA")
    icon = trim(logo.crop(ICON_CROP))

    outputs = {
        "favicon-16.png": 16,
        "favicon-32.png": 32,
        "apple-touch-icon.png": 180,
        "icon-192.png": 192,
    }
    for name, size in outputs.items():
        make_square_icon(icon, size).save(PUBLIC / name, optimize=True)

    ico16 = make_square_icon(icon, 16).convert("RGBA")
    ico32 = make_square_icon(icon, 32).convert("RGBA")
    ico32.save(
        PUBLIC / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32)],
        append_images=[ico16],
    )

    # Browsers often request /favicon.ico at site root.
    ico32.save(ROOT / "favicon.ico", format="ICO", sizes=[(32, 32)])

    print(f"Wrote favicons to {PUBLIC} and {ROOT / 'favicon.ico'}")


if __name__ == "__main__":
    main()
