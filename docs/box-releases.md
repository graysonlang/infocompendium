# Releases on original media

What the boxes actually shipped, one section per title.

This is a different question from [the de-facto builds](de-facto-builds.md), which names the one build the community treats as each game's version of record and says which compilation to get it from.
That page is for deciding where to play a game.
This one is a record of what has been read first hand off original diskettes: which build each platform's box carried, verified against the disc rather than against a catalog.
The two disagree more often than you would expect, which is the point - several boxes shipped builds that reached no compilation and survive in no leaked repository.

Every build below was read with a Greaseweazle from the physical diskette, extracted, and checked against its own Z-machine checksum; the checksum column is the declared value, confirmed by recomputing it over the story body.
Where a build is byte-identical to a copy from another source, that is stated, because agreement between independent witnesses is the strongest evidence available that a reconstruction is right.
Method is in [floppy-imaging.md](floppy-imaging.md).

**Absent from every compilation and from the leaked repositories:** Wishbringer r68.850501, Enchanter r10.830810, Sorcerer r4.840131, Beyond Zork r49.870917, Trinity r11.860509, Enchanter r16.831118 and Bureaucracy r86.870212.
Seven builds, on seven boxes, surviving nowhere else.

## A Mind Forever Voyaging

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Atari ST | 3.5" 360K SS | v4 r77.850814 | 262,016 | 5031 | The de-facto build. Byte-identical to the leak's compiled r77 and to LTOI2's Mac copy. |

## Beyond Zork

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Apple II | 5.25" 140K flippy | v5 r49.870917 | 261,900 | 24D6 | **On no compilation and in no repository.** Four releases earlier than the de-facto r57. Story spans both surfaces, the reverse in the 18-sector XZIP format. |
| PC | 5.25" 360K DS | v5 r57.871221 | 261,388 | C5AD | The de-facto build. |

## Border Zone

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Apple II | 5.25" 140K flippy | v5 r9.871008 | 178,372 | 2B37 | The de-facto build. Story spans both surfaces; matches the leak's build but for three Apple II header bytes. |

## Bureaucracy

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| PC | 5.25" 360K DS | v4 r86.870212 | 243,144 | E024 | **On no compilation.** Doherty's first release, thirty builds before the de-facto r116.870602. |

## Deadline

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| PC | 5.25" 180K SS | v3 r27.831005 | 108,454 | 54FC | The de-facto build. |

## Enchanter

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Atari 8-bit | 5.25" 90K | v3 r10.830810 | 109,126 | 6DB4 | **On no compilation and in no repository.** The first Enchanter release, five builds before the de-facto r29.860820. Story spans both surfaces; the jacket was punched for a second index hole to reach the reverse. |
| PC | 5.25" 180K SS | v3 r16.831118 | 109,234 | 58F5 | **On no compilation.** Thirteen builds before the de-facto. |

## The Hitchhiker's Guide to the Galaxy

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Apple II | 5.25" 140K | v3 r56.841221 | 113,444 | 9235 | A distinct Apple II build. |

## Leather Goddesses of Phobos

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| PC | 5.25" 180K SS | v3 r59.860730 | 129,022 | D070 | The de-facto build. |
| Atari ST | 3.5" 360K SS | v3 r59.860730 | 129,022 | D070 | **Byte-identical to the PC copy.** |
| Atari 8-bit | 5.25" 90K flippy | v3 r59.860730 | 129,022 | D070 | Reconstructed from both surfaces. Differs from the PC and ST copies in four places only: three header bytes at 0x01/0x04/0x05, below the checksummed region, plus one of trailing length. An independent platform agreeing to within the known header bytes is what confirms that reconstruction. |

## Leather Goddesses of Phobos (Solid Gold)

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Apple II | 5.25" 140K flippy | v5 r4.880405 | 159,928 | EFE4 | The Solid Gold build, which Masterpieces carries only on its Mac side. Story spans both surfaces. |

## The Lurking Horror

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| PC | 5.25" 360K DS | v3 r203.870506 | 128,986 | FB9C | The de-facto build. The box also bundles a Cornerstone demo. |

## Planetfall

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| TI-99/4A | 5.25" 90K flippy | r37.851003 | - | - | Imaged complete on both surfaces, volume `PLANETFALL`. The story has **not** been extracted: ZCut does not support TI-99, so the on-disk layout has to be worked out by hand. The last 8-bit gap. |

## Sorcerer

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Atari 8-bit | 5.25" 90K | v3 r4.840131 | 109,734 | 2E36 | **On no compilation and in no repository.** The first *released* Sorcerer - Doherty lists three earlier builds, all unreleased - eleven before the de-facto r15.851108. |

## Spellbreaker

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Commodore 64 | 5.25" 170K | v3 r63.850916 | 128,480 | 6C0A | Doherty's first release, one build before the de-facto r87.860904. Absent from every disc, but **byte-identical to the leak's compiled r63** - the first direct confirmation here that a "Revision NN (Original Source)" commit holds the build that actually shipped. |

## Stationfall

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| PC | 5.25" 360K DS | v3 r107.870430 | 128,934 | 2871 | The de-facto build. |
| Amiga | 3.5" 880K DS | v3 r107.870430 | 128,934 | 2871 | **Byte-identical to the PC copy and to the leak's compiled build.** |

## Trinity

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Atari ST | 3.5" 360K SS | v4 r11.860509 | 262,016 | FAAE | **On no compilation and in no repository.** Earlier than the r12.860926 the CDs and the leak's "Revision 12" commit carry. The disc also preserved `LONGWATE.SAV`, a period saved game left by an earlier player - the first save recovered from original media here. |

## Wishbringer

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Apple II | 5.25" 140K | v3 r68.850501 | 128,952 | 81A5 | **On no compilation and in no repository.** The first Wishbringer release, predating the r69.850920 the compilations standardized on. |

## Wishbringer (Solid Gold)

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| PC | 5.25" 360K DS | v5 r23.880706 | 164,712 | 4222 | The one shipped edition no compilation carried; the leak holds only its source. This box is the build's only known carrier. Built-in hints present. |

## Zork I, II and III

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| Apple II | 5.25" 140K flippy | Zork I v3 r88.840726 | 84,876 | A129 | Side 1 of the Trilogy's first disc. De-facto build; a byte-identical prefix of the LTOI1 copy. |
| Apple II | 5.25" 140K flippy | Zork II v3 r48.840904 | 89,912 | D899 | Side 2 of that same disc. Cross-checked against a separate period backup copy, byte-identical across all 559 of its readable sectors. |
| Apple II | 5.25" 140K | Zork III v3 r17.840727 | 82,714 | 2E7A | A second, non-flippy disc in the same package. |

## Zork Zero

| Platform | Media | Build | Bytes | Checksum | Notes |
| --- | --- | --- | --- | --- | --- |
| PC | 3.5" 720K x2, 5.25" 360K x3 | v6 r393.890714 | 299,968 | 791C | The de-facto build, from the dual-media retail box. The two media carry different graphics renditions: MCGA on the 3.5" set, EGA on the 5.25", CGA on both. |
