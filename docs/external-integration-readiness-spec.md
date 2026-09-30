# External Integration Readiness Assessment

Status: implemented locally; external blockers recorded

Date: 2026-09-30

Scope: the public Python API, terminal and browser CLIs, provider discovery,
packaging, release automation, documentation, and tests in `unicode-animatio`.
Agent reasoning, memory, orchestration, model routing, and unrelated framework
features are intentionally out of scope.

The findings below describe the assessed baseline at commit `435db2d`. Their
local resolution state is recorded in the paired execution tracker.

## Objective

Make the package dependable for external Python applications and agent
interfaces without turning it into a terminal framework. The package should
continue to own deterministic frame data, timing, catalog metadata, preview
tools, and one small structural provider. Host applications continue to own
lifecycle events, rendering, cancellation, accessibility policy, and task
state.

## Evidence reviewed

- Every tracked package file at commit `435db2d`, with source, test, script,
  example, documentation, workflow, and distribution surfaces inventoried
  separately.
- The current OpenMinion animation registry and validation path, including a
  live structural conformance run over all 58 presets.
- A baseline package run: `make check` passed with 335 tests and all structural
  validators clean.
- Current-source release checks plus separate fresh-environment installs of the
  published PyPI 0.0.10 wheel and forced source distribution on Python 3.11;
  the published wheel also passed a Python 3.14 runtime smoke.
- Current GitHub branch and environment settings for this repository.
- Current primary documentation for the relevant peer surfaces listed below.
- Three independent reviews covering the public surface, runtime API, and
  tests/releases.

## Relevant peer comparison

The comparison is limited to presentation and integration lessons that this
small data package can act on.

