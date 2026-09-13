# Development

Ithilien owns its palettes, ports, asset generators, and theme-specific regression
checks. The shared measurement and capture engine is
[Tintprobe](https://github.com/achandran/tintprobe), pinned to an exact Git revision
in `pyproject.toml` and `uv.lock`.

| Command | Purpose |
| --- | --- |
| `make build` | Audit both palettes and regenerate ports, README, palette chart, and previews. |
| `make test` | Run Ithilien's palette, export, and project-workflow policy tests. |
| `make evaluate` | Run tests and headless renderer/workflow evaluation through Tintprobe. |
| `make evaluate-ghostty` | Explicitly capture native Ghostty windows; requires an idle authorized desktop. |
| `make evaluate-offline GHOSTTY_OUTPUT=PATH` | Run tests and reanalyze saved screenshots without desktop interaction. |

Bare `make` only prints help. `make evaluate-headless` remains an alias for the
headless path. To include native Ghostty capture in the combined suite, explicitly
set `GHOSTTY_ARGS=--ghostty-capture`. Never run that while using the computer.
Missing tools and unavailable captures remain blocked or unverified, not passes.

## Dependencies and project inputs

Install uv and Make. Python 3.12+ is required. `uv run --locked` installs the
pinned evaluator and Python dependencies; normal evaluation does not fetch Git
theme/plugin sources. Prepare missing pinned source checkouts once:

```sh
make setup-evaluation
```

This uses Tintprobe's source manifests plus `evaluation/themes.json` and the
project plugin manifests. Sources live in ignored `evaluation/deps/`. Dirty or
mismatched checkouts are rejected rather than reset. It does not install system
tools or request desktop permissions.

`tintprobe.json` declares Ithilien's palette inputs, native ports, default adapter,
and `tests/workflows/` directory. `evaluation/` retains project rubrics, aesthetic
preferences, workflow scripts, and dependency declarations. Shared fixtures,
Codex instrumentation, and engine tests live in Tintprobe's package/repository.
The ANSI approval baseline and native diff-presentation pair remain in
`tests/fixtures/` because they support Ithilien's own regression contracts.

Neovim and the pinned Kanso checkout are required for previews. Rendering preview
PNGs also needs macOS Swift/AppKit and Berkeley Mono Medium. Tests and headless
comparison do not require the desktop. Python TS/LSP checks need the pinned grammar
and BasedPyright; Codex replay needs its pinned Rust source/toolchain, `just`, and
`cargo-nextest`. See Tintprobe's guides for capture-specific prerequisites.

## Native project checks

These do not open desktop windows:

```sh
KANSO_ROOT=evaluation/deps/kanso nvim --headless -u NONE -i NONE -l scripts/check_highlights.lua
uv run --locked python scripts/check_highlight_contrast.py
KANSO_ROOT=evaluation/deps/kanso nvim --headless -u NONE -i NONE -l scripts/check_native_diff.lua
KANSO_ROOT=evaluation/deps/kanso nvim --headless -u NONE -i NONE -l scripts/check_diff_presentation.lua
```

Outputs go to ignored `evaluation/results/highlight-checks/`. Override using
`ITHILIEN_CHECK_OUTPUT` for Lua checks and `--output` for the contrast reader.

Project-specific workflow adapters are explicit:

```sh
uv run --locked python -m tintprobe --project-root . workflow evaluate_git_review
uv run --locked python -m tintprobe --project-root . workflow evaluate_python_tools
uv run --locked python -m tintprobe --project-root . workflow evaluate_pickers
```

The installed-workflows adapter loads your installed LazyVim configuration; its
coverage differs from isolated fixtures. No pipeline installs themes or changes
the canonical palette. See the project workflow guides for their limits.

## Builds and evidence

`make build` writes palette audit JSON/Markdown to ignored
`evaluation/results/palette/` before generating the palette preview. To refresh
only audits and ports:

```sh
uv run --locked python scripts/audit_palette.py ithilien-dawn
uv run --locked python scripts/audit_palette.py ithilien-dusk
uv run --locked python scripts/generate_themes.py
```

Fresh combined runs live below `evaluation/results/full/`. A successful capture
is not a quality pass: inspect stage execution, findings, and missing coverage.
Native renderer cells, terminal pixels, and human comfort are distinct evidence.
Existing screenshot caches were preserved through extraction.

An optional ignored `evaluation/local.mk` may set `RUST_RUNTIME` to an isolated
rustup directory with `cargo/` and `rustup/` children. Codex replay temporarily
instruments its dedicated source checkout and restores it; do not run concurrent
replays on that checkout.

To update Tintprobe, change its Git revision deliberately, regenerate `uv.lock`,
then run both Tintprobe's tests and Ithilien's tests plus affected native checks.
A palette change still requires native evaluation; unit tests alone do not prove
rendering quality. Historical decisions are indexed in [design history](design-history.md).
