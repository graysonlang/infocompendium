#!/usr/bin/env python3
"""
xzip18.py -- recover the 18-sector second surface of an Infocom Apple II
XZIP (v5) diskette from Greaseweazle raw flux (.scp).

An XZIP title larger than 100,864 bytes puts the first 394 sectors of its
story on a 16-sector surface and the remainder on an 18-sector one.  That
second surface has NO ADDRESS FIELDS: one D5 AA AD mark per track, then a
two-byte 4-and-4 track number, then 18 data fields of 343 nibbles (342
six-and-two GCR plus a running-XOR checksum) at exactly 5 + 343*n from the
mark.  Story blocks map linearly: block b at track b // 18, sector b % 18.

The layout follows S. V. Nickolas's interlz5.c, which writes these images,
and Infocom's own RDFSEC routine ("read sector from big track") in the
leaked XZIP interpreter source, which reads them.  No stock Apple decoder
can read this surface, so a capture that reports 0 sectors is expected and
says nothing about whether the disc is good.

Two things matter when slicing the flux and neither is a guess:

  * The bit cell is NOT 4000 ns.  This media was written at 300 RPM; a
    360 RPM drive such as the TEAC FD-55GFR reads it 6/5 fast, putting the
    cell near 3355 ns.  The period is fitted per track.
  * These captures carry spurious flux reversals inside 3-cell gaps: a
    10,020 ns gap arrives as roughly 5,828 + 3,828, which slices to "011"
    instead of "001".  That single 0->1 bit flip destroys the rest of the
    sector through the running-XOR chain.  Neither piece fits the cell grid
    while their sum does, so the pair is recovered by re-fitting.

Do not trust the per-sector checksum on its own: it is six bits, so about
one bad sector in 64 passes it.  Measured against known builds, 228 of 231
sectors passed the checksum while 227 were actually correct.

Usage:
    python3 xzip18.py --prefix SIDE1.dat -o STORY.z5 capture.scp [more.scp]
    python3 xzip18.py --blocks-out DIR capture.scp [more.scp]
"""

import sys
sys.dont_write_bytecode = True

import argparse
import collections
import multiprocessing
import pathlib
import re
import struct

SECNIBS, NSEC, HDRNIBS, SIDE1_BYTES = 343, 18, 5, 100864

# Six-and-two write table.  Identical to interlz5.c's translate[] and to the
# table Apple DOS 3.3 writes; listed here so the tool stands alone.
TRANSLATE = [
    0x96, 0x97, 0x9A, 0x9B, 0x9D, 0x9E, 0x9F, 0xA6,
    0xA7, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB2, 0xB3,
    0xB4, 0xB5, 0xB6, 0xB7, 0xB9, 0xBA, 0xBB, 0xBC,
    0xBD, 0xBE, 0xBF, 0xCB, 0xCD, 0xCE, 0xCF, 0xD3,
    0xD6, 0xD7, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD, 0xDE,
    0xDF, 0xE5, 0xE6, 0xE7, 0xE9, 0xEA, 0xEB, 0xEC,
    0xED, 0xEE, 0xEF, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6,
    0xF7, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF,
]
UNTRANS = {v: i for i, v in enumerate(TRANSLATE)}

# Regrid aggressiveness.  Tuned against two builds with known contents; the
# optimum is sharp, so change it only with a reference to measure against.
REGRID_GAIN = 0.0875
# The regrid setting that is right for a clean track is WRONG for a marginal
# one. A noisy track has larger fit residuals everywhere, so an aggressive
# setting merges real transitions and silently shortens the track - measurable
# as a mark-to-mark gap too small to hold the 6179 nibbles the format needs.
# Beyond Zork's track 28 went from 0 to 15 of 18 sectors purely by easing off.
# Span both regimes rather than picking one; 1.0 effectively disables merging.
# Ordered so the FIRST two span both extremes: 1.0 leaves the flux alone, which
# is right for a clean capture (see --densel below), and 0.0875 repairs false
# transitions, which is right for a drive that produces them. The abandon-early
# test below consults both before giving up on a position - probing with only
# one silently loses every track that needs the other.
GAINS = (1.0, 0.0875, 0.095, 0.070, 0.15, 0.30)

# Cap on revolutions used per capture position, since slicing is the expensive
# step. Do NOT set this low on marginal media: on a degraded track, finding the
# sync mark at all is probabilistic per revolution - measured here, one track's
# mark appeared in 2 revolutions out of 10 and another's in 4. Capping at 6 lost
# a whole track of Beyond Zork that 10 revolutions recovered.
MAX_REVS = 20


