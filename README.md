# infocom-disc-preservation

Tooling and notes for imaging and extracting 1990s hybrid CD-ROMs, with a focus on the Activision Infocom compilations.

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
  knowledge-transfer.md   Method, pitfalls, and per-disc findings. Read this first.
scripts/
  hfscopy.py              Walks an HFS volume and copies it out preserving forks and metadata.
  build-masterpieces.sh   End-to-end wrapper: create HFS+ DMG, copy, verify, compress.
```

## Quick start

Prerequisites:

```
brew install hfsutils
```

Given an HFS slice image already dumped from the disc:

```
./scripts/build-masterpieces.sh ~/Desktop/mp-hfs.img
```

That produces `~/Desktop/masterpieces.dmg`, a compressed read-only HFS+ image with resource forks, type/creator codes, and modification dates intact.

If you are starting from a physical disc, read `docs/knowledge-transfer.md` first.
The imaging step has several traps that will silently produce a file full of zeros.

## Principles

Keep the raw sector image as the archival artifact and never modify it.
Everything else in this repo produces derivatives - convenience copies for browsing and emulation.
A derivative that has been re-catalogued will not hash against Redump, and that is fine, as long as the original is still around to verify against.
