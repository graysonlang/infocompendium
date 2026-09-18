# Floppy imaging: flux capture and the 8-bit formats

Optical discs are covered in [imaging.md](imaging.md).
This page is about 5.25" and 3.5" diskettes, where the disc is read at flux level and the format is decoded afterwards.
Every finding here was established against media that decoded completely, so each one has a positive control behind it.

Hardware used throughout: a Greaseweazle V4.1 (firmware 1.6) with a TEAC FD-55GFR.

## The drive is 96 tpi and the media is 48 tpi

The FD-55GFR is an 80-track high-density drive.
Apple II, Atari 8-bit, Commodore 1541 and PC 360K media are all 48 tpi, so every read needs `step=2` to land on track centers.
Omit it and the head sits between tracks.

## Capture flux, not sectors

```
gw read --tracks=c=0-34:step=2 --revs=2 --raw --format=<fmt> disk.scp
gw convert --format=<fmt> disk.scp disk.img
```

Both flags on the read matter.
`--format` makes the read verify each track as it goes, with retries on marginal ones.
`--raw` keeps the stored flux genuine - without it, `gw read` writes flux re-synthesized from the decoded sectors, which looks clean but has lost the weak bits and timing detail that flux capture exists to preserve.

## Formats and what a good read looks like

| Media | Format | Tracks | Complete read |
| --- | --- | --- | --- |
| Apple II | `apple2.appledos.140` | `c=0-34` | 560 sectors (35 x 16 x 256) |
| Atari 810/1050 | `atari.90` | `c=0-39` | 720 sectors (40 x 18 x 128) |
| Commodore 1541 | `commodore.1541` | `c=0-34` | **683** sectors (zoned) |
| PC 360K | `ibm.360` | `c=0-39` | 720 sectors, two heads |

The Commodore format is zoned and the others are not: 21 sectors on tracks 0-16, 19 on 17-23, 18 on 24-29, 17 from 30 up, with the clock stepping 3.25 -> 4.00us per zone.
A complete 35-track read is 683 sectors, not a round number, so do not read a non-round count as failure.
A 40-track C64 release is 768; `c=0-34` would silently miss the last five tracks.

Atari labels reading "810 or 1050 disk" mean single density - `atari.90`.
`atari.130` is 1050-only enhanced density and returns 0 sectors on single-density media.

`ibm.scan` auto-detects without being told the format, which makes it a useful independent check on a decode you are unsure of.

## Sector ordering is not cosmetic

Apple II images come in three sector orders that differ only in layout: `appledos`, `prodos`, `nofs`.
Choosing wrong still reports a full 560/560 while producing scrambled bytes.
`apple2.appledos.140` is correct for Infocom Apple II disks, confirmed with ZCut - appledos extracts Zork I with "Checksum good" where prodos gives "Checksum bad".

Sector position inside an appledos image is `(track * 16 + INV[sector]) * 256`, where `INV` is the inverse of the DOS 3.3 interleave `0DB97531ECA8642F`.

## Unrecovered sectors are marked, not zeroed

Greaseweazle fills a sector it could not recover with the ASCII string `-=[BAD SECTOR]=-` repeated to 256 bytes.
That is the reliable way to locate damage in a decoded image.
Do not assume zero-fill: a clean image legitimately contains empty sectors, and on one disc here 119 of them were genuinely blank.
Nor should damage be inferred from bytes that differ between two reads - those are simply sectors one read recovered and the other did not.

## Merging several reads of a damaged disc

`gw convert` can recover fewer sectors than `gw read` did from the same flux.
Read-time retries decode each attempt and accumulate recovered sectors; convert re-decodes the stored flux in a single pass.
Measured here on one title: read reported 559/560 while converting that same `.scp` gave 556/560.
It is not a sector-order or PLL artifact - both orderings give identical counts, and five PLL variations changed nothing.
Only marginal media is affected; clean captures convert identically.

So on a disc with weak sectors, also run a non-`--raw` read to keep the image the drive actually recovered, or take several captures and merge per-sector.
One title here reached a complete image only by merging four reads, none of which was complete alone.

