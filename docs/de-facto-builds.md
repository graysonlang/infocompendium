# The de-facto builds

Every disc in this catalog copies rather than remasters: one set of story-file builds was fixed in place by the 1992 Lost Treasures CDs, inherited byte-for-byte by every later compilation, and adopted by the interactive-fiction community as each game's version of record - the builds that interpreter authors test against, that reference materials describe, and that a player almost certainly has if they have the game at all.
This page names that de-facto build for each of the 35 games and lists which cataloged collections carry it, verified by hash throughout; each collection's `versions.md` holds the measurements, the platform variants, and the later masters that never shipped.

The status is descriptive, not editorial: these are not always the last builds Infocom made (the leaked repositories hold later masters for a third of the catalog), and not always one build per title (five games shipped platform splits that persist to this day, and the five Solid Gold editions appear as their own rows, since the community treats them as separate editions rather than replacements).

Columns: **Box** = original boxed retail media, checked where this catalog holds it (the 1989 Zork Zero floppies) and "doc" where a documented boxed release is the build's only known carrier; **MP** = Masterpieces (1996); **LTOI1**/**LTOI2** = the 1992 Lost Treasures CDs; **Leak** = the historicalsource repositories (2019), where "hist" marks a build present only in a repository's git history.
A hybrid disc carries two platform trees and so can hold two builds of one game: Masterpieces checks both Planetfall rows (plain on its PC side, Solid Gold on its Mac side) and both Leather Goddesses rows, and LTOI1 checks both Hitchhiker's rows - the `(PC)`/`(Mac)` marker on a build names the side that carries it.
The Zork Anthology (1994) and the Zork Legacy Collection (1997) are not columns because they never carry a build these columns lack: the anthology discs redistribute the Zork-family set, and the Legacy Collection's `DATA.Z` repeats Masterpieces' shared story files.

| Title | De-facto build | Box | MP | LTOI1 | LTOI2 | Leak |
| --- | --- | --- | --- | --- | --- | --- |
| A Mind Forever Voyaging | v4 r77.850814 |  | ✓ |  | ✓ | ✓ |
| Arthur | v6 r74.890714 (PC) |  | ✓ |  | ✓ |  |
| Ballyhoo | v3 r97.851218 |  | ✓ | ✓ |  | ✓ |
| Beyond Zork | v5 r57.871221 |  | ✓ | ✓ |  | hist |
| Border Zone | v5 r9.871008 |  | ✓ |  | ✓ | ✓ |
| Bureaucracy | v4 r116.870602 |  | ✓ |  | ✓ |  |
| Cutthroats | v3 r23.840809 |  | ✓ |  | ✓ | hist |
| Deadline | v3 r27.831005 |  | ✓ | ✓ |  | ✓ |
| Enchanter | v3 r29.860820 |  | ✓ | ✓ |  | ✓ |
| The Hitchhiker's Guide to the Galaxy | v3 r59.851108 (Mac) |  | | ✓ |  |  |
| The Hitchhiker's Guide to the Galaxy (Solid Gold) | v5 r31.871119 (PC) |  |  | ✓ |  | ✓ |
| Hollywood Hijinx | v3 r37.861215 |  | ✓ |  | ✓ | ✓ |
| Infidel | v3 r22.830916 |  | ✓ | ✓ |  | ✓ |
| Journey | v6 r83.890706 (PC) |  | ✓ |  | ✓ | ✓ |
| Leather Goddesses of Phobos | v3 r59.860730 (PC) |  | ✓ |  |  | ✓ |
| Leather Goddesses of Phobos (Solid Gold) | v5 r4.880405 (Mac) |  | ✓ |  |  | ✓ |
| The Lurking Horror | v3 r203.870506 |  | ✓† | ✓ |  | hist |
| Moonmist | v3 r9.861022 |  | ✓ | ✓ |  | hist |
| Nord and Bert | v4 r19.870722 |  | ✓ |  | ✓ | hist |
| Planetfall | v3 r37.851003 (PC) |  | ✓ | ✓ |  |  |
| Planetfall (Solid Gold) | v5 r10.880531 (Mac) |  | ✓ | ✓ |  | ✓ |
| Plundered Hearts | v3 r26.870730 |  | ✓ |  | ✓ | ✓ |
| Seastalker | v3 r16.850603 (PC) |  | ✓ |  | ✓ | ✓ |
| Sherlock | v5 r21.871214 (PC) |  | ✓ |  | ✓ |  |
| Shogun | v6 r322.890706 (PC) |  |  |  | ✓ | ✓ |
| Sorcerer | v3 r15.851108 |  | ✓ | ✓ |  |  |
| Spellbreaker | v3 r87.860904 |  | ✓ | ✓ |  | ✓ |
| Starcross | v3 r17.821021 |  | ✓ | ✓ |  |  |
| Stationfall | v3 r107.870430 |  | ✓ | ✓ |  | ✓ |
| Suspect | v3 r14.841005 |  | ✓ | ✓ |  | hist |
| Suspended | v3 r8.840521 |  | ✓ | ✓ |  | ✓ |
| Trinity | v4 r12.860926 |  | ✓ |  | ✓ | hist |
| The Witness | v3 r22.840924 |  | ✓ | ✓ |  | ✓ |
| Wishbringer | v3 r69.850920 (PC) |  | ✓ |  | ✓ | ✓ |
| Wishbringer (Solid Gold) | v5 r23.880706 | doc |  |  |  |  |
| Zork I | v3 r88.840726 |  | ✓ | ✓ |  | hist |
| Zork I (Solid Gold) | v5 r52.871125 |  |  |  |  | ✓ |
| Zork II | v3 r48.840904 |  | ✓ | ✓ |  | hist |
| Zork III | v3 r17.840727 |  | ✓ | ✓ |  | hist |
| Zork Zero | v6 r393.890714 (PC) | ✓ | ✓\* | ✓\* |  |  |

