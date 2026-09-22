#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import shutil
import re

SRC = Path("site/v0.1")
OUT = Path("site/v03")

PAGES = [
    "index.html",
    "category.html",
    "27785393213193427833393212770030ml.html",
    "27785393213193427833393212770050mlx.html",
    "27785393213193427833393212770050ml.html",
    "21697393212998327963.html",
    "258443932122294394722640829255.html",
    "36092360232796931243.html",
]

NAV = [
    ("index.html", "蝶漾香韻"),
    ("27785393213193427833393212770030ml.html", "沉香精油香水30ml"),
    ("27785393213193427833393212770050mlx.html", "沉香精油香水50mlx"),
    ("27785393213193427833393212770050ml.html", "沉香精油香水50ml"),
    ("21697393212998327963.html", "品香生活"),
    ("258443932122294394722640829255.html", "擴香圖騰木片"),
    ("36092360232796931243.html", "購買流程"),
    ("category.html", "Category"),
]

CSS = r"""
:root{--bg:#f5f1e9;--ink:#20221f;--muted:#6f716a;--line:#d9d2c6;--accent:#8b6b4b;--dark:#252922;--max:1440px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.8 ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans TC",sans-serif}
a{color:inherit}img{display:block;max-width:100%;height:auto}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;z-index:50;background:#fff;padding:.75rem 1rem}
.site-header{position:sticky;top:0;z-index:20;background:rgba(245,241,233,.96);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav{max-width:var(--max);margin:auto;padding:18px clamp(20px,5vw,72px);display:flex;align-items:center;gap:28px}
.brand{display:flex;align-items:baseline;gap:12px;text-decoration:none;margin-right:auto}.brand strong{font:600 1rem/1 ui-serif,Georgia,serif;letter-spacing:.2em}.brand span{font-size:.78rem;color:var(--muted)}
.nav-links{display:flex;flex-wrap:wrap;gap:18px 24px;font-size:.76rem}.nav-links a{text-decoration:none;padding:6px 0;border-bottom:1px solid transparent}.nav-links a:hover,.nav-links a[aria-current=page]{border-color:var(--accent);color:var(--accent)}
.menu{display:none;border:0;background:none;font-size:1.1rem}.hero{max-width:var(--max);margin:auto;display:grid;grid-template-columns:1.1fr .9fr;min-height:72vh;border-bottom:1px solid var(--line)}
.hero-copy{padding:clamp(60px,9vw,130px) clamp(20px,6vw,90px)}.eyebrow{font-size:.68rem;letter-spacing:.18em;color:var(--accent);text-transform:uppercase}
.hero h1,.page-title{font:500 clamp(3.4rem,8vw,8.5rem)/.98 ui-serif,Georgia,"Noto Serif TC",serif;letter-spacing:-.04em;margin:40px 0 28px}.hero h1 span{color:var(--accent)}
.hero-lead{max-width:720px;color:#55584f;font-family:ui-serif,Georgia,"Noto Serif TC",serif;font-size:1.05rem}.cta{display:inline-flex;gap:22px;align-items:center;margin-top:28px;padding:12px 18px;border:1px solid var(--ink);text-decoration:none;font-size:.78rem}.cta:hover{background:var(--ink);color:var(--bg)}
.hero-visual{position:relative;min-height:520px;background:linear-gradient(145deg,#d8c9b2,#7d806d 52%,#30382f);overflow:hidden}.hero-visual img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55;filter:saturate(.65)}.hero-visual:after{content:"";position:absolute;inset:10%;border:1px solid rgba(255,255,255,.42);transform:rotate(8deg)}
.hero-mark{position:absolute;inset:0;display:grid;place-items:center;color:#f7f1e7;font:500 clamp(7rem,18vw,15rem)/.7 ui-serif,Georgia,serif;z-index:1}.hero-meta{position:absolute;left:24px;top:24px;color:#fff;z-index:2;font-size:.65rem;letter-spacing:.18em;writing-mode:vertical-rl}
.content{max-width:var(--max);margin:auto;padding:0 clamp(20px,6vw,90px)}.source-content{padding:clamp(48px,7vw,100px)}.source-content>div{max-width:1000px;margin:auto}
.source-content h2{font:500 clamp(2rem,4.5vw,4.5rem)/1.08 ui-serif,Georgia,"Noto Serif TC",serif;letter-spacing:-.035em;margin:4rem 0 1rem}.source-content h3{font:500 1.5rem/1.25 ui-serif,Georgia,"Noto Serif TC",serif;margin:2.5rem 0 .8rem}
.source-content p{max-width:78ch;margin:1rem 0}.source-content img{margin:1.6rem auto;max-height:720px;object-fit:contain;background:#eee8dc}.source-content table{width:100%;border-collapse:collapse;overflow:auto;display:block}.source-content th,.source-content td{border-bottom:1px solid var(--line);padding:12px;text-align:left}
.source-content blockquote{border-left:3px solid var(--accent);margin:1.5rem 0;padding:.8rem 1.2rem;background:#ebe4d8}.source-content ul,.source-content ol{padding-left:1.4rem}
.source-note{max-width:var(--max);margin:auto;padding:16px clamp(20px,6vw,90px);font-size:.68rem;letter-spacing:.08em;color:var(--muted);border-top:1px solid var(--line)}
.site-footer{background:var(--dark);color:#f5f1e9;padding:34px clamp(20px,6vw,90px);display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}.site-footer a{color:#f5f1e9}
@media(max-width:820px){.nav{padding:16px 20px}.menu{display:block}.nav-links{display:none;position:absolute;left:0;right:0;top:64px;background:var(--bg);padding:20px;flex-direction:column;border-bottom:1px solid var(--line)}.nav-links.open{display:flex}.hero{grid-template-columns:1fr}.hero-visual{min-height:430px}.hero-copy{padding:60px 20px}.content{padding:0 20px}.source-content{padding:45px 0}.site-footer{padding:28px 20px;display:block}.site-footer>*{margin:.4rem 0}.page-title{font-size:clamp(3rem,14vw,6rem)}}
"""

