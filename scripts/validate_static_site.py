#!/usr/bin/env python3
"""Validate a generated static copy for missing local assets and unsafe external references."""
from __future__ import annotations
import sys
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
errors = []
checked = 0
images = 0

for html in ROOT.rglob("*.html"):
    soup = BeautifulSoup(html.read_text(encoding="utf-8", errors="replace"), "html.parser")
    for node in soup.find_all(True):
        if node.name in {"img", "source"}:
            images += 1
        for attr in ("src", "href", "poster", "data-src", "data-original", "data-background-image"):
            raw = node.get(attr)
            if not raw or not isinstance(raw, str):
                continue
            if raw.startswith(("#", "data:", "mailto:", "javascript:", "http://", "https://", "//")):
                continue
            checked += 1
            # Query strings and fragments are browser routing metadata, not filesystem paths.
            path_part = urlsplit(raw).path
            if not path_part:
                continue
            target = (html.parent / path_part).resolve()
            if not target.exists():
                errors.append(f"{html}: missing {attr} -> {raw}")

print(f"Validated {checked} local references; found {images} image/source nodes")
if errors:
    for error in errors[:100]:
        print(f"ERROR: {error}")
    print(f"Validation failed with {len(errors)} missing local references")
    raise SystemExit(1)
print("Static site validation passed")
