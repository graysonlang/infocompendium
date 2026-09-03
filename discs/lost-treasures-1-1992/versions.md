# The Lost Treasures of Infocom CD (1992) - title versions

Release and serial numbers read from the z-code headers of every story file on the disc, both platforms.
Generated from the extracted contents; see [notes.md](notes.md) for how the disc was read.
Where the two platforms ship different Z-machine versions, the cell reads Mac / PC.
"Built-in hints" marks builds whose z-code contains the in-game hint system (the on-screen InvisiClues menu), determined from the decoded game text rather than the mere presence of a HINT verb - several hint-less games define HINT only to point at the mail-order InvisiClues booklet.

| Title | Z-machine | Mac release | PC release | Same build | Built-in hints |
| --- | --- | --- | --- | --- | --- |
| Ballyhoo | v3 | r97.851218 | r97.851218 | yes | - |
| Beyond Zork | v5 | r57.871221 | r57.871221 | yes | - |
| Deadline | v3 | r27.831005 | r27.831005 | yes | - |
| Enchanter | v3 | r29.860820 | r29.860820 | yes | - |
| The Hitchhiker's Guide to the Galaxy | v3 / v5 | r59.851108 | r31.871119 | **no** | PC only |
| Infidel | v3 | r22.830916 | r22.830916 | yes | - |
| The Lurking Horror | v3 | r203.870506 | r203.870506 | yes | - |
| Moonmist | v3 | r9.861022 | r9.861022 | yes | - |
| Planetfall | v5 / v3 | r10.880531 | r37.851003 | **no** | Mac only |
| Sorcerer | v3 | r15.851108 | r15.851108 | yes | - |
| Spellbreaker | v3 | r87.860904 | r87.860904 | yes | - |
| Starcross | v3 | r17.821021 | r17.821021 | yes | - |
| Stationfall | v3 | r107.870430 | r107.870430 | yes | - |
| Suspect | v3 | r14.841005 | r14.841005 | yes | - |
| Suspended | v3 | r8.840521 | r8.840521 | yes | - |
| The Witness | v3 | r22.840924 | r22.840924 | yes | - |
| Zork I | v3 | r88.840726 | r88.840726 | yes | - |
| Zork II | v3 | r48.840904 | r48.840904 | yes | - |
| Zork III | v3 | r17.840727 | r17.840727 | yes | - |
| Zork Zero | v6 | r296.881019 | r393.890714 | **no** | yes |

The PC story files are padded to round sizes (92,160 / 122,880 / 153,600 / 184,320 / 276,480 bytes); the Mac data forks are the same builds at natural size where the release matches.
Interpreters: per-game DOS `.COM`/`.EXE` files on the PC side; on the Mac side each game is a double-clickable application (type `APPL`, per-game creators such as `INZ1`).

Of the three mismatches: r31.871119 is the Solid Gold Hitchhiker's (in-game hints) and r10.880531 the Solid Gold Planetfall, so each platform got the enhanced build of a different game; the Zork Zero split (r296 Mac, r393 PC) persisted into the 1996 and 1997 compilations.
The hints column tracks this exactly: on this disc, built-in hints exist only where a platform got a Solid Gold build, plus Zork Zero, whose on-screen hints are native to both of its releases.
