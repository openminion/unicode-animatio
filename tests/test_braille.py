from __future__ import annotations

import json
from pathlib import Path

import pytest

from unicode_animations import grid_to_braille, make_grid
from unicode_animations.braille import BRAILLE_SPINNER_NAMES, spinners

EXPECTED_PATH = Path(__file__).with_name("expected_spinners.json")
EXPECTED = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))


def test_make_grid_dimensions() -> None:
    grid = make_grid(4, 8)
    assert len(grid) == 4
    assert len(grid[0]) == 8
    assert all(cell is False for row in grid for cell in row)


def test_make_grid_returns_empty_for_nonpositive_dimensions() -> None:
    assert make_grid(0, 5) == []
    assert make_grid(5, 0) == []
    assert make_grid(-1, 5) == []
    assert make_grid(5, -1) == []


def test_grid_to_braille_empty_grid() -> None:
    assert grid_to_braille([]) == ""


def test_grid_to_braille_all_false_is_blank_braille() -> None:
    grid = make_grid(4, 2)
    assert grid_to_braille(grid) == "\u2800"


def test_grid_to_braille_all_true_is_full_braille() -> None:
    grid = make_grid(4, 2)
    for row in range(4):
        for col in range(2):
            grid[row][col] = True
    assert grid_to_braille(grid) == "\u28ff"


@pytest.mark.parametrize(
    ("row", "col", "expected"),
    [
        (0, 0, "\u2801"),
        (0, 1, "\u2808"),
        (1, 0, "\u2802"),
        (1, 1, "\u2810"),
        (2, 0, "\u2804"),
        (2, 1, "\u2820"),
        (3, 0, "\u2840"),
        (3, 1, "\u2880"),
    ],
)
def test_grid_to_braille_dot_mapping(row: int, col: int, expected: str) -> None:
    grid = make_grid(4, 2)
    grid[row][col] = True
    assert grid_to_braille(grid) == expected


def test_grid_to_braille_multiple_chars_for_wider_grids() -> None:
    grid = make_grid(4, 4)
    grid[0][0] = True
    grid[0][2] = True
    result = grid_to_braille(grid)
    assert len(result) == 2
    assert result == "\u2801\u2801"


def test_grid_to_braille_handles_odd_width_grids() -> None:
    grid = make_grid(4, 3)
    grid[0][0] = True
    grid[0][2] = True
    result = grid_to_braille(grid)
    assert len(result) == 2


def test_spinners_export_all_expected_names() -> None:
    assert sorted(spinners.keys()) == sorted(BRAILLE_SPINNER_NAMES)


@pytest.mark.parametrize("name", BRAILLE_SPINNER_NAMES)
def test_spinner_has_non_empty_frames(name: str) -> None:
    assert len(spinners[name].frames) > 0


@pytest.mark.parametrize("name", BRAILLE_SPINNER_NAMES)
def test_spinner_has_positive_interval(name: str) -> None:
    assert spinners[name].interval > 0


@pytest.mark.parametrize("name", BRAILLE_SPINNER_NAMES)
def test_spinner_has_consistent_frame_widths(name: str) -> None:
    widths = {len(frame) for frame in spinners[name].frames}
    assert len(widths) == 1


@pytest.mark.parametrize("name", BRAILLE_SPINNER_NAMES)
def test_spinner_frames_match_expected_snapshot(name: str) -> None:
    expected = EXPECTED[name]
    assert list(spinners[name].frames) == expected["frames"]
    assert spinners[name].interval == expected["interval"]
