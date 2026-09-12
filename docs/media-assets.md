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

Across *renditions*, though, nothing is interchangeable: the libraries are sibling compositions, not conversions of one another.
Every title's picture count differs per rendition (Arthur's four libraries hold 168, 169, 170 and 171 images; Shogun's Mac pair hold 48 to the PC's 50), the drawn geometry differs with the display standard, and each library pairs with its own platform's story release - all four titles ship different Mac and PC story builds.

What the gaps mean:

- **Zork Zero's `.MG1` is the one genuinely missing file** - absent from every disc here, though the complete set is only three files (its EGA never needed an `.EG2`). LTOI1 dropped it in 1992, and every later disc inherited the gap.
  - The IF Archive's `zorkzero.mg1` is the genuine Infocom file: byte-identical to the copy on the retail 3.5" diskettes - shipped retail, dropped by LTOI1, restored to the archive from a retail copy in 1994. The full provenance trail, physical media included, is in [the floppy entry](../discs/zork-zero-1989-dos/notes.md).
  - It cannot be a conversion: its 503 images include the twenty r393-only pictures that exist in no Amiga or Mac rendition. (The archive labels its one real conversion as such: Jokisch's `beyondzo.mg1`.)
  - It is the extreme case of the rendition split above: the Mac library is the 483-image r296-era layout whose borders are full 320x200 frames, the MG1 the 503-image r393 banner-plus-columns cut.
- **Shogun's three files are its complete PC set** (its fifty EGA pictures fit one file), and its graphics survive only on LTOI2 among the discs - Masterpieces dropped the title. The leaked `shogun` repository carries Mac and Apple II picture files (`a5.mac.1`, `a5.bwmac.1`, `a5.apple.1`) at sizes close to but not equal to LTOI2's, consistent with its later r322-era snapshot against the disc's r292-era Mac release.
- **Arthur's EGA files exist only because a CD wanted them**: the original floppy release shipped `MG1`, `CG1` and the `FILECVT.EXE` converter instead of EGA art; LTOI2's mastering pregenerated `EG1`/`EG2` in October 1992 and every later appearance inherits them. See [the LTOI2 notes](../discs/lost-treasures-2-1992/notes.md).
- The leaked repositories otherwise carry no PC graphics libraries at all - for Zork Zero only the picture-manifest sources (`zork0.zpic`, a text file of picture names; `zork0.pic`, its offset table), which is consistent with the art being drawn on the Amiga and converted elsewhere.

## Sound

| Title | Medium | LTOI2 (1992) | Masterpieces (1996) | Source leak (2019) |
| --- | --- | --- | --- | --- |
| Sherlock | Mac `SOUND/` folder | 13 `S` + 4 `M` files | 13 `S` + 4 `M` files (byte-identical) | raw sample sources and the number-to-name map |
| The Lurking Horror | PC, Sound Blaster | - | `LHSOUND.ZIP` (14 `.SND` files + the XOR patch to r221) | the r221 story file, no sounds |

In both games the sampled sounds start at number 3, because the Z-machine reserves 1 and 2 for its two interpreter-generated tones - the high and low bleep, which need no sample file and work on every interpreter - and both games' sources name them the same way: `S-BEEP` and `S-BOOP`.

Sherlock's sound numbers decode from the leaked repository twice over: the `s3.nam`-`s17.nam` files map each number to its sample, and `sounds.zil` carries Infocom's own constant names and descriptions:

| # | ZIL name | Sound | Shipped on the Mac discs as |
| --- | --- | --- | --- |
| 3 | `S-ARMOR` | armor squeaking - worn, removed, moving | `S3`, full rate |
| 4 | `S-BADVIOL` | Watson playing violin | `S4`, full rate |
| 5 | `S-BARK` | dog barking | `S5`, full rate |
| 6 | `S-BOATING` | background water sounds, in the boat (looping) | `S6`, full rate |
| 7 | `S-CLOCK` | Big Ben striking close up, long ring | `S7`, subsampled |
| 8 | `S-CROWD` | crowd noises (looping) | `S8`, full rate, plus the `M8` parameter record |
| 9 | `S-FANFARE` | trumpets for the ending | `S9`, full rate |
| 10 | `S-GROWL` | dog growling | `S10`, subsampled |
| 11 | `S-HEART1` | slow heartbeat | `M11` - replays `S12` slower |
| 12 | `S-HEART2` | medium heartbeat | `S12`, subsampled |
| 13 | `S-HEART3` | fast heartbeat | `M13` - replays `S12` faster |
| 14 | `S-HORSE` | sounds of the cab moving | `S14`, subsampled, plus the `M14` parameter record |
| 15 | `S-VIOLIN` | Holmes playing violin | `S15`, full rate |
| 16 | `S-SNORE` | snoring in the Diogenes Club (looping) | `S16`, full rate |
| 17 | `S-FARBEN` | Big Ben at a distance, short ring | `S17`, full rate |
| 18 | `S-WHISTLE` | whistle for calling cabs | commented out in the source; never shipped anywhere |

The `S` files are type `SDAT`, sound in the data fork: a 10-byte header, then unsigned 8-bit PCM.
The four 32-byte `M` files are playback-parameter records, each ending in the ASCII name of the `S` file it plays - which is how sounds 11 and 13 exist without samples of their own: the one heart recording replayed at different rates.

The Lurking Horror's sounds decode from the leaked repository's `sounds.txt` - Infocom's own internal sound list, which records that two samples were "cut for reasons of space", which is why the game has fourteen sounds and not sixteen.
Every documented size matches the corresponding `LURKINxx.SND` in Masterpieces' `LHSOUND.ZIP` (Jokisch's 1995 conversions of the Amiga samples):

