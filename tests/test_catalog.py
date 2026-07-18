from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import pytest
from wcwidth import wcswidth

from unicode_animations import (
    BRAILLE_SPINNER_NAMES,
    CATEGORY_NAMES,
    SPINNER_CATEGORIES,
    SPINNER_NAMES,
    spinner_names_for_category,
    spinners,
)

EXPECTED_PATH = Path(__file__).with_name("expected_spinners.json")
EXPECTED = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))


def _assert_terminal_safe(frames: tuple[str, ...]) -> None:
    assert frames
    widths = {wcswidth(frame) for frame in frames}
    assert -1 not in widths
    assert len(widths) == 1
    assert not any(
        char in {"\x1b", "\r", "\n", "\t"} or unicodedata.category(char).startswith("C")
        for frame in frames
        for char in frame
    )


def test_catalog_surfaces_share_the_same_ordered_names() -> None:
    assert len(SPINNER_NAMES) == 58
    assert BRAILLE_SPINNER_NAMES == SPINNER_NAMES
    assert tuple(spinners) == SPINNER_NAMES
    assert tuple(SPINNER_CATEGORIES) == SPINNER_NAMES


def test_categories_cover_every_spinner_exactly_once() -> None:
    assert set(SPINNER_CATEGORIES.values()) == set(CATEGORY_NAMES)
    names_by_category = tuple(
        name for category in CATEGORY_NAMES for name in spinner_names_for_category(category)
    )
    assert len(names_by_category) == len(set(names_by_category))
    assert set(names_by_category) == set(SPINNER_NAMES)


def test_existing_category_mapping_matches_reviewed_contract() -> None:
    assert spinner_names_for_category("subtle")[:4] == (
        "braille",
        "pulse",
        "orbit",
        "breathe",
    )
    assert SPINNER_CATEGORIES["diagswipe"] == "scan"
    assert SPINNER_CATEGORIES["helix"] == "data"
    assert SPINNER_CATEGORIES["fillsweep"] == "progress"
    assert SPINNER_CATEGORIES["sparkle"] == "alert"
    assert SPINNER_CATEGORIES["checkerboard"] == "dense"


def test_unknown_category_raises_key_error() -> None:
    with pytest.raises(KeyError, match="unknown"):
        spinner_names_for_category("unknown")


@pytest.mark.parametrize("name", SPINNER_NAMES)
def test_catalog_frames_are_terminal_safe(name: str) -> None:
    spinner = spinners[name]
    assert spinner.interval > 0
    _assert_terminal_safe(spinner.frames)


@pytest.mark.parametrize(
    "frames",
    [
        (".", ".."),
        ("\x1b[31m",),
        ("ok", "bad\n"),
        ("ok", "bad\t"),
    ],
)
def test_conformance_helper_rejects_malformed_examples(frames: tuple[str, ...]) -> None:
    with pytest.raises(AssertionError):
        _assert_terminal_safe(frames)


@pytest.mark.parametrize("name", SPINNER_NAMES)
def test_catalog_matches_expected_snapshot(name: str) -> None:
    expected = EXPECTED[name]
    assert list(spinners[name].frames) == expected["frames"]
    assert spinners[name].interval == expected["interval"]


def test_snapshot_contains_only_canonical_names() -> None:
    assert set(EXPECTED) == set(SPINNER_NAMES)
