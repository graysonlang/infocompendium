#!/usr/bin/env python3
"""
appleiso.py -- extract an Apple-extended ISO 9660 image natively,
resolving resource forks and Finder metadata.

Written for discs like the Lost Treasures of Infocom CD, whose Mac files
macOS's cd9660 driver refuses to open (EINVAL) because they carry
associated-file resource forks. This reads the image directly: directory
records give names, timestamps and the associated-file flag; each
associated entry's content is the raw resource fork, and the "AA"
system-use field in each record carries type, creator and Finder flags.
(The AppleDouble "._" companions the driver shows are its own synthesis,
not what is on disc; adcopy.py's parser is kept as a fallback for
masterings that do store AppleDouble.)

Usage:
    python3 appleiso.py disc-data.iso ~/Desktop/extracted
"""

import sys
sys.dont_write_bytecode = True

import argparse
import os
import struct
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adcopy import parse_appledouble, run, SETFILE   # noqa: E402

SECTOR = 2048


def read_records(data, lba, size):
    """Yield (name, extent, length, mtime, is_dir, is_assoc) from a directory."""
    raw = data[lba * SECTOR:lba * SECTOR + size]
    pos = 0
    while pos < len(raw):
        rlen = raw[pos]
        if rlen == 0:                       # rest of this sector is empty
            pos = (pos // SECTOR + 1) * SECTOR
            continue
        r = raw[pos:pos + rlen]
        extent = struct.unpack("<I", r[2:6])[0]
        length = struct.unpack("<I", r[10:14])[0]
        y, mo, d, h, mi, s = r[18], r[19], r[20], r[21], r[22], r[23]
        try:
            mtime = time.mktime((1900 + y, mo, d, h, mi, s, 0, 0, -1))
        except (ValueError, OverflowError):
            mtime = None
        flags = r[25]
        nlen = r[32]
        name = r[33:33 + nlen].decode("ascii", "replace").split(";")[0]
        if name in ("\x00", "\x01"):
            name = ""
        su = r[33 + nlen + (1 - nlen % 2):]
        finder = None
        while len(su) >= 4:
            if su[0:2] == b"AA" and su[2] >= 14 and su[3] == 2:
                ftype, creator, fflags = su[4:8], su[8:12], su[12:14]
                finder = ftype + creator + fflags + b"\x00" * 22
                break
            if su[2] == 0:
                break
            su = su[su[2]:]
        yield name, extent, length, mtime, bool(flags & 2), bool(flags & 4), finder
        pos += rlen


def walk(data, lba, size, outdir, stats):
    os.makedirs(outdir, exist_ok=True)
    entries = [e for e in read_records(data, lba, size) if e[0]]
    associated = {}
    for name, extent, length, mtime, is_dir, is_assoc, finder in entries:
        if is_assoc:
            associated[name] = (extent, length)
    for name, extent, length, mtime, is_dir, is_assoc, finder in entries:
        if is_assoc:
            continue
        out = os.path.join(outdir, name.replace("/", "_"))
        if is_dir:
            walk(data, extent, length, out, stats)
            if mtime:
                os.utime(out, (mtime, mtime))
            continue
        with open(out, "wb") as fh:
            fh.write(data[extent * SECTOR:extent * SECTOR + length])
        stats["files"] += 1
        if name in associated:
            aext, alen = associated[name]
            blob = data[aext * SECTOR:aext * SECTOR + alen]
            rsrc = blob
            tmp = out + ".adtmp"
            with open(tmp, "wb") as fh:
                fh.write(blob)
            try:
                ad = parse_appledouble(tmp)
                rsrc = ad.get("rsrc", b"")
                if ad.get("finder") and any(ad["finder"]):
                    finder = ad["finder"]
            except ValueError:
                pass                       # raw resource fork, the usual case
            finally:
                os.remove(tmp)
            if rsrc:
                with open(out + "/..namedfork/rsrc", "wb") as fh:
                    fh.write(rsrc)
                stats["forks"] += 1
        if finder and any(finder):
            run(["xattr", "-wx", "com.apple.FinderInfo", finder.hex(), out])
        if mtime:
            os.utime(out, (mtime, mtime))
            if SETFILE:
                stamp = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(mtime))
                run([SETFILE, "-d", stamp, out])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("iso")
    ap.add_argument("dest")
    args = ap.parse_args()
    if os.path.exists(args.dest):
        sys.exit(f"already exists, move it aside first: {args.dest}")

    data = open(args.iso, "rb").read()
    pvd = data[16 * SECTOR:17 * SECTOR]
    if pvd[0] != 1 or pvd[1:6] != b"CD001":
        sys.exit("no ISO 9660 primary volume descriptor at sector 16")
    root = pvd[156:190]
    lba = struct.unpack("<I", root[2:6])[0]
    size = struct.unpack("<I", root[10:14])[0]
    stats = {"files": 0, "forks": 0, "failed": 0}
    walk(data, lba, size, args.dest, stats)
    print(f"done: {stats['files']} files ({stats['forks']} with resource forks), "
          f"{stats['failed']} companion failures")
    if stats["failed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
