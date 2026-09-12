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

An earlier Computer Use session explicitly denied Ghostty access. Such a denial
must not be bypassed with another capture mechanism in that session. Native
execution requires authorization in the environment running it. Preparing
fixtures and testing the evaluator's logic require no native app access.

## Remaining acceptance work

- Verify full command output is visible, including wrapped paths, errors, and
  punctuation; add additional terminal command fixtures.
- Verify font and geometry, then measure glyph foreground/background samples.
- Extend cursor coverage to inactive windows and real shell mode hooks, then
  verify the implemented cursor and mouse selection cases on the target host.
- Display the existing native Neovim and Codex fixtures through Ghostty and
  compare their pixels with their recorded cells.
- Check stable repeated captures and reject stale, clipped, or occluded frames.

No comfort or Claude Code validation is claimed by this stage.

## Running from a regular checkout

Use `make evaluate-ghostty` to test only Ghostty. It does not require the pinned
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
acceptance remains incomplete because native Neovim/Codex workflows and font identity remain unverified. An OCR error never silently falls back to a passing pixel-only verdict.

Tests include blank/clipped calibration, erased glyphs, low-contrast cells,
tiny punctuation, altered comparison operators, omitted lines, and unsupported
ANSI control sequences. Captured PNG and ANSI hashes are recorded in the text
report. Existing fixtures must match the capture's stored ANSI hash and the
current theme must match its stored theme hash before analysis proceeds.

OCR now runs on isolated full-width terminal rows rather than a whole-window
image. Each crop is padded and scaled 2× to avoid adjacent-line merges. Saved
`ocr-rows/` images make recognition input reviewable. The engine receives row
numbers and PNG paths only—not expected text or custom-word hints. Comparison
still uses its top candidate and preserves every non-whitespace character;
`<`, `<=`, and the look-alike `‹=` are distinct. Pixel checks continue to use the
original unscaled screenshot. Engine failure remains unverified.


### Independent punctuation recognition

New captures include a separate ASCII reference sheet, rendered by Ghostty under
the same configuration in normal, bold, italic, and underline combinations. This
adds one fixture window. On OCR-mismatched rows, the analyzer classifies every
cell against the full reference alphabet; it never chooses a template using the
expected command character. Full 120-column rows must agree, including unexpected
suffixes. Shape distance must be at most 0.08 with a 0.04 lead over the next glyph;
ambiguous shapes remain unverified. Independent pixel/contrast checks still gate
acceptance. Reference PNG, payload, geometry, and classifier hashes are recorded.
Old captures without this sheet retain their OCR results; rerun native capture
to use the additional recognizer. The first native reference run passed all six real command fixtures and recovered
their OCR omissions. An offline mutation of that native diff passed unchanged and
was rejected after erasing the equals sign in `<=`. The white-on-white ANSI probe
still fails as intended. Synthetic mutation tests additionally cover replaced
operators and unexpected suffixes. Ligatures or differing rasterization may
remain unverified.

### Native steady block cursor

New captures also include `cursor-block`: the terminal receives a steady-block
cursor escape sequence and positions its actual cursor over the `=` in
`return attempt <= 3`. The emitter does not paint a replacement cursor. Its cell
must have the configured cursor fill and foreground, meet the 4.5:1 rendered
stroke contrast floor, and independently resolve to `=` against the native ASCII
reference sheet. Normal command text checks still apply to the rest of the row.
Missing fill, an outline cursor, erased or replaced glyphs cannot pass this gate.
The JSON report records cursor evidence separately from command text evidence.

Run `make evaluate-ghostty` to capture this case. Previous captures do not
establish coverage for newly added interactions.

### Cursor modes and real mouse selection

The native stage also requests steady bar and underline cursors, hidden cursors,
and blinking block/bar/underline cursors. Bar and underline checks enforce the
cursor's location, extent, and palette color, plus readable underlying glyphs.
Only exact cursor-colored strip pixels are removed for glyph/OCR recognition;
original pixels still undergo the independent cursor and text checks. A sequence
of 16 timed frames must contain at least two on frames, two off frames, and two
transitions before blinking passes. A static or unrecognizable cursor cannot pass.
A separate same-window sequence exercises bar → block → underline → hidden → block,
with an acknowledgment after each native escape sequence and a screenshot per
state. These are terminal protocol tests, not claims that every shell/plugin's
vi-mode hooks are configured correctly.

Mouse tests drag through a substring containing `<=` and across two lines. One
fixture includes blue ANSI text to verify that selection overrides its foreground.
The analyzer checks selected spaces and unselected neighbors as well as text:
missing selection, selection beyond the expected range, wrong fill, white text,
and damaged operators do not pass. Coordinates come from the captured terminal
grid and are converted to window-relative fractions for Retina displays. The
selection is native mouse input, not an ANSI-painted background or clipboard paste.

Native Ghostty may place a one-pixel bar immediately left of the inferred cell
boundary. Shape and hidden-phase checks include that single boundary pixel;
OCR cleanup uses the same boundary. A bar farther away, an erased bar, and an
erased covered glyph remain rejected. This allowance changes neither the
palette nor the contrast or independent glyph-classification thresholds.

In addition to Screen Recording, the helper needs **Accessibility** permission
for window focus and mouse input. It checks permission without prompting. A
missing permission produces a blocked run with the native error retained. Grant
permission to the helper identified by macOS, then rerun from your terminal.
The worker raises its own uniquely titled fixture window; it refuses input if
identity, focus, or ownership at the target coordinates changes. It never sends
input to your ordinary Ghostty windows. Keep this desktop session free of other
mouse/keyboard activity while the native interaction cases run. No clipboard or
shell-history access is involved.

The palette remains frozen. Tests mutate synthetic captures to ensure wrong
shapes, static blinking, missing/overextended selection, and altered text cannot
pass. A September 12, 2026 authorized native run, reanalyzed after the bar-boundary
repair, passed six command cases, eight cursor cases (including three timed blink
sequences and all five transition states), and both mouse selections. Selection
text measured 4.622:1 against the unchanged 4.5:1 floor. The white-on-white
attribute probe still failed as intended. Local evidence is in
`evaluation/results/ghostty-validation-20260912/quality.json` and `quality.html`;
`report.json` retains the original pre-repair analysis. Native-image mutation
controls in `bar-mutation-controls.json` reject erased/misplaced bars and an
erased equals sign. These results apply to this capture, not every installation.
Inactive-window
cursor appearance, shell-specific mode hooks, native Neovim/Codex sessions, and
long-session comfort remain outside this interaction set. The report lists
cursor and selection case counts separately from full native acceptance.
