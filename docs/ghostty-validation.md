# Ghostty validation

This stage is under development. It never counts prepared ANSI output or a
calibration-only screenshot as full native acceptance.

`make evaluate` prepares real Git status, Git diff, single-character Git word
diff, ripgrep, the generated zsh prompt, and pytest output in a disposable repository. Pytest deliberately
runs one passing and one failing Python test. A separate labeled probe covers
ANSI 0–15 and dim text. The palette remains frozen. No installed configuration,
user repository, shell history, or application data is changed.

## Native capture worker

On a macOS host where native UI automation is authorized and Screen Recording
is already available, run:

```sh
uv run --locked python scripts/evaluate_ghostty.py --capture
# Or include it in the combined suite:
make evaluate GHOSTTY_ARGS=--ghostty-capture
```

The worker compiles a small Swift helper, checks capture permission without
requesting it, and launches isolated Ghostty windows with unique titles. Each
window receives a generated config, Berkeley Mono Medium at 16 points, sRGB,
and one fixture. A ready-file handshake waits for the fixture output. Only the
uniquely titled Ghostty window is captured; there is no whole-desktop capture.
The fixture child exits after capture or after 45 seconds. The worker never
quits the user's other Ghostty windows.

Screenshots are decoded into sRGB and checked for six ANSI calibration swatches
(with a two-channel-value tolerance and at least 100 matching pixels per color).
This catches blank captures and gross palette mismatches. It does **not** prove
text content completeness, font selection, glyph contrast, cursor rendering,
selection, or readability. Actual screenshots are linked in the gallery when
captured. The report remains `incomplete`, with a nonzero acceptance exit,
until those additional gates exist. Partial failures remain visible.

The capture worker is not executable through the current Computer Use session:
that tool explicitly denies Ghostty access. Do not route around this restriction
with another capture mechanism in that session. Native execution must be tested
in an authorized environment. Preparing fixtures and testing the evaluator's
logic require no native app access.

## Remaining acceptance work

- Verify full command output is visible, including wrapped paths, errors, and
  punctuation; add additional terminal command fixtures.
- Verify font and geometry, then measure glyph foreground/background samples.
- Exercise real cursor and mouse selection states; do not substitute colored
  text backgrounds for native selection.
- Display the existing native Neovim and Codex fixtures through Ghostty and
  compare their pixels with their recorded cells.
- Check stable repeated captures and reject stale, clipped, or occluded frames.

No comfort or Claude Code validation is claimed by this stage.

## Running from a regular checkout

Use `make evaluate-ghostty` to test only Ghostty. It does not require the sibling
Kanso, Codex, or Tree-sitter source repositories used by the full evaluation.
`make evaluate-ghostty GHOSTTY_CAPTURE=` prepares fixtures without launching UI.
Both currently exit nonzero because native acceptance is incomplete, even if
all available calibration checks pass. Inspect `evaluation/results/ghostty/report.json`
for the precise status. The full `make evaluate` still requires its documented
pinned dependencies; this target does not install them.
