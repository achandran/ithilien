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

## Experimental scorecard

Every comparison now writes `scorecard.json` and `scorecard.html`. Re-score existing **region-aware** captures without rerendering:

```sh
uv run python scripts/score_themes.py evaluation/results/comparison
```

`rubric.json` versions weights, targets and small independent source-byte oracles. Version 0.1.0 produces a **provisional Neovim plain-diff score**, not a cross-application excellence score. Text readability has 50% weight, inline background separation 35%, and changed-line background separation 15%. Text contrast saturates at 4.5:1; distinction saturates at heuristic CIEDE2000 color distances of 15 and 5. The background targets are engineering choices, not validated UX thresholds. Equal weighting of fixture/width observations limits domination by long snippets. Missing components or a failed inline oracle prevent a total score.

Native screen positions map code cells back to buffer text. Gutters, filler and status lines are excluded. Explicit punctuation and Unicode-prefix byte-position oracles verify required inline cells; these are limited spot checks, not exhaustive edit-span verification. Whitespace and all renderer-reported inline regions participate in separation measurements when a surrounding changed-line background is visible. Search and Visual captures remain available but are not scored yet. Background color distance includes hue but omits typography, so this rubric can undervalue themes that distinguish regions using bold or underline.

Agent and long-session axes remain `null / not_evaluated`. The scorecard exposes a text-readability indicator, but does not relabel it as comfort. There is no overall score. Do not use this experimental rubric as the sole objective of unattended palette optimization until it has broader coverage and calibration. Deliberate low-contrast and indistinguishable-inline mutations are tested to ensure they lower the score; missing source regions cannot silently pass.

### Version 0.2: gates and distributions

The dashboard replaces headline aggregate scores with gate status and worst-case component measurements. Per-theme details expose minimum, median, maximum and linked cell-level failures. The old weighted score remains in JSON for compatibility only; it is not a ranking or acceptance criterion.

Critical source-byte oracles now cover the deleted `l` in ghosttyconfig, replacement punctuation, a Unicode-prefixed digit, a removed space and an added trailing space. Required inline backgrounds must differ from the same-side changed line by at least ΔE2000 5 (an experimental threshold). Any missing required cell/emphasis, failed critical background distinction or unreadable source character is recorded individually. Source text is assessed in all five states. Overlay presence is checked against the plain capture. It does not prove every expected overlay cell or disambiguate all overlay conflicts; typography-only emphasis can be flagged by the background gate.

Use `--strict-gates` with either comparison or scoring to return a failing exit status when any theme violates a gate. Ordinary comparison still completes and records all findings, permitting comparison of themes with known failures. Missing data are failures, not implicit passes. Candidate optimization should use strict mode on the candidate separately from competitor benchmarks.

Mutation tests exercise low-contrast characters, absent inline emphasis, merged backgrounds, invisible search overlays, harmless distinct hue changes, and gutter exclusion. These demonstrate sensitivity to specific degradations; they do not constitute human-performance calibration. Agent and comfort axes remain unscored.

### Failure audit and light-mode typography

The comparison command also writes `failure-audit.html` and JSON, grouping repeated findings by rendered style. Each representative includes foreground/background values, the measured value, a native-cell line reconstruction and a fixture link. Repeated cells across states and widths are not independent defects. Regenerate from saved captures with `uv run python scripts/audit_failures.py evaluation/results/comparison`.

The inline gate checks foreground and typography alternatives when background separation is weak. Alternative cues yield `inline_cue_review`, not an automatic background-only failure or an unearned pass. Bold/italic do not count as visible cues for spaces. Exact overlay boundaries and full cue effectiveness remain unverified.

Light-mode visual previews request **Berkeley Mono Medium, size 16** (16 pt in HTML/SVG), as recorded in `render-profile.json`. Neovim/Ratatui cell captures do not use fonts; browser font availability and native Ghostty font rendering are not verified. Theme-requested bold/italic styling is preserved for fair original-theme comparison. A browser missing the font will use a monospace fallback; these previews must not be described as verified font screenshots.

### Exact source-text overlay checks

Captures now retain Neovim highlight provenance (`ext_hlstate`), logical selection endpoints, virtual columns and per-character search matches. `overlay_checks.py` compares every visible source region against the expected characterwise/linewise/blockwise selection or search match. It detects missing cells, extra cells and highlights leaking into the other pane, including tab expansion and Unicode byte positions. The terminal-rendered cursor glyph is excluded from selection-attribute assertions. Search spans come from Neovim's regex matcher independently of highlight attributes.

