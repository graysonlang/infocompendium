# infocompendium

Tooling and notes for imaging and extracting 1990s hybrid CD-ROMs, with a focus on the Activision Infocom compilations.

The repo serves two purposes:

- Source material for filling gaps in the shared public knowledge of the Infocom catalogue and related assets. Per-disc notes record what a physical pressing actually contains, including where it contradicts the published references.
- A mechanism for people to archive their own media. Each disc folder documents how to image and verify that specific disc, and the shared scripts do the extraction.

No disc content is stored here - only identification records, catalogue listings, notes, and tooling.

These discs carry two filesystems over one set of data blocks: ISO 9660 for the PC side and HFS for the Mac side.
macOS dropped HFS support in Ventura, so modern Macs can identify these discs but refuse to mount them.
The scripts here work around that: image the disc at sector level, read the HFS volume with `hfsutils`, and rebuild the contents as an HFS+ disk image that current macOS mounts by double-click.

## Status

| Disc | Imaged | Extracted | Notes |
| --- | --- | --- | --- |
| [Classic Text Adventure Masterpieces of Infocom (1996)](discs/masterpieces-1996/README.md) | yes | yes | Full raw dump hash-matches the Redump database entry; extraction verified, 766 files with all resource forks |
| The Lost Treasures of Infocom (CD) | no | no | |
| The Lost Treasures of Infocom II (CD) | no | no | |
| The Zork Anthology (1994) | no | no | |

## Findings

What each disc actually contains, checked against the published references:

- [Masterpieces (1996)](discs/masterpieces-1996/notes.md) - the Leather Goddesses boss key survives, Lurking Horror sound on the PC side, real save files with the copy-protection credentials in them, and more. The pressing is Redump-verified, so these describe the reference disc, not a variant.

The disc-agnostic method - what a hybrid disc is, why macOS fights you, and the imaging traps - is in [docs/knowledge-transfer.md](docs/knowledge-transfer.md).

## Layout

```
docs/
  knowledge-transfer.md          Method and pitfalls, disc-agnostic. Read this first.
scripts/
  hfscopy.py                     Walks an HFS volume and copies it out preserving forks and metadata.
  raw2user.py                    Converts a raw 2352-byte/sector dump to 2048-byte user data,
                                 verifying sector structure and printing Redump-style hashes.
  picdir.py                      Lists the image directory of an Infocom V6 picture library
                                 (PC .CG1/.EG1/.MG1, Mac PIC.DATA), either byte order.
  get-ztools.sh                  Fetches and builds ztools (txd, infodump, pix2gif, check)
                                 from the IF Archive into tools/ztools/ (gitignored).
discs/
  masterpieces-1996/             One folder per disc: identification capture, catalogue
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

If you are starting from a physical disc, read [docs/knowledge-transfer.md](docs/knowledge-transfer.md) first - the imaging step has several traps that will silently produce a file full of zeros - then follow the per-disc steps in that disc's README, e.g. [Masterpieces](discs/masterpieces-1996/README.md).

## Principles

Keep the raw sector image as the archival artifact and never modify it.
Everything else in this repo produces derivatives - convenience copies for browsing and emulation.
A derivative that has been re-catalogued will not hash against Redump, and that is fine, as long as the original is still around to verify against.
