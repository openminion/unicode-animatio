from __future__ import annotations

from unicode_animations import grid_to_braille, gridToBraille, make_grid, makeGrid


def test_compatibility_aliases_point_to_canonical_helpers() -> None:
    assert makeGrid is make_grid
    assert gridToBraille is grid_to_braille