def _read_maybe_zst(path):
    """Read a capture, transparently decompressing a zstd-compressed one.

    Flux compresses to roughly a quarter of its size losslessly, which matters
    when captures are kept for provenance: compress BEFORE committing one, since
    a git blob is permanent and compressing afterwards only adds a second copy.
    """
    raw = pathlib.Path(path).read_bytes()
    if raw[:4] == b'\x28\xb5\x2f\xfd':
        from compression import zstd
        return zstd.decompress(raw)
    return raw


def scp_tracks(path, reverse=False):
    """Read an SCP capture into {index: [flux intervals in ns, per revolution]}.

    reverse=True time-reverses each revolution, for a second surface read in
    place through head 1 with the disc in its normal orientation. That surface
    was written with the disc flipped, so in place it passes the head backwards.
    Reversing the interval sequence undoes exactly that.
    """
    d = _read_maybe_zst(path)
    if d[:3] != b'SCP':
        raise ValueError("%s is not an SCP capture" % path)
    tick = 25 * (d[11] + 1)
    offs = struct.unpack('<168I', d[16:16 + 168 * 4])
    out = {}
    for i, o in enumerate(offs):
        if o == 0 or d[o:o + 3] != b'TRK':
            continue
        revs = []
        for r in range(d[5]):
            _, ln, do = struct.unpack('<III', d[o + 4 + r * 12:o + 16 + r * 12])
            vals = struct.unpack('>%dH' % ln, d[o + do:o + do + ln * 2])
            fl, acc = [], 0
            for v in vals:
                if v == 0:
                    acc += 65536
                else:
                    fl.append((acc + v) * tick)
                    acc = 0
            revs.append(fl[::-1] if reverse else fl)
        out[i] = revs
    return out


def estimate_cell(flux, start=3400.0, iters=6):
    """Least-squares fit of the bit-cell period.  Do not assume 4000 ns."""
    c = start
    for _ in range(iters):
        num = den = 0
        for x in flux:
            n = int(x / c + 0.5)
            n = 1 if n < 1 else (3 if n > 3 else n)
            num += x
            den += n
        if den:
            c = num / den
    return c


def despike(flux, cell, thresh=0.55):
    """Drop transitions closer together than the media can hold."""
    out = []
    for t in flux:
        if out and t < cell * thresh:
            out[-1] += t
        else:
            out.append(t)
    return out


def regrid(flux, cell, gain=None, keep=0.10):
    """Merge adjacent intervals when the pair fits the cell grid and the
    parts do not - this removes the spurious reversal inside a 3-cell gap."""
    if gain is None:
        gain = REGRID_GAIN

    def res(x):
        n = max(1, min(3, int(x / cell + 0.5)))
        return abs(x - n * cell), n

    out, i = [], 0
    while i < len(flux):
        if i + 1 < len(flux):
            e1, _ = res(flux[i])
            e2, _ = res(flux[i + 1])
            m = flux[i] + flux[i + 1]
            em, nm = res(m)
            if nm <= 3 and em < keep * cell and (e1 + e2) > em + gain * cell:
                out.append(m)
                i += 2
                continue
        out.append(flux[i])
        i += 1
    return out


def flux_to_bits(flux, nominal=None, gain=0.10):
    """Slice flux into bit cells.  Six-and-two GCR never has three
    consecutive zero bits, so an interval is only ever 1, 2 or 3 cells."""
    if nominal is None:
        nominal = estimate_cell(flux)
    flux = regrid(despike(flux, nominal), nominal)
    clock, bits = nominal, bytearray()
    for t in flux:
        n = int(t / clock + 0.5)
        n = 1 if n < 1 else (3 if n > 3 else n)
        bits.extend(b'\0' * (n - 1))
        bits.append(1)
        clock += (t / n - clock) * gain
        clock = min(max(clock, nominal * 0.93), nominal * 1.07)
    return bits


def bits_to_nibs(bits):
    """Emulate the Disk II read latch: a byte completes when its top bit is set."""
    reg, out = 0, bytearray()
    for b in bits:
        reg = ((reg << 1) | b) & 0xFF
        if reg & 0x80:
            out.append(reg)
            reg = 0
    return out


def de44(a, b):
    return ((a << 1) | 1) & b