\* The CD copies of Zork Zero are complete as a game but lack the MCGA graphics file (`ZORK0.MG1`) - only the retail floppies (and the IF Archive's separately hosted copy) carry it; see [media assets](media-assets.md).

† Masterpieces' PC copy also carries the sound upgrade in the game's `DATA` folder: `LHSOUND.ZIP`, with the fourteen samples and the patch that converts r203 into the r221 sound build; see [media assets](media-assets.md).

Reading the table:

- **The de-facto set is the 1992 file set.** Twenty-eight titles have a single standard build, and in every measured case it is byte-identical from its first CD appearance through 1997 - and for Zork Zero, back to the 1989 retail floppies themselves.
- **Five platform splits persist inside the de-facto set** (Arthur, Journey, Seastalker, Sherlock, Zork Zero): the PC build is the one that circulates in modern interpreters, the Mac build the one Mac-era players had. Where a split exists this table lists the PC build as the de-facto one, since that is what the compilations' installers, and everything downstream of them, deliver.
- **Solid Gold never supplanted the originals.** The plain builds remained the standard; the discs used the Solid Golds only as one-platform substitutes (Hitchhiker's PC side, Planetfall's and Leather Goddesses' Mac sides), and Zork I's never shipped on any cataloged disc. A parallel edition line, not a succession.
- **Wishbringer Solid Gold is the row with nothing but a `doc` in the Box column**: a real 1988 retail release (Doherty documents it as v5 r23.880706, 164,712 bytes, one of the five Solid Gold packagings) that no collection cataloged here carries - no disc includes it, and the leak holds only its ZIL source, plus what is likely the edition in development: the r32933 EZIP experiment in the `wishbringer` repository, serial-dated one month before the Solid Gold's. The build presumably survives on original 1988 diskettes - and that is the point of the empty row: the compilations transferred every other edition's canonicity from box to CD, and this is the one shipped edition the transfer skipped, so its de-facto carrier is still the box itself.
- **De facto rarely means final.** The leaked repositories hold later masters for eleven titles - Zork I r119 and Bureaucracy r160 most dramatically - none of which ever reached players. The community standard is wherever Activision's 1992 masters happened to stop.
