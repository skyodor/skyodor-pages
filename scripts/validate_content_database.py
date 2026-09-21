#!/usr/bin/env python3
"""Validate the new site's structured content database without publishing it."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "site/new/content/content-database.json"
SCHEMA = ROOT / "site/new/content/content-database.schema.json"


def main() -> int:
    database = json.loads(DB.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = schema.get("required", [])
    missing = [key for key in required if key not in database]
    if missing:
        raise SystemExit(f"Missing required top-level fields: {', '.join(missing)}")
    if database.get("database_name") != "skyodor_content":
        raise SystemExit("Unexpected database_name")
    entities = database.get("entities", {})
    for group_name, records in entities.items():
        if isinstance(records, list):
            for record in records:
                for field in ("id", "entity_type", "source_refs", "updated_at"):
                    if field not in record:
                        raise SystemExit(f"{group_name}: record missing {field}: {record.get('id', '<unknown>')}")
    print("content database: valid structure")
    print(f"entity groups: {len(entities)}")
    print(f"relationships: {len(database.get('relationships', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
