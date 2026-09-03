# The Zork Anthology (1994) - title versions

The games on this disc exist only inside `ZORKANTH.RED`, the Activision installer archive, so their versions cannot be read off the mounted volume.
They were identified from the archive itself: each member record carries the file's uncompressed size and a CRC-16 of the uncompressed data, and every game file's size and CRC match, exactly, the corresponding file on the other discs in this catalog - so the builds below are established without unpacking a byte.
The container's record layout is documented in [notes.md](notes.md).

"Built-in hints" marks builds whose z-code contains the in-game hint system, determined from the decoded text of the byte-identical copies on the other discs.

| Title | Z-machine | Release | Story file in the archive | Built-in hints |
| --- | --- | --- | --- | --- |
| Zork I | v3 | r88.840726 | `ZORK1.DAT` (92,160 bytes padded) | - |
| Zork II | v3 | r48.840904 | `ZORK2.DAT` (92,160 bytes padded) | - |
| Zork III | v3 | r17.840727 | `ZORK3.DAT` (92,160 bytes padded) | - |
| Zork Zero | v6 | r393.890714 | `ZORK0.ZIP` (300,032 bytes) | yes |
| Beyond Zork | v5 | r57.871221 | `BEYONDZO.DAT` (276,480 bytes padded) | - |
| Planetfall | v3 | r37.851003 | `PLANETFA.DAT` (122,880 bytes padded) | - |

Six games, not five: alongside the five Zork titles the archive carries Planetfall, the box's bonus game, with its own `PF.COM` interpreter, `PLANETF.BAT` and `PLANETF.ICO`.

Every one is the [1992 LTOI CD's](../lost-treasures-1-1992/versions.md) PC build, byte for byte, caret padding included, and the archive's internal timestamps agree: the story files are dated April-May 1992, two years before this disc, with only the Windows dressing (icons, batch files, the `ZORK.GRP` Program Manager group) dated August 1994.
Zork Zero is the PC-side r393 with the same incomplete graphics set (`ZORK0.CG1` and `ZORK0.EG1` only, no `.MG1` or `.EG2`).
The interpreters travel too: `Z1.COM`/`Z2.COM`/`Z3.COM` are the 11,402-byte 3M2 build that the [1997 Zork Legacy Collection disc](../zork-legacy-1997-rtz-anthology/versions.md) ships as `_ZORKn.COM`, and `PF.COM` at 12,004 bytes is interpreter 3N.
So the same 1992 masters flow unmodified through 1994, 1996 and 1997 - this disc completes the chain.
