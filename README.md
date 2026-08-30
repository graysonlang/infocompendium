# infocompendium

Tooling and notes for imaging and extracting 1990s hybrid CD-ROMs, with a focus on the Activision Infocom compilations.

The repo serves two purposes:

- Source material for filling gaps in the shared public knowledge of the Infocom catalog and related assets. Per-disc notes record what a physical pressing actually contains, including where it contradicts the published references.
- A mechanism for people to archive their own media. Each disc folder documents how to image and verify that specific disc, and the shared scripts do the extraction.

No disc content is stored here - only identification records, catalog listings, notes, and tooling.

These discs carry two filesystems over one set of data blocks: ISO 9660 for the PC side and HFS for the Mac side.
macOS dropped HFS support in Ventura, so modern Macs can identify these discs but refuse to mount them.
The scripts here work around that: image the disc at sector level, read the HFS volume with `hfsutils`, and rebuild the contents as an HFS+ disk image that current macOS mounts by double-click.

## Status

| Disc | Imaged | Extracted | Notes |
| --- | --- | --- | --- |
| [Classic Text Adventure Masterpieces of Infocom (1996)](discs/masterpieces-1996/README.md) | yes | yes | Full raw dump hash-matches the Redump database entry; extraction verified, 766 files with all resource forks |
| The Lost Treasures of Infocom (CD) | no | no | |
| The Lost Treasures of Infocom II (CD) | no | no | |
| [The Zork Anthology (1994)](discs/zork-anthology-1994/README.md) | yes | no | Redump-verified; games live inside the ZORKANTH.RED installer archive |
| [Return to Zork / The Zork Anthology (Zork Legacy Collection, 1997)](discs/zork-legacy-1997-rtz-anthology/README.md) | yes | no | Redump-verified on all 26 tracks (data plus 25 audio); anthology games as loose files |
| [GET LAMP (2010), disc 2](discs/get-lamp-2010-disc2/README.md) | yes (from existing rip) | n/a | Bonus DVD: Infocom catalog/ad scans, curated IF games |

## Findings

What each disc actually contains, checked against the published references:

- [Masterpieces (1996)](discs/masterpieces-1996/notes.md) - the Leather Goddesses boss key survives, Lurking Horror sound on the PC side, real save files with the copy-protection credentials in them, and more. The pressing is Redump-verified, so these describe the reference disc, not a variant.
- [The Zork Anthology (1994)](discs/zork-anthology-1994/notes.md) - an installer disc where the five classic games occupy 1.3 MB of 246 MB, the rest being Return to Zork and demos, including a 1994 demo of the cancelled Planetfall sequel under the title "Floyd Strikes Back".
- [Return to Zork / The Zork Anthology (1997)](discs/zork-legacy-1997-rtz-anthology/notes.md) - a mixed-mode disc verified against Redump on all 26 tracks; its anthology files are byte-identical to Masterpieces' PC builds, and its Windows installer archive quietly carries the story files of fourteen Infocom games the product never advertises.

The disc-agnostic method lives in [docs/](docs/identifying-discs.md): [what these discs are and how to identify them](docs/identifying-discs.md), [the imaging traps and what works](docs/imaging.md), and [extracting HFS volumes into modern images](docs/hfs-extraction.md), plus the [external references](docs/references.md).

## Layout

```
docs/
  identifying-discs.md           Hybrid discs, why macOS refuses them, identification. Start here.
  imaging.md                     The imaging traps and the working raw-dump method.
  hfs-extraction.md              hfsutils, forks, timestamps, building mountable images.
  references.md                  External references: Doherty, Plotkin, ztools, Redump.
scripts/
  hfscopy.py                     Walks an HFS volume and copies it out preserving forks and metadata.
  raw2user.py                    Converts a raw 2352-byte/sector dump to 2048-byte user data,
                                 verifying sector structure and printing Redump-style hashes.
  picdir.py                      Lists the image directory of an Infocom V6 picture library
                                 (PC .CG1/.EG1/.MG1, Mac PIC.DATA), either byte order.
  get-ztools.sh                  Fetches and builds ztools (txd, infodump, pix2gif, check)
                                 from the IF Archive into tools/ztools/ (gitignored).
  splittracks.py                 Splits a raw dump of a mixed-mode disc into per-track files
                                 at Redump's boundaries, hashing each track.
  isz.py                         Lists and extracts InstallShield 3 .Z archives (PKWARE DCL
                                 decoder included), as found on 1990s Windows installer discs.
discs/
  masterpieces-1996/             One folder per disc: identification capture, catalog
    README.md                    listing, findings, and disc-specific build scripts.
    disc-info.txt                No disc content, just the material needed to archive
    masterpieces-1996.hls.txt    and verify a copy.
    notes.md
    build-masterpieces.sh
```

## Quick start

Prerequisites:

```
brew install hfsutils
```

Given an HFS slice image already dumped from the disc:

```
./discs/masterpieces-1996/build-masterpieces.sh ~/Desktop/mp-hfs.img
```

That produces `~/Desktop/masterpieces.dmg`, a compressed read-only HFS+ image with resource forks, type/creator codes, and modification dates intact.

If you are starting from a physical disc, read [docs/imaging.md](docs/imaging.md) first - the imaging step has several traps that will silently produce a file full of zeros - then follow the per-disc steps in that disc's README, e.g. [Masterpieces](discs/masterpieces-1996/README.md).

## Principles

Keep the raw sector image as the archival artifact and never modify it.
Everything else in this repo produces derivatives - convenience copies for browsing and emulation.
A derivative that has been re-cataloged will not hash against Redump, and that is fine, as long as the original is still around to verify against.
