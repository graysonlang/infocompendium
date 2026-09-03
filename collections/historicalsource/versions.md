# The historicalsource repositories (2019) - title versions

In April 2019 the leaked Infocom source code was published on GitHub under the `historicalsource` account, one repository per game.
Treated as a compilation, it is the largest one there is: 49 repositories contain ZIL source, and 46 of them also carry compiled Z-machine story files - 70 distinct builds at the current HEAD, plus 19 more that exist only in earlier commits (see the git-history section below), enumerated the same way as the disc tables.
Captured 2026-09-03 by walking each repository's git tree through the GitHub API and reading each story file's z-code header; [checksums.txt](checksums.txt) records every file's git blob SHA, MD5 and SHA-1 so the exact bytes remain identifiable.

One thing this table does not claim: that a repository's compiled files correspond to its source.
The repositories' own READMEs state the binaries "were there as of final spin-down of the Infocom Drive" - leftovers archived beside the source, not builds of it - and the data below proves the point where it can: `witness` pairs one source tree with six builds spanning sixteen months, and `checkpoint` pairs Checkpoint source with a Journey binary.
With no surviving official compiler, source-to-build correspondence is unverifiable even where it is probable (the lone builds in `zork1` and `zorkzero` fit their source trees well).
The commit history settles how the binaries got there: they arrive in the initial source-import commits of 2019-04-14 (they are drive contents, not later additions), and the only archivist post-processing is the 2019-04-16 pair of reorganization commits, "Moved compilations to subdirectory" (creating `COMPILED/`) and "Extensions on Z-Machine Fixed" (adding the modern `.z3`/`.z5`-extension copies of the drive's `.zip` files).

Column notes:

- Most repositories carry each build twice (a `COMPILED/*.z*` copy and a `*.zip` twin, "ZIP" being Infocom's own name for Z-machine binaries); rows list every path that shares the one blob.
- "Built-in hints" uses the same test as the disc tables: the in-game hint system's machinery in the decoded text, not the mere presence of a HINT verb. The one `?` is a build `txd` cannot disassemble.
- "Same z-code as" marks builds byte-identical (up to the header-declared length) to a build on a cataloged disc: LTOI1 = [The Lost Treasures of Infocom (1992)](../../discs/lost-treasures-1-1992/versions.md), MP = [Masterpieces (1996)](../../discs/masterpieces-1996/versions.md), each split by platform side. A match against MP PC extends transitively to the [Zork Anthology (1994)](../../discs/zork-anthology-1994/versions.md) and [Zork Legacy Collection (1997)](../../discs/zork-legacy-1997-rtz-anthology/versions.md) copies of the anthology titles, which are the same bytes.

| Repository | Story file | Z-machine | Release | Built-in hints | Same z-code as |
| --- | --- | --- | --- | --- | --- |
| `abyss` | `abyss.z6` | v6 | r1.890320 | - | - |
| `amfv` | `s5.z4`, `s5.zip` | v4 | r77.850814 | - | MP Mac; MP PC |
| `ballyhoo` | `m4-release.z3`, `m4-release.zip` | v3 | r97.851218 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `ballyhoo` | `m4.z3`, `m4.zip` | v3 | r99.861014 | - | - |
| `beyondzork` | `bzalpha.z5`, `bzalpha.zip` | v5 | r1.870412 | - | - |
| `beyondzork` | `bzbeta.z5`, `bzbeta.zip` | v5 | r1.870715 | - | - |
| `beyondzork` | `z.zip` | v5 | r60.880610 | - | - |
| `borderzone` | `spy.z5`, `spy.zip` | v5 | r9.871008 | yes | MP Mac; MP PC |
| `bureaucracy` | `b.z4`, `b.zip` | v4 | r160.880521 | - | - |
| `checkpoint` | `spy.z5`, `spy.zip` | v5 | r46.880603 | - | - |
| `cutthroats` | `toa.z3`, `toa.zip` | v3 | r25.840917 | - | - |
| `deadline` | `dead-deadline.z3`, `dead-deadline.zip` | v3 | r28.850129 | - | - |
| `deadline` | `deadline.z3`, `deadline.zip` | v3 | r27.831005 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `enchanter` | `enchanter.z3`, `z4.z3` | v3 | r29.860820 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `hitchhikersguide-gold` | `nhitch.zip` | v5 | r31.871119 | yes | LTOI1 PC |
| `hitchhikersguide` | `s4.z3`, `s4.zip` | v3 | r60.861002 | - | - |
| `hollywoodhijinx` | `anthill.z3`, `anthill.zip` | v3 | r37.861215 | - | MP Mac; MP PC |
| `infidel` | `infidel.z3`, `infidel.zip` | v3 | r22.830916 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `infocom-sampler` | `demo-r15.z3`, `demo-r15.zip` | v3 | r15.840330 | - | - |
| `infocom-sampler` | `demo-r5.z3`, `demo-r5.zip` | v3 | r5.840512 | - | - |
| `infocom-sampler` | `sampler.z3`, `sampler.zip` | v3 | r55.850823 | - | - |
| `journey` | `journey.z6`, `journey.zip` | v6 | r83.890706 | - | MP PC |
| `journey` | `ojourney.zip` | v6 | r54.890526 | - | - |
| `leathergoddesses-gold` | `x1.z5`, `x1.zip` | v5 | r4.880405 | yes | MP Mac |
| `leathergoddesses` | `x1.z3`, `x1.zip` | v3 | r59.860730 | - | MP PC |
| `lurkinghorror` | `h1.z3`, `h1.zip` | v3 | r221.870918 | - | - |
| `minizork-1982` | `zork.z3`, `zork.zip` | v3 | r2.840207 | - | - |
| `minizork-1987` | `mini.z3`, `mini.zip` | v3 | r34.871124 | - | - |
| `minizork2-1988` | `mini2.z3`, `mini2.zip` | v3 | r2.871123 | - | - |
| `moonmist` | `m5.z3`, `m5.zip` | v3 | r13.880501 | - | - |
| `nordandbert` | `j3.z4`, `j3.zip` | v4 | r20.870722 | yes | - |
| `planetfall-gold` | `s3.zip` | v5 | r10.880531 | yes | LTOI1 Mac; MP Mac |
| `planetfall` | `planetfall.z3`, `planetfall.zip` | v3 | r39.880501 | - | - |
| `plunderedhearts` | `r1.z3`, `r1.zip` | v3 | r26.870730 | - | MP Mac; MP PC |
| `restaurant` | `h2.z6`, `h2.zip` | v6 | r184.890412 | - | - |
| `seastalker` | `atari.z3`, `atari.zip` | v3 | r17.850208 | - | - |
| `seastalker` | `coco.z3`, `coco.zip` | v3 | r15.840612 | - | - |
| `seastalker` | `j1.z3`, `j1.zip` | v3 | r18.850919 | - | - |
| `seastalker` | `non-atari.z3`, `non-atari.zip` | v3 | r17.850208 | - | - |
| `seastalker` | `reg.z3`, `reg.zip` | v3 | r16.850603 | - | MP PC |
| `seastalker` | `seastalker.z3`, `seastalker.zip` | v3 | r16.850515 | - | - |
| `seastalker` | `tandy.z3`, `tandy.zip` | v3 | r15.840716 | - | - |
| `sherlock` | `gamesound.zip` | v5 | r26.880127 | yes | MP Mac |
| `shogun` | `a5.zip` | v6 | r322.890706 | yes | - |
| `sorcerer` | `sorcerer.z3`, `sorcerer.zip` | v3 | r18.860904 | - | - |
| `spellbreaker` | `z6.z3`, `z6.zip` | v3 | r87.860904 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `starcross` | `starcross.z3`, `starcross.zip` | v3 | r18.830114 | - | - |
| `stationfall` | `s6.zip` | v3 | r107.870430 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `suspect` | `dm3.z3`, `dm3.zip` | v3 | r18.850222 | - | - |
| `suspect` | `m3.zip` | v3 | r18.850222 | - | - |
| `suspended` | `mac.z3`, `mac.zip` | v3 | r8.840521 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `suspended` | `r7.z3`, `r7.zip` | v3 | r7.830419 | - | - |
| `suspended` | `suspended.z3`, `suspended.zip` | v3 | r8.830521 | - | - |
| `trinity` | `tr.z4`, `tr.zip` | v4 | r15.870628 | - | - |
| `trinity` | `tralpha.z4`, `tralpha.zip` | v4 | r1.851202 | - | - |
| `trinity` | `trbeta.z4`, `trbeta.zip` | v4 | r1.860221 | - | - |
| `wishbringer` | `j2.z3`, `j2.zip` | v3 | r69.850920 | - | MP PC |
| `wishbringer` | `nj2.z3`, `nj2.zip` | v3 | r32933.880609 | ? | - |
| `witness` | `r13.z3`, `r13.zip` | v3 | r13.830524 | - | - |
| `witness` | `r18.z3`, `r18.zip` | v3 | r18.830910 | - | - |
| `witness` | `r20.z3`, `r20.zip` | v3 | r20.831119 | - | - |
| `witness` | `r21.z3`, `r21.zip` | v3 | r21.831208 | - | - |
| `witness` | `r22.z3`, `r22.zip` | v3 | r22.840924 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `witness` | `witness.z3`, `witness.zip` | v3 | r23.840925 | - | - |
| `zork-german` | `zork1.zip` | v6 | r15.890613 | yes | - |
| `zork1-gold` | `nzork1.zip`, `zork1.zip` | v5 | r52.871125 | yes | - |
| `zork1` | `zork1.z3`, `zork1.zip` | v3 | r119.880429 | - | - |
| `zork2` | `zork2.z3`, `zork2.zip` | v3 | r63.860811 | - | - |
| `zork3` | `zork3.z3`, `zork3.zip` | v3 | r25.860811 | - | - |
| `zorkzero` | `zork0.zip` | v6 | r296.881019 | yes | LTOI1 Mac; MP Mac |

## What matches the discs

Twenty-one of the seventy builds are z-code-identical to a disc build, including every Solid Gold repository: `hitchhikersguide-gold` is LTOI1's PC build, `planetfall-gold` is the Mac build on both hybrid discs, and `leathergoddesses-gold` is Masterpieces' Mac build.
`zorkzero` holds r296.881019 - the Mac disc build; the PC side's r393 with its reworked border graphics is **not** in the leak, consistent with [the Masterpieces analysis](../../discs/masterpieces-1996/notes.md) that the leaked ZIL predates the r393 border rework.
`journey` holds exactly Masterpieces' PC build (r83.890706), `sherlock` exactly its Mac sound build (r26.880127), and `seastalker`'s `reg.z3` is exactly Masterpieces' odd PC-only r16.850603 - the repositories settle where that disc's Seastalker split came from.

## What the discs never shipped

- **Post-release masters newer than any disc build**: Zork I r119.880429, Zork II r63.860811, Zork III r25.860811, Cutthroats r25.840917, Deadline r28.850129, Sorcerer r18.860904, Moonmist r13.880501, Planetfall r39.880501, Hitchhiker's r60.861002, Beyond Zork r60.880610, Trinity r15.870628, Bureaucracy r160.880521, Nord and Bert r20.870722, The Witness r23.840925, Ballyhoo r99.861014.
- **The Lurking Horror r221.870918, the sound release** (129,944 bytes). No cataloged disc ships this story file, but Masterpieces ships `LHSOUND.ZIP`, whose `LURKING.CNV` is an XOR patch (129,944 bytes, one byte per output byte; the algorithm is in the package's own `UPDATELH.C`) that converts the disc's r203 to r221. Verified 2026-09-03 by applying the patch to Masterpieces' r203: the output is **byte-identical** to this repository's `h1.z3`, with the patcher's own checksums valid. The leak and the disc carry the same r221, one as a file and one as a delta.
- **Unreleased games**: `abyss` (James Cameron's The Abyss, v6 r1.890320), `restaurant` (The Restaurant at the End of the Universe, v6 r184.890412), and `zork-german` (a v6 German translation of Zork I, r15.890613 - with built-in hints).
- **Development snapshots**: Beyond Zork alpha (r1.870412) and beta (r1.870715), Trinity alpha (r1.851202) and beta (r1.860221), a Journey beta (`ojourney.zip`, r54.890526), and five generations of The Witness (r13 through r23) of which only r22.840924 ever shipped on these discs.
- **The samplers**: three Infocom Sampler demos (r15.840330, r5.840512, r55.850823) and the three Mini-Zork releases, none of which appear on the compilations.
- **Zork I Solid Gold** (`zork1-gold`, v5 r52.871125, with hints): the one Solid Gold edition none of the cataloged discs carries in any form.

## Oddities

- **The `checkpoint` repository's compiled file is not Checkpoint.** The repo holds Stu Galley's unreleased *Checkpoint* in source form, but its lone `COMPILED/spy.z5` (v5 r46.880603, copyright 1988) is full of Praxix, Bergon, Esher and Astrix - it is an early, otherwise unknown v5 prototype of *Journey*, filed in the wrong game's repository. No compiled Checkpoint exists in the leak.
- **Two Suspects, one byte apart.** `suspect` carries two copies of r18.850222 that differ in exactly one content byte (plus the header checksum) - a hand-patched build, and neither is the r14.841005 the discs ship.
- **Two different "release 8" Suspendeds.** `suspended.z3` is r8.830521 and `mac.z3` is r8.840521 - same release number, serials a year apart; only the later one matches the discs. The serial, not the release, is the discriminator.
- **`wishbringer` carries an experimental build** (`nj2.z3`) whose release field reads 32933 with serial 880609 - an EZIP-era test binary that `txd` cannot disassemble.
- **Seastalker is the most-built game in the leak**: seven distinct builds, including platform-targeted Atari, TRS-80 CoCo and Tandy variants that the compilations never carried.

## A second layer in the git histories

The repositories were not imported as single snapshots.
For most classic games the archivist committed an earlier drive state first - the commit is labeled "Revision NN (Original Source)" where NN is a shipped release - and then committed "Final Revision", the drive's shutdown state, on top; `stationfall` even carries "Beta Version" and "Gamma Version" layers, and `beyondzork` a "Revision 57" between its two.
The HEAD trees enumerated above therefore hide a second census: 19 builds that exist only in earlier commits, recoverable with `git cat-file` at the commit shown.

| Repository | Commit | Import label | File | Z-machine | Release | Built-in hints | Same z-code as |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `beyondzork` | `86b36fa` | Revision 57 | `z.zip` | v5 | r57.871221 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `cutthroats` | `47fbe00` | Revision 23 (Original Source) | `toa.zip` | v3 | r23.840809 | - | MP Mac; MP PC |
| `enchanter` | `826abeb` | Revision 24 (Original Source) | `enchanter.zip` | v3 | r24.851118 | - | - |
| `hitchhikersguide` | `c55088a` | Revision 58 (Original Source) | `s4.zip` | v3 | r58.851002 | - | - |
| `lurkinghorror` | `7edaa11` | Revision 203 (Original Source) | `h1.zip` | v3 | r203.870506 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `moonmist` | `7dcf75b` | Revision 9 (Original Source) | `m5.zip` | v3 | r9.861022 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `nordandbert` | `1f51010` | Revision 19 (Original Source) | `j3.zip` | v4 | r19.870722 | yes | MP Mac; MP PC |
| `planetfall` | `281bd34` | Revision 37 (Original Source) | `planetfall.zip` | v3 | r37.851003 | - | LTOI1 PC; MP PC |
| `seastalker` | `18809a2` | Revision 15 (Original Source) | `atari.zip` | v3 | r15.840522 | - | MP Mac |
| `seastalker` | `18809a2` | Revision 15 (Original Source) | `j1.zip` | v3 | r15.840501 | - | - |
| `sorcerer` | `daad2bd` | Revision 13 (Original Source) | `sorcerer.zip` | v3 | r13.851021 | - | - |
| `spellbreaker` | `3a4d17d` | Revision 63 (Original Source) | `z6.zip` | v3 | r63.850916 | - | - |
| `stationfall` | `24f2323` | Gamma Version | `s6.zip` | v3 | r87.870326 | - | - |
| `stationfall` | `9c713dd` | Beta Version | `s6.zip` | v3 | r63.870218 | - | - |
| `suspect` | `1c8c4fc` | Revision 14 (Original Source) | `m3.zip` | v3 | r14.841005 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `trinity` | `54d8efc` | Revision 12 (Original Source) | `tr.zip` | v4 | r12.860926 | - | MP Mac; MP PC |
| `zork1` | `34cc828` | Revision 88 (Original Source) | `zork1.zip` | v3 | r88.840726 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `zork2` | `d26f157` | Revision 48 (Original Source) | `zork2.zip` | v3 | r48.840904 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |
| `zork3` | `1dfe76c` | Revision 17 (Original Source) | `zork3.zip` | v3 | r17.840727 | - | LTOI1 Mac; LTOI1 PC; MP Mac; MP PC |

Twelve of the nineteen are the exact shipped masters, and they close gaps the HEAD census left open: the shipped Zork I/II/III (r88/r48/r17), Beyond Zork r57, The Lurking Horror r203, Moonmist r9, Nord and Bert r19, Planetfall r37, Suspect r14, Trinity r12 and Cutthroats r23 - each z-code-identical to the disc copies - plus Seastalker's `atari.zip` in the "Revision 15" layer, which is actually the Mac disc build r15.840522 (the platform labels shifted between layers).
The other seven never shipped on the cataloged discs at all: Enchanter r24.851118, Hitchhiker's r58.851002, Sorcerer r13.851021, Spellbreaker's first release r63.850916, a second Seastalker r15 (serial 840501), and Stationfall's beta (r63.870218) and gamma (r87.870326).
So in these repositories the layer where source and binary do plausibly correspond is the "Revision NN (Original Source)" commit - shipped source paired with its shipped build - while HEAD pairs the final source state with whatever binaries the drive held last.

## Internal codenames

The leak's internal filenames - the compiled stories and their `.serial` companions - are Infocom's project codes, and they are genre-keyed.
Observed in the repositories:

| Series | Observed members |
| --- | --- |
| z (Zork line) | z4 Enchanter, z6 Spellbreaker, plain `z` Beyond Zork (Zork I-III themselves are simply `zork1`-`zork3`) |
| m (Mystery) | m3 Suspect, m4 Ballyhoo, m5 Moonmist |
| s (Science fiction) | s3 Planetfall, s4 Hitchhiker's Guide, s5 A Mind Forever Voyaging, s6 Stationfall |
| j (Junior/introductory) | j1 Seastalker, j2 Wishbringer, j3 Nord and Bert |
| One-offs | x1 Leather Goddesses, r1 Plundered Hearts, h1 The Lurking Horror, `spy` Border Zone, `tr` Trinity, `b` Bureaucracy, `toa` Cutthroats (Infocom's "Tales of Adventure" genre label), `anthill` Hollywood Hijinx (its working title) |
| n- prefix (remasters) | `nhitch` Solid Gold Hitchhiker's, `nzork1` Solid Gold Zork I, and Wishbringer's experimental `nj2.z3` - which this decodes as the abandoned start of an EZIP Wishbringer remaster |

Two codes are small revelations: `restaurant`'s story is `h2` - **H**itchhiker's **2**, the sequel tracked under its parent's letter, not a genre - and the unlabeled early mysteries Deadline and The Witness sit where m1 and m2 ought to be, before the convention took hold.

The Mac type/creator codes in [Masterpieces' catalog listing](../../discs/masterpieces-1996/masterpieces-1996.hls.txt) corroborate the scheme from the packaging side: `INm5` Moonmist, `INZ4` Enchanter, `INz6` Spellbreaker, `INH1` Lurking Horror, `INR1` Plundered Hearts - and extend it where the leak is silent: `INZ5` Sorcerer completes the Enchanter trilogy as z4/z5/z6, `INM9` makes Sherlock mystery number nine, `INZ7` Trinity and `INZ8` A Mind Forever Voyaging keep counting the Zork line, and `INE1` files Border Zone under espionage.

The two systems also drift, which dates them as different eras of the same idea: Nord and Bert is `j3` in the source but creator `INC3` on the disc (with Bureaucracy `INC2` - a comedy series?), Wishbringer is `j2` in the source but `INR2` on the disc, Leather Goddesses is `x1` in the source but `INS7` (science fiction) in the catalog, and by the v6 era the creators are per-game again: `INJ1` Journey, `INL1` Arthur, `IN0Z` Zork Zero.

## The .serial files do not hold the release numbers

Thirty-two repositories carry a `<codename>.serial` file next to the source - a bare number.
The natural guess is that it tracks the release, so here is the cross-check: every `.serial` value against the release of the same-codename compiled build in the same repository.

| Repository | File | Value | Same-codename build | Release minus value |
| --- | --- | --- | --- | --- |
| `ballyhoo` | `m4.serial` | 12 | r99.861014 | +87 |
| `beyondzork` | `z.serial` | 457 | r60.880610 | -397 |
| `bureaucracy` | `b.serial` | 56 | r160.880521 | +104 |
| `checkpoint` | `spy.serial` | 371 | r46.880603 | -325 |
| `cutthroats` | `toa.serial` | 2 | r25.840917 | +23 |
| `deadline` | `deadline.serial` | 1 | r27.831005 | +26 |
| `enchanter` | `z4.serial` | 24 | r29.860820 | +5 |
| `hitchhikersguide-gold` | `nhitch.serial` | 33 | r31.871119 | -2 |
| `hollywoodhijinx` | `anthill.serial` | 407 | r37.861215 | -370 |
| `infocom-sampler` | `sampler.serial` | 48 | r55.850823 | +7 |
| `lurkinghorror` | `h1.serial` | 132 | r221.870918 | +89 |
| `minizork-1987` | `mini.serial` | 1 | r34.871124 | +33 |
| `minizork2-1988` | `mini2.serial` | 1 | r2.871123 | +1 |
| `moonmist` | `m5.serial` | 67 | r13.880501 | -54 |
| `nordandbert` | `j3.serial` | 48 | r20.870722 | -28 |
| `planetfall-gold` | `s3.serial` | 23 | r10.880531 | -13 |
| `plunderedhearts` | `r1.serial` | 36 | r26.870730 | -10 |
| `restaurant` | `h2.serial` | 263 | r184.890412 | -79 |
| `seastalker` | `reg.serial` | 1 | r16.850603 | +15 |
| `seastalker` | `non-atari.serial` | 2 | r17.850208 | +15 |
| `seastalker` | `j1.serial` | 3 | r18.850919 | +15 |
| `sherlock` | `gamesound.serial` | 27 | r26.880127 | -1 |
| `spellbreaker` | `z6.serial` | 439 | r87.860904 | -352 |
| `suspect` | `m3.serial` | 137 | r18.850222 | -119 |
| `trinity` | `tr.serial` | 10 | r15.870628 | +5 |
| `wishbringer` | `j2.serial` | 10 | r69.850920 | +59 |
| `witness` | `witness.serial` | 4 | r23.840925 | +19 |
| `zork-german` | `zork1.serial` | 143 | r15.890613 | -128 |
| `zork1` | `zork1.serial` | 1 | r119.880429 | +118 |
| `zork1-gold` | `zork1.serial` | 60 | r52.871125 | -8 |
| `zork2` | `zork2.serial` | 15 | r63.860811 | +48 |
| `zork3` | `zork3.serial` | 12 | r25.860811 | +13 |

So: no.
The deltas run from -397 to +118, in both directions, and `witness.serial` reads 4 in a repository that preserves six successive release builds - the value tracks neither the release nor the count of kept builds.

The one place the relationship is visible is `seastalker`, the only repository with several `.serial` files: all three sit at exactly release minus 15, in sequence (1 -> r16, 2 -> r17, 3 -> r18).
Within one directory the counter and the release move in lockstep; across directories the offset is arbitrary.
That is consistent with the `.serial` file being a per-directory counter maintained by the toolchain while the release word tracked the output story file's TOPS-20 generation number: the two agree only up to whatever generation the directory's story file started at, which each new working directory reset differently.
The near-misses fit the same picture - young single-lineage trees land close (`sherlock` -1, `nhitch` -2, `mini2` +1), long-lived ones drift far (`beyondzork` at 457 against r60).

## Source-only and non-game repositories

`arthur` and `wishbringer-gold` contain ZIL source but no compiled story file, so the leak has no Arthur build at all (Masterpieces' r54/r74 exist only on disc) and no compiled Solid Gold Wishbringer.
`infocom-zcode-terps` (interpreter source for a dozen platforms) and `zil` (language documentation) round out the Infocom material; the account's Zork history repositories (`zork-mdl`, `zork-fortran`, `zork-1977-source`, `zork-german` aside) predate ZIL and hold no Z-machine files.
