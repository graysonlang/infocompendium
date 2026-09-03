# The Lost Treasures of Infocom CD (Activision, 1992)

Disc-specific material for archiving the Lost Treasures volume 1 CD-ROM (`DISK.ID`: "LTOICD / 1.0 / Disk 1", mastered 1992-05-26).
No disc content lives in this folder - only identification records, listings, notes.

A single 8 MB ISO 9660 data track, volume `INFOCOM`, with Apple ISO extensions carrying **both** the `MAC` and `PC` trees - not a hybrid, not separate per-platform discs.
Redump has no Lost Treasures entry, so [checksums.txt](checksums.txt) stands as the reference for this pressing.

## Contents

| File | What it is |
| --- | --- |
| `disc-info.txt` | Captured `drutil` and `diskutil` output |
| `lost-treasures-1-1992.ls.txt` | Recursive listing of the ISO volume |
| `notes.md` | Per-disc findings |
| `versions.md` | Release/serial table for every title, both platforms |
| `checksums.txt` | Reference hashes for a full dump |

## Archiving your own copy

1. Insert the disc; it may take macOS a while to enumerate (retry `diskutil list`). Confirm one session, one data track, 3895 blocks.
2. Unmount and dump (seconds, at this size):

   ```
   diskutil unmountDisk /dev/diskN
   dd if=/dev/rdiskN of=~/Desktop/ltoi1-full-2352.bin bs=2352 count=3895 status=progress
   python3 ../../scripts/raw2user.py ~/Desktop/ltoi1-full-2352.bin ~/Desktop/ltoi1-data.iso
   ```

3. Compare the printed hashes against [checksums.txt](checksums.txt).
4. Do not copy files off the mounted volume - macOS cannot open the Mac side's fork-bearing files. Extract from the image instead, which restores resource forks, Finder metadata and dates:

   ```
   python3 ../../scripts/appleiso.py ~/Desktop/ltoi1-data.iso ~/Desktop/ltoi1-extracted
   ```

Keep the raw `.bin` as the archival artifact and never modify it.
