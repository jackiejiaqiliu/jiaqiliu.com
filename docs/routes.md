# Routes

All 21 retained routes are built and checked locally: 19 saved sitemap routes, `/fullscreen-page`, and the `/projects` home alias. Six obsolete routes were removed at the owner’s request. Coverage is based on saved public captures, not a new crawl. Visual acceptance remains pending.

Generated files below are relative to `dist/`. Capture names identify matching files under `data/captures/desktop/`, `data/captures/mobile/`, and `data/captures/page-data/` (HTML, HTML, JSON respectively).

| Public URL / local route | Generated file | Capture/data stem | Origin | Status and behavior |
| --- | --- | --- | --- | --- |
| [/](https://www.jiaqiliu.com/) | `index.html` | `index` | sitemap | Verified locally; linked gallery |
| [/01001001-00100000-01000100-01001111](https://www.jiaqiliu.com/01001001-00100000-01000100-01001111) | `01001001-00100000-01000100-01001111/index.html` | `01001001-00100000-01000100-01001111` | sitemap | Verified locally; external video player |
| [/ads-named-desire](https://www.jiaqiliu.com/ads-named-desire) | `ads-named-desire/index.html` | `ads-named-desire` | sitemap | Verified locally; gallery with local lightbox |
| [/aesthetics-under-the-microscope](https://www.jiaqiliu.com/aesthetics-under-the-microscope) | `aesthetics-under-the-microscope/index.html` | `aesthetics-under-the-microscope` | sitemap | Verified locally; gallery with local lightbox |
| [/artist-statement](https://www.jiaqiliu.com/artist-statement) | `artist-statement/index.html` | `artist-statement` | sitemap | Verified locally |
| [/breathe](https://www.jiaqiliu.com/breathe) | `breathe/index.html` | `breathe` | sitemap | Verified locally; gallery with local lightbox |
| [/dear-water](https://www.jiaqiliu.com/dear-water) | `dear-water/index.html` | `dear-water` | sitemap | Verified locally; gallery with local lightbox; external video player |
| [/fullscreen-page](https://www.jiaqiliu.com/fullscreen-page) | `fullscreen-page/index.html` | `fullscreen-page` | supplemental | Verified locally; external video player; captured utility shell; local gallery enlargement uses dialog |
| [/info](https://www.jiaqiliu.com/info) | `info/index.html` | `info` | sitemap | Verified locally; CV download |
| [/maslows-hierarchy-of-needs](https://www.jiaqiliu.com/maslows-hierarchy-of-needs) | `maslows-hierarchy-of-needs/index.html` | `maslows-hierarchy-of-needs` | sitemap | Verified locally; gallery with local lightbox; source title says Song of a Lonely Bird; retained for fidelity |
| [/mirage](https://www.jiaqiliu.com/mirage) | `mirage/index.html` | `mirage` | sitemap | Verified locally; gallery with local lightbox |
| [/on-the-avant-garde-responses-and-how-an-artwork-can-stand-out](https://www.jiaqiliu.com/on-the-avant-garde-responses-and-how-an-artwork-can-stand-out) | `on-the-avant-garde-responses-and-how-an-artwork-can-stand-out/index.html` | `on-the-avant-garde-responses-and-how-an-artwork-can-stand-out` | sitemap | Verified locally |
| [/on-the-distinctions-between-ai-works-and-art-works](https://www.jiaqiliu.com/on-the-distinctions-between-ai-works-and-art-works) | `on-the-distinctions-between-ai-works-and-art-works/index.html` | `on-the-distinctions-between-ai-works-and-art-works` | sitemap | Verified locally |
| [/peace-and-peace](https://www.jiaqiliu.com/peace-and-peace) | `peace-and-peace/index.html` | `peace-and-peace` | sitemap | Verified locally |
| [/pointillism](https://www.jiaqiliu.com/pointillism) | `pointillism/index.html` | `pointillism` | sitemap | Verified locally; external video player |
| [/projects](https://www.jiaqiliu.com/projects) | `projects/index.html` | `index` | supplemental alias | Verified locally; linked gallery; exact home alias |
| [/random-thoughts](https://www.jiaqiliu.com/random-thoughts) | `random-thoughts/index.html` | `random-thoughts` | sitemap | Verified locally; gallery with local lightbox |
| [/song-of-a-lonely-bird](https://www.jiaqiliu.com/song-of-a-lonely-bird) | `song-of-a-lonely-bird/index.html` | `song-of-a-lonely-bird` | sitemap | Verified locally; gallery with local lightbox |
| [/song-of-a-lonely-bird-a-re-creation](https://www.jiaqiliu.com/song-of-a-lonely-bird-a-re-creation) | `song-of-a-lonely-bird-a-re-creation/index.html` | `song-of-a-lonely-bird-a-re-creation` | sitemap | Verified locally; external video player |
| [/texts](https://www.jiaqiliu.com/texts) | `texts/index.html` | `texts` | sitemap | Verified locally; linked gallery |
| [/the-clock](https://www.jiaqiliu.com/the-clock) | `the-clock/index.html` | `the-clock` | sitemap | Verified locally; gallery with local lightbox; external video player |

## Responsive layouts

The 11 gallery configurations retain their captured desktop/mobile column counts, gaps, crop ratios, and caption padding. The generated `source-layout.css` preserves the existing 750/751px breakpoint. Original page CSS and source DOM preserve other intentional page differences.
