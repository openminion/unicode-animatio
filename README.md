<p align="center">
  <img src="https://www.openminion.com/brand/openminion-logo.png" alt="OpenMinion logo" width="128" />
</p>

<h1 align="center">unicode-animatio</h1>

<p align="center">
  <strong>Lightweight Unicode and ASCII terminal animations for Python.</strong>
</p>

<p align="center">
  <a href="https://github.com/openminion/unicode-animatio">GitHub</a>
  · <a href="#install">Install</a>
  · <a href="#what-the-package-provides">What Ships</a>
  · <a href="https://www.openminion.com">Website</a>
  · <a href="https://x.com/OpenMinion">X</a>
</p>

<p align="center">
  <img alt="Package version" src="https://img.shields.io/badge/package-0.0.2-3775A9">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-3775A9">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue"></a>
  <img alt="Status" src="https://img.shields.io/badge/status-beta-5B8DEF">
</p>

- 58 terminal animation families as raw frame data
- 10 categories for browsing and selection
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
- canonical names and categories via `SPINNER_NAMES`, `CATEGORY_NAMES`, and
  `SPINNER_CATEGORIES`
- braille-grid helpers: `make_grid` and `grid_to_braille`
- compatibility aliases: `makeGrid` and `gridToBraille`
- a structural animation provider entry point for consumers such as OpenMinion
- a terminal preview CLI: `unicode-animatio`
- a local web preview CLI: `unicode-animatio-web`

## What the package does not provide

This package does not provide:

- async terminal rendering frameworks
- progress bars, task orchestration, or job-state tracking
- ANSI styling, background colors, or status text in frame data
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

Provider boundary:

```python
from unicode_animations import get_provider

provider = get_provider()
spec = provider.get("helix")
print(provider.provider_id)
print(spec.frames)
print(spec.interval_ms)
```

The provider returns raw frame strings and timing only. Foreground colors,
backgrounds, reduced-motion behavior, labels, and layout remain owned by the
rendering application.

## CLI and demos

Terminal preview:

```bash
unicode-animatio --list
unicode-animatio --categories
unicode-animatio --list --category graph
unicode-animatio
unicode-animatio helix
unicode-animatio edgepulse
unicode-animatio helix --color auto --foreground gray
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

The package ships 58 deterministic animations across 10 categories:

| Category | Presets |
| --- | --- |
| `subtle` | `braille`, `pulse`, `orbit`, `breathe`, `softdot`, `slowbreath`, `quietorbit`, `dimwave` |
| `scan` | `scan`, `scanline`, `snake`, `diagswipe`, `hscan`, `vscan`, `radar`, `focusbeam` |
| `build` | `blocks`, `stack`, `assemble`, `brickline` |
| `thinking` | `ellipsis`, `mindwave`, `synapse`, `neuron` |
| `tool` | `terminalblink`, `gearspin`, `wrench`, `sparkplug` |
| `data` | `braillewave`, `dna`, `rain`, `cascade`, `columns`, `waverows`, `helix`, `bitstream`, `packetflow`, `matrixrain`, `columns2` |
| `graph` | `nodes`, `edgepulse`, `cluster`, `orbitnodes` |
| `progress` | `fillsweep`, `meter`, `ladder`, `risingblocks`, `fillbar2` |
| `alert` | `sparkle`, `warningpulse`, `heartbeat`, `ping`, `flashdot` |
| `dense` | `checkerboard`, `plasma`, `noise`, `moire`, `shimmergrid` |

Selected first-frame examples:

| Name | Category | First frame | Interval |
| --- | --- | --- | ---: |
| `braille` | `subtle` | `⠋` | 80ms |
| `focusbeam` | `scan` | `----` | 90ms |
| `synapse` | `thinking` | `*..` | 100ms |
| `terminalblink` | `tool` | `$_` | 160ms |
| `packetflow` | `data` | `[>]---` | 100ms |
| `edgepulse` | `graph` | `o---o` | 90ms |
| `meter` | `progress` | `[   ]` | 120ms |
| `shimmergrid` | `dense` | `.+.` | 90ms |

## Choosing a preset

- Use `subtle` for calm background activity.
- Use `scan` or `data` for indexing and retrieval work.
- Use `thinking` for model activity and `tool` for command execution.
- Use `graph` for relation traversal and knowledge-graph work.
- Use `progress` when steady forward motion matters.
- Use `alert` sparingly for attention states.

For a live preview:

```bash
unicode-animatio --list
unicode-animatio --categories
unicode-animatio --list --category graph
unicode-animatio edgepulse --foreground gray
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
