#!/usr/bin/env python3
"""Validate the isolated site/new implementation."""
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import re, sys

ROOT = Path(__file__).resolve().parents[1] / "site" / "new"
errors = []
checked = 0

required = ["index.html","about.html","products.html","lifestyle.html","category.html","purchase.html","product.html","styles.css"]
for name in required:
    if not (ROOT / name).is_file():
        errors.append(f"missing required file: {name}")

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in {".html",".css",".js"}:
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    if re.search(r"chatgpt|openai\.com|utm_", text, re.I):
        errors.append(f"forbidden branding/tracking reference: {path.relative_to(ROOT)}")
    if re.search(r"(?:site/)?v0\.[123]|/v1\.[12]|(?:^|[^a-z])v03(?:[^a-z]|$)", text, re.I):
        errors.append(f"legacy-version reference: {path.relative_to(ROOT)}")

    if path.suffix.lower() == ".html":
        if re.search(r'href=["\']#["\']|src=["\']#["\']', text, re.I):
            errors.append(f"empty placeholder link: {path.relative_to(ROOT)}")
        soup = BeautifulSoup(text, "html.parser")
        for node in soup.find_all(True):
            for attr in ("src","href","poster","data-src","data-original"):
                raw = node.get(attr)
                if not isinstance(raw, str) or not raw:
                    continue
                if raw.startswith(("#","mailto:","tel:","data:","javascript:","http://","https://","//")):
                    continue
                target_path = urlsplit(raw).path
                if not target_path:
                    continue
                checked += 1
                if not (path.parent / target_path).resolve().exists():
                    errors.append(f"{path.relative_to(ROOT)}: missing {attr} -> {raw}")

print(f"Checked {checked} local references.")
if errors:
    print("New-site validation failed:")
    print("\n".join(f"- {error}" for error in errors[:100]))
    sys.exit(1)
print("New-site validation passed.")
