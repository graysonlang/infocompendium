# The Lost Treasures of Infocom II CD (1992) - findings

Established against a physical pressing read on an Apple Silicon Mac with a Pioneer BD-RW BDR-XS07U.
The general method is in [docs/imaging.md](../../docs/imaging.md); this file holds what is specific to this disc.

## Identity

A single 12.4 MB ISO 9660 data track: one session, 6,075 blocks = 12,441,600 bytes of user data, volume `LOST TREASURES II`.
Apple ISO extensions carry the `MAC` and `DOS` trees side by side on the one filesystem, exactly the shape of [volume 1](../lost-treasures-1-1992/notes.md); macOS mounts it but its cd9660 driver cannot open the fork-bearing Mac files, so extraction goes through `scripts/appleiso.py` (114 files, 18 resource forks, 0 failures).
The PVD was created 1992-11-06 14:12:33 (volume 1's was mastered 1992-05-26, so the two CDs were mastered about five months apart).
114 files; see [lost-treasures-2-1992.ls.txt](lost-treasures-2-1992.ls.txt).

**The pressing is Redump-verified.**
The raw dump made 2026-09-11 hashes byte-identical to redump.org disc 105382, edition "CD-ROM Version (3 Bonus Titles)", write offset 0; see [checksums.txt](checksums.txt).

## Structure

- `MAC/` holds all fourteen games: eleven as double-clickable applications with the z-code in the data fork, plus `ARTHUR FOLDER`, `JOURNEY FOLDER` and `SHOGUN FOLDER` with `STORY.DATA`/`PIC.DATA`/`CPIC.DATA` beside the application, and `SOUND/` with Sherlock's seventeen sound files (thirteen `S` files plus four 32-byte `M` files, February 1988).
- `DOS/` holds one folder per game - story file, per-game interpreter, `SETUP.EXE` (1,584 bytes) and `YES.COM` - plus `INFOCOM2.BAT`, an F-key launcher menu, and `REPLY.COM` at root.
- **No shared `DATA/` directory and no padding.** Volume 1's padded-to-round-sizes, caret-filled story files are absent here; every DOS story file is natural size plus a `$1a` terminator (`AMFV.DAT` 262,018 for 262,016 bytes of z-code, `BORDERZO.DAT` 178,373 for 178,372). The two 1992 CDs were mastered by different processes.

The full per-title release table for both platforms is in [versions.md](versions.md).

## Findings

- **This disc is Masterpieces' other source.** All thirteen titles shared with [Masterpieces (1996)](../masterpieces-1996/notes.md) are byte-identical to Masterpieces' builds on both platforms - and the DOS files match at full-file level, `$1a` terminators and all, which identifies Masterpieces' "natural size +1" provenance of PC story file as this disc's file set. The Mac/PC build splits Masterpieces shows for Arthur (r54/r74), Journey (r26/r83), Seastalker (r15/r16), Sherlock (r26/r21) and Wishbringer (r68/r69) all originate here, completing the pattern begun on volume 1 (Planetfall, Hitchhiker's, Zork Zero).
- **Shogun survives here and nowhere else in this catalog.** The three bonus titles are Arthur, Journey and Shogun - and Shogun is the title Masterpieces later dropped along with Hitchhiker's. The Mac build r292.890314 appears on no other cataloged medium (the leaked source repositories carry only r322); the PC build r322.890706 is byte-identical, full file, to `COMPILED/a5.zip` in the [leaked shogun repository](../../collections/historicalsource/versions.md). Both builds carry built-in hints.
- **Shogun ships three graphics libraries and that is the complete set**: `SHOGUN.CG1`, `.EG1` and `.MG1`, all dated June-July 1989, with no `.EG2` - but unlike Zork Zero's genuinely missing files, nothing is absent: Shogun's `.EG1` covers all 50 picture numbers by itself (see the `.EG2` note below), so there was never an `.EG2` to omit.
- **Arthur's EGA files were made for this disc; Journey's are the 1989 originals restamped.** Doherty documents Arthur's original MS-DOS release as shipping *no* EGA file at all - just `MG1`, `CG1`, and `FILECVT.EXE`, a converter that generates the EGA and CGA renditions from the MCGA master on the customer's machine. This disc's `ARTHUR.EG1`/`.EG2`, dated 1992-10-22 against 1989 dates on Arthur's other files, are therefore pregenerated for the CD (consistent with running Infocom's own converter during mastering, two weeks before the PVD date). Journey's `.EG1`/`.EG2` carry 1992-10-27 stamps but their sizes (360,500 / 249,241) match Doherty's original 1989-07-07 files exactly - originals recopied, not reconverted. The same files resurface inside Masterpieces' `DATA.Z` - including `JOURNEY.MG1`, whose 1996-06-13 stamp on Masterpieces covers a file byte-identical to this disc's 1992 copy. The timestamp stratigraphy recorded in the Masterpieces notes traces back to this mastering.
- **The `.CG1` files use a different pixel format, and `pix2gif` cannot decode it.** Arthur's `.CG1` looks broken in tooling - `pix2gif` emits blank white images for its art - but the file is fine: 170 directory entries, 136 with real compressed data (median 1.7 KB per picture), 34 with no data at all (the invisible layout-metrics pictures), byte-identical to Masterpieces' copy. The tell is a flag: every data-bearing image in every `.CG1` here (Arthur 136/136, Journey 134/134, Shogun 44/44) carries directory-flag bit 3 (`0x0008`), which no `.EG1` image has - it marks the CGA format, and `pix2gif`, documented for "MG1/EG1 files", ignores the bit and mis-decodes the stream. The dimensions give away what that format is: `.CG1` art is the same 584x196-class geometry as the EGA art, impossible in CGA's 4-color mode but native to its 640x200 two-color mode, and each picture's compressed data runs one-half to one-third of its EGA counterpart - one bit per pixel instead of four. `scripts/picdir.py` lists all four libraries correctly; only pixel decoding is affected.
- **`.EG2` is the EGA overflow file, and the overflow threshold is a 360K floppy.** Arthur's EGA art is split across `EG1` (125 images, 223,522 bytes) and `EG2` (101 images, 154,137 bytes), Journey's across 360,500 and 249,241 bytes - and in each case the two halves together exceed a 360K disk's capacity while each half fits, Journey's `EG1` with under 2K to spare. The EGA rendition targeted the era's lowest common medium; the CGA files fit a floppy whole, and MCGA (Journey's is 465,606 bytes, over 360K by itself) implied a PS/2-class machine with 3.5" drives, so neither needed splitting.
Period testimony corroborates this: the IF Archive's MCGA index quotes Graeme Cree that Journey's dual-media box put the VGA version only on the 3.5" diskettes, which is why used copies sold without them lack the `.MG1`. The split is play-aware, not a blind cut: 55 of Arthur's pictures and 12 of Journey's appear in *both* halves, duplicated so common elements need no disk swap. Shogun's fifty EGA pictures fit one file (verified: its `EG1` covers every picture number its `CG1` has), so its lack of an `EG2` is not an omission - and per Doherty's graphics-file table, Zork Zero's EGA likewise fit one file and never had an `EG2` at all.
- **Interpreters match Doherty's size table** (11394=3L, 11402=3M2, 12004=3N, 12640=4A, 12682=4E, 12688=4D, 33946=5J, 47442=6.68, 47528=6.71) with one size the other discs never showed: Shogun's `SHOGUN.EXE` at 47,402 bytes, a V6 interpreter build absent from the table as previously cited.
- Mac `SOUND/` is byte-identical, all seventeen files, to Masterpieces' `MAC/SOUND/`.

## Open items for this disc

None.

Resolved 2026-09-11: imaged, Redump-verified, extracted with forks, versions enumerated - same day the disc arrived.
