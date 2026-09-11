# The Lost Treasures of Infocom II CD (1992) - title versions

Release and serial numbers read from the z-code headers of every story file on the disc, both platforms.
On the Mac side the story is the data fork of each game application; Arthur, Journey and Shogun ship a separate `STORY.DATA` beside their picture libraries.
On the DOS side the story is the game's `.DAT` (or `.ZIP` for the V6 games) in its own folder - there is no shared `DATA/` directory and no padding to round sizes on this disc; each file is natural size plus a `$1a` terminator.
"Same build" compares the z-code up to each file's header-declared length.
"Built-in hints" uses the same test as the other disc tables: the in-game hint system's machinery in the decoded text.

| Title | Z-machine | Mac release | PC release | Same build | Built-in hints |
| --- | --- | --- | --- | --- | --- |
| A Mind Forever Voyaging | v4 | r77.850814 | r77.850814 | yes | - |
| Arthur: The Quest for Excalibur | v6 | r54.890606 | r74.890714 | **no** | yes |
| Border Zone | v5 | r9.871008 | r9.871008 | yes | yes |
| Bureaucracy | v4 | r116.870602 | r116.870602 | yes | - |
| Cutthroats | v3 | r23.840809 | r23.840809 | yes | - |
| Hollywood Hijinx | v3 | r37.861215 | r37.861215 | yes | - |
| Journey | v6 | r26.890316 | r83.890706 | **no** | - |
| Nord and Bert Couldn't Make Head or Tail of It | v4 | r19.870722 | r19.870722 | yes | yes |
| Plundered Hearts | v3 | r26.870730 | r26.870730 | yes | - |
| Seastalker | v3 | r15.840522 | r16.850603 | **no** | - |
| Sherlock: The Riddle of the Crown Jewels | v5 | r26.880127 | r21.871214 | **no** | yes |
| Shogun | v6 | r292.890314 | r322.890706 | **no** | yes |
| Trinity | v4 | r12.860926 | r12.860926 | yes | - |
| Wishbringer | v3 | r68.850501 | r69.850920 | **no** | - |

Fourteen titles: the eleven of the Lost Treasures II package plus the CD edition's three bonus games, Arthur, Journey and Shogun.
Six ship as different builds per platform, five of them the familiar Mac-older pattern (Arthur, Journey, Seastalker, Shogun, Wishbringer) and one the reverse - Mac Sherlock is the newer r26.880127 sound build, and the disc's Mac `SOUND/` folder carries its seventeen sound files, byte-identical to the set later shipped on Masterpieces.

Every one of the thirteen titles this disc shares with [Masterpieces (1996)](../masterpieces-1996/versions.md) is byte-identical to Masterpieces' build on both platforms, splits included - so the Arthur, Journey, Seastalker, Sherlock and Wishbringer splits that Masterpieces exhibits all originate here, exactly as the Planetfall and Zork Zero splits originate on [volume 1](../lost-treasures-1-1992/versions.md).
The fourteenth title, Shogun, is the one Masterpieces later dropped: its Mac r292.890314 appears on no other cataloged medium, and its PC r322.890706 is byte-identical to the build preserved in the leaked source repositories ([historicalsource](../../collections/historicalsource/versions.md)).
