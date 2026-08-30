#!/usr/bin/env python3
"""Check that release notes are where the release script will find them.

A note outside `NEWSFRAGMENTS_PATH` is silently dropped; one inside it but misnamed
aborts the release. Names only, no `git log`, so a shallow clone gives the same
answer. Run with `make news-check`.
"""

import os
import subprocess
import sys

from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent))

# pylint: disable=wrong-import-position
from prepare_release import NewsFragments, Release

CANONICAL = Path(Release.NEWSFRAGMENTS_PATH)
KINDS = {ext.lstrip(".") for ext in NewsFragments.KNOWN_EXTENSIONS}

def looks_like_a_fragment(name: str) -> bool:
    """Whether `name` is a release note, under either name order.

    `Path("fix.3809").suffix` is `".3809"`, so an extension test alone would miss the
    reversed form. It has to end in digits, so that `fix.py` is not a release note.
    """
    parts = name.split(".")
    if len(parts) < 2:
        return False
    return parts[-1] in KINDS or (parts[0] in KINDS and parts[-1].isdigit())

def repo_root() -> Path:
    try:
        proc = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                              capture_output=True, check=True, encoding="utf-8")
    except (OSError, subprocess.CalledProcessError) as e:
        sys.exit(f"Could not locate the root of the repository: {e}")
    return Path(proc.stdout.strip())

def unclassifiable_fragments() -> List[str]:
    """Names in `CANONICAL` that `NewsFragments._read_directory` would reject."""
    if not CANONICAL.is_dir():
        return []
    return sorted(p.name for p in CANONICAL.iterdir()
                  if p.suffix not in NewsFragments.KNOWN_EXTENSIONS
                  and p.name not in NewsFragments.IGNORED)

def stray_fragments() -> List[str]:
    """Release notes anywhere in the tree other than `CANONICAL`.

    Two passes: `--ignored` is the only way to see a note `.gitignore` hides
    (`.gitignore:72-74` hides `docs/dev/*.fix`), and it reports nothing else.
    """
    strays = set()
    for selection in (["--cached", "--others"], ["--others", "--ignored"]):
        proc = subprocess.run(["git", "ls-files", "-z", "--full-name",
                               "--exclude-standard", *selection],
                              capture_output=True, check=True, encoding="utf-8")
        strays.update(path for path in proc.stdout.split("\0")
                      if path and Path(path).parent != CANONICAL
                      and looks_like_a_fragment(Path(path).name))
    return sorted(strays)

def main() -> None:
    os.chdir(repo_root())
    problems = []

    if strays := stray_fragments():
        problems.append(
            f"These release notes are not in `{CANONICAL}`, so the release script "
            f"will never see them:\n" + "".join(f"  {s}\n" for s in strays)
            + f"Move them into `{CANONICAL}`.")

    if bad := unclassifiable_fragments():
        kinds = ", ".join(sorted(NewsFragments.KNOWN_EXTENSIONS))
        problems.append(
            f"These files in `{CANONICAL}` cannot be classified and would abort "
            f"the next release:\n" + "".join(f"  {b}\n" for b in bad)
            + f"The kind comes last: `<PR or issue number>.<kind>` (e.g. `1234.fix`)"
            f" or `<description>.<kind>`, where `<kind>` is one of {kinds}."
            f" See docs/dev/README.md.")

    if problems:
        print("\n\n".join(problems), file=sys.stderr)
        sys.exit(1)
    print(f"All release notes are in {CANONICAL} and correctly named.")

if __name__ == "__main__":
    main()
