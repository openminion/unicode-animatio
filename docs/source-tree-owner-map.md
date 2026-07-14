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
- `pyproject.toml`
  - packaging metadata, script entrypoints, and test/lint configuration

## Source package

- `src/unicode_animations/__init__.py`
  - package metadata, public exports, and compatibility aliases
- `src/unicode_animations/braille.py`
  - spinner frame data, grid helpers, and deterministic frame generation
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
- `.github/workflows/ci.yml`
  - GitHub Actions CI for test, Ruff, and build checks

## Tests

- `tests/test_braille.py`
  - grid-helper and spinner snapshot coverage
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

- `workspace-tmp/`
  - ad hoc cleanup, scan, or review artifacts
  - not part of the package contract and should stay uncommitted
