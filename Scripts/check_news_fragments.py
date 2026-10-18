#!/usr/bin/env python3
"""Fail if a release note is somewhere `prepare_release.py` never reads, or is named
so that `prepare_release.py` refuses to release."""

import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare_release import NewsFragments, Release  # pylint: disable=wrong-import-position

NEWS = Path(Release.NEWSFRAGMENTS_PATH)
KINDS = sorted(ext.lstrip(".") for ext in NewsFragments.KNOWN_EXTENSIONS)
KIND_FIRST = re.compile(rf"({'|'.join(KINDS)})\.[0-9]+")

def find_problems(root: Path) -> Tuple[List[str], List[str]]:
    """Tracked notes outside `NEWS`, and the files in `NEWS` that are not notes."""
    files = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True,
                           check=True, encoding="utf-8").stdout.split("\0")
    misplaced = [f for f in files if f and Path(f).parent != NEWS
                 and (Path(f).suffix in NewsFragments.KNOWN_EXTENSIONS
                      or KIND_FIRST.fullmatch(Path(f).name))]
    misnamed = sorted(p.name for p in NewsFragments.from_directory(str(root / NEWS)).unrecognized)
    return misplaced, misnamed

def main() -> None:
    misplaced, misnamed = find_problems(Path(__file__).resolve().parent.parent)
    if misplaced:
        print(f"Move these release notes to {NEWS}/, the only directory the release reads:",
              *misplaced, sep="\n  ", file=sys.stderr)
    if misnamed:
        print(f"Rename these files in {NEWS}/ to <issue>.<kind>, <PR>.<kind> or"
              f" <description>.<kind>, where <kind> is {', '.join(KINDS)}:",
              *misnamed, sep="\n  ", file=sys.stderr)
    sys.exit(1 if misplaced or misnamed else 0)

if __name__ == "__main__":
    main()
