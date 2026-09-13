# Ithilien Dusk: Warm Graphite

Dusk uses neutral graphite surfaces and warm stone-gray reading text, inspired
by the black ceramic and steel surrounding the Formex Reef GMT's white dial.
Dawn remains unchanged. Each palette has 18 distinct named sRGB colors.

- Canvas: Osgiliath `#202120`.
- Reading text: Nimloth `#BDB7AB`.
- Raised surfaces: Gondor `#282A28`.
- Supporting text: Ash `#AAA497`.
- Typography: Berkeley Mono Retina, 16 pt. Dawn uses Medium, 16 pt.

Both variants share Briar selection/cursors, Heather search, Celandine exact
edits, and Lebethron black interaction text. The paired foreground is essential:
normal reading text is unsuitable on those light interaction fills. Dusk's green,
red, and blue diff backgrounds keep larger changed regions subdued, while amber
marks individual changes in ordinary weight.

The six chromatic ANSI regular/bright pairs share values. Palette names retain
their Tolkien associations, with variant-specific shades where needed. Full
values and roles are in the generated [Dusk palette reference](dusk-palette.md).

## Validation

The final implementation passes 65 unit/regression tests, 136 authored contrast
checks, 154 native Neovim captures under Tintprobe's strict comparison gates, and
20 native interaction captures covering diagnostics, completion, and fzf.
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
Native Codex/Claude Code validation, Dusk Tree-sitter/LSP workflows, Ghostty pixels,
and extended-session comfort remain unverified. Theme exports do not guarantee
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
