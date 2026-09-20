# Source Inventory — New Site

## Scope

- Source baseline: `site/v0.1` in this repository.
- New implementation branch: `new-site-v1`.
- Legacy baseline files are not deleted or modified.
- The new interface must consume structured source data, not copy the legacy layout.

## Inventory result

The source catalog has been expanded from the initial partial list. It now records:

- All 8 archived HTML routes in `site/v0.1`.
- The complete source navigation order, including the Facebook external link.
- The catalog groups found in the 30ml source page: C1–C9, L1–L6, P1–P13, S1–S8 and N1–N6.
- Verified product names, package sizes and listed TWD prices where present in the source HTML.
- Other offerings from the `品香生活` and `擴香圖騰木片` pages.
- Verified image filenames for the cataloged pages.
- Verified brand labels used by the new site: `剎那與永恆`, `沉香`, `合香與調香`, and the original opening instruction.

## Source pages

| Source file | Title | State |
|---|---|---|
| `index.html` | 蝶漾香韻 | identified |
| `category.html` | 蝶漾香韻大香 | identified |
| `27785393213193427833393212770030ml.html` | 沉香精油香水30ml | cataloged: C/L/P/S/N groups and source image filenames |
| `27785393213193427833393212770050ml.html` | 關聖帝君沉香50ml | identified |
| `27785393213193427833393212770050mlx.html` | 沉香精油香水50mlx | identified |
| `21697393212998327963.html` | 品香生活 | cataloged: visible copy and image filenames |
| `258443932122294394722640829255.html` | 擴香圖騰木片 | cataloged: visible copy and image filenames |
| `36092360232796931243.html` | 購買流程 | identified: title, description and image filenames |

## Structured records

The machine-readable source records are in `inventory.json`.

Rules:

1. Preserve original Chinese text exactly when verified.
2. Keep unsupported fields empty; do not invent missing source data.
3. Do not invent product descriptions, sizes, image captions, links, or contact details.
4. Record source image filenames before binary asset migration.
5. Do not mark the website migration complete until asset transfer, link validation, build checks and live deployment verification pass.

## Remaining implementation work

- Copy the source binary assets into a self-contained new-site asset directory and verify every referenced file.
- Finish the new layout using the structured inventory without linking to old-version layouts.
- Add the remaining source page content and product detail views using the verified records.
- Generate and run link, missing-asset and HTML validation checks.
- Add a deployment path for the new site and verify the live URL before claiming completion.
