#!/usr/bin/env python3
"""Build a refined V03 presentation while retaining crawled source content and assets."""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import os, shutil

SRC = Path('site/v02')
OUT = Path('site/v03')
CSS = r'''
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@400;500;600&display=swap');
:root{--bg:#f7f4ee;--paper:#fffdf9;--ink:#24251f;--muted:#77766e;--line:#ded8cc;--wood:#846247;--dark:#24271f;--max:1500px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.75 'DM Sans',sans-serif}a{color:inherit;text-underline-offset:4px}img{max-width:100%;height:auto;display:block;border-radius:3px}button,input,textarea,select{font:inherit}.v03-skip{position:absolute;left:-9999px}.v03-skip:focus{left:1rem;top:1rem;z-index:100;background:#fff;padding:.7rem 1rem}.v03-header{background:rgba(247,244,238,.96);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}.v03-nav{max-width:var(--max);margin:auto;padding:22px clamp(22px,5vw,84px);display:flex;align-items:center;justify-content:space-between;gap:24px}.v03-brand{font:500 1.55rem/1 'Playfair Display',serif;letter-spacing:.08em;text-decoration:none}.v03-meta{font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}.v03-main{max-width:var(--max);margin:auto;padding:clamp(36px,7vw,100px) clamp(22px,5vw,84px)}.v03-hero{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(260px,.85fr);gap:clamp(30px,8vw,130px);align-items:end;padding:clamp(10px,3vw,45px) 0 clamp(55px,8vw,125px);border-bottom:1px solid var(--line)}.v03-hero h1{font:500 clamp(3.2rem,8.5vw,9rem)/.95 'Playfair Display',serif;letter-spacing:-.055em;margin:.3em 0 0;max-width:900px}.v03-hero-copy{color:var(--muted);max-width:34rem}.v03-content{padding-top:clamp(35px,5vw,75px)}.v03-section{display:grid;grid-template-columns:minmax(150px,.3fr) minmax(0,1fr);gap:clamp(25px,6vw,100px);padding:clamp(35px,5vw,75px) 0;border-bottom:1px solid var(--line)}.v03-section-label{font-size:.7rem;letter-spacing:.17em;text-transform:uppercase;color:var(--wood);padding-top:.5rem}.v03-section-body{min-width:0}.v03-section-body h2{font:500 clamp(2rem,4.6vw,5rem)/1.04 'Playfair Display',serif;letter-spacing:-.045em;margin:0 0 1.1rem}.v03-section-body h3{font-size:1.25rem;margin:2rem 0 .5rem}.v03-section-body p{max-width:70ch}.v03-section-body ul,.v03-section-body ol{padding-left:1.3rem}.v03-section-body img{margin:1.5rem 0;width:auto;max-height:620px;object-fit:cover}.v03-section-body img:nth-of-type(even){margin-left:auto}.v03-section-body a{ text-decoration-thickness:1px}.v03-section-body table{width:100%;border-collapse:collapse;margin:1.5rem 0;display:block;overflow-x:auto}.v03-section-body th,.v03-section-body td{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;white-space:normal}.v03-section-body th{font-weight:600;background:#ebe4d8}.v03-section-body blockquote{margin:1.5rem 0;padding:1rem 1.4rem;border-left:3px solid var(--wood);background:#eee7dc}.v03-footer{background:var(--dark);color:#f7f4ee;padding:42px clamp(22px,5vw,84px);display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}.v03-footer a{color:#f7f4ee}@media(max-width:800px){.v03-header{position:relative}.v03-nav{padding:18px 22px}.v03-main{padding-top:35px}.v03-hero{grid-template-columns:1fr;gap:20px}.v03-hero h1{font-size:clamp(3rem,15vw,6rem)}.v03-section{grid-template-columns:1fr;gap:10px;padding:38px 0}.v03-section-body img,.v03-section-body img:nth-of-type(even){width:100%;margin:1.2rem 0;max-height:none}.v03-footer{display:block}.v03-footer>*{margin:.4rem 0}}
'''

