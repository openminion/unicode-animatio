from __future__ import annotations

import unicodedata

import pytest

from unicode_animations import BRAILLE_SPINNER_NAMES, get_provider, spinners
from unicode_animations.provider import AnimationSpec, UnicodeAnimationProvider


def _terminal_cell_width(value: str) -> int:
    width = 0
    for char in value:
        if unicodedata.combining(char):
            continue
        width += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return width


def _has_terminal_control(value: str) -> bool:
    return any(
        char in {"\x1b", "\r", "\n", "\t"} or unicodedata.category(char).startswith("C")
        for char in value
    )


def test_get_provider_returns_structural_provider_without_openminion_import() -> None:
    provider = get_provider()

    assert isinstance(provider, UnicodeAnimationProvider)
    assert provider.provider_id == "unicode"
    assert provider.names() == tuple(BRAILLE_SPINNER_NAMES)


@pytest.mark.parametrize("name", BRAILLE_SPINNER_NAMES)
def test_provider_specs_match_spinner_catalog(name: str) -> None:
    provider = get_provider()
    spec = provider.get(name)

    assert spec == AnimationSpec(
        provider_id="unicode",
        name=name,
        frames=tuple(spinners[name].frames),
        interval_ms=spinners[name].interval,
    )


@pytest.mark.parametrize("name", BRAILLE_SPINNER_NAMES)
def test_provider_specs_are_terminal_safe_and_stable_width(name: str) -> None:
    spec = get_provider().get(name)

    assert spec.frames
    assert spec.interval_ms > 0
    assert not any(_has_terminal_control(frame) for frame in spec.frames)
    widths = {_terminal_cell_width(frame) for frame in spec.frames}
    assert len(widths) == 1


def test_provider_rejects_unknown_spinner_name() -> None:
    with pytest.raises(KeyError):
        get_provider().get("unknown")
