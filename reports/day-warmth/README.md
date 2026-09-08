# Warmer Day foundation experiments

**Historical experiment:** warm parchment with black neutral text and colored syntax has now been adopted. See the [accepted design](../day-adoption/README.md). The comparisons below retain their frozen pre-adoption reference; their “current” labels describe that earlier state.

These are reviewable experiments, not an adopted palette change. The current Day/Night palettes, generated application themes, shared highlight pair, and diff colors have not been changed by this exploration.

**A / Warm Ivory is the conservative refinement. B / Parchment is the more promising comfort trial for someone who likes Gruvbox Light Soft.** B gains warmth mostly through yellow chroma while keeping almost exactly A's brightness and contrast. C explores a deeper canvas and fails the existing secondary-text target. Neither passing experiment establishes better long-session comfort or better overall diffs.

[Canvas range](warmth-range.png) · [A code](warm-ivory-code.png) · [B code](parchment-code.png) · [A agent review](warm-ivory-agent.png) · [B agent review](parchment-agent.png) · [C agent review](soft-parchment-agent.png)

## What is held fixed

Only the six neutral backgrounds vary. Foregrounds, all nine syntax accents, ANSI colors, selection colors, every diff token, and semantic mappings remain identical to the current Day snapshot. Assertions in the generator check the color-family invariants and surface ordering.

Selections, search matches, and Neovim DiffText remain pure black on ochre, with 5.32:1 text contrast. After the follow-up black-text request, these specimens were regenerated with the current Day inline add/delete/change treatments: black characters on lighter green, rose, and ochre fills. GitSigns-style inline changes use bold and underline. Each warmth variant still holds those same diff tokens fixed; the warmth experiment itself does not redesign them.

The specimens use Berkeley Mono at 15 px and identical text, geometry, and highlighting. They show code, comments, popups, diagnostics, prose, terminal-style output, and character-level diffs. They are manually annotated role specimens, not native Codex/Claude screenshots. A visible dot represents the changed whitespace cell. No screenshot claims that an application detected that change automatically.

## The variants

| Variant | Canvas | Main text | Secondary | Comments | Muted | Weakest syntax | Existing audit |
|---|---|---:|---:|---:|---:|---:|---|
| Current Day | `#EEECE1` | 10.11 | 7.24 | 5.44 | 5.24 | 5.31 | PASS |
| A / Warm Ivory | `#EEE9D9` | 9.87 | 7.07 | 5.31 | 5.12 | 5.18 | PASS |
| B / Parchment | `#F0E9D2` | 9.87 | 7.07 | 5.31 | 5.12 | 5.18 | PASS |
| C / Soft Parchment | `#ECE5D0` | 9.52 | 6.82 | 5.12 | 4.94 | 5.00 | FAIL: secondary text < 7 |

Ratios are foreground against canvas. Audits gate unrounded values. The 7:1 secondary-text target is existing project policy; C remains above 4.5:1 but is not presented as passing. No thresholds were changed. A and B each pass all 126 current contrast checks and six existing semantic-separation gates. Full reports: [A](warm-ivory-audit.md), [B](parchment-audit.md), [C](soft-parchment-audit.md), [machine-readable summary](summary.json).

A softens the silver cast toward ivory without making yellow a prominent feature of the page. B gives prose and chrome a clearer parchment character. In the specimens, its unchanged olive-charcoal text still looks crisp, and the existing brick, olive, and brown syntax feels at home on the warmer canvas. C noticeably deepens the page, but gives up contrast and space between the surface levels without a decisive improvement in these samples.

A and B are both slightly darker than current Day, but essentially equal to one another in brightness. Their OKLCH lightness is approximately 0.934 versus current Day's 0.942. B's chroma is 0.031 versus A's 0.022 and current Day's 0.015. This is the useful finding: additional warmth does not require progressively darker backgrounds.