These checks cover visible source text, including wrapped source characters. They do not yet cover blank cells beyond end-of-line, blank lines, offscreen content, or cursor glyph appearance/placement. Selection endpoints reflect actual logical editor state, not a separate assertion of command intent. The same region can have correct provenance but unreadable colors; the separate contrast gates still check that. The prior presence-only test remains as a coarse check alongside exact source-region checks. Mutation tests verify partial selection, spillover, wrong-pane selection, search spillover, and tab-column behavior.

## Python Tree-sitter and LSP comparison

```sh
uv sync --locked
# Clone the source listed in python-runtime.json and check out its pinned revision.
uv run python scripts/compare_themes.py \
  --python-source /path/to/tree-sitter-python \
  --output evaluation/results/python-comparison
```

This uses the pinned upstream Python parser and highlights query, compiles it with `cc`, and starts pinned BasedPyright 1.40.1. It captures all four themes across three Python fixtures, two widths and five states (120 captures). Each buffer must have an active Tree-sitter highlighter, a nonempty semantic-token response, applied semantic extmarks, and diagnostics before capture. Fixtures deliberately contain a type mismatch; code is never executed. Native Neovim semantic highlighting and diagnostics are active together with Tree-sitter. The readiness check uses native parser and semantic evidence rather than requiring legacy syntax groups.

Each capture records runtime evidence; the report records dependency versions. Neovim state/cache directories are temporary, and the LSP root is confined to the fixture directory with dynamic file watchers disabled. Missing prerequisites and readiness timeouts fail the run. This tests source overlays and colors under the actual integrations; it does not claim exhaustive diagnostic-popup or completion-menu coverage. The parser queries are pinned upstream queries, not a user's custom Tree-sitter configuration.

## Codex flow replay

The main `evaluate_theme.py --codex-source ...` run now includes this stage after the diff-renderer checks.

```sh
uv run python scripts/codex_flows.py --source /path/to/pinned/codex
```

The flow adapter runs inside upstream `ChatWidget` tests using real event handlers and native Ratatui rendering. It loads the exported Ithilien theme and replays a request, commentary, approval modal, failed Python test output, patch in progress/completed, successful tests and final Markdown/Python response. Two widths produce 16 captures with accumulated native history and the current widget. The approval response and tool results are synthetic events; no command is executed, no files are patched and no model/API call occurs.

This is a complete scripted UI workflow, not a live app-server end-to-end session. It does not cover every Codex path, all color depths, Claude Code, or native Ghostty. The existing diff adapter still supplies explicit three-color-depth coverage. `native.log`, `codex-cells.json`, `codex-gallery.html` and `report.json` preserve evidence. Text contrast findings are reported without claiming a general agent-excellence score. Native DIM rendering remains terminal-dependent.

## Unified candidate suite

```sh
uv run python scripts/evaluate_suite.py \
  --codex-source /path/to/pinned/codex \
  --python-source /path/to/pinned/tree-sitter-python
# Candidate acceptance gates (competitor failures are expected in benchmark mode):
uv run python scripts/evaluate_suite.py \
  --codex-source /path/to/pinned/codex \
  --python-source /path/to/pinned/tree-sitter-python \
  --themes ithilien-dawn --strict-gates
```

One command runs built-in Neovim comparisons, Python Tree-sitter/LSP comparisons, native Codex diffs, and the scripted Codex workflow for every selected theme. `index.html` links the galleries and scorecards; `report.json` combines evidence and explicitly lists Ghostty, Claude Code and comfort as incomplete. Execution errors fail the command. Benchmark mode records quality failures without aborting comparison; strict mode rejects any supported-stage gate failure. No global excellence score is produced.

Ithilien uses its native tmTheme export. Other adapters are **evaluation conversions**, generated from pinned Neovim groups and their sixteen terminal colors. They are not claimed to be upstream Codex ports, even when other upstream application exports exist. `codex_theme_adapters.py` documents the exact common scope mapping; generated `adapter.json`, `resolved-neovim.json`, `terminal-palette.json` and tmTheme preserve provenance. Results evaluate that mapping, not an authoritative rendering of every upstream syntax feature. Custom manifests use the same conversion unless their id is the native Ithilien entry.

Agent gates report each workflow stage separately, with cell-level foreground/background contrast failures and required content-fragment checks. Stages include accumulated history; required fragments isolate selected key content but do not exhaustively classify all text by role. DIM cells are counted as unverified, not silently modeled as opaque. Every theme uses fresh native test processes, preventing global theme state leaking across candidates. Theme-specific colors are passed into the native renderer; captured cells are never recolored to simulate a different theme.
