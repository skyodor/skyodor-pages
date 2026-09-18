#!/usr/bin/env python3
"""Download image URLs found in href attributes and rewrite them locally."""
from pathlib import Path
from urllib.parse import urljoin, urlparse
import os
import requests
from bs4 import BeautifulSoup

BASE = 'https://www.skyodor.com/'
ROOT = Path('site')
EXTS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
session = requests.Session()
session.headers['User-Agent'] = 'skyodor-static-builder/6.2'

for version in ('v01', 'v02'):
    version_root = ROOT / version
    for html in version_root.rglob('*.html'):
        soup = BeautifulSoup(html.read_text(encoding='utf-8', errors='replace'), 'html.parser')
        changed = False
        for node in soup.find_all('a', href=True):
            href = str(node['href'])
            parsed = urlparse(href)
            if not parsed.path.lower().endswith(EXTS) or not parsed.path.startswith('/uploads/'):
                continue
            remote = urljoin(BASE, href)
            local_asset = version_root / 'assets' / parsed.path.lstrip('/')
            local_asset.parent.mkdir(parents=True, exist_ok=True)
            if not local_asset.exists():
                response = session.get(remote, timeout=30)
                response.raise_for_status()
                local_asset.write_bytes(response.content)
            relative = Path(os.path.relpath(local_asset, html.parent)).as_posix()
            node['href'] = relative
            changed = True
        if changed:
            html.write_text(str(soup), encoding='utf-8')
print('Repaired image href references')
