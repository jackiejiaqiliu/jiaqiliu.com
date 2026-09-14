"""Serve the generated site on the shared local preview address."""
import argparse
import errno
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dist', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    dist = args.dist.resolve()
    if not (dist / 'index.html').is_file():
        parser.error('Build the site first: python3 scripts/build.py')
    config = json.loads((ROOT / 'data/preview.json').read_text())
    handler = partial(SimpleHTTPRequestHandler, directory=str(dist))
    try:
        server = ThreadingHTTPServer((config['host'], config['port']), handler)
    except OSError as error:
        hint = f'Stop the existing preview on port {config["port"]} first.' if error.errno == errno.EADDRINUSE else 'Check local network/listen permissions.'
        parser.exit(1, f'Cannot start preview: {error}. {hint}\n')
    print(f'Preview: http://{config["host"]}:{config["port"]}/', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
