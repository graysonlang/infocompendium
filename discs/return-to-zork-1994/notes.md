# Return to Zork CD-ROM v1.1 (1994) - findings

Established against a physical pressing read on an Apple Silicon Mac with a Pioneer BD-RW BDR-XS07U.
The general method is in [docs/imaging.md](../../docs/imaging.md); this file holds what is specific to this disc.

## Identity

Mixed-mode CD: one Mode 1 data track (volume `RTZ-CD`, 81843 sectors) followed by 25 Red Book audio tracks, 191601 sectors in all.
`DISK.ID` reads "Return to Zork CD-ROM / 1.1 / Disk #1", dated 1993-12-12; the `READ.ME` is dated 7 December 1993 and the disc root 1994-02-07.
169 files; see [return-to-zork-1994.ls.txt](return-to-zork-1994.ls.txt).

Return to Zork exists in at least a dozen Redump-cataloged pressings (versions 1.00, 1.1 and 1.2, an OEM bundle, Megapak, Special Edition, FM Towns, and console ports).
This copy's sector count matches redump.org disc 80660 exactly - version 1.1, tagged "Rerelease", write offset -22 - while two other v1.1 entries (126092 and the OEM bundle 33185) are three sectors shorter.

## Structure

- **The 1993 Return to Zork build**: `RTZCD.PRJ` (43,016,792 bytes, 1993-09-15) and 84 `.PMV` movie files, identical in size and date to the copies on the 1997 Zork Legacy Collection disc. The 25 audio tracks are the game's CD audio.
- **The v1.1 installer**: `INSTALL.EXE`/`INSTALL.DAT`, `RTZCD.RED` (276,177 bytes, 1994-01-31) and `RTZCDDRV.RED` (111,013 bytes, 1994-02-06).
- **Three demos**, per the README: Simon the Sorcerer (`SIMON/`, 63 files - a playable demo run through `RUNVGA GDEMO`), MechWarrior II: The Clans (`MECH2/`, an intro movie), and Richard Scarry's Best Neighborhood Disc Ever (`SCARRY/`, `BEST.EXE` with a `BESTDEMO.PRJ` and four movies). The README promises MechWarrior II "early in 1994" - it shipped in 1995 - and the two Richard Scarry titles for IBM and Macintosh CD-ROM in early 1994.

## Compared with the 1997 Zork Legacy Collection pressing

The same disc, revised twice over. Against [the 1997 disc](../zork-legacy-1997-rtz-anthology/notes.md):

- **The game itself is unchanged.** 92 of the 97 filenames the two data volumes share are identical in size and date - every movie and the 43 MB `.PRJ` among them.
- **The install set was revised.** The five differing files are `DISK.ID` (v1.1 -> v1.2), `READ.ME`, `INSTALL.DAT`, `RTZCD.RED` (276,177 -> 276,584 bytes) and `RTZCDDRV.RED` (111,013 -> 104,708), all redated September 1994. With the 1994 Zork Anthology disc's much smaller `RTZCD.RED` (130,683 bytes, a demo install set), that makes three distinct Return to Zork `.RED` builds across three discs.
- **The demos were swapped.** This disc's Simon/MechWarrior II/Richard Scarry demos are gone from the 1997 disc, replaced by the anthology, the InstallShield Windows front end, and the PDF documentation - which is where the 1997 data track's extra 12,739 sectors go.
- **The audio was re-cut.** Every audio track on the 1997 disc is longer by the same amount: +304 sectors (4.05 seconds) on tracks 3-25, with the first and last audio tracks differing by 150 sectors either side of that because of how the pregaps fall. The 1997 mastering evidently padded each track, and its Redump entry carries a write offset of 0 against this disc's -22.

## Open items for this disc

- Redump hash verification of the full dump (in progress).
