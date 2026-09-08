# Pure black foreground exploration

**Historical experiment:** warm parchment with black neutral text and colored syntax has now been adopted. See the [accepted design](../day-adoption/README.md). The comparisons below retain their frozen pre-adoption reference; their “current” labels describe that earlier state.

Day's inline diff character foreground is now **`#000000`** in the canonical palette, including the six GitSigns inline groups. Neovim DiffText remains black-on-ochre. The rest of this study is a rendering experiment, not an adopted monochrome theme.

[All-black code comparison](all-black-code.png) · [Black neutral text with colored syntax](black-neutral-code.png) · [All-black agent prose and diffs](all-black-agent.png) · [Background range](black-background-range.png)

## Applied inline-diff change

| Treatment | Text | Background | Text contrast |
|---|---|---|---:|
| Inline addition | `#000000` | `#A1BA77` | 9.81:1 |
| Inline deletion | `#000000` | `#E2A69B` | 10.16:1 |
| Inline change | `#000000` | `#D2B16B` | 10.24:1 |
| Neovim DiffText | `#000000` | shared ochre `#B17232` | 5.32:1 |

The lighter inline fills retain the existing 7:1 / APCA 60 text gates. Their distinction from the surrounding line is weaker than with the previous dark fills: 1.23:1 for add, 1.44:1 for delete, and 1.68:1 for change. These are fill-to-fill ratios, not text ratios. Day GitSigns inline groups use bold **and underline** to make the exact changed span visible, including a whitespace cell. The palette lab reflects that style. Changed lines retain their markers. This is a real trade-off, not a claim that every measure improved.

The lighter change token was also inherited by completion-menu borders through Kanso. Those borders now explicitly use the existing readable FloatBorder treatment. All 830 resolved Neovim contrast checks pass, with additional assertions that DiffText and all six GitSigns inline groups are black. Seven regression tests pass. Night's resolved highlights remain identical to the baseline.

Generated Day themes are refreshed from the canonical source. Claude's word-background tokens receive the new fills, but its native renderer has not been tested here; a host that overrides text color or ignores underlining needs separate validation. The controlled specimens cannot certify its exact word-diff appearance.

## Three text policies

The main comparisons use the same warm parchment surfaces and the same font, content, diff fills, and selection background.

1. **Current Loden inks:** olive-charcoal neutral text and restrained colored syntax.
2. **Black neutral text:** primary/secondary text, comments, and muted labels become black; syntax, diagnostics, terminal palette, and diff-line text keep their semantic colors. Inline characters are already black.
3. **All text black:** every rendered glyph becomes black, including syntax, diagnostics, terminal output, and diff-line text. Colored fills stay intact. Keywords remain bold, comments italic, and inline diffs retain their cues.

Black neutral text is a plausible next trial. The prose has a stronger ink-on-paper character, and color still helps scan strings, numbers, types, and diagnostic severity. Black comments and line numbers also demand more attention; collapsing the neutral text hierarchy is a choice, not free contrast.

The all-black specimen is also readable. It has an intentionally monochrome code style: functions, types, strings, numbers, and identifiers share their foreground. Bold keywords and grammatical structure do more work. Diagnostic labels and diff markers become essential. There is no universal reason to reject this style, but it is a larger change than adjusting the normal foreground.

## Tempering the background

| Background | Black text contrast | Current olive-charcoal contrast |
|---|---:|---:|
| Current ivory `#EEECE1` | 17.72:1 | 10.11:1 |
| Warm parchment `#F0E9D2` | 17.29:1 | 9.87:1 |
| Deeper parchment `#E2D8BB` | 14.77:1 | 8.43:1 |

The warmer parchment can make black feel more like printed ink, but it barely reduces the numeric contrast. Even the substantially deeper background remains high contrast. Warming and darkening are different adjustments; background warmth is not evidence of reduced eye strain or better long-session comfort.

The deeper sample is a canvas-only specimen, not a complete palette proposal. Reusing current syntax and interactions on darker surfaces would require another full pairing audit. Screen brightness, font rendering, and the actual host remain outside these palette measurements.

## Status and reproduction

Only the inline-diff correction is applied to Day. Neither black-neutral nor all-black text has replaced the active syntax/foreground palette. The warmth candidates remain separate experiments. Nothing is installed into applications.

```sh
uv run python scripts/build.py
uv run python -m unittest discover -s tests -v
uv run python scripts/check_neovim.py /path/to/kanso.nvim --baseline /path/to/baseline
uv run python scripts/explore_black_text.py --png
```

[Experiment definitions](../../experiments/day-black-text.json) describe the rendering policies. The generator paints glyph foregrounds, not every palette token: blindly turning all accent tokens black would also destroy colored backgrounds and inverse labels. An adopted monochrome port would need explicit separation of text and fill roles and its own semantic contract. The existing color-separation gates have not been weakened or falsely reported as passing for the all-black experiment.

PNG specimens use Berkeley Mono at 15 px. All-black and black-neutral code, agent prose, and the background range were visually inspected. They are controlled specimens, not native application screenshots or long-duration use tests.