When merging, decode every source with the same geometry.
Passing `--tracks=c=0-69:step=2` to a convert of a `step=2` capture silently mis-decodes it; that is only correct for `step=1` sweeps.

## Reading the second side of a flippy

Apple II, Atari and Commodore drives are all soft-sectored: they find sectors by reading address marks and never need the index pulse.
The Greaseweazle does need it, to delimit revolutions.
That difference is the whole problem.

A disc with **two index holes** can simply be flipped and read normally.
A disc with **one** cannot: flipped, the hole no longer lines up, the drive's sensor never fires, and gw reports `GetFluxStatus: No Index`.
The index hole does not control spinning - the motor runs whenever the drive is selected - it only provides the timing reference.

`--fake-index` tells the firmware to synthesize its own pulses and is the documented workaround, but per the Greaseweazle wiki it "requires a drive which will spin up in the absence of index pulses (many will not)".
The TEAC FD-55GFR is one that will not: it returns `0 flux in 0.00ms` regardless of the value passed, and neither the drive's index-sensor jumpers nor its RY/DC jumper changes that.
For such a disc on such a drive there is no software route to the second surface - only a different drive, a flippy-modded drive with a second index sensor, or punching the jacket.
Punching does work: two Atari discs here were punched for a second index hole and their reverse sides then read normally, one at a clean 720/720 and one marginally at 700/720.
It destroys original packaging, so treat it as a last resort rather than a method.

### Reading side 2 through head 1

A double-sided drive's second head sits against the opposite surface, so it can read a flippy's second side in place, with no flipping and no index problem:

```
gw read --tracks=c=0-39:h=1:step=2 --revs=2 --raw disk_h1.scp
gw convert --format=<fmt> --reverse disk_h1.scp disk_h1.img
```

`--reverse` is required: the second surface was written for a flipped disc, so read in place it is rotationally reversed.
Verified symmetrically here - reading a known disc both ways round reproduced each side's known-good bytes exactly.

Two limits.
Some formats declare `heads = 1` and will refuse head 1 with "Out of range for format"; capture raw and decode with `ibm.scan --reverse` instead.
And on this drive head 1 sits **four cylinders inward**: head-1 cylinder N returns real track N+4, so the outermost four tracks of the second surface cannot be reached at all.
The Greaseweazle wiki documents `h1.off=-8` for flippy-modded drives, which is the same offset in physical steps.

## A format with no address fields at all

Not every soft-sectored format has address marks, and a decoder that assumes they exist will report a written surface as blank.

Infocom's Apple II XZIP (v5) titles are the case encountered here.
Per Michael Sternberg's *An Apple II Build Chain for Inform* (KansasFest 2017), an XZIP game ships on one or two disks: the first is 16-sector, with boot code and the interpreter on tracks 0-3 and the story from track 5, and "if the story file is larger than 100,864 bytes, the remainder of the Z-code is stored on a second 18-sector disk image."
On the three discs here that second image is the reverse side of the same diskette.

That 18-sector surface is laid out as:

- exactly **one** `D5 AA AD` sync mark per track, roughly 357 nibbles in, and no address fields anywhere;
- then 18 back-to-back data fields of 343 nibbles each (342 GCR bytes plus a checksum), at exactly `5 + 343*n` from the mark, with no drift;
- story blocks mapped linearly - block *b* at track `b // 18`, sector `b % 18` - where side 1's story is interleaved through the forward DOS 3.3 table.

Two lessons, both learned the hard way:

**A sector count of 0/560 under every stepping is not evidence of a blank surface.** No stock Apple decoder can read a track without address fields, so that result is what a perfectly good disc of this kind looks like. The written, reproducible flux is the signal; the decoder's silence is not a measurement.

**Do not search a window for a passing sector checksum.** The Apple 6-and-2 data-field checksum is only **6 bits**, so scanning N candidate offsets yields roughly N/64 false positives per sector. Wide-window searches reported 616 of 630 sectors "recovered" on one title here; an exhaustive scan of a single track found 102 valid-looking groups where 18 exist. Correct sectors sit at offset +0 exactly. Decode at computed positions and verify against something stronger.