[Gruvbox Light Soft's original canvas](https://github.com/morhetz/gruvbox/blob/master/colors/gruvbox.vim) is `#F2E5BC`, with approximately 0.922 lightness and 0.055 chroma. Our [reference specimen](gruvbox-canvas.png) borrows only that canvas while retaining Loden inks and other surfaces, so it isolates the foundation rather than claiming to represent the native Gruvbox theme. B is less yellow and a little lighter than this reference. A preference for Gruvbox may also involve its syntax colors, typography, or familiar role mappings; background matching cannot establish that preference alone.

## Surface hierarchy and constraints

| Purpose / token | Current | A | B | C |
|---|---|---|---|---|
| Raised popup / surface0 | `#F5F3EA` | `#F5F0E4` | `#F7F0DF` | `#F3ECDA` |
| Canvas / base | `#EEECE1` | `#EEE9D9` | `#F0E9D2` | `#ECE5D0` |
| Active line / surface1 | `#E8E8DE` | `#E9E5D7` | `#ECE5D2` | `#E9E3D0` |
| Chrome / mantle | `#E2E1D7` | `#E6E1D2` | `#E8E1CD` | `#E7E1CE` |
| Recessed chrome / crust | `#D5D6CD` | `#D5D2C5` | `#D8D2BE` | `#D5D0BF` |
| Structural fill / surface2 | `#B9BFB3` | `#BEBEAF` | `#C1BEAC` | `#BEBEAC` |

All preserve the same lightness ordering. All text/accent tokens stay valid at 4.5:1 on base, popup, active line, and mantle. Crust and surface2 remain restricted to text/subtext/bright; comments and muted text are not permitted there.

The chrome cannot simply be darkened by the same amount as the canvas. Initial darker mantles reduced the unchanged ochre selection boundary below 3:1. The final experiments warm the mantle while keeping its luminance close to current Day; the selection boundary stays above 3:1. This compresses the active-line/chrome hierarchy, especially in C. Essential boundaries still use the existing stronger foreground, not a pale structural fill.

## The diff trade-off

Holding diff colors fixed preserves text-to-diff and character-to-line contrast, but it does **not** preserve the relationship between a diff line and the surrounding page. The warmer canvas is closer to the existing yellow changed-line fill `#F2E8C9`.

| Changed-line fill versus canvas | Current | A | B | C |
|---|---:|---:|---:|---:|
| Normal ΔEOK | 0.0295 | 0.0204 | 0.0111 | 0.0161 |
| Grayscale ΔEOK | 0.0106 | 0.0025 | 0.0025 | 0.0092 |

These are observations, not universal thresholds or new gates. B most strongly reduces the normal-vision distinction. In the agent specimen, individual ochre-highlighted digits, the inserted equals sign, and the marked space remain easy to locate. The surrounding yellow changed-line fill is less useful for scanning. The `~` marker must carry more of that information. Existing added/deleted line fills and inline text pairs remain unchanged; their relation to the canvas also needs judgment in the actual host.

B's [protan](parchment-protan.png), [deutan](parchment-deutan.png), [tritan](parchment-tritan.png), and [grayscale](parchment-grayscale.png) specimens were visually reviewed. The warmth difference largely disappears in grayscale; line markers and inline character emphasis survive. Syntax/diagnostic foreground separations are unchanged because the foregrounds are fixed. A's matching simulations are also exported as `warm-ivory-{mode}.png` and SVG.

## Recommendation

Use **B as the next personal comfort trial**, compared with A and current Day at the same font, screen brightness, and time of day. It moves meaningfully toward the stated Gruvbox preference without sacrificing our existing contrast gates. Use **A if preserving more of the current diff-line separation is the deciding factor**. Keep C as evidence of the limit, not a proposed default.

Given that excellent diffs are the first guiding principle, B should not become the default solely because its prose sample looks warmer. A real review should include isolated changed lines, one-character operator edits, inserted whitespace, and long unmodified context in Neovim and the coding agents. If the changed-line fill becomes hard to scan there, retain A/current Day or separately revisit that fill; this foundation-only experiment does not silently alter it.

No experiment has been applied to the active palette or installed into applications. Warmth here describes visual character, not a measured reduction in glare or eye strain. Long-session comfort and native agent rendering remain untested.

## Reproduce

Sources: [experiment definitions](../../experiments/day-warmth.json) plus the current canonical Day palette. The [captured current palette](current-palette.json) records the reference for these artifacts. Generated candidate palettes and full audit JSON/Markdown live in this directory.

```sh
uv run python scripts/explore_day_warmth.py --png
```

PNG export uses macOS and installed Berkeley Mono. Without `--png`, the script writes SVGs and audits. It uses the unchanged production audit in an isolated temporary output directory; live themes and normal audit reports are not regenerated. C's expected failure is recorded in its report while exploration continues.
