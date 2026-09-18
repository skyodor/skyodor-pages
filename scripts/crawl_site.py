#!/usr/bin/env python3
"""Build a resilient offline copy of skyodor.com, including lazy-loaded and CSS assets."""
from __future__ import annotations

import hashlib
import mimetypes
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.skyodor.com/"
HOST = urlparse(BASE_URL).netloc
OUT = Path("site")
TIMEOUT = 30
session = requests.Session()
session.headers.update({"User-Agent": "skyodor-pages-static-builder/4.0"})
seen_pages: set[str] = set()
asset_map: dict[str, str] = {}


def normalize(url: str) -> str:
    parsed = urlparse(urljoin(BASE_URL, url))
    return parsed._replace(fragment="").geturl()


def safe_path(url: str, default_name: str = "index.html") -> Path:
    parsed = urlparse(url)
    raw = unquote(parsed.path).strip("/")
    if not raw:
        return Path(default_name)
    parts = [p for p in raw.split("/") if p not in (".", "..")]
    path = Path(*parts)
    if parsed.path.endswith("/"):
        return path / default_name
    return path if path.suffix else path / default_name


def asset_target(url: str, content_type: str = "") -> Path:
    parsed = urlparse(url)
    path = safe_path(url, "asset")
    if not path.suffix:
        ext = mimetypes.guess_extension(content_type.split(";", 1)[0].strip()) or ".bin"
        path = path.with_name(path.name + ext)
    if parsed.query:
        digest = hashlib.sha1(parsed.query.encode()).hexdigest()[:8]
        path = path.with_name(f"{path.stem}-{digest}{path.suffix}")
    return Path("assets") / path


def download(url: str) -> tuple[bytes, str]:
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return response.content, response.headers.get("content-type", "")


def relative(from_file: Path, target: str | Path) -> str:
    return Path(os.path.relpath(str(target), start=from_file.parent)).as_posix()


def save_asset(url: str, data: bytes | None = None, content_type: str = "") -> str:
    if url in asset_map and (OUT / asset_map[url]).exists():
        return asset_map[url]
    if data is None:
        data, content_type = download(url)
    target = asset_target(url, content_type)
    destination = OUT / target
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    asset_map[url] = target.as_posix()
    if "css" in content_type.lower() or target.suffix.lower() == ".css":
        destination.write_text(rewrite_css(data.decode("utf-8", errors="replace"), url, target), encoding="utf-8")
    return target.as_posix()


def rewrite_css(text: str, source_url: str, source_file: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        raw = match.group(1).strip().strip("'\"")
        if raw.startswith(("data:", "#")):
            return match.group(0)
        absolute = normalize(urljoin(source_url, raw))
        try:
            saved = save_asset(absolute)
            return match.group(0).replace(raw, relative(source_file, saved))
        except requests.RequestException:
            print(f"Asset unavailable in CSS: {absolute}")
            return match.group(0)
    return re.sub(r"url\(([^)]+)\)", replace, text, flags=re.I)


def save_reference(raw: str, page_url: str, output: Path) -> str | None:
    if not raw or raw.strip().startswith(("data:", "mailto:", "javascript:", "#")):
        return None
    absolute = normalize(urljoin(page_url, raw.strip()))
    try:
        return relative(output, save_asset(absolute))
    except requests.RequestException:
        print(f"Asset unavailable: {absolute}")
        return None


def rewrite_inline_style(value: str, page_url: str, output: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        raw = match.group(1).strip().strip("'\"")
        if raw.startswith(("data:", "#")):
            return match.group(0)
        saved = save_reference(raw, page_url, output)
        return match.group(0).replace(raw, saved) if saved else match.group(0)
    return re.sub(r"url\(([^)]+)\)", replace, value, flags=re.I)


def rewrite_srcset(value: str, page_url: str, output: Path) -> str:
    rewritten = []
    for item in value.split(","):
        bits = item.strip().split()
        if bits:
            saved = save_reference(bits[0], page_url, output)
            if saved:
                bits[0] = saved
            rewritten.append(" ".join(bits))
    return ", ".join(rewritten)


def process_page(url: str) -> None:
    url = normalize(url)
    parsed = urlparse(url)
    if url in seen_pages or parsed.netloc != HOST or parsed.path.lower().endswith((".pdf", ".zip")):
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
    soup = BeautifulSoup(data, "html.parser")

    asset_attrs = ("src", "poster", "data-src", "data-lazy-src", "data-original", "data-bg", "data-background-image", "data-image", "data-lazy", "data-flickity-lazyload")
    for node in soup.find_all(True):
        for attr in asset_attrs:
            raw = node.get(attr)
            if raw:
                saved = save_reference(raw, url, output)
                if saved:
                    node[attr] = saved
        for attr in ("srcset", "data-srcset", "data-lazy-srcset", "data-bgset"):
            raw = node.get(attr)
            if raw:
                node[attr] = rewrite_srcset(raw, url, output)
        if node.get("style"):
            node["style"] = rewrite_inline_style(node["style"], url, output)

    for node in soup.find_all("link", href=True):
        if node.get("rel") and "stylesheet" in node.get("rel"):
            saved = save_reference(node["href"], url, output)
            if saved:
                node["href"] = saved

    for node in soup.find_all("meta", content=True):
        if node.get("property", "").lower() in {"og:image", "og:image:url", "twitter:image"}:
            saved = save_reference(node["content"], url, output)
            if saved:
                node["content"] = saved

    for node in soup.find_all("style"):
        if node.string:
            node.string = rewrite_css(node.string, url, output)

    for node in soup.find_all(href=True):
        absolute = normalize(urljoin(url, node["href"]))
        target = urlparse(absolute)
        if target.netloc == HOST and not target.path.lower().endswith((".pdf", ".zip", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".css", ".js")):
            node["href"] = relative(output, safe_path(absolute))
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
