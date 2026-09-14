# Floppy imaging: flux capture and the 8-bit formats

Optical discs are covered in [imaging.md](imaging.md).
This page is about 5.25" and 3.5" diskettes, where the disc is read at flux level and the format is decoded afterwards.
Every finding here was established against media that decoded completely, so each one has a positive control behind it.

Hardware used throughout: a Greaseweazle V4.1 (firmware 1.6) with a TEAC FD-55GFR.

## The drive is 96 tpi and the media is 48 tpi

The FD-55GFR is an 80-track high-density drive.
Apple II, Atari 8-bit, Commodore 1541 and PC 360K media are all 48 tpi, so every read needs `step=2` to land on track centers.
Omit it and the head sits between tracks.

## Capture flux, not sectors

```
gw read --tracks=c=0-34:step=2 --revs=2 --raw --format=<fmt> disk.scp
gw convert --format=<fmt> disk.scp disk.img
```

Both flags on the read matter.
`--format` makes the read verify each track as it goes, with retries on marginal ones.
`--raw` keeps the stored flux genuine - without it, `gw read` writes flux re-synthesized from the decoded sectors, which looks clean but has lost the weak bits and timing detail that flux capture exists to preserve.

## Formats and what a good read looks like

| Media | Format | Tracks | Complete read |
| --- | --- | --- | --- |
| Apple II | `apple2.appledos.140` | `c=0-34` | 560 sectors (35 x 16 x 256) |
| Atari 810/1050 | `atari.90` | `c=0-39` | 720 sectors (40 x 18 x 128) |
| Commodore 1541 | `commodore.1541` | `c=0-34` | **683** sectors (zoned) |
| PC 360K | `ibm.360` | `c=0-39` | 720 sectors, two heads |

The Commodore format is zoned and the others are not: 21 sectors on tracks 0-16, 19 on 17-23, 18 on 24-29, 17 from 30 up, with the clock stepping 3.25 -> 4.00us per zone.
A complete 35-track read is 683 sectors, not a round number, so do not read a non-round count as failure.
A 40-track C64 release is 768; `c=0-34` would silently miss the last five tracks.

Atari labels reading "810 or 1050 disk" mean single density - `atari.90`.
`atari.130` is 1050-only enhanced density and returns 0 sectors on single-density media.

`ibm.scan` auto-detects without being told the format, which makes it a useful independent check on a decode you are unsure of.

## Sector ordering is not cosmetic

Apple II images come in three sector orders that differ only in layout: `appledos`, `prodos`, `nofs`.
Choosing wrong still reports a full 560/560 while producing scrambled bytes.
`apple2.appledos.140` is correct for Infocom Apple II disks, confirmed with ZCut - appledos extracts Zork I with "Checksum good" where prodos gives "Checksum bad".

Sector position inside an appledos image is `(track * 16 + INV[sector]) * 256`, where `INV` is the inverse of the DOS 3.3 interleave `0DB97531ECA8642F`.

## Unrecovered sectors are marked, not zeroed

Greaseweazle fills a sector it could not recover with the ASCII string `-=[BAD SECTOR]=-` repeated to 256 bytes.
That is the reliable way to locate damage in a decoded image.
Do not assume zero-fill: a clean image legitimately contains empty sectors, and on one disc here 119 of them were genuinely blank.
Nor should damage be inferred from bytes that differ between two reads - those are simply sectors one read recovered and the other did not.

## Merging several reads of a damaged disc

`gw convert` can recover fewer sectors than `gw read` did from the same flux.
Read-time retries decode each attempt and accumulate recovered sectors; convert re-decodes the stored flux in a single pass.
Measured here on one title: read reported 559/560 while converting that same `.scp` gave 556/560.
It is not a sector-order or PLL artifact - both orderings give identical counts, and five PLL variations changed nothing.
Only marginal media is affected; clean captures convert identically.

So on a disc with weak sectors, also run a non-`--raw` read to keep the image the drive actually recovered, or take several captures and merge per-sector.
One title here reached a complete image only by merging four reads, none of which was complete alone.

When merging, decode every source with the same geometry.
Passing `--tracks=c=0-69:step=2` to a convert of a `step=2` capture silently mis-decodes it; that is only correct for `step=1` sweeps.

