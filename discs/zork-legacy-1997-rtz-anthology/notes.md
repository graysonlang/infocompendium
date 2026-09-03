# Return to Zork / The Zork Anthology (Zork Legacy Collection, 1997) - findings

Established against a physical pressing read on an Apple Silicon Mac with a Pioneer BD-RW BDR-XS07U.
The general method is in [docs/imaging.md](../../docs/imaging.md); this file holds what is specific to this disc.

## Identity

Mixed-mode CD: one Mode 1 data track (volume `RTZ_ZA`, 94582 sectors) followed by 25 Red Book audio tracks, 211940 sectors in all, lead-out at 47:07.65.
`DISK.ID` reads "Return to Zork CD-ROM / 1.2 / CD-ROM" and is dated 1994-09-29; the disc identifies itself as a Return to Zork CD-ROM, with the anthology added alongside.
Mastering dates run to 1997-03-10 (`AUTORUN.INF`), so the disc is a 1997 pressing.
173 files; see [zork-legacy-1997-rtz-anthology.ls.txt](zork-legacy-1997-rtz-anthology.ls.txt).

**The pressing is Redump-verified, all 26 tracks.**
A full linear raw dump made 2026-08-29, split at Redump's track boundaries and corrected for the drive's +667-sample read offset, hashes byte-identical to redump.org disc 128285 ("Return to Zork / The Zork Anthology", edition The Zork Legacy Collection, serial 1000028-104-U3, write offset 0) on every track; see [checksums.txt](checksums.txt).
The data track matched with no correction at all; the audio tracks only after the offset shift, which is how the drive's read offset was measured in the first place.

## Structure

Three layers of different ages sit on one disc:

- **Return to Zork, 1993 build.** `RTZCD.PRJ` (43,016,792 bytes, 1993-09-15) is the same size and date as the copy on [The Zork Anthology (1994)](../zork-anthology-1994/notes.md), and the 84 `.PMV` movie files at root are all dated 1993. The 25 audio tracks are Return to Zork's CD audio.
- **1994 installer layer.** `INSTALL.EXE`/`INSTALL.DAT` (the Activision DOS installer) and the `.RED` archives `RTZCD.RED`, `RTZCDDRV.RED` and `DRIVERS.RED`, all dated September 1994 - but at different sizes from the 1994 disc's (276,584 vs 130,683; 104,708 vs 101,827; 28,032 vs 27,847), so the RTZ install set was revised between the two pressings.
- **1997 Legacy Collection layer.** A Windows InstallShield front end (`SETUP.EXE`, `_SETUP.LIB`, `DATA.Z`, `UNINST.EXE`), `SPLASH.EXE` with `SP256/` button bitmaps, `AUTORUN.INF`, a 5 MB `AVI/MOVIE.AVI` (1997-03-10), Acrobat Reader in `ACRODOS/`, and the documentation as PDFs in `DATA/` (`FINAL.PDF` 11.6 MB, `MAPS.PDF`, `HINTS.PDF`, all 1997-03-07).

## Gaps and post-gap

Measured on the raw dump (2026-08-29): the ISO volume declares 94,430 sectors and the data track runs to 94,582, so the data track ends with 152 structured empty Mode 1 sectors - the standard two-second post-gap before the mode change, and nothing like the 61-second pad on the [1994 pressing](../return-to-zork-1994/notes.md).
The 150-sector pregap before track 2 and the 150-sector pregaps before each of tracks 3-26 are all pure digital silence; in an uncorrected dump the first pregap's tail carries the opening 2,668 bytes of track 2, displaced by the drive's read offset.

## The anthology games

The per-title release table, including the unadvertised story files, is in [versions.md](versions.md).
Unlike the 1994 disc, where the games hide inside `ZORKANTH.RED`, here they sit as loose files under `DATA/`:

