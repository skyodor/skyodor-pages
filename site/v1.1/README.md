# ODOR Website v1.1

## Release intent

Version 1.1 introduces a new editorial homepage design while preserving the original crawled website content as an immutable reference set.

## Content lock

- Original website snapshot is retained at `site/v1.1/legacy/`.
- The legacy directory is linked to the existing `site/v0.1` Git tree, so the original files and assets remain available without rewriting them.
- New presentation files are isolated at `site/v1.1/index.html` and `site/v1.1/styles.css`.
- Existing product/detail pages remain accessible through the homepage links into `legacy/`.
- No original v0.1 files are deleted or overwritten by this release.

## Verification checklist

- [x] v1.1 branch created from `main`.
- [x] Original v0.1 tree preserved under `site/v1.1/legacy/`.
- [x] Responsive homepage added.
- [x] Original content routes linked from the new homepage.
- [x] Styling isolated from the legacy crawl.
- [ ] Browser screenshot test in the deployment environment.
- [ ] Final production domain cutover after stakeholder approval.

## Scope note

This is a static v1.1 presentation layer. Checkout, inventory, forms, analytics, and SEO redirects should be verified separately before production cutover.
