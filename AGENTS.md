# Repository Guidelines

## Project Structure & Module Organization

Ithilien is a Neovim colorscheme with Dawn and Dusk variants. `lua/ithilien/`
contains theme and highlight logic; `lua/lualine/` contains statusline themes.
`colors/` provides colorscheme entry points. Canonical palettes live in
`palette.json`; Python generators in `scripts/` produce application ports in
`extras/` and README assets in `docs/assets/`. Colorscheme tests live in `tests/`. Build helpers are pinned
in `pyproject.toml` and `uv.lock`.

## Build, Test, and Development Commands

Use Python 3.12+, uv, and Make. Bare `make` prints help.

- `make test`: run pytest unit and regression tests.
- `make build`: audit palettes, regenerate ports and palette chart, and capture
  the Neovim preview. Preview generation requires Neovim, Swift/AppKit,
  and Berkeley Mono fonts; see `docs/development.md`.
- `make check-neovim`: run native highlight, contrast, diff, and plugin checks.

## Coding Style & Naming Conventions

Use four-space Python indentation and two-space Lua indentation; follow surrounding
style and avoid unrelated reformatting. Use snake_case for Python functions and
`ithilien-dawn`/`ithilien-dusk` for theme identifiers. No dedicated formatter or
linter is configured. Edit canonical palette definitions and generators rather
than hand-editing generated ports. Both variants’ role mappings reference named colors.

## Testing Guidelines

Pytest discovers `tests/test_*.py`, including unittest-based cases. Add focused
regressions for changed palette mappings, exports, and highlight behavior. Run
`make test` and affected native checks; there is no numeric coverage target.
Palette changes require rendering evidence beyond unit tests. Keep generated test reports and dependency caches untracked.

## Commit & Pull Request Guidelines

Use concise imperative commit subjects, such as “Remove redundant build inputs,”
matching repository history. Describe the problem, resulting behavior, and
validation in pull requests. Link relevant issues and include updated previews
or rendering evidence for visual changes.
