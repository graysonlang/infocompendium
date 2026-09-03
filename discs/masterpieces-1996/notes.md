# Classic Text Adventure Masterpieces of Infocom (1996) - findings

Established against a physical pressing read on an Apple Silicon Mac with a Pioneer BD-RW BDR-XS07U.
The general method and its pitfalls are in [docs/imaging.md](../../docs/imaging.md) and [docs/hfs-extraction.md](../../docs/hfs-extraction.md); this file holds only what is specific to this disc.

## Identity

Hybrid CD: one Mode 1 data track carrying an ISO 9660 catalog (260 KB slice, pointer structure only) and an HFS catalog (308 MB volume holding everything).
Volume `Masterpieces`, created 18 June 1996, modified 22 June 1996.
`drutil status` reports 150515 blocks; 150515 x 2048 = 308,254,720 bytes of user data is the number to verify any image against.
879 catalog entries: 113 directories, 766 files.
See [disc-info.txt](disc-info.txt) for the captured TOC and slice layout.

**The pressing is Redump-verified.**
A full raw dump made 2026-08-29 hashes byte-identical to redump.org disc 64685 (serial CDD-3640-101-U3); see [checksums.txt](checksums.txt).
Every finding below therefore describes the reference pressing, not a variant or a damaged copy - including the `LHSOUND.ZIP` provenance question, now settled: Jokisch's freeware sound package genuinely shipped on the commercial disc.

## Structure

The HFS volume is the whole disc.
`MAC` and `PC` are sibling folders alongside shared `DOCS`, `PCDEMOS`, `ACRODOS`, and DOS/Windows installers at root.
There is no separate PC filesystem tree to merge - extracting the HFS volume once yields everything.

Mac and PC builds diverge for Sherlock, Seastalker, Wishbringer, Leather Goddesses, Planetfall, Arthur, Journey and Zork Zero.
Do not merge the two trees by filename; keep them as siblings.
The full per-title release table for both platforms is in [versions.md](versions.md).

## Zork Zero: how the changing border frames are built

The location-sensitive border frames (castle, outside, underground, plus the hint screen) are pictures 5-8, named `CASTLE-BORDER`, `OUTSIDE-BORDER`, `UNDERGROUND-BORDER` and `HINT-BORDER` in the leaked ZIL source.
The game draws whichever frame `SET-BORDER` picks as a single `<DISPLAY pic 1 1>` - there is no platform branching in that code path, and picture geometry is queried at runtime through `PICINF`, so each platform's picture library is free to cut the art differently behind the same picture numbers.

- Mac (`PIC.DATA`/`CPIC.DATA`, 483 images each): pictures 5-8 are full-screen frames (480x300 hi-res, 320x200 color), columns included; one draw paints everything. The Amiga art is reportedly built the same way.
- PC (`ZORK0.CG1`/`ZORK0.EG1`, 503 images each): the same numbers hold only the top banners (640 x 29-39), and the libraries carry twenty PC-only pictures, 484-504, that the leaked ZIL never references: eight column strips (60-86 wide x 161-171 tall - four left/right pairs matching the four frame themes), ten invisible 0x0 entries, and two 20x7 fragments. The IF Archive `.MG1` shows the same banner/column split.
- Both platforms use invisible pictures as a layout-data channel: entries such as 383, 417 and 422 have zero or hairline dimensions and exist so the game can read per-platform metrics through `PICINF` (picture 417 "measures" 0x127 on the PC but 0x186 on the Mac).

