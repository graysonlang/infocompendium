#!/usr/bin/env python3
"""
raw2user.py -- convert a raw 2352-byte/sector CD image (Mode 1) to
2048-byte/sector user data, verifying sector structure along the way.

A raw Mode 1 sector is:
    12 bytes sync (00 ff ff ff ff ff ff ff ff ff ff 00)
     4 bytes header (minute, second, frame in BCD; mode)
  2048 bytes user data
     4 bytes EDC (CRC over bytes 0..2063, little endian)
     8 bytes reserved
   276 bytes ECC

Every sector's sync, mode and address header are checked. The EDC is
checked on a sample (every Nth sector) because a full pass is slow in
Python; use --edc-all if you want it anyway.

Prints CRC32/MD5/SHA-1 for both the raw input and the converted output,
in the shape Redump publishes, so a dump can be recorded and compared.

Usage:
    python3 raw2user.py disc-raw.bin disc-user.img
"""

import argparse
import hashlib
import os
import sys
import zlib

SECTOR_RAW = 2352
SECTOR_USER = 2048
SYNC = bytes([0x00]) + b"\xff" * 10 + bytes([0x00])

# ECMA-130 EDC: 32-bit CRC, LSB first, polynomial 0xd8018001.
_EDC_TABLE = []
for i in range(256):
    v = i
    for _ in range(8):
        v = (v >> 1) ^ (0xd8018001 if v & 1 else 0)
    _EDC_TABLE.append(v)


def edc(data):
    v = 0
    for b in data:
        v = _EDC_TABLE[(v ^ b) & 0xff] ^ (v >> 8)
    return v


def unbcd(b):
    return (b >> 4) * 10 + (b & 0x0f)


class Hashes:
    def __init__(self):
        self.crc = 0
        self.md5 = hashlib.md5()
        self.sha1 = hashlib.sha1()

    def update(self, data):
        self.crc = zlib.crc32(data, self.crc)
        self.md5.update(data)
        self.sha1.update(data)

    def report(self, label, size):
        print(f"{label}: {size} bytes")
        print(f"  crc32 {self.crc & 0xffffffff:08x}")
        print(f"  md5   {self.md5.hexdigest()}")
        print(f"  sha1  {self.sha1.hexdigest()}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", help="input, raw 2352-byte sectors")
    ap.add_argument("out", help="output, 2048-byte user data per sector")
    ap.add_argument("--edc-sample", type=int, default=250,
                    help="check EDC on every Nth sector (default 250)")
    ap.add_argument("--edc-all", action="store_true",
                    help="check EDC on every sector (slow)")
    args = ap.parse_args()

    size = os.path.getsize(args.raw)
    if size % SECTOR_RAW:
        sys.exit(f"input size {size} is not a multiple of {SECTOR_RAW}")
    nsec = size // SECTOR_RAW

    if os.path.exists(args.out):
        sys.exit(f"already exists, move it aside first: {args.out}")

    hin, hout = Hashes(), Hashes()
    bad_sync = bad_addr = bad_mode = bad_edc = edc_checked = 0

    with open(args.raw, "rb") as src, open(args.out, "wb") as dst:
        for sec in range(nsec):
            raw = src.read(SECTOR_RAW)
            if len(raw) != SECTOR_RAW:
                sys.exit(f"short read at sector {sec}")
            hin.update(raw)

            if raw[:12] != SYNC:
                bad_sync += 1
            hdr = raw[12:16]
            if hdr[3] != 1:
                bad_mode += 1
            lba = (unbcd(hdr[0]) * 60 + unbcd(hdr[1])) * 75 + unbcd(hdr[2]) - 150
            if lba != sec:
                bad_addr += 1

            if args.edc_all or sec % args.edc_sample == 0:
                edc_checked += 1
                stored = int.from_bytes(raw[2064:2068], "little")
                if edc(raw[:2064]) != stored:
                    bad_edc += 1
                    print(f"  EDC mismatch at sector {sec}", file=sys.stderr)

            user = raw[16:16 + SECTOR_USER]
            dst.write(user)
            hout.update(user)

            if sec and sec % 25000 == 0:
                print(f"  {sec}/{nsec}...")

    print(f"{nsec} sectors converted")
    print(f"  bad sync: {bad_sync}  bad address: {bad_addr}  bad mode: {bad_mode}")
    print(f"  EDC checked on {edc_checked} sectors, {bad_edc} mismatches")
    hin.report("raw input", size)
    hout.report("user data", nsec * SECTOR_USER)

    if bad_sync or bad_addr or bad_mode or bad_edc:
        sys.exit("structure errors found; do not trust this conversion")


if __name__ == "__main__":
    main()
