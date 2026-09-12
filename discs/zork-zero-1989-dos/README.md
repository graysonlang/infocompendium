# Zork Zero, MS-DOS retail release (Infocom, 1989)

Disc-specific material for archiving the dual-media MS-DOS retail box: two 720K 3.5" diskettes and three 5.25" diskettes.
The catalog's first floppy entry.
No disc content lives in this folder - only identification records, listings, notes.

## Contents

| File | What it is |
| --- | --- |
| `zork-zero-1989-dos.ls.txt` | File listings of the 3.5" diskettes |
| `notes.md` | Per-release findings, including the media-targeted graphics renditions |
| `checksums.txt` | Reference hashes for raw images of the 3.5" diskettes |

## Archiving your own copy

USB 3.5" floppy drives mount on modern macOS, but `dd` against the device fails: unlike optical drives, the floppy's device node stays root-owned.
`hdiutil` reads it through a privileged helper instead:

```
diskutil unmountDisk /dev/diskN
hdiutil create -srcdevice /dev/diskN -format UDRO disk1.dmg
hdiutil convert disk1.dmg -format UDTO -o disk1    # produces disk1.cdr
mv disk1.cdr disk1.img                             # raw 737,280-byte image
```

Compare against [checksums.txt](checksums.txt).
The 5.25" diskettes need flux-level hardware (a Greaseweazle or similar); their reference hashes will follow once captured.
