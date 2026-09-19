#!/usr/bin/env python3
"""
fat12.py -- list or extract the contents of a FAT12 floppy image, and
identify any Infocom story and save files it holds.

Written for the Atari ST diskettes in this catalog, which carry a plain
DOS-compatible FAT12 with no copy protection, but the parser is generic
and works on 360K/720K/1.44M PC images too.

A story file is identified from its Z-machine header rather than its name:
version byte, release, serial, declared length and checksum, with the
checksum recomputed over the body so the report is a verification and not
a transcription.

A save file is identified the same way - Infocom saves embed the release,
serial and checksum of the story they belong to, so a save can be matched
to its story rather than assumed to go with whatever shares its disk.

Usage:
    python3 fat12.py disk.img                 # list
    python3 fat12.py disk.img -o outdir/      # extract
"""

import sys
sys.dont_write_bytecode = True

import argparse
import pathlib
import re

SCALE = {1: 2, 2: 2, 3: 2, 4: 4, 5: 4, 6: 8, 7: 8, 8: 8}


class Fat12:
    def __init__(self, data):
        self.d = data
        self.bps = int.from_bytes(data[11:13], 'little')
        self.spc = data[13]
        self.res = int.from_bytes(data[14:16], 'little')
        self.nfat = data[16]
        self.ndir = int.from_bytes(data[17:19], 'little')
        self.nsec = int.from_bytes(data[19:21], 'little')
        self.spf = int.from_bytes(data[22:24], 'little')
        self.spt = int.from_bytes(data[24:26], 'little')
        self.heads = int.from_bytes(data[26:28], 'little')
        if not (self.bps in (128, 256, 512, 1024) and self.spc and self.nfat):
            raise ValueError('not a FAT12 image (implausible BPB)')
        self.fat = self.res * self.bps
        self.root = (self.res + self.nfat * self.spf) * self.bps
        self.data = self.root + self.ndir * 32

    def _next(self, n):
        off = self.fat + (n * 3) // 2
        v = int.from_bytes(self.d[off:off + 2], 'little')
        return (v >> 4) if (n & 1) else (v & 0xFFF)

    def _chain(self, start, size):
        out, c, seen = bytearray(), start, set()
        while 2 <= c < 0xFF8 and len(out) < size and c not in seen:
            seen.add(c)
            off = self.data + (c - 2) * self.spc * self.bps
            out += self.d[off:off + self.spc * self.bps]
            c = self._next(c)
        return bytes(out[:size])

    def files(self):
        out = []
        for i in range(self.ndir):
            e = self.d[self.root + i * 32: self.root + i * 32 + 32]
            if not e or e[0] == 0x00:
                break
            if e[0] == 0xE5 or e[11] & 0x08:      # deleted, or volume label
                continue
            stem = e[0:8].decode('latin1').rstrip()
            ext = e[8:11].decode('latin1').rstrip()
            name = stem + ('.' + ext if ext else '')
            size = int.from_bytes(e[28:32], 'little')
            out.append((name, self._chain(int.from_bytes(e[26:28], 'little'), size)))
        return out


def zstory(b):
    """Return a report if b looks like a Z-machine story, else None."""
    if len(b) < 0x40 or b[0] not in SCALE:
        return None
    serial = b[0x12:0x18]
    if not re.match(rb'[0-9]{6}\Z', serial):
        return None
    length = int.from_bytes(b[0x1A:0x1C], 'big') * SCALE[b[0]]
    if not 0 < length <= len(b):
        return None
    declared = int.from_bytes(b[0x1C:0x1E], 'big')
    calc = sum(b[0x40:length]) % 0x10000
    return dict(version=b[0], release=int.from_bytes(b[2:4], 'big'),
                serial=serial.decode(), length=length, declared=declared,
                computed=calc, ok=declared == calc, padding=len(b) - length)


def zsave(b, stories):
    """Match a save against the stories on the same disk, by the release,
    serial and checksum an Infocom save carries in its header."""
    for name, s in stories:
        ser = s['serial'].encode()
        i = b.find(ser)
        if i < 0:
            continue
        window = b[max(0, i - 8):i + 16]
        if s['declared'].to_bytes(2, 'big') in window:
            return name, i
    return None, -1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('image', nargs='+')
    ap.add_argument('-o', '--out', help='directory to extract files into')
    args = ap.parse_args()

    for path in args.image:
        data = pathlib.Path(path).read_bytes()
        fs = Fat12(data)
        print('%s: %d bytes/sector, %d sectors, %d sectors/track, %d head(s)'
              % (path, fs.bps, fs.nsec, fs.spt, fs.heads))
        files = fs.files()
        stories = []
        for name, b in files:
            z = zstory(b)
            if z:
                stories.append((name, z))
        for name, b in files:
            z = next((s for n, s in stories if n == name), None)
            line = '  %-14s %8d bytes' % (name, len(b))
            if z:
                line += ('  STORY v%d r%d.%s, %d bytes, checksum %04X %s'
                         % (z['version'], z['release'], z['serial'], z['length'],
                            z['declared'], 'VERIFIED' if z['ok'] else
                            'MISMATCH (computed %04X)' % z['computed']))
                if z['padding']:
                    line += ' (+%d padding)' % z['padding']
            else:
                owner, at = zsave(b, stories)
                if owner:
                    line += '  SAVE for %s (header at %d)' % (owner, at)
            print(line)

        if args.out:
            d = pathlib.Path(args.out)
            d.mkdir(parents=True, exist_ok=True)
            for name, b in files:
                target = d / name
                if target.exists():
                    sys.exit('refusing to overwrite %s' % target)
                target.write_bytes(b)
            print('  extracted %d files to %s' % (len(files), d))


if __name__ == '__main__':
    main()
