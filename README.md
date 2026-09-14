# Jiaqi Liu — local website reconstruction

A static, locally runnable reconstruction of the saved public jiaqiliu.com site. This continues the existing migration: 21 routes, original page content and responsive styling, localized images/fonts/CV, and shared local gallery/navigation behavior.

The live Wix website, DNS, domain, and production hosting are untouched. Nothing has been deployed. Visual equivalence and interactive playback are still awaiting browser acceptance.

## Requirements

Python 3.9 (the verified runtime), BeautifulSoup 4.11.1, and lxml 4.9.1. No Node toolchain, framework, or runtime web server dependency is required. Python's standard HTTP server is sufficient for preview.

If the Python packages are not already installed:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Dependency installation needs a package source; subsequent site builds use only saved local files and never fetch assets or pages.

## Build and preview

Run these commands from this project root:

```sh
python3 scripts/build.py
python3 scripts/preview.py
```

Open **http://127.0.0.1:4175/**. Stop the server with Ctrl+C. The host and port are defined once in `data/preview.json`; do not run two previews on the same port. Root-relative asset URLs require HTTP preview, not opening HTML via `file://`.

The build runs in a fresh staging directory, validates it, and only then replaces `dist/`. A prior `dist/` is moved into `work/previous-builds/`. On failure the existing output is retained. Do not edit generated HTML/CSS/JS inside `dist/`.

To build separately without replacing `dist/`:

```sh
python3 scripts/build.py --output work/my-review-build
```

Choose a new directory under `work/`; an existing review directory is never overwritten.

## Validation

```sh
python3 scripts/validate.py
python3 scripts/validate.py --http
python3 scripts/check_reproducibility.py
```

The first command checks files without a running server. `--http` additionally compares all 21 served pages with the generated files at the canonical preview URL. Validation never changes `dist/`; reports print to stdout. The reproducibility check builds twice in temporary directories, compares every output file by SHA-256, verifies validation is read-only, and removes those temporary builds afterward.

Validation covers route completeness, non-empty local href/src/poster/data-full/CSS references, internal anchors, asset checksums, CV compatibility, exact external video embed references, developer/temporary path leaks, and the preserved text/image/gallery/link contract. It cannot establish pixel equivalence or third-party playback availability.

## Organization

| Directory/file | Purpose |
| --- | --- |
| `source/` | Authored shared CSS and JavaScript |
| `scripts/` | Offline build, layout generation, preview, validation, inventory and reproducibility tools |
| `data/captures/` | Saved desktop/mobile HTML and Wix page data; immutable migration inputs |
| `data/model.json`, `data/sitemap.xml` | Saved route/source metadata |
| `data/assets.json`, `data/routes.json` | Authoritative asset and route inventories |
| `data/render-contract.json` | Pre-cleanup content/structure contract, adjusted only for asset paths |
| `data/audits/` | Historical previous-session reports; not current validation results |
| `assets/` | Verified source images, fonts and document; retained hashed basenames |
| `docs/` | Route catalog, asset inventory, migration decisions and QA checklist |
| `dist/` | Complete generated static website |
| `work/` | Recoverable baseline archive, previous builds, temporary analysis and reports |
| `outputs/site/` | Compatibility entry point for the previous preview path; `dist` points to the current build |

To refresh the route/asset documentation after an intentional inventory change:

```sh
python3 scripts/inventory.py
```

Read [routes](docs/routes.md), [assets](docs/assets.md), and [migration notes](docs/migration-notes.md) before changing page behavior. Captured component IDs and page-specific responsive rules are intentional preservation decisions.

## UI and asset cleanup

Six obsolete film pages and their 43 exclusive images were removed. Retained images use readable filenames; `docs/image-path-mapping.json` records every rename. The homepage caption style now matches the captured below-image Avenir rule. Desktop navigation keeps Projects/Info with a 40px gap; the mobile menu remains separate. The Instagram control has explicit 30px dimensions rather than relying on the removed Wix image runtime.

Optional rendered-layout verification uses an already installed Playwright/Chrome:

```sh
node scripts/check_layout.cjs
```

Set `PLAYWRIGHT_MODULE` to your installed module path if it is not resolvable normally. This check does not install or download a browser.

## Recovery

`work/backups/migration-before-cleanup.tar.gz` contains the complete pre-cleanup `outputs/` and `work/` content. Extract it into a **separate recovery directory**, not over this project. The original output is also retained under `work/baseline-site/`. The pre-UI state is also committed locally as `1b2a258`. No Git remote or publication configuration was created.
