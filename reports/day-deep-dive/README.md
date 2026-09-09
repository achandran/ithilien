# Loden Day: independent quality assessment

**Loden Day has a strong, distinctive core palette, but the complete theme is not yet demonstrably world class.** Its parchment canvas, black main text, and restrained syntax are worth retaining. The most important remaining work concerns actual diff composition, terminal foreground/background combinations, and secondary hierarchy. More attractive swatches or larger color distances would not resolve those weaknesses.

This assessment examines commit **`4289246`**, committed on 2026-09-08. Subsequent design clarification establishes black as the **main foreground**, while allowing other colors for secondary and semantic roles. Selection text and specifically changed diff characters should remain black. Consequently, the committed choice to make every neutral foreground and neutral ANSI slot black is an overextension of the intended preference, not a requirement to preserve.

[Seven-palette code comparison](comparison.png) · [Diff composition specimen](diff-overlay.png) · [Stress specimen](stress-normal.png) · [Grayscale stress specimen](stress-grayscale.png) · [Reproducible measurements](measurements.json)

## Verdict by design objective

| Objective | Assessment | Confidence |
|---|---|---|
| Readable main text | Excellent on the intended light surfaces | High: measured |
| Warm, restrained visual character | Strong and coherent; worth preserving | Moderate: visual judgment |
| Readable syntax on the editor canvas | Strong; all nine accents exceed 4.5:1 | High: measured |
| Precise changed-character diffs | Strong explicit Neovim/GitSigns tokens; insufficient evidence across agent renderers | Mixed |
| Surface and foreground hierarchy | Understandable surface ordering, but foreground hierarchy is flattened | High for mappings; moderate for perceived impact |
| Terminal compatibility | Concrete failure in neutral indexed-color combinations | High: exact token collision |
| Color-independent semantics | Partially supported; several distinctions still depend on context or host cues | Moderate |
| Long-session comfort | Plausible fit for the stated taste; not established by testing | Unproven |

“World class” is an evaluative judgment, not an accessibility certification or a measurable percentile. A defensible claim would require excellent reading and navigation, dependable precise diffs, coherent identity, and evidence that these qualities survive the actual applications used. Loden meets several of these conditions, but currently has counterexamples to others.

## 1. The background and primary foreground are good decisions

Keep **`#F0E9D2`** as the working background and **`#000000`** as the main foreground. Their contrast is **17.29:1**. This gives ordinary text a substantial readability margin without relying on bright white as the canvas. The slightly subdued yellow parchment works naturally with olive, sage, clay, and dark gold. Blue serves a limited informational role and does not dominate the code specimen.

The visual result is related to Gruvbox Light Soft without becoming a direct copy. Loden's canvas is slightly lighter and less chromatic: its OKLCH lightness is 0.9334 and chroma 0.0313. The comparison shows a quieter red/green balance and more subdued warm accents. The original Gruvbox source supplies the soft canvas `#F2E5BC` and reference role colors used here. These observations concern the controlled specimens, not every Gruvbox port. [Gruvbox source](https://github.com/morhetz/gruvbox/blob/master/colors/gruvbox.vim)

The Citizen watch direction now plays a supporting role. Parchment is warmer than the original pale silver/gray-green brief; pure black also replaces the proposed olive-charcoal main markings. That is a legitimate shift toward the functional and personal preferences that govern this project. Without the photographs or physical measurements, an exact watch-match claim would be unjustified.

