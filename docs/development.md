# Development

Use Python 3.12+, uv, and Make. Run Python tools through `uv run --locked` from
this repository so they use its pinned environment. Neovim users need none of
these development tools.

## Commands

| Command | Purpose |
| --- | --- |
| `make test` | Unit and regression tests, including native standalone checks when Neovim is available. |
| `make build` | Audit palettes, regenerate ports and palette charts, and render both Neovim previews. |
| `make setup-evaluation` | Fetch pinned evaluation sources into the ignored dependency cache. |
| `make evaluate THEMES="ithilien-dawn ithilien-dusk"` | Tests, native comparisons, workflow checks, and saved Codex checks. |
| `make evaluate-full` | Opt into source-built Codex evaluation; requires its Rust toolchain. |
| `make evaluate-offline GHOSTTY_OUTPUT=PATH` | Tests and analysis of saved Ghostty screenshots. |

Bare `make` shows help. The shared evaluator is
[Tintprobe](https://github.com/achandran/tintprobe), pinned in `pyproject.toml` and
`uv.lock`. Project configuration belongs in tracked `tintprobe.json`; captures,
dependencies, and optional `tests/evaluation/local.mk` remain untracked.

## Editing and building

The canonical palette is [`scripts/palette/ithilien.json`](../scripts/palette/ithilien.json).
It contains both variants' named colors, role mappings, and naming sources.
Edit this file and the generators, not generated application ports. Neovim
highlight logic lives in `lua/ithilien/`; statusline themes live in `lua/lualine/`.

Palette changes require an explicit new palette decision. Preserve the approved
18-color palettes, shared interaction colors, consolidated chromatic ANSI pairs,
and ordinary-weight amber exact edits. Both variants use black text on shared
interaction fills. Interpret colors as sRGB. The palette fingerprint and fixtures
in `tests/` enforce the approved values; do not update them merely to make a
changed palette pass. Primary reading text targets 7:1 contrast; ordinary and
interaction text require at least 4.5:1 on their actual backgrounds.

Preview generation requires Neovim, macOS Swift/AppKit, and Berkeley Mono Medium
and Retina regular/oblique OTF files, plus Bold and Bold Oblique, in
`~/Library/Fonts`. Dawn uses Medium at 16 pt; Dusk uses Retina at 16 pt.
Refresh only the previews with:

```sh
uv run --locked python scripts/generate_preview.py
```

The PNGs rasterize native Neovim cells from `tests/fixtures/readme/`. They are not
terminal screenshots or Tree-sitter/LSP captures. Adjacent JSON files record
source hashes and the Neovim version. The README itself is edited manually.

## Native checks

These checks do not open desktop windows:

```sh
nvim --headless -u NONE -i NONE -l tests/check_highlights.lua
uv run --locked python tests/check_highlight_contrast.py
nvim --headless -u NONE -i NONE -l tests/check_dusk.lua
nvim --headless -u NONE -i NONE -l tests/check_native_diff.lua
nvim --headless -u NONE -i NONE -l tests/check_diff_presentation.lua
nvim --headless -u NONE -i NONE -l tests/check_plugin_semantics.lua
```

Workflow adapters run with `uv run --locked python -m tintprobe workflow NAME`:
`evaluate_git_review`, `evaluate_pickers`, `evaluate_python_tools`, and
`evaluate_installed_workflows`. The last loads your installed LazyVim configuration;
the others use isolated fixtures. Plugin pins live in `tests/evaluation/`.
Python tooling requires a compiled parser at
`$ITHILIEN_PYTHON_PARSER_ROOT/parser/python.so` (default root:
`~/.local/share/nvim/site`). Debugpy and fzf require local socket/terminal permissions.
Dusk interaction checks use `uv run --locked python scripts/check_dusk_interactions.py`.

Native Ghostty capture requires explicit desktop authorization and an idle desktop:
`make evaluate-ghostty`. Use saved-image analysis while the computer is in use.
Tests and cell captures do not establish terminal pixel quality or long-session comfort.

## Evidence and limitations

Inspect reports under `tests/evaluation/results/`; missing tools or failed captures
are not passes. Standalone Neovim tests skip when Neovim is unavailable. Palette
changes require rendering evidence beyond unit tests.

Saved Codex checks require matching recordings and do not validate the installed
CLI. Select a recording with `make evaluate-codex-recording CODEX_THEME=THEME
CODEX_RECORDING=PATH`. Source-built replay uses the pinned Rust tools; build output
defaults to `~/Library/Caches/ithilien/codex-target`. Do not run concurrent replays
against the same source checkout.

Dusk's native Codex/Claude Code, Ghostty pixel, Rust Tree-sitter/LSP, and extended
comfort coverage remains incomplete. The [historical Dusk validation snapshot](assets/ithilien-dusk-validation.json)
records its original validation scope; it is not certification of current sources.
Detailed design history is preserved in Git.
