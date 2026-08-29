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

For a **full-disc** image that can be verified against Redump, try native block size on the raw device:

```
sudo dd if=/dev/rdiskN of=full.img bs=2352 status=progress
```

That yields raw 2352-byte sectors rather than 2048-byte user data, so it needs converting before hashing. This is still an open item; see section 8.

Take ownership afterwards, since `sudo dd` leaves the file owned by root and `hmount` needs write access:

```
sudo chown $(whoami) ~/Desktop/mp-hfs.img
```

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

- Full-disc image with Redump-comparable hashes. The `bs=2352` route against `/dev/rdiskN` is untested. Redump already has a Masterpieces entry, so a hash match would confirm the pressing is unmodified - which matters for the `LHSOUND.ZIP` provenance question below.
- Whether the Pioneer BD combo drive reports sector layout in a way that confuses imaging tools generally, or only `dd`. DiscImageCreator on a PC is the fallback.
- `SetFile -d` pass to restore creation dates.
- Regression fixtures for the parser as more discs are added.

## 9. Per-disc findings

### Classic Text Adventure Masterpieces of Infocom (1996)

Volume `Masterpieces`, created 18 June 1996, modified 22 June 1996. 879 catalogue entries: 113 directories, 766 files.

Structure: the HFS volume is the whole disc. `MAC` and `PC` are sibling folders alongside shared `DOCS`, `PCDEMOS`, `ACRODOS`, and DOS/Windows installers at root. There is no separate PC filesystem tree to merge - extracting the HFS volume once yields everything.

Findings that correct or extend the published catalogues:

- **`LEATHER.SCR` is present** (1,408 bytes) in `PC/LEATHER/`, and `_LEATHER.COM` is 12,004 bytes, which is Infocom MS-DOS interpreter **3N** - the only build that loads a boss key screen. So the Leather Goddesses boss key works on this disc. Doherty's Infocom Fact Sheet notes the LTOI1 IBM packages dropped it, and is internally inconsistent about the filename (`LEATHER.DAT` in one section, `<GAMENAME>.SCR` in the interpreter table). The disc settles it: `.SCR`.
- **`PC/LURKING/DATA/LHSOUND.ZIP`** (589,733 bytes) is Stefan Jokisch's freeware sound package, shipped on a commercial Activision disc. Contents: fourteen `LURKINxx.SND` files matching Doherty's count of fourteen sounds, `UPDATELH.EXE` plus C source, and `LURKING.CNV` at 129,944 bytes - exactly the length Doherty gives for release 221.870918. The README is signed by Jokisch and mentions Frotz as unfinished, dating it before December 1995; internal file dates run January to August 1995. So a PC owner of this disc can convert the shipped r203 to r221 and play with sound on a Sound Blaster, contrary to the usual claim that Lurking Horror sound was Amiga-only.
- **Seventeen games ship with populated `SAVE` directories**: Ballyhoo, Deadline, Enchanter, Infidel, Lurking, Moonmist, Planetfall, Sorcerer, Spellbreaker, Starcross, Stationfall, Suspect, Suspended, Witness, Zork I, Zork II, Zork III. Sizes 10.8-15.3 KB. `PC/LURKING/SAVE/LURKING.DAT` contains the serial `870506` (confirming it was made against the shipped r203), the strings `872325412` and `uhlersoth` - the login and password for the opening terminal puzzle, which were feelie-based copy protection - and an input buffer holding `save`. These are real saves. Their timestamps are all 22 June 1996, the same stamp as nearly every file on the disc, so the dates reflect mastering rather than when the games were played.
- **Zork Zero's PC graphics are incomplete.** `PC/ZORK0/` has `.CG1`, `.EG1`, `.ZIP` and the interpreter but no `.MG1` and no `.EG2`. Arthur and Journey have all four. This is the same omission Doherty documented for LTOI1's IBM packages, carried forward.
- **Mac Sherlock ships its sound.** `MAC/SOUND/` holds thirteen `SDAT` files (S3-S17) plus four 32-byte `M` files dated February 1988. The Mac Sherlock is r26.880127, the sound build.
- **Two provenances of PC story file.** Games with a `DATA/` subfolder have files padded to round sizes (92160, 122880, 153600); the same files are duplicated in a shared `PC/DATA/`. Games without one have the `.DAT` in the game folder at natural size **+1 byte**, matching Doherty's note about IBM data files padded with a trailing `$1a`. Examples: `LEATHER.DAT` 129,023 vs 129,022; `WISHBRIN.DAT` 128,905 vs 128,904; `TRINITY.DAT` 262,065 vs 262,064.
- **Every interpreter matches Doherty's size table**: 11394=3L, 11402=3M2, 12004=3N, 12640=4A, 12682=4E, 12688=4D, 33946=5J, 47442=6.68, 47494/47528=6.71.
- Mac Zork I, II, III and Beyond Zork are dated 3 April 1995, a year older than the 19 June 1996 stamp on every other Mac game.
- `PCDEMOS/PLANETFALL/planetfall.avi` (4.2 MB) is likely promotional footage for the cancelled *Planetfall: The Search for Floyd*.
- `VERYLOST/` on both sides holds aborted game proposals (Amnesia, Boston, Creation, LG2 ideas, Oz, Thriller, Trek, Truffles) and three issues of the internal *Infodope* newsletter. The Mac copy of `MISC/` has one file the PC copy lacks.

Mac and PC builds diverge for Sherlock, Seastalker, Wishbringer, Leather Goddesses, Planetfall, Arthur, Journey and Zork Zero. Do not merge the two trees by filename; keep them as siblings.

### Others

Not yet imaged. The Lost Treasures CDs shipped as separate PC and Mac discs for volume 1 and a single combined disc for volume 2, so the partition layout may differ from the pattern above. Verify with `drutil toc` and `diskutil list` before assuming.

## 10. References

- Paul David Doherty, *Infocom Fact Sheet*: <http://pdd.if-legends.org/infocom/fact-sheet.txt>. Section VIII covers the compilations. The Masterpieces subsection is visibly unfinished - it omits Leather Goddesses entirely and has a placeholder in the prose - so prefer disc evidence where the two disagree.
- Andrew Plotkin, *The Obsessively Complete Infocom Catalog*: <https://eblong.com/infocom/>. Per-game file lists with release and serial numbers, and `zcanalyze.py` for reading z-code headers.
- IF Archive Infocom media: <https://ifarchive.org/indexes/if-archive/infocom/media/>. Portable conversions of the Lurking Horror and Sherlock sound files.
- Redump has a Masterpieces entry; the Internet Archive copy is tagged as a Redump dump.
