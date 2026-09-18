# Skyodor Pages

This repository builds a static copy of [skyodor.com](https://www.skyodor.com/) and deploys it to **GitHub Pages**.

## Deployment

The GitHub Actions workflow runs on pushes to `main` and deploys the generated `site/` directory to GitHub Pages.

Enable GitHub Pages in **Repository → Settings → Pages** and select **GitHub Actions** as the source if required.

The workflow is in `.github/workflows/pages.yml`.

> Note: pages that depend on server-side APIs, authentication, or dynamic JavaScript may require additional manual adaptation after the static build.
