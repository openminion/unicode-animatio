# unicode-animatio code quality and hygiene

This is the public contributor baseline for `unicode-animatio`.

## Keep the package small and deterministic

1. Keep animation frames deterministic and easy to inspect.
2. Keep terminal, provider, and browser entrypoints thin over shared frame
   owners.
3. Avoid stateful runtime policy, semantic inference, and unrelated UI
   framework behavior.
4. Preserve the documented public exports and CLI contract.

## Keep ownership explicit

1. Frame data and grid helpers belong in `braille.py`.
2. Terminal behavior belongs in `cli.py`.
3. Application-facing frame catalogs belong in `provider.py`.
4. Local browser preview behavior belongs in `web.py`.
5. Tests, examples, and quality scripts support the package but do not enlarge
   its runtime API.

Avoid duplicate helpers, generic junk-drawer modules, hidden imports from
OpenMinion, and wrappers that only rename another function.

## Validate changes

Run the package gate from the repository root:

```bash
make check
```

`make check` combines formatting, Ruff, structural quality ratchets, and tests.
Known structural debt is recorded under `scripts/baselines/` and may only stay
flat or shrink.

Run `make release-check` for packaging or public-surface changes. Use
`make hooks-install` once per checkout and `make hooks-run` to reproduce all
pre-commit checks locally.

See [Engineering patterns](docs/engineering-patterns.md),
[Code quality enforcement](docs/code-quality-enforcement.md), and
[Cleanup workflow](docs/cleanup-workflow.md) for the detailed process.
