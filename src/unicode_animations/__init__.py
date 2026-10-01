"""Unicode and ASCII terminal animations for Python."""

__version__ = "0.0.11"

from .braille import Spinner, grid_to_braille, make_grid
from .catalog import (
    BRAILLE_SPINNER_NAMES,
    CATEGORY_DESCRIPTIONS,
    CATEGORY_MOTION,
    CATEGORY_NAMES,
    SPINNER_CATEGORIES,
    SPINNER_NAMES,
    BrailleSpinnerName,
    CategoryName,
    SpinnerMetadata,
    SpinnerName,
    all_spinner_metadata,
    metadata_for_spinner,
    search_spinner_names,
    spinner_names_for_category,
    spinners,
)
from .provider import AnimationSpec, UnicodeAnimationProvider, get_provider

# Compatibility aliases mirroring the original JavaScript API style.
gridToBraille = grid_to_braille
makeGrid = make_grid

__all__ = [
    "__version__",
    "Spinner",
    "BrailleSpinnerName",
    "SpinnerName",
    "CategoryName",
    "SpinnerMetadata",
    "AnimationSpec",
    "UnicodeAnimationProvider",
    "BRAILLE_SPINNER_NAMES",
    "SPINNER_NAMES",
    "CATEGORY_NAMES",
    "CATEGORY_DESCRIPTIONS",
    "CATEGORY_MOTION",
    "SPINNER_CATEGORIES",
    "spinners",
    "grid_to_braille",
    "make_grid",
    "gridToBraille",
    "makeGrid",
    "all_spinner_metadata",
    "metadata_for_spinner",
    "search_spinner_names",
    "spinner_names_for_category",
    "get_provider",
]
