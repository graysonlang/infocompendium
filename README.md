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
| Classic Text Adventure Masterpieces of Infocom (1996) | partial | in progress | Slice dump works; full-disc dump blocked by drive block-size reporting |
| The Lost Treasures of Infocom (CD) | no | no | |
| The Lost Treasures of Infocom II (CD) | no | no | |
| The Zork Anthology (1994) | no | no | |

## Layout

```
docs/
  knowledge-transfer.md          Method and pitfalls, disc-agnostic. Read this first.
scripts/
  hfscopy.py                     Walks an HFS volume and copies it out preserving forks and metadata.
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

If you are starting from a physical disc, read `docs/knowledge-transfer.md` first.
The imaging step has several traps that will silently produce a file full of zeros.

## Principles

Keep the raw sector image as the archival artifact and never modify it.
Everything else in this repo produces derivatives - convenience copies for browsing and emulation.
A derivative that has been re-catalogued will not hash against Redump, and that is fine, as long as the original is still around to verify against.
