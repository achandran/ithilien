# Python test and debugger regression profile

This profile runs actual pytest and debugpy processes through pinned Neotest,
neotest-python, nvim-dap, and DAP UI. It does not load your personal Neovim config.

```sh
uv sync --locked
.venv/bin/python scripts/evaluate_python_tools.py --fetch-dependencies
# Offline subsequent runs:
.venv/bin/python scripts/evaluate_python_tools.py
# Combined gate, after dependencies are prepared:
.venv/bin/python scripts/evaluate_suite.py --python-tools
```

A compiled Python Tree-sitter parser must be available under
`$ITHILIEN_PYTHON_PARSER_ROOT/parser/python.so`. The default root is
`~/.local/share/nvim/site`. Its SHA-256 is recorded, alongside plugin revisions,
Python package versions, Neovim version, fixture digest, and palette digest.
Plugin revisions are enforced; the parser and package versions are recorded,
not enforced. Use `uv sync --locked` to reproduce the tested package versions.
Missing dependencies or unsuccessful execution fail; nothing is reported as
passing merely because a plugin is installed.

The 12-case matrix uses two widths (100/160) and initial/reloaded theme states:

| Scene | Evidence and gates |
|---|---|
| Neotest summary | One actual passed, failed, and skipped test; names in the summary pane; rendered Ilex/Annun/Ash status colors |
| Neotest failure | Actual failed-test concise output with AssertionError in the output pane |
| DAP scopes | debugpy stopped at a real breakpoint; scopes pane includes local total=42; stacks and breakpoints also displayed |

Every capture checks palette membership and 4.5:1 text contrast. Python
Tree-sitter must be active. Mutation checks prevent source-buffer text from
substituting for plugin pane contents and reject missing execution outcomes.
Fixtures run in temporary directories. Debugging uses local IPC only; network
access is unnecessary after dependency setup, but local sockets must be permitted.

The gallery reconstructs native Neovim RGB cells using Berkeley Mono Medium at
16 pt. It does not verify native Ghostty pixels, font availability, or comfort.
The summary uses actual status icons, but font glyph availability is not tested.

Coverage limits: a paused local-variable view is not exhaustive debugger coverage.
Exception stops, stepping, watches, nested variables, running-state animation,
parameterized tests, and the full pytest output view remain future scenarios.
The tested output uses Neotest's concise failure view; full output can scroll the
assertion off-screen and requires a separate viewport test.
