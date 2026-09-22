#!/usr/bin/env python3
"""Validate the isolated site/new implementation."""
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import json, re, sys

ROOT = Path(__file__).resolve().parents[1] / "site" / "new"
errors = []
checked = 0

required = [
    "index.html","about.html","products.html","lifestyle.html","category.html",
    "purchase.html","purchase-process.html","product.html","product-30ml.html",
    "product-50ml.html","product-50mlx.html","diffuser-wood.html","styles.css",
    "content/product-catalog.json","content/inventory.json"
]
for name in required:
    if not (ROOT / name).is_file():
        errors.append(f"missing required file: {name}")

catalog_path = ROOT / "content" / "product-catalog.json"
if catalog_path.is_file():
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        products = catalog.get("products", [])
        if len(products) < 40:
            errors.append(f"product catalogue incomplete: {len(products)} records")
        for product in products:
            image = product.get("image")
            if image:
                checked += 1
                if not (ROOT / image).resolve().exists():
                    errors.append(f"catalog image missing: {product.get('code')} -> {image}")
    except Exception as exc:
        errors.append(f"invalid product catalogue JSON: {exc}")

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
