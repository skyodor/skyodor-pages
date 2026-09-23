#!/usr/bin/env python3
"""Audit v2.1 for exact duplicate image binaries.

Images are grouped by SHA-256. Duplicate binaries are an error unless they are
outside site/v21. The report also records the canonical path and every duplicate
path so references can be consolidated before retirement.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".bmp", ".tif", ".tiff", ".svg"}
TEXT_EXTS = {".html", ".htm", ".css", ".js", ".json", ".md", ".txt", ".xml"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    args = ap.parse_args()
    root = args.root.resolve()

    groups: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            groups.setdefault(sha256(path), []).append(path)

    dupes = {digest: sorted(paths) for digest, paths in groups.items() if len(paths) > 1}
    print(f"v2.1 image files: {sum(len(v) for v in groups.values())}")
    print(f"v2.1 unique image binaries: {len(groups)}")
    print(f"v2.1 duplicate binary groups: {len(dupes)}")

    if not dupes:
        print("v2.1 exact image deduplication: PASS")
        return 0

    for digest, paths in sorted(dupes.items()):
        print(f"DUPLICATE SHA-256 {digest}")
        for p in paths:
            print(f"  - {p.relative_to(root).as_posix()}")

    print("ERROR: v2.1 contains exact duplicate image binaries; consolidate references and retire duplicates.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
