#!/usr/bin/env python3
"""
macscreen.py -- convert a raw Macintosh screen dump to PNG.

Handles the headerless 1-bit format of a classic Mac StartupScreen file: the
exact bytes of the original 512 x 342 frame buffer, 64 bytes per row, top row
first, most significant bit leftmost, 1 = black. Such a file is always 21,888
bytes; anything else is refused rather than guessed at.

This is NOT a MacPaint file (576 x 720, 512-byte header, PackBits).

Standard library only.

Usage:
    python3 macscreen.py StartupScreen                 # writes StartupScreen.png
    python3 macscreen.py StartupScreen -o splash.png
"""

import sys
sys.dont_write_bytecode = True

import argparse
import pathlib
import struct
import zlib

WIDTH, HEIGHT = 512, 342
ROW = WIDTH // 8
SIZE = ROW * HEIGHT          # 21,888


def to_png(raw):
    if len(raw) != SIZE:
        raise ValueError('expected %d bytes (512 x 342 at 1 bit), got %d' % (SIZE, len(raw)))
    # PNG grayscale treats 1 as white; the Mac treats 1 as black, so invert.
    scan = b''.join(b'\x00' + bytes(0xFF ^ b for b in raw[y * ROW:(y + 1) * ROW])
                    for y in range(HEIGHT))

    def chunk(kind, data):
        return (struct.pack('>I', len(data)) + kind + data
                + struct.pack('>I', zlib.crc32(kind + data) & 0xFFFFFFFF))

    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', WIDTH, HEIGHT, 1, 0, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(scan, 9))
            + chunk(b'IEND', b''))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('screen', help='raw 21,888-byte Mac screen dump')
    ap.add_argument('-o', '--out', help='output PNG (default: input name + .png)')
    args = ap.parse_args()

    src = pathlib.Path(args.screen)
    dst = pathlib.Path(args.out) if args.out else src.with_name(src.name + '.png')
    if dst.exists():
        sys.exit('refusing to overwrite %s' % dst)
    try:
        png = to_png(src.read_bytes())
    except (OSError, ValueError) as e:
        sys.exit('%s: %s' % (src, e))
    dst.write_bytes(png)
    print('%s -> %s (%d x %d, %d bytes)' % (src, dst, WIDTH, HEIGHT, len(png)))


if __name__ == '__main__':
    main()