def make_section(soup, nodes, index):
    section=soup.new_tag('section'); section['class']=['v03-section']
    label=soup.new_tag('div'); label['class']=['v03-section-label']; label.string=f'{index:02d}'
    body=soup.new_tag('div'); body['class']=['v03-section-body']
    for node in nodes: body.append(node)
    section.extend([label,body]); return section

def build_page(path, css_path):
    soup=BeautifulSoup(path.read_text(encoding='utf-8',errors='replace'),'html.parser')
    if not soup.html or not soup.body: return False
    source_nodes=[]; scripts=[]
    for node in list(soup.body.contents):
        if getattr(node,'name',None) in ('script','style'): scripts.append(node.extract())
        else: source_nodes.append(node.extract())
    title=soup.title.get_text(' ',strip=True) if soup.title else 'Skyodor'
    headings=[n for n in source_nodes if getattr(n,'name',None) in ('h1','h2','h3')]
    hero_heading=headings[0] if headings else None
    if hero_heading in source_nodes: source_nodes.remove(hero_heading)
    body=soup.new_tag('body'); body['class']=['skyodor-v03']
    skip=soup.new_tag('a',href='#v03-content'); skip['class']=['v03-skip']; skip.string='Skip to content'; body.append(skip)
    header=soup.new_tag('header'); header['class']=['v03-header']; nav=soup.new_tag('nav'); nav['class']=['v03-nav']
    brand=soup.new_tag('a',href='./'); brand['class']=['v03-brand']; brand.string='SKYODOR'
    meta=soup.new_tag('span'); meta['class']=['v03-meta']; meta.string='蝶漾香韻 / ODOR'
    nav.extend([brand,meta]); header.append(nav); body.append(header)
    main=soup.new_tag('main'); main['id']='v03-content'; main['class']=['v03-main']
    hero=soup.new_tag('section'); hero['class']=['v03-hero']; left=soup.new_tag('div'); right=soup.new_tag('div')
    if hero_heading: left.append(hero_heading)
    else:
        h=soup.new_tag('h1'); h.string=title; left.append(h)
    hero_copy=soup.new_tag('div'); hero_copy['class']=['v03-hero-copy']; hero_copy.string=''
    right.append(hero_copy); hero.extend([left,right]); main.append(hero)
    content=soup.new_tag('div'); content['class']=['v03-content']
    groups=[]; current=[]
    for node in source_nodes:
        if isinstance(node,NavigableString) and not node.strip(): continue
        if getattr(node,'name',None) in ('h2','h3') and current:
            groups.append(current); current=[]
        current.append(node)
    if current: groups.append(current)
    for i,group in enumerate(groups,1): content.append(make_section(soup,group,i))
    main.append(content); body.append(main)
    footer=soup.new_tag('footer'); footer['class']=['v03-footer']; footer.string='SKYODOR · 蝶漾香韻'; body.append(footer)
    for script in scripts: body.append(script)
    soup.body.replace_with(body)
    rel=Path(os.path.relpath(css_path,start=path.parent)).as_posix()
    link=soup.new_tag('link',rel='stylesheet',href=rel); (soup.head or soup).append(link)
    soup.html['data-design-version']='v03'
    path.write_text(str(soup),encoding='utf-8')
    return True

def main():
    if not SRC.exists(): raise SystemExit('Missing site/v02; run baseline build first')
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(SRC,OUT)
    css=OUT/'assets'/'css'/'skyodor-v03.css'; css.parent.mkdir(parents=True,exist_ok=True); css.write_text(CSS,encoding='utf-8')
    count=0
    for path in OUT.rglob('*.html'):
        if build_page(path,css): count+=1
    print(f'Built refined V03 layout across {count} HTML files')
if __name__=='__main__': main()
