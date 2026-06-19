# API Compatibility

Status: `beta`
Scope: public import roots and compatibility expectations for
`unicode-animations`

## Stable import roots

The current public import roots are:

- `unicode_animations`
- `unicode_animations.cli`
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

## CLI contract

The package currently treats these console scripts as public:

- `unicode-animations`
- `unicode-animations-web`

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
