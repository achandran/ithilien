# Loden Day design review

The accepted design is **warm parchment `#F0E9D2`, pure-black neutral text, and restrained colored syntax**. This replaces the initial silver-ivory proposal following the user's preference for Gruvbox Light Soft and black foreground text. Changes remain uncommitted.

[Accepted before/after code](../day-adoption/code-normal.png) · [Agent prose and character-level diffs](../day-adoption/agent.png) · [Latest audit](../loden-day-audit.md) · [Original baseline comparison](index.html)

The initial baseline was `1db45d561c403c7ece315e749487fa4d76c0b0cd`, verified against origin HEAD on 2026-09-08. Its palettes match the previously reviewed `c2d3c99`. The starting checkout was clean and contained no applicable AGENTS.md.

## Priorities and final decisions

Excellent diffs, including individual changed characters, and warmth through long coding/agent sessions govern the design. Watch resemblance and favorable palette measurements support those priorities. The Citizen photographs were unavailable; its described dial supplied direction, not measured colors. Flat parchment fills avoid adding texture behind glyphs. Night retains its Formex-inspired palette.

All five neutral foreground roles now map to `#000000`: text, subtext, comment, muted, and bright. The names remain semantic aliases for integrations; they no longer imply a lightness hierarchy. Comments use italics, keywords use bold, and layout supplies additional hierarchy. Neutral ANSI entries (black, white, brightBlack, brightWhite) and diff-context text also use black. Syntax, diagnostics, colored terminal entries, diff-state foregrounds, and inverse status labels retain their semantic colors.

Day functions use dark gold, keywords clay, numbers ochre, strings sage, types aqua, and informational messages blue. The nine accents are unchanged by the final adoption. Codex's Day TextMate mappings now follow those principal Neovim syntax roles; Night's mappings remain unchanged.

## Surface contract

| Token | Color | Purpose | Valid foregrounds |
|---|---|---|---|
| surface0 | `#F7F0DF` | Raised popup, documentation, message card | All neutral text and accents |
| base | `#F0E9D2` | Editor and terminal canvas | All neutral text, accents, and ANSI foregrounds |
| surface1 | `#ECE5D2` | Active line, reference highlight, hover | All neutral text and accents |
| mantle | `#E8E1CD` | Surrounding chrome, message panel, inactive status | All neutral text and accents |
| crust | `#D8D2BE` | Recessed chrome, tab strip | All neutral text; not a syntax canvas |
| surface2 | `#C1BEAC` | Structural fill, scrollbar thumb, status segment | All neutral text; not a syntax canvas |

Lightness order is `surface0 > base > surface1 > mantle > crust > surface2`. The palette audit checks neutral text on every surface, and accents on the four code/message surfaces. Crust/surface2 use text/subtext/bright as representative aliases; regression tests require all five neutral roles to remain black. Unlike the early olive-charcoal experiment, black comments and muted labels are valid on crust and surface2 too.

Essential popup and window boundaries use the neutral foreground. Structural fills and indent guides remain decorative, not 3:1 control boundaries. The warm mantle preserves the existing ochre-selection boundary gate. The active-line fill is subtle; the cursor and active-line number remain important.

## Contrast and semantics

Neutral text, including comments and muted labels, is **17.29:1** on the canvas. Syntax spans **5.18–7.37:1**. Selection and Neovim DiffText use shared ochre `#B17232` with black text, **5.32:1**. A green/light-text selection experiment was rejected in favor of the user's black-text preference and the established interaction identity.

The original close accent pairs improved during the first refinement: ochre/clay 0.040 → 0.071 ΔEOK, aqua/blue 0.040 → 0.078, olive/sage 0.026 → 0.047, clay/coral 0.042 → 0.059. Those gains are retained. They are comparative signals, not accessibility thresholds.

Information/hints and some syntax roles still converge under color-vision simulations. Diagnostics need severity labels or distinct glyphs; diffs retain + / - / ~ markers. Bold keywords and literal grammar distinguish numbers from control flow when hues converge. A palette cannot guarantee those cues if a host or user configuration removes them.

