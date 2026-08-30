# Return to Zork CD-ROM v1.1 (Activision, 1994)

Disc-specific material for archiving the standalone Return to Zork CD-ROM, version 1.1 (`DISK.ID` dated 1993-12-12, disc mastered 1994-02-07).
No disc content lives in this folder - only identification records, listings, notes.

A **mixed-mode** disc, like the [1997 Zork Legacy Collection pressing](../zork-legacy-1997-rtz-anthology/README.md) it was later folded into: one Mode 1 data track (volume `RTZ-CD`) followed by 25 Red Book audio tracks, 26 tracks and 191601 sectors in all.

## Contents

| File | What it is |
| --- | --- |
| `disc-info.txt` | Captured `drutil` and `diskutil` output: TOC with all 26 tracks, block count, slice layout, and the audio tracks as `cddafs` presents them |
| `return-to-zork-1994.ls.txt` | Recursive listing of the mounted data volume |
| `notes.md` | Per-disc findings, including a comparison with the 1997 pressing |
| `checksums.txt` | Reference hashes for a full dump and for each track, checked against Redump |

## Archiving your own copy

1. Insert the disc; macOS mounts `RTZ-CD` and an "Audio CD". Confirm it matches [disc-info.txt](disc-info.txt): one session, 26 tracks, 191601 blocks.
2. Unmount everything **before** reading the TOC - `drutil toc` needs exclusive access, and the mounted audio side blocks it - then dump the whole disc linearly as raw sectors:

   ```
   diskutil unmountDisk /dev/diskN
   drutil toc
   dd if=/dev/rdiskN of=~/Desktop/rtz-full-2352.bin bs=2352 count=191601 status=progress
   ```

3. Split the dump at Redump's track boundaries. This pressing has a pregap only before the first audio track (`--pregaps first`), and the offset to apply is your drive's read offset plus this disc's -22 write offset (645 for the Pioneer BDR-XS07U's +667):

   ```
   python3 ../../scripts/splittracks.py --toc disc-info.txt ~/Desktop/rtz-full-2352.bin --out ~/Desktop/rtz-tracks --pregaps first --offset 645
   ```

4. Convert the data track and compare everything against [checksums.txt](checksums.txt):

   ```
   python3 ../../scripts/raw2user.py ~/Desktop/rtz-tracks/track01.bin ~/Desktop/rtz-data.iso
   ```

Keep the linear raw `.bin` as the archival artifact and never modify it.
