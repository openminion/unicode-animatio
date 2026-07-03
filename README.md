<p align="center">
  <img src="https://www.openminion.com/brand/openminion-logo.png" alt="OpenMinion logo" width="128" />
</p>

<h1 align="center">unicode-animatio</h1>

<p align="center">
  <strong>Lightweight Unicode braille spinner animations for Python.</strong>
</p>

<p align="center">
  <a href="https://github.com/openminion/unicode-animatio">GitHub</a>
  · <a href="#install">Install</a>
  · <a href="#what-the-package-provides">What Ships</a>
  · <a href="https://www.openminion.com">Website</a>
  · <a href="https://x.com/OpenMinion">X</a>
</p>

<p align="center">
  <img alt="Package version" src="https://img.shields.io/badge/package-0.1.0-3775A9">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-3775A9">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <img alt="Status" src="https://img.shields.io/badge/status-beta-5B8DEF">
</p>

- 18 spinner families as raw frame data
- typed Python API with JS-style compatibility aliases
- built-in terminal preview CLI and local browser demo
- no runtime dependencies

`unicode-animatio` is the public package and repo name. The Python import root
remains `unicode_animations`, while the public CLI entrypoints use
`unicode-animatio` and `unicode-animatio-web`.

## Official project links

- GitHub: `https://github.com/openminion/unicode-animatio`
- Issues: `https://github.com/openminion/unicode-animatio/issues`

## What the package provides

`unicode-animatio` provides:

- immutable spinner frame data via `unicode_animations.spinners`
- braille-grid helpers: `make_grid` and `grid_to_braille`
- compatibility aliases: `makeGrid` and `gridToBraille`
- a terminal preview CLI: `unicode-animatio`
- a local web preview CLI: `unicode-animatio-web`

## What the package does not provide

This package does not provide:

- async terminal rendering frameworks
- progress bars, task orchestration, or job-state tracking
- hosted demo infrastructure or remote APIs
- framework-specific adapters for Rich, Textual, or Typer

## Install

Install from PyPI:

```bash
python3 -m pip install unicode-animatio
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
unicode-animatio --list
unicode-animatio
unicode-animatio helix
```

Local browser demo:

```bash
unicode-animatio --web
unicode-animatio-web --port 8765
unicode-animatio-web --host 0.0.0.0 --port 8765 --no-open
```

Python API terminal demo:

```bash
python examples/terminal_demo.py
python examples/terminal_demo.py --seconds-per-spinner 2 --loops 2
python examples/terminal_demo.py helix
python examples/terminal_demo.py --list
```

## Available animations

The package currently ships these braille spinner families. The preview glyph is
the first frame from each animation:

| Name | Preview | Frames | Interval |
| --- | --- | ---: | ---: |
| `braille` | `⠋` | 10 | 80ms |
| `braillewave` | `⠁⠂⠄⡀` | 8 | 100ms |
| `dna` | `⠋⠉⠙⠚` | 12 | 80ms |
| `scan` | `⠀⠀⠀⠀` | 10 | 70ms |
| `rain` | `⢁⠂⠔⠈` | 12 | 100ms |
| `scanline` | `⠉⠉⠉` | 6 | 120ms |
| `pulse` | `⠀⠶⠀` | 5 | 180ms |
| `snake` | `⣁⡀` | 16 | 80ms |
| `sparkle` | `⡡⠊⢔⠡` | 6 | 150ms |
| `cascade` | `⠀⠀⠀⠀` | 14 | 60ms |
| `columns` | `⡀⠀⠀` | 26 | 60ms |
| `orbit` | `⠃` | 8 | 100ms |
| `breathe` | `⠀` | 17 | 100ms |
| `waverows` | `⠖⠉⠉⠑` | 16 | 90ms |
| `checkerboard` | `⢕⢕⢕` | 4 | 250ms |
| `helix` | `⢌⣉⢎⣉` | 16 | 80ms |
| `fillsweep` | `⣀⣀` | 11 | 100ms |
| `diagswipe` | `⠁⠀` | 16 | 60ms |

For a live preview:

```bash
unicode-animatio --list
unicode-animatio helix
unicode-animatio --web
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

- Official GitHub: `https://github.com/openminion/unicode-animatio`
- Official website: `https://www.openminion.com`
- Official X account: `https://x.com/OpenMinion`

`unicode-animatio` has no official token, coin, NFT, airdrop, staking
program, treasury product, or investment offering. Any claim otherwise is
unauthorized and should be treated as a scam.

## License and brand-use boundary

- Source code license: `MIT`
- Brand/trademark grant: `none`

The software license grants rights to use, modify, and redistribute the code.
It does **not** grant rights to use the unicode-animatio or OpenMinion
names, logos, branding, website identity, or social identity except for
truthful attribution. Forks, clones, and derivative distributions must not
present themselves as the official unicode-animatio package or imply
affiliation, endorsement, or maintenance by unicode-animatio or OpenMinion
contributors unless that is actually true.

## Community

- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [License (MIT)](LICENSE)
