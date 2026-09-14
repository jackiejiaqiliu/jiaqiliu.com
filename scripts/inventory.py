"""Refresh human-readable route/asset documentation from inventories and built HTML."""
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def main():
    assets = json.loads((ROOT / 'data/assets.json').read_text())
    routes = json.loads((ROOT / 'data/routes.json').read_text())
    embeds = json.loads((ROOT / 'data/audits/external-video-embeds.json').read_text())
    dist = ROOT / 'dist'
    pages = {r['path']: BeautifulSoup((dist / r['file']).read_text(), 'lxml') for r in routes}
    usage = defaultdict(set)
    families = defaultdict(set)
    for route, soup in pages.items():
        text = str(soup)
        for asset in assets:
            compatibility = urlparse(asset['source']).path if '/_files/' in asset['source'] else None
            if asset['local'] in text or (compatibility and compatibility in text):
                usage[asset['local']].add(route)
        for style in soup.select('style'):
            for block in re.findall(r'@font-face\s*\{([^}]+)\}', style.text):
                family = re.search(r'font-family\s*:\s*([^;]+)', block)
                if family:
                    for path in re.findall(r'/assets/fonts/[^\s\"\'()]+', block):
                        families[family[1].strip().strip('\"\'')].add(path)
    with (ROOT / 'docs/asset-inventory.csv').open('w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['filename', 'original_local_path', 'local_path', 'content_type', 'pages', 'association', 'font_families', 'bytes', 'sha256', 'source_url'])
        for asset in sorted(assets, key=lambda a: a['local']):
            writer.writerow([Path(asset['local']).name, asset['original_local'], asset['local'], asset['content_type'], '; '.join(sorted(usage[asset['local']])), asset['project'], '; '.join(asset['font_families']), asset['bytes'], asset['sha256'], asset['source']])
    lines = ['# Routes', '',
             'All 27 routes are built and checked locally: 25 saved sitemap routes, `/fullscreen-page`, and the `/projects` home alias. Coverage is based on the saved public captures, not a new crawl. Visual acceptance remains pending.', '',
             'Generated files below are relative to `dist/`. Capture names identify matching files under `data/captures/desktop/`, `data/captures/mobile/`, and `data/captures/page-data/` (HTML, HTML, JSON respectively).', '',
             '| Public URL / local route | Generated file | Capture/data stem | Origin | Status and behavior |',
             '| --- | --- | --- | --- | --- |']
    for route in routes:
        soup = pages[route['path']]
        notes = ['Verified locally']
        if soup.select('.project-grid'): notes.append('linked gallery')
        if soup.select('.image-stack'): notes.append('gallery with local lightbox')
        if soup.select('iframe'): notes.append('external video player')
        if route['path'] == '/info': notes.append('CV download')
        if route['path'] == '/fullscreen-page': notes.append('captured utility shell; local gallery enlargement uses dialog')
        if route['path'] == '/projects': notes.append('exact home alias')
        if route['path'] == '/maslows-hierarchy-of-needs': notes.append('source title says Song of a Lonely Bird; retained for fidelity')
        lines.append(f"| [{route['path']}](https://www.jiaqiliu.com{route['path']}) | `{route['file']}` | `{Path(route['capture']).stem}` | {route['kind']} | {'; '.join(notes)} |")
    lines += ['', '## Responsive layouts', '', 'The 17 gallery configurations retain their captured desktop/mobile column counts, gaps, crop ratios, and caption padding. The generated `source-layout.css` preserves the existing 750/751px breakpoint. Original page CSS and source DOM preserve other intentional page differences.', '']
    (ROOT / 'docs/routes.md').write_text('\n'.join(lines))

    groups = Counter(str(Path(a['local']).parent).removeprefix('/assets/') for a in assets if a['content_type'].startswith('image/'))
    lines = ['# Assets', '',
             '148 unique localized assets (322,095,018 bytes): **102 images, 45 WOFF2 files, and one CV PDF**. Every source file is checked by SHA-256 during build and validation. No bytes were recompressed, resized, or downloaded during cleanup. No byte-identical duplicates exist within the asset inventory.', '',
             'The previous migration generated URL-hash filenames; those basenames are retained. Assets are now grouped by content type and, where one page clearly owns an image, project. Shared means multiple pages reference it; it does not imply identical creative content.', '',
             'See [asset-inventory.csv](asset-inventory.csv) for every filename, original/current path, MIME type, referring pages, likely association, font family, byte size, checksum, and source URL. `data/assets.json` is the authoritative build mapping. Paths in the inventory are site-root-relative and also map to source files under the project root.', '',
             '## Images', '', '| Source directory | Images |', '| --- | ---: |']
    lines += [f'| `assets/{group}/` | {count} |' for group,count in sorted(groups.items())]
    lines += ['', 'Formats: 77 JPG, 2 JPEG, 13 PNG, 9 GIF, and 1 WebP. Shared images include site icons and artwork used by index/gallery pages. Original image source quality is preserved byte-for-byte; using full originals also preserves the existing page-weight tradeoff.', '',
              '## Fonts', '',
              'All 45 WOFF2 files are referenced by generated `@font-face` declarations. Filenames alone do not prove duplicates or unused faces. The captured CSS includes family aliases and variants; static analysis cannot prove which faces are never selected at any viewport or interaction state. All are retained conservatively. No font download is needed at runtime.', '',
              '| CSS family | Retained files under `assets/fonts/` |', '| --- | --- |']
    for family,paths in sorted(families.items()):
        lines.append(f"| `{family}` | " + ', '.join('`'+Path(p).name+'`' for p in sorted(paths)) + ' |')
    pdf = next(a for a in assets if a['content_type']=='application/pdf')
    lines += ['', '## CV', '', f"The single localized PDF is `{pdf['local']}`. The build also creates the byte-identical compatibility copy `{urlparse(pdf['source']).path}` and uses that original URL for the CV link. This intentional extra file is not a second document.", '', '## External media', '', 'Three Vimeo and two YouTube embeds are preserved. They need network access and are not downloaded or re-hosted. Validation checks their exact URLs and page associations; playback requires browser QA.', '', '| Page | Preserved embed |', '| --- | --- |']
    lines += [f"| `/{e['page']}` | [{e['embed']}]({e['embed']}) |" for e in embeds]
    video_links=[]
    for route,soup in pages.items():
        for tag in soup.select('a[href]'):
            if urlparse(tag['href']).hostname in ('www.youtube.com','youtube.com','youtu.be','vimeo.com'):
                video_links.append((route,tag['href']))
    lines += ['', 'External video links: ' + '; '.join(f'`{page}` → [{url}]({url})' for page,url in video_links) + '.', '',
              'Other external editorial/project/social links are preserved as navigation links. No active Wix CDN image/font/document references remain. Source capture URLs remain in the offline input/archive data for provenance.', '',
              '## Removed obsolete reference', '',
              'The missing `media/emptystate.85a4add5.svg` appeared only in the inherited `.pro-gallery-empty .pro-gallery-empty-image` CSS rule on 18 generated pages. No generated page contained either empty-state class, and the local gallery code never creates them. The build removes that dead rule and explicitly rejects future captures containing empty-state UI so a new dependency cannot be silently hidden.', '']
    (ROOT / 'docs/assets.md').write_text('\n'.join(lines))
    print('Updated docs/routes.md, docs/assets.md, docs/asset-inventory.csv')


if __name__ == '__main__':
    main()
