#!/usr/bin/env python3
"""
adcopy.py -- copy a directory tree, resolving AppleDouble "._" companion
files into real resource forks and Finder metadata.

Made for ISO 9660 discs with Apple extensions (e.g. the Lost Treasures of
Infocom CD), where macOS shows each Mac file's metadata as a literal
"._Name" sibling that cp/ditto do not merge back. Each companion is parsed
and its pieces written natively: resource fork to path/..namedfork/rsrc,
Finder info to the com.apple.FinderInfo xattr, dates via os.utime (and
SetFile -d for creation dates, when the Xcode tools are present).

AppleDouble integers are big-endian per the spec, but some 1990s mastering
tools wrote them little-endian; both are handled, keyed off the magic.

Usage:
    python3 adcopy.py /Volumes/INFOCOM ~/Desktop/extracted
"""

import sys
sys.dont_write_bytecode = True

import argparse
import os
import shutil
import struct
import subprocess

MAGIC_BE = 0x00051607
AD_EPOCH = 946684800          # 2000-01-01, epoch of AppleDouble date entries
SETFILE = shutil.which("SetFile")


def parse_appledouble(path):
    """Return dict with optional 'finder' (32 bytes), 'rsrc' (bytes), 'dates'."""
    data = open(path, "rb").read()
    if len(data) < 26:
        raise ValueError("too short for AppleDouble")
    if struct.unpack(">I", data[0:4])[0] == MAGIC_BE:
        e = ">"
    elif struct.unpack("<I", data[0:4])[0] == MAGIC_BE:
        e = "<"
    else:
        raise ValueError("no AppleDouble magic in either byte order")
    nent = struct.unpack(e + "H", data[24:26])[0]
    out = {}
    for i in range(nent):
        eid, off, length = struct.unpack(e + "III", data[26 + 12*i:26 + 12*i + 12])
        blob = data[off:off + length]
        if eid == 9 and length >= 32:
            out["finder"] = blob[:32]
        elif eid == 2:
            out["rsrc"] = blob
        elif eid == 8 and length >= 16:
            create, modify = struct.unpack(e + "ii", blob[:8])
            out["dates"] = (create + AD_EPOCH, modify + AD_EPOCH)
    return out


def run(cmd):
    subprocess.run(cmd, capture_output=True)


def apply_companion(companion, outpath):
    ad = parse_appledouble(companion)
    rsrc = ad.get("rsrc")
    if rsrc:
        with open(outpath + "/..namedfork/rsrc", "wb") as fh:
            fh.write(rsrc)
    finder = ad.get("finder")
    if finder and any(finder):
        run(["xattr", "-wx", "com.apple.FinderInfo", finder.hex(), outpath])
    dates = ad.get("dates")
    if dates:
        create, modify = dates
        try:
            os.utime(outpath, (modify, modify))
        except OSError:
            pass
        if SETFILE and create > 0:
            import time
            stamp = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(create))
            run([SETFILE, "-d", stamp, outpath])
    return len(rsrc) if rsrc else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dest")
    args = ap.parse_args()

    if os.path.exists(args.dest):
        sys.exit(f"already exists, move it aside first: {args.dest}")
    if not SETFILE:
        print("SetFile not found; creation dates will not be restored", file=sys.stderr)

    copied = forks = failed = 0
    dir_times = []
    for root, dirs, files in os.walk(args.src):
        rel = os.path.relpath(root, args.src)
        outdir = args.dest if rel == "." else os.path.join(args.dest, rel)
        os.makedirs(outdir, exist_ok=True)
        dir_times.append((outdir, os.stat(root).st_mtime))
        for name in sorted(files):
            if name.startswith("._"):
                continue
            src = os.path.join(root, name)
            out = os.path.join(outdir, name)
            try:
                shutil.copyfile(src, out)
                st = os.stat(src)
                os.utime(out, (st.st_mtime, st.st_mtime))
                companion = os.path.join(root, "._" + name)
                if os.path.exists(companion):
                    forks += 1 if apply_companion(companion, out) else 0
                copied += 1
            except Exception as exc:                       # noqa: BLE001
                failed += 1
                print(f"  FAIL {os.path.join(rel, name)}: {exc}", file=sys.stderr)
    # Directory mtimes last: writing files into them bumped them.
    for outdir, mtime in reversed(dir_times):
        try:
            os.utime(outdir, (mtime, mtime))
        except OSError:
            pass

    print(f"done: {copied} files copied ({forks} with resource forks), {failed} failed")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
