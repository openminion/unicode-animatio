"""OpenMinion-compatible animation provider for unicode-animatio."""

from __future__ import annotations

from dataclasses import dataclass

from .braille import BRAILLE_SPINNER_NAMES, spinners


@dataclass(frozen=True)
class AnimationSpec:
    """Structural animation payload consumed by presentation registries."""

    provider_id: str
    name: str
    frames: tuple[str, ...]
    interval_ms: int


class UnicodeAnimationProvider:
    """Expose unicode-animatio spinners through a tiny structural contract."""

    provider_id = "unicode"

    def names(self) -> tuple[str, ...]:
        return tuple(BRAILLE_SPINNER_NAMES)

    def get(self, name: str) -> AnimationSpec:
        if name not in spinners:
            raise KeyError(name)
        spinner = spinners[name]
        return AnimationSpec(
            provider_id=self.provider_id,
            name=name,
            frames=tuple(spinner.frames),
            interval_ms=int(spinner.interval),
        )


def get_provider() -> UnicodeAnimationProvider:
    """Return the package provider without importing OpenMinion."""

    return UnicodeAnimationProvider()


__all__ = ["AnimationSpec", "UnicodeAnimationProvider", "get_provider"]
