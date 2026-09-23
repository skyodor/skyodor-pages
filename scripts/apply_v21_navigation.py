from pathlib import Path

ROOT = Path('site/v21')
SCRIPT = ROOT / 'navigation.js'

for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    relative_script = Path(__import__('os').path.relpath(SCRIPT, path.parent)).as_posix()
    tag = f'<script src="{relative_script}" defer></script>'

    # Remove any previous injected navigation.js tag, then insert the path
    # correct for this HTML file's directory.
    import re
    text = re.sub(r'\s*<script src="(?:\.\./)*navigation\.js" defer></script>', '', text)
    marker = '</head>'
    if marker not in text:
        raise SystemExit(f'Missing </head>: {path}')
    path.write_text(text.replace(marker, f'  {tag}\n{marker}', 1), encoding='utf-8')
    print(path)
