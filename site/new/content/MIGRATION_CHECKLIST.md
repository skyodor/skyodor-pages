# New Site Migration Checklist

Branch: `new-site-v1`
Content lock: `CONTENT_LOCK.md`

## Source coverage

- [ ] Enumerate every source HTML route from `site/v0.1`
- [ ] Extract and verify complete page text
- [ ] Reconcile all products, prices, sizes, and descriptions
- [ ] Map all source navigation and external links

## Assets

- [ ] Enumerate every referenced image and gallery asset
- [ ] Copy binary assets into the new site asset tree
- [ ] Verify file existence, dimensions, and checksums
- [ ] Check every rendered image for broken paths or distortion

## New implementation

- [ ] Replace the current partial homepage with the completed new layout
- [ ] Build complete product listing and detail routes
- [ ] Rebuild every verified source page using the new design system
- [ ] Add responsive desktop, tablet, and mobile layouts
- [ ] Add keyboard-accessible navigation and focus states
- [ ] Preserve verified metadata without adding unsupported claims

## Validation

- [ ] Validate JSON content database against schema
- [ ] Validate source-to-new content coverage
- [ ] Validate internal and external links
- [ ] Validate image references
- [ ] Run production build
- [ ] Inspect generated output for placeholders, old-version links, and broken assets
- [ ] Perform browser checks at desktop, tablet, and mobile widths

## Release

- [ ] Configure isolated deployment for the new site
- [ ] Verify deployment HTTP responses and nested routes
- [ ] Verify the live URL
- [ ] Merge only after all blocking checks pass

No item may be marked complete without direct verification.
