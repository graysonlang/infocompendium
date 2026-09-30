#!/usr/bin/env python3
"""
a2gcr.py -- decode an Apple II 16-sector disk from Greaseweazle flux, including
copy-protected disks that a stock decoder reports as empty.

Infocom protected some Apple II releases by changing the DATA field prologue
from the standard D5 AA AD to another value - D5 AA BC on the Sorcerer disk
this was written for - while leaving the ADDRESS fields (D5 AA 96) untouched.
The effect on `gw convert --format=apple2.appledos.140` is total: the affected
tracks decode as 0 of 16 sectors, which looks exactly like an unreadable disk.
It is not. Every sector is present and its checksum verifies; only the three
bytes announcing the data field differ.

The giveaway is a track with a full set of address marks and no data marks.
Count D5 AA 96 and D5 AA AD per track: 32 and 32 over two revolutions is a
healthy standard track, 32 and 0 is a protected one, and a mixture means the
protection was applied to part of the track - the Sorcerer disk's track 2 has
four standard sectors and twelve altered ones.

Sector placement comes from the address field rather than from counting, so a
disk with an odd sector order decodes correctly. Output is a DOS-order .dsk,
the layout `gw convert --format=apple2.appledos.140` produces, so the result
drops straight into the rest of this catalog's tooling.

Usage:
    python3 a2gcr.py capture.scp -o disk.dsk
    python3 a2gcr.py capture.scp --report        # per-track prologue census
"""

import sys
sys.dont_write_bytecode = True

import argparse
import collections
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import xzip18 as gcr

TRACKS, SECTORS, SECSIZE = 35, 16, 256
ADDR = (0xD5, 0xAA, 0x96)
DATA_MARKS = (0xAD, 0xBC)          # standard, and Infocom's altered prologue
# DOS 3.3 interleave; a physical sector lands at this offset within its track.
FORWARD = [int(c, 16) for c in "0DB97531ECA8642F"]
INVERSE = [FORWARD.index(k) for k in range(SECTORS)]
# The bit cell of an Apple disk read in a 360 RPM drive is not 4000 ns, and not
# every disk sits at the same figure; these are tried in turn.
NOMINALS = (3800, 3600, 4000, 3355)
GAINS = (1.0, 0.30, 0.0875)        # 1.0 leaves the flux alone; see floppy-imaging.md


def de44(a, b):
    """Decode a 4-and-4 encoded byte, as used by Apple address fields."""
    return ((a << 1) | 1) & b


def census(nibs):
    addr = data = 0
    marks = collections.Counter()
    for i in range(len(nibs) - 2):
        if nibs[i] == 0xD5 and nibs[i + 1] == 0xAA:
            if nibs[i + 2] == 0x96:
                addr += 1
            else:
                data += 1
                marks[nibs[i + 2]] += 1
    return addr, data, marks


def sectors(nibs, cyl):
    """Yield ((cyl, sector), (bytes, confidence)) for every data field found."""
    i, n = 0, len(nibs)
    while i < n - 400:
        if (nibs[i], nibs[i + 1], nibs[i + 2]) == ADDR:
            trk = de44(nibs[i + 5], nibs[i + 6])
            sec = de44(nibs[i + 7], nibs[i + 8])
            j, limit = i + 11, min(i + 120, n - 346)
            while j < limit:
                if nibs[j] == 0xD5 and nibs[j + 1] == 0xAA and nibs[j + 2] in DATA_MARKS:
                    res = gcr.decode_sector(nibs, j + 3)
                    if res and trk == cyl and sec < SECTORS:
                        yield (cyl, sec), res
                    i = j + 340
                    break
                j += 1
        i += 1


def decode(path, report=False):
    tracks = gcr.scp_tracks(path)
    found = collections.defaultdict(list)
    for cyl in range(TRACKS):
        revs = tracks.get(cyl * 2)
        if not revs:
            continue
        if report:
            gcr.REGRID_GAIN = GAINS[0]
            nibs = gcr.bits_to_nibs(gcr.flux_to_bits(revs[0] + revs[1], nominal=NOMINALS[0]))
            addr, data, marks = census(nibs)
            std, alt = marks.get(0xAD, 0), sum(v for k, v in marks.items()
                                                 if k in DATA_MARKS and k != 0xAD)
            kind = ('standard' if std and not alt else 'PROTECTED' if alt and not std
                    else 'mixed' if std and alt else '-')
            other = ' '.join('%02X:%d' % (k, v) for k, v in sorted(marks.items())
                             if k not in DATA_MARKS)
            print('  cyl %2d: address %2d  data AD:%2d %s  %-10s%s'
                  % (cyl, addr, std,
                     ' '.join('%02X:%d' % (k, v) for k, v in sorted(marks.items())
                              if k in DATA_MARKS and k != 0xAD) or '     ',
                     kind, '  (also %s)' % other if other else ''))
            continue
        for gain in GAINS:
            gcr.REGRID_GAIN = gain
            for nominal in NOMINALS:
                for r in range(len(revs)):
                    nibs = gcr.bits_to_nibs(gcr.flux_to_bits(
                        revs[r] + revs[(r + 1) % len(revs)], nominal=nominal))
                    for key, res in sectors(nibs, cyl):
                        found[key].append(res)
                if all(any(c == 2 for _, c in found.get((cyl, s), ()))
                       for s in range(SECTORS)):
                    break
            else:
                continue
            break
    gcr.REGRID_GAIN = GAINS[-1]
    return found


def build(found):
    img = bytearray(TRACKS * SECTORS * SECSIZE)
    verified = 0
    for (cyl, sec), lst in found.items():
        pool = ([d for d, c in lst if c == 2] or [d for d, c in lst if c == 1]
                or [d for d, _ in lst])
        data = collections.Counter(pool).most_common(1)[0][0]
        off = (cyl * SECTORS + INVERSE[sec]) * SECSIZE
        img[off:off + SECSIZE] = data
        verified += any(c == 2 for _, c in lst)
    return bytes(img), verified


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('scp')
    ap.add_argument('-o', '--out', help='write a DOS-order .dsk here')
    ap.add_argument('--report', action='store_true',
                    help='per-track prologue census, to tell protection from damage')
    args = ap.parse_args()

    if args.report:
        print('%s:' % args.scp)
        decode(args.scp, report=True)
        return

    found = decode(args.scp)
    img, verified = build(found)
    print('recovered %d of %d sectors, %d checksum-verified'
          % (len(found), TRACKS * SECTORS, verified))
    missing = [(t, s) for t in range(TRACKS) for s in range(SECTORS)
               if (t, s) not in found]
    if missing:
        print('missing: %s' % missing[:16])
    if args.out:
        dst = pathlib.Path(args.out)
        if dst.exists():
            sys.exit('refusing to overwrite %s' % dst)
        dst.write_bytes(img)
        print('wrote %s' % dst)


if __name__ == '__main__':
    main()
