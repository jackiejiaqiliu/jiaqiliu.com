"""Regenerate the static site offline from saved captures and verified local assets."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import urllib.parse

from bs4 import BeautifulSoup, Comment

from layout import refine_layout
from validate import validate

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "data/assets.json").read_text())
ASSETS = {entry["source"]: entry["local"] for entry in MANIFEST}


def asset(url):
    """Resolve only known local assets; a new CDN URL requires explicit inventory work."""
    url = url.strip().replace("&amp;", "&")
    if url.startswith("//"):
        url = "https:" + url
    host = urllib.parse.urlparse(url).hostname or ""
    if not (host.endswith(("wixstatic.com", "parastorage.com", "wix.com"))
            or (host.endswith("jiaqiliu.com") and "/_files/" in url)):
        return url
    if "/media/" in url and "wixstatic" in host:
        url = url.split("/v1/")[0]
    if url not in ASSETS:
        raise ValueError(f"Asset is absent from the offline inventory: {url}")
    return ASSETS[url]


def rewrite_css(text):
    return re.sub(r"url\([\s'\"]*((?:https?:)?//[^)\s'\"]+)[\s'\"]*\)",
                  lambda match: 'url("' + asset(match[1]) + '")', text)


def clean_inherited_markup(soup):
    # The replaced Wix galleries never contain the original empty-state UI.
    # Fail rather than hide a dependency if a later capture introduces that UI.
    if soup.select(".pro-gallery-empty, .pro-gallery-empty-image"):
        raise ValueError("Empty gallery UI needs a deliberate rendering implementation")
    for style in soup.select("style"):
        css = re.sub(r"\.pro-gallery-empty\s+\.pro-gallery-empty-image\s*\{[^}]*\}", "", str(style.string or ""))
        css = re.sub(r"/\*[#@]\s*sourceMappingURL=.*?\*/", "", css, flags=re.S)
        style.string = css
        for attribute in ("data-url", "data-href"):
            if "parastorage.com" in style.get(attribute, ""):
                del style[attribute]
    for meta in soup.select('meta[http-equiv="X-Wix-Published-Version"], meta[http-equiv="etag"]'):
        meta.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        # Captured build markers and commented-out Wix resources are not content.
        comment.extract()


def build_site(D):
    model = json.load(open(ROOT / 'data/model.json'))
    router = model['siteFeaturesConfigs']['router']
    paths = {k: '/' if k == router['mainPageId'] else '/' + v['pageUriSEO'] for (k, v) in router['pagesMap'].items()}
    for p in sorted((ROOT / 'data/captures/desktop').glob('*.html')):
        s = BeautifulSoup(p.read_text(), 'lxml')
        w = json.loads(s.find(id='wix-warmup-data').string)
        data = json.load(open(ROOT / 'data/captures/page-data' / (p.stem + '.json')))
        for t in s.select('script'):
            if t.get('type') != 'application/ld+json':
                t.decompose()
        for t in s.select('link'):
            if set(t.get('rel', [])) & {'preload', 'prefetch', 'preconnect', 'dns-prefetch', 'stylesheet'}:
                t.decompose()
            elif t.get('href'):
                t['href'] = asset(t['href'])
        for t in s.select('style'):
            t.string = rewrite_css(t.text)
        for t in s.select('[style]'):
            t['style'] = rewrite_css(t['style'])
        for t in s.select('source'):
            t.decompose()
        for t in s.select('img'):
            if t.get('src'):
                t['src'] = asset(t['src'])
            elif t.parent.get('data-image-info'):
                try:
                    info = json.loads(t.parent['data-image-info'])
                    t['src'] = asset('https://static.wixstatic.com/media/' + info['imageData']['uri'])
                except (KeyError, json.JSONDecodeError) as error:
                    raise ValueError(f"Invalid image metadata in {p.name}") from error
            t.attrs.pop('srcset', None)
        for t in s.select('a[href]'):
            u = t['href']
            if '/_files/' in u:
                t['href'] = asset(u)
            elif re.match('https?://(www\\.)?jiaqiliu.com(?:/|$)', u):
                t['href'] = re.sub('https?://(www\\.)?jiaqiliu.com', '', u) or '/'
        for app in w.get('appsWarmupData', {}).values():
            for (k, v) in app.items():
                if not isinstance(v, dict) or 'items' not in v:
                    continue
                comp = k.replace('_galleryData', '')
                gallery = s.find(id='pro-gallery-' + comp)
                if not gallery:
                    continue
                items = v['items']
                gallery.clear()
                gallery['class'] = ['local-gallery']
                gallery['data-gallery'] = comp
                linked = any((i.get('metaData', {}).get('link', {}).get('data', {}).get('pageId') for i in items))
                gallery['class'].append('project-grid' if linked else 'image-stack')
                for i in items:
                    meta = i.get('metaData', {})
                    u = asset('https://static.wixstatic.com/media/' + i['mediaUrl'])
                    pid = meta.get('link', {}).get('data', {}).get('pageId', '').lstrip('#')
                    a = s.new_tag('a' if pid else 'button')
                    a['class'] = 'local-gallery-item'
                    a['aria-label'] = meta.get('title') or 'View image'
                    a['href'] = paths.get(pid, '/') if pid else u
                    if not pid:
                        a['type'] = 'button'
                        a['data-full'] = u
                        del a['href']
                    im = s.new_tag('img', src=u, alt=meta.get('alt') or meta.get('title', ''))
                    im['loading'] = 'lazy'
                    im['width'] = meta.get('width', 1200)
                    im['height'] = meta.get('height', 900)
                    a.append(im)
                    if linked and meta.get('title'):
                        cap = s.new_tag('span')
                        cap.string = meta['title']
                        a.append(cap)
                    gallery.append(a)
        for (cid, props) in data['props'].get('render', {}).get('compProps', {}).items():
            if 'playableConfig' not in props:
                continue
            el = s.find(id=cid)
            if not el:
                continue
            u = props.get('src', '')
            el.clear()
            if 'youtu' in u:
                vid = u.split('/')[-1] if 'youtu.be' in u else urllib.parse.parse_qs(urllib.parse.urlparse(u).query).get('v', [''])[0]
                src = 'https://www.youtube.com/embed/' + vid
            elif 'vimeo.com' in u:
                src = 'https://player.vimeo.com/video/' + u.split('/')[-1]
            else:
                src = asset(u)
            tag = s.new_tag('iframe' if src.startswith('http') else 'video')
            tag['src'] = src
            tag['title'] = props.get('title') or 'Video'
            tag['style'] = 'width:100%;height:100%;border:0;min-height:200px'
            tag['allowfullscreen'] = ''
            tag['allow'] = 'autoplay; fullscreen; picture-in-picture'
            tag['loading'] = 'lazy'
            if tag.name == 'video':
                tag['controls'] = ''
            el.append(tag)
        clean_inherited_markup(s)
        st = s.new_tag('link', rel='stylesheet', href='/rebuild.css')
        s.head.append(st)
        js = s.new_tag('script', src='/rebuild.js', defer='')
        s.body.append(js)
        target = D / ('index.html' if p.stem == 'index' else p.stem + '/index.html')
        target.parent.mkdir(exist_ok=True)
        target.write_text(str(s).replace('viewbox=', 'viewBox=').replace('preserveaspectratio=', 'preserveAspectRatio='))

    for entry in MANIFEST:
        source = ROOT / entry["local"].lstrip("/")
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError(f"Missing or changed source asset: {source}")
        target = D / entry["local"].lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if "/_files/" in entry["source"]:
            compatibility = urllib.parse.urlparse(entry["source"]).path
            target = D / compatibility.lstrip("/")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            for page in D.rglob("*.html"):
                page.write_text(page.read_text().replace(entry["local"], compatibility))
    for name in ("rebuild.css", "rebuild.js"):
        shutil.copyfile(ROOT / "source" / name, D / name)
    refine_layout(D)
    (D / "projects").mkdir()
    shutil.copyfile(D / "index.html", D / "projects/index.html")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    destination = args.output.resolve()
    # Never replace an arbitrary source directory or the preserved baseline.
    if destination != ROOT / "dist" and not destination.is_relative_to(ROOT / "work"):
        parser.error("Output must be dist/ or a directory under work/")
    if destination == ROOT / "work" or destination.is_relative_to(ROOT / "work/backups"):
        parser.error("The work root and backups are not build destinations")
    if destination.exists() and destination != ROOT / "dist":
        parser.error("Use a fresh output directory under work/")
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".site-build-", dir=destination.parent))
    try:
        build_site(staging)
        report = validate(staging)
        if report["errors"]:
            raise ValueError(json.dumps(report, indent=2))
        if destination.exists():
            archive = ROOT / "work/previous-builds"
            archive.mkdir(parents=True, exist_ok=True)
            previous = Path(tempfile.mkdtemp(prefix="dist-", dir=archive)) / "dist"
            destination.rename(previous)
        staging.rename(destination)
        print(json.dumps(report, indent=2))
        print(f"Built {destination}")
    finally:
        if staging.exists():
            shutil.rmtree(staging)


if __name__ == "__main__":
    main()
