# Development

The normal workflow has three commands:

| Command | Purpose |
| --- | --- |
| `make build` | Audit Dawn and Dusk; regenerate all theme ports, palette assets, README, and preview images. |
| `make test` | Run the locked pytest unit and regression suite. |
| `make evaluate` | Run tests, then all implemented native evaluation stages, including Ghostty capture and text checks. |

Bare `make` shows this help without installing dependencies or starting work.
For a palette change, run `make build` then `make evaluate` (which includes
`make test`). Use `make test` alone for a fast check while editing.
Evaluation does not rebuild artifacts: this keeps it read-only with respect to
the palette and generated ports. No command installs themes into your apps;
installation remains `./install.sh`.

Install [uv](https://docs.astral.sh/uv/) and Make first. The commands use
`uv run --locked` to synchronize `.venv` from `pyproject.toml` and `uv.lock`.
Python 3.12+ is required; no separate pip installation or activation is needed.

The complete build requires macOS, Swift/AppKit, Neovim, `evaluation/deps/kanso`, and Berkeley
Mono Medium fonts; see [README generation](readme-generation.md). Missing build
dependencies cause an error rather than silently preserving stale previews.

Prepare the pinned source checkouts once:

```sh
make setup-evaluation
```

This downloads only missing sources to ignored `evaluation/deps/`, verifies exact
revisions, and refuses to reset dirty or mismatched existing checkouts. Interrupted
downloads do not leave a partial dependency in its final location. For comparison
themes, use `make setup-evaluation THEMES="ithilien-dawn kanso-pearl modus-operandi"`.
It does not install system tools, fonts, or request GUI permissions. Subsequent
normal build/test/evaluate commands do not fetch Git sources. Missing sources are
reported once per stage as **blocked**, with quality **unverified**.

Native renderer evaluation is separate from the Python regression tests. Prepare
its pinned dependencies using the relevant guide, then use the same uv environment:

```sh
uv run --locked python scripts/evaluate_git_review.py
uv run --locked python scripts/evaluate_python_tools.py
uv run --locked python scripts/evaluate_pickers.py
```

These run actual Neovim/plugin processes. See [Git review](git-review-suite.md),
[Python tools](python-tools-suite.md), [pickers](pickers-suite.md), and
[installed workflows](installed-workflows.md) for prerequisites and coverage limits.
Do not treat a passing `make test` as evidence that these native evaluations ran.

To update dependencies intentionally, use `uv add --dev PACKAGE` or `uv lock
--upgrade-package PACKAGE`, then rerun the relevant checks and commit both the
project metadata and lockfile. Pytest and debugpy versions have a single source
of truth in the uv project; there is no separate Python-tools requirements file.

## Full acceptance run

```sh
make evaluate
```

This runs pytest first, then the existing combined evaluator with strict quality
checks, including Neovim diff comparisons, Python Tree-sitter/LSP, native Codex
diffs and flow replay, terminal interactions, evaluator validation, installed
workflows, Git review/overlaps, Python test/debug tools, and picker/completion
captures, plus native Ghostty command screenshots, calibration, pixel checks,
and OCR text checks. No Ghostty flag is needed for the normal full run. It does
not build or install themes or alter the palette.

Each invocation creates a fresh directory below `evaluation/results/full` and
prints its path. Open its `index.html` for stage statuses and galleries, or read
`report.json` for machine-readable evidence. Checkpoints preserve partial progress.
A failed or blocked required stage produces a nonzero exit status; missing tools
never count as passing. Ghostty cursor and mouse selection now have implemented native gates, but
require a fresh authorized capture. Inactive-window cursors, shell-specific mode
hooks, Claude Code, and long-session comfort remain unverified even when implemented stages
pass; Ghostty text OCR can also remain unverified. Full evaluation does not yet
mean full coverage of every theme goal.

The default theme is Ithilien Dawn. Override paths or compare additional themes:

```sh
make evaluate THEMES="ithilien-dawn kanso-pearl" \
  CODEX_SOURCE=/path/to/pinned/codex \
  PYTHON_SOURCE=/path/to/pinned/tree-sitter-python \
  EVALUATE_OUTPUT=/path/to/results
```

The core comparison/agent stages use the selected themes. Installed, Git, Python
tools, and picker profiles currently certify Dawn only; they are not arbitrary
colorscheme adapters.

One-time prerequisites: Neovim, a C compiler, the Python parser/LSP described in
the workflow guides, pinned theme dependencies in `evaluation/themes.json`,
Codex at the revision in `evaluation/sources.json` (default `evaluation/deps/codex`),
a matching Rust/Cargo toolchain on PATH, and the pinned Python grammar from
`evaluation/python-runtime.json` (default `evaluation/deps/tree-sitter-python`). The Codex
runner temporarily patches its dedicated source checkout and restores it; use a
separate clean test checkout. Do not run concurrent evaluations on that checkout.
The stock Codex UI replay additionally uses `just` and `cargo-nextest`. See
[Codex UI validation](codex-ui-validation.md) for the motion profile, timed
negative control, and remaining stock-renderer limitations.
`make setup-evaluation` includes all three isolated plugin profiles.
The installed profile also requires your configured LazyVim installation; its
fzf case needs terminal-mode ioctl permission. The suite does not request GUI
access or silently skip restricted terminal operations.

For an isolated rustup installation, set `CARGO_HOME` to `RUNTIME/cargo` and
`RUSTUP_HOME` to `RUNTIME/rustup` when installing the toolchain named in Codex's
`codex-rs/rust-toolchain.toml`. Use rustup's `--no-modify-path` option to leave
your shell configuration alone. Then run:

```sh
make evaluate RUST_RUNTIME=/absolute/path/to/RUNTIME
```

This exports those two directories and prepends their Cargo binaries to PATH
for the run. To reuse this choice without repeating the argument, put
`RUST_RUNTIME ?= /absolute/path/to/RUNTIME` in ignored `evaluation/local.mk`.
The setting is optional; a normal Rust installation works without
it. The first native Codex build needs network access to download dependencies
and can take substantially longer than subsequent evaluations.

Ghostty capture requires an authorized macOS session with Screen Recording
permission, Accessibility permission for interaction input, Ghostty, and Swift. It remains blocked when those are unavailable;
the suite does not request permissions or bypass restrictions. See
[Ghostty validation](ghostty-validation.md) for coverage details.

## Targeted diagnostics

These are optional shortcuts; the normal workflow does not require them:

- `make evaluate-ghostty`: capture and check only terminal command fixtures.
- `make evaluate-ghostty-images`: reanalyze saved PNGs without opening Ghostty.
- `make evaluate-ghostty GHOSTTY_CAPTURE=`: prepare command fixtures only.
- `make evaluate GHOSTTY_ARGS=--ghostty`: prepare fixtures during the full run
  where native capture is unavailable; Ghostty remains explicitly blocked.

Use `GHOSTTY_OUTPUT=/path/to/results` to select a standalone capture directory.
The combined suite uses its fresh run directory instead.
