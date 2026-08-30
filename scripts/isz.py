#!/usr/bin/env python3
"""
isz.py -- list or extract an InstallShield 3.x archive (the .Z files that
1990s Windows installers ship next to _SETUP.LIB and SETUP.EXE).

The container is a 51-byte header (magic 13 5D 65 8C, file count at
offset 12, table-of-contents offset at 41, directory count at 49), the
members' compressed data, then the table of contents: directory entries
(file count, chunk size, name length, name) followed by file entries
(flag, directory index, uncompressed size, compressed size, data offset,
DOS date, DOS time, ..., chunk size, ..., name length, name).

Members are compressed with the PKWARE Data Compression Library format
("implode"). The decoder below is a port of Mark Adler's blast.c from
zlib's contrib directory, tables included.

Usage:
    python3 isz.py DATA.Z                 # list
    python3 isz.py DATA.Z --extract out/  # extract, preserving directories
"""

import sys
sys.dont_write_bytecode = True

import argparse
import os
import struct
import time

MAGIC = b"\x13\x5d\x65\x8c"

# Compact code-length tables from blast.c: each byte is (count-1) << 4 | length.
LITLEN = [11, 124, 8, 7, 28, 7, 188, 13, 76, 4, 10, 8, 12, 10, 12, 10, 8, 23, 8,
          9, 7, 6, 7, 8, 7, 6, 55, 8, 23, 24, 12, 11, 7, 9, 11, 12, 6, 7, 22, 5,
          7, 24, 6, 11, 9, 6, 7, 22, 7, 11, 38, 7, 9, 8, 25, 11, 8, 11, 9, 12,
          8, 12, 5, 38, 5, 38, 5, 11, 7, 5, 6, 21, 6, 10, 53, 8, 7, 24, 10, 27,
          44, 253, 253, 253, 252, 252, 252, 13, 12, 45, 12, 45, 12, 61, 12, 45,
          44, 173]
LENLEN = [2, 35, 36, 53, 38, 23]
DISTLEN = [2, 20, 53, 230, 247, 151, 248]
BASE = [3, 2, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 40, 72, 136, 264]
EXTRA = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8]
MAXBITS = 13


class Huffman:
    """Canonical Huffman decoder built from blast.c's compact length lists."""

    def __init__(self, rep):
        lengths = []
        for byte in rep:
            lengths.extend([byte & 15] * ((byte >> 4) + 1))
        self.count = [0] * (MAXBITS + 1)
        for length in lengths:
            self.count[length] += 1
        offs = [0] * (MAXBITS + 2)
        for length in range(1, MAXBITS + 1):
            offs[length + 1] = offs[length] + self.count[length]
        self.symbol = [0] * len(lengths)
        for sym, length in enumerate(lengths):
            if length:
                self.symbol[offs[length]] = sym
                offs[length] += 1


class BitReader:
    def __init__(self, data, pos=0):
        self.data = data
        self.pos = pos
        self.bitbuf = 0
        self.bitcnt = 0

    def bits(self, need):
        val = self.bitbuf
        while self.bitcnt < need:
            if self.pos >= len(self.data):
                raise ValueError("ran out of input")
            val |= self.data[self.pos] << self.bitcnt
            self.pos += 1
            self.bitcnt += 8
        self.bitbuf = val >> need
        self.bitcnt -= need
        return val & ((1 << need) - 1)

    def decode(self, h):
        code = first = index = 0
        for length in range(1, MAXBITS + 1):
            code |= self.bits(1) ^ 1        # blast inverts each code bit
            count = h.count[length]
            if code < first + count:
                return h.symbol[index + (code - first)]
            index += count
            first = (first + count) << 1
            code <<= 1
        raise ValueError("ran out of codes")


LITCODE = Huffman(LITLEN)
LENCODE = Huffman(LENLEN)
DISTCODE = Huffman(DISTLEN)


def explode(data, pos, expected):
    """Decompress one PKWARE DCL stream starting at data[pos]; returns bytes."""
    r = BitReader(data, pos)
    lit = r.bits(8)
    dict_bits = r.bits(8)
    if lit > 1 or dict_bits < 4 or dict_bits > 6:
        raise ValueError(f"bad DCL header lit={lit} dict={dict_bits}")
    out = bytearray()
    while True:
        if r.bits(1):
            sym = r.decode(LENCODE)
            length = BASE[sym] + r.bits(EXTRA[sym])
            if length == 519:
                break                       # end code
            shift = 2 if length == 2 else dict_bits
            dist = (r.decode(DISTCODE) << shift) + r.bits(shift) + 1
            if dist > len(out):
                raise ValueError("distance too far back")
            for _ in range(length):         # overlapping copies are intended
                out.append(out[-dist])
        else:
            out.append(r.decode(LITCODE) if lit else r.bits(8))
    if len(out) != expected:
        raise ValueError(f"decompressed {len(out)} bytes, expected {expected}")
    return bytes(out)


def dos_datetime(date, tm):
    return (1980 + (date >> 9), (date >> 5) & 15, date & 31,
            tm >> 11, (tm >> 5) & 63, (tm & 31) * 2)


def read_toc(data):
    if data[:4] != MAGIC:
        raise ValueError("not an InstallShield 3 archive")
    nfiles = struct.unpack("<H", data[12:14])[0]
    toc = struct.unpack("<I", data[41:45])[0]
    ndirs = struct.unpack("<H", data[49:51])[0]
    p = toc
    dirs = []
    for _ in range(ndirs):
        _count, chunk, nlen = struct.unpack("<HHH", data[p:p + 6])
        dirs.append(data[p + 6:p + 6 + nlen].decode("ascii", "replace"))
        p += chunk
    files = []
    for _ in range(nfiles):
        dix, unc, comp, off, date, tm = struct.unpack("<HIIIHH", data[p + 1:p + 19])
        chunk = struct.unpack("<H", data[p + 23:p + 25])[0]
        nlen = data[p + 29]
        name = data[p + 30:p + 30 + nlen].decode("ascii", "replace")
        files.append(dict(dir=dirs[dix], name=name, size=unc, csize=comp,
                          offset=off, when=dos_datetime(date, tm)))
        p += chunk
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archive")
    ap.add_argument("--extract", metavar="DIR", help="extract members into DIR")
    args = ap.parse_args()

    data = open(args.archive, "rb").read()
    files = read_toc(data)
    for f in files:
        y, mo, d, h, mi, s = f["when"]
        path = (f["dir"] + "\\" if f["dir"] else "") + f["name"]
        print(f"{f['size']:9d} {f['csize']:9d}  {y}-{mo:02d}-{d:02d} {h:02d}:{mi:02d}  {path}")
    print(f"{len(files)} files")

    if not args.extract:
        return
    for f in files:
        parts = [p for p in f["dir"].split("\\") if p]
        outdir = os.path.join(args.extract, *parts)
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, f["name"])
        if os.path.exists(outpath):
            sys.exit(f"already exists, move it aside first: {outpath}")
        with open(outpath, "wb") as out:
            out.write(explode(data, f["offset"], f["size"]))
        y, mo, d, h, mi, s = f["when"]
        stamp = time.mktime((y, mo, d, h, mi, s, 0, 0, -1))
        os.utime(outpath, (stamp, stamp))
    print(f"extracted to {args.extract}")


if __name__ == "__main__":
    main()