Where the PC columns get composited: in the r393 story file itself, confirmed by disassembly (routine at `0x1baf8` in `ZORK0.ZIP`).
It draws the border picture at (1,1) - which on the PC is just the banner - reads the banner's height and width back with `PICTURE_DATA`, selects the column pair for the current border (5 -> 497/498, 6 -> 501/502, 7 -> 499/500, 8 -> 503/504), then draws the left column at (1+height, 1) and the right column at (1+height, width-colwidth+1).
Crucially the code stays platform-agnostic: each column draw is guarded by a `PICTURE_DATA` existence check, so against a Mac-style library with full-frame borders and no pictures 497-504 the same code draws the frame and silently skips the columns.
The compiled `SET-BORDER` sits directly after it, matching the leaked source line for line; the leak (picture constants ending at 483, the Mac library's count) simply predates the r393 border rework.
Neither the leaked ZIL nor the shipped `ZORKZERO.EXE` (the generic 47,494-byte 6.71 interpreter) contains any of this - it is all r393 z-code.
The split also makes sense on 1989 PC hardware: on a region change, redrawing a 640x37 banner and two column strips is far cheaper in EGA planar memory than repainting a full 640x200 frame.

The invisible PC-only pictures are read via `PICTURE_DATA` as expected (486, 487 and 496 observed), confirming the layout-metrics channel.

The two 20x7 fragments 484/485 are resolved (2026-09-03): they are **border-themed covers for the compass rose's up/down buttons**.
The ZIL source draws `U-BOX` (479) or `D-BOX` (480) beside the compass when an up or down exit is available and otherwise blanks the button with `BOX-COVER` (481), at coordinates read from the invisible `U-BOX-LOC`/`D-BOX-LOC` pictures (482/483).
In r393's compiled compass-redraw routine the blanking became border-aware: the cover is chosen by the current border picture - castle (border 5) keeps the original 481, outside (6) draws 485, and everything else (underground, hints) draws 484 - because on the PC the area behind the buttons is banner art whose texture differs per border theme, so one cover no longer matched all three.
The r393 preload table is the source's `COMPASS-PICSET-TBL` with 484 and 485 appended, and in the CGA library the three covers are 21x8 against the 20x7 buttons, a one-pixel overpaint margin.
(The draw sites turned out to be plain constants after all - `txd` had been rendering the operands 0x1E4/0x1E5 as string references, which is why earlier searches missed them.)

Analyzed with `scripts/picdir.py` against this disc's picture libraries, `txd` from ztools 7.3.1 against this disc's `ZORK0.ZIP`, plus the ZIL source at <https://github.com/historicalsource/zorkzero> (`globals.zil` `SET-BORDER`/`INIT-STATUS-LINE`, `picdef.zil`).

## Findings that correct or extend the published catalogs

- **`LEATHER.SCR` is present** (1,408 bytes) in `PC/LEATHER/`, and `_LEATHER.COM` is 12,004 bytes, which is Infocom MS-DOS interpreter **3N** - the only build that loads a boss key screen. So the Leather Goddesses boss key works on this disc. Doherty's Infocom Fact Sheet notes the LTOI1 IBM packages dropped it, and is internally inconsistent about the filename (`LEATHER.DAT` in one section, `<GAMENAME>.SCR` in the interpreter table). The disc settles it: `.SCR`.
- **`PC/LURKING/DATA/LHSOUND.ZIP`** (589,733 bytes) is Stefan Jokisch's freeware sound package, shipped on a commercial Activision disc. Contents: fourteen `LURKINxx.SND` files matching Doherty's count of fourteen sounds, `UPDATELH.EXE` plus C source, and `LURKING.CNV` at 129,944 bytes - exactly the length Doherty gives for release 221.870918. The README is signed by Jokisch and mentions Frotz as unfinished, dating it before December 1995; internal file dates run January to August 1995. So a PC owner of this disc can convert the shipped r203 to r221 and play with sound on a Sound Blaster, contrary to the usual claim that Lurking Horror sound was Amiga-only.
Verified 2026-09-03: `LURKING.CNV` is an XOR patch (the algorithm is in the package's `UPDATELH.C`), and applying it to this disc's r203 produces r221.870918 byte-identical to the copy preserved in the leaked Infocom source repositories, with the patcher's checksums valid - the conversion genuinely works, end to end.
- **Seventeen games ship with populated `SAVE` directories**: Ballyhoo, Deadline, Enchanter, Infidel, Lurking, Moonmist, Planetfall, Sorcerer, Spellbreaker, Starcross, Stationfall, Suspect, Suspended, Witness, Zork I, Zork II, Zork III. Sizes 10.8-15.3 KB. `PC/LURKING/SAVE/LURKING.DAT` contains the serial `870506` (confirming it was made against the shipped r203), the strings `872325412` and `uhlersoth` - the login and password for the opening terminal puzzle, which were feelie-based copy protection - and an input buffer holding `save`. These are real saves. Their timestamps are all 22 June 1996, the same stamp as nearly every file on the disc, so the dates reflect mastering rather than when the games were played - confirmed by the [Zork Legacy Collection disc](../zork-legacy-1997-rtz-anthology/notes.md), which carries byte-identical Zork I-III saves dated 11 June 1996.
- **Zork Zero's PC graphics are incomplete.** `PC/ZORK0/` has `.CG1`, `.EG1`, `.ZIP` and the interpreter but no `.MG1` and no `.EG2`. Arthur and Journey have all four. This is the same omission Doherty documented for LTOI1's IBM packages, carried forward - and carried forward again: the 1997 Zork Legacy Collection disc ships the same four files, byte-identical, with the same two missing.
- **Mac and PC Zork Zero are different releases.** `MAC/ZORK ZERO/STORY.DATA` is r296.881019 - the first release - while `PC/ZORK0/ZORK0.ZIP` is r393.890714. Another instance of the Mac side shipping older masters (see the 1995 dates on Mac Zork I-III above).
- **Mac Sherlock ships its sound.** `MAC/SOUND/` holds thirteen `SDAT` files (S3-S17) plus four 32-byte `M` files dated February 1988. The Mac Sherlock is r26.880127, the sound build.
- **Two provenances of PC story file.** Games with a `DATA/` subfolder have files padded to round sizes (92160, 122880, 153600); the same files are duplicated in a shared `PC/DATA/` - a directory that resurfaces, byte-identical, inside the Windows installer archive on the [1997 Zork Legacy Collection disc](../zork-legacy-1997-rtz-anthology/notes.md). Games without one have the `.DAT` in the game folder at natural size **+1 byte**, matching Doherty's note about IBM data files padded with a trailing `$1a`. Examples: `LEATHER.DAT` 129,023 vs 129,022; `WISHBRIN.DAT` 128,905 vs 128,904; `TRINITY.DAT` 262,065 vs 262,064.
- **Every interpreter matches Doherty's size table**: 11394=3L, 11402=3M2, 12004=3N, 12640=4A, 12682=4E, 12688=4D, 33946=5J, 47442=6.68, 47494/47528=6.71.
- Mac Zork I, II, III and Beyond Zork are dated 3 April 1995, a year older than the 19 June 1996 stamp on every other Mac game.
- `PCDEMOS/PLANETFALL/planetfall.avi` (4.2 MB) is likely promotional footage for the cancelled *Planetfall: The Search for Floyd*.
- `VERYLOST/` on both sides holds aborted game proposals (Amnesia, Boston, Creation, LG2 ideas, Oz, Thriller, Trek, Truffles) and three issues of the internal *Infodope* newsletter. The Mac copy of `MISC/` has one file the PC copy lacks.

## Inside this disc's DATA.Z: the PC tree with its history intact

The root `DATA.Z` (10,587,923 bytes, an InstallShield 3 archive readable with `scripts/isz.py`) is what the Windows `SETUP.EXE` installs from: 215 members that are the entire `PC/` tree except `README.TXT`, byte-identical where compared (every story file, spot-checked saves) - with two exceptions that make the archive more interesting than the tree it copies.

**The archive preserves the timestamps the mastering destroyed.**
The disc stamps nearly every file 1996-06-22 (or 19 June on the Mac side); inside `DATA.Z` the members keep their working dates, a whole stratigraphy:

- The bulk of the PC set is mass-stamped 1995-05-31 12:00 - the assembly date of the PC file set, and the date the [Zork Legacy Collection disc](../zork-legacy-1997-rtz-anthology/notes.md) still shows on its loose copies of these files.
- The V6 games keep original dates that match their builds: `ARTHUR.ZIP` is dated 1989-07-14 (its serial is 890714) and `JOURNEY.ZIP` 1989-07-06 (serial 890706), the `.CG1` hi-res art is from July 1989, and the `.EG1`/`.EG2` EGA conversions from 22-27 October 1992, the Lost Treasures preparation window (matching the 1992-10-29 creation date on the Mac `ARTHUR` file).
- Leather Goddesses keeps 1986 dates on `_LEATHER.COM` (1986-07-30, the 3N interpreter) and `LEATHER.SCR` (1986-05-19, the boss-key screen).
- `JOURNEY.MG1` and `LHSOUND.ZIP` are both stamped 1996-06-13 22:56: the MCGA art and the Lurking Horror sound package were added together, late, nine days before mastering.
- **The seventeen save files were made in one 36-minute sitting**: 1996-06-11, Ballyhoo at 15:47 through Zork III at 16:23. Someone at Activision spent that afternoon opening seventeen games and saving, and the disc has carried the session ever since (the Legacy disc's loose saves show the same date; only the archive keeps the minutes).

**The Windows installer ships a suppressed draft of the Very Lost Treasures essay.**
`VERYLOST\ABOUT.TXT` inside the archive is 5,432 bytes, dated 1996-06-19 20:35 - a longer, earlier draft of the disc's 4,210-byte `PC/VERYLOST/ABOUT.TXT`, and the only member whose content differs from the tree.
The cut material describes content that is on neither the disc nor the archive: recovered **mail messages** from the old Infocom UNIX server ("thoughts on Activision's acquisition of Infocom... The politicking would have made many people proud"), and a set of 1996 Interactive Fiction Competition files (`SPAG.FAQ`, `CONTEST1.TXT`, `CONTEST2.TXT`, `INTRVIEW.TXT`, with a deadline of "Sept. 31, 1996").
So the Very Lost Treasures was planned to include the server's mail and the IF Competition documents, both were pulled, the essay was edited to match for the disc - and the unedited draft survived inside the installer archive, where every Windows installation of Masterpieces received it.
`DATA.Z` itself is dated 20 June on the disc, but `LEATHER\LEATHER.DAT` inside it is stamped 1996-06-20 21:45, so the archive was built on the evening of the 20th: after the draft, before the edit reached it.

## Open items for this disc

None.

Resolved 2026-09-03: this disc's `DATA.Z` enumerated; see the section above.

Resolved 2026-08-29: creation dates on extracted files.
`scripts/hfscopy.py` now restores them from the MacBinary header via `SetFile -d`.
The restored dates carry provenance: `MAC:SOUND:S3` was created 1988-02-08 (the original Sherlock sound build), and Mac `ARTHUR` (1992-10-29) and `ZORK I` (1991-10-28) carry Lost Treasures-era creation dates under their 1995/1996 modification stamps, consistent with Activision reusing the earlier masters.

Resolved 2026-08-29: full-disc image with Redump-comparable hashes.
`dd bs=2352 count=150515` against the raw whole-disc device produced a track that hashes identical to the Redump entry; see [checksums.txt](checksums.txt) and the method notes in [docs/imaging.md](../../docs/imaging.md).
