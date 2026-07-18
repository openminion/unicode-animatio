# unicode-animatio Cleanup Workflow

Use this workflow for cleanup, simplification, and maintainability work while
keeping the package lightweight and deterministic.

## Choose the right scope

1. Use a post-authoring pass for the files changed by one feature.
2. Use a bounded sweep for one package area or explicit file set.
3. Use a broad sweep only when every claimed source, test, example, or script
   file will receive an explicit review disposition.
4. Keep test cleanup separate when it changes frame snapshots or CLI/web proof.

Small local cleanup does not need a tracker. Broad cleanup needs a fresh
inventory and a ledger kept outside the committed package surface.

## Freeze the inventory

Before editing, inspect the worktree, preserve unrelated changes, list tracked
files with `git ls-files`, split source/tests/examples/scripts/docs when
needed, and record the exact count.

## Record every disposition

Use one ledger row per claimed file:

`path | area | before LOC | after LOC | disposition | rationale | validation`

Use `trim`, `keep`, `defer-owned:<issue>`, or
`defer-later:<reason>`. Close only when every row has a disposition and the
remaining count is zero.

## Keep the package small

Simplify duplicate frame data, pass-through wrappers, repeated CLI/web glue,
unnecessary commentary, and vague ownership. Preserve deterministic frame
ordering, compatibility aliases, CLI output, and browser-preview behavior.

## Validate

Use focused Ruff and pytest while editing. Close with:

```bash
make check
```

Run `make release-check` when packaging, public imports, entry points, or the
installed wheel changes. Refresh the inventory if the worktree moves during
validation.
