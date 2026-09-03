# GET LAMP (2010), disc 2 - findings

From the mounted image; see [disc-info.txt](disc-info.txt) for provenance.
Volume `GETLAMP`, UDF + ISO 9660 bridge, all content dated 2010-07-15.
7,617,241,088 bytes (dual-layer DVD), 799 listing lines; see [get-lamp-2010-disc2.ls.txt](get-lamp-2010-disc2.ls.txt).

## Structure

A hybrid DVD-Video/data disc.
`VIDEO_TS`/`AUDIO_TS`/`JACKET_P` hold the disc-2 documentary video content; the data side holds the bonus material:

- `games/` - a curated collection of 41 modern IF games with a `README.txt` crediting each author (Plotkin, Short, Montfort, Granade, Sherwin, Sousa, and others). Playable-with-permission copies, not Infocom material.
- `interpreters/` - `gargoyle` and `splatterlight` interpreter builds for playing them.
- `eamon/` - `EAG_90F.rar`, an Eamon Adventurer's Guild collection.
- `photos/infocom-ads/` - **38 scans of Infocom advertisements and catalogs, including the 1983-1987 product catalogs** (`1983Catalog.bmp` through `1987Catalog.bmp`, rear covers and interior pages, plus individual game ads: Deadline, Hitchhiker's, Cornerstone, and more). The most catalog-relevant material on the disc.
- `photos/bedquiltvideo/`, `audio/` - Colossal Cave-adjacent material, including "The Death of Floyd Collins" ballad and an "eyes and hands" recording with transcript.
- `production/` - production photos of the famous Get Lamp coin (proof, prototypes, bag) and the cover painting's drafts (`marc1.jpg`/`marc2.jpg` - Marc Ericksen's sketches through final).
- `video/` - trailer, MC Frontalot "It Is Pitch Dark" HD video, BBS documentary promo, and other shorts.

## Findings

- The `photos/infocom-ads/` catalog scans overlap this repo's mission directly: five year-complete Infocom catalogs (1983-1987) in uncompressed BMP, likely scanned for the documentary and not all mirrored elsewhere.
- Redump has no Get Lamp entry (checked 2026-08-29), so [checksums.txt](checksums.txt) stands as an independent reference for this pressing until one exists.
- **The image verifies against the Internet Archive's published copy.** The IA item `GET_LAMP_The_Text_Adventure_Documentary` carries both discs as ISO+MDS rips, and this rip plus 8,192 trailing zero bytes (four empty sectors, a rip-length convention difference) hashes byte-identical to IA's disc 2 ISO (md5 `39eb095aa3fc79159be84bd5601f66b3`). Established 2026-09-03; the closest thing to a Redump match this disc currently has.
- **The `infocom-ads` scans exist publicly only inside that ISO.** The IF Archive's `infocom/adverts/` directory (checked 2026-09-03) is a different, smaller corpus - other scans of other ads, JPEG/PNG/PDF, no overlap with this disc's 38 BMP files by name or content type. Nobody has published the disc's ad and catalog scans as individual files; anyone wanting the 1983-1987 catalog BMPs must extract them from a disc image.

## Open items for this disc

- Disc 1 of the set is not yet imaged from physical media. The IA item above carries a reference ISO for it (8,153,104,384 bytes, md5 `50ad27c56bcca22a9a86aaaa202c11dc`, sha1 `a9a68e986d136d2ec378f3bfbb3fb61562265c6b`) to verify any future dump against.

Resolved 2026-09-03: the `infocom-ads` comparison; see the findings above.
