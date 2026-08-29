# Classic Text Adventure Masterpieces of Infocom (Activision, 1996)

Disc-specific material for archiving this hybrid Mac/PC CD-ROM.
No disc content lives in this folder - only identification records, listings, notes, and the utilities particular to this disc.

## Contents

| File | What it is |
| --- | --- |
| `disc-info.txt` | Captured `drutil` and `diskutil` output from the physical disc: TOC, session/track/block counts, slice layout |
| `masterpieces-1996.hls.txt` | Full `hls -l -R` catalogue listing of the HFS volume (879 entries), also the parser fixture for `scripts/hfscopy.py --dry-run` |
| `notes.md` | Per-disc findings, including corrections and extensions to the published catalogues |
| `checksums.txt` | Reference hashes for a full dump of this disc, Redump-verified; check your own dump against these |
| `build-masterpieces.sh` | Turns a dumped HFS slice image into a modern, mountable HFS+ `.dmg` with resource forks and metadata intact |

## Archiving your own copy

The full method with its pitfalls is in [docs/knowledge-transfer.md](../../docs/knowledge-transfer.md). The short version for this disc:

1. Insert the disc and confirm it matches [disc-info.txt](disc-info.txt): one session, one data track, 150515 blocks, an Apple partition scheme with ISO9660 and Apple_HFS slices.
2. Unmount and dump the whole disc as raw sectors (no `sudo` needed; macOS gives the console user the optical device nodes):

   ```
   diskutil unmountDisk /dev/diskN
   dd if=/dev/rdiskN of=~/Desktop/mp-full-2352.bin bs=2352 count=150515 status=progress
   ```

   Expect ~1 MB/s and about six minutes. A transfer rate in the tens of MB/s means you are not reading the disc; stop and reread the traps in the method doc.

3. Convert to user data, which also verifies sector structure and prints hashes:

   ```
   python3 ../../scripts/raw2user.py ~/Desktop/mp-full-2352.bin ~/Desktop/mp-full-user.img
   ```

4. Compare the printed hashes against [checksums.txt](checksums.txt). A match means your copy is byte-identical to the Redump reference pressing.
5. The user-data image mounts directly with hfsutils (`hmount ~/Desktop/mp-full-user.img 1`). To build a double-clickable modern HFS+ image:

   ```
   ./build-masterpieces.sh ~/Desktop/mp-full-user.img
   ```

Keep the raw `.bin` as the archival artifact and never modify it; everything else is a convenience copy.