def decode_sector(nibs, off):
    """Invert interlz5's mksec().  Returns (bytes, checksum_ok) or None.

    A nibble that is not one of the 64 valid six-and-two bytes is an error
    whose POSITION is known, which makes it an erasure rather than a guess.
    One such erasure is exactly correctable: every value from it onward is
    off by the same unknown constant, and the trailing checksum nibble pins
    that constant.  Discarding these sectors instead - as an earlier version
    did - throws away everything the inner tracks have to offer, since a
    marginal track puts roughly one invalid nibble in each sector.
    """
    if off + SECNIBS > len(nibs):
        return None
    d = [UNTRANS.get(nibs[off + k]) for k in range(343)]
    bad = [k for k in range(342) if d[k] is None]
    if len(bad) > 1 or d[342] is None and bad:
        return None

    vals, run = [], 0
    for k in range(342):
        run ^= (d[k] or 0)
        vals.append(run)

    if bad:                       # solve the erasure from the checksum
        c = vals[341] ^ d[342]
        k = bad[0]
        vals = [v if i < k else v ^ c for i, v in enumerate(vals)]
        conf = 1                  # correcting CONSUMES the checksum, so this
                                  # sector is no longer independently verified:
                                  # rank it below a clean one or it will
                                  # displace good decodes from other captures
    else:
        conf = 2 if (d[342] is not None and (run ^ d[342]) == 0) else 0

    b = bytearray(256)
    for i in range(256):
        if i < 0x56:
            lo, sh = vals[i], 0
        elif i < 0xAC:
            lo, sh = vals[i - 0x56], 2
        else:
            lo, sh = vals[i - 0xAC], 4
        two = (lo >> sh) & 3
        b[i] = ((vals[0x56 + i] << 2) | ((two & 1) << 1) | ((two >> 1) & 1)) & 0xFF
    return bytes(b), conf


def _sectors_ok(seg):
    return sum(1 for s in range(NSEC)
               if (lambda r: r is not None and r[1] == 2)(
                   decode_sector(seg, HDRNIBS + SECNIBS * s)))


def track_runs(revs):
    """Nibble runs for one capture position, anchored on the track's own mark.

    Each revolution is joined to the next so a sector straddling the index is
    contiguous.  The track number comes from the disc, so nothing depends on
    guessing how a capture maps cylinders onto SCP indices.

    Three economies, because the gain ensemble is brute force and most work is
    wasted without them: the cell period is fitted once per revolution pair
    rather than once per gain, a position with no mark at the first gain is
    abandoned immediately (a step=1 sweep stores 160 positions of which only
    about 35 hold anything), and a track that is already fully verified does
    not try the remaining gains.
    """
    global REGRID_GAIN
    runs, tno = [], None
    nrev = min(len(revs), MAX_REVS)
    joined = [(revs[r] + revs[(r + 1) % len(revs)]) for r in range(nrev)]
    cells = [estimate_cell(f) for f in joined]

    for gi, g in enumerate(GAINS):
        REGRID_GAIN = g
        for f, cell in zip(joined, cells):
            nibs = bits_to_nibs(flux_to_bits(f, nominal=cell))
            for mk in range(len(nibs) - 4):
                if nibs[mk] != 0xD5 or nibs[mk + 1] != 0xAA or nibs[mk + 2] != 0xAD:
                    continue
                t = de44(nibs[mk + 3], nibs[mk + 4])
                if not 0 <= t < 35:
                    continue
                seg = nibs[mk:mk + HDRNIBS + SECNIBS * NSEC]
                if len(seg) == HDRNIBS + SECNIBS * NSEC:
                    runs.append(bytes(seg))
                    tno = t
                break
        if gi == 1 and tno is None:
            break                       # neither extreme found a mark; give up
        if runs and max(_sectors_ok(r) for r in runs) == NSEC:
            break                       # already complete
    REGRID_GAIN = GAINS[0]
    return runs, tno


VALIDSET = frozenset(TRANSLATE)


