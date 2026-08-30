# GET LAMP (2010), disc 2

Disc-specific material for Jason Scott's *GET LAMP: The Text Adventure Documentary*, second disc of the two-DVD set - the bonus disc.
No disc content lives in this folder - only identification records, listings, notes.

This one arrived as an existing image (`GETLAMP.cdr`, a raw UDTO rip - 2048-byte sectors, byte-identical to an `.iso`) rather than physical media, so there is no `drutil` capture; [disc-info.txt](disc-info.txt) records `hdiutil imageinfo` instead.

## Contents

| File | What it is |
| --- | --- |
| `disc-info.txt` | `hdiutil imageinfo` output and mount details for the image |
| `get-lamp-2010-disc2.ls.txt` | Recursive listing of the mounted volume |
| `notes.md` | Per-disc findings |
| `checksums.txt` | Reference hashes of the image |

## Working with the image

It is a hybrid DVD-Video/data disc (UDF + ISO 9660 bridge, volume `GETLAMP`).
macOS mounts it by double-click, or:

```
hdiutil attach -readonly GETLAMP.cdr
```

Always attach read-only; the image is the archival artifact.
Renaming a copy to `.iso` makes it usable anywhere an ISO is expected.
