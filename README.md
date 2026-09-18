# Skyodor Pages

This repository builds a static copy of [skyodor.com](https://www.skyodor.com/) and deploys it to GitHub Pages.

## Deployment

Pushes to `main` trigger `.github/workflows/pages.yml`. The workflow crawls the source site, rewrites same-origin links and assets to local paths, and deploys the generated `site/` directory.

If deployment is blocked, open **Settings → Pages** and set **Build and deployment → Source** to **GitHub Actions**.

> Note: pages that depend on server-side APIs, authentication, or dynamic JavaScript may require additional manual adaptation after the static build.