def cluster(runs, probe=600, thresh=0.55):
    """Keep only runs that are in positional agreement with each other.

    A single dropped or inserted nibble shifts everything after it, so two
    reads of the same track can share almost no positions. Merging across that
    produces a stream of individually-valid nibbles that is collectively wrong
    - which looks like clean data and is not. Measured here, aligned runs of
    one track agreed at 78-100% while misaligned ones sat at 3-20%, so the
    threshold goes between the two populations, not near 100%: on a marginal
    track each run is itself only ~88% valid, and two good runs of it will
    still differ in a fifth of their positions.
    """
    if len(runs) < 3:
        return runs
    best, bestn = runs[:1], 0
    for ref in runs:
        grp = [r for r in runs
               if sum(1 for a, b in zip(ref[:probe], r[:probe]) if a == b) >= probe * thresh]
        if len(grp) > bestn:
            best, bestn = grp, len(grp)
    return best


def vote(runs):
    """Merge nibble streams position by position.

    Prefer values that are valid six-and-two bytes: a value outside the 64 is
    certainly wrong, so a single capture that read it correctly outweighs any
    number that did not. On marginal tracks the invalid positions differ
    between captures and between heads, so this recovers far more than a plain
    majority, which a consistently-misread nibble can carry.
    """
    if len(runs) < 2:
        return runs[0] if runs else None
    out = bytearray(len(runs[0]))
    for i in range(len(out)):
        col = [r[i] for r in runs]
        good = [v for v in col if v in VALIDSET]
        out[i] = collections.Counter(good or col).most_common(1)[0][0]
    return bytes(out)


_CACHE = {}


def _load(path, reverse):
    key = (path, reverse)
    if key not in _CACHE:
        _CACHE[key] = scp_tracks(path, reverse)
    return _CACHE[key]


def _work(job):
    """Decode one capture position. Module level so it can be sent to a pool."""
    path, reverse, idx = job
    runs, tno = track_runs(_load(path, reverse)[idx])
    return path, tno, runs


def surface(scps, nblk, reversed_scps=(), jobs=None):
    """Decode the 18-sector surface from one or more captures of it.

    Captures listed in reversed_scps are time-reversed first. Mixing normal and
    reversed captures is fine: each track is identified by the 4-and-4 number
    the disc itself records, so nothing depends on knowing a head offset.

    Each capture position is independent, so they are spread across cores.
    """
    work = []
    for s in scps:
        rev = s in reversed_scps
        for idx in _load(s, rev):
            work.append((s, rev, idx))

    if jobs is None:
        jobs = min(len(work), multiprocessing.cpu_count()) or 1

    # Keep captures SEPARATE until candidates are formed. Clustering pooled
    # runs from different captures mixes streams that are merely misaligned
    # with each other, and the merged result looks clean while being wrong.
    # Clustering within each capture first was worth 5 sectors on Border Zone.
    per = collections.defaultdict(lambda: collections.defaultdict(list))
    if jobs > 1:
        _CACHE.clear()                  # children load their own; do not fork it
        with multiprocessing.Pool(jobs) as pool:
            for src, tno, runs in pool.imap_unordered(_work, work, chunksize=1):
                if tno is not None:
                    per[src][tno].extend(runs)
    else:
        for job in work:
            src, tno, runs = _work(job)
            if tno is not None:
                per[src][tno].extend(runs)

    # candidate -> [captures that produced it, run count, best confidence]
    cand = collections.defaultdict(lambda: collections.defaultdict(
        lambda: [set(), 0, -1]))
    for src, tracks in per.items():
        for cyl, runs in tracks.items():
            grp = cluster(runs)
            for c in ([vote(grp)] if len(grp) > 1 else []) + grp + runs:
                for s in range(NSEC):
                    b = cyl * NSEC + s
                    if b >= nblk:
                        break
                    res = decode_sector(c, HDRNIBS + SECNIBS * s)
                    if res is None:
                        continue
                    data, conf = res
                    e = cand[b][data]
                    e[0].add(src)
                    e[1] += 1
                    e[2] = max(e[2], conf)

    blocks, ck = {}, {}
    for b, opts in cand.items():
        data = max(opts.items(),
                   key=lambda kv: (kv[1][2], len(kv[1][0]), kv[1][1]))[0]
        blocks[b], ck[b] = data, opts[data][2]
    return blocks, ck


# DOS 3.3 sector interleave, as interlz5.c's interl[] and Infocom's own RWTS
# table. Side 1's story area is interleaved through this; tracks 0-3, holding
# the boot code and interpreter, are not.
INTERLEAVE = [0x0, 0xD, 0xB, 0x9, 0x7, 0x5, 0x3, 0x1,
              0xE, 0xC, 0xA, 0x8, 0x6, 0x4, 0x2, 0xF]


