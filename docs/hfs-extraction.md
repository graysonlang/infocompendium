# Extracting HFS volumes and producing modern images

Reading an HFS volume image with `hfsutils`, getting every fork and timestamp out intact, and rebuilding the contents as something current macOS mounts by double-click.
This picks up where [imaging.md](imaging.md) leaves off, with an image in hand.

## Reading the HFS volume

```
brew install hfsutils
hmount mp-full-user.img 1        # partition number optional; plain images need none
hls -l -R > listing.txt
humount
```

### The lock

hfsutils keeps mount state in `~/.hcwd` and it persists between invocations. A mount left open from an earlier command blocks the next one:

```
hmount: unable to obtain lock for medium (Resource temporarily unavailable)
```

Recovery, in order: `hvol` to see what it thinks is mounted, `humount` to release, `rm -f ~/.hcwd` if the state is stale, `lsof` on the image if something else holds it.

This is easy to loop on: you test `hmount` by hand to check it works, it succeeds and holds the lock, then a script's own `hmount` fails. `hfscopy.py` calls `humount` before mounting to break that cycle.

A second source of the same error, observed 2026-08-29: macOS itself holds an exclusive lock on any image the DiskImages framework has attached - which happens if anyone double-clicks the `.img` in Finder, even though the HFS volume inside never mounts. `lsof` on the image shows nothing. Check `hdiutil info` for the image path and `hdiutil detach` the disk it names.

### Paths starting with ":" are relative

In hfsutils path syntax, a leading colon means *relative to the current directory*; absolute paths start with the volume name (`Masterpieces:DOCS:`).
The `hls -l -R` listing prints its directory headers in the relative form (`:DOCS:`), so feeding those back to `hcd` verbatim only works while the current directory happens to be the root.
The failure mode found on real hardware: a copy loop that ran `hcd :ACRODOS:` (fine, from root), then `hcd :DOCS:` resolved *inside* ACRODOS, failed silently, and every subsequent file copy failed with "no such file or directory" - 730 of 766 files lost, while the script exited zero.
`hfscopy.py` now prefixes the volume root from `hpwd` onto every directory change, treats a failed `hcd` as a loud per-directory failure, and exits nonzero if any file failed, so the wrapper script aborts instead of packaging an almost-empty volume.

### Reading the listing format

```
f  APPL/INZ8     23047    262144 Jun 19  1996 A MIND FOREVER VOYAGING
d          4 items               Jun 15  1996 ARTHUR FOLDER
```

Columns are kind, type/creator, **resource fork size**, **data fork size**, date, name. Directory sections are introduced by a `:PATH:` header line. Filenames may contain spaces, so parse the name as everything following the date field.

## Extraction: forks matter

The critical thing: **some Mac files have a data fork of zero and live entirely in the resource fork.** On Masterpieces that includes the Arthur, Journey and Zork Zero applications. `hcopy -r` (raw, data fork only) produces empty files for those.

Use `hcopy -m` (MacBinary II) uniformly and unpack the container yourself. `scripts/hfscopy.py` does this: data fork written normally, resource fork to `path/..namedfork/rsrc`, type/creator into the `com.apple.FinderInfo` xattr, modification date from the MacBinary header.

MacBinary II header fields used:

| Offset | Bytes | Field |
| --- | --- | --- |
| 65 | 4 | file type |
| 69 | 4 | creator |
| 73 | 1 | Finder flags, high byte |
| 83 | 4 | data fork length, big endian |
| 87 | 4 | resource fork length, big endian |
| 91 | 4 | creation date, Mac epoch |
| 95 | 4 | modification date, Mac epoch |
| 101 | 1 | Finder flags, low byte |

Data fork begins at offset 128 and is padded to a 128-byte boundary; the resource fork follows.

Useful side effect: for Mac game applications that *do* have a data fork, that fork **is** the z-code story file. `hcopy -r` on those extracts a directly playable file.

## Timestamps

Creation dates are restored with `SetFile -d` from the Xcode command line tools (`os.utime` cannot set birth times). `hfscopy.py` finds `SetFile` on the PATH and warns but continues without it. Order matters on APFS: set the modification time first, then the creation date, because setting an mtime older than the current birth time silently lowers the birth time.

Directory dates come from the `hls` listing rather than MacBinary (directories have no MacBinary form), and are set in a final pass because writing a file into a folder bumps the folder's mtime. Two approximations follow: `hls` shows only a modification date, so a directory's birth time is set equal to it, and the listing is day-resolution, so directories get local midnight. Files are exact.

The restored dates are evidence in their own right: on Masterpieces they reach back to February 1988 and show 1991/1992 creation dates on Mac games modified in 1996, i.e. earlier masters reused.

## Producing a mountable modern image

`discs/masterpieces-1996/build-masterpieces.sh` runs the whole sequence for that disc: create a read/write HFS+ DMG, attach, copy via `hfscopy.py`, spot-check a known resource fork, detach, convert to compressed read-only UDZO, verify.

HFS+ is the right target. Current macOS mounts it read/write, it preserves forks and type/creator natively, and it is not going away as quickly as HFS did.

For the PC side alone, forks are irrelevant - every file under Masterpieces' `PC/` is `TEXT/mdos` with all content in the data fork - so a plain ISO is lossless and simpler:

```
hdiutil makehybrid -iso -joliet -o masterpieces-pc.iso ~/Desktop/extracted-pc
```

Joliet gets long filenames. The result mounts by double-click and works in DOSBox via `imgmount D file.iso -t iso`.

For the Mac side, note that the applications are 68k and will not run on modern macOS regardless of filesystem. Their only use is under SheepShaver or Basilisk II, and **both mount raw HFS images directly** - so the user-data image is simultaneously an archival derivative and the working copy for emulation. No conversion needed for that use case.
