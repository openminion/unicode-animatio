# External Integration Readiness Tracker

Status: local-complete / external-blocked; pull-request CI pending

Spec: [External integration readiness assessment](external-integration-readiness-spec.md)

| ID | Priority | Work item | Owner/files | Acceptance evidence | Status |
| --- | --- | --- | --- | --- | --- |
| UAR-01 | P0 | Make manual releases TestPyPI-only and production releases tag-only. | `.github/workflows/release.yml`, `RELEASING.md` | Workflow conditions and docs agree. | done |
| UAR-02 | P1 | Match release tags to package versions and fail duplicate production uploads. | `.github/workflows/release.yml` | Matching tag/version passes, mismatch fails before publish, and PyPI omits `skip-existing`. | done |
| UAR-03 | P1 | Remove stale-distribution reuse from release validation. | `scripts/release_check.py` | Every release check cleans and rebuilds before smoke testing. | done |
| UAR-04 | P1 | Modernize license metadata and test built metadata plus the installed entry point. | `pyproject.toml`, `scripts/release_check.py`, tests | Wheel and sdist license metadata/content plus fresh-wheel provider discovery pass. | done |
| UAR-05 | P1 | Repair public type consistency without adding runtime dependencies or new abstractions. | `catalog.py`, `provider.py`, `cli.py`, `web.py` | Strict full-source and external-consumer checks pass for Python 3.9. | done |
| UAR-06 | P2 | Reject invalid web ports at both CLI boundaries. | `cli.py`, `web.py`, CLI/web tests | `-1` and `65536` fail through argparse; `0` and `65535` still parse. | done |
| UAR-07 | P2 | Treat empty explicit spinner names as invalid selections. | `cli.py`, CLI tests | Empty `--show` and positional names fail; empty `--search` remains unfiltered. | done |
| UAR-08 | P2 | Cover supported current Python versions. | `pyproject.toml`, quality workflow | Python 3.9 through 3.14 pass the compatibility matrix. | implemented; CI pending |
| UAR-09 | P2 | Document JSON and provider integration contracts. | `README.md`, `API_COMPATIBILITY.md`, docs | Shapes, output channels, exit statuses, compatibility, generic import, and OpenMinion discovery are explicit. | done |
| UAR-10 | P2 | Remove the inaccessible release-process reference. | `RELEASING.md` | Release flow is self-contained. | done |
| UAR-11 | P3 | Expose release notes through package metadata. | `pyproject.toml`, metadata tests | Standard `Release Notes` URL is present. | done |
| UAR-12 | external | Configure GitHub branch and publishing-environment protection. | GitHub repository settings | Administrator-configured protection is visible through GitHub API. | blocked-external |
| UAR-13 | external | Publish these metadata and README improvements to PyPI in a future version. | Future release | A new immutable PyPI artifact exposes the updated metadata and long description. | deferred-external |

## Validation ledger

| Check | Result |
| --- | --- |
| Baseline `make check` | Passed: 335 tests; all format, lint, and structural checks clean. |
| OpenMinion registry conformance | Passed: all 58 presets accepted at OpenMinion commit `b1c966534`. |
| Published PyPI 0.0.10 wheel and forced-sdist probes | Passed in fresh Python 3.11 environments; wheel also passed Python 3.14 smoke. |
| Python 3.14 full source suite | Passed: 347 tests on Python 3.14.7. |
| Post-change OpenMinion registry conformance at `b1c966534` | Passed: all 58 presets accepted. |
| MyPy 1.20.2 one-off 3.9-target source and consumer checks | Passed with no issues. |
| Installed CLI boundary probes | Passed: bad ports exit `2`; empty explicit name exits `1`; no tracebacks. |
| Release-tag comparison probe | Passed: `v0.0.10` accepted; a mismatch returned nonzero before publication. |
| Post-authoring and minimal-usable-code sweep | Passed: no unrelated abstraction, fallback, dependency, or stale public link retained. |
| Focused regression tests | Passed for CLI, web, metadata, and package-layout owners. |
| `make check` | Passed: 347 tests; all format, lint, and structural checks clean. |
| `make hooks-run` | Passed, including actionlint. |
| `make release-check` | Passed: clean build, artifact metadata, fresh install, scripts, type marker, and entry point. |
| Pull request CI | Pending. |

## Reviewer reconciliation

| Reviewer | Accepted findings | Items intentionally excluded |
| --- | --- | --- |
| Public surface | License metadata, current-Python CI, JSON contract, provider-discovery clarity, release-notes URL | New docs platform and framework adapters |
| Runtime/API | Typed surface, port errors, empty explicit-name behavior | Runtime dependencies and fallback wrappers |
| Tests/release | Publish boundary, tag identity, stale-wheel smoke, installed entry-point proof, self-contained release docs | Redundant second source-distribution gate |

Local execution is complete when every local item is done or implemented and
the package-owned checks pass. Pull-request CI and merge state are verified in
the delivery record; external settings and publication remain explicitly
blocked or deferred here.
