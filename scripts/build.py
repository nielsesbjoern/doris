#!/usr/bin/env python3
"""Run the full static site build (fonts, assets, pages, sitemap)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STEPS = (
    "build_fonts.py",
    "build_images.py",
    "build_favicons.py",
    "wrap_pages.py",
    "build_referenzen.py",
    "build_standorte.py",
    "build_sitemap.py",
    "build_llms.py",
)


def main() -> None:
    scripts_dir = ROOT / "scripts"
    for step in STEPS:
        path = scripts_dir / step
        print(f"\n==> {step}")
        subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
