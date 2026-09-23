#!/usr/bin/env python3
"""Validate a portable static site for broken local references and deployment coupling."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
errors = []
checked = 0
images = 0
text_exts = {".html", ".css", ".js", ".json"}
internal_host_patterns = [
    re.compile(r"https?://(?:www\.)?skyodor\.com", re.I),
    re.compile(r"https?://skyodor\.github\.io", re.I),
]
internal_path_patterns = [
    re.compile(r"(?:^|[\"'=(])/(?:site/)?v21(?:/|[\"')?#]|$)", re.I),
    re.compile(r"(?:^|[\"'=(])/(?:site/)?new(?:/|[\"')?#]|$)", re.I),
]

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in text_exts:
        continue
    text = path.read_text(encoding="utf-8", errors="replace")

    for pattern in internal_host_patterns:
        if pattern.search(text):
            errors.append(f"{path.relative_to(ROOT)}: hard-coded internal domain URL")
    for pattern in internal_path_patterns:
        if pattern.search(text):
            errors.append(f"{path.relative_to(ROOT)}: hard-coded deployment path")
    if re.search(r"(?:utm_source=chatgpt|chatgpt\.com|openai\.com)", text, re.I):
        errors.append(f"{path.relative_to(ROOT)}: prohibited tracking/branding reference")

    if path.suffix.lower() == ".html":
        soup = BeautifulSoup(text, "html.parser")
        for node in soup.find_all(True):
            if node.name in {"img", "source"}:
                images += 1
            for attr in ("src", "href", "poster", "data-src", "data-original", "data-background-image"):
                raw = node.get(attr)
                if not isinstance(raw, str) or not raw:
                    continue
                if raw.startswith(("#", "data:", "mailto:", "tel:", "javascript:", "http://", "https://", "//")):
                    continue
                checked += 1
                target_path = urlsplit(raw).path
                if not target_path:
                    continue
                target = (path.parent / target_path).resolve()
                if not target.exists():
                    errors.append(f"{path.relative_to(ROOT)}: missing {attr} -> {raw}")

    # Validate relative url(...) references in CSS.
    if path.suffix.lower() == ".css":
        for raw in re.findall(r"url\(\s*['\"]?([^'\")]+)", text, re.I):
            if raw.startswith(("data:", "http://", "https://", "//", "#")):
                continue
            checked += 1
            target_path = urlsplit(raw).path
            if target_path and not (path.parent / target_path).resolve().exists():
                errors.append(f"{path.relative_to(ROOT)}: missing CSS asset -> {raw}")

print(f"Validated {checked} local references; found {images} image/source nodes")
if errors:
    for error in errors[:100]:
        print(f"ERROR: {error}")
    print(f"Validation failed with {len(errors)} issue(s)")
    raise SystemExit(1)
print("Portable static-site validation passed")
