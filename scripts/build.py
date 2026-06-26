#!/usr/bin/env python3
"""Run the full static site build (fonts, assets, pages, sitemap)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ASSET_STEPS = frozenset({
    "build_fonts.py",
    "build_images.py",
    "build_favicons.py",
})

STEPS = (
    "build_fonts.py",
    "build_images.py",
    "build_favicons.py",
    "build_psi_bridge.py",
    "wrap_pages.py",
    "build_referenzen.py",
    "build_coaching.py",
    "build_standorte.py",
    "build_sitemap.py",
    "build_llms.py",
)


def build_steps() -> tuple[str, ...]:
    if os.environ.get("VERCEL"):
        # Fonts, images and favicons are committed; Vercel has no Pillow by default.
        return tuple(step for step in STEPS if step not in ASSET_STEPS)
    return STEPS


def main() -> None:
    scripts_dir = ROOT / "scripts"
    for step in build_steps():
        path = scripts_dir / step
        print(f"\n==> {step}")
        subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
