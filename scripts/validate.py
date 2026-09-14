"""Read-only validation of generated pages, local references, assets, and embeds."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlparse
from urllib.request import urlopen

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CSS_URL = re.compile(r"url\(\s*[\"']?([^\"'\s)]+)")


def validate(dist, base_url=None):
    dist = Path(dist).resolve()
    routes = json.loads((ROOT / "data/routes.json").read_text())
    assets = json.loads((ROOT / "data/assets.json").read_text())
    embeds = json.loads((ROOT / "data/audits/external-video-embeds.json").read_text())
    expected_embeds = Counter((e['page'], e['embed']) for e in embeds)
    actual_embeds = Counter()
    errors = []
    checked = 0
    external = set()
    html_paths = sorted(dist.rglob('*.html'))
    expected_paths = {r['file'] for r in routes}
    if {str(p.relative_to(dist)) for p in html_paths} != expected_paths:
        errors.append('Generated HTML files do not match the 27-route inventory')
    soups = {p: BeautifulSoup(p.read_text(), 'lxml') for p in html_paths}

    def check_reference(page, value, kind):
        nonlocal checked
        parsed = urlparse(value)
        if parsed.scheme in ('data', 'mailto', 'tel', 'javascript'):
            return
        if parsed.netloc or parsed.scheme:
            if parsed.hostname in ('jiaqiliu.com', 'www.jiaqiliu.com') and kind == 'a':
                value = parsed.path or '/'
                parsed = urlparse(value)
            else:
                external.add(value)
                host = parsed.hostname or ''
                if host.endswith(('wixstatic.com', 'parastorage.com', 'wix.com')):
                    errors.append(f'{page.relative_to(dist)}: remote Wix reference {value}')
                return
        if not parsed.path and not parsed.fragment:
            return
        checked += 1
        target = dist / unquote(parsed.path).lstrip('/') if value.startswith('/') else page.parent / unquote(parsed.path)
        if not parsed.path:
            target = page
        target = target.resolve()
        if not target.is_relative_to(dist):
            errors.append(f'{page.relative_to(dist)}: reference escapes output: {value}')
            return
        if target.is_dir():
            target = target / 'index.html'
        if not target.is_file() or not target.stat().st_size:
            errors.append(f'{page.relative_to(dist)}: missing/empty reference {value}')
        elif parsed.fragment and target in soups:
            fragment = unquote(parsed.fragment)
            if fragment and not soups[target].find(id=fragment) and not soups[target].find('a', attrs={'name': fragment}):
                errors.append(f'{page.relative_to(dist)}: missing anchor {value}')

    for page in sorted(dist.rglob('*')):
        if not page.is_file():
            continue
        if not page.stat().st_size:
            errors.append(f'Empty output file: {page.relative_to(dist)}')
        if page.suffix not in ('.html', '.css', '.js', '.json', '.svg'):
            continue
        text = page.read_text()
        if '/Users/jiaqiliu/' in text or re.search(r'(?:["\'\s=/])(?:\.\./)*work/', text):
            errors.append(f'Developer/temporary path in {page.relative_to(dist)}')
        if page in soups:
            soup = soups[page]
            for tag in soup.select('[src], [href], [poster], [data-full]'):
                for attr in ('src', 'href', 'poster', 'data-full'):
                    if tag.get(attr):
                        check_reference(page, tag[attr], tag.name)
            for tag in soup.select('[srcset]'):
                for candidate in tag['srcset'].split(','):
                    check_reference(page, candidate.strip().split()[0], 'srcset')
            for tag in soup.select('meta[content]'):
                if tag['content'].startswith(('https://', 'http://', '/assets/')):
                    check_reference(page, tag['content'], 'meta')
            for tag in soup.select('iframe[src]'):
                actual_embeds[(page.parent.name, tag['src'])] += 1
            css = '\n'.join(tag.text for tag in soup.select('style'))
            css += '\n' + '\n'.join(tag['style'] for tag in soup.select('[style]'))
        else:
            css = text if page.suffix == '.css' else ''
        for value in CSS_URL.findall(css):
            check_reference(page, value, 'css')
        for value in re.findall(r'@import\s+["\']([^"\']+)', css):
            check_reference(page, value, 'css')

    # Compare content and page structure with the preserved pre-cleanup output.
    contract = json.loads((ROOT / "data/render-contract.json").read_text())
    for page, soup in soups.items():
        expected = contract.get(str(page.relative_to(dist)))
        if expected is None:
            continue
        actual = {
            'text': soup.get_text(' ', strip=True),
            'style_blocks': len(soup.select('style')),
            'images': [[t.get('src'), t.get('alt')] for t in soup.select('img')],
            'galleries': [[t.get('id'), len(t.select('.local-gallery-item'))] for t in soup.select('.local-gallery')],
            'links': [t.get('href') for t in soup.select('a[href]')],
        }
        for key, value in actual.items():
            if value != expected[key]:
                errors.append(f'{page.relative_to(dist)}: baseline {key} changed')
        if sum(len(t.text) for t in soup.select('style')) < expected['minimum_css_bytes']:
            errors.append(f'{page.relative_to(dist)}: inherited CSS unexpectedly lost')

    for entry in assets:
        path = dist / entry['local'].lstrip('/')
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            errors.append(f'Asset missing or changed: {entry["local"]}')
        if path.is_file():
            signature = path.read_bytes()[:16]
            mime = entry['content_type']
            valid = (signature.startswith(b'wOF2') if mime == 'font/woff2' else
                     signature.startswith(b'%PDF-') if mime == 'application/pdf' else
                     signature.startswith(b'\xff\xd8\xff') if mime == 'image/jpeg' else
                     signature.startswith(b'\x89PNG\r\n\x1a\n') if mime == 'image/png' else
                     signature.startswith((b'GIF87a', b'GIF89a')) if mime == 'image/gif' else
                     signature.startswith(b'RIFF') and signature[8:12] == b'WEBP' if mime == 'image/webp' else False)
            if not valid:
                errors.append(f'Unexpected file signature: {entry["local"]}')
        if '/_files/' in entry['source']:
            path = dist / urlparse(entry['source']).path.lstrip('/')
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
                errors.append('CV compatibility copy missing or changed')
    if actual_embeds != expected_embeds:
        errors.append('External video embeds differ from the captured inventory')
    statuses = {}
    if base_url:
        for route in routes:
            try:
                with urlopen(base_url.rstrip('/') + route['path'], timeout=10) as response:
                    statuses[route['path']] = response.status
                    local = (dist / route['file']).read_bytes()
                    if response.status != 200 or response.read() != local:
                        errors.append(f'HTTP content mismatch: {route["path"]}')
            except Exception as exc:
                errors.append(f'HTTP route {route["path"]}: {exc}')
    return {'routes_expected': len(routes), 'routes_present': len(html_paths),
            'local_references_checked': checked, 'assets_verified': len(assets),
            'external_video_embeds': sum(actual_embeds.values()),
            'http_status': statuses, 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dist', type=Path, default=ROOT / 'dist')
    parser.add_argument('--http', action='store_true', help='Also verify served HTML at the configured preview URL')
    args = parser.parse_args()
    config = json.loads((ROOT / 'data/preview.json').read_text())
    url = f'http://{config["host"]}:{config["port"]}' if args.http else None
    report = validate(args.dist, url)
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(report['errors']))


if __name__ == '__main__':
    main()
