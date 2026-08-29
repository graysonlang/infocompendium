# Classic Text Adventure Masterpieces of Infocom (1996) - findings

Established against a physical pressing read on an Apple Silicon Mac with a Pioneer BD-RW BDR-XS07U.
The general method and its pitfalls are in [docs/knowledge-transfer.md](../../docs/knowledge-transfer.md); this file holds only what is specific to this disc.

## Identity

Hybrid CD: one Mode 1 data track carrying an ISO 9660 catalogue (260 KB slice, pointer structure only) and an HFS catalogue (308 MB volume holding everything).
Volume `Masterpieces`, created 18 June 1996, modified 22 June 1996.
`drutil status` reports 150515 blocks; 150515 x 2048 = 308,254,720 bytes of user data is the number to verify any image against.
879 catalogue entries: 113 directories, 766 files.
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

## Findings that correct or extend the published catalogues

- **`LEATHER.SCR` is present** (1,408 bytes) in `PC/LEATHER/`, and `_LEATHER.COM` is 12,004 bytes, which is Infocom MS-DOS interpreter **3N** - the only build that loads a boss key screen. So the Leather Goddesses boss key works on this disc. Doherty's Infocom Fact Sheet notes the LTOI1 IBM packages dropped it, and is internally inconsistent about the filename (`LEATHER.DAT` in one section, `<GAMENAME>.SCR` in the interpreter table). The disc settles it: `.SCR`.
- **`PC/LURKING/DATA/LHSOUND.ZIP`** (589,733 bytes) is Stefan Jokisch's freeware sound package, shipped on a commercial Activision disc. Contents: fourteen `LURKINxx.SND` files matching Doherty's count of fourteen sounds, `UPDATELH.EXE` plus C source, and `LURKING.CNV` at 129,944 bytes - exactly the length Doherty gives for release 221.870918. The README is signed by Jokisch and mentions Frotz as unfinished, dating it before December 1995; internal file dates run January to August 1995. So a PC owner of this disc can convert the shipped r203 to r221 and play with sound on a Sound Blaster, contrary to the usual claim that Lurking Horror sound was Amiga-only.
- **Seventeen games ship with populated `SAVE` directories**: Ballyhoo, Deadline, Enchanter, Infidel, Lurking, Moonmist, Planetfall, Sorcerer, Spellbreaker, Starcross, Stationfall, Suspect, Suspended, Witness, Zork I, Zork II, Zork III. Sizes 10.8-15.3 KB. `PC/LURKING/SAVE/LURKING.DAT` contains the serial `870506` (confirming it was made against the shipped r203), the strings `872325412` and `uhlersoth` - the login and password for the opening terminal puzzle, which were feelie-based copy protection - and an input buffer holding `save`. These are real saves. Their timestamps are all 22 June 1996, the same stamp as nearly every file on the disc, so the dates reflect mastering rather than when the games were played.
- **Zork Zero's PC graphics are incomplete.** `PC/ZORK0/` has `.CG1`, `.EG1`, `.ZIP` and the interpreter but no `.MG1` and no `.EG2`. Arthur and Journey have all four. This is the same omission Doherty documented for LTOI1's IBM packages, carried forward.
- **Mac Sherlock ships its sound.** `MAC/SOUND/` holds thirteen `SDAT` files (S3-S17) plus four 32-byte `M` files dated February 1988. The Mac Sherlock is r26.880127, the sound build.
- **Two provenances of PC story file.** Games with a `DATA/` subfolder have files padded to round sizes (92160, 122880, 153600); the same files are duplicated in a shared `PC/DATA/`. Games without one have the `.DAT` in the game folder at natural size **+1 byte**, matching Doherty's note about IBM data files padded with a trailing `$1a`. Examples: `LEATHER.DAT` 129,023 vs 129,022; `WISHBRIN.DAT` 128,905 vs 128,904; `TRINITY.DAT` 262,065 vs 262,064.
- **Every interpreter matches Doherty's size table**: 11394=3L, 11402=3M2, 12004=3N, 12640=4A, 12682=4E, 12688=4D, 33946=5J, 47442=6.68, 47494/47528=6.71.
- Mac Zork I, II, III and Beyond Zork are dated 3 April 1995, a year older than the 19 June 1996 stamp on every other Mac game.
- `PCDEMOS/PLANETFALL/planetfall.avi` (4.2 MB) is likely promotional footage for the cancelled *Planetfall: The Search for Floyd*.
- `VERYLOST/` on both sides holds aborted game proposals (Amnesia, Boston, Creation, LG2 ideas, Oz, Thriller, Trek, Truffles) and three issues of the internal *Infodope* newsletter. The Mac copy of `MISC/` has one file the PC copy lacks.

## Open items for this disc

- `SetFile -d` pass to restore creation dates on extracted files.

Resolved 2026-08-29: full-disc image with Redump-comparable hashes.
`dd bs=2352 count=150515` against the raw whole-disc device produced a track that hashes identical to the Redump entry; see [checksums.txt](checksums.txt) and the method notes in [docs/knowledge-transfer.md](../../docs/knowledge-transfer.md).
