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
