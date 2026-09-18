#!/usr/bin/env python3
"""Create a redesigned v03 presentation layer without changing source wording or images."""
from pathlib import Path
from bs4 import BeautifulSoup
import shutil

SRC = Path('site/v02')
OUT = Path('site/v03')
CSS = '''
:root{--sky-ink:#17212b;--sky-muted:#5f6b76;--sky-surface:#f6f8fa;--sky-line:#e4e9ee;--sky-accent:#1769aa;--sky-radius:18px;--sky-max:1240px}
*,*:before,*:after{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--sky-ink);background:#fff;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.65;font-size:16px}body>*{max-width:var(--sky-max);margin-inline:auto;padding-inline:clamp(18px,4vw,42px)}header,nav,main,footer{max-width:none}header{position:relative;background:#fff;border-bottom:1px solid var(--sky-line);padding-block:18px}nav{display:flex;gap:clamp(14px,2.5vw,32px);align-items:center;flex-wrap:wrap;max-width:var(--sky-max);margin:auto;padding-inline:clamp(18px,4vw,42px)}a{color:var(--sky-accent);text-underline-offset:3px}a:hover{text-decoration-thickness:2px}main{padding-block:clamp(28px,5vw,72px)}h1,h2,h3,h4{color:var(--sky-ink);line-height:1.15;letter-spacing:-.025em;margin-top:1.4em}h1{font-size:clamp(2.1rem,5vw,4.8rem);max-width:1000px}h2{font-size:clamp(1.6rem,3vw,2.8rem)}h3{font-size:clamp(1.25rem,2vw,1.8rem)}p,li{max-width:75ch}img{display:block;max-width:100%;height:auto;border-radius:var(--sky-radius)}figure{margin:clamp(20px,4vw,48px) 0}button,input,textarea,select{font:inherit}button{cursor:pointer}.container,.content,.page-content{max-width:var(--sky-max);margin-inline:auto}.card,.product,.gallery-item,article{border:1px solid var(--sky-line);border-radius:var(--sky-radius);padding:clamp(16px,2.5vw,28px);background:#fff;box-shadow:0 10px 30px rgba(23,33,43,.06)}section{margin-block:clamp(28px,5vw,76px)}footer{border-top:1px solid var(--sky-line);background:var(--sky-surface);padding-block:36px;margin-top:40px} @media(max-width:700px){body{font-size:15px}header{padding-block:12px}nav{gap:12px}main{padding-block:28px}h1{font-size:clamp(2rem,10vw,3rem)}img{border-radius:12px}table{display:block;overflow-x:auto}button,a{min-height:42px}section{margin-block:34px}}
'''

def main():
    if not SRC.exists(): raise SystemExit('Missing site/v02; run baseline build first')
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)
    css_path = OUT / 'assets' / 'css' / 'skyodor-v03.css'
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(CSS, encoding='utf-8')
    for path in OUT.rglob('*.html'):
        soup = BeautifulSoup(path.read_text(encoding='utf-8', errors='replace'), 'html.parser')
        if not soup.html: continue
        soup.html['data-design-version'] = 'v03'
        body = soup.body or soup.new_tag('body')
        if not soup.body: soup.append(body)
        existing = body.get('class', [])
        body['class'] = list(dict.fromkeys(existing + ['skyodor-v03']))
        href = path.parent.relative_to(OUT)
        rel = Path(__import__('os').path.relpath(css_path, start=path.parent)).as_posix()
        if not soup.find('link', href=rel):
            link = soup.new_tag('link', rel='stylesheet', href=rel)
            (soup.head or soup).append(link)
        path.write_text(str(soup), encoding='utf-8')
    print(f'Built redesigned v03 from locked v02 content: {len(list(OUT.rglob("*.html")))} HTML files')

if __name__ == '__main__': main()
