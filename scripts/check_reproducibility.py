"""Build twice from source and verify byte identity and read-only validation."""
import hashlib
import json
from pathlib import Path
import tempfile

from build import ROOT, build_site
from validate import validate


def fingerprints(directory):
    return {str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(directory.rglob('*')) if path.is_file()}


def main():
    with tempfile.TemporaryDirectory(prefix='reproducibility-', dir=ROOT / 'work') as folder:
        outputs = [Path(folder) / name for name in ('first', 'second')]
        reports = []
        hashes = []
        for output in outputs:
            output.mkdir()
            build_site(output)
            before = fingerprints(output)
            report = validate(output)
            after = fingerprints(output)
            if report['errors'] or before != after:
                raise RuntimeError(f'Validation failed or changed output: {report}')
            reports.append(report)
            hashes.append(after)
        if hashes[0] != hashes[1]:
            raise RuntimeError('Independent builds differ')
        print(json.dumps({'identical_files': len(hashes[0]), 'validation_read_only': True,
                          'builds': reports}, indent=2))


if __name__ == '__main__':
    main()
