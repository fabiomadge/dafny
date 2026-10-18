"""Tests for `prepare_release.py`, and for the release notes of this repository."""

# pylint: disable=protected-access

import doctest
import os
import subprocess
import sys
import tempfile
import unittest

from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prepare_release  # pylint: disable=wrong-import-position
from prepare_release import NewsFragments, Release  # pylint: disable=wrong-import-position

BUILD_PROPS = """<Project>
  <PropertyGroup>
    <VersionPrefix>4.11.0</VersionPrefix>
  </PropertyGroup>
</Project>
"""

def git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, check=True,
                          encoding="utf-8").stdout.strip()

class ThisRepositoryTest(unittest.TestCase):
    def test_every_release_note_is_where_prepare_reads_it(self) -> None:
        root = Path(__file__).resolve().parent.parent
        news = Path(Release.NEWSFRAGMENTS_PATH)
        self.assertEqual(NewsFragments.misplaced(root, news), [], f"Move these to {news}/.")
        self.assertEqual([p.name for p in NewsFragments.from_directory(str(root / news)).unrecognized], [],
                         "Rename these to <issue>.<kind>, <PR>.<kind> or <description>.<kind>.")

class ReleaseTest(unittest.TestCase):
    """Runs `Release` in a throwaway repository shaped like this one."""

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

    def test_misplaced_finds_notes_outside_docs_dev_news(self) -> None:
        misplaced = ["docs/dev/1234.feat", "docs/dev/news/old/1234.break",
                     "docs/news/1234.fix", "docs/news/fix.1234"]
        for path in [*misplaced, "Source/break.dfy"]:
            (self.repo / path).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / path).write_text("A note.\n", encoding="utf-8")
        self.commit("Notes in the wrong places (#2000)")

        self.assertEqual(NewsFragments.misplaced(self.repo, Path(Release.NEWSFRAGMENTS_PATH)), misplaced)

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

    def test_render_puts_a_note_without_pr_number_last(self) -> None:
        self.write_note("unattributed.fix", "Fix another thing")
        self.commit("A commit without a PR number")

        rendered = NewsFragments.from_directory(Release.NEWSFRAGMENTS_PATH).render()

        self.assertTrue(rendered.endswith("\n- Fix another thing"), rendered)
        self.assertIn("- Fix the thing (https://github.com/dafny-lang/dafny/pull/1234)", rendered)

    def test_no_release_tag_is_false_for_an_annotated_tag(self) -> None:
        release = Release("4.12.0", "master")
        self.assertTrue(release._no_release_tag())
        git("tag", "--annotate", "--message=Dafny v4.12.0", "v4.12.0", cwd=self.repo)
        self.assertFalse(release._no_release_tag())

    def test_head_up_to_date_fails_when_fetch_fails(self) -> None:
        git("remote", "add", "origin", str(self.tmp / "no-such-repo"), cwd=self.repo)
        with self.assertRaises(subprocess.CalledProcessError):
            Release("4.12.0", "master")._head_up_to_date()

    def test_dry_run_changes_nothing(self) -> None:
        self.offline()
        head = git("rev-parse", "HEAD", cwd=self.repo)
        for action in ("prepare", "set-next-version", "release"):
            with self.subTest(action):
                argv = ["prepare_release.py", "--dry-run", "4.12.0", action]
                with mock.patch.object(sys, "argv", argv), mock.patch.object(prepare_release, "DRY_RUN", False):
                    prepare_release.main()

                self.assertEqual(git("rev-parse", "HEAD", cwd=self.repo), head)
                self.assertEqual(git("branch", "--show-current", cwd=self.repo), "master")
                self.assertEqual(git("status", "--porcelain", "--untracked-files=all", cwd=self.repo), "")
                self.assertEqual(git("tag", cwd=self.repo), "")

def load_tests(loader, tests, ignore):  # pylint: disable=unused-argument
    tests.addTests(doctest.DocTestSuite(prepare_release))
    return tests

if __name__ == "__main__":
    unittest.main()