## Diff treatments

Day inline add/delete/change characters are black. Their emphasis fills are `#A1BA77`, `#E2A69B`, and `#D2B16B`, giving **9.81–10.24:1** text contrast. GitSigns inline groups use bold and underline, including for whitespace cells. Their fill-to-line brightness contrast is lower than the old dark-emphasis design, so the extra non-color cue matters.

The changed-line fill is now **`#F4E3AD`**. The old `#F2E8C9` nearly merged with parchment (normal ΔEOK 0.0111); the new fill increases that distance to **0.0440**, while retaining **7.85:1** for its semantic foreground and **3.09:1** for the black-on-ochre DiffText boundary. All existing diff contrast and simulated state-separation gates still pass. A regression test requires at least 0.03 normal-vision changed-line/canvas ΔEOK as a project design floor, not a WCAG rule.

Search, substitution, selected popup metadata, error annotations, tab labels, picker states, and completion borders have explicit valid pairs. Kanso's completion borders no longer accidentally inherit the lighter inline-change background as their foreground. Night keeps its old mappings.

## Comparisons and trade-offs

The [comparison palettes](benchmarks.png) use fixed specimens with representative role assignments, not native screenshots. Their source tokens are in [benchmarks.json](benchmarks.json).

- [Modus Operandi](https://github.com/protesilaos/modus-themes/blob/main/modus-themes.el) remains the demanding contrast benchmark.
- [Ef Day](https://github.com/protesilaos/ef-themes/blob/e1f617607a5f0692b398365dcd8412ba1e98ccb3/ef-day-theme.el) illustrates warm readable variety.
- [Solarized](https://github.com/altercation/solarized), [Latte](https://github.com/catppuccin/palette/blob/main/palette.json), and [Everforest](https://github.com/sainnhe/everforest/blob/master/autoload/everforest.vim) provide surface and accent comparisons.
- [Gruvbox Light Soft](https://github.com/morhetz/gruvbox/blob/master/colors/gruvbox.vim) is the user's comfort reference. Loden's parchment is less yellow and slightly lighter than its original `#F2E5BC` canvas.

The [warmth study](../day-warmth/README.md) and [black-text study](../day-black-text/README.md) preserve historical snapshots. The adopted result uses the parchment surfaces and black neutral text, not fully monochrome syntax. The palette is deliberately high contrast. Warmth describes visual character; it does not establish reduced eye strain or better long-session comfort.

## Validation and reproduction

- 126 Day contrast checks and six existing semantic-separation gates pass.
- Nine regression tests cover contrast gaps, unrounded gates, black neutral and inline foregrounds, surface ordering, generated syntax roles, and changed-line visibility.
- 830 resolved Neovim checks pass against the Kanso revision in [neovim.json](neovim.json). Explicit pairs are checked directly; foreground-only groups use base, with the palette matrix covering surface overlays. Excluded decorative guides, hidden helper glyphs, and internal Neovim sentinels are listed.
- Night's resolved highlights and 13 Night/shared source or generated files remain identical to baseline. Night audit reports gain labeled observations without silently recoloring Night.
- The wallpaper generator reads canonical JSON. The final Day frame is regenerated; Night's decoded pixels are checked separately.
- Matched normal, protan, deutan, tritan, and grayscale specimens show the accepted design. They are controlled renderings, not a claim of native Codex/Claude behavior. Native agent rendering, exhaustive plugin combinations, and long-duration comfort remain untested.

```sh
uv run python scripts/build.py
uv run python -m unittest discover -s tests -v
uv run python scripts/check_neovim.py /path/to/kanso.nvim --baseline /path/to/1db45d5-checkout
uv run python scripts/review_day.py --png
uv run python scripts/review_adoption.py --png
```

PNG export requires macOS and installed Berkeley Mono. SVGs use the same 15 px geometry. [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) supplies normal-text requirements; unrounded ratios determine results. APCA floors and ΔEOK floors are project heuristics. A palette PASS does not certify application WCAG conformance.
