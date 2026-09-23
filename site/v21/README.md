# ODOR 新網站

This directory is the standalone new-site implementation under `site/new`.

## Completed in this migration pass

- Original source asset tree is available under `site/new/assets/`.
- Homepage uses verified source wording and original source imagery.
- Unverified descriptive copy was removed from the brand page.
- Responsive navigation and image sections are implemented without an external font/CDN dependency.
- Local-reference validation is available through `scripts/validate_new_site.py`.
- Legacy directories are not used as runtime dependencies by the new site.

## Scope

The new site remains separate from the legacy versions. The existing `v03` files and build process are intentionally untouched.

Product/purchase presentation remains subject to the existing source-verification and publication rules; no missing source information is invented.
