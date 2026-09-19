# ODOR Website v1.1

## Release intent

Version 1.1 introduces a new editorial homepage design while preserving the original crawled website content as a reference set.

## Content lock

- Original website snapshot is retained at `site/v1.1/legacy/`.
- The legacy directory uses the existing v0.1 Git tree content; original files are not rewritten by the homepage redesign.
- New presentation files are isolated at `site/v1.1/index.html` and `site/v1.1/styles.css`.
- Existing product/detail pages remain accessible through homepage links into `legacy/`.
- New homepage copy is presentation text only; the legacy snapshot remains the source reference for original content.

## Verification and fixes

- [x] v1.1 branch exists.
- [x] Original v0.1 tree preserved under `site/v1.1/legacy/`.
- [x] Homepage and stylesheet are isolated from the legacy crawl.
- [x] Homepage links point to legacy pages within the v1.1 tree.
- [x] Added skip navigation link for keyboard users.
- [x] Added visible focus styles for interactive elements.
- [x] Added responsive grid safeguards for narrow screens.
- [x] Added background-color fallbacks for image-backed sections.
- [x] Added reduced-motion support.
- [x] Added theme-color metadata.
- [ ] Browser screenshot test in the deployment environment.
- [ ] Production-domain cutover verification.

## Known scope limits

This is a static v1.1 presentation layer. Checkout, inventory, forms, analytics, SEO redirects, and production-domain routing must be verified separately before cutover. The repository connector can verify committed source files and referenced paths, but it does not provide a browser rendering session here.

## Deployment check

The v1.1 deployment workflow is the authoritative publishing path for this version and is triggered by changes on the `v1.1` branch.
