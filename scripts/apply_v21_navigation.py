from pathlib import Path

ROOT = Path('site/v21')
SCRIPT = 'navigation.js'
TAG = f'<script src="{SCRIPT}" defer></script>'

for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if TAG in text:
        continue
    marker = '</head>'
    if marker not in text:
        raise SystemExit(f'Missing </head>: {path}')
    path.write_text(text.replace(marker, f'  {TAG}\n{marker}', 1), encoding='utf-8')
    print(path)
