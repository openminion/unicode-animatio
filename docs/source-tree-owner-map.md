# unicode-animatio source tree owner map

This document maps the main source and support files in the package so the
public package boundary stays explicit.

## Root package surfaces

- `README.md`
  - public package overview, install, quickstart, and CLI/demo entrypoints
- `API_COMPATIBILITY.md`
  - public import roots, public names, and compatibility expectations
- `RELEASING.md`
  - package-local release contract and validation sequence
- `CODE_QUALITY.md`
  - public contributor quality and hygiene baseline
- `pyproject.toml`
  - packaging metadata, script entrypoints, and test/lint configuration

## Source package

- `src/unicode_animations/__init__.py`
  - package metadata, public exports, and compatibility aliases
- `src/unicode_animations/braille.py`
  - original braille frame data, grid helpers, and deterministic frame generation
- `src/unicode_animations/catalog.py`
  - canonical mixed Unicode/ASCII catalog, categories, and compatibility names
- `src/unicode_animations/cli.py`
  - terminal preview CLI
- `src/unicode_animations/provider.py`
  - structural provider entry point for applications that consume frame data
- `src/unicode_animations/web.py`
  - local browser demo server and web CLI
- `src/unicode_animations/__main__.py`
  - `python -m unicode_animations` entrypoint

## Support surfaces

- `examples/terminal_demo.py`
  - Python-API demo for local manual preview
- `scripts/release_check.py`
  - package-local release validation helper
- `scripts/validate_quality_patterns.py`
  - structural quality ratchets shared by local checks, hooks, and CI
- `scripts/baselines/`
  - current accepted structural findings; new debt must not exceed them
- `.github/workflows/quality.yml`
  - pull-request and protected-branch quality checks
- `.github/workflows/release.yml`
  - tagged package build and publish workflow

## Tests

- `tests/test_braille.py`
  - grid-helper and spinner snapshot coverage
- `tests/test_catalog.py`
  - canonical catalog, category, snapshot, and terminal-safety conformance
- `tests/test_cli.py`
  - terminal CLI contract checks
- `tests/test_provider.py`
  - structural provider and catalog conformance checks
- `tests/test_web.py`
  - local browser demo payload and HTTP coverage
- `tests/test_package.py`
  - compatibility alias coverage
- `tests/test_package_layout.py`
  - public docs/layout regression checks
- `tests/test_package_metadata.py`
  - package metadata and version-alignment checks

## Non-source artifacts

- Ad hoc cleanup, scan, and review artifacts belong in the containing
  workspace's external scratch root.
- Do not create a package-local scratch tree or commit those artifacts; they
  are not part of the package contract.
