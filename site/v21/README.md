# ODOR v2.1 — Portable Static Website

This directory is the authoritative v2.1 static-site implementation.

## Architecture

- Completely static HTML, CSS, JavaScript and local assets.
- Internal pages and assets use relative paths.
- No Weebly, WordPress, database, CMS, GitHub Pages, or domain dependency at runtime.
- The complete v2.1 directory can be copied to another host or directory and served as a standalone website.
- Source assets are contained under `assets/`; source/content records are retained under `content/`.

## Validation

The deployment workflow validates `site/v21` for missing local references and checks for hard-coded deployment/domain paths before publishing.

## Deployment

GitHub Pages is only one hosting destination. It is not part of the v2.1 runtime architecture.

## Content policy

Existing source content and imagery are retained where verified. Missing or uncertain source information is not silently invented.
