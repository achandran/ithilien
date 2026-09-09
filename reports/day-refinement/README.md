# Loden Day refinement

Loden Day retains **warm parchment `#F0E9D2`, black main text, restrained earthy syntax, and black selected/changed-character text**. This refinement corrects the concrete weaknesses found in the [assessment of `4289246`](../day-deep-dive/README.md), which was committed as `94e7c31` before implementation began.

[Before/after code](code-normal.png) · [Agent prose and precise diffs](agent.png) · [Previously failing compositions](composition.png) · [Measurements](summary.json) · [Current audit](../loden-day-audit.md)

## Design decisions

Black is the principal foreground, not a constraint on every semantic role. Comments and muted labels now use olive-gray `#53594E`, giving **5.95:1** on the canvas. Secondary text uses `#484E43`, giving **7.07:1**. Main text remains **17.29:1**. Comments remain distinguishable in renderers that suppress italics, while explanatory prose remains black.

The nine syntax accents are unchanged. This keeps the established balance of sage strings, clay keywords, dark-gold functions, aqua types, ochre numbers, and restrained blue information. Their canvas contrast remains **5.18–7.37:1**. Increasing color distance indiscriminately would work against the intended restraint.

Diff-line fills are lighter, while their inline emphasis remains stronger. Added lines use `#D5E1CA`; deleted lines use `#F0DCD6`. These support syntax foregrounds when an agent renderer preserves them over the line background. The dedicated deletion foreground changes to `#6B322E`, and the change foreground to `#453510`, preserving the existing diff-state separation gates across all simulations after the line fills became closer in lightness. No separation threshold was reduced.

| Measurement | Before | Refined |
|---|---:|---:|
| Lowest syntax contrast on added lines | 3.61:1 | **4.63:1** |
| Lowest syntax contrast on deleted lines, before host dimming | 4.38:1 | **4.76:1** |
| Lowest syntax contrast on changed lines | 4.92:1 | **4.92:1** |
| Added inline fill against its line | 1.23:1 | **1.58:1** |
| Deleted inline fill against its line | 1.44:1 | **1.57:1** |
| Changed inline fill against its line | 1.60:1 | **1.60:1** |
| Indexed ANSI white on black | 1.00:1 | **17.29:1** |

Inline fill/line ratios describe boundary visibility, not text accessibility thresholds. Black inline text retains **9.81–10.24:1** contrast. Bold and underline identify precise spans, including whitespace. The ochre Neovim DiffText treatment remains black at **5.32:1**, with underline added; its edge against the changed-line fill remains **3.09:1**.

Neovim's `DiffTextAdd` also receives the black, underlined ochre treatment. That group describes unmatched characters relative to another buffer and can occur on either side of a comparison; coloring it green would incorrectly imply a universal addition direction. GitSigns' explicitly directional inline groups retain green/red/gold fills.

The active line number is black and bold, while surrounding line numbers use readable olive-gray. Active and inactive statusline groups now differ in foreground and weight. Current search has bold and underline. Information diagnostics use a straight underline, and hints a dotted underline, adding a non-color distinction. Severity labels or distinct signs remain necessary when the host cannot render those styles.

## Surface contract

The background values and their ordering are unchanged. The new foreground hierarchy does more of the work, keeping the page warm and quiet without making essential text faint.

| Surface | Color | Purpose | Supported text |
|---|---|---|---|
| `surface0` | `#F7F0DF` | Popup/documentation/message card | All neutral roles and syntax accents |
| `base` | `#F0E9D2` | Editor/terminal canvas | All neutral roles and syntax accents; dark ANSI foregrounds |
| `surface1` | `#ECE5D2` | Active line and hover/reference fill | All neutral roles and syntax accents |
| `mantle` | `#E8E1CD` | Surrounding chrome and inactive panels | All neutral roles and syntax accents |
| `crust` | `#D8D2BE` | Recessed chrome/tab strip | All neutral roles |
| `surface2` | `#C1BEAC` | Structural fill/scrollbar/status segment | Main, bright, and secondary text; not comments or muted labels |

Comments and muted labels remain at least **4.78:1** across their supported surfaces, including crust. Secondary text remains **4.59:1** even on surface2. Essential borders use the readable muted foreground rather than black. The active-line fill remains deliberately subtle; the bold active number supplies the stronger navigation cue.

## Terminal and agent behavior

ANSI black stays black. ANSI white is parchment, bright white is pale ivory, and bright black is readable olive-gray. The default terminal foreground remains black. Light ANSI endpoints are intended for dark indexed backgrounds, including colored status backgrounds; they are not supported foregrounds on the parchment canvas without host correction.

