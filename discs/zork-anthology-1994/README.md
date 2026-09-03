# The Zork Anthology (Activision, 1994)

Disc-specific material for archiving this CD-ROM.
No disc content lives in this folder - only identification records, listings, notes, and disc-specific utilities.

Unlike the hybrid compilations, this is a plain ISO 9660 disc (one Mode 1 track, no HFS side), so modern macOS mounts it by double-click.
The catch is different: it is an **installer-based** disc.
The six classic games are not present as loose files; they live inside `ZORKANTH.RED`, an Activision installer archive unpacked by the DOS `INSTALL.EXE`.
See [notes.md](notes.md) for the container format and [versions.md](versions.md) for the exact builds inside it.

## Contents

| File | What it is |
| --- | --- |
| `disc-info.txt` | Captured `drutil` and `diskutil` output: TOC, block count, slice layout |
| `zork-anthology-1994.ls.txt` | Recursive listing of the mounted ISO volume |
| `notes.md` | Per-disc findings |
| `versions.md` | Release/serial table for the games inside `ZORKANTH.RED` |
| `checksums.txt` | Reference hashes for a full dump, checked against Redump |

## Archiving your own copy

1. Insert the disc; it mounts as `ZORK_ANTHOLOGY`. Confirm it matches [disc-info.txt](disc-info.txt): one session, one Mode 1 data track, 120295 blocks.
2. Unmount and dump the whole disc as raw sectors (no `sudo` needed):

   ```
   diskutil unmountDisk /dev/diskN
   dd if=/dev/rdiskN of=~/Desktop/za-full-2352.bin bs=2352 count=120295 status=progress
   ```

3. Convert to user data, which also verifies sector structure and prints hashes:

   ```
   python3 ../../scripts/raw2user.py ~/Desktop/za-full-2352.bin ~/Desktop/za-full-user.img
   ```

4. Compare the printed hashes against [checksums.txt](checksums.txt).
5. The user-data image is a mountable ISO; `hdiutil attach -readonly za-full-user.img` or use it directly in DOSBox with `imgmount d za-full-user.img -t iso`.

Keep the raw `.bin` as the archival artifact and never modify it.
