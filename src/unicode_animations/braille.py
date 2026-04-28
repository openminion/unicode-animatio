"""Unicode braille spinners and grid helpers."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

BrailleSpinnerName = Literal[
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
]

BRAILLE_SPINNER_NAMES: tuple[BrailleSpinnerName, ...] = (
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
)


@dataclass(frozen=True)
class Spinner:
    frames: tuple[str, ...]
    interval: int


BRAILLE_DOT_MAP = (
    (0x01, 0x08),  # row 0
    (0x02, 0x10),  # row 1
    (0x04, 0x20),  # row 2
    (0x40, 0x80),  # row 3
)


def grid_to_braille(grid: Sequence[Sequence[bool]]) -> str:
    """Convert a 2D boolean grid into a braille string."""
    rows = len(grid)
    cols = len(grid[0]) if rows and grid[0] else 0
    char_count = (cols + 1) // 2
    result: list[str] = []

    for c in range(char_count):
        code = 0x2800
        for r in range(min(4, rows)):
            row = grid[r]
            for d in range(2):
                col = c * 2 + d
                if col < cols and col < len(row) and row[col]:
                    code |= BRAILLE_DOT_MAP[r][d]
        result.append(chr(code))

    return "".join(result)


def make_grid(rows: int, cols: int) -> list[list[bool]]:
    """Create an empty grid of the given dimensions."""
    if rows <= 0 or cols <= 0:
        return []
    return [[False for _ in range(cols)] for _ in range(rows)]


def _js_round(value: float) -> int:
    """Match JavaScript's Math.round behavior for deterministic parity."""
    if value >= 0:
        return int(math.floor(value + 0.5))
    return int(math.ceil(value - 0.5))


def _gen_scan() -> list[str]:
    width, height = 8, 4
    frames: list[str] = []
    for pos in range(-1, width + 1):
        grid = make_grid(height, width)
        for row in range(height):
            for col in range(width):
                if col == pos or col == pos - 1:
                    grid[row][col] = True
        frames.append(grid_to_braille(grid))
    return frames


def _gen_rain() -> list[str]:
    width, height, total_frames = 8, 4, 12
    frames: list[str] = []
    offsets = [0, 3, 1, 5, 2, 7, 4, 6]

    for frame_idx in range(total_frames):
        grid = make_grid(height, width)
        for col in range(width):
            row = (frame_idx + offsets[col]) % (height + 2)
            if row < height:
                grid[row][col] = True
        frames.append(grid_to_braille(grid))

    return frames


def _gen_scanline() -> list[str]:
    width, height = 6, 4
    frames: list[str] = []
    positions = [0, 1, 2, 3, 2, 1]

    for row in positions:
        grid = make_grid(height, width)
        for col in range(width):
            grid[row][col] = True
            if row > 0:
                grid[row - 1][col] = col % 2 == 0
        frames.append(grid_to_braille(grid))

    return frames


def _gen_pulse() -> list[str]:
    width, height = 6, 4
    frames: list[str] = []
    cx = width / 2 - 0.5
    cy = height / 2 - 0.5
    radii = [0.5, 1.2, 2.0, 3.0, 3.5]

    for radius in radii:
        grid = make_grid(height, width)
        for row in range(height):
            for col in range(width):
                dist = math.sqrt((col - cx) ** 2 + (row - cy) ** 2)
                if abs(dist - radius) < 0.9:
                    grid[row][col] = True
        frames.append(grid_to_braille(grid))

    return frames


def _gen_snake() -> list[str]:
    width, height = 4, 4
    path: list[tuple[int, int]] = []

    for row in range(height):
        if row % 2 == 0:
            for col in range(width):
                path.append((row, col))
        else:
            for col in range(width - 1, -1, -1):
                path.append((row, col))

    frames: list[str] = []
    for idx in range(len(path)):
        grid = make_grid(height, width)
        for tail in range(4):
            point_idx = (idx - tail + len(path)) % len(path)
            row, col = path[point_idx]
            grid[row][col] = True
        frames.append(grid_to_braille(grid))

    return frames


