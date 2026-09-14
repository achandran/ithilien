# Testing

Run `make test` for the theme’s unit and regression tests. See
[development](development.md) for dependency setup and the combined headless
evaluation. The profiles below retain their own coverage and prerequisites.

## Git review

The first compatibility profile loads pinned Diffview, Neogit, Gitsigns, and Plenary
checkouts, without loading or changing your personal Neovim setup.
The Ithilien palette remains frozen.

```sh
# One-time dependency fetch, then the full 28-case matrix:
uv run --locked python -m tintprobe --project-root . workflow evaluate_git_review --fetch-dependencies
# Subsequent unattended runs require no network:
uv run --locked python -m tintprobe --project-root . workflow evaluate_git_review
# Include this required gate in the combined evaluation:
make evaluate
```

Revisions and source URLs are in `tests/evaluation/git-review-dependencies.json`.
Missing dependencies, modified checkouts, revision mismatches, missing windows,
and renderer errors fail the run. Fetching never updates an existing checkout.
To deliberately upgrade a dependency, update its pin and check it out explicitly.

| Plugin | Rendered coverage | Not yet covered |
|---|---|---|
| Diffview | Two-way Python working-tree diff and real three-way merge conflict; exact edited digit on both sides, search and linewise selection over edited text | History and conflict-resolution interactions |
| Neogit | Staged/untracked status and expanded staged hunks with inline digit checks | Commit popup, conflict resolution |
| Gitsigns | Actual floating hunk preview and inline digit emphasis | Staged preview, inline preview, search overlays |

Every scene runs at 100 and 160 columns, initially and after a colorscheme reload.
The fixture includes a digit replacement and operator deletion. The automated
character-emphasis assertion currently targets the digit, not the operator.
Rendered foreground/background membership and a 4.5:1 text-contrast floor are
checked throughout. Mutation tests reject absent panes, misplaced emphasis,
off-palette colors, and low-contrast text. Git commands only touch a temporary
repository; hooks are not installed and commits are not signed.

Outputs include a gallery, native RGB cell evidence, dependency pins, Neovim
version, fixture digest, palette digest, and the configured rendering profile.
The gallery uses Berkeley Mono Medium at 16 pt. It reconstructs Neovim cells;
it does not verify Ghostty pixels, font availability, or long-session comfort.

Initial profile: 12/12 passed after mapping Neogit's section headers and modified
file labels to Anduin. Their upstream defaults previously produced 48
out-of-palette, low-contrast cells per Neogit capture.

The expanded profile adds actual conflicts and staged hunks. Neogit diff mappings
now use Dawn's existing backgrounds and black inline text instead of derived
colors.

The Python and picker profiles below cover additional renderers; this Git
profile does not imply complete plugin support.

Overlap cases require Heather on both searched digits and Briar across the
selected source line, even where the diff would normally use Celandine.
Mutation tests reject a partially painted search or visual selection. These
checks cover Diffview overlaps; diagnostic/cursor-line and debugger overlaps
remain outside this profile.

The initial four Visual failures were capture false positives: only the cursor
cell lacked the Visual background in the text grid. The capture does not render
Neovim's separate cursor. The corrected fixture selects the changed line plus
the following blank line, with the cursor on the blank line. It requires mode V,
anchor on line 1, cursor on line 2, and Briar across every target character.
No target cells are exempted. Mutation tests still reject partial selections.
This verifies selection, not the cursor's native appearance. No theme or palette
change was needed.

## Pickers and completion

Run `uv run --locked python -m tintprobe --project-root . workflow evaluate_pickers --fetch-dependencies` once,
then omit the fetch flag for offline runs. Plugin revisions are pinned in
`tests/evaluation/pickers-dependencies.json`; no personal configuration is loaded.

The 12 captures cover Telescope and Snacks file results with Python previews,
and nvim-cmp with its real buffer source and a selected completion. Both widths
(100/160) and initial/reloaded theme states are captured. Checks require native
result panes, preview contents, visible completion, palette membership, and 4.5:1
text contrast. The gallery reconstructs native RGB cells with Berkeley Mono Medium
16 pt; it does not verify Ghostty pixels or font availability.

Snacks backdrop dimming is explicitly disabled in this profile because it creates
composited colors outside the palette. Default dimming is not certified by these
results. Completion documentation, LSP completion, deprecated items, and exhaustive
matching/selection semantics are not covered by this initial profile.

Include this gate in the combined suite with `--pickers` after fetching dependencies.

## Python tests and debugging

This profile runs actual pytest and debugpy processes through pinned Neotest,
neotest-python, nvim-dap, and DAP UI. It does not load your personal Neovim config.