- **Zork I, II, III** in `DATA/ZORK1..3/`: interpreter `_ZORKn.COM` at 11,402 bytes (Doherty's 3M2), `NNANSI.COM`, a `DATA/ZORKn.DAT` padded to 92,160 bytes, and a `SAVE/ZORKn.DAT`. Every file is dated 1995-05-31 except the saves.
- **Zork Zero** in `DATA/ZORKZERO/`: `ZORK0.ZIP` (300,032 bytes, r393), `ZORK0.CG1` (244,507) and `ZORK0.EG1` (333,654) plus `ZORKZERO.EXE` (47,494, interpreter 6.71) - byte-for-byte the same sizes as Masterpieces' `PC/ZORK0/`, and again **no `.MG1` and no `.EG2`**. The incomplete-graphics omission Doherty documented for LTOI1 persists on this disc too.
- **Beyond Zork**: `BZORK.EXE` (33,946 bytes, interpreter 5J) and `NNANSI.COM` sit in `DATA/` dated 1996-06-21, but there is no loose `BEYONDZO.DAT`. The story file ships inside the InstallShield `DATA.Z` - along with a great deal more; see below.
- **Real save files again.** `SAVE/ZORK1.DAT` (12,883 bytes), `ZORK2.DAT` (12,213) and `ZORK3.DAT` (12,680) are dated 1996-06-11 and are byte-identical to the saves on Masterpieces, which carry a 1996-06-22 stamp - so one set of saves, made on or before 11 June 1996, was reused across both products.

## Inside DATA.Z: fourteen unadvertised Infocom games

`DATA.Z` (2,835,304 bytes) is an InstallShield 3 archive - magic `13 5D 65 8C`, 42 members in 12 directories, PKWARE DCL "implode" compression - and it is what the Windows `SETUP.EXE` actually installs from.
`scripts/isz.py` lists and extracts it.

Its contents are the disc's `DATA/` tree again (the same 24 Zork I-III and Zork Zero files, byte-identical to the loose copies, plus `BZORK.EXE` and `NNANSI.COM`) **and a `DATA\` directory of 18 story files that is Masterpieces' `PC/DATA/` directory, byte for byte**, every one timestamped 1996-06-22 01:41, Masterpieces' mastering moment:

| File | Title | Release | On the box |
| --- | --- | --- | --- |
| `BALLYHOO.DAT` | Ballyhoo | r97.851218 | - |
| `BEYONDZO.DAT` | Beyond Zork | r57.871221 | yes |
| `DEADLINE.DAT` | Deadline | r27.831005 | - |
| `ENCHANTE.DAT` | Enchanter | r29.860820 | - |
| `INFIDEL.DAT` | Infidel | r22.830916 | - |
| `LURKING.DAT` | The Lurking Horror | r203.870506 | - |
| `MOONMIST.DAT` | Moonmist | r9.861022 | - |
| `PLANETFA.DAT` | Planetfall | r37.851003 | - |
| `SORCERER.DAT` | Sorcerer | r15.851108 | - |
| `SPELLBRE.DAT` | Spellbreaker | r87.860904 | - |
| `STARCROS.DAT` | Starcross | r17.821021 | - |
| `STATIONF.DAT` | Stationfall | r107.870430 | - |
| `SUSPECT.DAT` | Suspect | r14.841005 | - |
| `SUSPEND.DAT` | Suspended | r8.840521 | - |
| `WITNESS.DAT` | The Witness | r22.840924 | - |
| `ZORK1.DAT` | Zork I | r88.840726 | yes |
| `ZORK2.DAT` | Zork II | r48.840904 | yes |
| `ZORK3.DAT` | Zork III | r17.840727 | yes |

So a Zork Legacy Collection owner who runs the Windows installer receives the story files for fourteen Infocom games the product never mentions - no interpreters or documentation for them, just the padded `.DAT` files, playable in any Z-machine interpreter.
The simplest explanation is that the 1997 installer was built from Masterpieces' PC directory wholesale and nobody pruned the shared `DATA/` folder.
Beyond Zork's story file, the one anthology game not loose on the disc, is identical to Masterpieces' copy.

## Open items for this disc

Resolved 2026-08-29: `DATA.Z` extracted; see the section above.

Resolved 2026-08-29: Redump verification, including the audio tracks.

Resolved 2026-08-29: the anthology files are the same builds as Masterpieces'.
All 24 files compared against Masterpieces' `PC/` tree hash identical (SHA-1): the three Zork I-III sets (interpreter, `NNANSI.COM`, `SETUP.INF`, batch file, padded story file, and save), all four Zork Zero files, `BZORK.EXE` and the root `NNANSI.COM`.
The story files are Zork I r88.840726, Zork II r48.840904, Zork III r17.840727 and Zork Zero r393.890714.
The save files being identical settles their date: this disc stamps them 1996-06-11, so Masterpieces' 1996-06-22 stamps on the same bytes are its mastering date, and the saves were made on or before 11 June 1996.

