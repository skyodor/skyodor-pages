#!/usr/bin/env python3
"""Build a structurally redesigned v03 while preserving crawled source content and assets."""
from pathlib import Path
from bs4 import BeautifulSoup
import os
import shutil

SRC = Path('site/v02')
OUT = Path('site/v03')
CSS = r'''
:root{--ink:#172033;--muted:#687386;--paper:#f4f6f8;--panel:#fff;--line:#dfe5ec;--accent:#ff5c35;--accent2:#1647ff;--dark:#111827;--max:1280px;--radius:18px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.75 Inter,ui-sans-serif,system-ui,sans-serif}body:before{content:'';display:block;height:6px;background:linear-gradient(90deg,var(--accent),#ffb347,var(--accent2))}a{color:var(--accent2);text-underline-offset:4px}img{max-width:100%;height:auto;border-radius:14px}header{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.94);backdrop-filter:blur(16px);border-bottom:1px solid var(--line);padding:18px clamp(20px,5vw,72px)}nav{max-width:var(--max);margin:auto;display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap}nav a{text-decoration:none;color:var(--dark);font-size:.8rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase}main{max-width:var(--max);margin:auto;padding:clamp(42px,8vw,110px) clamp(20px,5vw,72px)}main:before{content:'SKYODOR / PRODUCT ARCHIVE';display:block;color:var(--accent);font-size:.72rem;font-weight:800;letter-spacing:.2em;margin-bottom:24px}h1,h2,h3,h4{font-family:ui-sans-serif,system-ui,sans-serif;color:var(--dark);line-height:1.08;letter-spacing:-.05em}h1{font-size:clamp(2.8rem,7vw,6.8rem);max-width:1000px;margin:.1em 0 .5em}h2{font-size:clamp(2rem,4vw,4rem);margin:1.5em 0 .6em}h3{font-size:clamp(1.3rem,2.5vw,2rem);margin-top:1.5em}section,.card,.product,article{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:clamp(20px,4vw,48px);box-shadow:0 16px 50px rgba(17,24,39,.06)}section{margin:42px 0}section>h2:first-child{margin-top:0}table{width:100%;border-collapse:collapse;background:#fff}th,td{padding:13px 15px;border-bottom:1px solid var(--line);text-align:left}th{background:var(--dark);color:#fff}blockquote{border-left:5px solid var(--accent);margin:30px 0;padding:18px 24px;background:#fff1ed}footer{background:var(--dark);color:#dce2ec;padding:44px clamp(20px,5vw,72px);max-width:none}footer a{color:#ffb9aa}.v03-shell{display:grid;grid-template-columns:minmax(0,1fr);gap:28px}.v03-intro{border-left:7px solid var(--accent);padding-left:22px}.v03-skip{position:absolute;left:-9999px}.v03-skip:focus{left:16px;top:16px;z-index:99;background:#fff;padding:10px 16px}@media(min-width:1000px){.v03-shell{grid-template-columns:minmax(0,1fr) 220px}.v03-rail{position:sticky;top:110px;align-self:start;border-top:3px solid var(--accent);padding-top:14px;font-size:.85rem;color:var(--muted)}}@media(max-width:760px){header{position:relative}body{font-size:15px}main{padding-top:35px}section,.card,.product,article{padding:22px;margin-block:28px}table{display:block;overflow-x:auto}}
'''

def redesign_document(path, css_path):
    soup = BeautifulSoup(path.read_text(encoding='utf-8', errors='replace'), 'html.parser')
    if not soup.html:
        return False
    soup.html['data-design-version'] = 'v03'
    body = soup.body or soup.new_tag('body')
    if not soup.body:
        soup.append(body)
    body['class'] = list(dict.fromkeys(body.get('class', []) + ['skyodor-v03', 'editorial-layout']))
    # Add accessible skip navigation and a deliberate page shell without rewriting source copy.
    if not soup.find(class_='v03-skip'):
        skip = soup.new_tag('a', href='#v03-content')
        skip['class'] = ['v03-skip']
        skip.string = 'Skip to content'
        body.insert(0, skip)
    main_tag = soup.find('main')
    if main_tag and not main_tag.find(id='v03-content'):
        main_tag['id'] = 'v03-content'
        shell = soup.new_tag('div'); shell['class'] = ['v03-shell']
        rail = soup.new_tag('aside'); rail['class'] = ['v03-rail']
        rail.string = 'SKYODOR\nARCHIVE'
        children = list(main_tag.contents)
        for child in children:
            shell.append(child.extract())
        main_tag.append(shell)
        shell.append(rail)
    rel = Path(os.path.relpath(css_path, start=path.parent)).as_posix()
    if not soup.find('link', href=rel):
        link = soup.new_tag('link', rel='stylesheet', href=rel)
        (soup.head or soup).append(link)
    path.write_text(str(soup), encoding='utf-8')
    return True

def main():
    if not SRC.exists():
        raise SystemExit('Missing site/v02; run baseline build first')
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)
    css_path = OUT/'assets'/'css'/'skyodor-v03.css'
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(CSS, encoding='utf-8')
    count = 0
    for path in OUT.rglob('*.html'):
        if redesign_document(path, css_path): count += 1
    print(f'Built structural v03 redesign across {count} HTML files')

if __name__ == '__main__': main()
