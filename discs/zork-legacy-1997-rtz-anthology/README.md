# Return to Zork / The Zork Anthology (The Zork Legacy Collection, 1997)

Disc-specific material for archiving the combined Return to Zork / Zork Anthology CD from Activision's *Zork Legacy Collection*.
No disc content lives in this folder - only identification records, listings, notes.

This is a **mixed-mode** disc: one Mode 1 data track (volume `RTZ_ZA`) followed by 25 Red Book audio tracks.
macOS mounts both sides - the data volume, and the audio tracks as a `cddafs` "Audio CD" - but a faithful archive needs the raw sector dump described below, not the mounted views.

## Contents

| File | What it is |
| --- | --- |
| `disc-info.txt` | Captured `drutil` and `diskutil` output: TOC with all 26 tracks, block count, slice layout, and the audio tracks as `cddafs` presents them |
| `zork-legacy-1997-rtz-anthology.ls.txt` | Recursive listing of the mounted data volume |
| `notes.md` | Per-disc findings |
| `checksums.txt` | Reference hashes for a full dump and for each track, checked against Redump |

## Archiving your own copy

1. Insert the disc; macOS mounts `RTZ_ZA` and an "Audio CD" (the device may briefly disappear while it re-enumerates). Confirm it matches [disc-info.txt](disc-info.txt): one session, 26 tracks, 211940 blocks, lead-out at 47:07.65.
2. Unmount everything and dump the whole disc linearly as raw sectors. The raw device delivers the audio tracks as well as the data track (no `sudo` needed):

   ```
   diskutil unmountDisk /dev/diskN
   dd if=/dev/rdiskN of=~/Desktop/zl-full-2352.bin bs=2352 count=211940 status=progress
   ```

3. Split the dump into per-track files at Redump's boundaries and hash each track, correcting for your drive's read offset (the Pioneer BDR-XS07U's is +667 samples; look yours up on the AccurateRip drive offset list, or find it by searching for the shift that makes one audio track's hash match Redump):

   ```
   python3 ../../scripts/splittracks.py --toc disc-info.txt ~/Desktop/zl-full-2352.bin --out ~/Desktop/zl-tracks --offset 667
   ```

4. Convert the data track to user data (this also verifies its sector structure):

   ```
   python3 ../../scripts/raw2user.py ~/Desktop/zl-tracks/track01.bin ~/Desktop/zl-data.iso
   ```

5. Compare the printed hashes against [checksums.txt](checksums.txt).
6. `zl-data.iso` mounts with `hdiutil attach -readonly` or in DOSBox; the audio tracks are raw 16-bit stereo 44.1 kHz PCM, playable after wrapping in a WAV header or via `ffmpeg -f s16le -ar 44100 -ac 2 -i trackNN.bin`.

Keep the linear raw `.bin` as the archival artifact and never modify it.
