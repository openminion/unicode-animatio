# Releasing `unicode-animatio`

Status: `beta`
Scope: package-local release contract for the standalone
`unicode-animatio` distribution

Naming note: the public distribution and CLI names use `unicode-animatio`,
while the source package and import root remain `unicode_animations`.

## Release contract

A publishable release must satisfy all of the following:

1. `pyproject.toml` and `src/unicode_animations/__init__.py` agree on the
   version.
2. `README.md` describes install, quickstart, CLI usage, and public package
   boundaries for external consumers.
3. `API_COMPATIBILITY.md` reflects the public import roots and compatibility
   aliases.
4. `docs/README.md` remains the package-local docs index.
5. `docs/source-tree-owner-map.md` remains the package-local owner map.
6. Package tests pass from the package root.
7. Ruff passes from the package root.
8. Both wheel and sdist build successfully.
9. A fresh-wheel install smoke passes from a temporary virtualenv.

## Version bump

Update:

- `pyproject.toml`
- `src/unicode_animations/__init__.py`

If the public contract changes, also update:

- `README.md`
- `API_COMPATIBILITY.md`
- `docs/README.md`
- `docs/source-tree-owner-map.md`

## Build and validation

Preferred deterministic release check:

```bash
python3 scripts/release_check.py
```

Manual equivalent:

```bash
python3 -m pytest -q
python3 -m ruff check .
python3 -m build
```

Fresh-install smoke:

```bash
TMP_VENV="$(mktemp -d)/unicode-animatio-venv"
python3 -m venv "$TMP_VENV"
"$TMP_VENV/bin/pip" install dist/unicode_animatio-*.whl
"$TMP_VENV/bin/unicode-animatio" --list
```

## Publish sequence

`unicode-animatio` follows the shared repo-family release flow documented in
`docs/reference/package-release-process.md`:

1. prepare and validate an RC branch,
2. push an RC tag such as `v0.0.2rc1` to publish to TestPyPI,
3. install and smoke-test the RC artifact from TestPyPI,
4. prepare and validate the final non-RC branch,
5. dispatch the `Release` workflow from that final branch with
   `target=testpypi`,
6. install and smoke-test the final TestPyPI artifact,
7. push the final non-RC tag such as `v0.0.2` to publish to PyPI,
8. create the GitHub Release using the bare version title, such as `0.0.2`.

## GitHub Actions Trusted Publishing

The canonical release workflow for this package is
`.github/workflows/release.yml`.

Trusted publishing must be configured for:

1. TestPyPI environment: `testpypi`
2. PyPI environment: `pypi`

## Notes

1. This package is intentionally standalone and should not depend on
   OpenMinion runtime modules.
2. Build outputs such as `build/`, `dist/`, and `*.egg-info` are release
   artifacts, not source-of-truth package content.
