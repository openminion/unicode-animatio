from __future__ import annotations

import re
from pathlib import Path

from unicode_animations import __version__

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT_TEXT = (ROOT / "pyproject.toml").read_text(encoding="utf-8")


def test_package_version_matches_pyproject() -> None:
    match = re.search(r'^version = "([^"]+)"$', PYPROJECT_TEXT, re.MULTILINE)
    assert match is not None
    assert __version__ == match.group(1)


def test_project_urls_point_to_openminion_repo() -> None:
    assert 'Homepage = "https://github.com/openminion/unicode-animations"' in PYPROJECT_TEXT
    assert 'Repository = "https://github.com/openminion/unicode-animations"' in PYPROJECT_TEXT
    assert (
        'Documentation = "https://github.com/openminion/unicode-animations/tree/main/docs"'
        in PYPROJECT_TEXT
    )
    assert 'Issues = "https://github.com/openminion/unicode-animations/issues"' in PYPROJECT_TEXT


def test_console_scripts_match_public_package_contract() -> None:
    assert 'unicode-animations = "unicode_animations.cli:main"' in PYPROJECT_TEXT
    assert 'unicode-animations-web = "unicode_animations.web:main"' in PYPROJECT_TEXT
