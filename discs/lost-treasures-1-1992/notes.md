# The Lost Treasures of Infocom CD (1992) - findings

Established against a physical pressing read on an Apple Silicon Mac with a Pioneer BD-RW BDR-XS07U.
The general method is in [docs/imaging.md](../../docs/imaging.md); this file holds what is specific to this disc.

## Identity

A single Mode 1 data track of just 3,895 sectors - 7,976,960 bytes of user data on the whole disc.
ISO 9660, volume `INFOCOM`, system identifier "APPLE COMPUTER, INC., TYPE: 0002" (Apple ISO extensions).
`DISK.ID` reads "LTOICD / 1.0 / Disk 1"; the volume is mastered 1992-05-26.
93 listing lines; see [lost-treasures-1-1992.ls.txt](lost-treasures-1-1992.ls.txt).

**Redump has no Lost Treasures entry** (checked 2026-09-02): [checksums.txt](checksums.txt) is offered as the reference for this pressing.

## Structure: one ISO, both platforms

`MAC/` and `PC/` sit side by side in one plain ISO - so at least this pressing of volume 1 is a combined disc, not the separate per-platform releases sometimes described.

- `MAC/` holds all 20 games. Nineteen are single files (the z-code in the data fork); Zork Zero is a folder with `STORY.DATA`, `PIC.DATA`, `CPIC.DATA` and the application. Resource forks travel as Apple-extension *associated files* whose content is the raw fork, with type/creator/Finder flags in an `AA` system-use field on each directory record. Modern macOS synthesizes `._Name` AppleDouble companions from these (with little-endian integers, oddly) but its cd9660 driver returns EINVAL when *opening* the fork-bearing data files themselves, so the mounted volume cannot be copied - extract from the image with `scripts/appleiso.py`, which reads the ISO structure directly.
- `PC/` holds per-game interpreter `.COM`/`.EXE` files, a shared `DATA/` directory of 19 padded story files, and `ZORK0/` with the interpreter and graphics.

The full per-title release table for both platforms is in [versions.md](versions.md).

## Findings

- **The Zork Zero graphics omission starts here.** `PC/ZORK0/` carries only `ZORK0.CG1` and `ZORK0.EG1` - no `.MG1`, no `.EG2` - exactly as Doherty documented for LTOI1's IBM packages, now confirmed on the CD itself. The same four-file set (with `.ZIP` and interpreter) was carried byte-for-byte into Masterpieces (1996) and the Zork Legacy Collection (1997).
- **The padding is caret characters.** Each padded story file has three layers: the z-code to its header-declared length, then Infocom's own padding (zeros to a 512-byte boundary - Zork I's padded 84,992 bytes exactly matches the Mac data fork on this disc - or a single `$1a` DOS end-of-file marker), then thousands of literal ASCII `^` (0x5E) characters out to the round CD size. The caret fill is this mastering's signature, reproduced byte-for-byte on every later disc that inherited these files.
- **The shared `DATA/` story files are the originals.** All 18 that reappear on Masterpieces' `PC/DATA/` (and inside the Legacy Collection's installer) hash identical to these 1992 files: the padded set was mastered once, in May 1992, and reused unchanged for five years.
- **Three titles ship as different builds per platform** (see [versions.md](versions.md)), and not in one consistent direction. Hitchhiker's: the PC gets the Solid Gold build (r31.871119, in-game hints) while the Mac gets plain 1985 r59.851108. Planetfall: reversed - the Mac gets Solid Gold v5 r10.880531 while the PC keeps plain v3 r37.851003. Zork Zero: Mac r296.881019 vs PC r393.890714, the same split later inherited by Masterpieces and the Legacy Collection - that asymmetry starts on this disc. Hitchhiker's itself was later dropped from Masterpieces entirely. PC release table: Ballyhoo r97.851218, Beyond Zork r57.871221, Deadline r27.831005, Enchanter r29.860820, Hitchhiker's r31.871119, Infidel r22.830916, Lurking Horror r203.870506, Moonmist r9.861022, Planetfall r37.851003, Sorcerer r15.851108, Spellbreaker r87.860904, Starcross r17.821021, Stationfall r107.870430, Suspect r14.841005, Suspended r8.840521, Witness r22.840924, Zork I r88.840726, Zork II r48.840904, Zork III r17.840727.
- The Mac Zork I file is dated 1991-10-28 - the same day as the creation date recovered from Masterpieces' Mac `ZORK I` birth time, tying that provenance chain back to the LTOI mastering.

## Open items for this disc

Resolved 2026-09-02: full extraction with forks.
`scripts/appleiso.py` reads the image natively (the cd9660 driver cannot open the Mac files at all) and restores all 20 resource forks, FinderInfo from the `AA` fields, and timestamps; 72 files, 0 failures.
- The Lost Treasures of Infocom II CD is not yet imaged (Redump disc 105382 exists for it).
