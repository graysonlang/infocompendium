# Knowledge transfer: imaging hybrid Mac/PC CD-ROMs on modern macOS

Everything below was established against a physical copy of *Classic Text Adventure Masterpieces of Infocom* (Activision, 1996) on an Apple Silicon Mac with an external Pioneer BD-RW BDR-XS07U.
Findings that are specific to that disc are marked as such. The method generalises to the other Activision Infocom compilations, which were built the same way.

## 1. What these discs are

A hybrid CD carries a single Mode 1 data track holding **two filesystem catalogues over one set of data blocks**. The PC reads an ISO 9660 catalogue; the Mac reads an HFS catalogue. Most content exists once and is indexed twice.

This is not the same as a *mixed mode* disc, which is a data track followed by Red Book audio tracks. Check with `drutil toc` before assuming: one track means hybrid.

Consequences worth internalising:

- The ISO slice can be tiny while the HFS volume holds everything. On Masterpieces the ISO slice is 260 KB and the HFS volume is 308 MB. The ISO slice is a pointer structure, not a copy of the content.
- The two catalogues do not necessarily index identical sets. Masterpieces has genuinely separate `MAC` and `PC` directory trees with different game files in each.
- The same bytes can present differently per side. A file may appear as a plain DOS file to the ISO catalogue and as a typed Mac document (creator `mdos`) to the HFS catalogue.

## 2. Why macOS fights you

macOS removed HFS (not HFS+) support in Ventura. `diskutil` still *identifies* an HFS volume - it reads the master directory block directly - but the mount subsystem refuses it. On an Apple-partitioned hybrid it appears to refuse the whole disc, including the ISO slice that it could in principle still handle.

Observed on the test machine:

```
diskutil mount readOnly disk8s1
Volume on disk8s1 failed to mount
diskutil mount readOnly disk8s1s2
Volume on disk8s1s2 failed to mount
```

No flag changes this. Do not spend time on it. Read the raw device instead, and use `hfsutils`, which implements HFS itself and does not care what the OS supports.

## 3. Identifying a disc

```
diskutil list                        # find the device node
diskutil info /dev/diskN
diskutil list diskN                  # slice breakdown
drutil status                        # session and track count, block count
drutil toc
```

Expected shape for a hybrid, using Masterpieces as the reference:

```
0:        CD_partition_scheme      *354.0 MB   disk8
1:     Apple_partition_scheme       308.3 MB   disk8s1
2:        Apple_partition_map       1.5 KB     disk8s1s1
3:             ISO9660_system       260.6 KB   disk8s1s2
4:                  Apple_HFS       308.0 MB   disk8s1s3
```

`drutil status` reported `blocks: 150515 / 308.25MB`. That block count is the number to verify any image against: `150515 x 2048 = 308,254,720` bytes of user data.

**The 354 MB figure is not the payload.** `Device Block Size: 2352 Bytes` in `diskutil info` is the raw sector including subchannel and ECC overhead. Dividing through gets you back to the ~308 MB of actual data.

### Confirming filesystems directly

If you want signatures rather than `diskutil`'s word for it:

```
# ISO 9660 primary volume descriptor, sector 16, expect "CD001"
sudo dd if=/dev/rdiskNsXsY bs=2048 count=1 skip=16 | xxd | head -3

# HFS master directory block at byte 0x400, expect "BD" (HFS) or "H+" (HFS+)
sudo dd if=/dev/rdiskNsXsY bs=2048 count=1 | xxd | sed -n '65,68p'
```

The MDB read also gives you the volume name as a Pascal string and the creation/modification dates as Mac timestamps (seconds since 1904-01-01; subtract 2082844800 for Unix time).

Note that `skip=16` against a *slice* device is sector 16 of the slice, not of the filesystem, so on a partitioned disc you may land on the volume descriptor set terminator (leading byte `ff`) rather than the primary descriptor (leading byte `01`). Both prove ISO 9660 is present. Walk back a sector or two if you want the PVD specifically.

Anything dated before early 1998 will be plain HFS, not HFS+. HFS+ shipped with Mac OS 8.1.

## 4. Imaging: the traps

### Trap 1 - raw device block size

`/dev/rdiskN` rejects reads that are not a multiple of the drive's physical block size. On the Pioneer, that is 2352, so `bs=2048` fails on **every** read:

