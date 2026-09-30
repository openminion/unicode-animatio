# unicode-animatio API Compatibility

Status: `beta`
Scope: public import roots and compatibility expectations for
`unicode-animatio`

Public naming note: the public distribution and CLI names use
`unicode-animatio`, while the Python import roots remain `unicode_animations`.

## Stable import roots

The current public import roots are:

- `unicode_animations`
- `unicode_animations.cli`
- `unicode_animations.provider`
- `unicode_animations.web`

## Stable public names

The package currently treats these names as public:

- `Spinner`
- `SpinnerName`
- `SPINNER_NAMES`
- `CategoryName`
- `CATEGORY_NAMES`
- `CATEGORY_DESCRIPTIONS`
- `CATEGORY_MOTION`
- `SPINNER_CATEGORIES`
- `SpinnerMetadata`
- `all_spinner_metadata`
- `metadata_for_spinner`
- `search_spinner_names`
- `spinner_names_for_category`
- `BrailleSpinnerName`
- `BRAILLE_SPINNER_NAMES`
- `spinners`
- `make_grid`
- `grid_to_braille`
- `makeGrid`
- `gridToBraille`
- `AnimationSpec`
- `UnicodeAnimationProvider`
- `get_provider`

## CLI contract

The package currently treats these console scripts as public:

- `unicode-animatio`
- `unicode-animatio-web`

Both commands expose `--version` using the installed package version.
Both accept `--host`, `--port`, and `--no-open` for browser previews; those
options require `--web` when using `unicode-animatio`.

## Provider entry point

The package declares this structural provider entry point for applications that
consume animation frames without importing CLI preview code:

- group: `openminion.cli.animation_providers`
- name: `unicode`
- target: `unicode_animations.provider:get_provider`

Provider payloads are raw frame strings, millisecond timing, and preset
selection metadata. Renderer colors, backgrounds, labels, layout, and
accessibility policy are not part of the provider contract.

`AnimationSpec` now also carries metadata fields for host integrations:

- `category`
- `tags`
- `frame_count`
- `frame_width`
- `motion`
- `description`

Those fields are additive and defaulted so older four-argument construction of
`AnimationSpec(provider_id, name, frames, interval_ms)` remains source
compatible.

`UnicodeAnimationProvider.get(name, *, length=1)` may repeat each frame into a
single synchronized animation. `length=1` preserves the original frame data;
larger positive values multiply `frame_width` while preserving frame count and
timing.

## Catalog naming compatibility

`SpinnerName` and `SPINNER_NAMES` are the canonical mixed Unicode/ASCII
catalog surfaces. `BrailleSpinnerName` and `BRAILLE_SPINNER_NAMES` remain
identity aliases over the complete catalog for compatibility with existing
imports. New integrations should use the canonical general names.

Every canonical name has exactly one value in `SPINNER_CATEGORIES`.
`spinner_names_for_category()` returns names in catalog order and raises
`KeyError` for an unknown category.
`metadata_for_spinner()` returns a `SpinnerMetadata` record for one preset.
`all_spinner_metadata()` returns metadata in catalog order.
`search_spinner_names()` searches names, categories, and tags in catalog order
and raises `KeyError` for an unknown category filter.

## CLI inspection compatibility

The terminal CLI supports human-readable and JSON inspection:

- `unicode-animatio --show NAME`
- `unicode-animatio --search TEXT`
- `unicode-animatio --list --category CATEGORY --json`
- `unicode-animatio --show NAME --json`

JSON output is intended for host discovery and smoke tests. The exact browser
demo markup remains non-contract, but `/spinners.json` exposes the same
metadata shape used by the gallery.

A named terminal preview prints its static metadata when standard output is
not interactive instead of emitting animation control sequences.

## Compatibility policy

For the current beta surface:

- new public names may be added in minor releases
- existing catalog order and category assignments remain deterministic
- existing public names should not be renamed or removed without a documented
  compatibility note
- JS-style aliases remain part of the compatibility surface until this file
  says otherwise

## Non-contract internals

The package does not currently promise compatibility for:

- private helper functions prefixed with `_`
- the exact HTML/CSS markup of the local browser demo
- internal frame-generation helper structure in `braille.py`
