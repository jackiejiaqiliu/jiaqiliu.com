# Migration notes

## Current scope

The maintained site has **21 routes**, **59 images**, **45 WOFF2 files**, one CV PDF plus its compatibility copy, and five external video embeds. Production Wix, DNS, domain and hosting remain untouched. No deployment or remote repository was created.

The stable pre-UI state was committed locally as `1b2a258` before any content, style or asset changes. Older recovery archives remain under `work/`; historical assets in Git/backups are intentional recovery copies and are not build inputs.

## Preserved architecture

This is the existing offline Python/BeautifulSoup generator, without a framework rewrite. `data/captures/` holds the retained source HTML/page data; `data/model.json` supplies the retained router model; `data/assets.json` resolves original asset URLs to verified local files. Source captures are now curated migration inputs: requested navigation removals and router pruning are applied there, not patched into `dist/`.

`scripts/layout.py` retains the existing desktop/mobile gallery measurement logic. The 11 retained gallery configurations preserve original columns, gaps, image ratios/cropping, and caption padding at the existing 750/751px breakpoint. Other page-specific responsive CSS remains intact. `source/` contains shared authored CSS/JS. Validation is read-only; staged builds must pass before replacing `dist/`.

The shared gallery, dialog lightbox, arrow keys/Escape/focus return, and separate mobile menu behavior are unchanged. `/projects` is a byte-identical home alias. `/fullscreen-page` remains a captured utility shell; gallery enlargement uses the local dialog rather than Wix runtime code.

## Requested UI corrections

- Desktop navigation contains only Projects and Info. The unused Wix More control and empty dropdown container are removed from source captures. A 40px flex gap increases link spacing; no new dropdown or hidden desktop menu was introduced.
- Homepage captions now match the original **below-image** rule: `avenir-lt-w01_35-light1475496`, bold/700, 14px size, 17px line-height, normal letter spacing. The previous override mistakenly used the 22px Poppins **hover-title** style. This correction is scoped to `#pro-gallery-comp-l9xopdjj`; unrelated headings/grid captions are unchanged.
- The Instagram asset has intrinsic 200px dimensions and previously depended on absent Wix image-runtime sizing inside a 30px social item. The obsolete `--wix-img-max-width:max(200px, 100%)` inline style is removed. The anchor, wrapper and image now have explicit 30px square sizing, max-width 100%, and border-box sizing. The image uses object-fit contain. No blanket global overflow hiding was added.
- The separate mobile menu DOM was compared with the baseline and remains unchanged on every retained page that contains it.

## Removed routes and assets

Removed from active source captures/page data, router/sitemap records, generated output, route documentation and links:

- `aphasia-describe-the-city-you-live-in`
- `film-pd-art-direction`
- `hydrogen-balloon`
- `museum-guard-tutorial`
- `oblivio`
- `the-ninth-marriage`

Retained experimentation pages now link back to Projects. Previous/Next links that targeted deleted pages were removed, including unused separators. No dead stubs are generated.

43 images used only by those pages were deleted. `6f04c697ac832136cdb3.jpg` was used by the film index and The Ninth Marriage; `89b48a4a4a1285ba2a8f.png` by the film index and ApHasiA. Neither had any retained-page reference. The complete deletion audit is in `removed-content.json`.

## Image renaming

All 59 retained image basenames were renamed programmatically. `image-path-mapping.json` records each old → new path. Images are grouped under `assets/images/projects/<project>/` and `assets/images/shared/`. The home card destination or retained-page association determines ownership. Ambiguous views use `<project>-image-NN.ext` rather than speculative descriptions; site icons have explicit names.

Extensions and original bytes are unchanged. Build and validation compare SHA-256 with the original inventory; no files were recompressed or downloaded. No hashed image files remain in the active source/generated asset pools. `data/assets.json` preserves original URL/filename provenance, while its `local` fields drive the readable build paths. Fonts and documents retain their existing filenames and directories.

All 45 fonts are still referenced by font-face declarations and retained conservatively. The original CV URL is generated as an identical compatibility copy. Three Vimeo and two YouTube embeds remain unchanged. The extra Oblivio YouTube link disappears with its removed page; other retained editorial/social links remain external.

## Validation and limits

Checks cover all retained routes, removed-route absence, local image/font/CV references, asset byte identity/signatures, exact video embed URLs, navigation contents, renamed-image paths, and absence of developer/temporary paths. The regression contract was adjusted from the Git baseline for exactly the authorized navigation/text/path removals; retained project content and gallery geometry remain checked. Two fresh builds must be byte-identical, and validation must leave output unchanged.

Static layout checks confirm the 30px footer constraint on every retained page with an icon and no matching fixed-width rule above 399px. The remaining inspected `100vw` rules belong to the responsive menu or border-box lightbox; translated rules belong to inherited animation/menu/gallery states. Static checks cannot establish actual browser scroll widths.

The Codex browser tool had already failed with `sandbox-exec: unbound variable: TIOCSTI` and was not retried in this pass. One direct local Playwright/Chrome attempt also failed at launch (SIGABRT / target closed). No launch retries or environment debugging were performed. **Rendered horizontal overflow, pixel comparison, interactive menu/lightbox behavior, and external playback remain unverified.** `scripts/check_layout.cjs` is available to measure all retained routes at 375/768/1440px when a browser can run.

Preview remains `http://127.0.0.1:4175/`; the old inherited server on 4174 could not be stopped under sandbox permissions. The Maslow page's captured title still says “Song of a Lonely Bird”; that unrelated source content is preserved.
