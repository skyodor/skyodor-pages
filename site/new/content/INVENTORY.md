# Source Inventory — New Site

## Scope

- Source baseline: `site/v0.1` in this repository.
- New implementation branch: `new-site-v1`.
- Legacy baseline files are not deleted or modified.
- The new interface must consume structured source data, not copy the legacy layout.

## Confirmed source page set

| Source file | Classification | Current inventory state |
|---|---|---|
| `index.html` | Home | title, story, metadata images recorded |
| `category.html` | Category | title and image names recorded |
| `27785393213193427833393212770030ml.html` | Product | requires exact title/body extraction |
| `27785393213193427833393212770050ml.html` | Product | title and metadata description recorded |
| `27785393213193427833393212770050mlx.html` | Product | title and image names recorded |
| `21697393212998327963.html` | Page | exact extraction pending |
| `258443932122294394722640829255.html` | Page | exact extraction pending |
| `36092360232796931243.html` | Page | exact extraction pending |

## Structured records

The machine-readable source records are in `inventory.json`.

Rules:

1. Preserve original Chinese text exactly when verified.
2. Keep unknown fields empty until extracted from source.
3. Do not invent product descriptions, sizes, image captions, links, or contact details.
4. Record image filenames before attempting binary asset migration.
5. Do not mark the migration complete until page, product, asset, link, and build checks pass.

## Current blockers

- Exact body text for several source pages still needs extraction from the original HTML.
- Binary asset transfer and path verification still need to be completed.
- Internal link mapping still needs to be generated from the source HTML.
