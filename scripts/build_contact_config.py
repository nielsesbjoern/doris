#!/usr/bin/env python3
"""Emit js/contact-config.js from scripts/contact_config.py."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from contact_config import FORMSPREE_ENDPOINT  # noqa: E402


def main() -> None:
    payload = json.dumps({"formspreeEndpoint": FORMSPREE_ENDPOINT}, ensure_ascii=False)
    js = f"window.DorisContactConfig = {payload};\n"
    out = ROOT / "js" / "contact-config.js"
    out.write_text(js, encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
