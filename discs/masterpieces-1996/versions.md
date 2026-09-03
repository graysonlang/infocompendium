# Classic Text Adventure Masterpieces of Infocom (1996) - title versions

Release and serial numbers read from the z-code headers of every story file on the disc, both platforms.
On the Mac side the story is the data fork of each double-clickable game application (the interpreter lives in the resource fork); Arthur, Journey and Zork Zero instead ship a separate `STORY.DATA` beside their picture libraries.
On the PC side the story is the game's `.DAT` (or `.ZIP` for the V6 games), whether in the shared `PC/DATA/` or the game's own folder.
"Same build" compares the z-code itself, up to each file's header-declared length, so platform padding is ignored.
Where the two platforms ship different Z-machine versions, the cell reads Mac / PC.

| Title | Z-machine | Mac release | PC release | Same build |
| --- | --- | --- | --- | --- |
| A Mind Forever Voyaging | v4 | r77.850814 | r77.850814 | yes |
| Arthur: The Quest for Excalibur | v6 | r54.890606 | r74.890714 | **no** |
| Ballyhoo | v3 | r97.851218 | r97.851218 | yes |
| Beyond Zork | v5 | r57.871221 | r57.871221 | yes |
| Border Zone | v5 | r9.871008 | r9.871008 | yes |
| Bureaucracy | v4 | r116.870602 | r116.870602 | yes |
| Cutthroats | v3 | r23.840809 | r23.840809 | yes |
| Deadline | v3 | r27.831005 | r27.831005 | yes |
| Enchanter | v3 | r29.860820 | r29.860820 | yes |
| Hollywood Hijinx | v3 | r37.861215 | r37.861215 | yes |
| Infidel | v3 | r22.830916 | r22.830916 | yes |
| Journey | v6 | r26.890316 | r83.890706 | **no** |
| Leather Goddesses of Phobos | v5 / v3 | r4.880405 | r59.860730 | **no** |
| The Lurking Horror | v3 | r203.870506 | r203.870506 | yes |
| Moonmist | v3 | r9.861022 | r9.861022 | yes |
| Nord and Bert Couldn't Make Head or Tail of It | v4 | r19.870722 | r19.870722 | yes |
| Planetfall | v5 / v3 | r10.880531 | r37.851003 | **no** |
| Plundered Hearts | v3 | r26.870730 | r26.870730 | yes |
| Seastalker | v3 | r15.840522 | r16.850603 | **no** |
| Sherlock: The Riddle of the Crown Jewels | v5 | r26.880127 | r21.871214 | **no** |
| Sorcerer | v3 | r15.851108 | r15.851108 | yes |
| Spellbreaker | v3 | r87.860904 | r87.860904 | yes |
| Starcross | v3 | r17.821021 | r17.821021 | yes |
| Stationfall | v3 | r107.870430 | r107.870430 | yes |
| Suspect | v3 | r14.841005 | r14.841005 | yes |
| Suspended | v3 | r8.840521 | r8.840521 | yes |
| Trinity | v4 | r12.860926 | r12.860926 | yes |
| The Witness | v3 | r22.840924 | r22.840924 | yes |
| Wishbringer | v3 | r68.850501 | r69.850920 | **no** |
| Zork I | v3 | r88.840726 | r88.840726 | yes |
| Zork II | v3 | r48.840904 | r48.840904 | yes |
| Zork III | v3 | r17.840727 | r17.840727 | yes |
| Zork Zero | v6 | r296.881019 | r393.890714 | **no** |

Thirty-three titles; The Hitchhiker's Guide to the Galaxy and Shogun are the catalog's absentees.
Twenty-five ship as the identical build on both platforms; the eight splits run in both directions:

- **Mac newer.** Planetfall and Leather Goddesses get their Solid Gold v5 builds on the Mac only, while the PC keeps the plain v3 releases - Planetfall's split carried over from [the 1992 LTOI CD](../lost-treasures-1-1992/versions.md); Leather Goddesses sat out LTOI volume 1, so its split has no 1992 precedent to compare. Mac Sherlock is r26.880127, the sound build that the shipped `MAC/SOUND/` files belong to; PC Sherlock is the older, soundless r21.871214.
- **Mac older.** The V6 games all pair an older Mac master with a newer PC one: Arthur r54 vs r74, Journey r26 vs r83, and Zork Zero r296 vs r393 (the split inherited from LTOI1). Seastalker and Wishbringer likewise keep first-release Mac builds (r15.840522, r68.850501) against later PC ones (r16.850603, r69.850920).

One spelling quirk preserved from the pressing: the Mac application is cataloged as `LEATHER GODESSES`, one d short.
