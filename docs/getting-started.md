# unicode-animatio Getting Started

Status: active

Purpose: give contributors and automation authors a package-local bootstrap
and execution summary for work inside the `unicode-animatio` repo.

## Fast bootstrap

```bash
cd unicode-animatio
python3.11 -m venv .venv
source .venv/bin/activate
python3.11 -m pip install -e ".[dev]"
```

## Read first

Before substantial code changes, read:

1. [`../README.md`](../README.md)
2. [`../CONTRIBUTING.md`](../CONTRIBUTING.md)
3. [`README.md`](README.md)

## Normal execution loop

1. Pick one focused change.
2. Update code and docs together when the public surface changes.
3. Add or update tests for the behavior you changed.
4. Run the smallest validation that proves the change.
5. Record validation commands in the PR description.

## Browse and preview animations

```bash
unicode-animatio --categories
unicode-animatio --list --category graph
unicode-animatio edgepulse --color auto --foreground gray
unicode-animatio-web --port 8765
```

The package exposes raw frames and timing. Terminal and browser renderers own
foreground color, backgrounds, labels, layout, and reduced-motion behavior.

Category-aware Python API:

```python
from unicode_animations import SPINNER_CATEGORIES, spinner_names_for_category

print(spinner_names_for_category("graph"))
print(SPINNER_CATEGORIES["edgepulse"])
```

## Validation baseline

```bash
python3 -m pytest -q
python3 -m ruff check .
python3 scripts/release_check.py
```