def _gen_sparkle() -> list[str]:
    patterns = [
        [
            1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0,
            0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0,
        ],
        [
            0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1,
            0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0,
        ],
        [
            0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
            1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1,
        ],
        [
            1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0,
            0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0,
        ],
        [
            0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
            1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
        ],
        [
            0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
            0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0,
        ],
    ]

    width, height = 8, 4
    frames: list[str] = []

    for pattern in patterns:
        grid = make_grid(height, width)
        for row in range(height):
            for col in range(width):
                grid[row][col] = bool(pattern[row * width + col])
        frames.append(grid_to_braille(grid))

    return frames


def _gen_cascade() -> list[str]:
    width, height = 8, 4
    frames: list[str] = []

    for offset in range(-2, width + height):
        grid = make_grid(height, width)
        for row in range(height):
            for col in range(width):
                diag = col + row
                if diag == offset or diag == offset - 1:
                    grid[row][col] = True
        frames.append(grid_to_braille(grid))

    return frames


def _gen_columns() -> list[str]:
    width, height = 6, 4
    frames: list[str] = []

    for col in range(width):
        for fill_to in range(height - 1, -1, -1):
            grid = make_grid(height, width)
            for prev_col in range(col):
                for row in range(height):
                    grid[row][prev_col] = True
            for row in range(fill_to, height):
                grid[row][col] = True
            frames.append(grid_to_braille(grid))

    full = make_grid(height, width)
    for row in range(height):
        for col in range(width):
            full[row][col] = True
    frames.append(grid_to_braille(full))
    frames.append(grid_to_braille(make_grid(height, width)))

    return frames


def _gen_orbit() -> list[str]:
    width, height = 2, 4
    path: list[tuple[int, int]] = [
        (0, 0),
        (0, 1),
        (1, 1),
        (2, 1),
        (3, 1),
        (3, 0),
        (2, 0),
        (1, 0),
    ]

    frames: list[str] = []
    for idx in range(len(path)):
        grid = make_grid(height, width)
        row, col = path[idx]
        grid[row][col] = True

        trail_idx = (idx - 1 + len(path)) % len(path)
        trail_row, trail_col = path[trail_idx]
        grid[trail_row][trail_col] = True

        frames.append(grid_to_braille(grid))

    return frames


