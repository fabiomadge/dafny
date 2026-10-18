"""Tests for `prepare_release.py`, run in a throwaway repository shaped like this one."""

import os
import subprocess
import sys
import tempfile
import unittest

from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prepare_release  # pylint: disable=wrong-import-position
from prepare_release import Release  # pylint: disable=wrong-import-position

BUILD_PROPS = """<Project>
  <PropertyGroup>
    <VersionPrefix>4.11.0</VersionPrefix>
  </PropertyGroup>
</Project>
"""

def git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, check=True,
                          encoding="utf-8").stdout.strip()

class ReleaseTest(unittest.TestCase):
    def setUp(self) -> None:
        # Ignore the developer's own git configuration.
        environ = mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"})
        environ.start()
        self.addCleanup(environ.stop)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.repo = self.tmp / "dafny"
        (self.repo / "Source").mkdir(parents=True)
        (self.repo / Release.NEWSFRAGMENTS_PATH).mkdir(parents=True)
        self.build_props = self.repo / "Source/Directory.Build.props"
        self.build_props.write_text(BUILD_PROPS, encoding="utf-8")
        self.release_notes = self.repo / "RELEASE_NOTES.md"
        self.release_notes.write_text(f"# Upcoming\n\n{Release.RELEASE_NOTES_MARKER}\n\n# 4.11.0\n",
                                      encoding="utf-8")
        self.write_note("README.md", "# Latest Dafny changes")
        self.write_note("1234.fix", "Fix the thing")

        git("init", "--quiet", "--initial-branch=master", cwd=self.repo)
        git("config", "user.name", "Dafny Test", cwd=self.repo)
        git("config", "user.email", "test@example.com", cwd=self.repo)
        self.commit("Initial commit (#1000)")

        # `Release` resolves its paths against the working directory.
        self.addCleanup(os.chdir, os.getcwd())
        os.chdir(self.repo)

    def write_note(self, name: str, contents: str) -> None:
        (self.repo / Release.NEWSFRAGMENTS_PATH / name).write_text(contents + "\n", encoding="utf-8")

    def commit(self, message: str) -> None:
        git("add", "--all", cwd=self.repo)
        git("commit", "--quiet", f"--message={message}", cwd=self.repo)

    def offline(self) -> None:
        """Stub the two checks that need the network."""
        for name in ("_head_up_to_date", "_no_release_blocking_issues"):
            patcher = mock.patch.object(Release, name, return_value=True)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_prepare_commits_the_release_notes_on_a_release_branch(self) -> None:
        self.offline()
        with mock.patch.object(Release, "_push_release_branch"):
            Release("4.12.0", "master").prepare()

        self.assertEqual(git("branch", "--show-current", cwd=self.repo), "release-4.12.0")
        self.assertEqual(git("status", "--porcelain", cwd=self.repo), "")
        self.assertIn("<VersionPrefix>4.12.0</VersionPrefix>", self.build_props.read_text(encoding="utf-8"))
        self.assertEqual(self.release_notes.read_text(encoding="utf-8"),
                         f"# Upcoming\n\n{Release.RELEASE_NOTES_MARKER}\n\n# 4.12.0\n\n## Bug fixes\n\n"
                         "- Fix the thing (https://github.com/dafny-lang/dafny/pull/1234)\n\n# 4.11.0\n")
        self.assertEqual(os.listdir(Release.NEWSFRAGMENTS_PATH), ["README.md"])

    def test_prepare_refuses_a_note_outside_docs_dev_news(self) -> None:
        self.offline()
        (self.repo / "docs/news").mkdir()
        (self.repo / "docs/news/1235.fix").write_text("Fix a third thing\n", encoding="utf-8")
        self.commit("A misplaced note (#1235)")

        with self.assertRaises(prepare_release.CannotReleaseError):
            Release("4.12.0", "master").prepare()
        self.assertEqual(git("branch", "--show-current", cwd=self.repo), "master")

if __name__ == "__main__":
    unittest.main()
