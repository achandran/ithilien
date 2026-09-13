# Installed Neovim workflow regression suite

Run from the repository virtual environment:

```sh
.venv/bin/python -m tintprobe --project-root . workflow evaluate_installed_workflows --output evaluation/results/installed-workflows
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

Add `--installed-workflows` to `evaluate_suite.py` to include this local Dawn gate
in the combined suite. It is opt-in because it requires your installed plugins;
it is independent of the arbitrary-theme comparison matrix. Any failure makes
that combined stage fail, even without `--strict-gates`.

This suite does not prove every possible plugin state or long-session comfort.
The palette-definition audit remains a separate check for all loaded plugins:

```sh
.venv/bin/python scripts/audit_installed_palette.py --output evaluation/results/plugin-palette
```

For static captures, OS-level Neo-tree file watching and LSP watched-file dynamic
registration are disabled. They exhausted file-watcher resources in the execution
environment; neither is needed to render these fixed files. File-system change
notification behavior is outside this suite's scope.

A terminal-mode permission error from fzf is reported as **blocked**, retains a
nonzero suite exit status, and cannot count as successful renderer coverage.
Run the same command in an environment permitting terminal-mode ioctls to complete
those cases. Palette and contrast gates are not relaxed for this condition.
