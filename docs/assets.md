# Assets

148 unique localized assets (322,095,018 bytes): **102 images, 45 WOFF2 files, and one CV PDF**. Every source file is checked by SHA-256 during build and validation. No bytes were recompressed, resized, or downloaded during cleanup. No byte-identical duplicates exist within the asset inventory.

The previous migration generated URL-hash filenames; those basenames are retained. Assets are now grouped by content type and, where one page clearly owns an image, project. Shared means multiple pages reference it; it does not imply identical creative content.

See [asset-inventory.csv](asset-inventory.csv) for every filename, original/current path, MIME type, referring pages, likely association, font family, byte size, checksum, and source URL. `data/assets.json` is the authoritative build mapping. Paths in the inventory are site-root-relative and also map to source files under the project root.

## Images

| Source directory | Images |
| --- | ---: |
| `assets/images/ads-named-desire/` | 4 |
| `assets/images/aesthetics-under-the-microscope/` | 9 |
| `assets/images/aphasia-describe-the-city-you-live-in/` | 7 |
| `assets/images/breathe/` | 8 |
| `assets/images/dear-water/` | 3 |
| `assets/images/film-pd-art-direction/` | 3 |
| `assets/images/hydrogen-balloon/` | 8 |
| `assets/images/maslows-hierarchy-of-needs/` | 6 |
| `assets/images/mirage/` | 3 |
| `assets/images/museum-guard-tutorial/` | 8 |
| `assets/images/oblivio/` | 8 |
| `assets/images/random-thoughts/` | 4 |
| `assets/images/shared/` | 12 |
| `assets/images/song-of-a-lonely-bird/` | 7 |
| `assets/images/texts/` | 2 |
| `assets/images/the-clock/` | 3 |
| `assets/images/the-ninth-marriage/` | 7 |

Formats: 77 JPG, 2 JPEG, 13 PNG, 9 GIF, and 1 WebP. Shared images include site icons and artwork used by index/gallery pages. Original image source quality is preserved byte-for-byte; using full originals also preserves the existing page-weight tradeoff.

## Fonts

All 45 WOFF2 files are referenced by generated `@font-face` declarations. Filenames alone do not prove duplicates or unused faces. The captured CSS includes family aliases and variants; static analysis cannot prove which faces are never selected at any viewport or interaction state. All are retained conservatively. No font download is needed at runtime.

| CSS family | Retained files under `assets/fonts/` |
| --- | --- |
| `avenir-lt-w01_35-light1475496` | `050d6b3d5e9a4d99c018.woff2`, `5582a9e94d609daf29cc.woff2` |
| `avenir-lt-w01_85-heavy1475544` | `5b2e517c96843c61f148.woff2`, `7895fc9f4725ea8fd43f.woff2` |
| `barlow` | `14f11a9f7dea1acccf1b.woff2`, `180f514cb2612eb5dadf.woff2`, `1ef75a7989e0293f381e.woff2`, `2e7b8b2962b57173d737.woff2`, `3b65a5ce1aca8f84a75b.woff2`, `417b2774430e2357d828.woff2`, `5dace36dc35c905c9e1f.woff2`, `6ae607e43a2fa098d7a2.woff2`, `6ea004fe8b3493b10cd2.woff2`, `78891389d8a13ce9cfbf.woff2`, `8664b122f38cddf7ebe7.woff2`, `e9cf26ffe1abd73e80ff.woff2` |
| `barlow-extralight` | `02784fdab3c1d0e78475.woff2`, `a3032db73efb4e1701b0.woff2`, `b1121bbc4182c47f7ac4.woff2`, `d3659e3c22b45c2bef89.woff2` |
| `din-next-w01-light` | `328d7eb6d22b62994beb.woff2`, `7001cafef9b9ce627a98.woff2`, `9252183be1d488af8243.woff2` |
| `helvetica-w01-bold` | `4459fda0f363dd7c45f9.woff2`, `4fd1215436dc32f740ac.woff2`, `7fe933283ba25bf8cab7.woff2` |
| `helvetica-w01-light` | `02558e81e565fbe1e699.woff2`, `7972bb30901c2b9a476a.woff2` |
| `helvetica-w01-roman` | `00915920e370420b6f07.woff2`, `3bf4f8385bc1f59db145.woff2`, `dc8f7d0e95109dc65245.woff2` |
| `poppins` | `2c9d6bb3baf447c70822.woff2`, `2fca2a872bd9a9a23e17.woff2`, `46ddeb66edf625fa4f1d.woff2`, `48dfb838aaeb6cf2a5e4.woff2`, `80bd3fa1b0177a6c46d4.woff2`, `a3df2fb40c6be271b315.woff2`, `b6165ef682446d7f62c2.woff2`, `f48c4f4ca5cb876c7554.woff2` |
| `poppins-semibold` | `535c8061da3d2052ad68.woff2`, `af999a22a5c607ef8081.woff2`, `e620ca959615875c1586.woff2`, `f27324544bae49d76209.woff2` |
| `proxima-n-w01-reg` | `3a94f23599ecc7df4bb0.woff2`, `99fba282244ecb8b5de6.woff2` |

## CV

The single localized PDF is `/assets/documents/2f5108b85fd4d2cf81ed.pdf`. The build also creates the byte-identical compatibility copy `/_files/ugd/430132_0c8c96a57057435298d6d9eba814c136.pdf` and uses that original URL for the CV link. This intentional extra file is not a second document.

## External media

Three Vimeo and two YouTube embeds are preserved. They need network access and are not downloaded or re-hosted. Validation checks their exact URLs and page associations; playback requires browser QA.

| Page | Preserved embed |
| --- | --- |
| `/dear-water` | [https://www.youtube.com/embed/v36EJoDS4aA](https://www.youtube.com/embed/v36EJoDS4aA) |
| `/song-of-a-lonely-bird-a-re-creation` | [https://player.vimeo.com/video/637236266](https://player.vimeo.com/video/637236266) |
| `/pointillism` | [https://player.vimeo.com/video/638218379](https://player.vimeo.com/video/638218379) |
| `/01001001-00100000-01000100-01001111` | [https://player.vimeo.com/video/569937926](https://player.vimeo.com/video/569937926) |
| `/the-clock` | [https://www.youtube.com/embed/vqhTacybLm0](https://www.youtube.com/embed/vqhTacybLm0) |

External video links: `/oblivio` → [https://www.youtube.com/watch?v=ehUtYYprSTI](https://www.youtube.com/watch?v=ehUtYYprSTI).

Other external editorial/project/social links are preserved as navigation links. No active Wix CDN image/font/document references remain. Source capture URLs remain in the offline input/archive data for provenance.

## Removed obsolete reference

The missing `media/emptystate.85a4add5.svg` appeared only in the inherited `.pro-gallery-empty .pro-gallery-empty-image` CSS rule on 18 generated pages. No generated page contained either empty-state class, and the local gallery code never creates them. The build removes that dead rule and explicitly rejects future captures containing empty-state UI so a new dependency cannot be silently hidden.
