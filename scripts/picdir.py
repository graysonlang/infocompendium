#!/usr/bin/env python3
"""
picdir.py -- list the image directory of an Infocom V6 picture library
(.CG1/.EG1/.MG1 on the PC, PIC.DATA/CPIC.DATA on the Mac).

Byte order differs by platform (PC little endian, Mac big endian);
both are tried and the one that yields sane dimensions wins.

Directory layout (after ztools' pix2gif): a 16-byte header with the
image count at offset 4 and the per-entry size at offset 8, then one
entry per image: number, width, height, flags (2 bytes each), followed
by data/palette offsets depending on entry size.

Entries with a zero dimension are not drawable art: Infocom used
invisible pictures as a data channel for per-platform layout metrics,
read by the game with the PICINF opcode.

Usage:
    python3 picdir.py ZORK0.EG1 [more files...]
"""

import sys
sys.dont_write_bytecode = True

import argparse
import struct

MAX_DIM = 1024  # sanity bound used to pick the byte order


def parse(path, big_endian):
    e = ">" if big_endian else "<"
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) < 16:
        return None
    images = struct.unpack(e + "H", data[4:6])[0]
    entry_size = data[8]
    if entry_size < 8 or images == 0:
        return None
    entries = []
    off = 16
    for _ in range(images):
        ent = data[off:off + entry_size]
        if len(ent) < 8:
            return None
        num, width, height, flags = struct.unpack(e + "4H", ent[:8])
        if width > MAX_DIM or height > MAX_DIM:
            return None
        entries.append((num, width, height, flags))
        off += entry_size
    return entries, entry_size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--sort", choices=("number", "area"), default="number")
    args = ap.parse_args()

    for path in args.files:
        result = None
        for be in (False, True):
            result = parse(path, be)
            if result:
                break
        if not result:
            print(f"{path}: not a recognizable picture library", file=sys.stderr)
            continue
        entries, entry_size = result
        order = " big-endian" if be else " little-endian"
        print(f"{path}:{order}, {len(entries)} images, {entry_size}-byte entries")
        if args.sort == "area":
            entries = sorted(entries, key=lambda t: t[1] * t[2], reverse=True)
        for num, w, h, flags in entries:
            note = "  (invisible/metric)" if w == 0 or h == 0 else ""
            print(f"  pic {num:5d}  {w:4d} x {h:4d}  flags {flags:04x}{note}")


if __name__ == "__main__":
    main()