| # | ZIL name | Sound | Shipped as |
| --- | --- | --- | --- |
| 3 | `S-BLOOD` | axe hitting the maintenance man | `LURKIN03.SND`, 49,766 bytes |
| 4 | `S-ATTACK` | rats attacking (looping) | `LURKIN04.SND`, 20,530 |
| 5 | `S-SQUEAL` | single rat | cut for space; never shipped anywhere |
| 6 | `S-HATCH` | rusty hatch in the tomb opening | `LURKIN06.SND`, 46,010 |
| 7 | `S-ELCRSH` | elevator pulling the wall out | `LURKIN07.SND`, 60,000 |
| 8 | `S-CRACK` | crack of stone | `LURKIN08.SND`, 7,738 |
| 9 | `S-GHIDRA` | frob flapping away | `LURKIN09.SND`, 58,024 |
| 10 | `S-DRONE` | drone of frob worshippers in the dream (looping) | `LURKIN10.SND`, 33,290 |
| 11 | `S-SPARKY` | electrical zap of the high-voltage line in water | `LURKIN11.SND`, 40,010 |
| 12 | `S-DIE` | flier after the stone is thrown at it | `LURKIN12.SND`, 44,330 |
| 13 | `S-PSYCHO` | demon in the alchemy lab getting the professor (looping) | `LURKIN13.SND`, 56,586 |
| 14 | `S-STORMY` | storm (looping) | cut for space; never shipped anywhere |
| 15 | `S-VOICE` | zombie urchins chanting (looping) | `LURKIN15.SND`, 51,610 |
| 16 | `S-CRETIN` | frob frying on the high voltage (looping) | `LURKIN16.SND`, 25,050 |
| 17 | `S-ZOMBIE` | frob noises in the inner lair (looping) | `LURKIN17.SND`, 39,258 |
| 18 | `S-MONSTR` | things in the pit in the altar area (looping) | `LURKIN18.SND`, 50,010 |
Measured against the leaked repository's sources (2026-09-12): the disc samples are the same recordings converted from signed to unsigned 8-bit PCM - 99.4-99.5% byte-identical under a sign-bit flip, the remainder scattered single bytes at near-silence, a different processing generation of the same masters.
The Lurking Horror's sound was native to the Amiga; no cataloged disc carries those samples, and the Masterpieces package is Stefan Jokisch's 1995 freeware conversion kit, not Infocom's - see [the Masterpieces notes](../discs/masterpieces-1996/notes.md) for its verification.
