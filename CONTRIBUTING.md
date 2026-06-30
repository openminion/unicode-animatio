# Contributing to unicode-animations

Thanks for your interest in improving `unicode-animations`.

## Read first

1. [README.md](./README.md)
2. [API_COMPATIBILITY.md](./API_COMPATIBILITY.md)
3. [docs/README.md](./docs/README.md)
4. [docs/getting-started.md](./docs/getting-started.md)
5. [docs/source-tree-owner-map.md](./docs/source-tree-owner-map.md)
6. [RELEASING.md](./RELEASING.md) when the work affects packaging or release
   behavior

Treat the package README and API compatibility policy as the stable public
contract. `unicode-animations` ships deterministic frame data, CLI helpers, and
simple browser preview support. It should stay lightweight and dependency-aware.

## Development setup

Requires Python 3.11+ for the shared local quality loop.

```bash
# 1. Clone and enter the repo
git clone https://github.com/openminion/unicode-animations.git unicode-animations
cd unicode-animations

# 2. Create and activate a virtualenv
python3.11 -m venv .venv
source .venv/bin/activate

# 3. Install in editable mode with dev extras
make dev-install

# 4. Install local hooks, including commit-message enforcement
make hooks-install
```

## Running tests

```bash
# Full package test suite
make test

# Full local quality gate
make check

# Release/install smoke
make release-check
```

If you need a narrower loop while iterating, run `python3.11 -m pytest -q
tests/<target>` inside the activated virtualenv.

## Running lint and formatting

```bash
# Lint only
make lint

# Check formatting without rewriting files
make format-check

# Apply formatting and autofixes
make fix
```

If pre-commit, `make hooks-run`, or GitHub Actions reports formatter changes,
run `make fix`, review the diff, rerun `make check`, and recommit before
pushing again.

## Running the demos

Terminal demo (Python API):

```bash
python examples/terminal_demo.py
```

CLI demo:

```bash
unicode-animations --list
unicode-animations helix
unicode-animations --web
```

## Development basics

1. Keep pull requests focused and small when possible.
2. Include tests for behavior changes.
3. Keep frame definitions deterministic and easy to inspect.
4. Avoid growing the package into a stateful runtime or unrelated UI framework.
5. Keep docs and examples copy/paste friendly.

Commit message guidance:

1. Use commit messages in the form `<type>: <summary>` or
   `<type>(<scope>): <summary>`.
2. Approved current types are `feat`, `fix`, `docs`, `refactor`, `test`,
   `chore`, `style`, and `build`.
3. In this package, scope is optional but encouraged when it improves owner
   clarity, for example `cli`, `web`, `braille`, `docs`, or `release`.
4. Keep the summary specific to the landed change and avoid vague messages like
   `update`.
5. Prefer the most specific truthful type; do not use `chore` when `docs`,
   `test`, `refactor`, or `build` is more accurate.
6. Do not use local shorthand or planning labels as normal commit types.

The same policy runs locally through `make hooks-install` and again in GitHub
Actions on pull requests plus `dev`/`main` pushes.

Preferred PR shape:

`Improve browser preview packaging checks`

- add ...
- align ...
- document ...

Validation
- `<command>`
- `<command>`

## Pull requests

1. Be respectful and collaborative. Please follow the
   [Code of Conduct](CODE_OF_CONDUCT.md).
2. Make your change; add or update tests; run the relevant local validation.
3. Open a PR with a clear summary. Use a short GitHub-native title, then flat
   line-item bullets, then a plain `Validation` label with exact command
   bullets.
4. Keep PRs focused and reviewable.

## Reporting issues

If you find a bug or have a feature request, please open an issue with:

1. What you expected to happen
2. What happened instead
3. Steps to reproduce
4. Python version and OS details

## License

By contributing to this project, you agree that your contributions will be
licensed under the [MIT License](LICENSE).
