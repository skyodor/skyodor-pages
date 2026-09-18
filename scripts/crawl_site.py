#!/usr/bin/env python3
"""Build a static, GitHub-Pages-friendly copy of skyodor.com."""
from __future__ import annotations

import hashlib
import mimetypes
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.skyodor.com/"
HOST = urlparse(BASE_URL).netloc
OUT = Path("site")
TIMEOUT = 25

session = requests.Session()
session.headers.update({"User-Agent": "skyodor-pages-static-builder/1.0"})
seen_pages: set[str] = set()
asset_map: dict[str, str] = {}


def normalize(url: str) -> str:
    p = urlparse(urljoin(BASE_URL, url))
    return p._replace(fragment="").geturl()


def safe_path(url: str, default_name: str = "index.html") -> Path:
    p = urlparse(url)
    raw = unquote(p.path).strip("/")
    if not raw:
        return Path(default_name)
    path = Path(*[part for part in raw.split("/") if part not in (".", "..")])
    if p.path.endswith("/"):
        return path / default_name
    if path.suffix:
        return path
    return path / default_name


def local_asset(url: str, content_type: str | None = None) -> Path:
    if url in asset_map:
        return Path(asset_map[url])
    p = urlparse(url)
    candidate = safe_path(url, "asset")
    if not candidate.suffix:
        ext = mimetypes.guess_extension((content_type or "").split(";")[0]) or ".bin"
        candidate = candidate.with_name(candidate.name + ext)
    # Query-string collisions get a stable suffix.
    if p.query:
        digest = hashlib.sha1(p.query.encode()).hexdigest()[:8]
        candidate = candidate.with_name(f"{candidate.stem}-{digest}{candidate.suffix}")
    rel = Path("assets") / candidate
    asset_map[url] = rel.as_posix()
    return rel


def download(url: str) -> tuple[bytes, str]:
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return response.content, response.headers.get("content-type", "")


def save_asset(url: str) -> str:
    target = local_asset(url)
    if (OUT / target).exists():
        return target.as_posix()
    data, content_type = download(url)
    target = local_asset(url, content_type)
    destination = OUT / target
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    if "css" in content_type or target.suffix.lower() == ".css":
        text = data.decode("utf-8", errors="replace")
        text = rewrite_css(text, url, target.parent)
        destination.write_text(text, encoding="utf-8")
    return target.as_posix()


def relative(from_file: Path, target: str) -> str:
    return Path(__import__("os").path.relpath(target, start=from_file.parent)).as_posix()


def rewrite_css(text: str, source_url: str, source_dir: Path) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(1).strip(" \'\"")
        if raw.startswith(("data:", "#")):
            return match.group(0)
        absolute = normalize(urljoin(source_url, raw))
        if urlparse(absolute).netloc not in (HOST, ""):
            return match.group(0)
        try:
            saved = save_asset(absolute)
            return match.group(0).replace(raw, relative(source_dir, saved))
        except requests.RequestException:
            return match.group(0)
    return re.sub(r"url\(([^)]+)\)", repl, text, flags=re.I)


def process_page(url: str) -> None:
    url = normalize(url)
    if url in seen_pages:
        return
    parsed = urlparse(url)
    if parsed.netloc != HOST or parsed.path.lower().endswith(('.pdf', '.zip')):
        return
    seen_pages.add(url)
    try:
        data, content_type = download(url)
    except requests.RequestException as exc:
        print(f"Skipping {url}: {exc}")
        return
    if "html" not in content_type and not parsed.path.endswith(("/", ".html")):
        return

    output = safe_path(url)
    output.parent.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(data, "html.parser")

    for tag, attr in [("img", "src"), ("script", "src"), ("link", "href"), ("source", "src")]:
        for node in soup.find_all(tag):
            raw = node.get(attr)
            if not raw or raw.startswith(("data:", "mailto:", "javascript:", "#")):
                continue
            absolute = normalize(urljoin(url, raw))
            if urlparse(absolute).netloc != HOST:
                continue
            try:
                saved = save_asset(absolute)
                node[attr] = relative(output, saved)
            except requests.RequestException:
                continue

    for node in soup.find_all(href=True):
        absolute = normalize(urljoin(url, node["href"]))
        if urlparse(absolute).netloc == HOST and not urlparse(absolute).path.lower().endswith(('.pdf', '.zip')):
            target = safe_path(absolute)
            node["href"] = relative(output, target)
            process_page(absolute)

    for node in soup.find_all(src=True):
        if node.name in ("img", "script", "source"):
            continue
        absolute = normalize(urljoin(url, node["src"]))
        if urlparse(absolute).netloc == HOST:
            process_page(absolute)

    destination = OUT / output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(str(soup), encoding="utf-8")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    process_page(BASE_URL)
    print(f"Built {len(seen_pages)} pages in {OUT}")


if __name__ == "__main__":
    main()