JS = """const menu=document.querySelector('.menu');const links=document.querySelector('.nav-links');if(menu&&links){menu.addEventListener('click',()=>{const open=links.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});}"""

def clean_source_content(soup):
    root = soup.select_one("#wsite-content")
    if not root:
        return "<p>Source content could not be extracted.</p>"
    for node in root.select("script,style,noscript,form,#customer-accounts-app,.wsite-footer"):
        node.decompose()
    for node in root.select("[style]"):
        del node["style"]
    for node in root.select("[class]"):
        del node["class"]
    for node in root.select("[id]"):
        del node["id"]
    html = str(root)
    html = re.sub(r'([?&])utm_source=chatgpt\.com(?:&[^"\']*)?', '', html, flags=re.I)
    return html

def first_image(soup):
    node = soup.select_one("#wsite-content img[src]")
    return node.get("src") if node else ""

def page_title(soup, fallback):
    return soup.title.get_text(" ", strip=True) if soup.title else fallback

def nav_html(current):
    return "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>'
        for href, label in NAV
    )

def make_page(filename):
    soup = BeautifulSoup((SRC / filename).read_text(encoding="utf-8", errors="replace"), "html.parser")
    title = page_title(soup, filename)
    body = clean_source_content(soup)
    img = first_image(soup)
    hero = ""
    if filename == "index.html":
        hero = f"""<section class="hero"><div class="hero-copy"><p class="eyebrow">ODOR / 蝶漾香韻</p>
<h1>剎那<br><span>與永恆</span></h1>
<div class="hero-lead">我們總是對於剎那間會消失的，抱持一種特有的感情，想要留住也害怕失去，也之所以會更珍惜，而花便是古時詩人寄情與此的典型代表，它可豔麗、可清新、可哀傷、可短暫，一如我們所要表達的氣味，而蝶之守護也讓我們記住也留住瞬間的永恆。</div>
<a class="cta" href="27785393213193427833393212770030ml.html">探索產品 ↗</a></div>
<div class="hero-visual">{f'<img src="{img}" alt="" loading="eager">' if img else ''}
<div class="hero-meta">ODOR / 01</div><div class="hero-mark" aria-hidden="true">蝶漾</div></div></section>"""
    else:
        hero = f'<main id="main" class="content"><p class="eyebrow">ODOR / SOURCE PAGE</p><h1 class="page-title">{title}</h1></main>'
    return f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{title}｜ODOR 蝶漾香韻"><title>{title}｜ODOR 蝶漾香韻</title>
<link rel="stylesheet" href="assets/css/site-v03.css"></head><body><a class="skip" href="#main">跳至內容</a>
<header class="site-header"><div class="nav"><a class="brand" href="index.html"><strong>ODOR</strong><span>蝶漾香韻</span></a>
<button class="menu" type="button" aria-label="開啟選單" aria-expanded="false">☰</button><nav class="nav-links" aria-label="主要導覽">{nav_html(filename)}</nav></div></header>
{hero}<main id="main" class="content"><div class="source-content"><div>{body}</div></div></main>
<div class="source-note">來源內容與圖片逐項遷移；本頁改造呈現介面，不新增來源未提供的商業資訊。</div>
<footer class="site-footer"><span>ODOR 蝶漾香韻</span><a href="index.html">返回首頁 ↗</a></footer>
<script src="assets/js/site-v03.js"></script></body></html>"""

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "assets", OUT / "assets")
    (OUT / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "js").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "css" / "site-v03.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "js" / "site-v03.js").write_text(JS, encoding="utf-8")
    for page in PAGES:
        (OUT / page).write_text(make_page(page), encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Skyodor V03\n\nNew editorial presentation built from the verified archived source pages and original image assets. Legacy versions remain untouched.\n",
        encoding="utf-8",
    )
    print(f"Built {len(PAGES)} V03 pages with copied source assets.")

if __name__ == "__main__":
    main()
