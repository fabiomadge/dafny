#!/usr/bin/env python3
"""Fixture helpers shared by the release-tooling tests."""

import subprocess

from pathlib import Path

def git(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd,
                          capture_output=True, check=True, encoding="utf-8")

def configure(repo: Path) -> None:
    """Settings a test repository needs regardless of the developer's global ones.

    A global `commit.gpgsign` or `core.hooksPath` would otherwise make these tests
    fail on their machine and nowhere else.
    """
    for key, value in (("user.name", "Dafny Test"),
                       ("user.email", "test@example.com"),
                       ("commit.gpgsign", "false"),
                       ("tag.gpgsign", "false"),
                       ("core.hooksPath", str(repo / ".no-such-hooks"))):
        git("config", key, value, cwd=repo)

def init_repo(repo: Path) -> None:
    git("init", "--quiet", "--initial-branch=master", ".", cwd=repo)
    configure(repo)
