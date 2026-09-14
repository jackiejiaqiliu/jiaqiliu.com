"""Preserve the existing per-gallery desktop/mobile measurements from Wix captures."""
from pathlib import Path
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def dimensions(tag):
    return {key: float(value) for key, value in
            re.findall(r"(left|top|width|height):([\d.]+)", tag.get("style", ""))}


def refine_layout(D):
    rules = []
    audit = []
    for p in sorted((ROOT / 'data/captures/desktop').glob('*.html')):
        old = BeautifulSoup(p.read_text(), 'lxml')
        mob = BeautifulSoup((ROOT / 'data/captures/mobile' / p.name).read_text(), 'lxml')
        for root in old.select('[id^="pro-gallery-margin-container-"]'):
            cid = root['id'].replace('pro-gallery-margin-container-', '')
            sel = '#pro-gallery-' + cid
            for (mobile, s) in [(False, old), (True, mob)]:
                g = s.find(id='pro-gallery-margin-container-' + cid)
                if not g:
                    continue
                items = g.select('.gallery-item-container')
                ds = [dimensions(i) for i in items]
                xs = sorted(set((d['left'] for d in ds)))
                cols = len(xs)
                gap = xs[1] - xs[0] - ds[0]['width'] if cols > 1 else ds[1]['top'] - ds[0]['top'] - ds[0]['height'] if len(ds) > 1 else 0
                gap = max(0, gap)
                css = [f'{sel}{{display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:{gap}px}}']
                for (n, it) in enumerate(items):
                    im = it.select_one('.gallery-item-content')
                    di = dimensions(im) if im else ds[n]
                    css.append(f"{sel} .local-gallery-item:nth-child({n + 1}) img{{aspect-ratio:{di.get('width', ds[n]['width'])}/{di.get('height', ds[n]['height'])};object-fit:cover;width:100%;height:auto}}")
                    text = it.select_one('.info-element-text')
                    if text:
                        pad = ';'.join((x for x in text.get('style', '').split(';') if x.startswith('padding') or x.startswith('text-align')))
                        css.append(f'{sel} .local-gallery-item:nth-child({n + 1})>span{{{pad}}}')
                rules.append(('@media(max-width:750px){' if mobile else '@media(min-width:751px){') + '\n'.join(css) + '}')
                audit.append({'page': p.stem, 'gallery': cid, 'viewport': 'mobile' if mobile else 'desktop', 'columns': cols, 'gap': gap, 'images': len(items)})
    (D / 'source-layout.css').write_text('\n'.join(rules))
    for p in D.rglob('*.html'):
        t = p.read_text()
        if '/source-layout.css' not in t:
            t = t.replace('</head>', '<link rel="stylesheet" href="/source-layout.css"></head>')
        p.write_text(t)
    return audit
