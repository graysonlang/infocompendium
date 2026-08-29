# Classic Text Adventure Masterpieces of Infocom (Activision, 1996)

Disc-specific material for archiving this hybrid Mac/PC CD-ROM.
No disc content lives in this folder - only identification records, listings, notes, and the utilities particular to this disc.

## Contents

| File | What it is |
| --- | --- |
| `disc-info.txt` | Captured `drutil` and `diskutil` output from the physical disc: TOC, session/track/block counts, slice layout |
| `masterpieces-1996.hls.txt` | Full `hls -l -R` catalogue listing of the HFS volume (879 entries), also the parser fixture for `scripts/hfscopy.py --dry-run` |
| `notes.md` | Per-disc findings, including corrections and extensions to the published catalogues |
| `build-masterpieces.sh` | Turns a dumped HFS slice image into a modern, mountable HFS+ `.dmg` with resource forks and metadata intact |

## Archiving your own copy

The full method with its pitfalls is in [docs/knowledge-transfer.md](../../docs/knowledge-transfer.md). The short version for this disc:

1. Insert the disc and confirm it matches [disc-info.txt](disc-info.txt): one session, one data track, 150515 blocks, an Apple partition scheme with ISO9660 and Apple_HFS slices.
2. Unmount and dump the HFS slice from the *buffered* device (the raw device rejects 2048-byte reads on some drives):

   ```
   diskutil unmountDisk /dev/diskN
   sudo dd if=/dev/diskNs1s3 of=~/Desktop/mp-hfs.img bs=2048 status=progress
   sudo chown $(whoami) ~/Desktop/mp-hfs.img
   ```

3. Verify before anything else: the image should be 308,254,720 bytes at most (slice-sized), with zeros for the first 1024 bytes and `BD` at offset 0x400 followed by the volume name `Masterpieces`.
4. Build the mountable derivative:

   ```
   ./build-masterpieces.sh ~/Desktop/mp-hfs.img
   ```

Keep the slice image as the archival artifact and never modify it; the `.dmg` is a convenience copy.
