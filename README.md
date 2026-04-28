# unicode-animations

Python port of `unicode-animations` with 18 braille spinner animations as raw frame data.

- Raw spinner frame data for terminal and web previews
- Typed Python API with compatibility aliases for the original JS-style helpers
- Built-in CLI and browser demo for quick verification before shipping

## Install

```bash
pip install unicode-animations
```

## Quick start

```python
from unicode_animations import spinners

spinner = spinners["braille"]
print(spinner.frames)
print(spinner.interval)
```

Each spinner is a `Spinner(frames: tuple[str, ...], interval: int)`.

## Utilities

```python
from unicode_animations import make_grid, grid_to_braille

grid = make_grid(4, 4)
grid[0][0] = True
grid[1][1] = True
grid[2][2] = True
grid[3][3] = True

print(grid_to_braille(grid))
```

## CLI

```bash
unicode-animations --list
unicode-animations
unicode-animations helix
unicode-animations --web
unicode-animations-web --port 8765
unicode-animations-web --host 0.0.0.0 --port 8765 --no-open
```

`--web` launches a local browser preview that serves all spinner frames from the
Python package itself.

## Terminal Demo Script (Python API)

From the project root:

```bash
python examples/terminal_demo.py
python examples/terminal_demo.py --seconds-per-spinner 2 --loops 2
python examples/terminal_demo.py helix
python examples/terminal_demo.py --list
```

This demo is useful if you want to see how to animate spinners directly from
Python code (without using the built-in CLI command).

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
python -m build
```

The test suite is configured for the `src/` layout, so `pytest` works from a
fresh checkout after installing the dev dependencies.

## Release checklist

```bash
pytest
ruff check .
python -m build
```

## Community

- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [License (MIT)](LICENSE)
