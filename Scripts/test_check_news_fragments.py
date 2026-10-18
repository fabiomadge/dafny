"""Tests for `check_news_fragments.py`."""

import subprocess
import sys
import tempfile
import unittest

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_news_fragments import find_problems  # pylint: disable=wrong-import-position

class FindProblemsTest(unittest.TestCase):
    def find_problems_in_repo_with(self, *paths: str):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for path in paths:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_text("A note.\n", encoding="utf-8")
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(["git", "add", "--all"], cwd=root, check=True)
            return find_problems(root)

    def test_well_placed_notes_pass(self) -> None:
        self.assertEqual(self.find_problems_in_repo_with(
            "docs/dev/news/1234.fix", "docs/dev/news/some-feature.feat",
            "docs/dev/news/.gitignore", "Source/break.dfy"), ([], []))

    def test_notes_outside_docs_dev_news_are_misplaced(self) -> None:
        notes = ["docs/dev/1234.feat", "docs/dev/news/old/1234.break",
                 "docs/news/1234.fix", "docs/news/fix.1234"]
        self.assertEqual(self.find_problems_in_repo_with(*notes)[0], notes)

    def test_kind_first_name_in_docs_dev_news_is_misnamed(self) -> None:
        self.assertEqual(self.find_problems_in_repo_with("docs/dev/news/fix.1234"),
                         ([], ["fix.1234"]))

if __name__ == "__main__":
    unittest.main()
