#!/usr/bin/env python3
"""Static checks for the isolated site/new implementation."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / "site" / "new"
required = ["index.html", "products.html", "styles.css"]
errors = []

for name in required:
    if not (ROOT / name).is_file():
        errors.append(f"missing required file: {name}")

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in {".html", ".css", ".js"}:
        continue
    text = path.read_text(encoding="utf-8")
    if re.search(r"chatgpt|openai\\.com|utm_", text, re.I):
        errors.append(f"forbidden branding/tracking reference: {path.relative_to(ROOT)}")
    if re.search(r"site/v0\\.[123]|/v1\\.[12]", text):
        errors.append(f"legacy-version reference: {path.relative_to(ROOT)}")
    if "href=\"#\"" in text or "src=\"#\"" in text:
        errors.append(f"empty placeholder link: {path.relative_to(ROOT)}")

if errors:
    print("New-site validation failed:")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print("New-site static checks passed.")
