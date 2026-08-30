# Return to Zork CD-ROM v1.1 (1994) - findings

Established against a physical pressing read on an Apple Silicon Mac with a Pioneer BD-RW BDR-XS07U.
The general method is in [docs/imaging.md](../../docs/imaging.md); this file holds what is specific to this disc.

## Identity

Mixed-mode CD: one Mode 1 data track (volume `RTZ-CD`, 81843 sectors) followed by 25 Red Book audio tracks, 191601 sectors in all.
`DISK.ID` reads "Return to Zork CD-ROM / 1.1 / Disk #1", dated 1993-12-12; the `READ.ME` is dated 7 December 1993 and the disc root 1994-02-07.
169 files; see [return-to-zork-1994.ls.txt](return-to-zork-1994.ls.txt).

Return to Zork exists in at least a dozen Redump-cataloged pressings (versions 1.00, 1.1 and 1.2, an OEM bundle, Megapak, Special Edition, FM Towns, and console ports).
This copy's sector count matches redump.org disc 80660 exactly - version 1.1, tagged "Rerelease", write offset -22 - while two other v1.1 entries (126092 and the OEM bundle 33185) are three sectors shorter.

**The pressing is Redump-verified, all 26 tracks.**
A full linear raw dump made 2026-08-29, split at Redump's boundaries and corrected by 645 samples, hashes byte-identical to disc 80660 on every track; see [checksums.txt](checksums.txt).
Two things had to be right for that to work, both learned on this disc: the correction is the *combined* offset (the drive's +667 read offset plus the disc's -22 write offset), and only track 2 carries a 150-sector pregap - the pause required after a data track - while the audio tracks that follow are gapless, so each later track's file begins exactly at its TOC start.

## Structure

- **The 1993 Return to Zork build**: `RTZCD.PRJ` (43,016,792 bytes, 1993-09-15) and 84 `.PMV` movie files, identical in size and date to the copies on the 1997 Zork Legacy Collection disc. The 25 audio tracks are the game's CD audio.
- **The v1.1 installer**: `INSTALL.EXE`/`INSTALL.DAT`, `RTZCD.RED` (276,177 bytes, 1994-01-31) and `RTZCDDRV.RED` (111,013 bytes, 1994-02-06).
- **Three demos**, per the README: Simon the Sorcerer (`SIMON/`, 63 files - a playable demo run through `RUNVGA GDEMO`), MechWarrior II: The Clans (`MECH2/`, an intro movie), and Richard Scarry's Best Neighborhood Disc Ever (`SCARRY/`, `BEST.EXE` with a `BESTDEMO.PRJ` and four movies). The README promises MechWarrior II "early in 1994" - it shipped in 1995 - and the two Richard Scarry titles for IBM and Macintosh CD-ROM in early 1994.

## Gaps, post-gap and padding

Measured on the raw dump (2026-08-29):

- **The data track is padded by a minute.** The ISO volume declares 77,268 sectors, but the data track runs to 81,843: the last 4,575 sectors (9.4 MB, 61 seconds) are structured empty Mode 1 sectors - sync, headers, EDC and ECC present, user data all zero. The Yellow Book calls for about two seconds of such post-gap before a mode change; this is thirty times that, and the reason is unknown. (The 1997 pressing has exactly 152.)
- **The pregap before track 2 is 150 sectors of digital silence**, all zero bytes. In an uncorrected dump its tail holds the first 2,580 bytes of track 2's audio, pulled back by the drive's read offset; the correction restores them.
- **No pregaps between audio tracks.** The silence between songs is inside the audio instead: the last 75 sectors (one second) of track 2 are zero and track 3 sounds from its first sector. The 1997 pressing does the opposite, with a 150-sector zero pregap before every track.

## Compared with the 1997 Zork Legacy Collection pressing

The same disc, revised twice over. Against [the 1997 disc](../zork-legacy-1997-rtz-anthology/notes.md):

- **The game itself is unchanged.** 92 of the 97 filenames the two data volumes share are identical in size and date - every movie and the 43 MB `.PRJ` among them.
- **The install set was revised.** The five differing files are `DISK.ID` (v1.1 -> v1.2), `READ.ME`, `INSTALL.DAT`, `RTZCD.RED` (276,177 -> 276,584 bytes) and `RTZCDDRV.RED` (111,013 -> 104,708), all redated September 1994. With the 1994 Zork Anthology disc's much smaller `RTZCD.RED` (130,683 bytes, a demo install set), that makes three distinct Return to Zork `.RED` builds across three discs.
- **The demos were swapped.** This disc's Simon/MechWarrior II/Richard Scarry demos are gone from the 1997 disc, replaced by the anthology, the InstallShield Windows front end, and the PDF documentation - which is where the 1997 data track's extra 12,739 sectors go.
- **The audio was re-cut.** This disc's audio is gapless after track 2; the 1997 disc inserts a 2-second (150-sector) pregap before every audio track, and each track's content is also 154 sectors (2.05 seconds) longer, the last track's 304. The two masterings also differ in write offset: -22 here, 0 on the 1997 disc.

## Open items for this disc

None.

Resolved 2026-08-29: Redump verification, all 26 tracks; see above.
