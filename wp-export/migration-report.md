# Migration verification report

## Verified

- Destination repository: `skyodor/skyodor-pages`
- Destination branch: `main`
- Destination directory: `/wp-export`
- Source domain: `www.skyodor.com`
- Catalogued source pages: home, category, product pages, 品香生活, 擴香圖騰木片, and 購買流程.
- Catalogued product names, sizes, prices, and known image filenames are available in `site/new/content/inventory.json` on branch `new-site-v1`.

## Limitations

- The inventory explicitly records that binary asset transfer is pending.
- This initial package does not claim that all original images, CSS, JavaScript, checkout behavior, or third-party integrations have been mirrored.
- The duplicate product code `NO.N5` is preserved as catalogued and requires business-side confirmation before final WooCommerce import.

## Required before production use

1. Retrieve and checksum every source image and verify it against the catalogued filename list.
2. Capture and validate source CSS and JavaScript dependencies.
3. Convert products into the chosen WordPress/WooCommerce data model.
4. Test internal links, responsive layout, image loading, forms, external links, and purchase instructions.
5. Perform a test import into a staging WordPress site before production.
