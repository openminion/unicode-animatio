# unicode-animatio engineering patterns

This package intentionally has a small runtime surface: deterministic Unicode
frames, terminal helpers, a structural provider, and a local browser preview.

## Boundaries

1. Keep generated frames deterministic for identical inputs.
2. Keep the package useful without OpenMinion or another host framework.
3. Keep browser preview code local and dependency-light.
4. Keep compatibility aliases explicit and tested.
5. Treat examples as examples, not hidden public APIs.

## Implementation style

1. Prefer direct functions and immutable constants over layered wrappers.
2. Keep terminal output stable and readable.
3. Keep HTML generation and HTTP serving separated when either owner grows.
4. Avoid broad exception handling and unexplained type suppressions.
5. Use concise comments only for non-obvious constraints.

## Validation

Run `make check` before closing a change. Run `make release-check` when package
metadata, public exports, entrypoints, or wheel contents change. For broad
maintainability work, use the [Cleanup workflow](cleanup-workflow.md).
