#!/usr/bin/env python3
"""Remove residual site-builder branding and references from generated HTML."""
from pathlib import Path
import re
from bs4 import BeautifulSoup

ROOT = Path('site')
MARKERS = re.compile(r'(?i)(weebly(?:cloud)?|powered\s+by\s+weebly)')
URL_MARKERS = re.compile(r'(?i)(https?:)?//[^\"\'\s>]*(?:weebly|weeblycloud)[^\"\'\s>]*')
SCRIPT_MARKERS = re.compile(r'(?i)(?:_W\.configDomain|_W\.relinquish|weebly(?:cloud)?)')

for path in ROOT.rglob('*.html'):
    soup = BeautifulSoup(path.read_text(encoding='utf-8', errors='replace'), 'html.parser')
    for node in list(soup.find_all(['script', 'iframe', 'a', 'link', 'img', 'source'])):
        values = ' '.join(str(node.get(k, '')) for k in node.attrs)
        script_text = node.string if node.name == 'script' and node.string else ''
        if (MARKERS.search(values) or URL_MARKERS.search(values)
                or SCRIPT_MARKERS.search(script_text)):
            node.decompose()
    for node in soup.find_all(string=True):
        if node.parent and node.parent.name not in ('script', 'style'):
            cleaned = MARKERS.sub('', str(node))
            if cleaned != str(node):
                node.replace_with(cleaned)
    for node in soup.find_all(True):
        for key, value in list(node.attrs.items()):
            if isinstance(value, list):
                value = [MARKERS.sub('', str(v)) for v in value]
            elif isinstance(value, str):
                value = URL_MARKERS.sub('', MARKERS.sub('', value))
            node.attrs[key] = value
    path.write_text(str(soup), encoding='utf-8')
print('Residual branding cleanup completed')
