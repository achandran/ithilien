# Development

Install [uv](https://docs.astral.sh/uv/) and Make, then run from the checkout:

```sh
make test
make build
```

`make` also defaults to `make test`. Both targets use `uv run --locked`, which
creates/synchronizes `.venv` from `pyproject.toml` and `uv.lock`. No separate pip
installation or virtual-environment activation is needed. Python 3.12+ is required.

- `make test` runs all Python unit and regression tests with pytest. Existing
  unittest-based tests are discovered by pytest without rewriting their assertions.
- `make build` audits Dawn and Dusk, regenerates every supported theme port,
  palette references/charts, README, and its native-cell preview images. It does
  not install themes into your applications.

The complete build requires macOS, Swift/AppKit, Neovim, `../kanso`, and Berkeley
Mono Medium fonts; see [README generation](readme-generation.md). Missing build
dependencies cause an error rather than silently preserving stale previews.

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
captures. It does not build or install themes or alter the palette.

Each invocation creates a fresh directory below `evaluation/results/full` and
prints its path. Open its `index.html` for stage statuses and galleries, or read
`report.json` for machine-readable evidence. Checkpoints preserve partial progress.
A failed or blocked required stage produces a nonzero exit status; missing tools
never count as passing. Ghostty pixels, Claude Code, and long-session comfort
remain explicitly untested, even when implemented stages pass.

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
Codex at the revision in `evaluation/sources.json` (default `../review-codex`),
a matching Rust/Cargo toolchain on PATH, and the pinned Python grammar from
`evaluation/python-runtime.json` (default `../eval-tree-sitter-python`). The Codex
runner temporarily patches its dedicated source checkout and restores it; use a
separate clean test checkout. Do not run concurrent evaluations on that checkout.
Fetch the isolated plugin profiles once using their `--fetch-dependencies` flag.
The installed profile also requires your configured LazyVim installation; its
fzf case needs terminal-mode ioctl permission. The suite does not request GUI
access or silently skip restricted terminal operations.
