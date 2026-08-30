#!/usr/bin/env python3
"""
splittracks.py -- split a linear raw 2352-byte/sector dump of a mixed-mode
CD into per-track files at Redump's boundaries, hashing each track.

Track starts come from `drutil toc` output (saved in a disc's disc-info.txt).
Redump attaches each audio track's 150-sector pregap to the front of that
track, so the cut for track N (N >= 2) is at its TOC start minus 150
sectors; track 1 starts at sector 0 and carries no pregap.

Drives return audio shifted by their read offset (in 16-bit stereo
samples, 4 bytes each); Redump hashes are offset-corrected. Pass the
drive's offset with --offset to shift the audio tracks back into place;
bytes shifted in from beyond the lead-out are zero, as Redump pads them.
The data track is never shifted.

Usage:
    python3 splittracks.py --toc disc-info.txt full-2352.bin
    python3 splittracks.py --toc disc-info.txt full-2352.bin --out tracks/ --offset 667
"""

import sys
sys.dont_write_bytecode = True

import argparse
import hashlib
import os
import re
import zlib

SECTOR = 2352
PREGAP = 150
TOC_RE = re.compile(r"Track\s+(\d+):\s+(\d+):(\d+)\.(\d+)\s+(data track|\dch audio)")
LEADOUT_RE = re.compile(r"Lead-out:\s+(\d+):(\d+)\.(\d+)")


def msf_to_lba(m, s, f):
    """Absolute MSF -> disc-relative LBA (the 150-sector lead-in offset removed)."""
    return (int(m) * 60 + int(s)) * 75 + int(f) - PREGAP


def parse_toc(text):
    tracks = []
    for m in TOC_RE.finditer(text):
        num = int(m.group(1))
        lba = msf_to_lba(m.group(2), m.group(3), m.group(4))
        kind = "data" if m.group(5) == "data track" else "audio"
        tracks.append((num, lba, kind))
    lo = LEADOUT_RE.search(text)
    if not tracks or not lo:
        sys.exit("could not find track list and lead-out in the TOC text")
    leadout = msf_to_lba(lo.group(1), lo.group(2), lo.group(3))
    return tracks, leadout


def read_span(fh, offset, length):
    """Yield `length` bytes starting at byte `offset`, zero-padded outside the file."""
    size = os.fstat(fh.fileno()).st_size
    pos = offset
    left = length
    while left:
        if pos < 0:
            n = min(-pos, left)
            yield b"\0" * n
        elif pos >= size:
            yield b"\0" * left
            n = left
        else:
            fh.seek(pos)
            chunk = fh.read(min(1 << 22, left, size - pos))
            n = len(chunk)
            yield chunk
        pos += n
        left -= n


def hashes(path, offset, length):
    crc = 0
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(path, "rb") as fh:
        for chunk in read_span(fh, offset, length):
            crc = zlib.crc32(chunk, crc)
            md5.update(chunk)
            sha1.update(chunk)
    return crc & 0xffffffff, md5.hexdigest(), sha1.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dump", help="linear raw dump, 2352 bytes per sector")
    ap.add_argument("--toc", required=True, help="file containing drutil toc output")
    ap.add_argument("--out", help="directory to write per-track .bin files into")
    ap.add_argument("--offset", type=int, default=0,
                    help="drive read offset in samples, applied to audio tracks")
    args = ap.parse_args()

    tracks, leadout = parse_toc(open(args.toc, encoding="utf-8", errors="replace").read())
    size = os.path.getsize(args.dump)
    if size != leadout * SECTOR:
        print(f"warning: dump is {size // SECTOR} sectors, TOC lead-out says {leadout}",
              file=sys.stderr)

    # Cut points: track 1 at 0; later tracks at TOC start minus the pregap.
    cuts = []
    for i, (num, lba, kind) in enumerate(tracks):
        cuts.append(0 if i == 0 else lba - PREGAP)
    cuts.append(leadout)

    if args.out:
        os.makedirs(args.out, exist_ok=True)

    for i, (num, lba, kind) in enumerate(tracks):
        start, end = cuts[i], cuts[i + 1]
        nsec = end - start
        shift = 4 * args.offset if kind == "audio" else 0
        crc, md5, sha1 = hashes(args.dump, start * SECTOR + shift, nsec * SECTOR)
        print(f"track {num:2d} {kind:5s} sectors {nsec:7d} bytes {nsec * SECTOR:10d} "
              f"crc32 {crc:08x} md5 {md5} sha1 {sha1}")
        if args.out:
            outpath = os.path.join(args.out, f"track{num:02d}.bin")
            if os.path.exists(outpath):
                sys.exit(f"already exists, move it aside first: {outpath}")
            with open(args.dump, "rb") as src, open(outpath, "wb") as dst:
                for chunk in read_span(src, start * SECTOR + shift, nsec * SECTOR):
                    dst.write(chunk)


if __name__ == "__main__":
    main()
