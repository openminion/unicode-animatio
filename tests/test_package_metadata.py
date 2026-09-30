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
    assert 'Homepage = "https://github.com/openminion/unicode-animatio"' in PYPROJECT_TEXT
    assert 'Repository = "https://github.com/openminion/unicode-animatio"' in PYPROJECT_TEXT
    assert (
        'Documentation = "https://github.com/openminion/unicode-animatio/tree/main/docs"'
        in PYPROJECT_TEXT
    )
    assert 'Issues = "https://github.com/openminion/unicode-animatio/issues"' in PYPROJECT_TEXT
    assert (
        '"Release Notes" = "https://github.com/openminion/unicode-animatio/releases"'
        in PYPROJECT_TEXT
    )


def test_package_metadata_uses_spdx_license_and_current_python_classifiers() -> None:
    assert 'license = "MIT"' in PYPROJECT_TEXT
    assert 'license-files = ["LICENSE"]' in PYPROJECT_TEXT
    assert "License :: OSI Approved" not in PYPROJECT_TEXT
    assert '"Programming Language :: Python :: 3.13"' in PYPROJECT_TEXT
    assert '"Programming Language :: Python :: 3.14"' in PYPROJECT_TEXT


def test_console_scripts_match_public_package_contract() -> None:
    assert 'unicode-animatio = "unicode_animations.cli:main"' in PYPROJECT_TEXT
    assert 'unicode-animatio-web = "unicode_animations.web:main"' in PYPROJECT_TEXT


def test_openminion_animation_provider_entry_point_is_declared() -> None:
    assert '[project.entry-points."openminion.cli.animation_providers"]' in PYPROJECT_TEXT
    assert 'unicode = "unicode_animations.provider:get_provider"' in PYPROJECT_TEXT
