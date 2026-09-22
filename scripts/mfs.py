#!/usr/bin/env python3
"""
mfs.py -- list or extract the contents of a Macintosh MFS floppy image, and
identify any Infocom story and save files it holds.

MFS is the flat, directory-less filesystem the original 1984 Macintosh used on
400K disks, before HFS. hfsutils does not read it. Its layout is small:

    block 2          master directory block: signature D2D7, file count,
                     directory location, allocation block size and start,
                     volume name, then the allocation map
    allocation map   12-bit entries packed after the MDB, one per allocation
                     block from block 2 on: 0 free, 1 end of file, otherwise
                     the next block in the chain
    file directory   variable-length entries that never span a 512-byte
                     block, each carrying Finder type/creator and the first
                     block and length of both the data and resource forks

Both forks are extracted; the Mac interpreter keeps its code in the resource
fork. Stories are identified from the Z-machine header with the checksum
recomputed, as in fat12.py and adf.py.

Usage:
    python3 mfs.py disk.img                 # list
    python3 mfs.py disk.img -o outdir/      # extract (name, name.rsrc)
"""

import sys
sys.dont_write_bytecode = True

import argparse
import pathlib
import re

MDB = 1024
SCALE = {1: 2, 2: 2, 3: 2, 4: 4, 5: 4, 6: 8, 7: 8, 8: 8}


def be(b, off, n):
    return int.from_bytes(b[off:off + n], 'big')


class Mfs:
    def __init__(self, data):
        self.d = data
        if data[MDB:MDB + 2] != b'\xd2\xd7':
            raise ValueError('not an MFS image (no D2D7 signature at block 2)')
        m = data[MDB:MDB + 512]
        self.nfiles = be(m, 12, 2)
        self.dirst = be(m, 14, 2)
        self.dirlen = be(m, 16, 2)
        self.nalblks = be(m, 18, 2)
        self.alblksiz = be(m, 20, 4)
        self.alblst = be(m, 28, 2)
        n = m[36]
        self.volume = m[37:37 + n].decode('mac_roman')

    def _next(self, blk):
        """Allocation map entry for allocation block blk (numbered from 2)."""
        i = blk - 2
        off = MDB + 64 + (i * 3) // 2
        v = be(self.d, off, 2)
        return (v & 0xFFF) if (i & 1) else (v >> 4)

    def _fork(self, start, length):
        out, blk, seen = bytearray(), start, set()
        while blk >= 2 and len(out) < length and blk not in seen:
            seen.add(blk)
            off = self.alblst * 512 + (blk - 2) * self.alblksiz
            out += self.d[off:off + self.alblksiz]
            nxt = self._next(blk)
            if nxt == 1:
                break
            blk = nxt
        return bytes(out[:length])

    def files(self):
        out = []
        for b in range(self.dirst, self.dirst + self.dirlen):
            blk = self.d[b * 512:(b + 1) * 512]
            pos = 0
            while pos + 51 <= 512:
                if not blk[pos] & 0x80:           # unused: rest of block is empty
                    break
                ftype = blk[pos + 2:pos + 6].decode('mac_roman')
                creator = blk[pos + 6:pos + 10].decode('mac_roman')
                dst, dlen = be(blk, pos + 22, 2), be(blk, pos + 24, 4)
                rst, rlen = be(blk, pos + 32, 2), be(blk, pos + 34, 4)
                nlen = blk[pos + 50]
                name = blk[pos + 51:pos + 51 + nlen].decode('mac_roman')
                out.append(dict(name=name, type=ftype, creator=creator,
                                data=self._fork(dst, dlen) if dlen else b'',
                                rsrc=self._fork(rst, rlen) if rlen else b''))
                pos += 51 + nlen
                pos += pos & 1                     # entries are word-aligned
        return out


def zstory(b):
    if len(b) < 0x40 or b[0] not in SCALE:
        return None
    serial = b[0x12:0x18]
    if not re.match(rb'[0-9]{6}\Z', serial):
        return None
    length = be(b, 0x1A, 2) * SCALE[b[0]]
    if not 0 < length <= len(b):
        return None
    declared = be(b, 0x1C, 2)
    return dict(version=b[0], release=be(b, 2, 2), serial=serial.decode(),
                length=length, declared=declared,
                computed=sum(b[0x40:length]) % 0x10000, padding=len(b) - length)


def safe(name):
    return re.sub(r'[^A-Za-z0-9._ -]', '_', name).strip() or 'unnamed'


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('image', nargs='+')
    ap.add_argument('-o', '--out')
    args = ap.parse_args()

    for path in args.image:
        fs = Mfs(pathlib.Path(path).read_bytes())
        print('%s: MFS, volume %r, %d files, %d allocation blocks of %d bytes'
              % (path, fs.volume, fs.nfiles, fs.nalblks, fs.alblksiz))
        files = fs.files()
        stories = []
        for f in files:
            z = zstory(f['data'])
            if z:
                stories.append((f['name'], z))
            line = '  %-22s %s/%s  data %7d  rsrc %7d' % (
                f['name'], f['type'], f['creator'], len(f['data']), len(f['rsrc']))
            if z:
                line += ('  STORY v%d r%d.%s, %d bytes, checksum %04X %s'
                         % (z['version'], z['release'], z['serial'], z['length'],
                            z['declared'],
                            'VERIFIED' if z['declared'] == z['computed']
                            else 'MISMATCH (computed %04X)' % z['computed']))
            else:
                for sname, s in stories:
                    i = f['data'].find(s['serial'].encode())
                    if i >= 0 and s['declared'].to_bytes(2, 'big') in f['data'][max(0, i - 8):i + 16]:
                        line += '  SAVE for %s' % sname
            print(line)

        if args.out:
            d = pathlib.Path(args.out)
            d.mkdir(parents=True, exist_ok=True)
            for f in files:
                for suffix, key in (('', 'data'), ('.rsrc', 'rsrc')):
                    if not f[key]:
                        continue
                    t = d / (safe(f['name']) + suffix)
                    if t.exists():
                        sys.exit('refusing to overwrite %s' % t)
                    t.write_bytes(f[key])
            print('  extracted to %s' % d)


if __name__ == '__main__':
    main()