The layout above was reverse-engineered off the flux and then confirmed against two sources that agree with it exactly.
S. V. Nickolas's `interlz5.c`, which writes these images, contains the literal line `o=5+(s*343);`, fills `track[3]`/`track[4]` from a hardcoded 35-entry table of 4-and-4 track numbers, and uses the same `{0,D,B,9,7,5,3,1,E,C,A,8,6,4,2,F}` interleave for side 1.
Infocom's own XZIP interpreter source contains the reading half, a routine commented "READ SECTOR FROM BIG TRACK" that hunts the mark, decodes the 4-and-4 track number, and then walks forward sector by sector, checking the checksum only on the one it wants.
That is why the stride never drifts: the interpreter has no way to seek within the track, so the sectors must be exactly where it counts them.

### Two things to get right when slicing the flux

**The bit cell is not 4000 ns.** This media was written at 300 RPM. A 360 RPM drive such as the TEAC FD-55GFR reads it 6/5 fast, putting the cell near **3355 ns**. Fit the period per track rather than assuming it; a fixed 4000 ns nominal with a +/-10% clamp cannot even reach the true value.

**Spurious flux reversals land inside 3-cell gaps.** A genuine 10,020 ns gap arrives as roughly 5828 + 3828 ns, which slices to `011` where the disc says `001`. Every decode error observed here was that one defect: a single 0 bit read as 1, never the reverse. It is quiet and it is devastating, because one wrong nibble propagates through the running-XOR chain and corrupts every byte after it in the sector - which is why a sector with a single bad bit comes back looking like 256 bytes of garbage.

Neither piece of a split gap fits the cell grid (residuals around 0.26 and 0.15 cell) while their sum fits to about 0.11, so the pair can be re-fitted and merged. On a known build that one correction moved the result from 122 to 223 of 231 sectors. Combining independent captures and voting across revolutions took it to 227.

### One setting does not fit every track

The re-fitting above is tuned against clean tracks, and that tuning is actively wrong on marginal ones.
A noisy track has larger fit residuals everywhere, so an aggressive setting merges transitions that are real and silently shortens the track.
That is measurable rather than a matter of taste: count nibbles between one track's mark and the next, and compare against the `5 + 343*18 = 6179` the format needs.
Good tracks here showed about 60 nibbles of slack; over-merged ones showed 25, and one showed *minus* 65 - the decoded track could not physically hold its own data.
Easing off took Beyond Zork's track 28 from 0 of 18 sectors to 15.
Run a spread of settings rather than choosing one, and let the sector checksum pick.

### Keep captures separate until the last moment

It is tempting to pool every revolution of every capture and vote across the lot.
Do not. A single dropped nibble shifts a whole stream, and two reads of one track can then share almost no positions - measured here, runs of the same track ranged from 3% to 100% agreement.
Merging across that produces a stream of individually-valid nibbles that is collectively wrong, which is worse than an obvious failure because it looks like clean data.
Cluster runs *within* each capture, form candidate sectors there, and only then combine candidates across captures, preferring ones that more than one capture produced.
That ordering alone was worth five sectors on Border Zone.

### What it yields

Measured against builds whose contents are known, with [scripts/xzip18.py](../scripts/xzip18.py):

| Title | Sectors on the second surface | Byte-exact |
| --- | --- | --- |
| Leather Goddesses Solid Gold | 231 | 228 |
| Border Zone | 303 | 302 |
| Beyond Zork | 630 | 630 decoded, story checksum unmatched |

The assembled Leather Goddesses story differs from the reference build in 3 blocks out of 625, plus three header bytes that genuinely differ on the disc.

### An invalid nibble is worth more than a valid one

A nibble that is not one of the 64 six-and-two bytes cannot be data, so its *position* is known.
That makes it an erasure rather than an unknown error, and a single erasure in a sector is exactly correctable: every value from it onward is off by one constant, and the trailing checksum nibble pins that constant.
Discarding such sectors - which is the obvious thing to do, and what this tool did at first - throws away most of what a marginal track has to offer, because a marginal track puts roughly one invalid nibble in each sector.

