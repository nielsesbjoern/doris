#!/usr/bin/env python3
"""Generate square favicons from the Doris Gunsch logo mark (speech bubbles)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
LOGO = PUBLIC / "doris-logo-web.png"
LEGACY_WIDE_FAVICON = PUBLIC / "favicon.png"

# Icon-only region in source logo (speech bubbles, no wordmark).
ICON_CROP = (68, 155, 192, 318)
PADDING_RATIO = 0.1
RENDER_SIZE = 256
BG = (255, 255, 255, 255)
ICO_SIZES = (16, 32, 48)


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
    if max_x < min_x or max_y < min_y:
        return icon
    return icon.crop((min_x, min_y, max_x + 1, max_y + 1))


def make_square_icon(src: Image.Image, size: int) -> Image.Image:
    """Render large, then downscale for sharper small favicons."""
    sw, sh = src.size
    inner = int(RENDER_SIZE * (1 - 2 * PADDING_RATIO))
    scale = min(inner / sw, inner / sh)
    nw = max(1, int(sw * scale))
    nh = max(1, int(sh * scale))
    large = Image.new("RGBA", (RENDER_SIZE, RENDER_SIZE), BG)
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
    large.paste(resized, ((RENDER_SIZE - nw) // 2, (RENDER_SIZE - nh) // 2), resized)
    if size == RENDER_SIZE:
        return large.convert("RGB")
    return large.resize((size, size), Image.Resampling.LANCZOS).convert("RGB")


def write_ico(path: Path, icon: Image.Image) -> None:
    frames = {size: make_square_icon(icon, size).convert("RGBA") for size in ICO_SIZES}
    frames[32].save(
        path,
        format="ICO",
        sizes=[(size, size) for size in ICO_SIZES],
        append_images=[frames[48], frames[16]],
    )


def main() -> None:
    logo = Image.open(LOGO).convert("RGBA")
    icon = trim(logo.crop(ICON_CROP))

    outputs = {
        "favicon-16.png": 16,
        "favicon-32.png": 32,
        "favicon-48.png": 48,
        "apple-touch-icon.png": 180,
        "icon-192.png": 192,
    }
    for name, size in outputs.items():
        make_square_icon(icon, size).save(PUBLIC / name, optimize=True)

    write_ico(PUBLIC / "favicon.ico", icon)
    write_ico(ROOT / "favicon.ico", icon)

    if LEGACY_WIDE_FAVICON.exists():
        LEGACY_WIDE_FAVICON.unlink()
        print(f"Removed legacy wide {LEGACY_WIDE_FAVICON.name}")

    print(f"Wrote favicons to {PUBLIC} and {ROOT / 'favicon.ico'}")


if __name__ == "__main__":
    main()
