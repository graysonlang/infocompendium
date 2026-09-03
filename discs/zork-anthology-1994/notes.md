# The Zork Anthology (1994) - findings

Established against a physical pressing read on an Apple Silicon Mac with a Pioneer BD-RW BDR-XS07U.
The general method is in [docs/imaging.md](../../docs/imaging.md); this file holds what is specific to this disc.

## Identity

Plain ISO 9660, volume `ZORK_ANTHOLOGY`, one session, one Mode 1 data track, 120295 blocks = 282,933,840 bytes of user data.
`DISK.ID` reads "The Zork Anthology / 1.0 / ZORK".
Not a hybrid: there is no HFS side, and modern macOS mounts it directly.
94 files in three directories (root, `DEMOS`, `MECH2`); see [zork-anthology-1994.ls.txt](zork-anthology-1994.ls.txt).

Redump has two pressings of this disc: disc 82144 (120295 sectors, tagged "Original, Special Edition") matches this copy's block count exactly; disc 80023 is a different mastering (120445 sectors, tagged "Version 1.0").

## Structure: an installer disc, and mostly not the anthology

The surprise is proportions: the six classic games this disc carries occupy 1.3 MB of a 246 MB disc.

- **`ZORKANTH.RED` (1,289,064 bytes) holds the entire classic anthology** - Zork I, II, III, Zork Zero, Beyond Zork, and the box's bonus game Planetfall - as an Activision installer archive (magic bytes `52 52 01 29`, "RR"). The DOS `INSTALL.EXE` unpacks it; the files do not exist loose on the disc.
- **Most of the disc is Return to Zork demo/full data**: `RTZ.PRJ` (47 MB), `RTZCD.PRJ` (43 MB), and dozens of `.MMV`/`.PMV`/`.LMV` movie files at root, plus `RTZCD.RED`/`RTZCDDRV.RED` installer archives.
- **Demos of four products** (per `DEMOS/READ.ME`, dated 1994-09-12): Simon the Sorcerer CD-ROM (`SIMON.GME`, `SIMON.VOC` at 34 MB), Return to Zork, MechWarrior 2: The Clans (`MECH2/`), and **Planetfall: Floyd Strikes Back** (`PLANETF.IBM`, 7.6 MB).

## Inside ZORKANTH.RED

The `.RED` container turned out to be simple enough to read without running the installer.
It is a bare concatenation of member records, each one self-contained (measured on this file; the whole archive walks cleanly as 27 records with no global header or directory):

| Offset | Size | Field |
| --- | --- | --- |
| +0 | 4 | Magic `52 52 01 29` ("RR") |
| +4 | 4 | DOS packed timestamp (time in the low word, date in the high word), little-endian like all fields |
| +8 | 4 | Compressed size |
| +12 | 4 | Uncompressed size |
| +16 | 2 | `FF FF` on every compressed member; on stored members it repeats the CRC at +18 |
| +18 | 2 | CRC-16 of the uncompressed data |
| +20 | 2 | Zero |
| +22 | 2 | 1 |
| +24 | 2 | Method: 1 = stored, 11 = compressed |
| +26 | 13 | Filename, 8.3 plus NUL padding |
| +39 | 2 | Unidentified (varies per member) |
| +41 | comp | Payload |

The CRC is CRC-16/CCITT-FALSE (polynomial `0x1021`, init `0xFFFF`, non-reflected, no final XOR), determined by brute-forcing the parameters against the stored members, whose payloads are readable in place.
The method-11 compression itself has not been identified (it is not PKWARE DCL), but it does not need to be: the recorded uncompressed size and CRC-16 identify every member against known files.

All 27 members: `Z1.COM`, `Z2.COM`, `Z3.COM`, `PF.COM`, `BZORK.EXE`, `ZORK1.DAT`, `ZORK2.DAT`, `ZORK3.DAT`, `PLANETFA.DAT`, `BEYONDZO.DAT`, `ZORKZERO.EXE`, `ZORK0.EG1`, `ZORK0.CG1`, `ZORK0.ZIP`, `ZORK0.BAT`, `NNANSI.COM`, `ZORK1.BAT`, `ZORK2.BAT`, `ZORK3.BAT`, `PLANETF.BAT`, six `.ICO` files, and a `ZORK.GRP` Program Manager group.
The internal timestamps tell the disc's build story: game payloads April-May 1992, `NNANSI.COM` January 1993, and the Windows dressing (icons, batch files, `ZORK.GRP`) August 1994.
Even `ZORK0.BAT` is the 1992 LTOI file, stored with its 1992-05-11 timestamp.

Every game file's size and CRC-16 match the byte-identical files on the [1992 LTOI CD](../lost-treasures-1-1992/notes.md) and (via the shared lineage) [Masterpieces](../masterpieces-1996/notes.md) and the [1997 Legacy Collection disc](../zork-legacy-1997-rtz-anthology/notes.md); the per-title table is in [versions.md](versions.md).
This closes the loop on the shared-masters chain: the same 1992 files ship unmodified on all four products, 1992 through 1997.

## Findings

- **"Planetfall: Floyd Strikes Back" is the demo's 1994 title.** The cancelled Planetfall sequel is usually referred to as *Planetfall: The Search for Floyd* (the title associated with the promotional `planetfall.avi` on the 1996 Masterpieces disc - see [that disc's notes](../masterpieces-1996/notes.md)). This disc's READ.ME uses "Floyd Strikes Back" two years earlier, and ships a 7.6 MB `PLANETF.IBM` demo of it. The two discs bracket the project's public naming history.
- The READ.ME also dates Simon the Sorcerer's CD-ROM release as "available ... in 1995" and notes Return to Zork was already out on Mac CD-ROM.
- `.RED` is Activision's in-house installer archive format of this era (`INSTALL.EXE`/`INSTALL.DAT`/`ITXT.*` framework, "RR" magic). `DRIVERS.RED` and the RTZ `.RED` files use the same container.

## Open items for this disc

- Identify the `.RED` method-11 compression, so members can actually be extracted rather than just verified. Until then, `INSTALL.EXE` under DOSBox remains the way to unpack.

Resolved 2026-09-02: the game builds inside `ZORKANTH.RED` are enumerated and matched against the other discs via the container's own size and CRC-16 records; see the section above and [versions.md](versions.md).

Resolved 2026-08-29: Redump verification.
The full dump hashes byte-identical to redump.org disc 82144; see [checksums.txt](checksums.txt).