The catch is that correcting an erasure *consumes* the checksum, so the result is no longer independently verified.
Rank it below a cleanly-verified sector rather than equal to it.
Treating the two as equivalent here let corrected sectors displace good decodes from other captures and cost 11 sectors on Border Zone before the ranking was fixed.
With the ranking right, the same change added a sector on one title and cost nothing on the other, and every sector reported as checksum-verified was genuinely correct - the false positives disappeared.
The residual failures are physical, not structural - specific spots that read the same way every revolution - and the fix is more revolutions on those tracks, not more processing.
Because `--retries` only means something when a format is being decoded, and nothing here can decode this surface, use `--revs` instead: a raw read with many revolutions gives the voting more independent samples.
Independent *captures* are worth more than extra revolutions of one, and a read through the other head is worth more still - see below.

### The other head is a second opinion

A flippy's second surface can be read two ways, and they fail differently.
Flipping the disc puts it under head 0; leaving it the normal way up puts it under head 1, which on this drive sits four cylinders inward and reads the data time-reversed, since that surface was written for a flipped disc.
Reversing the interval sequence undoes exactly that, and the track numbers confirm it within seconds: reversed, 31 tracks identified themselves at 99.9% valid nibbles; unreversed, 2 did at 52%.
Nothing depends on getting the cylinder offset right, because the format records its own track number.
On Beyond Zork the head-1 read was markedly cleaner over the outer two thirds and took the recovery from 485 blocks to 522 on its own.

A closing caution on the checksum: on Border Zone, 302 of 303 sectors passed it while 297 were actually correct.
Six bits is six bits. Treat a passing sector checksum as weak evidence and verify the assembled story against the Z-machine header.

## Compare decodes as sets, not by position

Two images of the same data decoded by different formats will not line up positionally, because each applies its own sector skew.
Comparing them index by index can report zero matching sectors while the two are in fact identical.
Compare them as multisets of sectors first, then establish the track mapping.
This nearly caused a correct result to be discarded here.

## The Z-machine checksum is weak

An Infocom story file's header declares a checksum, but it is a 16-bit **byte sum** over the body.
It cannot detect a permutation, and it is far too weak to select among candidate reassemblies of a split story: searching some 80,000 of them yields about 1.2 false matches by chance, and in practice two and three false matches were found.
The sharpest discriminator is a disassembler.
Run `txd` on each candidate: the correct assembly disassembles fully - hundreds of routines over thousands of lines - while a wrong one emits nothing, or hangs outright on garbage code.
That separated four checksum-valid candidates cleanly on both Atari titles here, where a longest-common-run comparison against a known build of the same game scored all four identically and settled nothing.
Bound each run with a timeout, since a wrong candidate may not terminate.
On one title here, both checksum-valid candidates scored *below* the unrelated-game baseline and were correctly rejected.

## Story data is not always stored plainly

Whether a story file can be read straight off a decoded image varies by platform:

- **Apple II** stores story bytes plainly but paged, so byte-coverage against a reference works while a linear read does not.
- **Atari 8-bit** stores everything **inverted** (one's complement). Un-complemented, a good image shows no header, no text, and `0xFF` "fill" which is just `0x00` empty space stored inverted. Byte-coverage returns 0.0% on a side that provably contains the game until the image is complemented.
- **Commodore 64** stores data normally, in a real CBM DOS filesystem - though the directory may be vestigial, with the story body living outside it.

ZCut ([references.md](references.md)) understands all three layouts and is the practical way to extract a story file.
Verify its output independently, though: its own "Checksum good" is the byte sum described above.

## Capture size

Flux is roughly 33x the size of the decoded image, and retries multiply it.
A clean read stores about 125 KB per track; a read that fought an unreadable surface stored 746 KB per track, six times larger for the same 35 tracks.
On a surface expected to be blank or unreadable, `--retries=0` avoids the storm.
Do not drop to `--revs=1` to save space: one revolution loses exactly one sector per track, because a sector always straddles the index pulse.
`zstd -19` compresses clean flux to about 28% losslessly, and the decompressed file still decodes identically.
