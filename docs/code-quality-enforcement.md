# unicode-animatio code quality enforcement

The repository keeps local development, pre-commit, and GitHub Actions aligned
around the same package-owned commands.

## Local gates

```bash
make format-check
make lint
make validate-patterns
make test
make check
```

`make check` is the normal closeout command.

## Structural ratchets

`scripts/validate_quality_patterns.py` checks file and method size, duplicate
private helpers, path and filename drift, broad exception handling, bare type
ignores, and public-package boundary drift. The current accepted findings live
under `scripts/baselines/` so new debt fails locally and in CI.

Do not raise a baseline merely to make a change pass. Prefer simplifying the
new code or extracting the correct owner.

## Hooks and CI

Install hooks with `make hooks-install` and reproduce them with
`make hooks-run`. `.github/workflows/quality.yml` runs the formatter, Ruff,
ratchets, tests, and package build checks for pull requests and protected branch
pushes.

Run `make release-check` when release metadata, exports, command entrypoints,
or wheel contents change. Follow [Cleanup workflow](cleanup-workflow.md) for
broad sweeps that claim complete package coverage.
