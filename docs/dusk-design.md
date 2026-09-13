# Ithilien Dusk: Warm Graphite

Dusk uses neutral graphite surfaces and warm stone-gray reading text, inspired
by the black ceramic and steel surrounding the Formex Reef GMT's white dial.
Dawn remains unchanged. Each palette has 18 distinct named sRGB colors.

- Canvas: Graphite `#202120`.
- Reading text: Ithil `#BDB7AB`.
- Soft surfaces: Arnen `#2C2E2C` (cursor line and popups).
- Muted surfaces: Slate `#303437` (statuslines and secondary panels).
- Supporting text: Flint `#AAA497`.
- Typography: Berkeley Mono Retina, 16 pt. Dawn uses Medium, 16 pt.

Both variants share Briar selection/cursors, Heather search, Celandine exact
edits, and Lebethron black interaction text. The paired foreground is essential:
normal reading text is unsuitable on those light interaction fills. Dusk's green,
red, and blue diff backgrounds keep larger changed regions subdued, while amber
marks individual changes in ordinary weight.

The six chromatic ANSI regular/bright pairs share values. Across Dawn and Dusk,
each palette name identifies one exact hex value. The four shared colors retain
their names; Dusk’s other 14 shades draw on plants, landscapes, materials,
and moonlight. Material names are poetic landscape associations, not claims about
Middle-earth’s geology. Functional roles remain stable: `foregrounds.text` →
`Ithil` → `#BDB7AB`. Full values and roles are in the generated
[Dusk palette reference](dusk-palette.md).

Dusk’s named Lua palette now uses `Ithil`, `Arnen`, and `Poros` in place of
`Parchment`, `Shale`, and `Foam`. Direct `.colors` users should update those
keys; functional role mappings and hex values are unchanged.

Surface designations match Dawn: canvas (`backgrounds.base`), soft
(`backgrounds.surface1`), and muted (`backgrounds.mantle`). Both palettes define
the same 60 functional roles across backgrounds, foregrounds, accents, ANSI,
diffs, and highlights. Arnen `#2C2E2C` supports popups and the cursor line; Slate
`#303437` distinguishes statuslines and secondary panels. Their OKLab distance is
0.0256. Flint text on Slate measures 5.06:1. This prioritizes readable supporting
text over a larger distance between soft and muted surfaces.

Olive `#A6C995` marks success and added-code signs, Poros `#83C9BE` marks hints,
and Mist `#9DBDE0` marks information. Olive–Poros separation is 0.0634 in OKLab;
Poros–Mist separation is 0.0747. These measurements support comparison, not a
guarantee of perceptual recognition. Reading text, comments, the canvas, diff
backgrounds, and all four shared colors retain their selected values.

## Syntax

Everyday syntax follows Dawn’s neutral treatment: Ithil for functions,
identifiers, keywords, types, numbers, and constants; Flint for strings and
comments. Keywords and types use bold when enabled. Special syntax, regexes,
and preprocessor highlights retain selective accents as in Dawn. Diagnostics,
terminal ANSI colors, diffs, and interactions retain their distinct colors.
This changes Neovim syntax mappings, not the 18-color palette or application ports.

## Validation

The final implementation passes 74 unit/regression tests, 136 authored contrast
checks, 154 native Neovim captures under Tintprobe's strict comparison gates, and
20 native interaction captures covering diagnostics, completion, and fzf.
An additional 42 Python captures exercise Tree-sitter, BasedPyright diagnostics,
and semantic tokens. This corpus has no exact-character oracles; the separate
154-capture diff corpus covers those checks.
Dawn's native highlight, contrast, and character-diff checks also pass.

[Compact evidence and source hashes](assets/ithilien-dusk-validation.json)
record the validation scope. Raw temporary captures and tooling are removed after
validation; the commands below reproduce them.

```sh
make test
uv run --locked python scripts/audit_dusk.py
KANSO_ROOT=tests/evaluation/deps/kanso nvim --headless -u NONE -i NONE -l tests/check_dusk.lua
uv run --locked python -m tintprobe compare --themes ithilien-dusk --strict-gates --output tests/evaluation/results/dusk
uv run --locked python scripts/check_dusk_interactions.py
```

The interaction wrapper corrects the pinned static fzf pointer-background mapping:
its active pointer is rendered on the selected row, not the inactive gutter.
Native contrast checks and selected-item oracles remain unchanged. fzf requires
local terminal permissions.

The README preview uses actual Neovim cells rasterized with Retina at 16 pt.
Native Codex/Claude Code validation, Rust Tree-sitter/LSP workflows, Ghostty
pixels, and extended-session comfort remain unverified. Dusk’s saved Codex check
is blocked: available recordings do not match its exported theme, and the local
source-replay toolchain lacks Cargo. Python Tree-sitter/LSP coverage is limited
to the captured corpus, not every plugin workflow. Theme exports do not guarantee
that every application exposes character-level diff styling.

## Design rationale

Contrast is a readability floor, not a comfort score. We require at least 4.5:1
for ordinary text on its actual surfaces and at least 7:1 for primary reading
text. The main text/canvas pair is approximately 8.10:1; Briar/black is 4.62:1.
[W3C contrast guidance](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum)
and [Apple's dark-mode guidance](https://developer.apple.com/design/human-interface-guidelines/dark-mode)
support checking foreground/background pairs and actual presentation.

Dark-mode preference and performance vary by person and task. The palette needs
real use in the intended lighting before any long-session claim can be made.
[While and Sarvghad, IEEE VIS 2024](https://arxiv.org/abs/2409.10841).

## Remaining release checks

Run native Codex patches, long explanations, dimmed tool output, diagnostics,
and text selections in the intended terminal. A matching Dusk recording is
required; Dawn replay evidence cannot certify Dusk. Use
`make evaluate-codex-recording CODEX_THEME=ithilien-dusk CODEX_RECORDING=...`
to check an explicitly captured recording. Source-built replay additionally
requires the pinned Rust toolchain and repository-local build caches.

During sustained use with Berkeley Mono Retina at 16 pt, record concrete friction:
rereading comments, losing the cursor, confusing diagnostic states, or difficulty
identifying punctuation edits. Compare usual daytime and evening lighting. These
observations are still required before claiming long-session comfort.