This revises the earlier incorrect foreground-only ANSI contract. The audit now checks both neutral directions and light text on the supported dark ANSI backgrounds. The numerical targets are unchanged: ordinary text still needs 4.5:1, with 7:1 for specified enhanced pairs. A finite indexed palette cannot make every possible pairing readable.

The generated Day Ghostty theme adds `faint-opacity = 1` and `minimum-contrast = 4.5`. The first keeps deleted agent text from losing contrast through a faint modifier. The second protects unexpected foreground/background combinations, including light ANSI text emitted onto a light canvas. It can adjust colors in otherwise unsupported combinations; this is an intentional readability safeguard, not a substitute for auditing the designed pairs. Native indexed or RGB text on already compliant surfaces retains the intended palette subject to the renderer. [Ghostty configuration reference](https://ghostty.org/docs/config/reference#minimum-contrast)

The trade-off is that an application cannot use faint opacity alone to distinguish a state in this Day Ghostty theme. Explicit secondary colors, line markers, backgrounds, weight, and layout provide hierarchy instead. Other terminal emulators need equivalent handling or separate validation. These settings do not establish the final rendering of every Codex or Claude version.

## Validation

- **196 contrast checks and six semantic-separation gates pass.** New checks include all neutral/syntax roles on add/delete/change line fills, and light ANSI text on supported dark backgrounds. Added comments/muted checks cover crust explicitly.
- **11 regression tests pass**, including rejection of the previous dark added-line background and the previous black-on-black ANSI endpoint collapse.
- **830 resolved Neovim highlight checks pass**, with assertions for black/underlined diff text, active-number/status distinction, and different info/hint underline styles.
- **Six native Neovim character-diff cases pass** on Neovim 0.12.5: a digit replacement, inserted equals sign, separated changed digits, removed space, trailing space, and replaced operator. The test asserts exact changed columns in both buffers and their black, underlined foreground treatment. [Native results](native-diffs.json)
- The Day Ghostty file passes the installed configuration validator. Palette generation is idempotent, and the preview JavaScript passes syntax validation.
- Night's resolved highlights remain identical to the original baseline. Night/shared theme artifacts and the wallpaper remain byte-identical to the pre-refinement commit. Audit JSON now represents undefined neutral hues with `null` rather than nonstandard `NaN`; this changes metadata, not colors.

The native diff test sets `inline:char` explicitly. A theme does not choose a diff algorithm for an application. Older Neovim versions or `inline:simple` can highlight the entire span between the first and last change; configure character-level diffing where supported to obtain the tested behavior. The theme does not change global `diffopt` on load.

[Protan](code-protan.png) · [Deutan](code-deutan.png) · [Tritan](code-tritan.png) · [Grayscale](code-grayscale.png)

Matched specimens use the same 15 px Berkeley Mono and geometry. They show complete code, comments, diagnostic labels, selection, completion, agent prose, line diffs, and explicit changed-character spans. They are controlled renderings rather than native agent screenshots; the separate Neovim test exercises actual diff computation. Ghostty font thickening is not simulated in these images.

## Remaining trade-offs

Loden now addresses the reproducible palette failures in the deep dive while better matching the clarified preference. It is a stronger and more coherent light theme, particularly for precise diffs and readable agent prose. The work does not prove universal “world-class” status or long-session comfort.

Information/hint and some syntax hues still converge under color-vision simulations; redundant cues remain important. A terminal that cannot display dotted underlines may need severity text or distinct glyphs. The native character tests cover the listed Neovim cases, not every plugin, wrapped Unicode span, or agent diff renderer. Application-computed inline foregrounds must still be verified in the actual Codex/Claude version used.

Keep the current background stable during real-use evaluation. The useful next evidence is whether small changed characters are consistently noticed, comments are easy to read without competing with code, and the palette remains comfortable across comparable coding sessions. Those observations matter more than another round of hex optimization.

## Reproduction

```sh
uv run python scripts/build.py
uv run python -m unittest discover -s tests -v
uv run python scripts/check_neovim.py /path/to/kanso.nvim --baseline /path/to/original-loden
KANSO_ROOT=/path/to/kanso.nvim nvim --headless -u NONE -i NONE -l scripts/check_day_diff.lua
uv run python scripts/review_refinement.py --png
ghostty +validate-config --config-file=/absolute/path/to/loden/ghostty/themes/loden-day
```

PNG export uses the existing macOS renderer and installed Berkeley Mono. Canonical colors live in [palette/loden-day.json](../../palette/loden-day.json); generator logic and Neovim role mappings are the editable sources. No personal application configuration was installed or modified by this refinement.
