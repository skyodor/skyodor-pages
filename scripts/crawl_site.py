#!/usr/bin/env python3
"""Build an offline copy of the Weebly site with local assets."""
from __future__ import annotations
import hashlib, mimetypes, os, re, shutil
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.skyodor.com/'
HOST = urlparse(BASE_URL).netloc
OUT = Path('site')
TIMEOUT = 30
session = requests.Session()
session.headers['User-Agent'] = 'skyodor-pages-static-builder/5.0'
seen_pages, asset_map, failed = set(), {}, set()

def normalize(value, base=BASE_URL):
    p = urlparse(urljoin(base, value))._replace(fragment='')
    return p.geturl()

def safe_path(url, default='index.html'):
    p = urlparse(url); raw = unquote(p.path).strip('/')
    if not raw: return Path(default)
    parts = [x for x in raw.split('/') if x not in ('.', '..')]
    result = Path(*parts)
    return result / default if p.path.endswith('/') else (result if result.suffix else result / default)

def target_for(url, content_type=''):
    p = safe_path(url, 'asset')
    if not p.suffix:
        p = p.with_name(p.name + (mimetypes.guess_extension(content_type.split(';')[0].strip()) or '.bin'))
    q = urlparse(url).query
    if q: p = p.with_name(f'{p.stem}-{hashlib.sha1(q.encode()).hexdigest()[:8]}{p.suffix}')
    return Path('assets') / p

def download(url):
    candidates = [url]
    parsed = urlparse(url)
    if parsed.netloc == 'www.skyodor.com':
        candidates.append(parsed._replace(netloc='skyodor.com').geturl())
    for candidate in candidates:
        try:
            r = session.get(candidate, timeout=TIMEOUT); r.raise_for_status()
            return r.content, r.headers.get('content-type','')
        except requests.RequestException:
            pass
    raise requests.RequestException(url)

def relative(source, target):
    return Path(os.path.relpath(str(target), start=Path(source).parent)).as_posix()

def save_asset(url, data=None, content_type=''):
    if url in asset_map and (OUT / asset_map[url]).exists(): return asset_map[url]
    if data is None: data, content_type = download(url)
    target = target_for(url, content_type); dest = OUT / target
    dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(data)
    asset_map[url] = target.as_posix()
    if 'css' in content_type.lower() or target.suffix.lower() == '.css':
        dest.write_text(rewrite_css(data.decode('utf-8','replace'), url, target), encoding='utf-8')
    return target.as_posix()

def rewrite_css(text, source_url, source_file):
    def repl(m):
        raw = m.group(1).strip().strip("'\"")
        if raw.startswith(('data:', '#')): return m.group(0)
        absolute = normalize(raw, source_url)
        try: saved = save_asset(absolute); return m.group(0).replace(raw, relative(source_file, saved))
        except requests.RequestException:
            return m.group(0)
    return re.sub(r'url\(([^)]+)\)', repl, text, flags=re.I)

def reference(raw, page_url, output):
    if not raw or raw.strip().startswith(('data:','mailto:','javascript:','#')): return None
    absolute = normalize(raw.strip(), page_url)
    try: return relative(output, save_asset(absolute))
    except requests.RequestException:
        if absolute not in failed:
            failed.add(absolute); print(f'Asset unavailable: {absolute}')
        return None

def srcset(value, page_url, output):
    result=[]
    for item in value.split(','):
        bits=item.strip().split()
        if bits:
            saved=reference(bits[0],page_url,output)
            if saved: bits[0]=saved
            result.append(' '.join(bits))
    return ', '.join(result)

def process(url):
    url=normalize(url)
    p=urlparse(url)
    if url in seen_pages or p.netloc != HOST or p.path.lower().endswith(('.pdf','.zip')): return
    seen_pages.add(url)
    try: data, ctype=download(url)
    except requests.RequestException as e: print(f'Skipping {url}: {e}'); return
    if 'html' not in ctype and not p.path.endswith(('/', '.html')): return
    output=safe_path(url); soup=BeautifulSoup(data,'html.parser')
    attrs=('src','poster','data-src','data-lazy-src','data-original','data-bg','data-background-image','data-image','data-lazy','data-flickity-lazyload')
    for node in soup.find_all(True):
        for attr in attrs:
            saved=reference(node.get(attr),url,output)
            if saved: node[attr]=saved
        for attr in ('srcset','data-srcset','data-lazy-srcset','data-bgset'):
            if node.get(attr): node[attr]=srcset(node[attr],url,output)
        if node.get('style'):
            node['style']=rewrite_css(node['style'],url,output)
    for node in soup.find_all('link',href=True):
        rel=[str(x).lower() for x in node.get('rel',[])]
        if 'stylesheet' in rel:
            saved=reference(node['href'],url,output)
            if saved: node['href']=saved
    for node in soup.find_all('meta',content=True):
        prop=str(node.get('property') or node.get('name') or '').lower()
        if prop in {'og:image','og:image:url','twitter:image'}:
            saved=reference(node['content'],url,output)
            if saved: node['content']=saved
    for node in soup.find_all('style'):
        if node.string: node.string=rewrite_css(node.string,url,output)
    for node in soup.find_all('a',href=True):
        absolute=normalize(node['href'],url); target=urlparse(absolute)
        if target.netloc==HOST and not target.path.lower().endswith(('.pdf','.zip','.jpg','.jpeg','.png','.gif','.webp','.svg','.css','.js')):
            node['href']=relative(output,safe_path(absolute)); process(absolute)
    dest=OUT/output; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(str(soup),encoding='utf-8')

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True); process(BASE_URL); print(f'Built {len(seen_pages)} pages in {OUT}')

if __name__ == '__main__': main()
