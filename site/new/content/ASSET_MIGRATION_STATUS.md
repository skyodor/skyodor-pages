# Asset Migration Status

**Branch:** `new-site-v1`  
**Status:** Source-reference manifest tooling added; binary asset verification is not yet marked complete.

## Verification rules

- Every source image reference must be cataloged.
- A referenced file must be checked for existence in the archived source tree.
- Available files must receive byte size and SHA-256 values.
- Missing or externally hosted assets remain unresolved; they must not be replaced with generated imagery.
- The new site must not publish an asset as verified until its source path and binary are confirmed.

## Run locally

```bash
python3 scripts/build_new_site_asset_manifest.py
```

The generated `site/new/content/asset-manifest.json` is an audit artifact and must be reviewed before release. This commit adds the scanner and status documentation only; it does not claim that the complete binary migration has been finished.