```
sudo dd if=/dev/rdisk8 of=out.img bs=2048 conv=noerror,sync
dd: /dev/rdisk8: Invalid argument
```

### Trap 2 - `conv=noerror,sync` turns that into silent data loss

Paired with trap 1, `conv=noerror,sync` responds to each rejected read by writing 2048 zero bytes and moving on. The result is a full-size image containing nothing, produced at RAM speed. The tell is the transfer rate: real optical reads run at a few MB/s, so figures like 140 MB/s mean fabrication.

**Do not use `conv=noerror,sync` on a first attempt.** Add it only after confirming reads succeed and you are dealing with genuine media damage.

### Trap 3 - a bad image still attaches

`hdiutil attach -nomount` on a zero-filled image succeeds and shows a device with no partition structure:

```
/dev/disk4 (disk image):
   0:                       +354.0 MB   disk4
```

Compare against the physical disc, which decomposes into slices. If the image shows no partition scheme, it is empty.

### What works

Buffered slice devices accept 2048-byte reads even when the raw whole-disc device does not:

```
diskutil unmountDisk /dev/diskN
sudo dd if=/dev/diskNsXsY of=~/Desktop/mp-hfs.img bs=2048 status=progress
```

Then verify before doing anything else:

```
ls -l ~/Desktop/mp-hfs.img          # expect ~308 MB
hexdump -C ~/Desktop/mp-hfs.img | head -5
```

A good HFS image shows zeros for the first 1024 bytes (empty boot blocks on a non-bootable volume) and then `BD` at offset 0x400 followed by the volume name.

For a **full-disc** image that can be verified against Redump, use the drive's native block size on the raw device with an explicit sector count from `drutil status`:

```
diskutil unmountDisk /dev/diskN
dd if=/dev/rdiskN of=full-2352.bin bs=2352 count=<blocks> status=progress
```

Confirmed working on the Pioneer (2026-08-29): the resulting track hashed byte-identical to the Redump database entry for Masterpieces, so this route produces Redump-comparable dumps directly. Reading to EOF probably also works, but an explicit `count` avoids any chance of an error at the lead-out; `drutil status` gives the exact block count.

Note that `sudo` turned out to be unnecessary: macOS gives the console user ownership of removable-media device nodes (`ls -l /dev/rdiskN` shows your user), so plain `dd` can read the disc. If you do use `sudo`, take ownership afterwards, since `hmount` needs write access:

```
sudo chown $(whoami) ~/Desktop/mp-hfs.img
```

Convert raw sectors to 2048-byte user data with `scripts/raw2user.py`, which also checks every sector's sync pattern, mode and address header, samples the EDC checksums, and prints CRC32/MD5/SHA-1 for both forms in the shape Redump publishes:

```
python3 scripts/raw2user.py full-2352.bin full-user.img
```

The user-data image is directly usable: `hmount full-user.img 1` mounts the first HFS partition through the Apple partition map, no carving needed.

## 5. Reading the HFS volume

```
brew install hfsutils
hmount ~/Desktop/mp-hfs.img
hls -l -R > ~/Desktop/mp-hfs.txt
humount
```

### The lock

hfsutils keeps mount state in `~/.hcwd` and it persists between invocations. A mount left open from an earlier command blocks the next one:

```
hmount: unable to obtain lock for medium (Resource temporarily unavailable)
```

Recovery, in order: `hvol` to see what it thinks is mounted, `humount` to release, `rm -f ~/.hcwd` if the state is stale, `lsof` on the image if something else holds it.

This is easy to loop on: you test `hmount` by hand to check it works, it succeeds and holds the lock, then a script's own `hmount` fails. `hfscopy.py` calls `humount` before mounting to break that cycle.

### Reading the listing format

```
f  APPL/INZ8     23047    262144 Jun 19  1996 A MIND FOREVER VOYAGING
d          4 items               Jun 15  1996 ARTHUR FOLDER
```

Columns are kind, type/creator, **resource fork size**, **data fork size**, date, name. Directory sections are introduced by a `:PATH:` header line. Filenames may contain spaces, so parse the name as everything following the date field.

## 6. Extraction: forks matter

The critical thing: **some Mac files have a data fork of zero and live entirely in the resource fork.** On Masterpieces that includes the Arthur, Journey and Zork Zero applications. `hcopy -r` (raw, data fork only) produces empty files for those.

