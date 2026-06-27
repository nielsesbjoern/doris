#!/usr/bin/env python3
"""CSS minify/beautify helpers for the static site build."""
from __future__ import annotations

import re


def minify_css(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", text)
    text = text.replace(";}", "}")
    return text.strip()


def beautify_css(text: str, *, indent: int = 0) -> str:
    """Format minified CSS into readable blocks (stdlib only)."""
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return ""

    pad = "  " * indent
    out: list[str] = []
    i = 0
    n = len(text)

    while i < n:
        while i < n and text[i] == " ":
            i += 1
        if i >= n:
            break

        open_brace = text.find("{", i)
        if open_brace == -1:
            break

        selector = text[i:open_brace].strip()
        depth = 0
        j = open_brace
        while j < n:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1

        content = text[open_brace + 1 : j]
        out.append(f"{pad}{selector} {{")
        if "{" in content:
            nested = beautify_css(content, indent=indent + 1)
            if nested:
                out.append(nested)
        else:
            for part in content.split(";"):
                part = part.strip()
                if part:
                    out.append(f"{pad}  {part};")
        out.append(f"{pad}}}")
        out.append("")
        i = j + 1

    return "\n".join(out)


def _find_block_end(text: str, open_brace: int) -> int:
    depth = 0
    j = open_brace
    while j < len(text):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return len(text) - 1


def remove_rules_matching(text: str, predicate) -> str:
    """Remove top-level CSS blocks whose selector matches predicate."""
    text = re.sub(r"\s+", " ", text.strip())
    out: list[str] = []
    i = 0
    n = len(text)

    while i < n:
        while i < n and text[i] == " ":
            i += 1
        if i >= n:
            break

        open_brace = text.find("{", i)
        if open_brace == -1:
            out.append(text[i:])
            break

        selector = text[i:open_brace].strip()
        close = _find_block_end(text, open_brace)
        block = text[i : close + 1]

        if predicate(selector):
            i = close + 1
            continue

        if selector.startswith("@media") or selector.startswith("@supports"):
            inner = text[open_brace + 1 : close]
            cleaned_inner = remove_rules_matching(inner, predicate)
            cleaned_inner = re.sub(r"\s+", " ", cleaned_inner.strip())
            if cleaned_inner:
                out.append(f"{selector}{{{cleaned_inner}}}")
        else:
            out.append(block)

        i = close + 1

    return "".join(out)


def strip_format_compare_css(text: str) -> str:
    """Remove legacy .format-compare__* rules (replaced by .format-guide__*)."""

    def is_dead(selector: str) -> bool:
        return ".format-compare" in selector

    return remove_rules_matching(text, is_dead)
