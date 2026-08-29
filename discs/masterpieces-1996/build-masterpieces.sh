#!/bin/bash
#
# build-masterpieces.sh -- turn an HFS disk image into a modern,
# mountable HFS+ .dmg with resource forks and metadata intact.
#
#   ./build-masterpieces.sh ~/Desktop/mp-hfs.img
#
set -euo pipefail

SRC_IMG="${1:-$HOME/Desktop/mp-hfs.img}"
VOLNAME="Masterpieces"
WORKDIR="$HOME/Desktop"
RW_DMG="$WORKDIR/masterpieces-rw.dmg"
FINAL_DMG="$WORKDIR/masterpieces.dmg"
SIZE="420m"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" >/dev/null 2>&1 && pwd -P)"
# Shared tooling lives at the repo root; this script is disc-specific.
HFSCOPY="$SCRIPT_DIR/../../scripts/hfscopy.py"

echo "==> checking prerequisites"
[ -f "$SRC_IMG" ] || { echo "source image not found: $SRC_IMG"; exit 1; }
command -v hmount >/dev/null || { echo "hfsutils missing -- run: brew install hfsutils"; exit 1; }
command -v python3 >/dev/null || { echo "python3 missing"; exit 1; }
[ -f "$HFSCOPY" ] || { echo "hfscopy.py not found at $HFSCOPY"; exit 1; }

# Refuse to clobber silently.
for f in "$RW_DMG" "$FINAL_DMG"; do
    [ -e "$f" ] && { echo "already exists, move it aside first: $f"; exit 1; }
done

echo "==> creating read/write HFS+ image ($SIZE)"
hdiutil create -size "$SIZE" -fs "HFS+" -volname "$VOLNAME" -type UDIF "$RW_DMG"

echo "==> attaching"
MOUNTPOINT=$(hdiutil attach "$RW_DMG" -nobrowse | grep -oE '/Volumes/.*' | head -1)
[ -n "$MOUNTPOINT" ] || { echo "attach failed"; exit 1; }
echo "    mounted at $MOUNTPOINT"

cleanup() {
    if mount | grep -q "$MOUNTPOINT"; then
        echo "==> detaching (cleanup)"
        hdiutil detach "$MOUNTPOINT" -force >/dev/null 2>&1 || true
    fi
}
trap cleanup EXIT

echo "==> copying contents (this walks ~766 files; a few minutes)"
python3 "$HFSCOPY" --image "$SRC_IMG" --dest "$MOUNTPOINT"

echo "==> spot-checking resource forks"
PROBE="$MOUNTPOINT/MAC/ARTHUR FOLDER/ARTHUR"
if [ -f "$PROBE" ]; then
    RSRC=$(ls -l "$PROBE/..namedfork/rsrc" 2>/dev/null | awk '{print $5}')
    echo "    ARTHUR resource fork: ${RSRC:-MISSING} bytes (expect 43798)"
    xattr -l "$PROBE" | head -2 || true
else
    echo "    WARNING: probe file not found"
fi

echo "==> detaching"
hdiutil detach "$MOUNTPOINT"
trap - EXIT

echo "==> converting to compressed read-only image"
hdiutil convert "$RW_DMG" -format UDZO -o "$FINAL_DMG"

echo "==> verifying"
hdiutil verify "$FINAL_DMG"

echo
echo "done."
echo "  source image (keep, do not modify): $SRC_IMG"
echo "  working, double-clickable:          $FINAL_DMG"
echo "  scratch r/w copy:                   $RW_DMG   (delete once happy)"
echo "The archival artifact is the raw sector dump the source image came from; keep that above all."
