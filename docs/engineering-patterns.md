# unicode-animatio engineering patterns

Status: active
Last updated: 2026-11-01

This package intentionally has a small runtime surface: deterministic Unicode
frames, terminal helpers, a structural provider, and a local browser preview.

## Boundaries

1. Keep generated frames deterministic for identical inputs.
2. Keep the package useful without OpenMinion or another host framework.
3. Keep browser preview code local and dependency-light.
4. Keep compatibility aliases explicit and tested.
5. Treat examples as examples, not hidden public APIs.

## Ownership

1. `braille.py` owns the original braille data and deterministic grid/frame
   generation.
2. `catalog.py` owns canonical entries, categories, metadata, search, and label
   normalization shared by terminal, provider, and browser surfaces.
3. `cli.py` owns terminal parsing and presentation; it should consume catalog
   behavior instead of reimplementing search or metadata rules.
4. `provider.py` owns the structural application-facing adapter over public
   frame and catalog facts. It does not gain host-framework semantics.
5. `web.py` owns the local gallery payload, HTML, bounded server, and web CLI.
   Extract a focused owner if those responsibilities stop being readable
   together; do not create wrappers that only move names.

## Output and accessibility rules

1. Preserve exact frame order, dimensions, timing metadata, terminal safety,
   and stable scriptable output unless the public compatibility policy records
   an intentional change.
2. Normalize search and labels once in the catalog owner so CLI, provider, and
   browser results agree for empty, mixed-case, and Unicode input.
3. Keep the gallery keyboard reachable, visibly focused, responsive, and usable
   with reduced motion. Animation may pause or simplify; content and controls
   must remain available.
4. Escape untrusted display values and keep JSON/HTML payload construction
   structural. The local preview server must not become a general filesystem,
   proxy, or remote-execution surface.
5. Distinguish unit/HTTP proof from real browser interaction and visual proof.
   Use the browser-facing acceptance path when changing layout, keyboard,
   search interaction, or motion behavior.

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
