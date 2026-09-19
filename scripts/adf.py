#!/usr/bin/env python3
"""
adf.py -- list or extract the contents of an AmigaDOS floppy image (.adf),
and identify any Infocom story and save files it holds.

Amiga discs are not FAT: an 880K disc is 1760 blocks of 512 bytes with the
root block at 880, directories are hash tables of block pointers, and under
the Old File System every data block spends its first 24 bytes on a header,
so a file's bytes are NOT contiguous on disc. Reading one means walking the
chain, which is why scraping an image for a story file gives you 488 good
bytes followed by a block header.

Both OFS (DOS\\0) and FFS (DOS\\1) are handled: OFS follows the next-data
pointer in each block header, FFS reads the header block's data-block table,
which is stored in reverse.

Story and save files are identified from the Z-machine header, as in
fat12.py - the checksum is recomputed rather than trusted.

Usage:
    python3 adf.py disk.adf                 # list
    python3 adf.py disk.adf -o outdir/      # extract
"""

import sys
sys.dont_write_bytecode = True

import argparse
import pathlib
import re
import struct

BSIZE = 512
T_HEADER, T_DATA, T_LIST = 2, 8, 16
ST_FILE, ST_ROOT, ST_DIR = -3, 1, 2
SCALE = {1: 2, 2: 2, 3: 2, 4: 4, 5: 4, 6: 8, 7: 8, 8: 8}


class Adf:
    def __init__(self, data):
        self.d = data
        if data[:3] != b'DOS':
            raise ValueError('not an AmigaDOS image')
        self.ffs = bool(data[3] & 1)
        self.nblocks = len(data) // BSIZE
        self.root = self.nblocks // 2

    def blk(self, n):
        return self.d[n * BSIZE:(n + 1) * BSIZE]

    def _be(self, b, off):
        return int.from_bytes(b[off:off + 4], 'big')

    def _name(self, b):
        n = b[BSIZE - 80]
        return b[BSIZE - 79:BSIZE - 79 + n].decode('latin1')

    def _data(self, hdr, size):
        """Bytes of one file, from its header block."""
        out = bytearray()
        if not self.ffs:
            nxt = self._be(hdr, 16)                  # first_data
            while nxt and len(out) < size:
                b = self.blk(nxt)
                if self._be(b, 0) != T_DATA:
                    break
                n = self._be(b, 12)                  # data_size
                out += b[24:24 + n]
                nxt = self._be(b, 16)                # next_data
        else:
            block = hdr
            while block is not None and len(out) < size:
                high = self._be(block, 8)
                for i in range(high):
                    ptr = self._be(block, BSIZE - 204 - i * 4)
                    if ptr:
                        out += self.blk(ptr)
                ext = self._be(block, BSIZE - 8)
                block = self.blk(ext) if ext else None
        return bytes(out[:size])

    def walk(self, block=None, prefix=''):
        """Yield (path, bytes) for every file, descending into directories."""
        if block is None:
            block = self.root
        b = self.blk(block)
        entries = BSIZE // 4 - 56
        start = 24 if struct.unpack('>i', b[BSIZE - 4:])[0] in (ST_ROOT, ST_DIR) else 24
        for i in range(entries):
            ptr = self._be(b, start + i * 4)
            while ptr:
                e = self.blk(ptr)
                sec = struct.unpack('>i', e[BSIZE - 4:])[0]
                name = prefix + self._name(e)
                if sec == ST_FILE:
                    size = self._be(e, BSIZE - 188)
                    yield name, self._data(e, size)
                elif sec == ST_DIR:
                    for x in self.walk(ptr, name + '/'):
                        yield x
                ptr = self._be(e, BSIZE - 16)        # hash chain
        return

    def volume(self):
        return self._name(self.blk(self.root))


def zstory(b):
    if len(b) < 0x40 or b[0] not in SCALE:
        return None
    serial = b[0x12:0x18]
    if not re.match(rb'[0-9]{6}\Z', serial):
        return None
    length = int.from_bytes(b[0x1A:0x1C], 'big') * SCALE[b[0]]
    if not 0 < length <= len(b):
        return None
    declared = int.from_bytes(b[0x1C:0x1E], 'big')
    return dict(version=b[0], release=int.from_bytes(b[2:4], 'big'),
                serial=serial.decode(), length=length, declared=declared,
                computed=sum(b[0x40:length]) % 0x10000, padding=len(b) - length)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('image', nargs='+')
    ap.add_argument('-o', '--out')
    args = ap.parse_args()

    for path in args.image:
        fs = Adf(pathlib.Path(path).read_bytes())
        print('%s: %s, %d blocks, volume %r'
              % (path, 'FFS' if fs.ffs else 'OFS', fs.nblocks, fs.volume()))
        files = list(fs.walk())
        stories = []
        for name, b in files:
            z = zstory(b)
            if z:
                stories.append((name, z))
            line = '  %-20s %8d bytes' % (name, len(b))
            if z:
                line += ('  STORY v%d r%d.%s, %d bytes, checksum %04X %s'
                         % (z['version'], z['release'], z['serial'], z['length'],
                            z['declared'],
                            'VERIFIED' if z['declared'] == z['computed']
                            else 'MISMATCH (computed %04X)' % z['computed']))
                if z['padding']:
                    line += ' (+%d padding)' % z['padding']
            else:
                for sname, s in stories:
                    i = b.find(s['serial'].encode())
                    if i >= 0 and s['declared'].to_bytes(2, 'big') in b[max(0, i - 8):i + 16]:
                        line += '  SAVE for %s (header at %d)' % (sname, i)
                        break
            print(line)

        if args.out:
            d = pathlib.Path(args.out)
            d.mkdir(parents=True, exist_ok=True)
            for name, b in files:
                t = d / name.replace('/', '_')
                if t.exists():
                    sys.exit('refusing to overwrite %s' % t)
                t.write_bytes(b)
            print('  extracted %d files to %s' % (len(files), d))


if __name__ == '__main__':
    main()
