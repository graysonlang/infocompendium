# The historicalsource repositories (2019)

Not a disc: this folder treats the April 2019 GitHub publication of Infocom's leaked source code (github.com/historicalsource) as a compilation and catalogs it the same way as the physical media.
The account holds 329 repositories, most of them other companies' games; the Infocom material is the 49 repositories containing ZIL source, 46 of which also carry compiled Z-machine story files.

## Contents

| File | What it is |
| --- | --- |
| `versions.md` | Release/serial table for all 70 compiled story files, cross-referenced against the disc builds |
| `checksums.txt` | Per-file git blob SHA, size, MD5 and SHA-1, so the exact bytes stay identifiable if the repositories change |

## Method

Enumerated 2026-09-03 without cloning:

1. List the account's repositories through the GitHub API and fetch each one's recursive git tree.
2. A repository is a member if its tree contains `.zil` files.
3. Candidate story files (`.z1`-`.z8`, `.zip`, `.dat` blobs above 20 KB) are downloaded by blob SHA and validated by z-code header: version byte 1-8, printable serial, plausible length. Interpreter binaries and data tables fail this and drop out.
4. Duplicate paths pointing at one blob (most repos ship `COMPILED/x.z3` plus an `x.zip` twin) collapse to one entry via the blob SHA.
5. Release and serial come from the z-code header; the built-in-hints test and the cross-referencing against the disc builds work exactly as described in the disc folders' `versions.md` files.

Because everything is keyed to git blob SHAs, any claim here can be re-verified against a clone with `git cat-file blob <sha>` even after the repositories move or rewrite history.
