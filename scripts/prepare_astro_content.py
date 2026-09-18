from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'site' / 'v02' / 'index.html'
target = ROOT / 'astro' / 'src' / 'content' / 'home.html'
target.parent.mkdir(parents=True, exist_ok=True)
if source.exists():
    shutil.copyfile(source, target)
else:
    target.write_text('<body><p>Skyodor</p></body>', encoding='utf-8')
print('Prepared Astro content snapshot from v02 index')
