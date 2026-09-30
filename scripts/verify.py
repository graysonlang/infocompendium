#!/usr/bin/env python3
"""
verify.py -- check a checksums.txt against the files it describes.

Reads a record in this catalog's format: a comment line naming a file,
followed by its md5, sha1 and/or crc32. Every file under the search roots is
hashed once and matched against the record, so files may be renamed, moved
between roots, or stored compressed without invalidating anything - the hash
is the identity, not the path.

Two conveniences that matter for flux captures:

  * a .zst capture is hashed BOTH as stored and as its decompressed contents,
    because the record holds the hash of the uncompressed flux - that being
    the artifact's identity, the container is not;
  * search roots are given on the command line, never stored here, so a record
    stays valid when working files move to another disk or a sync folder.

Exit status is 1 if any entry is unaccounted for.

Usage:
    python3 verify.py checksums.txt ROOT [ROOT ...]
    python3 verify.py checksums.txt ROOT --list-missing
"""

import sys
sys.dont_write_bytecode = True

import argparse
import hashlib
import pathlib
import re
import zlib

CHUNK = 1 << 20
HASHLINE = re.compile(r'^(md5|sha1|crc32)\s+([0-9a-f]{8,40})\s*$')
# "# name - 12,345 bytes" or "# path/name.ext" -- the label for following hashes
NAMELINE = re.compile(r'^#\s*([A-Za-z0-9][\w./+-]*\.[A-Za-z0-9]{1,6})\b')


def digests(path):
    """md5, sha1 and crc32 of a file, plus of its contents if zstd-compressed."""
    out = set()

    def of(stream):
        m, s, c = hashlib.md5(), hashlib.sha1(), 0
        while True:
            b = stream.read(CHUNK)
            if not b:
                break
            m.update(b); s.update(b); c = zlib.crc32(b, c)
        return {m.hexdigest(), s.hexdigest(), '%08x' % (c & 0xFFFFFFFF)}

    with open(path, 'rb') as f:
        out |= of(f)
    if path.suffix == '.zst':
        try:
            from compression import zstd
            with zstd.ZstdFile(path, 'rb') as f:
                out |= of(f)
        except ImportError:
            print('  note: no zstd module, %s hashed only as stored' % path.name,
                  file=sys.stderr)
        except Exception as e:
            print('  note: could not decompress %s (%s)' % (path.name, e),
                  file=sys.stderr)
    return out


def index(roots):
    seen, files = set(), 0
    for root in roots:
        base = pathlib.Path(root)
        if not base.exists():
            print('  warning: %s does not exist' % base, file=sys.stderr)
            continue
        for p in base.rglob('*'):
            if not p.is_file() or '.git' in p.parts:
                continue
            try:
                seen |= digests(p)
            except OSError as e:
                print('  warning: %s: %s' % (p, e), file=sys.stderr)
                continue
            files += 1
    return seen, files


def entries(record):
    """[(label, [hashes])] in file order."""
    out, label = [], '(unlabelled)'
    for line in pathlib.Path(record).read_text().splitlines():
        m = NAMELINE.match(line)
        if m:
            label = m.group(1)
            continue
        h = HASHLINE.match(line)
        if h:
            if out and out[-1][0] == label:
                out[-1][1].append(h.group(2))
            else:
                out.append((label, [h.group(2)]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('record', help='a checksums.txt')
    ap.add_argument('roots', nargs='+', help='directories to search')
    ap.add_argument('--list-missing', action='store_true',
                    help='name every unaccounted-for entry, not just the count')
    args = ap.parse_args()

    have, nfiles = index(args.roots)
    rows = entries(args.record)
    total = sum(len(h) for _, h in rows)
    missing = [(label, [h for h in hs if h not in have]) for label, hs in rows]
    missing = [(label, hs) for label, hs in missing if hs]

    print('indexed %d files under %d root(s)' % (nfiles, len(args.roots)))
    print('%s: %d hashes over %d entries, %d entries unaccounted for'
          % (args.record, total, len(rows), len(missing)))
    if missing and args.list_missing:
        for label, hs in missing:
            print('  MISSING %-52s %s' % (label, hs[0]))
    elif missing:
        print('  re-run with --list-missing to name them')
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
