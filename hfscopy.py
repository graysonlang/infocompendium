#!/usr/bin/env python3
"""
hfscopy.py -- copy an HFS volume image to a mounted HFS+ volume,
preserving resource forks, type/creator codes and timestamps.

Reads the tree from `hls -l -R` output, pulls each file out through
`hcopy -m` (MacBinary II), then unpacks the MacBinary container itself
so nothing depends on unar behaving a particular way.

Usage:
    python3 hfscopy.py --image mp-hfs.img --dest /Volumes/Masterpieces
    python3 hfscopy.py --listing mp-hfs.txt --dry-run
"""

import argparse
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

MAC_EPOCH_OFFSET = 2082844800  # seconds between 1904-01-01 and 1970-01-01

# "Jun 19  1996 " or "Feb 10 14:32 " -- everything after this is the name
DATE_RE = re.compile(r"[A-Z][a-z]{2} +\d+ +(?:\d{4}|\d{1,2}:\d{2}) ")
HEADER_RE = re.compile(r"^:.*:$")


class Entry:
    def __init__(self, kind, name, hfs_dir, type_creator=None):
        self.kind = kind              # 'f' or 'd'
        self.name = name
        self.hfs_dir = hfs_dir        # ':' or ':MAC:ARTHUR FOLDER:'
        self.type_creator = type_creator

    @property
    def hfs_path(self):
        return self.hfs_dir + self.name

    def local_path(self, dest):
        # HFS allows '/' in names; it is the separator on Unix. Swap it.
        parts = [p for p in self.hfs_dir.strip(":").split(":") if p]
        parts = [p.replace("/", "_") for p in parts]
        return os.path.join(dest, *parts, self.name.replace("/", "_"))


def parse_listing(text):
    """Parse `hls -l -R` output into a flat list of Entry objects."""
    entries = []
    current = ":"
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        if HEADER_RE.match(line):
            current = line
            continue
        if line.startswith("Volume "):
            continue
        if line[0] not in "fFd":
            continue

        m = DATE_RE.search(line)
        if not m:
            continue
        name = line[m.end():].strip()
        if not name:
            continue

        kind = "d" if line[0] == "d" else "f"
        tc = None
        if kind == "f":
            tcm = re.match(r"^[fF]\s+(\S*/\S*|\s*/\s*)", line)
            if tcm:
                tc = tcm.group(1).strip()
        entries.append(Entry(kind, name, current, tc))
    return entries


def run(cmd, check=True):
    """Run a command, surfacing the real stderr on failure rather than a bare traceback."""
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode != 0:
        msg = r.stderr.strip() or r.stdout.strip() or f"exit {r.returncode}"
        raise RuntimeError(f"{cmd[0]}: {msg}")
    return r


def unpack_macbinary(binpath, outpath):
    """Write data fork, resource fork, FinderInfo and mtime from a MacBinary II file."""
    with open(binpath, "rb") as fh:
        hdr = fh.read(128)
        if len(hdr) < 128:
            raise ValueError("short MacBinary header")

        ftype = hdr[65:69]
        creator = hdr[69:73]
        flags_hi = hdr[73]
        flags_lo = hdr[101]
        datalen = struct.unpack(">I", hdr[83:87])[0]
        rsrclen = struct.unpack(">I", hdr[87:91])[0]
        mtime_mac = struct.unpack(">I", hdr[95:99])[0]

        data = fh.read(datalen)
        pad = (-datalen) % 128
        fh.read(pad)
        rsrc = fh.read(rsrclen)

    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, "wb") as out:
        out.write(data)

    if rsrclen:
        with open(outpath + "/..namedfork/rsrc", "wb") as out:
            out.write(rsrc)

    # com.apple.FinderInfo: type, creator, flags, location, folder, 16 bytes ext
    finfo = ftype + creator + bytes([flags_hi, flags_lo]) + b"\x00" * 22
    run(["xattr", "-wx", "com.apple.FinderInfo", finfo.hex(), outpath], check=False)

    if mtime_mac > MAC_EPOCH_OFFSET:
        unix_mtime = mtime_mac - MAC_EPOCH_OFFSET
        try:
            os.utime(outpath, (unix_mtime, unix_mtime))
        except OSError:
            pass

    return datalen, rsrclen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", help="HFS disk image (passed to hmount)")
    ap.add_argument("--listing", help="pre-captured `hls -l -R` output")
    ap.add_argument("--dest", help="mounted HFS+ volume to write into")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.listing:
        text = open(args.listing, encoding="utf-8", errors="replace").read()
    elif args.image:
        # hfsutils keeps mount state in ~/.hcwd between invocations; a mount left
        # open by an earlier command blocks this one with "unable to obtain lock".
        run(["humount"], check=False)
        run(["hmount", args.image])
        text = run(["hls", "-l", "-R"]).stdout
    else:
        ap.error("need --image or --listing")

    entries = parse_listing(text)
    dirs = [e for e in entries if e.kind == "d"]
    files = [e for e in entries if e.kind == "f"]

    print(f"parsed {len(entries)} entries: {len(dirs)} directories, {len(files)} files")

    if args.dry_run:
        forked = [e for e in files if e.type_creator and e.type_creator.startswith("APPL")]
        print(f"  {len(forked)} APPL files (resource forks matter)")
        for e in entries[:8]:
            print(f"  {e.kind}  {e.hfs_path}")
        print("  ...")
        return

    if not args.dest:
        ap.error("--dest required unless --dry-run")

    for e in dirs:
        os.makedirs(e.local_path(args.dest), exist_ok=True)

    tmpdir = tempfile.mkdtemp()
    ok = failed = 0
    total_rsrc = 0
    try:
        by_dir = {}
        for e in files:
            by_dir.setdefault(e.hfs_dir, []).append(e)

        for hfs_dir, group in by_dir.items():
            run(["hcd", hfs_dir], check=False)
            for e in group:
                tmp = os.path.join(tmpdir, "item.bin")
                try:
                    r = run(["hcopy", "-m", ":" + e.name, tmp], check=False)
                    if r.returncode != 0 or not os.path.exists(tmp):
                        raise RuntimeError(r.stderr.strip() or "hcopy failed")
                    _, rsrclen = unpack_macbinary(tmp, e.local_path(args.dest))
                    total_rsrc += 1 if rsrclen else 0
                    ok += 1
                except Exception as exc:                      # noqa: BLE001
                    failed += 1
                    print(f"  FAIL {e.hfs_path}: {exc}", file=sys.stderr)
                finally:
                    if os.path.exists(tmp):
                        os.remove(tmp)
                if ok % 100 == 0 and ok:
                    print(f"  {ok}/{len(files)}...")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        run(["humount"], check=False)

    print(f"done: {ok} copied ({total_rsrc} with resource forks), {failed} failed")


if __name__ == "__main__":
    main()
