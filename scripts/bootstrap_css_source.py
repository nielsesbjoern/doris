#!/usr/bin/env python3
"""One-off helper: rebuild css/styles.source.css from legacy minified+tail layout."""
from __future__ import annotations

import os
from pathlib import Path

from css_utils import beautify_css, strip_format_compare_css

ROOT = Path(__file__).resolve().parent.parent
LEGACY = ROOT / "css" / "styles.css"
SOURCE = ROOT / "css" / "styles.source.css"
TAIL_MARKER = "/* Contact enquiry wizard */"


def main() -> None:
    if SOURCE.exists() and not os.environ.get("FORCE_BOOTSTRAP_CSS"):
        raise SystemExit(
            f"{SOURCE.name} already exists. Edit it directly or set FORCE_BOOTSTRAP_CSS=1 to rebuild."
        )
    raw = LEGACY.read_text(encoding="utf-8")
    lines = raw.splitlines()

    if len(lines) < 3:
        raise SystemExit("Unexpected styles.css layout")

    minified = lines[0]
    minified = strip_format_compare_css(minified)
    head = beautify_css(minified)

    try:
        tail_start = next(i for i, line in enumerate(lines) if line.strip() == TAIL_MARKER)
    except StopIteration:
        tail_start = 2

    tail = "\n".join(lines[tail_start:]).strip()
    source = f"{head.rstrip()}\n\n{tail}\n"
    SOURCE.write_text(source, encoding="utf-8")
    print(f"Wrote {SOURCE.relative_to(ROOT)} ({len(source)} bytes)")


if __name__ == "__main__":
    main()
