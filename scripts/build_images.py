#!/usr/bin/env python3
"""Generate responsive, compressed WebP/PNG/JPEG assets."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

LOGO_SRC = PUBLIC / "doris-logo-web.png"
PROFILE_SRC = PUBLIC / "doris-web.jpg"


def _save_webp(img: Image.Image, path: Path, quality: int = 82) -> None:
    img.save(path, format="WEBP", quality=quality, method=6)


def _save_jpeg(img: Image.Image, path: Path, quality: int = 82) -> None:
    img.convert("RGB").save(path, format="JPEG", quality=quality, optimize=True)


def _resize_logo(width: int) -> Image.Image:
    logo = Image.open(LOGO_SRC).convert("RGBA")
    ratio = width / logo.width
    height = max(1, round(logo.height * ratio))
    return logo.resize((width, height), Image.Resampling.LANCZOS)


def build_logos() -> None:
    for width in (280, 400):
        img = _resize_logo(width)
        height = img.height
        png_path = PUBLIC / f"doris-logo-{width}.png"
        webp_path = PUBLIC / f"doris-logo-{width}.webp"
        img.save(png_path, format="PNG", optimize=True)
        _save_webp(img, webp_path)
        print(f"  Logo {width}x{height}: {webp_path.name} ({webp_path.stat().st_size // 1024} KiB)")


def build_profile() -> None:
    photo = Image.open(PROFILE_SRC).convert("RGB")
    width = 600
    ratio = width / photo.width
    height = max(1, round(photo.height * ratio))
    resized = photo.resize((width, height), Image.Resampling.LANCZOS)
    jpg_path = PUBLIC / "doris-web-600.jpg"
    webp_path = PUBLIC / "doris-web-600.webp"
    _save_jpeg(resized, jpg_path)
    _save_webp(resized, webp_path)
    print(
        f"  Profile {width}x{height}: {webp_path.name} ({webp_path.stat().st_size // 1024} KiB)"
    )


def main() -> None:
    if not LOGO_SRC.exists():
        raise SystemExit(f"Missing {LOGO_SRC}")
    if not PROFILE_SRC.exists():
        raise SystemExit(f"Missing {PROFILE_SRC}")
    print("Building optimized images…")
    build_logos()
    build_profile()
    print("Done.")


if __name__ == "__main__":
    main()
