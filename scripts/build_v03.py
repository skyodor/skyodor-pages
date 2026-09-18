#!/usr/bin/env python3
"""Build V03 as a new presentation shell while preserving crawled source nodes."""
from pathlib import Path
from bs4 import BeautifulSoup
import os, shutil

SRC = Path('site/v02')
OUT = Path('site/v03')
CSS = r'''
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@500;600&display=swap');
:root{--paper:#f5f1e9;--ink:#22251f;--muted:#6d7068;--line:#d9d4c9;--accent:#8b6848;--dark:#20241f;--max:1440px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.8 'DM Sans',sans-serif}a{color:inherit;text-underline-offset:4px}img{display:block;max-width:100%;height:auto;border-radius:2px} .v03-header{padding:26px clamp(22px,5vw,80px);border-bottom:1px solid var(--line);background:rgba(245,241,233,.96);position:sticky;top:0;z-index:20}.v03-nav{max-width:var(--max);margin:auto;display:flex;justify-content:space-between;align-items:center;gap:25px}.v03-brand{font:600 1.45rem 'Playfair Display',serif;letter-spacing:.06em;text-decoration:none}.v03-label{font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}.v03-main{max-width:var(--max);margin:auto;padding:clamp(45px,8vw,120px) clamp(22px,5vw,80px)}.v03-hero{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(30px,7vw,110px);align-items:end;padding-bottom:clamp(55px,9vw,130px);border-bottom:1px solid var(--line)}.v03-hero h1{font:500 clamp(3rem,8vw,8.5rem)/.98 'Playfair Display',serif;letter-spacing:-.055em;margin:15px 0}.v03-hero p{max-width:38rem;color:var(--muted)}.v03-content{padding-top:20px}.v03-content>section{margin:70px 0;padding-top:40px;border-top:1px solid var(--line)}.v03-content h2{font:500 clamp(2rem,4.4vw,4.8rem)/1.05 'Playfair Display',serif;letter-spacing:-.04em;margin:0 0 28px}.v03-content h3{font-size:1.35rem;margin-top:35px}.v03-content p{max-width:70ch}.v03-content table{width:100%;border-collapse:collapse;overflow:auto}.v03-content th,.v03-content td{padding:12px;border-bottom:1px solid var(--line);text-align:left}.v03-footer{padding:55px clamp(22px,5vw,80px);background:var(--dark);color:#f5f1e9}.v03-footer a{color:#f5f1e9}.v03-skip{position:absolute;left:-9999px}.v03-skip:focus{left:15px;top:15px;background:#fff;padding:10px;z-index:99}@media(max-width:800px){.v03-header{position:relative}.v03-hero{grid-template-columns:1fr;gap:25px}.v03-main{padding-top:45px}.v03-content>section{margin:45px 0;padding-top:25px}}
'''

def text_of(node):
    return ' '.join(node.get_text(' ', strip=True).split())

def build_page(path, css_path):
    soup=BeautifulSoup(path.read_text(encoding='utf-8',errors='replace'),'html.parser')
    if not soup.html: return False
    old_body=soup.body
    if not old_body: return False
    original=[x.extract() for x in list(old_body.contents) if getattr(x,'name',None) not in ('script','style')]
    # Keep all source nodes, but place them inside a newly constructed page architecture.
    title=(soup.title.get_text(' ',strip=True) if soup.title else 'Skyodor')
    headings=[x for x in original if getattr(x,'name',None) in ('h1','h2','h3')]
    hero_heading=headings[0] if headings else None
    if hero_heading: original.remove(hero_heading)
    body=soup.new_tag('body'); body['class']=['skyodor-v03']
    skip=soup.new_tag('a',href='#v03-content'); skip['class']=['v03-skip']; skip.string='Skip to content'; body.append(skip)
    header=soup.new_tag('header'); header['class']=['v03-header']; nav=soup.new_tag('nav'); nav['class']=['v03-nav']
    brand=soup.new_tag('a',href='./'); brand['class']=['v03-brand']; brand.string='SKYODOR'
    label=soup.new_tag('span'); label['class']=['v03-label']; label.string='Scent · Wood · Time'
    nav.extend([brand,label]); header.append(nav); body.append(header)
    main=soup.new_tag('main'); main['id']='v03-content'; main['class']=['v03-main']
    hero=soup.new_tag('section'); hero['class']=['v03-hero']
    left=soup.new_tag('div'); eyebrow=soup.new_tag('div'); eyebrow['class']=['v03-label']; eyebrow.string='蝶漾香韻 / ODOR'; left.append(eyebrow)
    if hero_heading: left.append(hero_heading)
    else:
        h=soup.new_tag('h1'); h.string=title; left.append(h)
    right=soup.new_tag('div'); p=soup.new_tag('p'); p.string='An editorial presentation of the original Skyodor website content.'; right.append(p)
    hero.extend([left,right]); main.append(hero)
    content=soup.new_tag('div'); content['class']=['v03-content']
    section=None
    for node in original:
        if getattr(node,'name',None) in ('h2','h3'):
            section=soup.new_tag('section'); content.append(section)
        if section is None:
            section=soup.new_tag('section'); content.append(section)
        section.append(node)
    main.append(content); body.append(main)
    footer=soup.new_tag('footer'); footer['class']=['v03-footer']; footer.string='SKYODOR · 蝶漾香韻'; body.append(footer)
    soup.body.replace_with(body)
    rel=Path(os.path.relpath(css_path,start=path.parent)).as_posix()
    link=soup.new_tag('link',rel='stylesheet',href=rel); (soup.head or soup).append(link)
    soup.html['data-design-version']='v03'
    path.write_text(str(soup),encoding='utf-8'); return True

def main():
    if not SRC.exists(): raise SystemExit('Missing site/v02; run baseline build first')
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(SRC,OUT)
    css=OUT/'assets'/'css'/'skyodor-v03.css'; css.parent.mkdir(parents=True,exist_ok=True); css.write_text(CSS,encoding='utf-8')
    count=0
    for path in OUT.rglob('*.html'):
        if build_page(path,css): count+=1
    print(f'Built V03 structural shell across {count} HTML files')
if __name__=='__main__': main()