Use `hcopy -m` (MacBinary II) uniformly and unpack the container yourself. `scripts/hfscopy.py` does this: data fork written normally, resource fork to `path/..namedfork/rsrc`, type/creator into the `com.apple.FinderInfo` xattr, modification date from the MacBinary header.

MacBinary II header fields used:

| Offset | Bytes | Field |
| --- | --- | --- |
| 65 | 4 | file type |
| 69 | 4 | creator |
| 73 | 1 | Finder flags, high byte |
| 83 | 4 | data fork length, big endian |
| 87 | 4 | resource fork length, big endian |
| 95 | 4 | modification date, Mac epoch |
| 101 | 1 | Finder flags, low byte |

Data fork begins at offset 128 and is padded to a 128-byte boundary; the resource fork follows.

Useful side effect: for Mac game applications that *do* have a data fork, that fork **is** the z-code story file. `hcopy -r` on those extracts a directly playable file.

Not preserved: creation dates. `os.utime` cannot set birth times. Add `SetFile -d` from the Xcode command line tools if you need them.

## 7. Producing a mountable modern image

`scripts/build-masterpieces.sh` runs the whole sequence: create a read/write HFS+ DMG, attach, copy via `hfscopy.py`, spot-check a known resource fork, detach, convert to compressed read-only UDZO, verify.

HFS+ is the right target. Current macOS mounts it read/write, it preserves forks and type/creator natively, and it is not going away as quickly as HFS did.

For the PC side alone, forks are irrelevant - every file under `PC/` is `TEXT/mdos` with all content in the data fork - so a plain ISO is lossless and simpler:

```
hdiutil makehybrid -iso -joliet -o masterpieces-pc.iso ~/Desktop/extracted-pc
```

Joliet gets long filenames. The result mounts by double-click and works in DOSBox via `imgmount D file.iso -t iso`.

For the Mac side, note that the applications are 68k and will not run on modern macOS regardless of filesystem. Their only use is under SheepShaver or Basilisk II, and **both mount raw HFS images directly** - so `mp-hfs.img` is simultaneously the archival copy and the working copy for emulation. No conversion needed for that use case.

## 8. Open items

- Regression fixtures for the parser as more discs are added.

Resolved 2026-08-29:

- Full-disc imaging with Redump-comparable hashes: works. `dd bs=2352` against `/dev/rdiskN` with an explicit count, then `scripts/raw2user.py`; see section 4. The Masterpieces dump matched Redump exactly.
- The Pioneer drive does not confuse imaging tools generally. The only real constraint is that the raw device requires reads in multiples of 2352; `bs=2048` failing was that constraint, not a drive quirk.

Per-disc open items (creation-date restoration passes and the like) live in each disc's `notes.md` under `discs/`.

## 9. Per-disc findings

Per-disc material lives under `discs/`, one folder per disc, holding the captured disc identification (`disc-info.txt`), the catalogue listing, findings (`notes.md`), and any disc-specific build scripts. This document stays method-level.

- [`discs/masterpieces-1996/`](../discs/masterpieces-1996/) - Classic Text Adventure Masterpieces of Infocom (1996). Imaged and catalogued; findings there correct several published-catalogue errors.

### Discs not yet imaged

The Lost Treasures CDs shipped as separate PC and Mac discs for volume 1 and a single combined disc for volume 2, so the partition layout may differ from the pattern above. Verify with `drutil toc` and `diskutil list` before assuming.

## 10. References

- Paul David Doherty, *Infocom Fact Sheet*: <http://pdd.if-legends.org/infocom/fact-sheet.txt>. Section VIII covers the compilations. The Masterpieces subsection is visibly unfinished - it omits Leather Goddesses entirely and has a placeholder in the prose - so prefer disc evidence where the two disagree.
- Andrew Plotkin, *The Obsessively Complete Infocom Catalog*: <https://eblong.com/infocom/>. Per-game file lists with release and serial numbers, and `zcanalyze.py` for reading z-code headers.
- IF Archive Infocom media: <https://ifarchive.org/indexes/if-archive/infocom/media/>. Portable conversions of the Lurking Horror and Sherlock sound files.
- Redump has a Masterpieces entry; the Internet Archive copy is tagged as a Redump dump.
