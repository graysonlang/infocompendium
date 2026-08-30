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

The surprise is proportions: the five classic games this disc is named for occupy 1.3 MB of a 246 MB disc.

- **`ZORKANTH.RED` (1,289,064 bytes) holds the entire classic anthology** - Zork I, II, III, Beyond Zork, Zork Zero - as an Activision installer archive (magic bytes `52 52 01 29`, "RR"). Filenames are visible in the archive (`Z1.COM` is the first entry). The DOS `INSTALL.EXE` unpacks it; the files do not exist loose on the disc.
- **Most of the disc is Return to Zork demo/full data**: `RTZ.PRJ` (47 MB), `RTZCD.PRJ` (43 MB), and dozens of `.MMV`/`.PMV`/`.LMV` movie files at root, plus `RTZCD.RED`/`RTZCDDRV.RED` installer archives.
- **Demos of four products** (per `DEMOS/READ.ME`, dated 1994-09-12): Simon the Sorcerer CD-ROM (`SIMON.GME`, `SIMON.VOC` at 34 MB), Return to Zork, MechWarrior 2: The Clans (`MECH2/`), and **Planetfall: Floyd Strikes Back** (`PLANETF.IBM`, 7.6 MB).

## Findings

- **"Planetfall: Floyd Strikes Back" is the demo's 1994 title.** The cancelled Planetfall sequel is usually referred to as *Planetfall: The Search for Floyd* (the title associated with the promotional `planetfall.avi` on the 1996 Masterpieces disc - see [that disc's notes](../masterpieces-1996/notes.md)). This disc's READ.ME uses "Floyd Strikes Back" two years earlier, and ships a 7.6 MB `PLANETF.IBM` demo of it. The two discs bracket the project's public naming history.
- The READ.ME also dates Simon the Sorcerer's CD-ROM release as "available ... in 1995" and notes Return to Zork was already out on Mac CD-ROM.
- `.RED` is Activision's in-house installer archive format of this era (`INSTALL.EXE`/`INSTALL.DAT`/`ITXT.*` framework, "RR" magic). `DRIVERS.RED` and the RTZ `.RED` files use the same container.

## Open items for this disc

- Unpack `ZORKANTH.RED` to enumerate the exact game builds (releases/serials) shipped, and compare against the LTOI and Masterpieces builds. Options: run `INSTALL.EXE` under DOSBox against the mounted ISO, or reverse the `.RED` container.

Resolved 2026-08-29: Redump verification.
The full dump hashes byte-identical to redump.org disc 82144; see [checksums.txt](checksums.txt).
