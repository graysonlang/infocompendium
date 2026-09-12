# Media assets across the collections

Six Infocom titles carry media: the four V6 graphical games (Zork Zero, Arthur, Journey, Shogun) and the two with sampled sound (Sherlock on the Mac, The Lurking Horror on the PC).
This table records which collections carry each title's assets and which files those are, as measured on the cataloged media; the per-disc detail lives in each disc's notes.

File vocabulary: PC graphics are `.CG1` (CGA, two-color), `.EG1`/`.EG2` (EGA, split when the set exceeded a 360K floppy), `.MG1` (MCGA); Mac graphics are `PIC.DATA` (black-and-white) and `CPIC.DATA` (color).

## Graphics

| Title | Side | LTOI1 (1992) | LTOI2 (1992) | Anthology (1994) | Masterpieces (1996) | Legacy (1997) | Source leak (2019) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zork Zero | Mac | PIC, CPIC | - | - | PIC, CPIC | - | - |
| Zork Zero | PC | CG1, EG1 | - | CG1, EG1 (inside the installer archive) | CG1, EG1 | CG1, EG1 | - |
| Arthur | Mac | - | PIC, CPIC | - | PIC, CPIC | - | - |
| Arthur | PC | - | CG1, EG1, EG2, MG1 | - | CG1, EG1, EG2, MG1 | - | - |
| Journey | Mac | - | PIC, CPIC | - | PIC, CPIC | - | PIC (`journey.bwmac.1`) |
| Journey | PC | - | CG1, EG1, EG2, MG1 | - | CG1, EG1, EG2, MG1 | - | - |
| Shogun | Mac | - | PIC, CPIC | - | - | - | PIC, CPIC and Apple II pictures, different versions |
| Shogun | PC | - | CG1, EG1, MG1 | - | - | - | - |

Every repeated file is byte-identical across the collections that carry it, verified by hash: Zork Zero's four PC files across all four of its discs and its Mac pictures across both hybrids; Arthur's and Journey's complete Mac and PC sets between LTOI2 and Masterpieces; and Journey's Mac `PIC.DATA` a third time in the leaked `journey` repository, where `journey.bwmac.1` is the same 473,730 bytes exactly.

What the gaps mean:

- **Zork Zero's `.MG1` is the one genuinely missing file** - absent from every disc here, though the complete set is only three files (its EGA never needed an `.EG2`). The IF Archive's separately hosted `zorkzero.mg1` is the genuine Infocom file, not a conversion: 226,436 bytes in PC little-endian format with 503 images, including the twenty PC-only pictures (the r393 border columns and metrics) that exist in no Amiga or Mac rendition - so no conversion from those renditions could produce it. Its provenance is settled against physical media: disk 1 of the 3.5" side of an original 1989 dual-media MS-DOS Zork Zero (this repo's owner's copy, imaged 2026-09-12) carries `ZORK0.MG1`, dated 1989-07-10, **byte-identical to the archive's copy** - which was uploaded 1994-05-16 with an index note that it "was left out of the Lost Treasures of Infocom I package". So the file shipped retail on the 3.5" diskettes (the same place Journey's VGA rendition rode, per Graeme Cree's testimony quoted in that index), LTOI1 dropped it in 1992, and the community restored it from the retail edition two years later. The box also shows the renditions were media-targeted - its 3.5" set carries no `EG1` despite free space, while the 5.25" set's three-diskette budget has room for EGA but not MCGA; see [the floppy entry](../discs/zork-zero-1989-dos/notes.md). The same floppy's `ZORK0.ZIP` and `ZORKZERO.EXE` are byte-identical to the LTOI1 copies, so the compilations' entire Zork Zero PC lineage traces to this disk, minus its `MG1`. (The archive index labels its one actual fabrication as such: `beyondzo.mg1`, the Atari ST Beyond Zork title picture converted by Stefan Jokisch in 1997.) The `MG1` is also not interchangeable with the Mac `CPIC.DATA`: that is the 483-image r296-era library whose borders are full 320x200 frames, where the MG1's are the r393 banner-plus-columns cut - each pairs only with its own story release.
- **Shogun's three files are its complete PC set** (its fifty EGA pictures fit one file), and its graphics survive only on LTOI2 among the discs - Masterpieces dropped the title. The leaked `shogun` repository carries Mac and Apple II picture files (`a5.mac.1`, `a5.bwmac.1`, `a5.apple.1`) at sizes close to but not equal to LTOI2's, consistent with its later r322-era snapshot against the disc's r292-era Mac release.
- **Arthur's EGA files exist only because a CD wanted them**: the original floppy release shipped `MG1`, `CG1` and the `FILECVT.EXE` converter instead of EGA art; LTOI2's mastering pregenerated `EG1`/`EG2` in October 1992 and every later appearance inherits them. See [the LTOI2 notes](../discs/lost-treasures-2-1992/notes.md).
- The leaked repositories otherwise carry no PC graphics libraries at all - for Zork Zero only the picture-manifest sources (`zork0.zpic`, a text file of picture names; `zork0.pic`, its offset table), which is consistent with the art being drawn on the Amiga and converted elsewhere.

## Sound

| Title | Medium | LTOI2 (1992) | Masterpieces (1996) | Source leak (2019) |
| --- | --- | --- | --- | --- |
| Sherlock | Mac `SOUND/` folder | 13 `S` + 4 `M` files | 13 `S` + 4 `M` files (byte-identical) | raw sample sources and the number-to-name map |
| The Lurking Horror | PC, Sound Blaster | - | `LHSOUND.ZIP` (14 `.SND` files + the XOR patch to r221) | the r221 story file, no sounds |

Sherlock's sound numbers decode via the leaked repository's `s3.nam`-`s17.nam` files, each naming a sample and a MIDI companion:

| # | Sample | # | Sample | # | Sample |
| --- | --- | --- | --- | --- | --- |
| S3 | armor | S8 | crowd1 | S13 | heart (variant) |
| S4 | badvio | S9 | fanfare | S14 | horse |
| S5 | bark | S10 | growl | S15 | violin |
| S6 | splash | S11 | heart | S16 | snore |
| S7 | benclk (Big Ben) | S12 | heart (variant) | S17 | ben2 |

The Mac discs ship `S` files for thirteen of the fifteen numbers (S11 and S13, two of the three heart variants, appear only as 32-byte `M` files, alongside `M8` and `M14`).
The Lurking Horror's sound was native to the Amiga; no cataloged disc carries those samples, and the Masterpieces package is Stefan Jokisch's 1995 freeware conversion kit, not Infocom's - see [the Masterpieces notes](../discs/masterpieces-1996/notes.md) for its verification.