Warmth should be described as a visual quality, not as proof of reduced fatigue. A controlled proofreading study found an advantage for dark text on a light background, especially at smaller sizes. It did not compare Loden with Gruvbox, test parchment against white, or establish comfort over a day of programming. Display brightness, font weight, size, ambient light, and individual preference remain relevant. [Piepenbrock, Mayr and Buchner, 2014](https://pubmed.ncbi.nlm.nih.gov/25141597/)

## 2. Readability is competitive; contrast alone does not establish superiority

The following ratios were recalculated with the published piecewise sRGB transfer function and rounded only for presentation. They describe representative role selections in the linked specimen, not native application accessibility scores.

| Palette specimen | Main text | Comments | Strings | Keywords | Functions | Types | Numbers |
|---|---:|---:|---:|---:|---:|---:|---:|
| Loden Day `4289246` | 17.29 | 17.29 | 5.54 | 5.68 | 7.37 | 5.48 | 5.18 |
| Gruvbox Light Soft, original | 9.23 | 2.92 | 3.87 | 6.86 | 3.87 | 3.00 | 5.36 |
| Modus Operandi reference | 21.00 | 7.00 | 7.05 | 9.58 | 11.20 | 7.49 | 21.00 |
| Ef Day, pinned `e1f6176` | 8.68 | 4.89 | 5.01 | 4.80 | 4.51 | 4.62 | 8.68 |
| Solarized Light reference | 4.13 | 2.48 | 2.93 | 2.97 | 3.41 | 2.98 | 4.21 |
| Catppuccin Latte reference | 7.06 | 2.30 | 2.96 | 4.79 | 4.34 | 2.31 | 2.64 |
| Everforest Light medium reference | 5.18 | 2.56 | 2.69 | 3.04 | 2.69 | 2.12 | 2.83 |

Exact tokens and source links are retained in [measurements.json](measurements.json). Except for the newly added original Gruvbox specimen, comparison tokens are the explicitly recorded snapshots from the earlier review. In particular, Ef Day is a historical pinned reference: current Ef architecture builds on Modus, so this row must not be presented as a fresh audit of current Ef defaults. [Ef documentation](https://protesilaos.com/emacs/ef-themes)

Modus is the stronger demanding benchmark because its stated objective includes at least 7:1 for small text and broad face coverage, together with dedicated color-vision variants. Loden does not meet that contrast target for most syntax accents, although it comfortably exceeds the ordinary 4.5:1 minimum on the canvas. Raising every accent to 7:1 could compress Loden's visual range; it is a possible accessibility variant, not an automatic improvement to this design. [Modus manual](https://protesilaos.com/emacs/modus-themes)

Ef demonstrates that readable variety can remain warm. Solarized offers disciplined relationships among neutral levels and a strong cohesive identity; its designer also describes extensive display and lighting trials. Those qualities cannot be replaced by a favorable contrast table. Latte and Everforest provide softer, more colorful comparison points, but the sampled light accents have less text contrast than Loden. This does not establish that every port uses those exact roles, weights, or backgrounds. [Solarized design notes](https://ethanschoonover.com/solarized/), [Latte palette](https://github.com/catppuccin/palette/blob/main/palette.json), [Everforest palette](https://github.com/sainnhe/everforest/blob/master/autoload/everforest.vim)

W3C specifies 4.5:1 for ordinary text and 3:1 for qualifying large text. A normal coding font does not become large text merely because a token is bold. The measurements here are pair-level checks, not a claim of full WCAG conformance for an editor. [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

## 3. The highest-priority gap is actual diff composition

The explicit diff pairs are a genuine strength. Addition, deletion, change, hunk, and conflict have dedicated treatments. Inline characters use black, with **9.81:1**, **10.16:1**, and **10.24:1** on the add, delete, and change emphasis fills. GitSigns adds bold and underline. The richer golden changed-line background also separates better from parchment than the previous nearly identical fill.

However, the current upstream Codex diff implementation reads inserted/deleted theme backgrounds while preserving syntax foregrounds in recognized-language code. It also adds a dim modifier to deleted syntax. This makes the editor-canvas accent checks insufficient for that rendering path. The source-derived result is eight of nine accents below 4.5:1 on Loden's added-line background, including ochre numbers at **3.61:1**, sage strings at **3.87:1**, and clay keywords at **3.96:1**. This is based on the upstream source accessed on 2026-09-08, not a screenshot or verification of the installed binary. [Codex diff renderer](https://github.com/openai/codex/blob/main/codex-rs/tui/src/diff_render.rs)

The [composition specimen](diff-overlay.png) makes this pairing visible. It does not simulate deletion dimming, which depends on the host. The generated theme's dedicated dark diff foreground does not protect syntax tokens when a renderer keeps their individual foregrounds.

This is a design issue rather than a request for more integrations: the existing intended application is composing the supplied palette in a way the audit did not model. The next refinement should explicitly support syntax on line-diff fills, either by using a lighter added-line fill or by supplying a faithfully controlled diff foreground path where the host supports one. Preserve stronger inline emphasis and black changed characters. Test the actual result before accepting a new fill.

There is a second, separate diff concern. Inline text contrast and inline span discoverability are different measurements. The emphasis-to-line ratios are only **1.23:1 for addition**, **1.44:1 for deletion**, and **1.60:1 for change**. An added whitespace cell has no glyph to reveal its position; underline therefore matters disproportionately. The [stress specimen](stress-normal.png) compares that cue present and absent. In grayscale the extra line is materially more useful than the slight fill darkening.

These fill ratios are observations, not automatic WCAG failures. Whether a boundary needs 3:1 depends on its role and other identifying information. The practical design requirement is that a reviewer can find the exact changed cell without relying solely on color. [W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

Claude Code's documented theme interface supplies separate line and word-level background tokens, which Loden maps. That establishes an available mechanism, not proof that every changed character is black or that all whitespace spans are exposed in the actual renderer. Native acceptance should include a changed digit, inserted equals sign, replaced operator, leading space, trailing space, and wrapped line. [Claude Code theme documentation](https://code.claude.com/docs/en/terminal-config#custom-themes)

## 4. Black main text should not collapse the ANSI palette

The committed Day palette maps ANSI slots 0, 7, 8, and 15 to exactly `#000000`. Consequently, indexed foreground/background sequences `37;40`, `30;47`, and `97;40` all resolve to **black on black, 1:1** before any host contrast correction. The [stress specimen](stress-normal.png) intentionally contains invisible text in those three rectangles.

SGR selects foreground and background colors from the indexed palette; those entries are not foreground-only semantic tokens. Testing every entry as text on parchment therefore cannot establish general terminal compatibility. [XTerm control sequences](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html)

The correction should preserve black default text while restoring distinct terminal neutral endpoints and checking common combinations. Explicitly colored terminal output may then use a light foreground on a dark background. That is consistent with black as the main foreground and the clarified allowance for other roles. No sixteen-color palette can make every arbitrary foreground/background pair accessible, so the contract must list supported pairs rather than assert universal compatibility.

This is the clearest example of why higher single-background scores can accompany a worse complete system. The earlier audit passed because its ANSI scope was too narrow.

## 5. Secondary hierarchy needs deliberate restoration

All five neutral foreground roles are identical in the committed palette. Fresh resolved Neovim capture also shows `LineNr` and `CursorLineNr` both as black with no distinguishing weight, and `StatusLine` and `StatusLineNC` both as black without an explicit background in those groups. Host layout or a statusline plugin can still distinguish context, but these mappings themselves no longer do so.

The active-line fill has **1.035:1** contrast against the canvas and ΔEOK **0.0122**. Its subtlety is not inherently wrong: a cursorline should not dominate a page. Combined with identical line-number styling, though, it leaves a weak navigation cue. A bold black active line number or another clear marker is preferable to making all chrome more intense.

Comments are black and italic in Neovim. The current upstream Codex syntax converter deliberately suppresses italics and underlining, although it retains bold. Thus the italic comment distinction in controlled previews is not transferable to that renderer. Black comments there depend on punctuation and context alone. [Codex syntax style conversion](https://github.com/openai/codex/blob/main/codex-rs/tui/src/render/highlight.rs)

With the clarified design intent, a readable olive-gray comment/secondary family is available again. It should remain at least 4.5:1 on every surface where it is actually used; an enhanced target around 7:1 can be considered for frequently read secondary text. Muted labels must not be exempted just because they are secondary. Main prose, ordinary identifiers, selection text, and precise changed characters can remain black.

The surface ordering itself is coherent: popup → canvas → active line → surrounding chrome → recessed chrome → structural fill. The closely spaced canvas, active line, and mantle serve different purposes, but their ordering is easier to understand in documentation than to perceive at a glance. Avoid another broad surface redesign until the text and active-state cues have been restored.

Black popup borders are conspicuous in the specimen. Text preference does not require every structural stroke to be black; an appropriate lower-contrast border can be tested independently while retaining sufficient visibility for essential boundaries. This is a visual refinement, subordinate to the diff and ANSI defects.

## 6. Syntax distinction is improved but not uniformly robust

Numbers and keywords now have useful normal-vision separation, with ochre/clay ΔEOK **0.0708**. Dark gold functions also differ from ochre numbers across the simulations: their distance stays around **0.079–0.085**. That is a particularly useful distinction in call-heavy code. These measurements support retaining the current accent direction.

The remaining close pairs are role-specific:

| Pair | Normal | Protan | Deutan | Tritan | Grayscale |
|---|---:|---:|---:|---:|---:|
| Numbers / keywords | 0.0708 | 0.0566 | 0.0302 | 0.0526 | 0.0216 |
| Information / hints | 0.0778 | 0.0663 | 0.0597 | 0.0258 | 0.0098 |
| Strings / types | 0.0444 | 0.0411 | 0.0433 | 0.0470 | 0.0026 |
| Operators / numbers | 0.0360 | 0.0081 | 0.0173 | 0.0458 | 0.0059 |

These are comparative signals rather than universal thresholds. Quotation marks, numeric syntax, and bold keywords provide context; diagnostic severity needs labels or distinct glyphs. The resolved info/hint underlines share the same undercurl style, so their distinguishing property in that treatment is color alone. A plain undercurl without a severity label cannot carry the same promise as a labeled diagnostic message.

The supplied simulations use the Machado model at severity 1, plus grayscale. They help discover vulnerabilities but do not reproduce every person's perception or demonstrate task performance. A robust design combines the measured palette with redundant cues. [Machado, Oliveira and Fernandes, 2009](https://pubmed.ncbi.nlm.nih.gov/19834201/), [W3C use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

Do not widen every pair indiscriminately. Strings and types can remain related greens if they are legible and structurally distinguishable. Information and hints deserve more attention because their meaning can disappear when their hue distinction weakens. A brighter blue is not required; labels and symbols can do more useful work without disrupting the palette.

## 7. What the current validation establishes

The committed reports contain 126 passing contrast checks, six passing internal semantic gates, nine passing regression tests, and 830 resolved Neovim checks. Those are meaningful engineering safeguards. They do not test every composed cell, indexed terminal background, dimmed agent span, or native changed-character calculation.

The independent contrast formula agrees with every committed WCAG gate outcome. Across all unique-position color pairs considered, its largest difference from the library calculation is below **0.000462**. The small numerical difference comes from the library's higher-precision luminance coefficients versus the rounded WCAG coefficients. It does not explain the new failures; missing pair coverage does.

The semantic gate uses the larger distance of foreground or background for certain diff states. That can show that two states retain some distinguishing color information, but it does not measure whether a specific changed character is visible within a line. Likewise, a highlight-definition audit checks available styles, not necessarily their effective composition after syntax, selections, extmarks, and host modifiers.

The new specimens use matched 15 px Berkeley Mono and manually assigned roles. Normal and simulated stress renderings and the code comparison were inspected for readability and layout. They are evidence of palette relationships, not native screenshots. The Ghostty theme also enables font thickening, which the specimens do not reproduce. Live font rendering and prolonged reading remain outside the completed validation.

## 8. Recommended next refinement

1. **Retain the identity:** parchment `#F0E9D2`, black main text, restrained earthy syntax, black selection text, and black precise changed characters.
2. **Fix actual diff pair coverage first:** require supported syntax/line-fill pairs to meet the text target; account for host dimming and verify native exact-span behavior. Keep the strongest emphasis at the changed characters.
3. **Restore ANSI role distinction:** separate default foreground preference from indexed terminal foreground/background semantics. Add common opposite-neutral and colored-status pairs to the audit.
4. **Restore readable secondary roles:** choose a restrained olive-gray family with explicit surface pairings; avoid dimming frequently read agent prose into low contrast. Give active line numbers a non-color distinction.
5. **Validate navigation and semantic cues in use:** verify info versus hint, active versus inactive panes, current versus other search results, and one-character/whitespace diffs with both normal and weakened color cues.

These are targeted corrections. They do not justify replacing the background or making the entire syntax palette brighter, darker, or more colorful.

A practical final acceptance trial should alternate Loden and the preferred Gruvbox Light Soft at the same font size and display brightness, across comparable editing and agent-review sessions. Include ordinary code reading, comment-heavy code, logs, completion menus, dense patches, and tiny dangerous edits. Record missed changed characters, navigation mistakes, and subjective comfort separately. Several sessions can reveal personal fit; they still would not establish universal superiority.

The appropriate present description is **a distinctive, high-contrast light theme with a strong foundation and identifiable remaining defects**. “World class” should remain an aspiration until the diff and terminal counterexamples are corrected and the intended workflows have been exercised.

## Evidence and reproduction

The assessment leaves production colors unchanged. The accepted theme was committed before this report. The new findings qualify the earlier passing audit rather than invalidate its correctly scoped calculations.

```sh
.venv/bin/python scripts/review_world_class.py --png --kanso /path/to/kanso.nvim
```

PNG rendering requires the existing macOS renderer and Berkeley Mono installation. Without `--png`, the script still creates SVGs and measurements. Optional Neovim capture records the Kanso revision and selected resolved groups in the measurements file.

Primary references, accessed 2026-09-08:

- W3C WAI: [Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html), [Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).
- Protesilaos Stavrou: [Modus manual](https://protesilaos.com/emacs/modus-themes), [Ef manual](https://protesilaos.com/emacs/ef-themes), [pinned Ef Day palette](https://github.com/protesilaos/ef-themes/blob/e1f617607a5f0692b398365dcd8412ba1e98ccb3/ef-day-theme.el).
- morhetz: [original Gruvbox palette and role mappings](https://github.com/morhetz/gruvbox/blob/master/colors/gruvbox.vim).
- Ethan Schoonover: [Solarized design and palette](https://ethanschoonover.com/solarized/).
- Catppuccin: [canonical palette](https://github.com/catppuccin/palette/blob/main/palette.json). sainnhe: [Everforest palette](https://github.com/sainnhe/everforest/blob/master/autoload/everforest.vim).
- OpenAI: [Codex diff renderer](https://github.com/openai/codex/blob/main/codex-rs/tui/src/diff_render.rs) and [syntax style conversion](https://github.com/openai/codex/blob/main/codex-rs/tui/src/render/highlight.rs), upstream main as accessed; installed binary not verified.
- Anthropic: [Claude Code terminal/theme documentation](https://code.claude.com/docs/en/terminal-config#custom-themes).
- Thomas Dickey et al.: [XTerm Control Sequences](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html), page updated for patch 411.
- Piepenbrock, Mayr and Buchner: [Positive display polarity is particularly advantageous for small character sizes](https://pubmed.ncbi.nlm.nih.gov/25141597/), Human Factors, 2014.
- Machado, Oliveira and Fernandes: [A physiologically-based model for simulation of color vision deficiency](https://pubmed.ncbi.nlm.nih.gov/19834201/), IEEE TVCG, 2009.
- Repository evidence: [canonical Day palette](../../palette/loden-day.json), [audit](../loden-day-audit.md), [resolved Neovim audit](../day-review/neovim.json), [measurement and rendering script](../../scripts/review_world_class.py).
