#!/usr/bin/env python3
"""Build a deterministic asset manifest from the archived source site.

This script is intentionally read-only: it scans source HTML and records image
references, existence, byte size, and SHA-256 when files are available.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

IMAGE_RE = re.compile(r"(?:src|data-src|href)=[\"']([^\"']+\.(?:png|jpe?g|gif|webp|svg)(?:\?[^\"']*)?)[\"']", re.I)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("site/v0.1"))
    parser.add_argument("--output", type=Path, default=Path("site/new/content/asset-manifest.json"))
    args = parser.parse_args()

    records = []
    for html in sorted(args.source.rglob("*.html")):
        text = html.read_text(encoding="utf-8", errors="replace")
        for raw in sorted(set(IMAGE_RE.findall(text))):
            ref = raw.split("?", 1)[0]
            candidate = (html.parent / ref).resolve() if not ref.startswith("/") else (args.source / ref.lstrip("/")).resolve()
            try:
                candidate.relative_to(args.source.resolve())
            except ValueError:
                candidate = args.source / ref.lstrip("/")
            item = {"source_page": html.relative_to(args.source).as_posix(), "reference": ref, "exists": candidate.is_file()}
            if candidate.is_file():
                item["bytes"] = candidate.stat().st_size
                item["sha256"] = sha256(candidate)
                item["path"] = candidate.relative_to(args.source).as_posix()
            records.append(item)

    payload = {
        "schema_version": "1.0.0",
        "source_root": args.source.as_posix(),
        "generated_by": "scripts/build_new_site_asset_manifest.py",
        "asset_count": len(records),
        "missing_count": sum(not item["exists"] for item in records),
        "assets": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}: {len(records)} references, {payload['missing_count']} missing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
