# The community-sanctioned builds

Every disc in this catalog copies rather than remasters: one set of story-file builds was fixed in place by the 1992 Lost Treasures CDs, inherited byte-for-byte by every later compilation, and adopted by the interactive-fiction community as each game's version of record - the builds that interpreter authors test against, that reference materials describe, and that a player almost certainly has if they have the game at all.
This page names that community-sanctioned build for each of the 35 games and lists which cataloged collections carry it, verified by hash throughout (see each collection's `versions.md` for the measurements).

The sanction is de facto, not editorial: these are not always the last builds Infocom made (the leaked repositories hold later masters for a third of the catalog), and not always one build per title (five games shipped platform splits that persist to this day, and the community treats the Solid Gold editions and the r221 Lurking Horror sound build as sanctioned variants alongside the standard builds).

Collections: **FL89** = the 1989 Zork Zero retail floppies; **LTOI1**/**LTOI2** = the 1992 Lost Treasures CDs; **ZA** = the Zork Anthology (1994, inside its installer archive); **MP** = Masterpieces (1996); **ZLC** = the Zork Legacy Collection (1997, loose and/or inside `DATA.Z`); **leak** = the historicalsource repositories (2019), with "hist" marking builds only in their git history.

| Title | Sanctioned build | Carried by | Variants and later masters |
| --- | --- | --- | --- |
| A Mind Forever Voyaging | v4 r77.850814 | LTOI2, MP, leak | - |
| Arthur | v6 r74.890714 (PC) | LTOI2, MP | Mac r54.890606 (LTOI2, MP); leak has source only |
| Ballyhoo | v3 r97.851218 | LTOI1, MP, ZLC, leak | leak: unreleased r99.861014 |
| Beyond Zork | v5 r57.871221 | LTOI1, ZA, MP, ZLC, leak (hist) | leak: alpha, beta, unreleased r60.880610 |
| Border Zone | v5 r9.871008 | LTOI2, MP, leak | - |
| Bureaucracy | v4 r116.870602 | LTOI2, MP | leak: later r160.880521 |
| Cutthroats | v3 r23.840809 | LTOI2, MP, leak (hist) | leak: later r25.840917 |
| Deadline | v3 r27.831005 | LTOI1, MP, leak | leak: later r28.850129 |
| Enchanter | v3 r29.860820 | LTOI1, MP, leak | leak (hist): earlier r24.851118 |
| The Hitchhiker's Guide to the Galaxy | v3 r59.851108 (Mac) | LTOI1 only | PC got Solid Gold v5 r31.871119 instead (LTOI1, leak); leak: later plain r60.861002 |
| Hollywood Hijinx | v3 r37.861215 | LTOI2, MP, leak | - |
| Infidel | v3 r22.830916 | LTOI1, MP, leak | - |
| Journey | v6 r83.890706 (PC) | LTOI2, MP, leak | Mac r26.890316 (LTOI2, MP); leak: r54.890526 beta |
| Leather Goddesses of Phobos | v3 r59.860730 (PC) | MP, leak | Mac got Solid Gold v5 r4.880405 (MP, leak) |
| The Lurking Horror | v3 r203.870506 | LTOI1, MP, leak (hist) | r221.870918 sound build via MP's converter kit; leak carries it whole |
| Moonmist | v3 r9.861022 | LTOI1, MP, leak (hist) | leak: later r13.880501 |
| Nord and Bert | v4 r19.870722 | LTOI2, MP, leak (hist) | leak: later r20.870722 |
| Planetfall | v3 r37.851003 (PC) | LTOI1, MP, ZLC | Mac got Solid Gold v5 r10.880531 (LTOI1, MP, leak); leak: later plain r39.880501 |
| Plundered Hearts | v3 r26.870730 | LTOI2, MP, leak | - |
| Seastalker | v3 r16.850603 (PC) | LTOI2, MP, leak | Mac r15.840522 (LTOI2, MP, leak hist); leak: five more platform builds |
| Sherlock | v5 r21.871214 (PC) | LTOI2, MP | Mac got the newer r26.880127 sound build (LTOI2, MP, leak) |
| Shogun | v6 r322.890706 (PC) | LTOI2, leak | Mac r292.890314 exists only on LTOI2 |
| Sorcerer | v3 r15.851108 | LTOI1, MP | leak (hist): earlier r13.851021; leak: later r18.860904 |
| Spellbreaker | v3 r87.860904 | LTOI1, MP, leak | leak (hist): first release r63.850916 |
| Starcross | v3 r17.821021 | LTOI1, MP | leak: later r18.830114 |
| Stationfall | v3 r107.870430 | LTOI1, MP, leak | leak (hist): beta r63.870218, gamma r87.870326 |
| Suspect | v3 r14.841005 | LTOI1, MP, leak (hist) | leak: two one-byte-apart copies of later r18.850222 |
| Suspended | v3 r8.840521 | LTOI1, MP, leak | leak: earlier r7.830419 and a different r8.830521 |
| Trinity | v4 r12.860926 | LTOI2, MP, leak (hist) | leak: alpha, beta, later r15.870628 |
| The Witness | v3 r22.840924 | LTOI1, MP, leak | leak: r13-r23 series, incl. later r23.840925 |
| Wishbringer | v3 r69.850920 (PC) | LTOI2, MP, leak | Mac r68.850501 (LTOI2, MP); leak: an undisassemblable EZIP experiment; Solid Gold survives as source only |
| Zork I | v3 r88.840726 | LTOI1, ZA, MP, ZLC, leak (hist) | leak: later r119.880429, Solid Gold v5 r52.871125 |
| Zork II | v3 r48.840904 | LTOI1, ZA, MP, ZLC, leak (hist) | leak: later r63.860811 |
| Zork III | v3 r17.840727 | LTOI1, ZA, MP, ZLC, leak (hist) | leak: later r25.860811 |
| Zork Zero | v6 r393.890714 (PC) | FL89, LTOI1, ZA, MP, ZLC | Mac r296.881019 (LTOI1, MP, leak) |

Reading the table:

- **The sanctioned set is the 1992 file set.** Twenty-eight titles have a single standard build, and in every measured case it is byte-identical from its first CD appearance through 1997 - and for Zork Zero, back to the 1989 retail floppies themselves.
- **Five platform splits persist inside the sanctioned set** (Arthur, Journey, Seastalker, Sherlock, Zork Zero, plus the Solid Gold asymmetries of Hitchhiker's, Planetfall and Leather Goddesses): the PC build is the one that circulates in modern interpreters, the Mac build the one Mac-era players had. Where a split exists this table lists the PC build as the sanctioned one, since that is what the compilations' installers, and everything downstream of them, deliver.
- **Sanctioned rarely means final.** The leaked repositories hold post-sanction masters for eleven titles - Zork I r119 and Bureaucracy r160 most dramatically - none of which ever reached players. The community standard is wherever Activision's 1992 masters happened to stop.
- Hitchhiker's and Shogun are the fragile ones: each has exactly one disc carrying it (LTOI1 and LTOI2 respectively), which is precisely why those discs matter.
