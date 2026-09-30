"""Canonical Unicode and ASCII animation catalog."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, cast

from .braille import Spinner
from .braille import spinners as _braille_spinners

CategoryName = Literal[
    "subtle",
    "scan",
    "build",
    "thinking",
    "tool",
    "data",
    "graph",
    "progress",
    "alert",
    "dense",
]


@dataclass(frozen=True)
class SpinnerMetadata:
    """Public metadata for choosing a spinner without reading frame internals."""

    name: SpinnerName
    category: CategoryName
    tags: tuple[str, ...]
    frame_count: int
    interval_ms: int
    frame_width: int
    preview_frame: str
    motion: str
    description: str


SpinnerName = Literal[
    "braille",
    "braillewave",
    "dna",
    "scan",
    "rain",
    "scanline",
    "pulse",
    "snake",
    "sparkle",
    "cascade",
    "columns",
    "orbit",
    "breathe",
    "waverows",
    "checkerboard",
    "helix",
    "fillsweep",
    "diagswipe",
    "softdot",
    "slowbreath",
    "quietorbit",
    "dimwave",
    "hscan",
    "vscan",
    "radar",
    "focusbeam",
    "blocks",
    "stack",
    "assemble",
    "brickline",
    "ellipsis",
    "mindwave",
    "synapse",
    "neuron",
    "terminalblink",
    "gearspin",
    "wrench",
    "sparkplug",
    "bitstream",
    "packetflow",
    "matrixrain",
    "columns2",
    "nodes",
    "edgepulse",
    "cluster",
    "orbitnodes",
    "meter",
    "ladder",
    "risingblocks",
    "fillbar2",
    "warningpulse",
    "heartbeat",
    "ping",
    "flashdot",
    "plasma",
    "noise",
    "moire",
    "shimmergrid",
]

CATEGORY_NAMES: tuple[CategoryName, ...] = (
    "subtle",
    "scan",
    "build",
    "thinking",
    "tool",
    "data",
    "graph",
    "progress",
    "alert",
    "dense",
)

SPINNER_NAMES: tuple[SpinnerName, ...] = (
    "braille",
    "braillewave",
    "dna",
    "scan",
    "rain",
    "scanline",
    "pulse",
    "snake",
    "sparkle",
    "cascade",
    "columns",
    "orbit",
    "breathe",
    "waverows",
    "checkerboard",
    "helix",
    "fillsweep",
    "diagswipe",
    "softdot",
    "slowbreath",
    "quietorbit",
    "dimwave",
    "hscan",
    "vscan",
    "radar",
    "focusbeam",
    "blocks",
    "stack",
    "assemble",
    "brickline",
    "ellipsis",
    "mindwave",
    "synapse",
    "neuron",
    "terminalblink",
    "gearspin",
    "wrench",
    "sparkplug",
    "bitstream",
    "packetflow",
    "matrixrain",
    "columns2",
    "nodes",
    "edgepulse",
    "cluster",
    "orbitnodes",
    "meter",
    "ladder",
    "risingblocks",
    "fillbar2",
    "warningpulse",
    "heartbeat",
    "ping",
    "flashdot",
    "plasma",
    "noise",
    "moire",
    "shimmergrid",
)

_ASCII_SPINNERS: dict[SpinnerName, Spinner] = {
    "softdot": Spinner(frames=(".", "o", "O", "o"), interval=140),
    "slowbreath": Spinner(frames=(".", "-", "=", "#", "=", "-"), interval=160),
    "quietorbit": Spinner(frames=(".", ":", "*", ":"), interval=140),
    "dimwave": Spinner(frames=("-", "~", "=", "~"), interval=150),
    "hscan": Spinner(frames=(">---", "->--", "-->-", "--->"), interval=90),
    "vscan": Spinner(frames=("|", "/", "-", "\\"), interval=100),
    "radar": Spinner(frames=(".   ", "..  ", "... ", "....", "... ", "..  "), interval=120),
    "focusbeam": Spinner(frames=("----", "===-", "-===", "--==", "---="), interval=90),
    "blocks": Spinner(frames=("[   ]", "[=  ]", "[== ]", "[===]", "[ ==]", "[  =]"), interval=110),
    "stack": Spinner(frames=("_  ", "=  ", "#  ", "## ", "###"), interval=140),
    "assemble": Spinner(frames=(". . .", ":. .:", "::.::", ":::::", ".:::."), interval=120),
    "brickline": Spinner(frames=("[]  ", "[][]", " [] ", "  []"), interval=130),
    "ellipsis": Spinner(frames=(".  ", ".. ", "...", ".. "), interval=180),
    "mindwave": Spinner(frames=("~  ", "~~ ", "~~~", "~~ "), interval=140),
    "synapse": Spinner(frames=("*..", ".*.", "..*", ".*."), interval=100),
    "neuron": Spinner(frames=("o..", ".o.", "..o", ".o."), interval=110),
    "terminalblink": Spinner(frames=("$_", "$ "), interval=160),
    "gearspin": Spinner(frames=("|", "/", "-", "\\"), interval=90),
    "wrench": Spinner(frames=("-T-", "-|-", "-T-", "-|-"), interval=120),
    "sparkplug": Spinner(frames=("*--", "-*-", "--*", "-*-"), interval=100),
    "bitstream": Spinner(frames=("1000", "0100", "0010", "0001"), interval=90),
    "packetflow": Spinner(frames=("[>]---", "-[>]--", "--[>]-", "---[>]"), interval=100),
    "matrixrain": Spinner(frames=("|..", ".|.", "..|", ".|."), interval=100),
    "columns2": Spinner(frames=("| |", " ||", "|| ", " | "), interval=110),
    "nodes": Spinner(frames=("o--o", "o==o", "O==o", "o==O"), interval=110),
    "edgepulse": Spinner(frames=("o---o", "o=--o", "o-=-o", "o--=o"), interval=90),
    "cluster": Spinner(frames=(".o.", "oOo", ".O.", "oOo"), interval=120),
    "orbitnodes": Spinner(frames=("o.o", ".o.", "o.o", "O.o"), interval=120),
    "meter": Spinner(frames=("[   ]", "[=  ]", "[== ]", "[===]"), interval=120),
    "ladder": Spinner(frames=("_", "=", "#", "=", "_"), interval=140),
    "risingblocks": Spinner(frames=("_", "-", "=", "#", "="), interval=120),
    "fillbar2": Spinner(frames=("....", "=...", "==..", "===.", "===="), interval=100),
    "warningpulse": Spinner(frames=("!  ", " ! ", "  !", " ! "), interval=140),
    "heartbeat": Spinner(frames=("_/_", "_/\\", "_/_", "___"), interval=140),
    "ping": Spinner(frames=(".  ", "o  ", "O  ", "o  "), interval=130),
    "flashdot": Spinner(frames=("*", ".", "*", " "), interval=160),
    "plasma": Spinner(frames=("~*~", "*~*", "~#~", "*~*"), interval=80),
    "noise": Spinner(frames=(".:*", "*:.", ":*.", ".*:"), interval=90),
    "moire": Spinner(frames=("///", "---", "|||", "---"), interval=100),
    "shimmergrid": Spinner(frames=(".+.", "+.+", "*+*", "+.+"), interval=90),
}

spinners = cast(dict[str, Spinner], {**_braille_spinners, **_ASCII_SPINNERS})

SPINNER_CATEGORIES: dict[SpinnerName, CategoryName] = {
    "braille": "subtle",
    "braillewave": "data",
    "dna": "data",
    "scan": "scan",
    "rain": "data",
    "scanline": "scan",
    "pulse": "subtle",
    "snake": "scan",
    "sparkle": "alert",
    "cascade": "data",
    "columns": "data",
    "orbit": "subtle",
    "breathe": "subtle",
    "waverows": "data",
    "checkerboard": "dense",
    "helix": "data",
    "fillsweep": "progress",
    "diagswipe": "scan",
    "softdot": "subtle",
    "slowbreath": "subtle",
    "quietorbit": "subtle",
    "dimwave": "subtle",
    "hscan": "scan",
    "vscan": "scan",
    "radar": "scan",
    "focusbeam": "scan",
    "blocks": "build",
    "stack": "build",
    "assemble": "build",
    "brickline": "build",
    "ellipsis": "thinking",
    "mindwave": "thinking",
    "synapse": "thinking",
    "neuron": "thinking",
    "terminalblink": "tool",
    "gearspin": "tool",
    "wrench": "tool",
    "sparkplug": "tool",
    "bitstream": "data",
    "packetflow": "data",
    "matrixrain": "data",
    "columns2": "data",
    "nodes": "graph",
    "edgepulse": "graph",
    "cluster": "graph",
    "orbitnodes": "graph",
    "meter": "progress",
    "ladder": "progress",
    "risingblocks": "progress",
    "fillbar2": "progress",
    "warningpulse": "alert",
    "heartbeat": "alert",
    "ping": "alert",
    "flashdot": "alert",
    "plasma": "dense",
    "noise": "dense",
    "moire": "dense",
    "shimmergrid": "dense",
}

CATEGORY_TAGS: dict[CategoryName, tuple[str, ...]] = {
    "subtle": ("calm", "minimal", "status"),
    "scan": ("inspection", "directional", "active"),
    "build": ("assembly", "progress", "work"),
    "thinking": ("agent", "reasoning", "ambient"),
    "tool": ("operation", "terminal", "action"),
    "data": ("stream", "ingestion", "flow"),
    "graph": ("nodes", "edges", "knowledge"),
    "progress": ("meter", "completion", "task"),
    "alert": ("attention", "pulse", "status"),
    "dense": ("visual", "high-energy", "showcase"),
}

CATEGORY_DESCRIPTIONS: dict[CategoryName, str] = {
    "subtle": "quiet background status for long-running work",
    "scan": "inspection, search, and navigation states",
    "build": "assembly and construction-style progress",
    "thinking": "agent reasoning and waiting states",
    "tool": "terminal and tool execution states",
    "data": "streaming, ingestion, and packet movement",
    "graph": "knowledge graph and relationship traversal",
    "progress": "explicit loading or completion movement",
    "alert": "attention states that should still stay lightweight",
    "dense": "public demos and high-energy showcase moments",
}

CATEGORY_MOTION: dict[CategoryName, str] = {
    "subtle": "low",
    "scan": "medium",
    "build": "medium",
    "thinking": "low",
    "tool": "medium",
    "data": "medium",
    "graph": "medium",
    "progress": "medium",
    "alert": "high",
    "dense": "high",
}


def metadata_for_spinner(name: str) -> SpinnerMetadata:
    spinner_name = cast(SpinnerName, name)
    spinner = spinners[spinner_name]
    category = SPINNER_CATEGORIES[spinner_name]
    return SpinnerMetadata(
        name=spinner_name,
        category=category,
        tags=CATEGORY_TAGS[category],
        frame_count=len(spinner.frames),
        interval_ms=spinner.interval,
        frame_width=max(len(frame) for frame in spinner.frames),
        preview_frame=spinner.frames[0],
        motion=CATEGORY_MOTION[category],
        description=CATEGORY_DESCRIPTIONS[category],
    )


def all_spinner_metadata() -> tuple[SpinnerMetadata, ...]:
    return tuple(metadata_for_spinner(name) for name in SPINNER_NAMES)


def spinner_names_for_category(category: str) -> tuple[SpinnerName, ...]:
    if category not in CATEGORY_NAMES:
        raise KeyError(category)
    return tuple(name for name in SPINNER_NAMES if SPINNER_CATEGORIES[name] == category)


def search_spinner_names(query: str, *, category: str | None = None) -> tuple[SpinnerName, ...]:
    normalized_query = query.strip().lower()
    names = SPINNER_NAMES if category is None else spinner_names_for_category(category)
    if not normalized_query:
        return names

    matches: list[SpinnerName] = []
    for name in names:
        metadata = metadata_for_spinner(name)
        search_text = " ".join((metadata.name, metadata.category, *metadata.tags)).lower()
        if normalized_query in search_text:
            matches.append(name)
    return tuple(matches)


BrailleSpinnerName = SpinnerName
BRAILLE_SPINNER_NAMES = SPINNER_NAMES

__all__ = [
    "BRAILLE_SPINNER_NAMES",
    "CATEGORY_NAMES",
    "CATEGORY_DESCRIPTIONS",
    "CATEGORY_MOTION",
    "SPINNER_CATEGORIES",
    "SPINNER_NAMES",
    "BrailleSpinnerName",
    "CategoryName",
    "SpinnerName",
    "SpinnerMetadata",
    "all_spinner_metadata",
    "metadata_for_spinner",
    "search_spinner_names",
    "spinner_names_for_category",
    "spinners",
]