## Reading the second side of a flippy

Apple II, Atari and Commodore drives are all soft-sectored: they find sectors by reading address marks and never need the index pulse.
The Greaseweazle does need it, to delimit revolutions.
That difference is the whole problem.

A disc with **two index holes** can simply be flipped and read normally.
A disc with **one** cannot: flipped, the hole no longer lines up, the drive's sensor never fires, and gw reports `GetFluxStatus: No Index`.
The index hole does not control spinning - the motor runs whenever the drive is selected - it only provides the timing reference.

`--fake-index` tells the firmware to synthesize its own pulses and is the documented workaround, but per the Greaseweazle wiki it "requires a drive which will spin up in the absence of index pulses (many will not)".
The TEAC FD-55GFR is one that will not: it returns `0 flux in 0.00ms` regardless of the value passed, and neither the drive's index-sensor jumpers nor its RY/DC jumper changes that.
For such a disc on such a drive there is no software route to the second surface - only a different drive, a flippy-modded drive with a second index sensor, or punching the jacket.

### Reading side 2 through head 1

A double-sided drive's second head sits against the opposite surface, so it can read a flippy's second side in place, with no flipping and no index problem:

```
gw read --tracks=c=0-39:h=1:step=2 --revs=2 --raw disk_h1.scp
gw convert --format=<fmt> --reverse disk_h1.scp disk_h1.img
```

`--reverse` is required: the second surface was written for a flipped disc, so read in place it is rotationally reversed.
Verified symmetrically here - reading a known disc both ways round reproduced each side's known-good bytes exactly.

Two limits.
Some formats declare `heads = 1` and will refuse head 1 with "Out of range for format"; capture raw and decode with `ibm.scan --reverse` instead.
And on this drive head 1 sits **four cylinders inward**: head-1 cylinder N returns real track N+4, so the outermost four tracks of the second surface cannot be reached at all.
The Greaseweazle wiki documents `h1.off=-8` for flippy-modded drives, which is the same offset in physical steps.

## Compare decodes as sets, not by position

Two images of the same data decoded by different formats will not line up positionally, because each applies its own sector skew.
Comparing them index by index can report zero matching sectors while the two are in fact identical.
Compare them as multisets of sectors first, then establish the track mapping.
This nearly caused a correct result to be discarded here.

## The Z-machine checksum is weak

An Infocom story file's header declares a checksum, but it is a 16-bit **byte sum** over the body.
It cannot detect a permutation, and it is far too weak to select among candidate reassemblies of a split story: searching some 80,000 of them yields about 1.2 false matches by chance, and in practice two and three false matches were found.
Corroborate any reconstruction against a known build of the same game by longest-common-run, and establish a baseline with an *unrelated* game - a true match must beat that baseline comfortably.
On one title here, both checksum-valid candidates scored *below* the unrelated-game baseline and were correctly rejected.

## Story data is not always stored plainly

Whether a story file can be read straight off a decoded image varies by platform:

- **Apple II** stores story bytes plainly but paged, so byte-coverage against a reference works while a linear read does not.
- **Atari 8-bit** stores everything **inverted** (one's complement). Un-complemented, a good image shows no header, no text, and `0xFF` "fill" which is just `0x00` empty space stored inverted. Byte-coverage returns 0.0% on a side that provably contains the game until the image is complemented.
- **Commodore 64** stores data normally, in a real CBM DOS filesystem - though the directory may be vestigial, with the story body living outside it.

ZCut ([references.md](references.md)) understands all three layouts and is the practical way to extract a story file.
Verify its output independently, though: its own "Checksum good" is the byte sum described above.

## Capture size

Flux is roughly 33x the size of the decoded image, and retries multiply it.
A clean read stores about 125 KB per track; a read that fought an unreadable surface stored 746 KB per track, six times larger for the same 35 tracks.
On a surface expected to be blank or unreadable, `--retries=0` avoids the storm.
Do not drop to `--revs=1` to save space: one revolution loses exactly one sector per track, because a sector always straddles the index pulse.
`zstd -19` compresses clean flux to about 28% losslessly, and the decompressed file still decodes identically.
