# Skyodor Content Database

## Files

- `content-database.json`: canonical source catalog with provenance and verification state.
- `content-database.schema.json`: JSON Schema for structural validation.
- `content-database.sql`: normalized relational schema for production implementation.

## Publication gates

A record may be marked `approved` only after:

1. Its source file is identified.
2. Text, title, metadata, and price are checked against the source.
3. Every referenced image has a verified filename and binary checksum.
4. Internal and external links are checked.
5. The record passes JSON Schema validation.
6. The new page renders without broken asset or navigation references.

## Data rules

- Do not invent missing text, prices, product details, images, or links.
- Use `null` for unknown or unextracted values.
- Preserve Traditional Chinese source wording when verified.
- Keep source paths and provenance on every record.
- Keep legacy site files untouched.
- Keep unverified records in `draft` or `review`; never publish them automatically.

## Current implementation state

The catalog structure is present, but source extraction and binary asset verification are still separate migration tasks. This file is documentation, not a claim that the migration is complete.
