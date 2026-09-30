# unicode-animatio Docs

This directory is the package-local documentation root for
`unicode-animatio`, a standalone package for deterministic terminal animation
frames, preset metadata, and local preview tools.

## Start Here

| If you want to... | Read |
| --- | --- |
| Install the package and run a first preset | [Getting started](getting-started.md) |
| Browse the catalog visually or script preset discovery | [Getting started](getting-started.md) |
| Understand package ownership and file layout | [Source tree owner map](source-tree-owner-map.md) |
| Contribute without adding avoidable complexity | [Engineering patterns](engineering-patterns.md) |
| Run the expected checks | [Code quality enforcement](code-quality-enforcement.md) |
| Do broad cleanup safely | [Cleanup workflow](cleanup-workflow.md) |

## Root Package Docs

- [README](../README.md): public package overview, CLI examples, catalog notes,
  and brand/security boundary.
- [API compatibility](../API_COMPATIBILITY.md): supported import roots and
  stability posture.
- [Code quality](../CODE_QUALITY.md): contributor quality rules.
- [Release guide](../RELEASING.md): package release flow.

## Assessment Records

- [External integration readiness assessment](external-integration-readiness-spec.md)
  and [execution tracker](external-integration-readiness-tracker.md): dated
  contributor evidence for the 2026-09-30 readiness pass.

## Public Package Boundary

These docs are for external users and contributors. Keep them portable, avoid
machine-local path assumptions, and describe `unicode-animatio` as a standalone
Python distribution rather than as an OpenMinion-only implementation detail.
