# unicode-animations Getting Started

Status: active

Purpose: give contributors and automation authors a package-local bootstrap
and execution summary for work inside the `unicode-animations` repo.

## Fast bootstrap

```bash
cd unicode-animations
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

## Validation baseline

```bash
python3 -m pytest -q
python3 -m ruff check .
python3 scripts/release_check.py
```
