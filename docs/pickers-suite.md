# Picker and completion profile

Run `.venv/bin/python scripts/evaluate_pickers.py --fetch-dependencies` once,
then omit the fetch flag for offline runs. Plugin revisions are pinned in
`evaluation/pickers-dependencies.json`; no personal configuration is loaded.

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