def side1_prefix(dsk_path):
    """Pull the story's first 100,864 bytes out of a 16-sector side-1 image.

    The XZIP stub occupies the first 64 sectors (tracks 0-3); the story starts
    at sector 64 and runs 394 sectors, each located through the FORWARD
    interleave. Reading the story SEQUENCE uses the forward table; locating a
    physical sector inside an appledos image uses its inverse. Confusing the two
    yields a readable header followed by garbage.
    """
    dsk = pathlib.Path(dsk_path).read_bytes()
    if len(dsk) != 143360:
        raise ValueError("%s is not a 143,360-byte appledos image" % dsk_path)
    out = bytearray()
    for k in range(64, 64 + 394):
        trk, sec = divmod(k, 16)
        off = (trk * 16 + INTERLEAVE[sec]) * 256
        out += dsk[off:off + 256]
    return bytes(out)


def zheader(data):
    scale = {1: 2, 2: 2, 3: 2, 4: 4, 5: 4, 6: 8, 7: 8, 8: 8}[data[0]]
    length = int.from_bytes(data[0x1A:0x1C], 'big') * scale
    return (data[0], int.from_bytes(data[2:4], 'big'),
            data[0x12:0x18].decode('latin1'), length,
            int.from_bytes(data[0x1C:0x1E], 'big'))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('scp', nargs='+', help='raw flux captures of the 18-sector surface')
    ap.add_argument('--max-revs', type=int, default=MAX_REVS,
                    help='revolutions to use per capture position '
                         '(default %d); raise it for marginal media' % MAX_REVS)
    ap.add_argument('-j', '--jobs', type=int, default=None,
                    help='worker processes (default: one per core)')
    ap.add_argument('--reverse', metavar='SCP', action='append', default=[],
                    help='treat this capture as time-reversed (a head-1 read of '
                         'the second surface with the disc the normal way up); '
                         'repeatable, and it must also appear in the scp list')
    ap.add_argument('--prefix', help='the 100,864-byte story prefix read from side 1')
    ap.add_argument('--side1', metavar='DSK',
                    help='side-1 appledos .dsk to take that prefix from directly, '
                         'instead of a pre-extracted --prefix file')
    ap.add_argument('-o', '--out', help='write the assembled story file here')
    ap.add_argument('--blocks-out', help='write each recovered block as DIR/NNNN.bin')
    args = ap.parse_args()
    globals()['MAX_REVS'] = args.max_revs

    if args.side1 and args.prefix:
        sys.exit('give --side1 or --prefix, not both')
    if args.side1 or args.prefix:
        prefix = (side1_prefix(args.side1) if args.side1
                  else pathlib.Path(args.prefix).read_bytes())
        if len(prefix) != SIDE1_BYTES:
            sys.exit('prefix must be exactly %d bytes' % SIDE1_BYTES)
        ver, rel, ser, length, declared = zheader(prefix)
        nblk = (length - SIDE1_BYTES + 255) // 256
        print('v%d r%d.%s, %d bytes: %d blocks on the 18-sector surface'
              % (ver, rel, ser, length, nblk))
    else:
        prefix, nblk, length, declared = None, 35 * NSEC, None, None

    blocks, ck = surface(args.scp, nblk, set(args.reverse), args.jobs)
    missing = sorted(set(range(nblk)) - set(blocks))
    print('recovered %d/%d blocks (%d passed the sector checksum)'
          % (len(blocks), nblk, sum(1 for c in ck.values() if c == 2)))
    if missing:
        bad = sorted({b // NSEC for b in missing})
        print('missing %d blocks, on tracks %s' % (len(missing), bad))

    if args.blocks_out:
        d = pathlib.Path(args.blocks_out)
        d.mkdir(parents=True, exist_ok=True)
        for b, data in sorted(blocks.items()):
            (d / ('%04d.bin' % b)).write_bytes(data)

    if args.out and prefix:
        body = bytearray(prefix)
        for b in range(nblk):
            body += blocks.get(b, b'\0' * 256)
        body = bytes(body[:length])
        pathlib.Path(args.out).write_bytes(body)
        calc = sum(body[0x40:length]) % 0x10000
        print('wrote %s; z-checksum declared %04X computed %04X -> %s'
              % (args.out, declared, calc, 'MATCH' if declared == calc else 'MISMATCH'))
        if declared != calc:
            print('the story is incomplete; re-read the tracks listed above '
                  'with more revolutions (--revs=20) and pass both captures')


if __name__ == '__main__':
    main()
