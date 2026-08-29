#!/bin/bash
#
# get-ztools.sh -- fetch and build ztools (Mark Howell's Infocom tools)
# from the IF Archive: txd (z-code disassembler), infodump (story file
# inspector), pix2gif (picture extractor), check.
#
# Everything lands in tools/ztools/ at the repo root (gitignored).
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" >/dev/null 2>&1 && pwd -P)"
DEST="$SCRIPT_DIR/../tools/ztools"
URL="https://ifarchive.org/if-archive/infocom/tools/ztools/ztools731.tar.gz"
TARBALL="ztools731.tar.gz"
BINARIES="txd infodump pix2gif check"

mkdir -p "$DEST"
cd "$DEST"

ALL_PRESENT=yes
for b in $BINARIES; do
    [ -x "$b" ] || ALL_PRESENT=no
done
if [ "$ALL_PRESENT" = yes ]; then
    echo "already built in $DEST -- delete the directory to force a rebuild"
    exit 0
fi

if [ ! -f "$TARBALL" ]; then
    echo "==> downloading $URL"
    curl -sSfL -o "$TARBALL" "$URL"
fi

# A failed fetch can leave an HTML error page with a .tar.gz name.
if ! gzip -t "$TARBALL" 2>/dev/null; then
    echo "downloaded file is not a gzip archive (error page?); inspect $DEST/$TARBALL" >&2
    exit 1
fi

# The tarball has no top-level directory; it extracts flat.
echo "==> unpacking"
tar xzf "$TARBALL"

# Vintage C: implicit ints need a pre-C99 dialect.
echo "==> building"
make -s check infodump pix2gif txd CFLAGS="-O2 -w -std=gnu89"

echo "==> smoke test"
for b in $BINARIES; do
    [ -x "$b" ] || { echo "build produced no $b" >&2; exit 1; }
done
"./txd" 2>&1 | head -2 || true

echo "done. binaries in $DEST"
