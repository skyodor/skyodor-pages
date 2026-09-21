# Skyodor WordPress Export

Source: https://www.skyodor.com/
Destination: `main/wp-export/`

## Package status

This package is a **structured migration baseline**, not a claim of a complete binary mirror. The existing source inventory confirms page routes, product data, and known image filenames, while binary asset transfer remains pending.

## Files

- `wordpress-import.xml`: WXR-compatible import baseline containing catalogued pages and products.
- `migration-report.md`: verification status, limitations, and required follow-up.
- `media/` and `static-assets/`: reserved for verified binary assets and source CSS/JS when available.

## Import notes

1. In WordPress, use Tools → Import → WordPress.
2. Import `wordpress-import.xml`.
3. Do not delete the existing site until media, links, styling, and JavaScript have been manually verified.
4. Upload verified media separately and update image references as required.
