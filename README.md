# Skyodor Pages

This repository builds a static copy of [skyodor.com](https://www.skyodor.com/) and deploys it to **Cloudflare Pages**.

## Cloudflare setup

The GitHub Actions workflow runs on pushes to `main` and deploys the generated `site/` directory to the Cloudflare Pages project named `skyodor-pages`.

Add these repository secrets in **GitHub → Settings → Secrets and variables → Actions**:

- `CLOUDFLARE_API_TOKEN`: Cloudflare API token with Pages deployment permissions.
- `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare account ID.

Create the Cloudflare Pages project first, using the project name `skyodor-pages`. The workflow is in `.github/workflows/cloudflare-pages.yml`.

> Note: pages that depend on server-side APIs, authentication, or dynamic JavaScript may require additional manual adaptation after the static build.
