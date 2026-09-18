#!/usr/bin/env python3
"""Build the v03 presentation layer while preserving crawled content and assets."""
from pathlib import Path
from bs4 import BeautifulSoup
import os
import shutil

SRC = Path('site/v02')
OUT = Path('site/v03')
CSS = r'''
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--ink:#102a43;--muted:#627d98;--paper:#f7fafc;--panel:#fff;--line:#d9e2ec;--blue:#1677ff;--cyan:#36d1dc;--navy:#071b33;--radius:22px;--max:1320px;--shadow:0 18px 60px rgba(16,42,67,.10)}
*,*:before,*:after{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--paper);font:400 16px/1.7 'DM Sans',system-ui,sans-serif;letter-spacing:-.01em}body:before{content:'';display:block;height:5px;background:linear-gradient(90deg,var(--blue),var(--cyan),#b8f171)}
body>*{max-width:var(--max);margin-inline:auto;padding-inline:clamp(20px,4vw,64px)}header{max-width:none;padding-block:20px;background:rgba(255,255,255,.92);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20;backdrop-filter:blur(18px)}nav{max-width:var(--max);margin:auto;display:flex;align-items:center;justify-content:space-between;gap:22px;flex-wrap:wrap}nav a{font-size:.86rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;color:var(--ink);padding:8px 0}nav a:hover{color:var(--blue)}main{max-width:var(--max);padding-top:clamp(34px,6vw,96px);padding-bottom:clamp(50px,8vw,120px)}main:before{content:'SKYODOR / DIGITAL CATALOG';display:block;color:var(--blue);font-size:.72rem;font-weight:700;letter-spacing:.18em;margin-bottom:22px}h1,h2,h3,h4{font-family:'Space Grotesk',system-ui,sans-serif;letter-spacing:-.055em;line-height:1.05;color:var(--navy);font-weight:700}h1{font-size:clamp(2.7rem,7vw,7.2rem);max-width:1050px;margin:.1em 0 .35em}h2{font-size:clamp(2rem,4vw,4rem);margin:1.5em 0 .55em}h3{font-size:clamp(1.3rem,2.3vw,2rem);margin-top:1.5em}h4{font-size:1.15rem}p,li{max-width:76ch}a{color:var(--blue);text-underline-offset:4px;text-decoration-thickness:1px}a:hover{text-decoration-thickness:2px}img{display:block;max-width:100%;height:auto;border-radius:var(--radius);box-shadow:var(--shadow)}figure{margin:clamp(28px,5vw,70px) 0}figcaption{font-size:.82rem;color:var(--muted);margin-top:10px}section{margin:clamp(38px,7vw,100px) 0;padding:clamp(24px,4vw,58px);border:1px solid var(--line);border-radius:var(--radius);background:var(--panel);box-shadow:0 8px 35px rgba(16,42,67,.045)}section>h2:first-child{margin-top:0}.container,.content,.page-content{max-width:var(--max);margin-inline:auto}.card,.product,.gallery-item,article{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(18px,3vw,34px);box-shadow:var(--shadow)}table{width:100%;border-collapse:collapse;background:var(--panel);border-radius:16px;overflow:hidden}th,td{padding:14px 16px;border-bottom:1px solid var(--line);text-align:left}th{background:var(--navy);color:#fff;font-weight:700}tr:last-child td{border-bottom:0}blockquote{margin:32px 0;padding:22px 28px;border-left:5px solid var(--cyan);background:#eafcff;border-radius:0 18px 18px 0}hr{border:0;border-top:1px solid var(--line);margin:50px 0}button,input,textarea,select{font:inherit}button{cursor:pointer;border:0;border-radius:999px;background:var(--blue);color:#fff;padding:12px 22px;font-weight:700}footer{max-width:none;margin-top:0;padding-top:44px;padding-bottom:44px;background:var(--navy);color:#d9e2ec}footer a{color:#9be7ff}ul,ol{padding-left:1.4em}::selection{background:#b8f171;color:var(--navy)}:focus-visible{outline:3px solid var(--cyan);outline-offset:4px}@media(max-width:760px){body{font-size:15px}header{position:relative;padding-block:14px}nav{justify-content:flex-start;gap:14px}main{padding-top:34px}main:before{font-size:.64rem}h1{font-size:clamp(2.6rem,12vw,4.4rem)}section{padding:22px;margin-block:34px}img{border-radius:15px}table{display:block;overflow-x:auto}button{min-height:44px}}
'''

def main():
    if not SRC.exists():
        raise SystemExit('Missing site/v02; run baseline build first')
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)
    css_path = OUT / 'assets' / 'css' / 'skyodor-v03.css'
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(CSS, encoding='utf-8')
    count = 0
    for path in OUT.rglob('*.html'):
        soup = BeautifulSoup(path.read_text(encoding='utf-8', errors='replace'), 'html.parser')
        if not soup.html:
            continue
        soup.html['data-design-version'] = 'v03'
        body = soup.body or soup.new_tag('body')
        if not soup.body:
            soup.append(body)
        body['class'] = list(dict.fromkeys(body.get('class', []) + ['skyodor-v03', 'editorial-layout']))
        rel = Path(os.path.relpath(css_path, start=path.parent)).as_posix()
        if not soup.find('link', href=rel):
            link = soup.new_tag('link', rel='stylesheet', href=rel)
            (soup.head or soup).append(link)
        path.write_text(str(soup), encoding='utf-8')
        count += 1
    print(f'Built v03 editorial design across {count} HTML files')

if __name__ == '__main__':
    main()