```sh
uv sync --locked
uv run --locked python -m tintprobe --project-root . workflow evaluate_python_tools --fetch-dependencies
# Offline subsequent runs:
uv run --locked python -m tintprobe --project-root . workflow evaluate_python_tools
# Combined gate, after dependencies are prepared:
make evaluate
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

## Installed Neovim workflows

Run from the repository virtual environment:

```sh
uv run --locked python -m tintprobe --project-root . workflow evaluate_installed_workflows --output tests/evaluation/results/installed-workflows
```

This captures the actual installed Lazy configuration, with the working Ithilien
checkout substituted for its installed copy. It does not update plugins or edit
your Neovim configuration. Temporary Python fixtures, state, and logs are isolated.
The configured automatic language servers are disabled; the explicit Python LSP
case uses `basedpyright-langserver` beside the Python executable, or
`ITHILIEN_LSP_COMMAND` when specified. Local RPC sockets must be permitted for
Fzf-lua. Missing dependencies and timeouts are failures, not successful coverage.

The matrix uses 100 and 160 columns, at initial load and after a theme reload:

- Python Tree-sitter and live BasedPyright semantic tokens and diagnostics.
- Python changed-character diffs, search, full-line visual selection, and floats.
- Neo-tree, Trouble, Which-key, Grug-far, Fzf-lua, Snacks dashboard, and Blink.
- The installed status line and buffer line wherever those workflows show them.

Each capture checks expected content, plugin loading, Python parser activity,
rendered palette membership, and a 4.5:1 text contrast floor. Interaction states
must show their expected background. Mutation tests verify that missing UI,
missing highlighting, off-palette colors, and unreadable pairs are rejected.

`report.json` records failures and plugin revisions. `cells.json` preserves native
Neovim RGB cell output. `gallery.html` displays that output using Berkeley Mono
Medium at 16 pt. These are faithful cell reconstructions, not native Ghostty
screenshots; font availability and rasterization are not verified by this gate.

Add `--installed-workflows` to `tintprobe suite` to include this local Dawn gate
in the combined suite. It is opt-in because it requires your installed plugins;
it is independent of the arbitrary-theme comparison matrix. Any failure makes
that combined stage fail, even without `--strict-gates`.

This suite does not prove every possible plugin state or long-session comfort.
The palette-definition audit remains a separate check for all loaded plugins:

```sh
uv run --locked python scripts/audit_installed_palette.py --output tests/evaluation/results/plugin-palette
```

For static captures, OS-level Neo-tree file watching and LSP watched-file dynamic
registration are disabled. They exhausted file-watcher resources in the execution
environment; neither is needed to render these fixed files. File-system change
notification behavior is outside this suite's scope.

A terminal-mode permission error from fzf is reported as **blocked**, retains a
nonzero suite exit status, and cannot count as successful renderer coverage.
Run the same command in an environment permitting terminal-mode ioctls to complete
those cases. Palette and contrast gates are not relaxed for this condition.

## Palette membership and load order

Dawn explicitly maps core defaults, Fzf-lua, Bufferline, and Grug-far colors that
otherwise fall outside its palette. Overrides also run after LazyLoad, VeryLazy,
and colorscheme reloads. They do not run when another theme is active. Fzf's
backdrop uses an opaque palette surface instead of a blended gray.

Run the portable semantic regression check from the repository:

```sh
nvim --headless -u NONE -i NONE -n -l tests/check_plugin_semantics.lua
```

Audit your installed Lazy configuration:

```sh
uv run --locked python scripts/audit_installed_palette.py --output tests/evaluation/results/plugin-palette
```

Use `--init` and `--lazy-root` for nonstandard installations. This loads your
configuration and installed plugins, substitutes this checkout for Ithilien,
disables Lazy's automatic installation/update checks, and redirects state and
cache to a temporary directory. Your configuration still executes its own code.
The report records startup, plugin loading, and colorscheme reload snapshots.
Any off-palette RGB foreground, background, or special color fails the command,
as does a missing or unloaded configured plugin. Alternate themes and the
OS appearance watcher are explicitly excluded and recorded.

This is a highlight-definition gate, not a claim of exhaustive pixel coverage.
Plugin-local namespaces, terminal ANSI output, image/emoji rendering, and states
created only by interaction need separate rendered checks. Anti-aliasing naturally
produces intermediate pixel colors and should not fail palette membership.

### Gitsigns load order

The standalone Gitsigns check verifies staged sign cues and ordinary-weight
inline spans before and after the plugin recreates its fallback highlights:

```sh
GITSIGNS_ROOT=tests/evaluation/deps/gitsigns.nvim nvim --headless -u NONE -i NONE -l tests/check_gitsigns.lua
```

This complements the live hunk captures in the Git review suite.
