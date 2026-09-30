# unicode-animatio Getting Started

Status: active

Purpose: give contributors and automation authors a package-local bootstrap
and execution summary for work inside the `unicode-animatio` repo.

## Fast bootstrap

```bash
cd unicode-animatio
make dev-install
source .venv/bin/activate
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
unicode-animatio --search knowledge --category graph
unicode-animatio --show edgepulse --json
unicode-animatio edgepulse --color auto --foreground gray
unicode-animatio --web --port 8765
```

The package exposes raw frames and timing. Terminal and browser renderers own
foreground color, backgrounds, labels, layout, and reduced-motion behavior.
The browser preview models the intended integration controls: category filters,
search, reduced motion, selected-preset details, and copyable provider snippets.
It follows system color and motion preferences until the user makes a saved
choice, supports arrow-key preset selection, and exposes live copy and
filter-result status to assistive technology.

Category-aware Python API:

```python
from unicode_animations import (
    SPINNER_CATEGORIES,
    metadata_for_spinner,
    search_spinner_names,
    spinner_names_for_category,
)

print(spinner_names_for_category("graph"))
print(SPINNER_CATEGORIES["edgepulse"])
print(search_spinner_names("knowledge", category="graph"))
print(metadata_for_spinner("edgepulse").tags)
```

Provider integrations can request a synchronized wider animation without
changing its timing:

```python
from unicode_animations import get_provider

animation = get_provider().get("edgepulse", length=3)
print(animation.frames)
```

Direct `get_provider()` imports work in any Python host. The installed
`openminion.cli.animation_providers` entry point is only for OpenMinion's
automatic discovery. Other hosts retain their own lifecycle-event and renderer
integration.

## Validation baseline

```bash
make check
```

Run `make release-check` when packaging, public imports, entry points, or wheel
contents change.
