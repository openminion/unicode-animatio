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

## Provider entry point

The package declares this structural provider entry point for applications that
consume animation frames without importing CLI preview code:

- group: `openminion.cli.animation_providers`
- name: `unicode`
- target: `unicode_animations.provider:get_provider`

Provider payloads are raw frame strings and millisecond timing only. Renderer
colors, backgrounds, labels, layout, and accessibility policy are not part of
the provider contract.

## Compatibility policy

For the current beta surface:

- new public names may be added in minor releases
- existing public names should not be renamed or removed without a documented
  compatibility note
- JS-style aliases remain part of the compatibility surface until this file
  says otherwise

## Non-contract internals

The package does not currently promise compatibility for:

- private helper functions prefixed with `_`
- the exact HTML/CSS markup of the local browser demo
- internal frame-generation helper structure in `braille.py`
