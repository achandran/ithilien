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

Startup diagnostics distinguish an unstarted launcher, a failed child process,
and a ready fixture whose window cannot be located. Each scene retains a
`*.child.log` and `*.started` marker. The launcher uses Ghostty's explicit
`initial-command=shell:...` form, quotes every path, disables shell integration
for the fixture, and keeps the byte emitter free of third-party imports.

## Command text checks

Native runs now also produce `quality.html` and `quality.json`. To analyze
existing screenshots without launching or capturing any app:

```sh
make evaluate-ghostty-images
```

The analyzer locates the six calibration bars to infer the terminal grid, parses
the recorded ANSI output, and checks every expected nonspace ASCII cell for
clipping, the expected foreground color, and dark stroke contrast against the
cell's modal background (minimum 4.5:1). Pixels are converted using their ICC
profile into sRGB. This is a solid-stroke rendering proxy, not a psychophysical
readability or comfort score. Antialiased edge pixels are not required to meet
the solid-text contrast threshold. Tiny punctuation is tested explicitly.

An independent Apple Vision OCR pass compares each expected line at its rendered
vertical position. Only whitespace is normalized: missing `=`, punctuation,
case changes and missing lines do not pass. OCR disagreement or engine failure
is `unverified`, not proof that the palette is defective. Font identity, exact
indentation, and character-shape fidelity are not certified by these checks.

The attribute probe deliberately contains white ANSI text on the light canvas;
those incompatible pairs are exposed as findings, not hidden or changed during
evaluation. The six real command cases are reported separately. Full native
acceptance remains incomplete because cursor and selection checks do not yet
exist. An OCR error never silently falls back to a passing pixel-only verdict.

Tests include blank/clipped calibration, erased glyphs, low-contrast cells,
tiny punctuation, altered comparison operators, omitted lines, and unsupported
ANSI control sequences. Captured PNG and ANSI hashes are recorded in the text
report. Existing fixtures must match the capture's stored ANSI hash and the
current theme must match its stored theme hash before analysis proceeds.
