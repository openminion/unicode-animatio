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

## Comment and docstring review

This rule applies to every contributor and coding agent, including tests and
scripts. Let clear names, types and direct control flow explain ordinary steps.
Review every added or changed comment and docstring in the final diff; remove
obvious restatements, decorative banners and duplicated walkthroughs. Keep one
concise explanation at the owner when a constraint is not obvious.

Preserve public API and model-facing descriptions, required notices/directives,
and useful safety, compatibility and regression-oracle rationale. Keep short
factual module explainers; move longer design/history narratives to docs.
Passing automated checks does not replace this review, and there is no comment
quota. Check current source and existing reports before filing cleanup debt;
keep unrelated cleanup out of a feature PR.

## Minimum usable code

These rules apply to maintainers, external contributors and coding agents, in
new work and cleanup of merged code. Start with actual callers, supported inputs
and concrete failure paths. Use the existing owner and a direct implementation;
add a helper or abstraction only when current callers need it.

Do not add speculative frameworks, unused modes or extension points,
pass-through wrappers, duplicate validation, silent defaults, blanket exception
handling, or retries that hide failures. Validate at the boundary that owns the
contract instead of repeatedly normalizing internal values. A retry needs a
specific transient failure, a bound and safe repeat behavior. Preserve necessary
trust-boundary checks, permissions, compatibility, persistence/replay and cleanup.

Preserve deterministic frame generation, provider contracts and terminal/browser
cleanup. Keep the standalone package lightweight.

## Review and cleanup evidence

Review the complete final diff and every new delta for simplicity and the
[comment and docstring rules](#comment-and-docstring-review). Record the exact
reviewed head, checked callers, supported failure cases, findings and disposition
in the PR or linked review evidence. Passing automated checks does not replace
this review. Block approval or merge while a substantiated finding remains;
request the smaller existing-owner change when it satisfies the same contract.
Validate the current integration with the target branch and require all required
hosted checks on the exact head before merging. Never relax a gate to land cleanup.

For merged work, first verify that the code still exists on the current
development branch. Reuse existing findings and respect active ownership; record
obsolete findings without reopening old PRs, duplicating issues or taking over
another contributor's branch. Do not label all historical code clean from a
partial review.

A broad cleanup starts with a fresh file inventory at a recorded revision. Keep
source, tests and scripts separate, give each claimed file a trim, keep or explicit
defer disposition, and work in bounded tranches. Record callers, rationale,
validation and remaining work after each tranche; deferred files remain open.
Refresh evidence if the tree changes during validation. Record before/after LOC
for source cleanup and retain a simplification only when it reduces code and
improves readability while preserving the contract. Review the changed files
again after authoring; this is not proof of a package-wide sweep.

Preserve test assertions and negative controls. Do not introduce skips, expected
failures, extra waits or retries to conceal a regression. Preserve script output,
exit behavior and operator clarity. Run the repository's documented gates and
report local, hosted, installed-package and live-system evidence separately.