def _gen_breathe() -> list[str]:
    stages: list[list[tuple[int, int]]] = [
        [],
        [(1, 0)],
        [(0, 1), (2, 0)],
        [(0, 0), (1, 1), (3, 0)],
        [(0, 0), (1, 1), (2, 0), (3, 1)],
        [(0, 0), (0, 1), (1, 1), (2, 0), (3, 1)],
        [(0, 0), (0, 1), (1, 0), (2, 1), (3, 0), (3, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (3, 0), (3, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)],
    ]

    frames: list[str] = []
    sequence = stages + list(reversed(stages))[1:]

    for dots in sequence:
        grid = make_grid(4, 2)
        for row, col in dots:
            grid[row][col] = True
        frames.append(grid_to_braille(grid))

    return frames


def _gen_waverows() -> list[str]:
    width, height, total_frames = 8, 4, 16
    frames: list[str] = []

    for frame_idx in range(total_frames):
        grid = make_grid(height, width)
        for col in range(width):
            phase = frame_idx - col * 0.5
            row = _js_round(((math.sin(phase * 0.8) + 1.0) / 2.0) * (height - 1))
            grid[row][col] = True
            if row > 0:
                grid[row - 1][col] = (frame_idx + col) % 3 == 0
        frames.append(grid_to_braille(grid))

    return frames


def _gen_checkerboard() -> list[str]:
    width, height = 6, 4
    frames: list[str] = []

    for phase in range(4):
        grid = make_grid(height, width)
        for row in range(height):
            for col in range(width):
                if phase < 2:
                    grid[row][col] = (row + col + phase) % 2 == 0
                else:
                    grid[row][col] = (row + col + phase) % 3 == 0
        frames.append(grid_to_braille(grid))

    return frames


def _gen_helix() -> list[str]:
    width, height, total_frames = 8, 4, 16
    frames: list[str] = []

    for frame_idx in range(total_frames):
        grid = make_grid(height, width)
        for col in range(width):
            phase = (frame_idx + col) * (math.pi / 4)
            y1 = _js_round(((math.sin(phase) + 1.0) / 2.0) * (height - 1))
            y2 = _js_round(((math.sin(phase + math.pi) + 1.0) / 2.0) * (height - 1))
            grid[y1][col] = True
            grid[y2][col] = True
        frames.append(grid_to_braille(grid))

    return frames


def _gen_fillsweep() -> list[str]:
    width, height = 4, 4
    frames: list[str] = []

    for row in range(height - 1, -1, -1):
        grid = make_grid(height, width)
        for inner_row in range(row, height):
            for col in range(width):
                grid[inner_row][col] = True
        frames.append(grid_to_braille(grid))

    full = make_grid(height, width)
    for row in range(height):
        for col in range(width):
            full[row][col] = True

    frames.append(grid_to_braille(full))
    frames.append(grid_to_braille(full))

    for row in range(height):
        grid = make_grid(height, width)
        for inner_row in range(row + 1, height):
            for col in range(width):
                grid[inner_row][col] = True
        frames.append(grid_to_braille(grid))

    frames.append(grid_to_braille(make_grid(height, width)))

    return frames


def _gen_diagonal_swipe() -> list[str]:
    width, height = 4, 4
    frames: list[str] = []
    max_diag = width + height - 2

    for diag in range(max_diag + 1):
        grid = make_grid(height, width)
        for row in range(height):
            for col in range(width):
                if row + col <= diag:
                    grid[row][col] = True
        frames.append(grid_to_braille(grid))

    full = make_grid(height, width)
    for row in range(height):
        for col in range(width):
            full[row][col] = True
    frames.append(grid_to_braille(full))

    for diag in range(max_diag + 1):
        grid = make_grid(height, width)
        for row in range(height):
            for col in range(width):
                if row + col > diag:
                    grid[row][col] = True
        frames.append(grid_to_braille(grid))

    frames.append(grid_to_braille(make_grid(height, width)))
    return frames


spinners: dict[BrailleSpinnerName, Spinner] = {
    "braille": Spinner(
        frames=("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"),
        interval=80,
    ),
    "braillewave": Spinner(
        frames=(
            "⠁⠂⠄⡀",
            "⠂⠄⡀⢀",
            "⠄⡀⢀⠠",
            "⡀⢀⠠⠐",
            "⢀⠠⠐⠈",
            "⠠⠐⠈⠁",
            "⠐⠈⠁⠂",
            "⠈⠁⠂⠄",
        ),
        interval=100,
    ),
    "dna": Spinner(
        frames=(
            "⠋⠉⠙⠚",
            "⠉⠙⠚⠒",
            "⠙⠚⠒⠂",
            "⠚⠒⠂⠂",
            "⠒⠂⠂⠒",
            "⠂⠂⠒⠲",
            "⠂⠒⠲⠴",
            "⠒⠲⠴⠤",
            "⠲⠴⠤⠄",
            "⠴⠤⠄⠋",
            "⠤⠄⠋⠉",
            "⠄⠋⠉⠙",
        ),
        interval=80,
    ),
    "scan": Spinner(frames=tuple(_gen_scan()), interval=70),
    "rain": Spinner(frames=tuple(_gen_rain()), interval=100),
    "scanline": Spinner(frames=tuple(_gen_scanline()), interval=120),
    "pulse": Spinner(frames=tuple(_gen_pulse()), interval=180),
    "snake": Spinner(frames=tuple(_gen_snake()), interval=80),
    "sparkle": Spinner(frames=tuple(_gen_sparkle()), interval=150),
    "cascade": Spinner(frames=tuple(_gen_cascade()), interval=60),
    "columns": Spinner(frames=tuple(_gen_columns()), interval=60),
    "orbit": Spinner(frames=tuple(_gen_orbit()), interval=100),
    "breathe": Spinner(frames=tuple(_gen_breathe()), interval=100),
    "waverows": Spinner(frames=tuple(_gen_waverows()), interval=90),
    "checkerboard": Spinner(frames=tuple(_gen_checkerboard()), interval=250),
    "helix": Spinner(frames=tuple(_gen_helix()), interval=80),
    "fillsweep": Spinner(frames=tuple(_gen_fillsweep()), interval=100),
    "diagswipe": Spinner(frames=tuple(_gen_diagonal_swipe()), interval=60),
}


__all__ = [
    "Spinner",
    "BrailleSpinnerName",
    "BRAILLE_SPINNER_NAMES",
    "grid_to_braille",
    "make_grid",
    "spinners",
]
