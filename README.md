# unicode-animations

Lightweight Unicode braille spinner animations for Python.

- 18 spinner families as raw frame data
- typed Python API with JS-style compatibility aliases
- built-in terminal preview CLI and local browser demo
- no runtime dependencies

## Official project links

- GitHub: `https://github.com/openminion/unicode-animations`
- Issues: `https://github.com/openminion/unicode-animations/issues`

## What the package provides

`unicode-animations` provides:

- immutable spinner frame data via `unicode_animations.spinners`
- braille-grid helpers: `make_grid` and `grid_to_braille`
- compatibility aliases: `makeGrid` and `gridToBraille`
- a terminal preview CLI: `unicode-animations`
- a local web preview CLI: `unicode-animations-web`

## What the package does not provide

This package does not provide:

- async terminal rendering frameworks
- progress bars, task orchestration, or job-state tracking
- hosted demo infrastructure or remote APIs
- framework-specific adapters for Rich, Textual, or Typer

## Install

From PyPI:

```bash
python3 -m pip install unicode-animations
```

Editable install during local development:

```bash
python3 -m pip install -e ".[dev]"
```

## Quick start

```python
from unicode_animations import spinners

spinner = spinners["braille"]
print(spinner.frames)
print(spinner.interval)
```

Grid helpers:

```python
from unicode_animations import grid_to_braille, make_grid

grid = make_grid(4, 4)
grid[0][0] = True
grid[1][1] = True
grid[2][2] = True
grid[3][3] = True

print(grid_to_braille(grid))
```

## CLI and demos

Terminal preview:

```bash
unicode-animations --list
unicode-animations
unicode-animations helix
```

Local browser demo:

```bash
unicode-animations --web
unicode-animations-web --port 8765
unicode-animations-web --host 0.0.0.0 --port 8765 --no-open
```

Python API terminal demo:

```bash
python examples/terminal_demo.py
python examples/terminal_demo.py --seconds-per-spinner 2 --loops 2
python examples/terminal_demo.py helix
python examples/terminal_demo.py --list
```

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
python3 -m pytest -q
python3 -m ruff check .
python3 -m build
```

## Package docs

- [Getting started](docs/getting-started.md)
- [Package docs index](docs/README.md)
- [API compatibility](API_COMPATIBILITY.md)
- [Release guide](RELEASING.md)
- [Source tree owner map](docs/source-tree-owner-map.md)

## Trust and Brand Safety

- Official GitHub: `https://github.com/openminion/unicode-animations`
- Official website: `https://www.openminion.com`
- Official X account: `https://x.com/OpenMinion`

`unicode-animations` has no official token, coin, NFT, airdrop, staking
program, treasury product, or investment offering. Any claim otherwise is
unauthorized and should be treated as a scam.

## License and brand-use boundary

- Source code license: `MIT`
- Brand/trademark grant: `none`

The software license grants rights to use, modify, and redistribute the code.
It does **not** grant rights to use the unicode-animations or OpenMinion
names, logos, branding, website identity, or social identity except for
truthful attribution. Forks, clones, and derivative distributions must not
present themselves as the official unicode-animations package or imply
affiliation, endorsement, or maintenance by unicode-animations or OpenMinion
contributors unless that is actually true.

## Community

- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [License (MIT)](LICENSE)
