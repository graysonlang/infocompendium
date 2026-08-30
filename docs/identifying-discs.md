# Identifying discs

What a hybrid disc is, why modern macOS refuses to mount one, and how to identify what is in the drive.
Established against physical media on an Apple Silicon Mac with an external Pioneer BD-RW BDR-XS07U; the reference example throughout is *Classic Text Adventure Masterpieces of Infocom* (1996).

Once a disc is identified, continue with [imaging.md](imaging.md).

## What hybrid discs are

A hybrid CD carries a single Mode 1 data track holding **two filesystem catalogs over one set of data blocks**. The PC reads an ISO 9660 catalog; the Mac reads an HFS catalog. Most content exists once and is indexed twice.

This is not the same as a *mixed mode* disc, which is a data track followed by Red Book audio tracks. Check with `drutil toc` before assuming: one track means hybrid.

Consequences worth internalizing:

- The ISO slice can be tiny while the HFS volume holds everything. On Masterpieces the ISO slice is 260 KB and the HFS volume is 308 MB. The ISO slice is a pointer structure, not a copy of the content.
- The two catalogs do not necessarily index identical sets. Masterpieces has genuinely separate `MAC` and `PC` directory trees with different game files in each.
- The same bytes can present differently per side. A file may appear as a plain DOS file to the ISO catalog and as a typed Mac document (creator `mdos`) to the HFS catalog.

Not every disc in this project is a hybrid: The Zork Anthology (1994) is plain ISO 9660, mounts fine on modern macOS, and the identification commands below apply unchanged.
The Zork Legacy Collection's Return to Zork / Zork Anthology disc (1997) is a genuine *mixed mode* disc - one data track followed by 25 audio tracks - and `diskutil list` shows every audio track as its own `CD_DA` slice while macOS mounts the audio side as a `cddafs` "Audio CD" volume alongside the data volume.
Expect macOS to re-enumerate such a disc a few seconds after insertion (the device node briefly disappears) as it sets up both mounts.
The Lost Treasures CDs shipped as separate PC and Mac discs for volume 1 and a single combined disc for volume 2, so the partition layout may differ per disc.
Verify with `drutil toc` and `diskutil list` before assuming.

## Why macOS fights you

macOS removed HFS (not HFS+) support in Ventura. `diskutil` still *identifies* an HFS volume - it reads the master directory block directly - but the mount subsystem refuses it. On an Apple-partitioned hybrid it appears to refuse the whole disc, including the ISO slice that it could in principle still handle.

Observed on the test machine:

```
diskutil mount readOnly disk8s1
Volume on disk8s1 failed to mount
diskutil mount readOnly disk8s1s2
Volume on disk8s1s2 failed to mount
```

No flag changes this. Do not spend time on it. Read the raw device instead, and use `hfsutils`, which implements HFS itself and does not care what the OS supports (see [hfs-extraction.md](hfs-extraction.md)).

## Identifying a disc

```
diskutil list                        # find the device node
diskutil info /dev/diskN
diskutil list diskN                  # slice breakdown
drutil status                        # session and track count, block count
drutil toc
```

`diskutil` can transiently report "Could not find disk" for a disc that is present; retry before concluding anything.
`drutil toc` needs exclusive access to the drive and fails with "Could not unmount disc" once macOS has mounted a mixed-mode disc's audio side as a `cddafs` volume; run `diskutil unmountDisk` first, or read the TOC in the seconds before the audio mount appears.

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

## Confirming filesystems directly

If you want signatures rather than `diskutil`'s word for it:

```
# ISO 9660 primary volume descriptor, sector 16, expect "CD001"
dd if=/dev/rdiskNsXsY bs=2048 count=1 skip=16 | xxd | head -3

# HFS master directory block at byte 0x400, expect "BD" (HFS) or "H+" (HFS+)
dd if=/dev/rdiskNsXsY bs=2048 count=1 | xxd | sed -n '65,68p'
```

(`sudo` is unnecessary: macOS gives the console user ownership of removable-media device nodes.)

The MDB read also gives you the volume name as a Pascal string and the creation/modification dates as Mac timestamps (seconds since 1904-01-01; subtract 2082844800 for Unix time).

Note that `skip=16` against a *slice* device is sector 16 of the slice, not of the filesystem, so on a partitioned disc you may land on the volume descriptor set terminator (leading byte `ff`) rather than the primary descriptor (leading byte `01`). Both prove ISO 9660 is present. Walk back a sector or two if you want the PVD specifically.

Anything dated before early 1998 will be plain HFS, not HFS+. HFS+ shipped with Mac OS 8.1.
