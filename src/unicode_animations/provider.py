"""OpenMinion-compatible animation provider for unicode-animatio."""

from __future__ import annotations

from dataclasses import dataclass

from .catalog import (
    SpinnerMetadata,
    all_spinner_metadata,
    metadata_for_spinner,
    search_spinner_names,
    spinners,
)


@dataclass(frozen=True)
class AnimationSpec:
    """Structural animation payload consumed by presentation registries."""

    provider_id: str
    name: str
    frames: tuple[str, ...]
    interval_ms: int
    category: str = ""
    tags: tuple[str, ...] = ()
    frame_count: int = 0
    frame_width: int = 0
    motion: str = ""
    description: str = ""


class UnicodeAnimationProvider:
    """Expose unicode-animatio spinners through a tiny structural contract."""

    provider_id = "unicode"

    def names(self, *, category: str | None = None, search: str = "") -> tuple[str, ...]:
        return search_spinner_names(search, category=category)

    def catalog(self) -> tuple[SpinnerMetadata, ...]:
        return all_spinner_metadata()

    def describe(self, name: str) -> SpinnerMetadata:
        return metadata_for_spinner(name)

    def get(self, name: str, *, length: int = 1) -> AnimationSpec:
        if length < 1:
            raise ValueError("length must be positive")
        metadata = metadata_for_spinner(name)
        spinner = spinners[metadata.name]
        return AnimationSpec(
            provider_id=self.provider_id,
            name=metadata.name,
            frames=tuple(frame * length for frame in spinner.frames),
            interval_ms=spinner.interval,
            category=metadata.category,
            tags=metadata.tags,
            frame_count=metadata.frame_count,
            frame_width=metadata.frame_width * length,
            motion=metadata.motion,
            description=metadata.description,
        )


def get_provider() -> UnicodeAnimationProvider:
    """Return the package provider without importing OpenMinion."""

    return UnicodeAnimationProvider()


__all__ = ["AnimationSpec", "UnicodeAnimationProvider", "get_provider"]