| Surface | Relevant current behavior | Concrete lesson for this package |
| --- | --- | --- |
| [OpenMinion](https://github.com/openminion/openminion) | Discovers `openminion.cli.animation_providers`, validates identifiers, frame safety, stable terminal width, and timing, then lets its renderer own lifecycle and fallback policy. | Keep the structural provider independent, and prove every shipped preset through the consumer registry. |
| [Codex CLI](https://learn.chatgpt.com/docs/config-file/config-reference) | Owns built-in terminal animations, lets users disable them, and exposes configured footer and terminal-title items. Its [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) provides structured automation output. | Document machine-readable discovery clearly; do not build a Codex adapter for an internal presentation owner. |
| [Claude Code](https://code.claude.com/docs/en/statusline) | Runs a command-backed status line from event data, with event-driven refresh and an optional interval whose minimum is one second. [Hooks](https://code.claude.com/docs/en/hooks) expose lifecycle events. | A host may map events to one static or selected frame, but the status line cannot faithfully drive this catalog's 60-250 ms animations. Do not add an unsuitable adapter. |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Owns a full terminal UI with streaming output and exposes structured CLI modes in its [command reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands). | Raw frames can be consumed by a renderer, but terminal ownership belongs in Hermes rather than this package. |
| [Gemini CLI](https://geminicli.com/docs/cli/headless/) | Exposes headless structured output for automation. | Stable JSON documentation matters more than another framework-specific integration. |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Is a provider-agnostic agent library focused on agents, tools, handoffs, sessions, guardrails, and tracing rather than terminal presentation. | Keep direct Python consumption framework-neutral and free of agent-runtime dependencies. |

There is no shared visual-provider protocol across these tools. A vendor
adapter, MCP server, ACP bridge, event bus, or renderer abstraction would add
parallel ownership without creating interoperable behavior.

## Findings and required changes

### P0: production publication is insufficiently constrained

The release workflow allows a manual run to select PyPI from any ref. Live
repository settings also show unprotected `main` and `dev` branches and no
protection rules or branch policy on the `pypi` and `testpypi` environments.
TestPyPI intentionally remains approval-free because it is the non-production
validation target; production PyPI requires the stronger policy.

Repository-owned change:

- make manual workflow runs TestPyPI-only;
- keep production publication tag-only;
- verify a pushed tag is exactly `v` plus the package version;
- let a duplicate or incorrect PyPI upload fail instead of using
  `skip-existing`.

External blocker:

- a repository administrator must configure branch protection and a PyPI
  environment approval/ref policy in GitHub.

### P1: release smoke can select a stale wheel

`scripts/release_check.py --skip-build-clean` retains old distributions and
then selects the lexicographically last filename. For example, `0.0.9` sorts
after `0.0.10`, so the option can validate the wrong artifact.

Required change: remove the option and always rebuild from an empty `build/`
and `dist/`.

### P1: installed metadata and provider discovery are under-tested

Source tests check entry-point text in `pyproject.toml`, but the fresh-wheel
smoke does not discover and load the installed entry point. The package also
uses deprecated license-table/classifier metadata, so PyPI does not expose a
license expression.

Required change:

- adopt SPDX `license = "MIT"` and `license-files = ["LICENSE"]`;
- remove the deprecated license classifier;
- assert the installed wheel's license expression, license file, provider
  entry point, provider identity, names, and one animation lookup.

### P1: the advertised typed surface is internally inconsistent

The wheel ships `py.typed` and advertises `Typing :: Typed`. A strict check of
the complete source package reports six errors across the catalog, provider,
CLI, and web owners. A separate external top-level import snippet reproduces
the two catalog/provider traversal errors. The causes are an invariant catalog
dictionary widening, metadata names typed only as `str`, a CLI list/index
mismatch, and an overly broad HTTP server address type.

Required change: correct the existing annotations and one justified address
cast. Do not add a typing runtime, wrapper, plugin, or new runtime dependency.

### P2: two CLI boundaries expose broken behavior

- Both browser entry paths accept ports outside `0..65535` and expose an
  internal `OverflowError` traceback.
- Explicit empty values for `--show` or the positional spinner name silently
  switch to list/default mode.

Required change: validate the port at argument parsing and use explicit
`is not None` mode selection. Preserve port `0` as automatic selection, accept
the valid upper bound `65535`, preserve an empty `--search ''` as the existing
unfiltered search, and keep the concise unknown-spinner error.

### P2: supported current Python versions are not in CI

The package declares Python 3.9 or newer, but metadata and CI stop at 3.12.
The complete suite passes on local Python 3.14.7.

Required change: add Python 3.13 and 3.14 classifiers and compatibility jobs.
Retain 3.9 because removing a documented compatibility version is a separate
breaking decision.

### P2: external integration contracts need sharper documentation

The JSON CLI exists but its shapes, stdout/stderr placement, failure behavior,
and additive field policy are not documented. It emits one complete JSON
document per invocation rather than a JSONL stream. The generic
`get_provider()` boundary can also be mistaken for automatic discovery across
frameworks, while the entry point group is specifically OpenMinion-owned.

Required change:

- document the three JSON record shapes, stdout/stderr behavior, exit statuses,
  non-streaming behavior, and beta compatibility rule;
- identify `get_provider()` as the generic Python surface;
- identify the entry point as OpenMinion-only automatic discovery;
- state that other hosts map their own lifecycle events and render frames;
- add the standardized PyPI `Release Notes` project URL;
- remove the release guide's inaccessible cross-repository documentation
  reference.

Published-impact blocker: PyPI artifacts are immutable. The metadata and
README improvements in this change will appear on PyPI only in a future
versioned release; publishing a new package version is outside this change.

## Explicit non-goals

- No agent framework, terminal UI, async renderer, progress model, or event
  loop.
- No Codex, Claude, Hermes, Gemini, Rich, Textual, MCP, or ACP adapter.
- No runtime fallback, retry ladder, broad exception handling, or alias
  guessing.
- No runtime dependency added to the zero-runtime-dependency package.
- No new schema framework for the small documented JSON surface.
- No version bump or package publication in this change.

## Acceptance criteria

1. Invalid ports and empty explicit names produce concise CLI errors without
   tracebacks or mode changes.
2. MyPy 1.20.2 passes both
   `mypy --strict --python-version 3.9 src/unicode_animations` and
   `MYPYPATH=src mypy --strict --python-version 3.9 -c 'from unicode_animations import get_provider, metadata_for_spinner, spinners'`.
   This remains recorded one-off proof for the six known errors, not a package
   dependency or new gate.
3. A separate integration probe, not package CI, proves all 58 presets against
   the OpenMinion registry at commit `b1c966534`.
4. The release check always removes stale `build/` and `dist/` content before
   producing artifacts. Its wheel and source distributions include `LICENSE`
   and expose `License-Expression: MIT` plus `License-File: LICENSE`; the
   installed wheel also exposes both console scripts, the type marker, and a
   loadable provider entry point.
5. Python 3.9 through 3.14 are declared and pass the compatibility CI matrix,
   with available local current-Python proof recorded separately.
6. Manual dispatch can publish only to TestPyPI; PyPI can run only from a
   matching version tag; tag/version mismatch fails before publication; and
   the production upload does not use `skip-existing`.
7. The JSON contract records success as exit `0`, unknown spinner as exit `1`,
   and argument misuse as exit `2`, with data on stdout and errors on stderr.
8. The public docs distinguish generic import, OpenMinion discovery, and host
   rendering responsibilities; document the categories-array,
   list/search-array, and show-object JSON shapes; state the additive beta
   field policy; expose the Release Notes URL; and contain no inaccessible
   release-process reference.
9. `make check`, `make hooks-run`, and `make release-check` pass from the
   package root.

## Review decisions

The three reviewers agreed that the package's existing owner boundaries are
sound and that all 58 animation records conform to OpenMinion. Their findings
were reconciled into the items above. Proposed framework adapters, a schema
generator, a dedicated documentation site, runtime recovery branches, and new
dependencies were rejected as unrelated or disproportionate.
