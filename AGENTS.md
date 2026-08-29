# Agent instructions

## Markdown

Do not hard-wrap paragraphs to a fixed column. The renderer re-wraps, so a fixed width only makes diffs noisy. Break lines at sentence or phrase boundaries instead - that is where edits land, so it plays nicely with source control. Applies to every `.md` in the repo except `LICENSE.md`.

The same rule governs prose inside HTML content: keep each sentence or phrase on its own line. The browser re-wraps it anyway.

## Source character set

Source code stays 7-bit ASCII (bytes 0x00-0x7F), comments and string literals included. No em-dash, en-dash, arrows, multiplication signs, check marks, or smart quotes. Use the low-ASCII equivalent: ` - `, `-`, `->`, `x`, straight quotes.

This governs source files. Markdown prose may use non-ASCII freely.

## Python scripts

Start every script with `import sys` followed by `sys.dont_write_bytecode = True`, before the other imports, so no `.pyc` files are created.

## Shell scripts

Use `set -euo pipefail`. Quote every variable expansion. Never write a destructive command that can run without an explicit path argument.

Resolve a script's own directory as `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" >/dev/null 2>&1 && pwd -P)"` - the `:-$0` fallback and `pwd -P` make it survive `sh` invocation and symlinked paths.

Scripts must refuse to overwrite existing output files rather than clobbering silently. Disc images take minutes to produce and hours to re-source if the disc is damaged in the meantime.

## Working with disc images

Never modify a raw sector image in place. Treat `*-hfs.img`, `*.iso`, and any full-disc dump as read-only inputs. Derivatives go to new filenames.

Do not add image files to source control. They are hundreds of megabytes and some of the content is still under copyright. `.gitignore` covers the usual extensions; extend it rather than making exceptions.

## Verifying rather than assuming

This repo exists because several plausible-sounding assumptions turned out to be wrong on real hardware. When a command fails, read the actual error before proposing a fix.

Specific habits that matter here:

- Do not use `capture_output=True` or `2>/dev/null` on a command whose failure you are trying to diagnose. Both have already cost debugging time on this project.
- After any `dd`, check the output size and hexdump the head before proceeding. A zero-filled image looks like a successful run.
- When a claim about a disc's contents can be checked against the disc, check it. Published catalogues of these compilations contain errors and omissions, several of which this repo has already documented.

## Testing

The scripts touch real hardware and real disk images, so they cannot be fully tested in isolation. Where logic can be separated from I/O, separate it: `hfscopy.py` parses a captured listing independently of any mount, and `--dry-run` exercises that path against a saved `hls -l -R` capture with no disc present.

Each disc folder under `discs/` keeps a saved `hls -l -R` listing; add one when adding support for a new disc, so the parser can be regression-tested without the physical media (e.g. `python3 scripts/hfscopy.py --listing discs/masterpieces-1996/masterpieces-1996.hls.txt --dry-run`).
