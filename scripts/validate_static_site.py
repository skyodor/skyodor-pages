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

# Audit every UTF-8 text file type that can participate in a static deployment.
text_exts = {
    ".html", ".htm", ".css", ".js", ".mjs", ".cjs", ".json", ".jsonc",
    ".md", ".txt", ".xml", ".svg", ".webmanifest", ".map", ".yaml", ".yml",
    ".toml", ".ini", ".sql"
}
internal_host_patterns = [
    re.compile(r"https?://(?:www\.)?skyodor\.com", re.I),
    re.compile(r"https?://skyodor\.github\.io", re.I),
]
internal_path_patterns = [
    re.compile(r"(?:^|[\"'=(])/(?:site/)?v21(?:/|[\"')?#]|$)", re.I),
    re.compile(r"(?:^|[\"'=(])/(?:site/)?new(?:/|[\"')?#]|$)", re.I),
]
prohibited_patterns = [
    re.compile(r"utm_source=chatgpt", re.I),
    re.compile(r"(?:https?:)?//(?:www\.)?(?:chatgpt|openai)\.com", re.I),
]
local_string_pattern = re.compile(
    r"[\"'`]((?:\.\.?/|assets/|content/|images/|css/|js/|fonts/)[^\"'`\s]+)"
)

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in text_exts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"{path.relative_to(ROOT)}: text file is not valid UTF-8")
        continue

    rel = path.relative_to(ROOT)
    for pattern in internal_host_patterns:
        if pattern.search(text):
            errors.append(f"{rel}: hard-coded internal domain URL")
    for pattern in internal_path_patterns:
        if pattern.search(text):
            errors.append(f"{rel}: hard-coded deployment path")
    for pattern in prohibited_patterns:
        if pattern.search(text):
            errors.append(f"{rel}: prohibited tracking/branding reference")

    if path.suffix.lower() in {".html", ".htm"}:
        soup = BeautifulSoup(text, "html.parser")
        for node in soup.find_all(True):
            if node.name in {"img", "source"}:
                images += 1
            for attr in ("src", "href", "poster", "data-src", "data-original", "data-background-image", "srcset"):
                raw = node.get(attr)
                if not isinstance(raw, str) or not raw:
                    continue
                # srcset may contain several candidates; validate each local candidate.
                values = [part.strip().split()[0] for part in raw.split(",")] if attr == "srcset" else [raw]
                for value in values:
                    if value.startswith(("#", "data:", "mailto:", "tel:", "javascript:", "http://", "https://", "//")):
                        continue
                    checked += 1
                    target_path = urlsplit(value).path
                    if not target_path:
                        continue
                    target = (path.parent / target_path).resolve()
                    if not target.exists():
                        errors.append(f"{rel}: missing {attr} -> {value}")

    if path.suffix.lower() == ".css":
        for raw in re.findall(r"url\(\s*['\"]?([^'\")]+)", text, re.I):
            if raw.startswith(("data:", "http://", "https://", "//", "#")):
                continue
            checked += 1
            target_path = urlsplit(raw).path
            if target_path and not (path.parent / target_path).resolve().exists():
                errors.append(f"{rel}: missing CSS asset -> {raw}")

    # Check explicit local asset/path strings in JS/JSON/Markdown/config files.
    if path.suffix.lower() not in {".html", ".htm", ".css"}:
        for raw in local_string_pattern.findall(text):
            raw_path = urlsplit(raw).path
            if not raw_path:
                continue
            # Source provenance such as site/v0.1/... is reference data, not a runtime path.
            if raw.startswith("assets/") or raw.startswith(("./assets/", "../assets/", "content/", "./content/", "../content/", "fonts/", "images/", "css/", "js/")):
                checked += 1
                target = (path.parent / raw_path).resolve()
                if not target.exists():
                    errors.append(f"{rel}: missing local reference -> {raw}")

print(f"Audited all text files under {ROOT}; validated {checked} local references; found {images} image/source nodes")
if errors:
    for error in errors[:200]:
        print(f"ERROR: {error}")
    print(f"Validation failed with {len(errors)} issue(s)")
    raise SystemExit(1)
print("Portable static-site full-file validation passed")
