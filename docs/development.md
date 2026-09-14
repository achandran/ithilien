# Development

Use Python 3.12+, uv, and Make. Run Python tools through `uv run --locked` from
this repository so they use its pinned environment. Neovim users need none of
these development tools.

| Command | Purpose |
| --- | --- |
| `make test` | Palette, export, and standalone Neovim regression tests. Native tests skip if Neovim is unavailable. |
| `make check-neovim` | Native highlight, contrast, diff, and plugin checks. Requires Neovim. |
| `make build` | Audit palettes, regenerate application ports, and render README assets. |

## Sources

[`palette.json`](../palette.json) is the canonical palette for both variants.
It contains named colors, role mappings, and naming sources. Edit it and the
generators, not generated application ports. Neovim highlight logic lives in
`lua/ithilien/`; statusline themes live in `lua/lualine/`.

Palette changes require an explicit new palette decision. Preserve the approved
18-color palettes, shared interaction colors, consolidated chromatic ANSI pairs,
and ordinary-weight amber exact edits. Both variants use black text on shared
interaction fills. Interpret colors as sRGB. The fingerprints and fixtures in
`tests/` enforce approved values; do not update them merely to make a change pass.
Primary reading text targets 7:1 contrast; ordinary and interaction text require
at least 4.5:1 on their actual backgrounds. Palette changes also need rendering
evidence beyond unit tests.

## Builds and previews

Preview generation requires Neovim, macOS Swift/AppKit, and Berkeley Mono Medium
and Retina regular/oblique OTF files, plus Bold and Bold Oblique, in
`~/Library/Fonts`. Dawn uses Medium at 16 pt; Dusk uses Retina at 16 pt.
Refresh only the previews with:

```sh
uv run --locked python scripts/generate_preview.py
```

The PNGs rasterize native Neovim cells from `tests/fixtures/readme/`; they are not
terminal screenshots or Tree-sitter/LSP captures. Adjacent JSON files record
source hashes and the Neovim version. The README itself is edited manually.

Color math and preview capture currently use the pinned Tintprobe library.
Its project configuration, evaluation CLI integration, and workflow suites are
not part of this repository. Builds and tests require no evaluator configuration.
Generated audit and native-check reports go in ignored `tests/results/`.
