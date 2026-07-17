from __future__ import annotations

import pytest

from unicode_animations import SPINNER_NAMES, get_provider, spinners
from unicode_animations.provider import AnimationSpec, UnicodeAnimationProvider


def test_get_provider_returns_structural_provider_without_openminion_import() -> None:
    provider = get_provider()

    assert isinstance(provider, UnicodeAnimationProvider)
    assert provider.provider_id == "unicode"
    assert provider.names() == tuple(SPINNER_NAMES)


@pytest.mark.parametrize("name", SPINNER_NAMES)
def test_provider_specs_match_spinner_catalog(name: str) -> None:
    provider = get_provider()
    spec = provider.get(name)

    assert spec == AnimationSpec(
        provider_id="unicode",
        name=name,
        frames=tuple(spinners[name].frames),
        interval_ms=spinners[name].interval,
    )


def test_provider_rejects_unknown_spinner_name() -> None:
    with pytest.raises(KeyError):
        get_provider().get("unknown")
