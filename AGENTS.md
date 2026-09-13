# Repository Guidelines

## Project Structure & Module Organization

Ithilien is a Neovim colorscheme with Dawn and Dusk variants. `lua/ithilien/`
contains theme and highlight logic; `lua/lualine/` contains statusline themes.
`colors/` provides colorscheme entry points. Canonical palettes live in
`scripts/palette/`; Python generators in `scripts/` produce application ports in
`extras/` and README assets in `docs/assets/`. Tests live in `tests/`, with native
workflow adapters in `tests/workflows/`. The shared evaluation engine is Tintprobe,
pinned in `pyproject.toml` and `uv.lock`.

## Build, Test, and Development Commands

Use Python 3.12+, uv, and Make. Bare `make` prints help.

- `make test`: run pytest unit and regression tests.
- `make build`: audit palettes, regenerate ports and palette chart, and capture
  the Neovim preview. Preview generation requires Neovim, Kanso, Swift/AppKit,
  and Berkeley Mono fonts; see `docs/development.md`.
- `make setup-evaluation`: fetch pinned evaluation source dependencies.
- `make evaluate`: run tests, Neovim/workflow checks, and saved Codex-cell checks.
- `make evaluate-full`: opt into source-built Codex evaluation. Rust build output
  defaults to `~/Library/Caches/ithilien/codex-target`.

## Coding Style & Naming Conventions

Use four-space Python indentation and two-space Lua indentation; follow surrounding
style and avoid unrelated reformatting. Use snake_case for Python functions and
`ithilien-dawn`/`ithilien-dusk` for theme identifiers. No dedicated formatter or
linter is configured. Edit canonical palette definitions and generators rather
than hand-editing generated ports. Dawn role mappings reference named colors.

## Testing Guidelines

Pytest discovers `tests/test_*.py`, including unittest-based cases. Add focused
regressions for changed palette mappings, exports, and highlight behavior. Run
`make test` and affected native checks; there is no numeric coverage target.
Palette changes require rendering evidence beyond unit tests. Saved Codex checks
block when recordings are missing or the exported theme changes; they do not
validate the installed CLI. Native Ghostty capture requires explicit desktop
authorization. Keep captures and dependency caches untracked.

## Commit & Pull Request Guidelines

Use concise imperative commit subjects, such as “Remove redundant build inputs,”
matching repository history. Describe the problem, resulting behavior, and
validation in pull requests. Link relevant issues and include updated previews
or rendering evidence for visual changes. Keep `tintprobe.json` tracked: it is
shared project configuration, not machine-local state.
