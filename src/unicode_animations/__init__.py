"""Unicode braille spinner animations for Python."""

from .braille import (
    BRAILLE_SPINNER_NAMES,
    BrailleSpinnerName,
    Spinner,
    grid_to_braille,
    make_grid,
    spinners,
)

# Compatibility aliases mirroring the original JavaScript API style.
gridToBraille = grid_to_braille
makeGrid = make_grid

__all__ = [
    "Spinner",
    "BrailleSpinnerName",
    "BRAILLE_SPINNER_NAMES",
    "spinners",
    "grid_to_braille",
    "make_grid",
    "gridToBraille",
    "makeGrid",
]
