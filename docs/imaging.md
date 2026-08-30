# Imaging: the traps, and what works

How to get a faithful image off a disc, and the several ways the obvious commands silently produce a file full of zeros.
Identify the disc first ([identifying-discs.md](identifying-discs.md)); for reading and extracting HFS content from the image, continue with [hfs-extraction.md](hfs-extraction.md).

## Trap 1 - raw device block size

`/dev/rdiskN` rejects reads that are not a multiple of the drive's physical block size. On the Pioneer, that is 2352, so `bs=2048` fails on **every** read:

```
sudo dd if=/dev/rdisk8 of=out.img bs=2048 conv=noerror,sync
dd: /dev/rdisk8: Invalid argument
```

This is a constraint of raw optical devices, not a drive quirk; the drive does not otherwise confuse imaging tools.

## Trap 2 - `conv=noerror,sync` turns that into silent data loss

Paired with trap 1, `conv=noerror,sync` responds to each rejected read by writing 2048 zero bytes and moving on. The result is a full-size image containing nothing, produced at RAM speed. The tell is the transfer rate: real optical reads run at a few MB/s, so figures like 140 MB/s mean fabrication.

**Do not use `conv=noerror,sync` on a first attempt.** Add it only after confirming reads succeed and you are dealing with genuine media damage.

## Trap 3 - a bad image still attaches

`hdiutil attach -nomount` on a zero-filled image succeeds and shows a device with no partition structure:

```
/dev/disk4 (disk image):
   0:                       +354.0 MB   disk4
```

Compare against the physical disc, which decomposes into slices. If the image shows no partition scheme, it is empty.

## What works: the full-disc raw dump

For a **full-disc** image that can be verified against Redump, use the drive's native block size on the raw device with an explicit sector count from `drutil status`:

```
diskutil unmountDisk /dev/diskN
dd if=/dev/rdiskN of=full-2352.bin bs=2352 count=<blocks> status=progress
```

Confirmed working on the Pioneer (2026-08-29): the resulting tracks for Masterpieces and The Zork Anthology hashed byte-identical to their Redump database entries, so this route produces Redump-comparable dumps directly. Reading to EOF probably also works, but an explicit `count` avoids any chance of an error at the lead-out; `drutil status` gives the exact block count.

`sudo` is unnecessary: macOS gives the console user ownership of removable-media device nodes (`ls -l /dev/rdiskN` shows your user), so plain `dd` can read the disc. If you do use `sudo`, take ownership afterwards, since `hmount` needs write access:

```
sudo chown $(whoami) full-2352.bin
```

Convert raw sectors to 2048-byte user data with `scripts/raw2user.py`, which also checks every sector's sync pattern, mode and address header, samples the EDC checksums, and prints CRC32/MD5/SHA-1 for both forms in the shape Redump publishes:

```
python3 scripts/raw2user.py full-2352.bin full-user.img
```

The user-data image is directly usable: for a hybrid, `hmount full-user.img 1` mounts the first HFS partition through the Apple partition map, no carving needed; for a plain ISO disc it attaches with `hdiutil attach -readonly` or feeds DOSBox via `imgmount d full-user.img -t iso`.

Keep the raw `.bin` as the archival artifact and never modify it; everything else is a derivative.

## What also works: dumping a single slice

Buffered slice devices accept 2048-byte reads even when the raw whole-disc device does not, so a single slice (say, the HFS volume of a hybrid) can be dumped directly:

```
diskutil unmountDisk /dev/diskN
dd if=/dev/diskNsXsY of=mp-hfs.img bs=2048 status=progress
```

Then verify before doing anything else:

```
ls -l mp-hfs.img                    # expect the slice size from diskutil list
hexdump -C mp-hfs.img | head -5
```

A good HFS image shows zeros for the first 1024 bytes (empty boot blocks on a non-bootable volume) and then `BD` at offset 0x400 followed by the volume name.
The full-disc dump above supersedes this route - it captures everything and verifies against Redump - but the slice dump remains useful for a quick look at one volume.

## Mixed-mode discs: audio tracks come along for free

A mixed-mode disc (one data track followed by Red Book audio tracks) needs no special handling on the dump side.
The raw whole-disc device delivers every sector linearly - data sectors with their sync/header structure, audio sectors as 2352 bytes of 16-bit stereo PCM - so the same `dd bs=2352 count=<blocks>` captures the entire disc, `drutil status` block count included.
Established on the Zork Legacy Collection's Return to Zork / Zork Anthology disc (2026-08-29).

Two things that look like problems but are not:

- The 150-sector pregap between the data track and the first audio track, and the first sectors of a quiet track, read back as all zeros. That is genuine silence, not the driver blanking non-data sectors; sectors further into any audio track are full of signal.
- macOS mounts the audio side as a `cddafs` "Audio CD" of AIFF files. Those are convenient for listening but are not sector-precise (track 2 came back as 3,859,560 PCM bytes, not a whole number of sectors), so do not use them as the archival copy.

Split the linear dump at Redump's track boundaries with `scripts/splittracks.py --toc disc-info.txt`, which reads the `drutil toc` capture, cuts each audio track 150 sectors before its TOC start (Redump attaches the pregap to the front of the following track), and hashes every track in Redump's shape.
Feed only the data track (`track01.bin`) to `raw2user.py`; audio sectors have no sync pattern and would fail its structure checks.

### Audio and the drive's read offset

Every CD drive returns audio shifted by a fixed number of samples from where it was asked to read - the read offset - and Redump's audio track hashes are offset-corrected, so a raw dump's audio tracks will not match Redump until the shift is undone.
The data track is unaffected (data sectors carry their own addresses), which is why it matches straight away while every audio track differs by the same amount.

Measured on the Pioneer BD-RW BDR-XS07U on 2026-08-29: **+667 samples** (2,668 bytes). Found by taking one short audio track and searching for the sample shift at which its CRC32 matches Redump's; a second track confirmed it, and with `--offset 667` all 25 audio tracks of the Zork Legacy Collection disc matched Redump exactly.
The search is cheap (a few thousand CRCs of a few megabytes), so a drive with an unknown offset can be characterized from any disc Redump already has.

Record the *uncorrected* linear dump as the archival file: it is what the drive actually read, and the correction is a pure function of the offset applied at split time.
