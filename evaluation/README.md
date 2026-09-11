# Ithilien palette evaluation

Goals: precise diffs, readable coding-agent output, sustained comfort, and the white-dial Formex Reef GMT character. Automated checks catch regressions; they cannot certify comfort or a “world class” theme.

## Run

Install Python dependencies with `uv sync`. Supply a Kanso checkout for Neovim. For native Codex, check out the exact `codex.revision` in `sources.json` and install its Rust toolchain and build prerequisites.

```sh
uv run python scripts/build.py
uv run python scripts/evaluate_theme.py --kanso /path/to/kanso.nvim
# Complete current automated renderer coverage:
uv run python scripts/evaluate_theme.py --kanso /path/to/kanso.nvim \
  --codex-source /path/to/codex --require-codex
```

The first command without Codex records `not_run` for that stage. `--require-codex` makes missing Codex validation a failure. Rust compilation can be expensive on its first run; subsequent runs reuse Cargo's cache. The runner temporarily includes our adapter in the pinned renderer and restores it afterward. It refuses an already modified renderer. Interrupted processes may require removing the appended include manually.

## Evidence and outputs

`evaluation/results/` contains:

- `report.json`: renderer status, visible-cell contrast failures, palette hash and Neovim version.
- `cells.json` and `gallery.html`: 110 actual Neovim UI captures: eleven cases, two widths, diff/search/line/character/block selection states.
- `codex-cells.json`, `codex-gallery.html`, `codex-test.log`: 60 native Codex captures, across two languages, two widths, insert/delete and truecolor/256/16-color modes.
- `comparison.json` when `--baseline /path/to/previous-results` is supplied.

HTML galleries reconstruct actual renderer cells. They are not Ghostty screenshots and do not reproduce terminal font rasterization. Neovim captures show the initial viewport. Existing native exact-character and diff-presentation assertions also run. Overlay checks establish presence, not correctness of every selected cell. Ordinary visible text is checked at 4.5:1; structural filler/separators at 3:1. These are contrast gates, not measured edit-discovery or comfort scores.

The Codex adapter loads the actual exported Ithilien tmTheme into the upstream syntax/diff renderer and captures Ratatui cells. It does not replay a complete agent session, run the patch algorithm, validate terminal color detection, or prove inline edit emphasis. ANSI fallbacks use the Ithilien terminal palette for named colors. Missing coverage must remain explicit.

## Corpus provenance

`sources.json` pins upstream commits, paths and SHA-256 hashes. Fixtures include Codex's own synthetic diff-gallery specimens, an unmodified excerpt from a public Codex commit, our local ghosttyconfig regression, and labeled synthetic punctuation/whitespace/Unicode/wrapping cases. Upstream snapshots are reference text only, not style validation. The upstream license is included. No private agent transcripts are used. Fixture code is displayed, never executed.

## Iterate

1. Run the suite and preserve the whole results directory as a baseline.
2. Change palette roles, regenerate exports, and rerun into a different `--output` directory with `--baseline` pointing to the previous results.
3. Inspect failures and both galleries. Check single-character edits, spaces, search and selections, not just overall appearance. Keep amber changed characters and dark text as the current baseline.
4. Review native Ghostty with the actual font, scaling and color-space settings. Record versions and settings with observations.
5. Compare equivalent long work sessions. Record missed edits, time to locate changes, cursor visibility, and fatigue separately from aesthetic preference. Preserve the neutral white/steel foundation and restrained red accent unless evidence warrants a deliberate change.

## Still unverified

Complete Codex conversations and tool/error/approval output; Claude Code rendering; native Ghostty pixels and selection/cursor behavior; three-pane diffs; scrolling; exhaustive overlay extents; human task performance and long-session comfort. These are future coverage, not implied passes. Palette changes should not automatically replace an approved baseline.

## Python priority

Python is the primary language: eight of eleven Neovim cases are Python, and four of five Codex specimens are Python. Dedicated fixtures cover decorators, dataclasses, annotations, optional/union types, f-strings, async/await, context managers, exception chaining, comprehensions, regex/string escapes, lambdas, and match/case. Their before/after code is parsed for validity and checked for coverage of these constructs. Neovim also asserts syntax groups are active before checking rendered colors. The runner currently uses built-in Neovim syntax, not Tree-sitter or LSP semantic tokens; those integrations remain a separate coverage gap.

## Compare arbitrary Neovim themes

```sh
uv run python scripts/compare_themes.py
# Limit the run or use your own adapter manifest:
uv run python scripts/compare_themes.py --themes kanso-pearl modus-operandi
uv run python scripts/compare_themes.py --manifest /path/to/themes.json --output /path/to/results
```

`themes.json` defines local runtime paths (relative to the Ithilien repository), pinned dependency revisions, source URLs and trusted Lua setup code. Clone each source to its specified path and check out its pinned revision before running. The default manifest uses sibling directories `kanso`, `eval-gruvbox` and `eval-modus`. Adapters execute code: only use trusted manifests and themes. To add a theme, supply a unique `id`, `paths`, `pins`, and `setup`. The working Ithilien checkout is deliberately unpinned to support candidate iteration; external dependencies must be clean and match their pins.

This first comparison mode preserves original theme highlights. It applies the same editor fixture settings to everyone and does not load Ithilien's diff presentation helper. It does not map competitors onto Ithilien's palette. The Modus entry is miikanissi's Neovim port, default `modus_operandi`, not the original Emacs implementation. Gruvbox Material uses light mode, the soft background variant and the original foreground palette; all other options remain upstream defaults.

The run produces 440 native UI captures, per-theme cell JSON, an expandable matched-fixture gallery and a machine-readable report. Below-4.5 contrast counts include structural characters and are observations, not pass/fail rankings. Background contrast ratios are not perceptual hue distances or comfort scores. Syntax failures fail the run; measured accessibility concerns remain in the report so comparison can complete. Missing dependencies or renderer failures also fail the command rather than silently omit a theme.

Comparison currently covers built-in Neovim syntax only. Competitor Codex ports, palette-only mode, Tree-sitter/LSP and native Ghostty screenshots are not implemented by this command. The separate Ithilien evaluator retains its existing Codex and exact-character checks.
