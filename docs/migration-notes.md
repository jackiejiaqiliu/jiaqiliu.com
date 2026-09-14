# Migration notes

## Architecture and preserved work

This remains a small Python-generated static website, not a framework rewrite. `scripts/build.py` reads the saved desktop HTML, saved Wix warmup/page data, router model, and verified local asset inventory. `scripts/layout.py` retains the prior gallery measurement logic using saved mobile/desktop captures. Authored files in `source/` are copied into the build. Generation is offline; unknown CDN assets fail explicitly rather than initiating downloads.

Original content, semantic links, page DOM/component IDs, inline responsive CSS, canonical URLs, Open Graph/Twitter metadata, and SVG casing are preserved. The original home-page JSON-LD is now retained as inert structured metadata; the previous generator removed it along with all scripts. Wix runtime scripts are not included. Captured rich text, images, gallery ordering, and navigation links are checked against a contract derived from the pre-cleanup output.

## Custom behavior and intentional substitutions

- Linked index galleries are local anchors; artwork galleries use buttons with full-image URLs and a shared native dialog lightbox. Previous/next controls, arrow keys, Escape, and focus return are preserved.
- The mobile menu keeps the captured Wix DOM, CSS open-state class, inert/ARIA state handling, Escape, and focus cycling. Obsolete `.local-menu` CSS from the discarded menu implementation was removed.
- Gallery layout is generated separately for desktop and mobile at the existing 750/751px breakpoint. The 17 gallery configurations preserve individual columns, gaps, image ratios/cropping, and caption padding. Other page-specific responsive rules remain in original inline CSS.
- Shared CSS changes are limited to the dead menu rules and caption declarations demonstrably superseded later in the cascade. Page-specific overrides retain their order. JavaScript was formatted and named for readability without changing behavior.
- The `/fullscreen-page` captured utility route remains; gallery enlargement uses the existing local dialog, not Wix's gallery runtime. `/projects` remains a byte-identical home alias.
- Three Vimeo and two YouTube embeds, the Oblivio YouTube link, and other editorial/social/project links remain external. Exact embed references are verified locally; external availability/playback is not asserted.

## Assets and cleanup

All 148 original localized asset byte streams are retained. URL-hash basenames are unchanged. Images are grouped by identifiable owning page or shared use; fonts and the PDF have their own directories. All mappings are programmatic. The original CV public path is generated as an intentional identical compatibility copy.

All 45 WOFF2 files appear in generated font-face declarations. Static analysis cannot safely establish unused face variants across all responsive states, so none were deleted. No images, videos, fonts, or documents were downloaded during this cleanup.

The missing empty-state SVG was only a background in `.pro-gallery-empty .pro-gallery-empty-image`, on 18 pages. Neither empty-state class occurs in generated markup; the replacement gallery code never adds them. The build removes that obsolete rule and raises an error if future source pages contain empty-state UI. This fixes the reference rather than exempting it from validation.

Captured HTML comments, Wix CSS source-map annotations, and stylesheet `data-url`/`data-href` provenance attributes and obsolete Wix publication/etag meta tags were removed from output. SEO/canonical/social metadata and functional external URLs remain. Original snapshots retain provenance and are not meant to be served.

## Reproducibility and recovery

`source/`, `assets/`, `data/`, and `scripts/` are sufficient to generate a complete `dist/`. The CV copy, home alias, measured gallery CSS, and authored CSS/JS are now explicit build steps. Validation is read-only. A fresh build must pass validation before replacing `dist/`; the previous build is retained under `work/previous-builds/`.

A full pre-cleanup archive is in `work/backups/migration-before-cleanup.tar.gz`. A separate original output is kept in `work/baseline-site/`. This local archive supplies recovery without introducing Git or any remote. Historical audit JSON files under `data/audits/` describe the previous session and may include its old preview port; active tools use `data/preview.json` (127.0.0.1:4175).

The inherited preview still occupied port 4174, and the sandbox denied terminating that old process. The maintained preview therefore uses 4175 consistently. This avoids changing the old process or serving stale output as the new build.

## Verification and browser acceptance

The offline checks cover 27 routes, all 148 asset checksums, the CV compatibility copy, local references and anchors, inherited style retention, original page content/gallery/navigation, five exact external video embeds, and absence of developer-machine or temporary paths. Two independent fresh builds must be byte-identical, and checksums before/after validation must match. These checks do not prove visual fidelity.

Browser visual/interaction QA is pending. After all filesystem/build/HTTP checks passed, exactly one browser automation attempt was made against the local preview. It failed immediately with `sandbox-exec: unbound variable: TIOCSTI` (kernel exit 65), reproducing the previous environment issue. No retries or browser-environment debugging were performed.

Remaining acceptance checklist:

- Compare all pages at representative desktop/mobile widths, including typography, spacing, crops, scroll length, and page-specific layouts.
- Exercise linked gallery cards, lightbox open/close/previous/next/keyboard controls, menu focus/Escape, and CV download.
- Verify Vimeo/YouTube playback and responsive sizing in a real browser.
- Check the utility fullscreen route and verify there is no unexpected horizontal overflow or broken imagery.

The `maslows-hierarchy-of-needs` source title says “Song of a Lonely Bird”; it remains unchanged pending a content decision. Full-quality originals can be large; this pass deliberately preserves existing bytes. No live Wix, DNS, domain, hosting, or deployment changes were made.
