# The Lost Treasures of Infocom II CD (Activision, 1992)

Disc-specific material for archiving the Lost Treasures volume 2 CD-ROM.
No disc content lives in this folder - only identification records, listings, notes.

A single 12.4 MB ISO 9660 data track, volume `LOST TREASURES II`, with Apple ISO extensions carrying both the `MAC` and `DOS` trees on one filesystem - the same shape as [volume 1](../lost-treasures-1-1992/README.md).
Unlike volume 1, Redump has an entry for this disc (105382), and this dump verifies against it.

## Contents

| File | What it is |
| --- | --- |
| `disc-info.txt` | Captured `drutil` and `diskutil` output |
| `lost-treasures-2-1992.ls.txt` | Recursive listing of the ISO volume |
| `notes.md` | Per-disc findings |
| `versions.md` | Release/serial table for every title, both platforms |
| `checksums.txt` | Reference hashes for a full dump, Redump-verified |

## Archiving your own copy

1. Insert the disc; confirm one session, one Mode 1 data track, 6075 blocks.
2. Unmount and dump (seconds, at this size):

   ```
   diskutil unmountDisk /dev/diskN
   dd if=/dev/rdiskN of="$HOME/Desktop/ltoi2-full-2352.bin" bs=2352 count=6075 status=progress
   python3 ../../scripts/raw2user.py "$HOME/Desktop/ltoi2-full-2352.bin" "$HOME/Desktop/ltoi2-data.iso"
   ```

3. Compare the printed hashes against [checksums.txt](checksums.txt); a match is a Redump-verified copy.
4. Do not copy the Mac files from the mounted volume - macOS's cd9660 driver cannot open the fork-bearing files (see [volume 1's notes](../lost-treasures-1-1992/notes.md)). Extract from the image instead:

   ```
   python3 ../../scripts/appleiso.py "$HOME/Desktop/ltoi2-data.iso" "$HOME/Desktop/ltoi2-extracted"
   ```

Keep the raw `.bin` as the archival artifact and never modify it.
