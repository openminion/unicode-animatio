from __future__ import annotations

from unicode_animations import (
    BRAILLE_SPINNER_NAMES,
    SPINNER_NAMES,
    BrailleSpinnerName,
    SpinnerName,
    grid_to_braille,
    gridToBraille,
    make_grid,
    makeGrid,
)


def test_compatibility_aliases_point_to_canonical_helpers() -> None:
    assert makeGrid is make_grid
    assert gridToBraille is grid_to_braille
    assert BrailleSpinnerName is SpinnerName
    assert BRAILLE_SPINNER_NAMES is SPINNER_NAMES
