# Zork Zero, MS-DOS retail release (1989) - findings

The catalog's first floppy entry: an original dual-media retail box - two 720K 3.5" diskettes and three 5.25" diskettes - examined and partially imaged 2026-09-12.
The 3.5" side is captured and hashed ([checksums.txt](checksums.txt)); the 5.25" side awaits flux-imaging hardware.

## Contents of the 3.5" diskettes

See [zork-zero-1989-dos.ls.txt](zork-zero-1989-dos.ls.txt) for the full listings.

- **Disk 1** (`ZORK0 1`): `ZORK0.ZIP` (r393.890714), `ZORKZERO.EXE` (interpreter, 47,494 bytes), `ZORK0.MG1` (the MCGA graphics, 226,436 bytes, 1989-07-10 11:35 - matching Doherty's documented timestamp to the minute), `INSTALL.EXE`, `IZORK03.RUN`, `EZR.EXE`.
- **Disk 2** (`ZORK0 2`): `ZORK0.CG1` alone, 244,507 bytes, with some 476K of the diskette unused.

There is **no `ZORK0.EG1` on the 3.5" set**.

## Findings

- **The MG1 provenance question is closed.** This box's `ZORK0.MG1` is byte-identical to the IF Archive's `zorkzero.mg1`, uploaded 1994-05-16 to patch the Lost Treasures omission. The archive's copy is the retail 3.5" edition's file; see [docs/media-assets.md](../../docs/media-assets.md) for the full chain.
- **The compilations' Zork Zero traces to these diskettes.** `ZORK0.ZIP`, `ZORKZERO.EXE` and `ZORK0.CG1` are byte-identical to the copies on the 1992 Lost Treasures CD and everything downstream of it. The CD lineage (1992 -> 1994 -> 1996 -> 1997) now begins at physical retail floppies.
- **The graphics renditions were media-targeted.** The 3.5" set carries MCGA plus the CGA fallback but no EGA file - and not for lack of room, since EG1 (333,654 bytes) would fit disk 2's free space. On the 5.25" side the arithmetic runs the other way: three 360K diskettes (1,087,488 bytes) can hold the game with EGA and CGA, but adding the MG1 would force a fourth diskette. So each media format shipped the renditions matching its buyer's likely hardware - 3.5" for PS/2-class MCGA machines, 5.25" for the older EGA installed base, CGA as the universal fallback - the same policy Graeme Cree describes for Journey's dual-media box, where the VGA rendition rode only the 3.5" diskettes.

## Open items for this disc

- Image the three 5.25" diskettes at flux level once the controller (Greaseweazle V4.1, on order) arrives.
  Prediction on record: they hold the same `ZORK0.ZIP`/`ZORKZERO.EXE`/installer set plus `ZORK0.EG1` and `ZORK0.CG1`, and no `ZORK0.MG1`.
